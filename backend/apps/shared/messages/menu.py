from typing import Dict

from .types import MessageTemplate

MENU_MESSAGES: Dict[str, MessageTemplate] = {
    "MENU_CREATED": {
        "id": "MENU_CREATED",
        "messages": {
            "uz": "Menyu yaratildi",
            "ru": "Меню создано",
            "en": "Menu created",
        },
        "status_code": 201,
    },
    "MENU_CLEARED": {
        "id": "MENU_CLEARED",
        "messages": {
            "uz": "Menyu tozalandi",
            "ru": "Меню очищено",
            "en": "Menu cleared",
        },
        "status_code": 200,
    },
    "MEAL_ITEM_ADDED": {
        "id": "MEAL_ITEM_ADDED",
        "messages": {
            "uz": "Ovqat qo'shildi",
            "ru": "Блюдо добавлено",
            "en": "Meal item added",
        },
        "status_code": 201,
    },
    "MEAL_ITEM_NOT_FOUND": {
        "id": "MEAL_ITEM_NOT_FOUND",
        "messages": {
            "uz": "Element topilmadi",
            "ru": "Элемент не найден",
            "en": "Item not found",
        },
        "status_code": 404,
    },
    "RECIPE_CATEGORY_MISMATCH": {
        "id": "RECIPE_CATEGORY_MISMATCH",
        "messages": {
            "uz": "Retsept kategoriyasi bu bo'limga mos emas",
            "ru": "Категория рецепта не подходит для этого раздела",
            "en": "Recipe category does not match this slot",
        },
        "status_code": 400,
    },
    "MENU_NOT_FOUND": {
        "id": "MENU_NOT_FOUND",
        "messages": {
            "uz": "Menyu topilmadi",
            "ru": "Меню не найдено",
            "en": "Menu not found",
        },
        "status_code": 404,
    },
    "FAMILY_HAS_NO_MEMBERS": {
        "id": "FAMILY_HAS_NO_MEMBERS",
        "messages": {
            "uz": "Menyu tuzish uchun avval oila a'zolarini qo'shing",
            "ru": "Сначала добавьте членов семьи",
            "en": "Add family members first before generating a menu",
        },
        "status_code": 400,
    },
    "MEAL_NOT_FOUND": {
        "id": "MEAL_NOT_FOUND",
        "messages": {
            "uz": "Mahal topilmadi",
            "ru": "Приём пищи не найден",
            "en": "Meal not found",
        },
        "status_code": 404,
    },
    "DAY_NOT_FOUND": {
        "id": "DAY_NOT_FOUND",
        "messages": {
            "uz": "Kun topilmadi",
            "ru": "День не найден",
            "en": "Day not found",
        },
        "status_code": 404,
    },
    "WEATHER_FETCH_FAILED": {
        "id": "WEATHER_FETCH_FAILED",
        "messages": {
            "uz": "Ob-havo ma'lumotini olishda xatolik",
            "ru": "Ошибка получения погоды",
            "en": "Failed to fetch weather data",
        },
        "status_code": 502,
    },
    "WEATHER_CITY_NOT_FOUND": {
        "id": "WEATHER_CITY_NOT_FOUND",
        "messages": {
            "uz": "Ob-havo bazasida bu shahar topilmadi: {city}",
            "ru": "Город не найден в базе погоды: {city}",
            "en": "City not found in weather service: {city}",
        },
        "status_code": 404,
    },
}
