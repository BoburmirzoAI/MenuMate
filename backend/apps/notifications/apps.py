from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.notifications'

    def ready(self) -> None:
        # Signal'larni ro'yxatga olish
        try:
            from apps.notifications import signals  # noqa: F401
        except ImportError:
            pass

        # Firebase Admin SDK'ni ishga tushirish (lazy — service account
        # yo'q bo'lsa ham servis buzilmaydi, faqat log yozadi).
        try:
            from apps.notifications.utils.fcm import initialize_firebase
            initialize_firebase()
        except Exception:  # noqa: BLE001  (server boot vaqti — hech qanday xato yo'l qo'ymaymiz)
            pass
