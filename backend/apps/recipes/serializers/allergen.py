"""
Allergen va Ingredient serializerlari.
Til `Accept-Language` header'dan aniqlanadi (LocaleMiddleware + modeltranslation).
"""
from rest_framework import serializers

from apps.products.utils.images import ingredient_image_url
from apps.recipes.models.recipes import AllergenTag, Ingredient


class AllergenTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllergenTag
        fields = ['id', 'slug', 'name', 'name_uz', 'name_ru', 'name_en']
        read_only_fields = fields


class IngredientSerializer(serializers.ModelSerializer):
    allergen_tags = AllergenTagSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name', 'name_uz', 'name_ru', 'name_en',
            'category',
            'default_unit',
            'image_url',
            'allergen_tags',
        ]
        read_only_fields = fields

    def get_image_url(self, obj) -> str:
        return ingredient_image_url(obj)


class IngredientLightSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name', 'name_uz', 'name_ru', 'name_en',
            'category', 'default_unit',
            'image_url',
        ]
        read_only_fields = fields

    def get_image_url(self, obj) -> str:
        return ingredient_image_url(obj)
