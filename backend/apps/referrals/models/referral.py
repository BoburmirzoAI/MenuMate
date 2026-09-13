"""
Referral kod — har foydalanuvchining unique kodi.
Kim kimni taklif qilgani (ReferralUse) hozircha kerak emas.
"""
import secrets
import string

from django.conf import settings
from django.db import models

from apps.shared.models import BaseModel


class ReferralCode(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='referral_code_obj',
    )
    code = models.CharField(max_length=20, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'users_referral_code'
        verbose_name = 'Referral kod'
        verbose_name_plural = 'Referral kodlari'

    def __str__(self):
        return f"{self.code} ({self.user.email})"

    @classmethod
    def get_or_create_for(cls, user) -> 'ReferralCode':
        existing = cls.objects.filter(user=user).first()
        if existing:
            return existing
        while True:
            code = ''.join(
                secrets.choice(string.ascii_uppercase + string.digits)
                for _ in range(8)
            )
            if not cls.objects.filter(code=code).exists():
                return cls.objects.create(user=user, code=code)
