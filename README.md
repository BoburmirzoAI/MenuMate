# 🍽️ Menu Mate

**Family meal planner.** An intelligent system that automatically generates
weekly or monthly meal menus tailored to each family member's dietary
restrictions, health conditions, and preferences — then produces a categorized
shopping list for what you actually need to buy.

Built as a full-stack platform: a Django REST API, a Flutter mobile app, and a
React admin panel — everything runs from a single `docker compose up`.

---

## ✨ Features

- 🧠 **Smart menu generation** — 7 or 30-day plans that respect allergies,
  diabetes, halal/vegan requirements, weather, and holidays
- 👨‍👩‍👧 **Family profiles** — each member has their own allergies, liked/disliked
  recipes, and health conditions (22 predefined conditions across 5 categories)
- 📖 **Recipe library** — 35 Uzbek and international recipes with 3-language
  support (Uzbek, Russian, English)
- 🛒 **Shopping list** — automatically calculated from the menu, grouped by
  category (meat, dairy, vegetables, spices, etc.) with unit conversions
- 🖼️ **Automatic images** — recipe and ingredient photos are fetched live from
  Wikipedia + Korzinka catalogs; nothing needs to be uploaded manually
- 🌤️ **Weather-aware** — hot summer days get lighter meals; cold days get soups
- 🎉 **Holiday-aware** — 10 Uzbek holidays trigger special menu suggestions
- 🔔 **Push notifications** via FCM
- 🌍 **Full i18n** — every string, error message, and recipe available in
  Uzbek / Russian / English (backend uses `django-modeltranslation`, mobile
  uses a custom string map, admin honors `Accept-Language`)

---

## 🏗️ Architecture

```
Menu Mate/
├── backend/          # Django 5 + DRF — 12 apps, 40+ endpoints
├── mobile/           # Flutter — ~20 screens, feature-first
├── admin/            # React 19 + Vite + TypeScript — web admin panel
├── deploy/           # nginx.conf for production
├── docker-compose.yml
├── docker-compose.prod.yml
├── Makefile
└── .github/workflows/  # CI/CD (backend-ci, docker-build, deploy)
```

### Tech stack

| Layer     | Stack |
|-----------|-------|
| Backend   | Django 5, DRF, PostgreSQL 16, Redis, Celery, JWT (SimpleJWT) |
| Mobile    | Flutter 3, Riverpod, Dio, go_router, secure_storage |
| Admin     | React 19, Vite 6, TypeScript 5.7, Zustand, TanStack Query, CSS Modules |
| Infra     | Docker Compose, GitHub Actions, Nginx |
| External  | OpenWeatherMap (weather), Wikipedia (images), Karzinka Go (products) |

---

## ⚡ Quick start

**Requirements:** Docker, Docker Compose, `make`

```bash
# 1. Clone
git clone <repo-url> menu-mate
cd menu-mate

# 2. Configure environment
cp .env.example .env
# Open .env and fill in SECRET_KEY, OPENWEATHER_API_KEY, etc.

# 3. Boot the whole stack
make init                # build + up + migrate + sync-endpoints
make superuser           # create Django admin user
```

That single `make init` brings up Postgres, Redis, the API, Celery worker and
beat. On first boot, a Celery `worker_ready` signal auto-loads all fixtures —
35 recipes, 73 ingredients, 22 health conditions, 10 holidays — so the system
is instantly usable.

**Open:**
- 🌐 REST API — http://localhost:8000/api/v1/
- 📚 Swagger UI — http://localhost:8000/api/v1/docs/
- 🔧 Django Admin — http://localhost:8000/admin/

### Admin panel (React)

```bash
cd admin
cp .env.example .env
npm install
npm run dev              # http://localhost:5173
```

### Mobile app (Flutter)

```bash
cd mobile
flutter pub get
flutter run              # pick a device / simulator
```

---

## 🛠️ Common commands

```bash
make help                # list all commands

make up                  # start services
make down                # stop
make logs                # tail backend logs
make shell               # exec into backend container
make dj-shell            # Django shell
make migrate             # apply migrations
make makemigrations
make test                # run backend tests
make db-backup           # snapshot the database
```

---

## 🐳 Docker services

| Service        | Port  | Purpose                    |
|----------------|-------|----------------------------|
| `backend`      | 8000  | Django REST API            |
| `db`           | 5433  | PostgreSQL 16              |
| `redis`        | 6379  | Cache + Celery broker      |
| `celery`       | —     | Async task worker          |
| `celery_beat`  | —     | Cron scheduler             |
| `pgadmin`      | 5051  | Postgres GUI (dev only)    |

Production adds an `nginx` reverse proxy for TLS termination and static files.

---

## 📡 API surface (40+ endpoints)

| Domain | Highlights |
|--------|------------|
| `/users/` | register, login, refresh, forgot/reset password, email verification, profile CRUD, soft-delete |
| `/family/` | family + members + health conditions |
| `/recipes/` | 35 recipes with filters (category, season, allergens, search) |
| `/menu/` | generate, list, clear, per-day stats, meal swap |
| `/products/` | auto-generated shopping list per menu, toggle purchased |
| `/weather/` | OpenWeatherMap wrapper with 3h Redis cache |
| `/notifications/` | user notifications + 10 holidays + upcoming |
| `/devices/` | device registration for FCM push |

All responses follow a uniform envelope:

```json
{ "success": true, "id": "MENU_GENERATED", "message": "...", "data": { ... } }
```

Error responses swap `data` for `errors` and use the same shape — so the mobile
and admin clients handle every error the same way.

---

## 🚀 Deployment

Three GitHub Actions pipelines under `.github/workflows/`:

1. **`backend-ci.yml`** — lint + tests on every push
2. **`docker-build.yml`** — pushes to `main` build and publish a Docker image
   to GitHub Container Registry
3. **`deploy.yml`** — SSH-based deploy to the production server

Required GitHub Secrets:

```
DEPLOY_HOST         # server IP or domain
DEPLOY_USER         # SSH user
DEPLOY_SSH_KEY      # SSH private key
DEPLOY_PATH         # project path on the server
```

---

## 📜 License & author

Built by **Boburmirzo Sobirjonov**, 2026. Internship project.
