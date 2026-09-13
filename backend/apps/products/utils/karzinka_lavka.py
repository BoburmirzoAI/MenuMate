"""Karzinka Go (Yandex Lavka B2B) API klienti.

Bu endpoint Karzinka Go mobil ilovasining ichida ishlatiladi. Ochiq API emas —
Proxyman orqali aniqlangan. JWT token 1 soatda tugaydi; `.env`'da yangilaymiz.

Endpoint: POST /4.0/eda-superapp/lavka/v1/api/v2/modes/category
- Kategoriya ID beriladi → o'sha kategoriyaning mahsulotlari ro'yxati keladi.
- Butun katalog uchun barcha kategoriya ID'lari kerak (get_category_group orqali).
"""
from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

_BASE = "https://grocery-b2b-authproxy-ng.lavka.yandex.net/4.0/eda-superapp/lavka/v1"
_URL_CATEGORY = f"{_BASE}/api/v2/modes/category"
_URL_CATEGORY_GROUP = f"{_BASE}/api/v1/category-group"
_URL_PRODUCT = f"{_BASE}/api/v1/product"

_CACHE_TTL = 60 * 30  # 30 daqiqa
_HTTP_TIMEOUT = 15


@dataclass(frozen=True)
class LavkaProduct:
    id: str
    title: str
    subtitle: str
    amount: str
    price: Decimal
    image_url_template: str  # {w}x{h} placeholder
    available: bool

    def image_url(self, width: int = 400, height: int = 400) -> str:
        return self.image_url_template.replace("{w}", str(width)).replace("{h}", str(height))


def _parse_price(raw: object) -> Decimal | None:
    if raw is None:
        return None
    s = str(raw).replace(' ', '').replace('\xa0', '')
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


def _headers() -> dict[str, str]:
    """JWT + zaruriy Yandex header'lari."""
    token = settings.KARZINKA_LAVKA_TOKEN
    session_id = settings.KARZINKA_LAVKA_SESSION_ID
    cookie = f"webviewtoken={token}"
    if session_id:
        cookie = f"grocery_session_id={session_id}; {cookie}"

    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Accept-Language": "uz",
        "X-Yandex-UID": settings.KARZINKA_LAVKA_YAUID,
        "X-YaTaxi-GeoId": settings.KARZINKA_LAVKA_GEOID,
        "X-Grocery-Trusted-User": "true",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://grocery-b2b-authproxy-ng.lavka.yandex.net",
        "User-Agent": (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Korzinka/korzinkago_sdk/3.10.1 GrocerySDK/1.1.8"
        ),
        "Cookie": cookie,
    }


def _position() -> dict:
    return {"location": [settings.KARZINKA_LAVKA_LON, settings.KARZINKA_LAVKA_LAT]}


def _is_configured() -> bool:
    return bool(
        settings.KARZINKA_LAVKA_TOKEN
        and settings.KARZINKA_LAVKA_YAUID
        and settings.KARZINKA_LAVKA_GEOID,
    )


def fetch_category_group() -> dict | None:
    """Butun kategoriya daraxti (barcha ID'lar bilan)."""
    if not _is_configured():
        logger.info("Lavka token o'rnatilmagan — kategoriya olinmadi")
        return None

    cache_key = "lavka:category_group:v1"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    body = {"position": _position(), "modes": ["grocery"], "is_supermarket": False}
    try:
        resp = requests.post(_URL_CATEGORY_GROUP, json=body, headers=_headers(), timeout=_HTTP_TIMEOUT)
        if resp.status_code == 401:
            logger.info("Lavka token muddati tugagan — Proxyman'dan yangi token oling")
            # Muddati tugagan tokenni 5 daqiqaga cache qilamiz, retry siljitish uchun.
            cache.set(cache_key, {}, 300)
            return None
        resp.raise_for_status()
        data = resp.json()
        cache.set(cache_key, data, _CACHE_TTL)
        return data
    except requests.RequestException as e:
        logger.warning("Lavka category_group fetch failed: %s", e)
        return None


def fetch_category(category_id: str, group_id: str = "", layout_slug: str = "grocery") -> list[LavkaProduct]:
    """Bitta kategoriyadagi barcha mahsulotlar."""
    if not _is_configured():
        return []

    cache_key = f"lavka:category:{category_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return [LavkaProduct(**{**p, "price": Decimal(p["price"])}) for p in cached]

    body = {
        "modes": ["grocery"],
        "category_id": category_id,
        "category_slug_path": {"layout_slug": layout_slug, "group_id": group_id},
        "position": _position(),
        "additional_data": {
            "cart_id": str(uuid.uuid4()),
            "device_coordinates": _position(),
        },
        "cart": {"cart_items": [], "total_price_value": "0", "delivery_cost": "0"},
        "is_supermarket": False,
    }

    try:
        resp = requests.post(_URL_CATEGORY, json=body, headers=_headers(), timeout=_HTTP_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        logger.warning("Lavka category %s fetch failed: %s", category_id, e)
        return []

    products = list(_extract_products(data))
    cache.set(
        cache_key,
        [{
            "id": p.id, "title": p.title, "subtitle": p.subtitle, "amount": p.amount,
            "price": str(p.price), "image_url_template": p.image_url_template,
            "available": p.available,
        } for p in products],
        _CACHE_TTL,
    )
    return products


def _extract_products(data: dict) -> list[LavkaProduct]:
    """Lavka javobidan LavkaProduct'lar chiqarish.

    Response strukturasi (aniqlangan):
    - `products: [...]` — asosiy ro'yxat, bo'lishi mumkin
    - `items: [...]` — cart-uslub javoblarda
    - `modes: [{items: [...]}]` — mode ichida bo'lishi ham mumkin

    Har mahsulotda: id, title, price, image (snippet_image.url yoki image_url_templates[0]).
    """
    products: list[LavkaProduct] = []

    def _from_item(item: dict) -> LavkaProduct | None:
        if not isinstance(item, dict):
            return None
        pid = item.get("id") or item.get("product_id")
        if not pid:
            return None
        price = _parse_price(item.get("price") or item.get("catalog_price"))
        if price is None:
            return None

        image_tpl = ""
        img_list = item.get("image_url_templates") or []
        if isinstance(img_list, list) and img_list:
            image_tpl = img_list[0]
        elif isinstance(item.get("snippet_image"), dict):
            image_tpl = item["snippet_image"].get("url", "")

        return LavkaProduct(
            id=str(pid),
            title=item.get("title") or "",
            subtitle=item.get("subtitle") or item.get("long_title") or "",
            amount=item.get("amount") or item.get("weight_amount") or "",
            price=price,
            image_url_template=image_tpl,
            available=item.get("available", True),
        )

    for key in ("products", "items"):
        for item in data.get(key) or []:
            p = _from_item(item)
            if p:
                products.append(p)

    for mode in data.get("modes") or []:
        if isinstance(mode, dict):
            for item in mode.get("items") or mode.get("products") or []:
                p = _from_item(item)
                if p:
                    products.append(p)

    return products


def fetch_all_products() -> list[LavkaProduct]:
    """Butun katalog — barcha kategoriya + ichidagi mahsulotlar."""
    group = fetch_category_group()
    if not group:
        return []

    result: dict[str, LavkaProduct] = {}
    for cat in _walk_categories(group):
        cat_id = cat.get("id") or cat.get("category_id")
        group_id = cat.get("group_id", "")
        if not cat_id:
            continue
        for p in fetch_category(cat_id, group_id=group_id):
            result[p.id] = p

    logger.info("Lavka: yig'ilgan mahsulotlar soni: %s", len(result))
    return list(result.values())


def _walk_categories(node: dict):
    """Rekursiv — kategoriya daraxtidan barcha yaproqli kategoriyalarni chiqaradi."""
    if not isinstance(node, dict):
        return
    if node.get("id") or node.get("category_id"):
        yield node
    for key in ("children", "categories", "groups", "modes", "data"):
        val = node.get(key)
        if isinstance(val, list):
            for child in val:
                yield from _walk_categories(child)
        elif isinstance(val, dict):
            yield from _walk_categories(val)
