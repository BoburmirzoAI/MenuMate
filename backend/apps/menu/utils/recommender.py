"""Menu slot uchun retsept tavsiya qilish."""
from django.db.models import Count, Q, QuerySet

from apps.family.models.family import FamilyProfile
from apps.menu.models.menu import MenuMeal, MenuMealItem
from apps.recipes.models.recipes import Recipe

# Slot kategoriyasi (MAIN/SOUP/…) → Recipe kategoriyalari.
# MAIN har uch mahalda o'zining recipe.category si bilan mos keladi.
_CATEGORY_MAP = {
    MenuMealItem.Category.SOUP: [Recipe.Category.SOUP],
    MenuMealItem.Category.SALAD: [Recipe.Category.SALAD],
    MenuMealItem.Category.DRINK: [Recipe.Category.DRINK],
    MenuMealItem.Category.BREAD: [Recipe.Category.BREAD],
    MenuMealItem.Category.DESSERT: [Recipe.Category.DESSERT],
}

_MAIN_FOR_MEAL = {
    MenuMeal.MealType.BREAKFAST: [
        Recipe.Category.BREAKFAST, Recipe.Category.SNACK,
    ],
    MenuMeal.MealType.LUNCH: [Recipe.Category.LUNCH],
    MenuMeal.MealType.DINNER: [Recipe.Category.DINNER],
}


def _recipe_categories(meal_type: str, item_category: str) -> list[str]:
    if item_category == MenuMealItem.Category.MAIN:
        return _MAIN_FOR_MEAL[meal_type]
    return _CATEGORY_MAP[item_category]


def recommend_recipes(
    family: FamilyProfile, meal: MenuMeal, item_category: str,
) -> QuerySet[Recipe]:
    """Slot uchun mos retseptlar — allergiya/yoqmaydiganlarni chiqarib tashlab."""
    categories = _recipe_categories(meal.meal_type, item_category)

    members = family.members.all()
    allergen_ingredient_ids = set()
    disliked_recipe_ids = set()
    liked_recipe_ids = set()
    for m in members:
        allergen_ingredient_ids.update(m.allergen_ingredients.values_list('id', flat=True))
        disliked_recipe_ids.update(m.disliked_recipes.values_list('id', flat=True))
        liked_recipe_ids.update(m.liked_recipes.values_list('id', flat=True))

    qs = Recipe.objects.filter(category__in=categories)
    if disliked_recipe_ids:
        qs = qs.exclude(id__in=disliked_recipe_ids)
    if allergen_ingredient_ids:
        qs = qs.exclude(ingredients__ingredient_id__in=allergen_ingredient_ids)

    # Yoqadigan retseptlarga bonus — birinchi tartibda chiqadi
    qs = qs.annotate(
        like_score=Count('id', filter=Q(id__in=liked_recipe_ids)),
    ).order_by('-like_score', 'name_uz').distinct()

    return qs
