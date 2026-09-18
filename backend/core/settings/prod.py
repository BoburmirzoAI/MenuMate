from .base import *
from core import config
from core.sentry import init_sentry

DEBUG = False
SECRET_KEY = config.SECRET_KEY
ALLOWED_HOSTS = config.ALLOWED_HOSTS

# Sentry — SENTRY_DSN env'da bo'lsa init qilinadi, aks holda o'tkazib yuboriladi.
init_sentry(
    dsn=config.SENTRY_DSN,
    environment=config.SENTRY_ENVIRONMENT,
    release=config.SENTRY_RELEASE or None,
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config.DB_NAME,
        'USER': config.DB_USER,
        'PASSWORD': config.DB_PASSWORD,
        'HOST': config.DB_HOST,
        'PORT': config.DB_PORT,
        'CONN_MAX_AGE': 0,
        'OPTIONS': {
            'sslmode': config.DB_SSLMODE,
        },
    }
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Redis cache — DRF throttling shu cache orqali hisoblanadi.
# Multi-worker gunicorn'da bir xil counter'ga ega bo'lish uchun majburiy.
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config.REDIS_CACHE_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
}
