"""Menyu Celery tasklari."""
import logging

from celery import shared_task

from apps.menu.utils.rollover import roll_over_completed_menus

logger = logging.getLogger(__name__)


@shared_task(name='menu.roll_over_menus')
def roll_over_menus():
    """Tugagan menyularni COMPLETED qiladi va nusxa yaratadi."""
    count = roll_over_completed_menus()
    logger.info("Rolled over %s menus", count)
    return count
