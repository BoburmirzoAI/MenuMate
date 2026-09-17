"""
Notification signal'lari.

`Notification` obyekti yaratilganda avtomatik push yuboradi. Boshqa app'larda
(masalan `apps.menu`) `Notification.objects.create(...)` chaqirish yetarli —
push tomonga bog'lanish shu joyda bir marta.

Signal orqali — DB rollback bo'lsa push ham yuborilmaydi (transaction on_commit
bilan mustahkam integratsiya). Async — Celery orqali.
"""
from __future__ import annotations

import logging

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notifications.models.notifications import Notification

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Notification)
def dispatch_push_on_create(sender, instance: Notification, created: bool, **_kwargs):
    """Yangi Notification yaratilganda push yuboriladi.

    - Faqat yangi yozuv uchun.
    - `sent_at` allaqachon to'ldirilgan bo'lsa (misol: import) — o'tkazib yuboramiz.
    - Foydalanuvchi push'ni o'chirgan bo'lsa (`is_push_enabled=False`) yubormaymiz.
    """
    if not created:
        return
    if instance.sent_at is not None:
        return

    user = instance.user
    if user is None or not getattr(user, 'is_push_enabled', True):
        return

    tokens = list(
        user.devices.filter(is_active=True)
        .exclude(fcm_token='')
        .values_list('fcm_token', flat=True)
    )
    if not tokens:
        return

    payload = {
        'notification_id': instance.id,
        'kind': instance.kind,
    }

    # DB commit tugagach yuboramiz — rollback bo'lsa push ham ketmaydi.
    def _enqueue() -> None:
        from apps.notifications.tasks import send_push_multicast

        send_push_multicast.delay(
            tokens,
            title=instance.title,
            body=instance.body,
            data=payload,
            image_url=instance.image_url or '',
        )
        logger.info(
            "Push queued: notification=%s, user=%s, tokens=%d",
            instance.id, user.email, len(tokens),
        )

    transaction.on_commit(_enqueue)
