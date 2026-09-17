"""Admin: Xarid ro'yxatlari."""
from rest_framework import serializers

from apps.products.models.products import ShoppingItem, ShoppingList
from apps.products.utils.images import ingredient_image_url


class ShoppingItemAdminSerializer(serializers.ModelSerializer):
    ingredient_id = serializers.IntegerField(source='ingredient.id', read_only=True)
    ingredient_name = serializers.CharField(source='ingredient.name_uz', read_only=True)
    category = serializers.CharField(source='ingredient.category', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingItem
        fields = [
            'id',
            'ingredient_id', 'ingredient_name', 'category', 'image_url',
            'total_amount', 'unit',
            'is_purchased',
        ]

    def get_image_url(self, obj) -> str:
        return ingredient_image_url(obj.ingredient)


class ShoppingListAdminSerializer(serializers.ModelSerializer):
    menu_id = serializers.IntegerField(source='menu.id', read_only=True)
    family_name = serializers.CharField(source='menu.family.family_name', read_only=True)
    start_date = serializers.DateField(source='menu.start_date', read_only=True)
    end_date = serializers.DateField(source='menu.end_date', read_only=True)
    items = ShoppingItemAdminSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingList
        fields = [
            'id',
            'menu_id', 'family_name',
            'start_date', 'end_date',
            'total_estimated_cost',
            'items',
        ]
