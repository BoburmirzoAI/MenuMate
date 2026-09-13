"""
Device — foydalanuvchining qurilmasi (soddalashtirilgan).
Faqat push notification uchun kerakli fields.
"""
from django.conf import settings
from django.db import models

from apps.shared.models import BaseModel, DeviceType


class Device(BaseModel):
    """Har foydalanuvchi qurilmasi push notification uchun."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='devices',
        db_index=True,
    )
    device_id = models.CharField(
        max_length=255, db_index=True,
        help_text="Mobile ilova bergan unique ID",
    )
    device_type = models.CharField(
        max_length=10, choices=DeviceType.choices,
        default=DeviceType.ANDROID,
    )
    fcm_token = models.CharField(max_length=500, blank=True, db_index=True)
    app_version = models.CharField(
        max_length=20, blank=True,
        help_text="Foydalanuvchi ilovasining versiyasi (masalan 1.2.3)",
    )
    is_active = models.BooleanField(default=True, db_index=True)
    last_login = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users_device'
        ordering = ['-last_login']
        indexes = [
            models.Index(fields=['user', 'is_active']),
        ]
        unique_together = ('user', 'device_id')

    def __str__(self):
        return f"{self.user.email} — {self.device_type} ({self.device_id[:8]})"
