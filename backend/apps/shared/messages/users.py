from typing import Dict

from .types import MessageTemplate

USER_MESSAGES: Dict[str, MessageTemplate] = {
    "USER_REGISTERED_SUCCESSFULLY": {
        "id": "USER_REGISTERED_SUCCESSFULLY",
        "messages": {
            "uz": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi",
            "ru": "Пользователь успешно зарегистрирован",
            "en": "User registered successfully",
        },
        "status_code": 201,
    },
    "LOGIN_SUCCESSFUL": {
        "id": "LOGIN_SUCCESSFUL",
        "messages": {
            "uz": "Kirish muvaffaqiyatli",
            "ru": "Вход выполнен успешно",
            "en": "Login successful",
        },
        "status_code": 200,
    },
    "USER_NOT_FOUND": {
        "id": "USER_NOT_FOUND",
        "messages": {
            "uz": "Foydalanuvchi topilmadi",
            "ru": "Пользователь не найден",
            "en": "User not found",
        },
        "status_code": 404,
    },
    "EMAIL_ALREADY_EXISTS": {
        "id": "EMAIL_ALREADY_EXISTS",
        "messages": {
            "uz": "Bu email allaqachon ro'yxatdan o'tgan",
            "ru": "Этот email уже зарегистрирован",
            "en": "Email already registered",
        },
        "status_code": 400,
    },
    "INVALID_CREDENTIALS": {
        "id": "INVALID_CREDENTIALS",
        "messages": {
            "uz": "Email yoki parol noto'g'ri",
            "ru": "Неверный email или пароль",
            "en": "Invalid email or password",
        },
        "status_code": 400,
    },
    "INVALID_PASSWORD": {
        "id": "INVALID_PASSWORD",
        "messages": {
            "uz": "Parol noto'g'ri",
            "ru": "Неверный пароль",
            "en": "Invalid password",
        },
        "status_code": 400,
    },
    "PASSWORDS_DO_NOT_MATCH": {
        "id": "PASSWORDS_DO_NOT_MATCH",
        "messages": {
            "uz": "Parollar mos kelmadi",
            "ru": "Пароли не совпадают",
            "en": "Passwords do not match",
        },
        "status_code": 400,
    },
    "INVALID_TOKEN": {
        "id": "INVALID_TOKEN",
        "messages": {
            "uz": "Token yaroqli emas",
            "ru": "Недействительный токен",
            "en": "Invalid token",
        },
        "status_code": 401,
    },
    "UPDATE_REQUIRED": {
        "id": "UPDATE_REQUIRED",
        "messages": {
            "uz": "Ilovaning yangi versiyasi majburiy. Iltimos yangilang.",
            "ru": "Требуется обновление приложения.",
            "en": "App update required. Please update.",
        },
        "status_code": 426,
    },
    "UPDATE_RECOMMENDED": {
        "id": "UPDATE_RECOMMENDED",
        "messages": {
            "uz": "Ilovaning yangi versiyasi mavjud",
            "ru": "Доступна новая версия приложения",
            "en": "A new version is available",
        },
        "status_code": 200,
    },
    "OS_NOT_SUPPORTED": {
        "id": "OS_NOT_SUPPORTED",
        "messages": {
            "uz": "Qurilmangizning operatsion tizimi qo'llab-quvvatlanmaydi",
            "ru": "ОС вашего устройства не поддерживается",
            "en": "Your device OS is not supported",
        },
        "status_code": 426,
    },
    "USER_BLOCKED": {
        "id": "USER_BLOCKED",
        "messages": {
            "uz": "Foydalanuvchi bloklangan",
            "ru": "Пользователь заблокирован",
            "en": "User is blocked",
        },
        "status_code": 403,
    },
    "USER_INACTIVE": {
        "id": "USER_INACTIVE",
        "messages": {
            "uz": "Foydalanuvchi aktiv emas",
            "ru": "Пользователь неактивен",
            "en": "User is not active",
        },
        "status_code": 403,
    },
    "TOO_MANY_ATTEMPTS": {
        "id": "TOO_MANY_ATTEMPTS",
        "messages": {
            "uz": "Juda ko'p noto'g'ri urinish. 15 daqiqadan keyin qayta urinib ko'ring",
            "ru": "Слишком много попыток. Попробуйте через 15 минут",
            "en": "Too many failed attempts. Try again in 15 minutes",
        },
        "status_code": 429,
    },
    "DEVICE_NOT_FOUND": {
        "id": "DEVICE_NOT_FOUND",
        "messages": {
            "uz": "Qurilma topilmadi",
            "ru": "Устройство не найдено",
            "en": "Device not found",
        },
        "status_code": 404,
    },
    "LOGOUT_SUCCESSFUL": {
        "id": "LOGOUT_SUCCESSFUL",
        "messages": {
            "uz": "Muvaffaqiyatli chiqdingiz",
            "ru": "Вы успешно вышли",
            "en": "Logged out successfully",
        },
        "status_code": 200,
    },
    "INVALID_OLD_PASSWORD": {
        "id": "INVALID_OLD_PASSWORD",
        "messages": {
            "uz": "Eski parol noto'g'ri",
            "ru": "Старый пароль неверный",
            "en": "Old password is incorrect",
        },
        "status_code": 400,
    },
    "NEW_PASSWORD_SAME_AS_OLD": {
        "id": "NEW_PASSWORD_SAME_AS_OLD",
        "messages": {
            "uz": "Yangi parol eskisi bilan bir xil bo'lmasligi kerak",
            "ru": "Новый пароль должен отличаться от старого",
            "en": "New password must differ from old",
        },
        "status_code": 400,
    },
    "WEAK_PASSWORD": {
        "id": "WEAK_PASSWORD",
        "messages": {
            "uz": "Parol yetarli darajada murakkab emas",
            "ru": "Пароль недостаточно надёжный",
            "en": "Password is not strong enough",
        },
        "status_code": 400,
    },
    "PASSWORD_CHANGED": {
        "id": "PASSWORD_CHANGED",
        "messages": {
            "uz": "Parol muvaffaqiyatli o'zgartirildi",
            "ru": "Пароль успешно изменён",
            "en": "Password changed successfully",
        },
        "status_code": 200,
    },
    "PASSWORD_RESET_CODE_SENT": {
        "id": "PASSWORD_RESET_CODE_SENT",
        "messages": {
            "uz": "Agar bu email tizimda bo'lsa, tiklash kodi yuborildi",
            "ru": "Если email существует, код для сброса отправлен",
            "en": "If the email exists, a reset code has been sent",
        },
        "status_code": 200,
    },
    "PASSWORD_RESET_SUCCESSFUL": {
        "id": "PASSWORD_RESET_SUCCESSFUL",
        "messages": {
            "uz": "Parol muvaffaqiyatli tiklandi",
            "ru": "Пароль успешно сброшен",
            "en": "Password has been reset",
        },
        "status_code": 200,
    },
    "INVALID_LANGUAGE_TYPE": {
        "id": "INVALID_LANGUAGE_TYPE",
        "messages": {
            "uz": "Noto'g'ri til",
            "ru": "Неверный язык",
            "en": "Invalid language",
        },
        "status_code": 400,
    },
    "INVALID_VERIFICATION_CODE": {
        "id": "INVALID_VERIFICATION_CODE",
        "messages": {
            "uz": "Tasdiqlash kodi noto'g'ri yoki muddati o'tgan",
            "ru": "Код подтверждения неверный или истёк",
            "en": "Verification code is invalid or expired",
        },
        "status_code": 400,
    },
    "VERIFICATION_CODE_SENT": {
        "id": "VERIFICATION_CODE_SENT",
        "messages": {
            "uz": "Tasdiqlash kodi yuborildi",
            "ru": "Код подтверждения отправлен",
            "en": "Verification code has been sent",
        },
        "status_code": 200,
    },
    "EMAIL_VERIFIED": {
        "id": "EMAIL_VERIFIED",
        "messages": {
            "uz": "Email muvaffaqiyatli tasdiqlandi",
            "ru": "Email успешно подтверждён",
            "en": "Email verified successfully",
        },
        "status_code": 200,
    },
    "EMAIL_ALREADY_VERIFIED": {
        "id": "EMAIL_ALREADY_VERIFIED",
        "messages": {
            "uz": "Email allaqachon tasdiqlangan",
            "ru": "Email уже подтверждён",
            "en": "Email is already verified",
        },
        "status_code": 400,
    },
    "DELETE_CONFIRMATION_INVALID": {
        "id": "DELETE_CONFIRMATION_INVALID",
        "messages": {
            "uz": "Tasdiqlash uchun aynan 'DELETE' deb yozing",
            "ru": "Для подтверждения введите 'DELETE'",
            "en": "Type 'DELETE' to confirm",
        },
        "status_code": 400,
    },
    "ACCOUNT_DELETED": {
        "id": "ACCOUNT_DELETED",
        "messages": {
            "uz": "Hisob muvaffaqiyatli o'chirildi",
            "ru": "Аккаунт успешно удалён",
            "en": "Account has been deleted",
        },
        "status_code": 200,
    },
}
