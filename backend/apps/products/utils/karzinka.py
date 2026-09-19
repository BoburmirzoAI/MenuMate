"""Karzinka Go bilan real integratsiya.

Ochiq API: https://catalog.korzinka.uz/api/catalogs/categories/
- API key kerak emas.
- Har mahsulotda: nom (3 tilda), narx, rasm, product_url (deep link).
- Cache Redis'da 60 daqiqa saqlanadi — Karzinka'ga ortiqcha yuk bermaymiz.

Ingredient bilan Karzinka product moslash (matching) — nom o'xshashligi bo'yicha.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Iterable

import requests
from django.core.cache import cache

from apps.products.utils.karzinka_lavka import fetch_all_products

from apps.recipes.models.recipes import Ingredient

logger = logging.getLogger(__name__)

_API_URL = "https://catalog.korzinka.uz/api/catalogs/categories/"
_CACHE_KEY = "karzinka:catalog:v1"
_CACHE_TTL = 60 * 60  # 1 soat
_HTTP_TIMEOUT = 10


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
        return [KarzinkaProduct(
            **{**p,
               'price': Decimal(p['price']),
               'old_price': Decimal(p['old_price']) if p.get('old_price') else None}
        ) for p in cached]

    products: list[KarzinkaProduct] = _fetch_from_lavka()

    raw = _fetch_raw()
    for cat in raw:
        for p in cat.get("products") or []:
            price = _parse_price(p.get("prices", {}).get("actual_price"))
            if price is None:
                continue
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
            ))

    # Cache saqlab qo'yamiz — dataclass'ni dict shakliga o'girib.
    cache.set(
        _CACHE_KEY,
        [{
            "id": p.id, "title_uz": p.title_uz, "title_ru": p.title_ru, "title_en": p.title_en,
            "price": str(p.price),
            "old_price": str(p.old_price) if p.old_price is not None else None,
            "is_discount": p.is_discount, "image_url": p.image_url,
            "product_url": p.product_url, "weight_param": p.weight_param,
            "category_id": p.category_id,
        } for p in products],
        _CACHE_TTL,
    )
    logger.info("Karzinka catalog cached: %s products", len(products))
    return products


# ---------------------------------------------------------------------------
# Ingredient ↔ Karzinka product matching
# ---------------------------------------------------------------------------

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
    """
    names = [
        _normalize(ingredient.name_uz or ""),
        _normalize(ingredient.name_ru or ""),
        _normalize(ingredient.name_en or ""),
        _normalize(ingredient.name),
    ]
    # Bo'sh yoki juda qisqa nomlarni tashlaymiz
    names = [n for n in names if n and len(n) >= 3]
    if not names:
        return None

    for product in get_catalog():
        for text in (product.title_uz, product.title_ru, product.title_en):
            if not text:
                continue
            normalized = _normalize(text)
            for name in names:
                # Nom mahsulotning boshida turgan bo'lishi kerak
                if normalized == name or normalized.startswith(name + " "):
                    return product
    return None


def match_ingredients(ingredients: Iterable[Ingredient]) -> dict[int, KarzinkaProduct]:
    """Ingredient id → mos Karzinka mahsuloti (topilganlari)."""
    result: dict[int, KarzinkaProduct] = {}
    for ing in ingredients:
        match = find_karzinka_match(ing)
        if match is not None:
            result[ing.id] = match
    return result
