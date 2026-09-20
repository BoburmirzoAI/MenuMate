"""Rasm cache'ni oldindan to'ldiruvchi Celery task'lari.

`ingredient_image_url()` va `recipe_image_url()` Wikipedia REST API'siga so'rov
yuboradi va topilgan URL'ni 7 kunga Redis'ga saqlaydi. Cache bo'sh bo'lsa,
har admin sahifa yoki mobile ekran uzoq kutadi.

`warmup_images` — hamma ingredient va retseptlar uchun ushbu funksiyani
oldindan chaqirib qo'yadi. Har suton ishga tushiriladi (CELERY_BEAT_SCHEDULE)
va worker ishga tushganida bir marta (worker_ready signal).
"""
import logging
import time

from celery import shared_task
from celery.signals import worker_ready

from apps.products.utils.images import ingredient_image_url, recipe_image_url
from apps.recipes.models.recipes import Ingredient, Recipe

logger = logging.getLogger(__name__)

_WIKI_REQUEST_DELAY_SEC = 0.35


@shared_task(name='products.warmup_images')
def warmup_images() -> dict[str, int]:
    """Ingredient va retsept rasmlarini Wikipedia'dan oldindan yig'ib qo'yadi.

    Idempotent — cache mavjud bo'lsa qayta so'rov yubormaydi. Har so'rov
    orasida ~0.35s pauza (Wikipedia 429'dan qochish uchun).
    """
    ing_done = ing_missing = 0
    for ing in Ingredient.objects.all().only(
        'id', 'name', 'name_uz', 'name_ru', 'name_en', 'image_url',
    ):
        try:
            url = ingredient_image_url(ing)
        except Exception as exc:
            logger.warning("warmup ingredient %s xato: %s", ing.pk, exc)
            ing_missing += 1
            continue
        if url:
            ing_done += 1
        else:
            ing_missing += 1
        time.sleep(_WIKI_REQUEST_DELAY_SEC)

    rec_done = rec_missing = 0
    for rec in Recipe.objects.all().only(
        'id', 'name', 'name_uz', 'name_ru', 'name_en', 'image_url',
    ):
        try:
            url = recipe_image_url(rec)
        except Exception as exc:
            logger.warning("warmup recipe %s xato: %s", rec.pk, exc)
            rec_missing += 1
            continue
        if url:
            rec_done += 1
        else:
            rec_missing += 1
        time.sleep(_WIKI_REQUEST_DELAY_SEC)

    result = {
        'ingredients_ok': ing_done,
        'ingredients_missing': ing_missing,
        'recipes_ok': rec_done,
        'recipes_missing': rec_missing,
    }
    logger.info("warmup_images tugadi: %s", result)
    return result


@worker_ready.connect
def _warmup_on_worker_start(sender, **_kwargs) -> None:
    """Worker ishga tushganda cache'ni bir marta to'ldirib qo'yamiz.

    Birinchi deploy'da yoki cache tozalangandan keyin bo'sh Redis holatini
    hal qiladi — foydalanuvchi birinchi so'rov yuborganida rasmlar tayyor.
    """
    try:
        warmup_images.apply_async(countdown=30)
    except Exception as exc:
        logger.warning("warmup_images worker_ready'dan ishga tushirilmadi: %s", exc)
