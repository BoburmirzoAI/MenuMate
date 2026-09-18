"""
Sentry initsializatsiyasi — xato monitoringi.

`SENTRY_DSN` sozlanmagan bo'lsa hech narsa qilmaydi (masalan, dev muhitida
yoki test paytida). Faqat bir marta chaqirilishi kerak — settings faylidan
oxirida.
"""
import logging

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

    try:
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration
        from sentry_sdk.integrations.celery import CeleryIntegration
        from sentry_sdk.integrations.redis import RedisIntegration
        from sentry_sdk.integrations.logging import LoggingIntegration
    except ImportError:
        logger.warning("sentry-sdk o'rnatilmagan — Sentry init o'tkazib yuborildi.")
        return False

    sentry_logging = LoggingIntegration(
        level=logging.INFO,        # breadcrumb sifatida INFO+ yig'iladi
        event_level=logging.ERROR, # Sentry'ga faqat ERROR+ yuboriladi
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
        # Performance monitoring — kichik ulush (production'da yuklamani oshirmaslik uchun)
        traces_sample_rate=0.1,
        # PII yuborilmaydi (email/parol Sentry'ga bormasin)
        send_default_pii=False,
        # Nozik ma'lumotlarni scrub qiladi (default 'True' — profilaktik)
        request_bodies='small',
    )
    return True
