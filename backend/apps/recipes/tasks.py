"""Celery tasks — dastlabki ma'lumotlarni bazaga yuklash.

Task beruvchi `docker compose up` qilsa:
1. `migrate` ishlaydi — jadvallar tuziladi (bo'sh)
2. Celery worker ishga tushadi
3. `worker_ready` signal `seed_initial_data`'ni chaqiradi
4. Task bazaga fixtures yuklaydi (agar bo'sh bo'lsa) — retseptlar/ingredientlar keladi

Idempotent: fixtures faqat bo'sh bazaga yuklanadi. Qayta ishga tushirsa — qaytamaydi.
"""
import logging

from celery import shared_task
from celery.signals import worker_ready
from django.core.management import call_command

logger = logging.getLogger(__name__)

_FIXTURES = [
    'allergen_tags',
    'ingredients',
    'recipes',
    'recipe_ingredients',
    'recipe_steps',
]


@shared_task(name='recipes.seed_initial_data')
def seed_initial_data() -> str:
    """Bazadagi retseptlar bo'sh bo'lsa — fixtures'ni yuklaydi.

    Idempotent: mavjud ma'lumotlarni buzmasdan, faqat bo'sh jadvallarni to'ldiradi.
    """
    from apps.recipes.models.recipes import Recipe

    if Recipe.objects.exists():
        logger.info("Seed: retseptlar mavjud, o'tkazib yuborildi")
        return "already seeded"

    for name in _FIXTURES:
        try:
            call_command('loaddata', name, verbosity=0)
            logger.info("Seed: %s yuklandi", name)
        except Exception as e:
            logger.error("Seed: %s yuklashda xato: %s", name, e)

    count = Recipe.objects.count()
    logger.info("Seed: %s retsept yuklandi", count)
    return f"seeded {count} recipes"


@worker_ready.connect
def _on_worker_ready(sender, **kwargs):
    """Celery worker ishga tushishi bilan seed'ni ishga tushirish."""
    try:
        seed_initial_data.delay()
    except Exception as e:
        logger.warning("Seed task jo'natilmadi: %s", e)
