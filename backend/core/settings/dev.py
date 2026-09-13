from core import config
from .base import *

DEBUG = True
SECRET_KEY = config.SECRET_KEY
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config.DB_NAME,
        'USER': config.DB_USER,
        'PASSWORD': config.DB_PASSWORD,
        'HOST': config.DB_HOST,
        'PORT': config.DB_PORT,
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config.REDIS_CACHE_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# --- CORS (dev — hamma origin'ga ruxsat) ---
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_HEADERS = [
    'accept', 'accept-language', 'authorization', 'content-type',
    'origin', 'user-agent', 'x-requested-with',
]
