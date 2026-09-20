"""Admin interfeys uchun rasm qidirish.

Berilgan matn bo'yicha Wikipedia summary API va Wikimedia Commons fayllar
qidiruvidan nomzodlar to'playdi. Har nomzod: rasm URL, manba (wiki/commons),
qayerdan olindi (title), til.

Cache 24 soat — bir xil qidiruv qayta ishga tushmasin.
"""
from __future__ import annotations

import logging
import urllib.parse
from dataclasses import dataclass, asdict

import requests
from django.core.cache import cache

logger = logging.getLogger(__name__)

_TIMEOUT = 5
_CACHE_TTL = 60 * 60 * 24
_USER_AGENT = 'MenuMate/1.0 (admin image search)'
_DEFAULT_LANGS = ('uz', 'ru', 'en')
_COMMONS_LIMIT = 12


@dataclass(frozen=True)
class ImageCandidate:
    url: str
    thumb_url: str
    source: str
    title: str
    lang: str


def search_images(query: str) -> list[dict]:
    """Query uchun nomzod rasmlar ro'yxatini qaytaradi.

    Qidiruv strategiyasi taom nomi uchun optimallashtirilgan:
      1. Har til uchun Wikipedia summary (uz/ru/en).
      2. Wikimedia Commons — ovqat kontekstiga aniqroq qidiruv:
         ``<query> food``, ``<query> dish``, ``<query> taom`` va sof ``<query>``.
    Natijalar `thumb_url` bo'yicha takrorlanmaydi, ovqat kontekstidagilar
    birinchi navbatda ko'rinadi.
    """
    query = (query or '').strip()
    if not query:
        return []

    cache_key = f'admin_img_search:v2:{query.lower()}'
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    results: list[ImageCandidate] = []
    seen_urls: set[str] = set()

    def _add(cand: ImageCandidate | None) -> None:
        if cand is None or not cand.thumb_url or cand.thumb_url in seen_urls:
            return
        results.append(cand)
        seen_urls.add(cand.thumb_url)

    for lang in _DEFAULT_LANGS:
        _add(_wikipedia_summary(query, lang))

    for suffix in (' food', ' dish', ' taom', ''):
        for cand in _commons_search(f'{query}{suffix}'.strip()):
            _add(cand)

    payload = [asdict(c) for c in results]
    cache.set(cache_key, payload, _CACHE_TTL)
    return payload


def _wikipedia_summary(query: str, lang: str) -> ImageCandidate | None:
    url = f'https://{lang}.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}'
    try:
        r = requests.get(url, headers={'User-Agent': _USER_AGENT}, timeout=_TIMEOUT)
    except requests.RequestException as exc:
        logger.debug('wiki summary failed for %s/%s: %s', lang, query, exc)
        return None
    if r.status_code != 200:
        return None
    try:
        data = r.json()
    except ValueError:
        return None
    thumb = (data.get('thumbnail') or {}).get('source') or ''
    orig = (data.get('originalimage') or {}).get('source') or ''
    if not thumb and not orig:
        return None
    return ImageCandidate(
        url=orig or thumb,
        thumb_url=thumb or orig,
        source='wikipedia',
        title=data.get('title', query),
        lang=lang,
    )


def _commons_search(query: str) -> list[ImageCandidate]:
    api = 'https://commons.wikimedia.org/w/api.php'
    try:
        r = requests.get(
            api,
            params={
                'action': 'query',
                'list': 'search',
                'srsearch': query,
                'srnamespace': 6,
                'format': 'json',
                'srlimit': _COMMONS_LIMIT,
            },
            headers={'User-Agent': _USER_AGENT},
            timeout=_TIMEOUT,
        )
    except requests.RequestException as exc:
        logger.debug('commons search failed for %s: %s', query, exc)
        return []
    if r.status_code != 200:
        return []
    try:
        hits = r.json().get('query', {}).get('search', []) or []
    except ValueError:
        return []
    if not hits:
        return []

    titles = [h['title'] for h in hits if isinstance(h, dict) and h.get('title')]
    return _commons_imageinfo(titles)


def _commons_imageinfo(titles: list[str]) -> list[ImageCandidate]:
    if not titles:
        return []
    api = 'https://commons.wikimedia.org/w/api.php'
    try:
        r = requests.get(
            api,
            params={
                'action': 'query',
                'titles': '|'.join(titles),
                'prop': 'imageinfo',
                'iiprop': 'url|mime',
                'iiurlwidth': 500,
                'format': 'json',
            },
            headers={'User-Agent': _USER_AGENT},
            timeout=_TIMEOUT,
        )
    except requests.RequestException as exc:
        logger.debug('commons imageinfo failed: %s', exc)
        return []
    if r.status_code != 200:
        return []
    try:
        pages = r.json().get('query', {}).get('pages', {}) or {}
    except ValueError:
        return []

    out: list[ImageCandidate] = []
    for page in pages.values():
        info = (page.get('imageinfo') or [None])[0]
        if not info:
            continue
        mime = info.get('mime', '')
        if not mime.startswith('image/') or mime == 'image/svg+xml':
            continue
        thumb = info.get('thumburl') or ''
        orig = info.get('url') or ''
        if not thumb and not orig:
            continue
        title = page.get('title', '').removeprefix('File:')
        out.append(ImageCandidate(
            url=orig or thumb,
            thumb_url=thumb or orig,
            source='commons',
            title=title,
            lang='',
        ))
    return out
