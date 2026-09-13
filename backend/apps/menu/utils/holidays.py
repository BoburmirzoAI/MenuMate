"""Menyu kunlariga bayram belgisini qo'yish."""
from datetime import date

from apps.notifications.models.notifications import Holiday


def holiday_map_for_year(year: int) -> dict[tuple[int, int], str]:
    """(month, day) → holiday name — bir yilgi barcha bayramlar."""
    return {
        (h.month, h.day): h.name for h in Holiday.objects.all()
    }


def annotate_day(day_date: date, holidays: dict[tuple[int, int], str]) -> tuple[bool, str]:
    name = holidays.get((day_date.month, day_date.day))
    return (bool(name), name or '')
