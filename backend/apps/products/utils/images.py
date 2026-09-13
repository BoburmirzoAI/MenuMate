"""Ingredient/Recipe rasmlarini avtomatik olish.

Manba tartibi:
1. Model'dagi `image_url` (agar qo'lda kiritilgan bo'lsa)
2. Karzinka mos mahsulotning rasmi (Lavka token amal qilsa)
3. Wikipedia thumbnail — RECIPE_WIKI_OVERRIDES dan aniq article, yoki qidiruv API bilan
4. Retsept uchun: birinchi ingredient rasmi

Har lookup Redis'da 7 kun cache'lanadi.
"""
from __future__ import annotations

import logging
import urllib.parse

import requests
from django.core.cache import cache

from apps.products.utils.karzinka import find_karzinka_match

logger = logging.getLogger(__name__)

_WIKI_TTL = 60 * 60 * 24 * 7  # 7 kun
_WIKI_TIMEOUT = 5

# Retsept nomi (name_uz) → Wikipedia article + lang.
# Hozir DB dagi 35 retseptning har biri uchun to'g'ri, mazmun bo'yicha aniq rasm keltiradi.
# Wikipedia article aynan taom rasmi bilan chiqadigan qilib tanlangan (davlat bayrog'i, ingredient
# yoki halolsiz variantlar mahsus chetlab o'tilgan).
RECIPE_WIKI_OVERRIDES: dict[str, tuple[str, str]] = {
    # O'zbek/markaziy osiyo taomlari
    "Osh (Palov)":               ("Плов", "ru"),
    "Tovuqli guruchli osh":      ("Плов", "ru"),
    "Lag'mon":                   ("Лагман", "ru"),
    "Chuchvara":                 ("Пельмени", "ru"),
    "Manti":                     ("Manti (food)", "en"),
    "Sho'rva":                   ("Шурпа", "ru"),
    "Somsa":                     ("Самса", "ru"),
    "Non":                       ("Лепёшка", "ru"),
    "Non-choy nonushtasi":       ("Лепёшка", "ru"),
    "Dimlama":                   ("Дымлама", "ru"),
    "Xonim":                     ("Ханум (блюдо)", "ru"),
    "Mastava":                   ("Мастава", "ru"),
    # Mosh xo'rda uchun Wikipedia'da alohida article yo'q — mos ovqat rasmi Mastava (o'xshash sho'rva)
    "Mosh xo'rda":               ("Мастава", "ru"),
    # Halol qovurma — cho'chqa emas (Kavurma turk taomi, halol)
    "Qovurma":                   ("Kavurma", "en"),
    # cache eski jaуно natijasini "wiki_img:override:Kavurma:en" kalitiga qo'shadi.

    # Bo'tqalar
    "Grechka bo'tqasi":          ("Гречневая каша", "ru"),
    "Suli bo'tqasi (Ovsyanka)":  ("Овсяная каша", "ru"),
    "Manniy bo'tqa":             ("Манная каша", "ru"),

    # Sut mahsulotlari asosidagi
    "Sirniki":                   ("Сырники", "ru"),
    "Suzmali desert":            ("Cheesecake", "en"),
    "Suzmali salat (nonushta)":  ("Сырники", "ru"),

    # Sho'rvalar
    "Adas sho'rva":              ("Lentil soup", "en"),
    "Ismaloq sho'rva":           ("Spinach soup", "en"),
    "Piyoz sho'rva":             ("Луковый суп", "ru"),
    "No'xatli sho'rva":          ("Гороховый суп", "ru"),
    "Borsch":                    ("Борщ", "ru"),
    "Solyanka":                  ("Солянка", "ru"),

    # Go'shtli
    "Kebab (Shashlik)":          ("Шашлык", "ru"),
    "Kotlet":                    ("Котлета", "ru"),
    "Turkey kotletlar":          ("Turkey meat", "en"),
    "Pelmeni":                   ("Пельмени", "ru"),
    "Kurka barbekyu":            ("Barbecue chicken", "en"),
    "Tovuqli sabzavot":          ("Chicken cacciatore", "en"),

    # Baliq/dengiz mahsulotlari
    "Baliq pech (dukhovka)":     ("Fish as food", "en"),
    "Krevetka guruch bilan":     ("Fried rice", "en"),

    # Salatlar
    "Vinegret":                  ("Винегрет", "ru"),
    "Olivye salati":             ("Оливье (салат)", "ru"),
    "Grekcha salat":             ("Греческий салат", "ru"),
    "Sezar salat":               ("Цезарь (салат)", "ru"),
    "Meva salati":               ("Fruit salad", "en"),
    "Bodring salati":            ("Cucumber salad", "en"),
    "Karam salati":              ("Coleslaw", "en"),
    "Achchiq-chuchuk":           ("Ачик-чучук", "ru"),

    # Nonushta
    "Blin":                      ("Блины", "ru"),
    "Omlet":                     ("Омлет", "ru"),
    "Yaishnitsa":                ("Яичница", "ru"),
    "Piroski":                   ("Пирожки", "ru"),

    # Ichimliklar
    "Kompot":                    ("Компот", "ru"),
    "Kompot (mevali)":           ("Компот", "ru"),
    "Ko'k choy":                 ("Зелёный чай", "ru"),
    "Qora choy":                 ("Чёрный чай", "ru"),
    "Ayron":                     ("Айран", "ru"),
    "Qatiqli ichimlik (Ayron)":  ("Айран", "ru"),
    "Limonad":                   ("Лимонад", "ru"),
    "Limonli suv":               ("Лимонад", "ru"),
    "Kefir":                     ("Кефир", "ru"),

    # Shirinliklar
    "Halvo":                     ("Халва", "ru"),
    "Chak-chak":                 ("Чак-чак", "ru"),

    # ────────────────────── INGREDIENTLAR ──────────────────────
    # Rasmsiz qolgan yoki noaniq keladigan ingredientlar uchun aniq Wikipedia article.
    # Sut mahsulotlari va sabzavot uchun ham override — Karzinka topmasa fallback ishlaydi.
    "Mol go'shti":               ("Beef", "en"),
    "Qo'y go'shti":              ("Lamb and mutton", "en"),
    "Farshli go'sht":            ("Ground meat", "en"),
    "Losos":                     ("Salmon as food", "en"),
    "Cho'chqa go'shti":          ("Pork", "en"),
    "Kurka go'shti":             ("Turkey meat", "en"),
    "Tovuq go'shti":             ("Chicken as food", "en"),
    "Baliq (som/karp)":          ("Carp", "en"),
    "Krevetka":                  ("Shrimp", "en"),

    "Baqlajon":                  ("Eggplant", "en"),
    "Bodring":                   ("Cucumber", "en"),
    "Sabzi":                     ("Carrot", "en"),
    "Sholg'om":                  ("Turnip", "en"),
    "Bulg'or qalampiri":         ("Bell pepper", "en"),
    "Ismaloq":                   ("Spinach", "en"),
    "Karam":                     ("Cabbage", "en"),
    "Kartoshka":                 ("Potato", "en"),
    "Piyoz":                     ("Onion", "en"),
    "Ko'k piyoz":                ("Scallion", "en"),
    "Sarimsoq":                  ("Garlic", "en"),
    "Pomidor":                   ("Tomato", "en"),
    "Qovoq":                     ("Pumpkin", "en"),
    "Qovoqcha":                  ("Zucchini", "en"),
    "Turp":                      ("Radish", "en"),
    "Kashnich":                  ("Coriander", "en"),
    "Petrushka":                 ("Parsley", "en"),
    "Rayxon":                    ("Basil", "en"),
    "Ukrop":                     ("Dill", "en"),

    "Zaytun yog'i":              ("Olive oil", "en"),
    "Kungaboqar yog'i":          ("Sunflower oil", "en"),
    "Yog' (sariyog')":           ("Butter", "en"),

    "Achchiq qalampir":          ("Chili pepper", "en"),
    "Qizil murch":               ("Paprika", "en"),
    "Qora murch":                ("Black pepper", "en"),
    "Lavr yaprog'i":             ("Bay leaf", "en"),
    "Zira":                      ("Cumin", "en"),
    "Tuz":                       ("Salt", "en"),
    "Ziravor (aralashma)":       ("Spice", "en"),

    "Anor":                      ("Pomegranate", "en"),
    "Apelsin":                   ("Orange (fruit)", "en"),
    "Banan":                     ("Banana", "en"),
    "Behi":                      ("Quince", "en"),
    "Limon":                     ("Lemon", "en"),
    "Nok":                       ("Pear", "en"),
    "Olma":                      ("Apple", "en"),
    "Qovun":                     ("Muskmelon", "en"),
    "Qulupnay":                  ("Strawberry", "en"),
    "Tarvuz":                    ("Watermelon", "en"),
    "Uzum":                      ("Grape", "en"),

    "Adas":                      ("Lentil", "en"),
    "Grechka":                   ("Buckwheat", "en"),
    "Guruch":                    ("Rice", "en"),
    "Loviya":                    ("Common bean", "en"),
    "Makaron":                   ("Pasta", "en"),
    "Mosh":                      ("Mung bean", "en"),
    "No'xat":                    ("Chickpea", "en"),
    "Suli (ovsyanka)":           ("Oat", "en"),
    "Un (bug'doy)":              ("Wheat flour", "en"),

    "Asal":                      ("Honey", "en"),
    "Bodom":                     ("Almond", "en"),
    "Choy barglari":             ("Tea", "en"),
    "Shakar":                    ("Sugar", "en"),
    "Sirka":                     ("Vinegar", "en"),
    "Suv":                       ("Water", "en"),
    "Tuxum":                     ("Chicken egg as food", "en"),
    "Yeryong'oq":                ("Peanut", "en"),
    "Yong'oq":                   ("Walnut", "en"),
}

# Backwards-compat: eski nomlar bilan izlanishi mumkin.
INGREDIENT_WIKI_OVERRIDES = RECIPE_WIKI_OVERRIDES


def _wiki_summary_image(title: str, lang: str) -> str | None:
    """REST API `page/summary` orqali lead-thumbnail. Ba'zi article'larda bo'lmasligi mumkin."""
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
    try:
        r = requests.get(url, headers={"User-Agent": "MenuMate/1.0"}, timeout=_WIKI_TIMEOUT)
        if r.status_code != 200:
            return None
        d = r.json()
        thumb = (d.get("thumbnail") or {}).get("source")
        if thumb:
            return thumb
        orig = (d.get("originalimage") or {}).get("source")
        if orig:
            return orig
    except requests.RequestException:
        return None
    # REST summary'da lead rasm yo'q — pageimages API bilan urinamiz.
    return _wiki_pageimage(title, lang)


def _wiki_pageimage(title: str, lang: str, size: int = 400) -> str | None:
    """MediaWiki `pageimages` API — page image thumbnail'ini oladi.

    REST `page/summary` ba'zi article'lar (masalan Wiki'da hech qanday lead rasm
    aniqlanmagan) uchun `thumbnail` qaytarmaydi. `pageimages` esa har article'ning
    asosiy rasmini olib kelishga urinadi.
    """
    url = (
        f"https://{lang}.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}"
        f"&prop=pageimages&format=json&pithumbsize={size}&redirects=1"
    )
    try:
        r = requests.get(url, headers={"User-Agent": "MenuMate/1.0"}, timeout=_WIKI_TIMEOUT)
        if r.status_code != 200:
            return None
        pages = (r.json().get("query") or {}).get("pages") or {}
        for _, page in pages.items():
            thumb = (page.get("thumbnail") or {}).get("source")
            if thumb:
                return thumb
    except requests.RequestException:
        return None
    return None


def _wiki_search(query: str, lang: str) -> str | None:
    url = (
        f"https://{lang}.wikipedia.org/w/api.php?action=query&list=search"
        f"&srsearch={urllib.parse.quote(query)}&format=json&srlimit=1"
    )
    try:
        r = requests.get(url, headers={"User-Agent": "MenuMate/1.0"}, timeout=_WIKI_TIMEOUT)
        if r.status_code != 200:
            return None
        hits = r.json().get("query", {}).get("search", [])
        return hits[0]["title"] if hits else None
    except requests.RequestException:
        return None


def _wiki_image(name_uz: str, name_ru: str, name_en: str) -> str:
    """Nom asosida Wikipedia rasm URL topadi. Cache 7 kun.

    Ustunlik:
    1. `RECIPE_WIKI_OVERRIDES` dagi aniq article — rasm topilsa qaytaradi.
    2. Override natija bergani bo'lmasa yoki override umuman yo'q bo'lsa —
       en/ru/uz Wikipedia'da summary + search fallback bilan qidiradi.
    """
    # 1. Aniq override — rasmi bo'lsa qaytamiz, bo'lmasa fallback'ga tushamiz.
    #    Bo'sh natijani qisqa muddatga (1 soat) cache'lamoqchimiz — ehtimol keyingi
    #    urinishida Wikipedia rate-limit'i pasaygan bo'ladi va rasm keladi.
    if name_uz in RECIPE_WIKI_OVERRIDES:
        article, lang = RECIPE_WIKI_OVERRIDES[name_uz]
        cache_key = f"wiki_img:override:{article}:{lang}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        if cached is None:
            img = _wiki_summary_image(article, lang) or ''
            # Bo'sh natijani faqat 1 soat saqlaymiz — retry imkoni qolsin.
            cache.set(cache_key, img, _WIKI_TTL if img else 3600)
            if img:
                return img

    # 2. Umumiy qidiruv fallback
    cache_key = f"wiki_img:{name_uz}|{name_ru}|{name_en}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    for query, lang in [(name_en, "en"), (name_ru, "ru"), (name_uz, "uz")]:
        if not query:
            continue
        img = _wiki_summary_image(query, lang)
        if img:
            cache.set(cache_key, img, _WIKI_TTL)
            return img
        title = _wiki_search(query, lang)
        if title and title != query:
            img = _wiki_summary_image(title, lang)
            if img:
                cache.set(cache_key, img, _WIKI_TTL)
                return img

    cache.set(cache_key, '', 3600)  # 1 soatga bo'sh cache — keyin retry
    return ''


def ingredient_image_url(ingredient) -> str:
    if ingredient is None:
        return ''
    if ingredient.image_url:
        return ingredient.image_url

    match = find_karzinka_match(ingredient)
    if match and match.image_url:
        return match.image_url

    return _wiki_image(
        ingredient.name_uz or ingredient.name or '',
        ingredient.name_ru or '',
        ingredient.name_en or '',
    )


def recipe_image_url(recipe) -> str:
    if recipe is None:
        return ''
    if recipe.image_url:
        return recipe.image_url

    img = _wiki_image(
        recipe.name_uz or recipe.name or '',
        recipe.name_ru or '',
        recipe.name_en or '',
    )
    if img:
        return img

    # Karzinka'da tayyor ovqat sifatida bo'lishi mumkin (Osh, Manti)
    proxy = type('_P', (), {
        'name': recipe.name,
        'name_uz': recipe.name_uz or recipe.name,
        'name_ru': recipe.name_ru or '',
        'name_en': recipe.name_en or '',
        'id': recipe.id,
    })
    match = find_karzinka_match(proxy)
    if match and match.image_url:
        return match.image_url

    # Birinchi ingredient rasmi
    first_ri = recipe.ingredients.order_by('id').select_related('ingredient').first()
    if first_ri:
        return ingredient_image_url(first_ri.ingredient)
    return ''
