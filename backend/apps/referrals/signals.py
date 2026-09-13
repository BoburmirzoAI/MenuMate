"""
Referrals app signals.
Har yangi User uchun avtomatik ReferralCode yaratamiz.
"""
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.referrals.models.referral import ReferralCode


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_referral_code(sender, instance, created, **kwargs):
    if created:
        ReferralCode.get_or_create_for(instance)
