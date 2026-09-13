from typing import Dict

from .types import MessageTemplate

SHARED_MESSAGES: Dict[str, MessageTemplate] = {
    "SUCCESS": {
        "id": "SUCCESS",
        "messages": {
            "uz": "Operatsiya muvaffaqiyatli yakunlandi",
            "ru": "Операция успешно завершена",
            "en": "Operation completed successfully",
        },
        "status_code": 200,
    },
    "CREATED": {
        "id": "CREATED",
        "messages": {
            "uz": "Resurs muvaffaqiyatli yaratildi",
            "ru": "Ресурс успешно создан",
            "en": "Resource created successfully",
        },
        "status_code": 201,
    },
    "UPDATED": {
        "id": "UPDATED",
        "messages": {
            "uz": "Resurs muvaffaqiyatli yangilandi",
            "ru": "Ресурс успешно обновлен",
            "en": "Resource updated successfully",
        },
        "status_code": 200,
    },
    "DELETED": {
        "id": "DELETED",
        "messages": {
            "uz": "Resurs muvaffaqiyatli o'chirildi",
            "ru": "Ресурс успешно удален",
            "en": "Resource deleted successfully",
        },
        "status_code": 200,
    },
    "VALIDATION_ERROR": {
        "id": "VALIDATION_ERROR",
        "messages": {
            "uz": "Noto'g'ri ma'lumot kiritildi",
            "ru": "Неверные входные данные",
            "en": "Invalid input data",
        },
        "status_code": 400,
    },
    "NOT_FOUND": {
        "id": "NOT_FOUND",
        "messages": {
            "uz": "Resurs topilmadi",
            "ru": "Ресурс не найден",
            "en": "Resource not found",
        },
        "status_code": 404,
    },
    "PERMISSION_DENIED": {
        "id": "PERMISSION_DENIED",
        "messages": {
            "uz": "Sizda bu amalni bajarish uchun ruxsat yo'q",
            "ru": "У вас нет прав для выполнения этого действия",
            "en": "You don't have permission to perform this action",
        },
        "status_code": 403,
    },
    "UNAUTHORIZED": {
        "id": "UNAUTHORIZED",
        "messages": {
            "uz": "Autentifikatsiya talab qilinadi",
            "ru": "Требуется аутентификация",
            "en": "Authentication required",
        },
        "status_code": 401,
    },
    "AUTHENTICATION_FAILED": {
        "id": "AUTHENTICATION_FAILED",
        "messages": {
            "uz": "Autentifikatsiya ma'lumotlari noto'g'ri",
            "ru": "Учетные данные недействительны",
            "en": "Authentication credentials are invalid",
        },
        "status_code": 401,
    },
    "METHOD_NOT_ALLOWED": {
        "id": "METHOD_NOT_ALLOWED",
        "messages": {
            "uz": "Bu endpoint uchun metod ruxsat etilmagan",
            "ru": "Метод не разрешен",
            "en": "Method not allowed",
        },
        "status_code": 405,
    },
    "NOT_ACCEPTABLE": {
        "id": "NOT_ACCEPTABLE",
        "messages": {
            "uz": "So'rovning Accept sarlavhasi qondirilmadi",
            "ru": "Не удалось удовлетворить Accept",
            "en": "Not acceptable",
        },
        "status_code": 406,
    },
    "UNSUPPORTED_MEDIA_TYPE": {
        "id": "UNSUPPORTED_MEDIA_TYPE",
        "messages": {
            "uz": "Qo'llab-quvvatlanmaydigan media turi",
            "ru": "Неподдерживаемый тип медиа",
            "en": "Unsupported media type",
        },
        "status_code": 415,
    },
    "THROTTLED": {
        "id": "THROTTLED",
        "messages": {
            "uz": "So'rov cheklandi. Keyinroq qayta urinib ko'ring",
            "ru": "Запрос ограничен. Попробуйте позже",
            "en": "Request throttled",
        },
        "status_code": 429,
    },
    "INTERNAL_SERVER_ERROR": {
        "id": "INTERNAL_SERVER_ERROR",
        "messages": {
            "uz": "Ichki server xatosi yuz berdi",
            "ru": "Внутренняя ошибка сервера",
            "en": "Internal server error",
        },
        "status_code": 500,
    },
    "UNKNOWN_ERROR": {
        "id": "UNKNOWN_ERROR",
        "messages": {
            "uz": "Kutilmagan xatolik yuz berdi",
            "ru": "Произошла непредвиденная ошибка",
            "en": "An unexpected error occurred",
        },
        "status_code": 500,
    },
}
