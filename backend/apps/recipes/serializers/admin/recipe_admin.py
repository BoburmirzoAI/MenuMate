"""Admin: retseptlar, ingredientlar, allergenlar."""
from rest_framework import serializers

from apps.products.utils.images import ingredient_image_url, recipe_image_url
from apps.recipes.models.recipes import AllergenTag, Ingredient, Recipe


class AllergenTagAdminSerializer(serializers.ModelSerializer):
    code = serializers.CharField(source='slug', read_only=True)
    icon = serializers.SerializerMethodField()

    class Meta:
        model = AllergenTag
        fields = ['id', 'name', 'name_uz', 'name_ru', 'name_en', 'code', 'icon']

    def get_icon(self, obj) -> str:
        emoji_map = {
            'dairy': '🥛', 'egg': '🥚', 'gluten': '🌾', 'nuts': '🥜',
            'peanut': '🥜', 'shellfish': '🦐', 'fish': '🐟', 'soy': '🌱',
            'sesame': '🌰', 'sulfite': '🍷', 'mustard': '🌿',
        }
        return emoji_map.get((obj.slug or '').lower(), '⚠️')


class IngredientAdminSerializer(serializers.ModelSerializer):
    """Ro'yxat + read uchun — dinamik rasm."""
    image_url = serializers.SerializerMethodField()
    unit = serializers.CharField(source='default_unit', read_only=True)

    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name', 'name_uz', 'name_ru', 'name_en',
            'category', 'unit',
            'image_url',
        ]

    def get_image_url(self, obj) -> str:
        return ingredient_image_url(obj)


class IngredientWritableSerializer(serializers.ModelSerializer):
    """CREATE/UPDATE — 3 tilli nom + kategoriya + birlik."""
    allergen_tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=AllergenTag.objects.all(),
        source='allergen_tags',
        required=False,
        write_only=True,
    )

    class Meta:
        model = Ingredient
        fields = [
            'name', 'name_uz', 'name_ru', 'name_en',
            'category',
            'default_unit',
            'image_url',
            'allergen_tag_ids',
        ]


class RecipeAdminListSerializer(serializers.ModelSerializer):
    """Grid uchun karta ma'lumotlari + rasm."""
    image_url = serializers.SerializerMethodField()
    allergen_tags = AllergenTagAdminSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name', 'name_uz', 'name_ru', 'name_en',
            'category', 'season',
            'prep_time_minutes', 'calories_per_serving',
            'servings',
            'is_hot',
            'image_url',
            'allergen_tags',
        ]

    def get_image_url(self, obj) -> str:
        return recipe_image_url(obj)


class RecipeAdminDetailSerializer(RecipeAdminListSerializer):
    class Meta(RecipeAdminListSerializer.Meta):
        fields = RecipeAdminListSerializer.Meta.fields + [
            'description', 'description_uz', 'description_ru', 'description_en',
        ]


class RecipeWritableSerializer(serializers.ModelSerializer):
    """CREATE/UPDATE — 3 tilli nom va tavsif + allergenlar."""
    allergen_tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=AllergenTag.objects.all(),
        source='allergen_tags',
        required=False,
        write_only=True,
    )

    class Meta:
        model = Recipe
        fields = [
            'name', 'name_uz', 'name_ru', 'name_en',
            'description', 'description_uz', 'description_ru', 'description_en',
            'category', 'season',
            'prep_time_minutes',
            'calories_per_serving',
            'servings',
            'is_hot',
            'image_url',
            'allergen_tag_ids',
        ]


class AllergenTagWritableSerializer(serializers.ModelSerializer):
    """CREATE/UPDATE Allergen — slug bilan."""

    class Meta:
        model = AllergenTag
        fields = ['name', 'name_uz', 'name_ru', 'name_en', 'slug']
