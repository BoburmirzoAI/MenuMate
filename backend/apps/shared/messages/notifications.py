from typing import Dict

from .types import MessageTemplate

NOTIFICATIONS_MESSAGES: Dict[str, MessageTemplate] = {
    "NOTIFICATION_NOT_FOUND": {
        "id": "NOTIFICATION_NOT_FOUND",
        "messages": {
            "uz": "Bildirishnoma topilmadi",
            "ru": "Уведомление не найдено",
            "en": "Notification not found",
        },
        "status_code": 404,
    },
    "ALL_NOTIFICATIONS_READ": {
        "id": "ALL_NOTIFICATIONS_READ",
        "messages": {
            "uz": "Barcha bildirishnomalar o'qildi",
            "ru": "Все уведомления помечены прочитанными",
            "en": "All notifications marked as read",
        },
        "status_code": 200,
    },
}
