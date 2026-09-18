import os
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()

env_path = os.path.join(BASE_DIR, '.env')
if not os.path.exists(env_path):
    env_path = os.path.join(BASE_DIR.parent, '.env')

if os.path.exists(env_path):
    environ.Env.read_env(env_path)
else:
    print("⚠️  Warning: .env file not found!")

# DJANGO CORE
DJANGO_SETTINGS_MODULE = env.str('DJANGO_SETTINGS_MODULE', default='core.settings.dev')
SECRET_KEY = env.str('SECRET_KEY', default='unsafe-secret-key')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# DATABASE
DB_NAME = env.str('DB_NAME', default='menu_mate')
DB_USER = env.str('DB_USER', default='postgres')
DB_PASSWORD = env.str('DB_PASSWORD', default='postgres')
DB_HOST = env.str('DB_HOST', default='127.0.0.1')
DB_PORT = env.str('DB_PORT', default='5432')
DB_SSLMODE = env.str('DB_SSLMODE', default='prefer')

# Redis (Celery + cache)
REDIS_HOST = env.str('REDIS_HOST', default='127.0.0.1')
REDIS_PORT = env.str('REDIS_PORT', default='6379')
CELERY_BROKER_URL = env.str(
    'CELERY_BROKER_URL',
    default=f'redis://{REDIS_HOST}:{REDIS_PORT}/2',
)
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND', default='django-db')
REDIS_CACHE_URL = env.str(
    'REDIS_CACHE_URL',
    default=f'redis://{REDIS_HOST}:{REDIS_PORT}/1',
)

# External APIs
OPENWEATHER_API_KEY = env.str('OPENWEATHER_API_KEY', default='')
FCM_SERVER_KEY = env.str('FCM_SERVER_KEY', default='')

# Firebase Admin SDK — Service Account JSON fayl yo'li (yoki inline JSON string).
# Yo'l bo'sh bo'lsa push yuborilmaydi (loglanadi), tizim boshqa aspektlarda ishlayveradi.
FIREBASE_SERVICE_ACCOUNT_PATH = env.str(
    'FIREBASE_SERVICE_ACCOUNT_PATH',
    default='/app/firebase-service-account.json',
)
# Kelajakda "Menu tuzilgan" yoki "Bayram bugun" kabi avtomatik push'lar
# xohishga qarab yoqilib/o'chirilishi uchun feature flag.
PUSH_NOTIFICATIONS_ENABLED = env.bool('PUSH_NOTIFICATIONS_ENABLED', default=True)

# Karzinka Go (Yandex Lavka B2B API) — Proxymandan olingan JWT token va koordinata.
# Token ~1 soatda tugaydi; qayta yig'ish uchun Proxyman'dan yangi webviewtoken oling.
KARZINKA_LAVKA_TOKEN = env.str('KARZINKA_LAVKA_TOKEN', default='')
KARZINKA_LAVKA_YAUID = env.str('KARZINKA_LAVKA_YAUID', default='')
KARZINKA_LAVKA_GEOID = env.str('KARZINKA_LAVKA_GEOID', default='')
KARZINKA_LAVKA_SESSION_ID = env.str('KARZINKA_LAVKA_SESSION_ID', default='')
KARZINKA_LAVKA_LAT = env.float('KARZINKA_LAVKA_LAT', default=41.2694820819372)
KARZINKA_LAVKA_LON = env.float('KARZINKA_LAVKA_LON', default=69.24657079428343)

# Telegram (for error alerts)
TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN', default='')
TELEGRAM_CHANNEL_ID = env.str('TELEGRAM_CHANNEL_ID', default='')

# Sentry (xato monitoringi) — DSN bo'sh bo'lsa Sentry yoqilmaydi.
SENTRY_DSN = env.str('SENTRY_DSN', default='')
SENTRY_ENVIRONMENT = env.str('SENTRY_ENVIRONMENT', default='production')
SENTRY_RELEASE = env.str('SENTRY_RELEASE', default='')
