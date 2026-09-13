# Menu Mate — Backend

Family Menu Planner uchun Django REST API.

## Struktura

```
backend/
├── core/                    # Django project
│   ├── settings/            # base.py, dev.py, prod.py
│   ├── urls.py
│   ├── wsgi.py, asgi.py
│   ├── celery.py
│   └── config.py            # .env dan sozlamalar
├── apps/
│   ├── shared/              # BaseModel, Media, exceptions, messages, utils
│   ├── users/               # Foydalanuvchi, JWT auth
│   ├── family/              # Oila profili, a'zolar, sog'liq holati
│   ├── recipes/             # Retseptlar, ingredientlar, allergen tags
│   ├── menu/                # Menu, MenuDay, MenuMeal (algoritm)
│   ├── products/            # Xarid ro'yxati (menyudan hisoblanadi)
│   ├── weather/             # OpenWeatherMap integratsiyasi
│   ├── notifications/       # Bayramlar, FCM, push notification
│   └── urls/v1.py           # Barcha v1 endpointlar
├── locale/
├── manage.py
├── pyproject.toml
└── .env
```

## O'rnatish

```bash
cd backend
poetry install
# yoki
pip install django djangorestframework djangorestframework-simplejwt django-environ psycopg2-binary drf-spectacular django-modeltranslation django-redis celery django-celery-results django-celery-beat requests phonenumbers pytelegrambotapi
```

## Ma'lumotlar bazasi

`.env` faylida:
```
DB_NAME=menu_mate
DB_USER=<sizning postgres user>
DB_PASSWORD=<parol>
DB_HOST=127.0.0.1
DB_PORT=5432
```

Postgres ichida DB yaratish:
```bash
createdb menu_mate
```

## Ishga tushirish

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API endpointlar

- Swagger: `http://127.0.0.1:8000/api/v1/docs/`
- Admin: `http://127.0.0.1:8000/admin/`

### Asosiy endpointlar
```
POST /api/v1/users/register/
POST /api/v1/users/login/
POST /api/v1/users/refresh/

GET  /api/v1/family/
POST /api/v1/family/members/

GET  /api/v1/recipes/
POST /api/v1/menu/generate/
GET  /api/v1/menu/{id}/
GET  /api/v1/menu/{id}/products/

GET  /api/v1/weather/
GET  /api/v1/notifications/holidays/
```
