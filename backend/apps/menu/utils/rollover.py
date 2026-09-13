"""Tugagan menyu → COMPLETED, yangi menyu (nusxa) yaratish."""
from datetime import date, timedelta

from django.db import transaction

from apps.menu.models.menu import Menu, MenuDay, MenuMeal, MenuMealItem
from apps.menu.utils.builder import DURATION_DAYS
from apps.menu.utils.holidays import annotate_day, holiday_map_for_year
from apps.notifications.models.notifications import Notification


@transaction.atomic
def roll_over_menu(menu: Menu) -> Menu:
    """Tugagan menyudan yangi menyu yaratadi (slot va itemlarni nusxa qilib)."""
    menu.status = Menu.Status.COMPLETED
    menu.save(update_fields=['status'])

    days_count = DURATION_DAYS[menu.duration]
    new_start = menu.end_date + timedelta(days=1)
    new_end = new_start + timedelta(days=days_count - 1)

    new_menu = Menu.objects.create(
        family=menu.family,
        start_date=new_start,
        end_date=new_end,
        duration=menu.duration,
        status=Menu.Status.ACTIVE,
    )

    old_days = list(menu.days.order_by('date').prefetch_related('meals__items'))
    holidays = holiday_map_for_year(new_start.year)
    for offset, old_day in enumerate(old_days):
        d = new_start + timedelta(days=offset)
        is_hol, hol_name = annotate_day(d, holidays)
        new_day = MenuDay.objects.create(
            menu=new_menu, date=d,
            is_holiday=is_hol, holiday_name=hol_name,
        )
        for old_meal in old_day.meals.all():
            new_meal = MenuMeal.objects.create(
                day=new_day, meal_type=old_meal.meal_type,
            )
            MenuMealItem.objects.bulk_create([
                MenuMealItem(
                    meal=new_meal, category=it.category, recipe_id=it.recipe_id,
                )
                for it in old_meal.items.all()
            ])

    Notification.objects.create(
        user=menu.family.user,
        kind=Notification.Kind.MENU,
        title="Yangi hafta menyusi tayyor",
        body=(
            "Oldingi menyu tugadi. Yangi menyu avtomatik yaratildi — "
            "kerak bo'lsa o'zgartirishingiz mumkin."
        ),
    )

    return new_menu


def roll_over_completed_menus(today: date | None = None) -> int:
    today = today or date.today()
    expired = Menu.objects.filter(status=Menu.Status.ACTIVE, end_date__lt=today)
    count = 0
    for menu in expired:
        roll_over_menu(menu)
        count += 1
    return count
