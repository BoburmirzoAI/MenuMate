from django.db import models

from apps.shared.models import BaseModel


class Holiday(BaseModel):
    """O'zbekiston rasmiy bayramlari."""
    name = models.CharField(max_length=100)
    month = models.PositiveSmallIntegerField(help_text="Oy (1-12)")
    day = models.PositiveSmallIntegerField(help_text="Kun (1-31)")
    is_movable = models.BooleanField(
        default=False, help_text="Ramazon hayiti kabi ko'chuvchi bayram"
    )
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'notifications_holiday'
        ordering = ['month', 'day']

    def __str__(self):
        return f"{self.day}.{self.month} — {self.name}"


class Notification(BaseModel):
    """
    Foydalanuvchiga yuborilgan (yoki yuborilishi kerak) notification.
    FCM push token Device modelidan olinadi (apps.devices.models.device.Device).
    """
    class Kind(models.TextChoices):
        HOLIDAY = 'HOLIDAY', 'Bayram'
        ALLERGY = 'ALLERGY', 'Allergiya ogohlantirish'
        MENU = 'MENU', 'Menyu'
        UPDATE = 'UPDATE', 'Ilova yangilanishi'
        GENERAL = 'GENERAL', 'Umumiy'

    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='notifications'
    )
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.GENERAL)
    title = models.CharField(max_length=200)
    body = models.TextField()
    image_url = models.URLField(blank=True, help_text="Bildiruv bilan birga ko'rsatiladigan rasm")
    is_read = models.BooleanField(default=False, db_index=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'notifications_notification'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email}: {self.title}"
