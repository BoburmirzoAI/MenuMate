"""
Sentry initsializatsiyasi — xato monitoringi.

`SENTRY_DSN` sozlanmagan bo'lsa hech narsa qilmaydi (masalan, dev muhitida
yoki test paytida). Faqat bir marta chaqirilishi kerak — settings faylining
oxirida.
"""
import logging

try:
    import sentry_sdk
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    from sentry_sdk.integrations.redis import RedisIntegration
    _SENTRY_AVAILABLE = True
except ImportError:
    _SENTRY_AVAILABLE = False

logger = logging.getLogger(__name__)


def init_sentry(*, dsn: str, environment: str = 'production', release: str | None = None) -> bool:
    """
    Sentry SDK'ni ishga tushirish.

    Args:
        dsn: Sentry loyihasining DSN URL'i. Bo'sh bo'lsa init o'tkazib yuboriladi.
        environment: 'production' | 'staging' | 'development'.
        release: (ixtiyoriy) app versiyasi — release tracking uchun.

    Returns:
        True — Sentry yoqildi; False — o'tkazib yuborildi.
    """
    if not dsn:
        return False

    if not _SENTRY_AVAILABLE:
        logger.warning("sentry-sdk o'rnatilmagan — Sentry init o'tkazib yuborildi.")
        return False

    sentry_logging = LoggingIntegration(
        level=logging.INFO,
        event_level=logging.ERROR,
    )

    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        release=release,
        integrations=[
            DjangoIntegration(
                transaction_style='url',
                middleware_spans=True,
                signals_spans=False,
            ),
            CeleryIntegration(monitor_beat_tasks=True),
            RedisIntegration(),
            sentry_logging,
        ],
        traces_sample_rate=0.1,
        send_default_pii=False,
        request_bodies='small',
    )
    return True
