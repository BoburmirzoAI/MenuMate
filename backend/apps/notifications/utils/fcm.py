"""
Firebase Cloud Messaging (FCM) — push notification'lar uchun yuborish qatlami.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Loyihaga qanday integratsiyalangan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 1. Firebase project'ida Service Account key olinadi (JSON), fayl loyihaga
    `firebase-service-account.json` sifatida qo'yiladi (git'ga tushmaydi).
 2. `settings.FIREBASE_SERVICE_ACCOUNT_PATH` shu faylga qaratadi.
 3. `initialize_firebase()` — Django ilk yuklanishida bir marta chaqiriladi
    (`apps.py:ready()` orqali).
 4. `send_to_token(...)` / `send_multicast(...)` funksiyalari boshqa app'lardan
    chaqiriladi. Xato tokenlar avtomatik `Device.is_active=False` qilinadi.
 5. Har real yuborish `Celery` task orqali async bo'ladi (`tasks.py`).
    Bu joyda esa sinxron ishlaydigan asos qatlam.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Xatolar bilan ishlash
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 Firebase quyidagi xatolarni qaytaradi:
   - UNREGISTERED / NOT_FOUND — token endi mavjud emas (foydalanuvchi ilovani
     olib tashladi yoki qayta o'rnatdi). Qurilma o'chirilib qo'yilishi kerak.
   - INVALID_ARGUMENT — token noto'g'ri formatda. Xuddi shunday, o'chirib qo'yish.
   - SENDER_ID_MISMATCH — bu FCM Server bilan mos kelmayapti. Konfiguratsiya
     muammosi; xato loglanadi, foydalanuvchi qurilmasi tegilmaydi.
   - Boshqa xatolar (network, quota) — retry qilinadi (Celery orqali).
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any

from django.conf import settings

logger = logging.getLogger(__name__)

_firebase_initialized = False


@dataclass(frozen=True)
class FcmResult:
    """Bir yuborish urinishining natijasi."""
    success_count: int
    failure_count: int
    invalid_tokens: list[str]
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None and self.success_count > 0


def initialize_firebase() -> bool:
    """Firebase Admin SDK'ni bir marta init qiladi.

    Success bo'lsa ham, xato bo'lsa ham qayta chaqirilsa ish qilmaydi.
    Return: True — SDK tayyor; False — konfigi yo'q yoki xato bo'ldi.
    """
    global _firebase_initialized
    if _firebase_initialized:
        return True

    try:
        import firebase_admin
        from firebase_admin import credentials
    except ImportError:
        logger.warning(
            "firebase-admin paket o'rnatilmagan. Push notification o'chirilgan.",
        )
        return False

    if firebase_admin._apps:  # noqa: SLF001 (yopiq atribut, boshqa yo'l yo'q)
        _firebase_initialized = True
        return True

    path = getattr(settings, 'FIREBASE_SERVICE_ACCOUNT_PATH', '')
    if not path or not os.path.exists(path):
        logger.warning(
            "FIREBASE_SERVICE_ACCOUNT_PATH topilmadi (%s). "
            "Push notification'lar yuborilmaydi.",
            path or '<bo\'sh>',
        )
        return False

    try:
        cred = credentials.Certificate(path)
        firebase_admin.initialize_app(cred)
        _firebase_initialized = True
        logger.info("Firebase Admin SDK ishga tushirildi (%s)", path)
        return True
    except Exception as exc:  # pragma: no cover
        logger.exception("Firebase init xatosi: %s", exc)
        return False


def _is_push_enabled() -> bool:
    """Feature flag va Firebase mavjudligi tekshiruvi."""
    if not getattr(settings, 'PUSH_NOTIFICATIONS_ENABLED', True):
        return False
    return initialize_firebase()


def _build_message(
    *,
    title: str,
    body: str,
    data: dict[str, str] | None,
    image_url: str = '',
) -> Any:
    """Firebase Message obyektini yasaydi (multi-platform)."""
    from firebase_admin import messaging

    notification_kwargs: dict[str, Any] = {'title': title, 'body': body}
    if image_url:
        notification_kwargs['image'] = image_url

    android = messaging.AndroidConfig(
        priority='high',
        notification=messaging.AndroidNotification(
            title=title,
            body=body,
            sound='default',
            channel_id='menumate_default',
            **({'image': image_url} if image_url else {}),
        ),
    )

    apns_payload = messaging.APNSPayload(
        aps=messaging.Aps(
            alert=messaging.ApsAlert(title=title, body=body),
            sound='default',
            content_available=True,
        ),
    )
    apns = messaging.APNSConfig(payload=apns_payload)

    # FCM data payload'da barcha qiymatlar str bo'lishi shart.
    string_data: dict[str, str] = {}
    for k, v in (data or {}).items():
        if v is None:
            continue
        string_data[str(k)] = str(v)

    return messaging.Message(
        notification=messaging.Notification(**notification_kwargs),
        android=android,
        apns=apns,
        data=string_data,
    )


def send_to_token(
    token: str,
    *,
    title: str,
    body: str,
    data: dict[str, str] | None = None,
    image_url: str = '',
) -> FcmResult:
    """Bitta tokenga xabar yuborish (sinxron)."""
    if not token:
        return FcmResult(0, 0, [], error='EMPTY_TOKEN')

    if not _is_push_enabled():
        return FcmResult(0, 0, [], error='PUSH_DISABLED')

    from firebase_admin import messaging
    from firebase_admin import exceptions as fb_exceptions

    message = _build_message(title=title, body=body, data=data, image_url=image_url)
    message.token = token  # type: ignore[attr-defined]

    try:
        messaging.send(message)
        return FcmResult(1, 0, [])
    except messaging.UnregisteredError:
        logger.info("FCM token endi mavjud emas: %s...", token[:20])
        return FcmResult(0, 1, [token], error='UNREGISTERED')
    except (fb_exceptions.InvalidArgumentError, ValueError) as exc:
        logger.info("FCM token noto'g'ri: %s...  (%s)", token[:20], exc)
        return FcmResult(0, 1, [token], error='INVALID_ARGUMENT')
    except Exception as exc:  # pragma: no cover
        logger.exception("FCM send xatosi: %s", exc)
        return FcmResult(0, 1, [], error='UNKNOWN')


def send_multicast(
    tokens: list[str],
    *,
    title: str,
    body: str,
    data: dict[str, str] | None = None,
    image_url: str = '',
) -> FcmResult:
    """Ko'p tokenga bir vaqtda yuborish. FCM chekkasi — 500 token per batch."""
    tokens = [t for t in tokens if t]
    if not tokens:
        return FcmResult(0, 0, [])

    if not _is_push_enabled():
        return FcmResult(0, 0, [], error='PUSH_DISABLED')

    from firebase_admin import messaging

    total_success = 0
    total_failure = 0
    invalid_tokens: list[str] = []

    # FCM'ning `send_each_for_multicast` — batch limit 500.
    BATCH = 500
    for start in range(0, len(tokens), BATCH):
        batch_tokens = tokens[start:start + BATCH]
        message = _build_message(title=title, body=body, data=data, image_url=image_url)

        multicast = messaging.MulticastMessage(
            tokens=batch_tokens,
            notification=message.notification,
            android=message.android,
            apns=message.apns,
            data=message.data,
        )
        try:
            response = messaging.send_each_for_multicast(multicast)
        except Exception as exc:  # pragma: no cover
            logger.exception("FCM multicast xatosi: %s", exc)
            total_failure += len(batch_tokens)
            continue

        total_success += response.success_count
        total_failure += response.failure_count

        for idx, resp in enumerate(response.responses):
            if resp.success:
                continue
            error = resp.exception
            token = batch_tokens[idx]
            # Faqat qayta ishlatib bo'lmaydigan xatolarda tokenni o'chiramiz.
            if isinstance(error, messaging.UnregisteredError):
                invalid_tokens.append(token)
            elif error and getattr(error, 'code', '') in {
                'INVALID_ARGUMENT', 'invalid-argument',
            }:
                invalid_tokens.append(token)

    return FcmResult(
        success_count=total_success,
        failure_count=total_failure,
        invalid_tokens=invalid_tokens,
    )


def deactivate_invalid_tokens(tokens: list[str]) -> int:
    """Yaroqsiz FCM tokenlar bilan bog'liq qurilmalarni o'chirib qo'yadi.

    Foydalanuvchi ilovani qayta o'rnatsa yangi token bilan qayta ro'yxatga oladi.
    """
    if not tokens:
        return 0

    from apps.devices.models.device import Device

    return Device.objects.filter(fcm_token__in=tokens).update(
        fcm_token='',
        is_active=False,
    )
