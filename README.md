# 🍽️ Menu Mate

Family Menu Planner — oilaviy ovqat menyu rejalashtiruvchi ilova.

Oila a'zolarining ovqat xohishi, allergiyasi va sog'liq holatiga qarab avtomatik
haftalik yoki oylik menyu tuzuvchi, kerakli mahsulotlarni hisoblab beruvchi tizim.

## 🏗️ Arxitektura

```
Menu Mate/
├── backend/          # Django REST API (Python)
├── mobile/           # Flutter mobil ilova (Dart)
├── admin/            # Admin panel (React yoki Django admin)
├── deploy/           # nginx.conf va boshqa deploy fayllari
├── docker-compose.yml
├── docker-compose.prod.yml
├── Makefile
└── .github/workflows/  # CI/CD
```

## ⚡ Tez ishga tushirish

**Talab qilinadi:** Docker + Docker Compose, `make`

```bash
# 1. Repository'ni klonlash
git clone <repo-url> menu-mate
cd menu-mate

# 2. Environment sozlash
cp .env.example .env
# .env faylini ochib parol va API keylarni to'ldiring

# 3. Barcha servislarni ishga tushirish
make init         # build + up + migrate + sync-endpoints
make superuser    # admin foydalanuvchi yaratish
```

**Ochish:**
- 🌐 Backend API: http://localhost:8000
- 📚 Swagger docs: http://localhost:8000/api/v1/docs/
- 🔧 Django Admin: http://localhost:8000/admin/

## 🛠️ Ko'p ishlatiladigan buyruqlar

```bash
make help              # barcha buyruqlar ro'yxati

make up                # servislarni ishga tushirish
make down              # to'xtatish
make logs              # backend loglar
make shell             # backend container ichiga kirish
make dj-shell          # Django shell
make migrate           # migration
make makemigrations
make test              # testlar
make db-backup         # DB backup
```

## 🐳 Docker stack

Development'da 4 ta container ishlaydi:

| Servis     | Port  | Vazifasi                |
|------------|-------|-------------------------|
| `backend`  | 8000  | Django REST API         |
| `db`       | 5432  | PostgreSQL 16           |
| `redis`    | 6379  | Cache + Celery broker   |
| `celery`   | —     | Async task worker       |
| `celery_beat` | —  | Scheduled tasks (cron)  |

Production'da qo'shimcha:
- `nginx` — reverse proxy, static/media serve

## 📱 Mobile (Flutter)

Backend to'liq tayyor bo'lgach `mobile/` papkasida Flutter loyihasi
yaratiladi (`flutter create .`). Flutter Docker'ga tushmaydi — u
APK/IPA fayl bo'lib kompilyatsiya qilinadi.

## 🚀 Production Deploy

`.github/workflows/`da 3 ta pipeline:

1. **`backend-ci.yml`** — har push'da lint + test
2. **`docker-build.yml`** — main branch push'da Docker image GitHub Container Registry'ga
3. **`deploy.yml`** — SSH orqali serverga deploy (env secretlar kerak)

Kerakli GitHub Secrets:
```
DEPLOY_HOST         # server IP yoki domain
DEPLOY_USER         # SSH user
DEPLOY_SSH_KEY      # private key
DEPLOY_PATH         # server'dagi loyiha yo'li
```

## 📖 Tafsilotlar

- Backend hujjatlar: [`backend/README.md`](backend/README.md)
- Loyiha rejasi: [`loyiha_reja.md`](loyiha_reja.md)

## 📜 Litsenziya

Intern loyihasi — Boburmirzo Sobirjonov, 2026.
