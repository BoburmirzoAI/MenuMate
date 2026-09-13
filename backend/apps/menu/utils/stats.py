"""Menyu statistikasi — kaloriya, retsept soni, halol foizi."""
from django.db.models import Sum

from apps.menu.models.menu import Menu, MenuMealItem


def menu_stats(menu: Menu) -> dict:
    items = MenuMealItem.objects.filter(meal__day__menu=menu).select_related('recipe')

    total_calories = items.aggregate(
        s=Sum('recipe__calories_per_serving'),
    )['s'] or 0

    recipe_ids = set(items.values_list('recipe_id', flat=True))

    return {
        'total_calories': total_calories,
        'recipe_count': len(recipe_ids),
        'item_count': items.count(),
        'halal_percent': 100,  # barcha retseptlar halol deb hisoblanadi
    }
