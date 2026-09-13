from typing import Dict

from .types import MessageTemplate

PRODUCTS_MESSAGES: Dict[str, MessageTemplate] = {
    "SHOPPING_LIST_REGENERATED": {
        "id": "SHOPPING_LIST_REGENERATED",
        "messages": {
            "uz": "Xarid ro'yxati qayta hisoblandi",
            "ru": "Список покупок пересчитан",
            "en": "Shopping list recalculated",
        },
        "status_code": 200,
    },
    "SHOPPING_ITEM_NOT_FOUND": {
        "id": "SHOPPING_ITEM_NOT_FOUND",
        "messages": {
            "uz": "Xarid ro'yxatida bu mahsulot topilmadi",
            "ru": "Товар не найден в списке покупок",
            "en": "Shopping item not found",
        },
        "status_code": 404,
    },
    "SHOPPING_LIST_NOT_FOUND": {
        "id": "SHOPPING_LIST_NOT_FOUND",
        "messages": {
            "uz": "Xarid ro'yxati topilmadi",
            "ru": "Список покупок не найден",
            "en": "Shopping list not found",
        },
        "status_code": 404,
    },
}
