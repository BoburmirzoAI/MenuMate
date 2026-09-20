"""Karzinka Go bilan real integratsiya.

Ikki manba: public catalog.korzinka.uz (223 promo mahsulot, tokensiz) va
Yandex Lavka B2B API (5000+ mahsulot, JWT token bilan). Ingredient bilan
mahsulot moslash nom o'xshashligi (name prefix) bo'yicha ishlaydi.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Iterable

import requests
from django.core.cache import cache
from django.utils import timezone

from apps.products.utils.karzinka_lavka import fetch_all_products

from apps.recipes.models.recipes import Ingredient

logger = logging.getLogger(__name__)

_API_URL = "https://catalog.korzinka.uz/api/catalogs/categories/"
# `:v3` — promotion_end schema o'zgargani sababli eski `:v2` yozuvlari o'qilmaydi.
_CACHE_KEY = "karzinka:catalog:v3"
_CACHE_TTL = 5 * 60
_HTTP_TIMEOUT = 10

# "17.09.2026-23.09.2026" ko'rinishidagi aksiya sanalari uchun regex.
_PROMO_DATE_RANGE_RE = re.compile(
    r'(\d{2})\.(\d{2})\.(\d{4})\s*-\s*(\d{2})\.(\d{2})\.(\d{4})'
)


@dataclass(frozen=True)
class KarzinkaProduct:
    id: int
    title_uz: str
    title_ru: str
    title_en: str
    price: Decimal
    old_price: Decimal | None
    is_discount: bool
    image_url: str
    product_url: str
    weight_param: str
    category_id: int
    in_stock: bool = True
    promotion_end: date | None = None


def _parse_price(raw: object) -> Decimal | None:
    """`"21 990"` yoki `21990` → Decimal(21990)."""
    if raw is None:
        return None
    s = str(raw).replace(' ', '').replace(' ', '')
    if not s:
        return None
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


def _fetch_raw() -> list[dict]:
    """API'dan yangi ma'lumot olib, cache'ga yozadi."""
    try:
        resp = requests.get(_API_URL, timeout=_HTTP_TIMEOUT)
        resp.raise_for_status()
        return resp.json().get("data") or []
    except Exception as e:
        logger.warning("Karzinka fetch failed: %s", e)
        return []


def _fetch_from_lavka() -> list[KarzinkaProduct]:
    """Karzinka Go (Yandex Lavka B2B) API'dan qo'shimcha mahsulotlar.

    Faqat KARZINKA_LAVKA_TOKEN .env'da bo'lsa ishlaydi. Aks holda bo'sh ro'yxat.
    """
    try:
        lavka = fetch_all_products()
    except Exception as e:
        logger.warning("Lavka fetch failed: %s", e)
        return []

    result: list[KarzinkaProduct] = []
    for p in lavka:
        result.append(KarzinkaProduct(
            id=hash(p.id) & 0x7fffffff,
            title_uz=p.title,
            title_ru=p.title,
            title_en=p.subtitle,
            price=p.price,
            old_price=None,
            is_discount=False,
            image_url=p.image_url(400, 400),
            product_url=f"https://korzinka.uz/go",
            weight_param=p.amount,
            category_id=0,
            in_stock=p.available,
            promotion_end=None,
        ))
    return result


def get_catalog() -> list[KarzinkaProduct]:
    """Karzinka mahsulotlarini qaytaradi (cache'dan yoki API'dan).

    Manba tartibi:
    1. Yandex Lavka B2B API (agar token bor bo'lsa) — 5000+ mahsulot
    2. catalog.korzinka.uz ochiq API — 223 promo mahsulot (fallback)
    """
    cached = cache.get(_CACHE_KEY)
    if cached is not None:
        return [_from_cache_dict(p) for p in cached]

    products: list[KarzinkaProduct] = _fetch_from_lavka()

    today = timezone.localdate()
    raw = _fetch_raw()
    for cat in raw:
        for p in cat.get("products") or []:
            price = _parse_price(p.get("prices", {}).get("actual_price"))
            if price is None:
                continue
            promotion_end = _parse_promotion_end(p.get("promotion_tags"))
            products.append(KarzinkaProduct(
                id=p["id"],
                title_uz=p.get("title_uz") or p.get("title") or "",
                title_ru=p.get("title_ru") or "",
                title_en=p.get("title_en") or "",
                price=price,
                old_price=_parse_price(p.get("prices", {}).get("old_price")),
                is_discount=bool(p.get("prices", {}).get("is_discount")),
                image_url=p.get("small_image_url") or "",
                product_url=p.get("product_url") or "",
                weight_param=p.get("weight_param") or "",
                category_id=p.get("catalog_category_id") or 0,
                in_stock=_derive_in_stock(p, promotion_end, today),
                promotion_end=promotion_end,
            ))

    cache.set(
        _CACHE_KEY,
        [{
            "id": p.id, "title_uz": p.title_uz, "title_ru": p.title_ru, "title_en": p.title_en,
            "price": str(p.price),
            "old_price": str(p.old_price) if p.old_price is not None else None,
            "is_discount": p.is_discount, "image_url": p.image_url,
            "product_url": p.product_url, "weight_param": p.weight_param,
            "category_id": p.category_id,
            "in_stock": p.in_stock,
            "promotion_end": p.promotion_end.isoformat() if p.promotion_end else None,
        } for p in products],
        _CACHE_TTL,
    )
    in_stock_count = sum(1 for p in products if p.in_stock)
    logger.info(
        "Karzinka catalog cached: %s products (%s in-stock)",
        len(products), in_stock_count,
    )
    return products


def _from_cache_dict(p: dict) -> KarzinkaProduct:
    """Cache'dagi dict'ni KarzinkaProduct'ga qayta hosil qiladi."""
    promotion_end = None
    raw_end = p.get('promotion_end')
    if raw_end:
        try:
            promotion_end = date.fromisoformat(raw_end)
        except (TypeError, ValueError):
            promotion_end = None
    return KarzinkaProduct(
        id=p['id'],
        title_uz=p['title_uz'],
        title_ru=p['title_ru'],
        title_en=p['title_en'],
        price=Decimal(p['price']),
        old_price=Decimal(p['old_price']) if p.get('old_price') else None,
        is_discount=p.get('is_discount', False),
        image_url=p.get('image_url', ''),
        product_url=p.get('product_url', ''),
        weight_param=p.get('weight_param', ''),
        category_id=p.get('category_id', 0),
        in_stock=p.get('in_stock', True),
        promotion_end=promotion_end,
    )


def _parse_promotion_end(promotion_tags: list | None) -> date | None:
    """`promotion_tags` ro'yxatidan aksiya tugash sanasini oladi.

    Karzinka javobida shunday keladi:
        [{"id": 2, "value": "17.09.2026-23.09.2026"}, {"id": 3, "value": "17"}]
    Bizga faqat `DD.MM.YYYY-DD.MM.YYYY` formatidagi qiymat kerak — oxirgi sana
    aksiyaning tugash kuni sifatida qaytariladi.
    """
    if not promotion_tags:
        return None
    for tag in promotion_tags:
        value = (tag or {}).get('value') if isinstance(tag, dict) else None
        if not isinstance(value, str):
            continue
        m = _PROMO_DATE_RANGE_RE.search(value)
        if not m:
            continue
        try:
            return datetime(int(m.group(6)), int(m.group(5)), int(m.group(4))).date()
        except ValueError:
            continue
    return None


def _derive_in_stock(p: dict, promotion_end: date | None, today: date) -> bool:
    """API javobidan mahsulot mavjudligini aniqlaydi.

    Karzinka public API stock haqida to'g'ridan-to'g'ri ma'lumot bermaydi.
    Tekshirish tartibi:
      1. Agar API'da stock field bo'lsa — o'shani ishlatamiz.
      2. Aks holda `promotion_end` bugundan avval bo'lsa — aksiya tugagan
         hisoblab `False` qaytaramiz (eskirgan taklif ko'rsatilmasin).
      3. Boshqa holatlarda default `True` (eski xatti-harakat).
    """
    for key in ("in_stock", "available", "is_available", "is_in_stock"):
        if key in p:
            return bool(p[key])
    for key in ("is_sold_out", "sold_out", "is_out_of_stock", "out_of_stock"):
        if key in p:
            return not bool(p[key])
    if "stock" in p:
        try:
            return int(p["stock"]) > 0
        except (TypeError, ValueError):
            pass
    status = str(p.get("stock_status") or "").lower()
    if status in {"in_stock", "available", "instock"}:
        return True
    if status in {"out_of_stock", "sold_out", "outofstock"}:
        return False

    if promotion_end is not None and promotion_end < today:
        return False
    return True


def _normalize(text: str) -> str:
    """Nomni o'zaro solishtirish uchun tozalash: kichik harf, ortiqcha bo'shliqlar, harflar."""
    t = text.lower().strip()
    t = re.sub(r"[^a-zа-яё0-9\s'ʻ]", " ", t, flags=re.IGNORECASE)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _tokens(text: str) -> set[str]:
    return {w for w in _normalize(text).split() if len(w) >= 3}


def find_karzinka_match(ingredient: Ingredient) -> KarzinkaProduct | None:
    """Ingredient uchun Karzinka mahsulotini topadi.

    Qattiq qoida: mahsulot nomi ingredient nomi bilan **boshlanishi** kerak.
    Masalan: "Olma" ingredienti → "Olma Jeromin O'zb, kg" ✓, lekin
    "Sabzavotli chips" ✗ (ichida "sabzavot" bo'lsa ham nomdan boshlanmaydi).

    Stock filtri: agar biror nomga bir nechta mahsulot mos kelsa,
    **avval in_stock=True** bo'lganini qaytaramiz. Faqat tugagan (in_stock=False)
    variantlar bo'lsa ham qaytariladi — mobile UI kerak bo'lsa "tugagan" belgisi
    ko'rsatishi mumkin. Aks holda hech nima topilmasa None qaytadi.
    """
    names = [
        _normalize(ingredient.name_uz or ""),
        _normalize(ingredient.name_ru or ""),
        _normalize(ingredient.name_en or ""),
        _normalize(ingredient.name),
    ]
    names = [n for n in names if n and len(n) >= 3]
    if not names:
        return None

    fallback: KarzinkaProduct | None = None
    for product in get_catalog():
        for text in (product.title_uz, product.title_ru, product.title_en):
            if not text:
                continue
            normalized = _normalize(text)
            for name in names:
                if normalized == name or normalized.startswith(name + " "):
                    if product.in_stock:
                        return product
                    if fallback is None:
                        fallback = product
                    break
    return fallback


def match_ingredients(ingredients: Iterable[Ingredient]) -> dict[int, KarzinkaProduct]:
    """Ingredient id → mos Karzinka mahsuloti (topilganlari)."""
    result: dict[int, KarzinkaProduct] = {}
    for ing in ingredients:
        match = find_karzinka_match(ing)
        if match is not None:
            result[ing.id] = match
    return result
