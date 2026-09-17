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
