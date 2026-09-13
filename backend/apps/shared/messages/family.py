from typing import Dict

from .types import MessageTemplate

FAMILY_MESSAGES: Dict[str, MessageTemplate] = {
    "FAMILY_CREATED": {
        "id": "FAMILY_CREATED",
        "messages": {
            "uz": "Oila muvaffaqiyatli yaratildi",
            "ru": "Семья успешно создана",
            "en": "Family created successfully",
        },
        "status_code": 201,
    },
    "FAMILY_DELETED": {
        "id": "FAMILY_DELETED",
        "messages": {
            "uz": "Oila muvaffaqiyatli o'chirildi",
            "ru": "Семья успешно удалена",
            "en": "Family deleted successfully",
        },
        "status_code": 200,
    },
    "FAMILY_ALREADY_EXISTS": {
        "id": "FAMILY_ALREADY_EXISTS",
        "messages": {
            "uz": "Sizda allaqachon oila mavjud",
            "ru": "У вас уже есть семья",
            "en": "You already have a family",
        },
        "status_code": 400,
    },
    "FAMILY_NOT_FOUND": {
        "id": "FAMILY_NOT_FOUND",
        "messages": {
            "uz": "Oila topilmadi. Avval oila yarating",
            "ru": "Семья не найдена. Сначала создайте семью",
            "en": "Family not found. Create one first",
        },
        "status_code": 404,
    },
    "MEMBER_CREATED": {
        "id": "MEMBER_CREATED",
        "messages": {
            "uz": "Oila a'zosi muvaffaqiyatli qo'shildi",
            "ru": "Член семьи успешно добавлен",
            "en": "Family member added successfully",
        },
        "status_code": 201,
    },
    "MEMBER_DELETED": {
        "id": "MEMBER_DELETED",
        "messages": {
            "uz": "Oila a'zosi o'chirildi",
            "ru": "Член семьи удалён",
            "en": "Family member deleted",
        },
        "status_code": 200,
    },
    "MEMBER_NOT_FOUND": {
        "id": "MEMBER_NOT_FOUND",
        "messages": {
            "uz": "Oila a'zosi topilmadi",
            "ru": "Член семьи не найден",
            "en": "Family member not found",
        },
        "status_code": 404,
    },
    "HEALTH_CONDITION_NOT_FOUND": {
        "id": "HEALTH_CONDITION_NOT_FOUND",
        "messages": {
            "uz": "Ba'zi sog'liq holatlari topilmadi: {ids}",
            "ru": "Некоторые состояния здоровья не найдены: {ids}",
            "en": "Some health conditions not found: {ids}",
        },
        "status_code": 400,
    },
    "RECIPE_NOT_FOUND": {
        "id": "RECIPE_NOT_FOUND",
        "messages": {
            "uz": "Ba'zi retseptlar topilmadi: {ids}",
            "ru": "Некоторые рецепты не найдены: {ids}",
            "en": "Some recipes not found: {ids}",
        },
        "status_code": 400,
    },
    "INGREDIENT_NOT_FOUND": {
        "id": "INGREDIENT_NOT_FOUND",
        "messages": {
            "uz": "Ba'zi ingredientlar topilmadi: {ids}",
            "ru": "Некоторые ингредиенты не найдены: {ids}",
            "en": "Some ingredients not found: {ids}",
        },
        "status_code": 400,
    },
    "RECIPE_LIKE_DISLIKE_CONFLICT": {
        "id": "RECIPE_LIKE_DISLIKE_CONFLICT",
        "messages": {
            "uz": "Bir xil retsept liked va disliked ro'yxatida bo'lishi mumkin emas: {ids}",
            "ru": "Один рецепт не может быть одновременно в liked и disliked: {ids}",
            "en": "Same recipe cannot be both liked and disliked: {ids}",
        },
        "status_code": 400,
    },
}
