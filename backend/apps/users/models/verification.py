"""
Verification codes — email verification, phone verification, password reset.
"""
import secrets
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.shared.models import BaseModel


class VerificationCode(BaseModel):
    """
    Bir marotabalik kod: email tasdiqlash, telefon tasdiqlash yoki parolni tiklash.
    Kod 6-raqamli, 10 daqiqa amal qiladi.
    """

    class Purpose(models.TextChoices):
        EMAIL_VERIFY = 'EMAIL_VERIFY', 'Email tasdiqlash'
        PHONE_VERIFY = 'PHONE_VERIFY', 'Telefon tasdiqlash'
        PASSWORD_RESET = 'PASSWORD_RESET', 'Parolni tiklash'
        EMAIL_CHANGE = 'EMAIL_CHANGE', 'Emailni almashtirish'
        PHONE_CHANGE = 'PHONE_CHANGE', 'Telefonni almashtirish'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='verification_codes',
    )
    purpose = models.CharField(max_length=20, choices=Purpose.choices, db_index=True)
    code = models.CharField(max_length=6, db_index=True)

    # Kod qanday kanal orqali yuborilgan
    destination = models.CharField(
        max_length=255, help_text="Yuborilgan email yoki telefon raqami"
    )

    expires_at = models.DateTimeField(db_index=True)
    is_used = models.BooleanField(default=False, db_index=True)
    used_at = models.DateTimeField(null=True, blank=True)
    attempts = models.PositiveSmallIntegerField(
        default=0, help_text="Necha marta noto'g'ri kod kiritildi",
    )

    class Meta:
        db_table = 'users_verification_code'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'purpose', 'is_used']),
            models.Index(fields=['code', 'purpose']),
        ]

    def __str__(self):
        return f"{self.user.email} — {self.purpose} — {'used' if self.is_used else 'active'}"

    @property
    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at

    @property
    def is_valid(self) -> bool:
        return not self.is_used and not self.is_expired and self.attempts < 5

    def mark_used(self):
        self.is_used = True
        self.used_at = timezone.now()
        self.save(update_fields=['is_used', 'used_at'])

    @classmethod
    def generate(cls, user, purpose: str, destination: str,
                 lifetime_minutes: int = 10) -> 'VerificationCode':
        """Yangi kod yaratadi. Eski shu maqsaddagi kodlarni bekor qiladi."""
        cls.objects.filter(
            user=user, purpose=purpose, is_used=False,
        ).update(is_used=True, used_at=timezone.now())

        code = ''.join(str(secrets.randbelow(10)) for _ in range(6))
        return cls.objects.create(
            user=user,
            purpose=purpose,
            code=code,
            destination=destination,
            expires_at=timezone.now() + timedelta(minutes=lifetime_minutes),
        )

    def verify(self, code: str) -> bool:
        """Kodni tekshiradi. To'g'ri bo'lsa ishlatilgan deb belgilaydi."""
        if not self.is_valid:
            return False
        if self.code != code:
            self.attempts += 1
            self.save(update_fields=['attempts'])
            return False
        self.mark_used()
        return True
