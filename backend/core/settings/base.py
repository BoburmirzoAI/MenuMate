"""
Base Django settings for Menu Mate project.

Shared configuration. Environment-specific overrides live in:
- core/settings/dev.py
- core/settings/prod.py
"""
from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab

# -------------------------------------------------------------------
# PATHS
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------------------
# APPLICATIONS
# -------------------------------------------------------------------

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'drf_spectacular',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_celery_beat',
    'django_celery_results',
    'corsheaders',
]

MY_APPS = [
    'apps.shared',
    'apps.permissions',
    'apps.users',
    'apps.devices',
    'apps.referrals',
    'apps.family',
    'apps.recipes',
    'apps.menu',
    'apps.products',
    'apps.weather',
    'apps.notifications',
]

INSTALLED_APPS += THIRD_PARTY_APPS
INSTALLED_APPS += MY_APPS

# -------------------------------------------------------------------
# MIDDLEWARE
# -------------------------------------------------------------------

MIDDLEWARE = [
    # corsheaders CommonMiddleware'dan OLDIN turishi shart (CORS spec talab)
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.shared.middlewares.permission.EndpointPermissionMiddleware',
]

# -------------------------------------------------------------------
# URLS / WSGI
# -------------------------------------------------------------------

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

# -------------------------------------------------------------------
# TEMPLATES
# -------------------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# -------------------------------------------------------------------
# AUTH / PASSWORDS
# -------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------------------------------------------
# INTERNATIONALIZATION
# -------------------------------------------------------------------
LANGUAGE_CODE = 'uz'
LANGUAGES = (
    ('uz', 'Uzbek'),
    ('ru', 'Russian'),
    ('en', 'English'),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz'
MODELTRANSLATION_LANGUAGES = ('uz', 'ru', 'en')
MODELTRANSLATION_FALLBACK_LANGUAGES = ('uz', 'en', 'ru')

LOCALE_PATHS = (BASE_DIR / 'locale',)

TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------
# STATIC & MEDIA
# -------------------------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.parent / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.parent / 'media'

# -------------------------------------------------------------------
# DEFAULT PRIMARY KEY
# -------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

# -------------------------------------------------------------------
# DJANGO REST FRAMEWORK
# -------------------------------------------------------------------

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'PAGE_SIZE': 20,
    'EXCEPTION_HANDLER': 'apps.shared.exceptions.handler.custom_exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'apps.shared.utils.custom_pagination.CustomPageNumberPagination',

    # ── Rate limiting (per-view scoped throttles + global anon/user limitlari) ──
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/min',
        'user': '300/min',
        'login': '5/min',
        'register': '5/hour',
        'password': '5/hour',
        'menu_generate': '5/min',
        'broadcast': '10/hour',
    },
}

# -------------------------------------------------------------------
# DRF SPECTACULAR
# -------------------------------------------------------------------

SPECTACULAR_SETTINGS = {
    'TITLE': 'Menu Mate | Family Menu Planner',
    'DESCRIPTION': 'Oilaviy menyu rejalashtiruvchi ilova uchun REST API',
    'VERSION': '1.0.0',
}

# -------------------------------------------------------------------
# SIMPLEJWT
# -------------------------------------------------------------------

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
}

# -------------------------------------------------------------------
# CELERY
# -------------------------------------------------------------------

from core import config as _cfg

CELERY_BROKER_URL = _cfg.CELERY_BROKER_URL
CELERY_RESULT_BACKEND = _cfg.CELERY_RESULT_BACKEND

OPENWEATHER_API_KEY = _cfg.OPENWEATHER_API_KEY
FCM_SERVER_KEY = _cfg.FCM_SERVER_KEY
FIREBASE_SERVICE_ACCOUNT_PATH = _cfg.FIREBASE_SERVICE_ACCOUNT_PATH
PUSH_NOTIFICATIONS_ENABLED = _cfg.PUSH_NOTIFICATIONS_ENABLED

KARZINKA_LAVKA_TOKEN = _cfg.KARZINKA_LAVKA_TOKEN
KARZINKA_LAVKA_YAUID = _cfg.KARZINKA_LAVKA_YAUID
KARZINKA_LAVKA_GEOID = _cfg.KARZINKA_LAVKA_GEOID
KARZINKA_LAVKA_SESSION_ID = _cfg.KARZINKA_LAVKA_SESSION_ID
KARZINKA_LAVKA_LAT = _cfg.KARZINKA_LAVKA_LAT
KARZINKA_LAVKA_LON = _cfg.KARZINKA_LAVKA_LON

TELEGRAM_BOT_TOKEN = _cfg.TELEGRAM_BOT_TOKEN
TELEGRAM_CHANNEL_ID = _cfg.TELEGRAM_CHANNEL_ID
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_BEAT_SCHEDULE = {
    'menu-roll-over-daily': {
        'task': 'menu.roll_over_menus',
        'schedule': crontab(hour=1, minute=0),
    },
}
