"""
Recipe serializerlari — read-only public API uchun.
Til: Accept-Language header + modeltranslation.
"""
from rest_framework import serializers

from apps.products.utils.images import recipe_image_url
from apps.recipes.models.recipes import (
    Recipe,
    RecipeIngredient,
    RecipeStep,
)
from apps.recipes.serializers.allergen import (
    AllergenTagSerializer,
    IngredientLightSerializer,
)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientLightSerializer(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'amount', 'unit']
        read_only_fields = fields


class RecipeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        fields = [
            'id', 'order',
            'description',
            'description_uz', 'description_ru', 'description_en',
        ]
        read_only_fields = fields


class RecipeListSerializer(serializers.ModelSerializer):
    allergen_tags = AllergenTagSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name', 'name_uz', 'name_ru', 'name_en',
            'category',
            'season',
            'prep_time_minutes',
            'calories_per_serving',
            'servings',
            'is_hot',
            'image_url',
            'allergen_tags',
        ]
        read_only_fields = fields

    def get_image_url(self, obj) -> str:
        return recipe_image_url(obj)


class RecipeDetailSerializer(serializers.ModelSerializer):
    allergen_tags = AllergenTagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    steps = RecipeStepSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name', 'name_uz', 'name_ru', 'name_en',
            'description', 'description_uz', 'description_ru', 'description_en',
            'category',
            'season',
            'prep_time_minutes',
            'calories_per_serving',
            'servings',
            'is_hot',
            'image',
            'image_url',
            'allergen_tags',
            'ingredients',
            'steps',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields

    def get_image_url(self, obj) -> str:
        return recipe_image_url(obj)
