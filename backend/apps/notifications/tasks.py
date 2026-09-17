"""
Push notification Celery task'lari.

Sinxron `fcm.py` funksiyalari orqali push yuboradi, xato bo'lgan qurilmalar
tokenini tozalab qo'yadi. Async bo'lganda — HTTP request yuborilib, javob kutmaydi.
"""
from __future__ import annotations

import logging
from typing import Any

from celery import shared_task

from apps.notifications.utils.fcm import (
    deactivate_invalid_tokens,
    send_multicast,
    send_to_token,
)

logger = logging.getLogger(__name__)


@shared_task(name='notifications.send_push_to_token', bind=True, max_retries=3)
def send_push_to_token(
    self,
    token: str,
    *,
    title: str,
    body: str,
    data: dict[str, Any] | None = None,
    image_url: str = '',
    notification_id: int | None = None,
) -> dict[str, Any]:
    """
    Bitta tokenga push yuborish.

    `notification_id` — DB'dagi `Notification` obyektining ID'si (bo'lsa yangilaymiz:
    `sent_at` maydonini beramiz).
    """
    result = send_to_token(
        token, title=title, body=body, data=data or {}, image_url=image_url,
    )

    if result.invalid_tokens:
        deactivate_invalid_tokens(result.invalid_tokens)

    if not result.ok and result.error not in {'PUSH_DISABLED', 'EMPTY_TOKEN'}:
        # Retry — quota yoki tarmoq muammosi
        if result.error not in {'UNREGISTERED', 'INVALID_ARGUMENT'}:
            raise self.retry(countdown=60, max_retries=3)

    if notification_id and result.ok:
        _mark_sent(notification_id)

    return {
        'success_count': result.success_count,
        'failure_count': result.failure_count,
        'error': result.error,
    }


@shared_task(name='notifications.send_push_multicast', bind=True, max_retries=2)
def send_push_multicast(
    self,
    tokens: list[str],
    *,
    title: str,
    body: str,
    data: dict[str, Any] | None = None,
    image_url: str = '',
) -> dict[str, Any]:
    """Ko'p qurilmaga bir vaqtda push (broadcast)."""
    result = send_multicast(
        tokens, title=title, body=body, data=data or {}, image_url=image_url,
    )

    if result.invalid_tokens:
        removed = deactivate_invalid_tokens(result.invalid_tokens)
        logger.info(
            "FCM: %d ta yaroqsiz token o'chirildi (batch: %d ta)",
            removed, len(tokens),
        )

    return {
        'success_count': result.success_count,
        'failure_count': result.failure_count,
        'invalid_count': len(result.invalid_tokens),
    }


def _mark_sent(notification_id: int) -> None:
    """Yuborilgan Notification'ning `sent_at`ini yozib qo'yadi."""
    from django.utils import timezone
    from apps.notifications.models.notifications import Notification

    Notification.objects.filter(id=notification_id).update(sent_at=timezone.now())
