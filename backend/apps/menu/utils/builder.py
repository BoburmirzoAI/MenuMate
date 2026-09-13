"""Bo'sh menyu yaratish (kunlar + slotlar) va tozalash."""
from datetime import date, timedelta

from django.db import transaction

from apps.family.models.family import FamilyProfile
from apps.menu.models.menu import Menu, MenuDay, MenuMeal, MenuMealItem
from apps.menu.utils.holidays import annotate_day, holiday_map_for_year

DURATION_DAYS = {
    Menu.Duration.WEEKLY: 7,
    Menu.Duration.MONTHLY: 30,
}

_MEAL_TYPES = [
    MenuMeal.MealType.BREAKFAST,
    MenuMeal.MealType.LUNCH,
    MenuMeal.MealType.DINNER,
]


@transaction.atomic
def create_empty_menu(family: FamilyProfile, start_date: date, duration: str) -> Menu:
    days_count = DURATION_DAYS[duration]
    end_date = start_date + timedelta(days=days_count - 1)

    menu = Menu.objects.create(
        family=family,
        start_date=start_date,
        end_date=end_date,
        duration=duration,
        status=Menu.Status.ACTIVE,
    )

    holidays = holiday_map_for_year(start_date.year)
    for offset in range(days_count):
        d = start_date + timedelta(days=offset)
        is_hol, hol_name = annotate_day(d, holidays)
        day = MenuDay.objects.create(
            menu=menu, date=d, is_holiday=is_hol, holiday_name=hol_name,
        )
        MenuMeal.objects.bulk_create(
            [MenuMeal(day=day, meal_type=mt) for mt in _MEAL_TYPES]
        )

    return menu


@transaction.atomic
def clear_menu(menu: Menu) -> None:
    MenuMealItem.objects.filter(meal__day__menu=menu).delete()
