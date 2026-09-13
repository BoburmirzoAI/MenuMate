from rest_framework import serializers

from apps.menu.models.menu import Menu, MenuDay, MenuMeal, MenuMealItem
from apps.products.utils.images import recipe_image_url
from apps.recipes.models.recipes import Recipe


class RecipeShortSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name', 'name_uz', 'name_ru', 'name_en',
            'category',
            'prep_time_minutes',
            'calories_per_serving',
            'is_hot',
            'image_url',
        ]
        read_only_fields = fields

    def get_image_url(self, obj) -> str:
        return recipe_image_url(obj)


class MenuMealItemSerializer(serializers.ModelSerializer):
    recipe = RecipeShortSerializer(read_only=True)

    class Meta:
        model = MenuMealItem
        fields = ['id', 'category', 'recipe']
        read_only_fields = fields


class MenuMealSerializer(serializers.ModelSerializer):
    items = MenuMealItemSerializer(many=True, read_only=True)

    class Meta:
        model = MenuMeal
        fields = ['id', 'meal_type', 'items']
        read_only_fields = fields


class MenuDaySerializer(serializers.ModelSerializer):
    meals = MenuMealSerializer(many=True, read_only=True)

    class Meta:
        model = MenuDay
        fields = ['id', 'date', 'is_holiday', 'holiday_name', 'meals']
        read_only_fields = fields


class MenuListSerializer(serializers.ModelSerializer):
    days_count = serializers.IntegerField(source='days.count', read_only=True)

    class Meta:
        model = Menu
        fields = [
            'id', 'start_date', 'end_date',
            'duration', 'status', 'days_count', 'created_at',
        ]
        read_only_fields = fields


class MenuDetailSerializer(serializers.ModelSerializer):
    days = MenuDaySerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = [
            'id', 'start_date', 'end_date',
            'duration', 'status', 'notes',
            'days', 'created_at',
        ]
        read_only_fields = fields


class CreateMenuSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    duration = serializers.ChoiceField(
        choices=Menu.Duration.choices, default=Menu.Duration.WEEKLY,
    )


class AddMealItemSerializer(serializers.Serializer):
    category = serializers.ChoiceField(choices=MenuMealItem.Category.choices)
    recipe_id = serializers.IntegerField()
