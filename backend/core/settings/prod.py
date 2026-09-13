from .base import *
from core import config

DEBUG = False
SECRET_KEY = config.SECRET_KEY
ALLOWED_HOSTS = config.ALLOWED_HOSTS

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
