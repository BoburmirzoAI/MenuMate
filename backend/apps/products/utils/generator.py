"""Menyu asosida xarid ro'yxati generatsiyasi (ingredientlar bo'yicha jamlash)."""
import logging
from decimal import Decimal
from typing import Dict, Tuple

from django.db import transaction

from apps.menu.models.menu import Menu, MenuMealItem
from apps.products.models.products import ShoppingItem, ShoppingList

logger = logging.getLogger(__name__)

# Vaznlar → gramm; suyuqliklar → millilitr; qoshiqlar → millilitr.
UNIT_TO_BASE = {
    'g': ('g', Decimal(1)),
    'kg': ('g', Decimal(1000)),
    'ml': ('ml', Decimal(1)),
    'l': ('ml', Decimal(1000)),
    'pcs': ('pcs', Decimal(1)),
    'tsp': ('ml', Decimal(5)),
    'tbsp': ('ml', Decimal(15)),
}


def _to_base_unit(amount: Decimal, unit: str) -> Tuple[Decimal, str]:
    if unit not in UNIT_TO_BASE:
        return amount, unit
    base_unit, coef = UNIT_TO_BASE[unit]
    return amount * coef, base_unit


def _to_display_unit(amount: Decimal, base_unit: str) -> Tuple[Decimal, str]:
    if base_unit == 'g' and amount >= 1000:
        return (amount / Decimal(1000)).quantize(Decimal('0.01')), 'kg'
    if base_unit == 'ml' and amount >= 1000:
        return (amount / Decimal(1000)).quantize(Decimal('0.01')), 'l'
    return amount.quantize(Decimal('0.01')), base_unit


@transaction.atomic
def generate_shopping_list(menu: Menu) -> ShoppingList:
    family = menu.family
    members_count = family.members.count() or 1

    items = MenuMealItem.objects.filter(meal__day__menu=menu).select_related(
        'recipe',
    ).prefetch_related('recipe__ingredients__ingredient')

    totals: Dict[int, Tuple[Decimal, str]] = {}
    for item in items:
        recipe = item.recipe
        servings = recipe.servings or 1
        for ri in recipe.ingredients.all():
            per_person = Decimal(ri.amount) / Decimal(servings)
            total = per_person * Decimal(members_count)
            base_amount, base_unit = _to_base_unit(total, ri.unit)

            if ri.ingredient_id in totals:
                prev_amount, prev_unit = totals[ri.ingredient_id]
                if prev_unit == base_unit:
                    totals[ri.ingredient_id] = (prev_amount + base_amount, base_unit)
                else:
                    logger.warning(
                        "Unit mismatch for ingredient %s: %s vs %s",
                        ri.ingredient_id, prev_unit, base_unit,
                    )
            else:
                totals[ri.ingredient_id] = (base_amount, base_unit)

    shopping_list, _ = ShoppingList.objects.get_or_create(menu=menu)
    shopping_list.items.all().delete()

    for ingredient_id, (amount, base_unit) in totals.items():
        display_amount, display_unit = _to_display_unit(amount, base_unit)
        ShoppingItem.objects.create(
            shopping_list=shopping_list,
            ingredient_id=ingredient_id,
            total_amount=display_amount,
            unit=display_unit,
        )

    logger.info(
        "Shopping list generated: menu=%s, items=%s, members=%s",
        menu.id, len(totals), members_count,
    )
    return shopping_list
