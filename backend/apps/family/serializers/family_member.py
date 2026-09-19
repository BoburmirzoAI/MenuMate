"""
FamilyMember serializerlari.

Cross-app M2M (recipes.Recipe, recipes.Ingredient, family.HealthCondition)
va validation control kerak → plain Serializer + explicit save.

Response uchun alohida ReadSerializer (nested view).
"""
from django.db import transaction
from rest_framework import serializers

from apps.family.models.family import FamilyMember, HealthCondition
from apps.family.serializers.health_condition import HealthConditionSerializer
from apps.recipes.models.recipes import Ingredient, Recipe
from apps.shared.exceptions.custom_exceptions import CustomException


# ---------------------------------------------------------------------
# Read serializer — response uchun
# ---------------------------------------------------------------------

class NestedIngredientSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    name_uz = serializers.CharField()
    name_ru = serializers.CharField()
    name_en = serializers.CharField()
    category = serializers.CharField()


class NestedRecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    name_uz = serializers.CharField()
    name_ru = serializers.CharField()
    name_en = serializers.CharField()
    category = serializers.CharField()


class FamilyMemberReadSerializer(serializers.ModelSerializer):
    """Response strukturasi. M2M'lar nested ko'rinishida."""
    health_conditions = HealthConditionSerializer(many=True, read_only=True)
    liked_recipes = NestedRecipeSerializer(many=True, read_only=True)
    disliked_recipes = NestedRecipeSerializer(many=True, read_only=True)
    allergen_ingredients = NestedIngredientSerializer(many=True, read_only=True)

    class Meta:
        model = FamilyMember
        fields = [
            'id',
            'name', 'age', 'gender',
            'liked_recipes',
            'disliked_recipes',
            'health_conditions',
            'allergen_ingredients',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields


# ---------------------------------------------------------------------
# Write serializer — create / update
# ---------------------------------------------------------------------

class FamilyMemberWriteSerializer(serializers.Serializer):
    """
    A'zo yaratish/yangilash. M2M ID list sifatida qabul qilinadi.
    IDlarning validligini o'zi tekshiradi va aniq xato qaytaradi.
    """
    name = serializers.CharField(max_length=100)
    age = serializers.IntegerField(min_value=0, max_value=120)
    gender = serializers.ChoiceField(choices=FamilyMember.Gender.choices)

    liked_recipe_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, default=list,
    )
    disliked_recipe_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, default=list,
    )
    health_condition_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, default=list,
    )
    allergen_ingredient_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, default=list,
    )

    # ---- Validators ----

    def validate_name(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise CustomException(
                "VALIDATION_ERROR",
                errors={"name": "Ism bo'sh bo'lmasligi kerak"},
            )
        return value

    def validate_health_condition_ids(self, ids: list) -> list:
        if not ids:
            return ids
        existing = set(
            HealthCondition.objects.filter(id__in=ids).values_list('id', flat=True)
        )
        missing = [i for i in ids if i not in existing]
        if missing:
            raise CustomException(
                "HEALTH_CONDITION_NOT_FOUND",
                status_code=400,
                context={"ids": missing},
                errors={"health_condition_ids": missing},
            )
        return ids

    def validate_liked_recipe_ids(self, ids):
        return self._validate_recipe_ids(ids, "liked_recipe_ids")

    def validate_disliked_recipe_ids(self, ids):
        return self._validate_recipe_ids(ids, "disliked_recipe_ids")

    def validate_allergen_ingredient_ids(self, ids: list) -> list:
        if not ids:
            return ids
        existing = set(
            Ingredient.objects.filter(id__in=ids).values_list('id', flat=True)
        )
        missing = [i for i in ids if i not in existing]
        if missing:
            raise CustomException(
                "INGREDIENT_NOT_FOUND",
                status_code=400,
                context={"ids": missing},
                errors={"allergen_ingredient_ids": missing},
            )
        return ids

    @staticmethod
    def _validate_recipe_ids(ids: list, field_name: str) -> list:
        if not ids:
            return ids
        existing = set(
            Recipe.objects.filter(id__in=ids).values_list('id', flat=True)
        )
        missing = [i for i in ids if i not in existing]
        if missing:
            raise CustomException(
                "RECIPE_NOT_FOUND",
                status_code=400,
                context={"ids": missing},
                errors={field_name: missing},
            )
        return ids

    def validate(self, attrs):
        liked = set(attrs.get('liked_recipe_ids', []))
        disliked = set(attrs.get('disliked_recipe_ids', []))
        conflict = liked & disliked
        if conflict:
            raise CustomException(
                "RECIPE_LIKE_DISLIKE_CONFLICT",
                status_code=400,
                context={"ids": list(conflict)},
                errors={"liked_recipe_ids": list(conflict)},
            )
        return attrs

    # ---- Save ----

    @transaction.atomic
    def create(self, validated_data):
        family = self.context['family']
        liked = validated_data.pop('liked_recipe_ids', [])
        disliked = validated_data.pop('disliked_recipe_ids', [])
        health = validated_data.pop('health_condition_ids', [])
        allergens = validated_data.pop('allergen_ingredient_ids', [])

        member = FamilyMember.objects.create(family=family, **validated_data)
        self._set_m2m(member, liked, disliked, health, allergens)
        return member

    @transaction.atomic
    def update(self, instance, validated_data):
        # Scalar fields
        for field in ('name', 'age', 'gender'):
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()

        # M2M — faqat request'da yuborilgan bo'lsa update qilinadi
        m2m_updates = {
            'liked_recipes': validated_data.get('liked_recipe_ids'),
            'disliked_recipes': validated_data.get('disliked_recipe_ids'),
            'health_conditions': validated_data.get('health_condition_ids'),
            'allergen_ingredients': validated_data.get('allergen_ingredient_ids'),
        }
        for attr, ids in m2m_updates.items():
            if ids is not None:
                getattr(instance, attr).set(ids)
        return instance

    @staticmethod
    def _set_m2m(member, liked, disliked, health, allergens):
        if liked:
            member.liked_recipes.set(liked)
        if disliked:
            member.disliked_recipes.set(disliked)
        if health:
            member.health_conditions.set(health)
        if allergens:
            member.allergen_ingredients.set(allergens)
