# Menu Mate — Root Makefile
# Butun stack (backend + db + redis + celery) uchun buyruqlar.

.DEFAULT_GOAL := help
COMPOSE := docker compose
COMPOSE_PROD := docker compose -f docker-compose.yml -f docker-compose.prod.yml
BACKEND := $(COMPOSE) exec backend

# --- Help ---
help:  ## Barcha buyruqlar ro'yxati
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'

# --- Docker stack ---
up:  ## Barcha servislarni ishga tushirish (dev)
	$(COMPOSE) up -d
	@echo "\n✅ Backend: http://localhost:8000"
	@echo "✅ Swagger: http://localhost:8000/api/v1/docs/"
	@echo "✅ Admin:   http://localhost:8000/admin/"

down:  ## Barcha servislarni to'xtatish
	$(COMPOSE) down

restart:  ## Restart
	$(COMPOSE) restart

redis-flush:  ## Redis cache'ni to'liq tozalash (Django cache DB 1 + Celery DB 2)
	$(COMPOSE) exec redis redis-cli FLUSHALL
	@echo "✅ Redis cache tozalandi (barcha DB'lar)"

restart-fresh: restart redis-flush  ## Restart + cache flush (yangi kod deploy qilingandan keyin)
	@echo "✅ Backend qayta ishga tushdi va cache tozalandi"

build:  ## Docker imagelarni qayta qurish
	$(COMPOSE) build

logs:  ## Backend loglarini ko'rish
	$(COMPOSE) logs -f backend

logs-all:  ## Barcha servislar loglari
	$(COMPOSE) logs -f

ps:  ## Servislar holati
	$(COMPOSE) ps

clean:  ## To'xtatish + volumelarni o'chirish (DB YO'QOLADI!)
	$(COMPOSE) down -v

# --- Backend (Django) ---
shell:  ## Backend container ichiga kirish
	$(BACKEND) bash

dj-shell:  ## Django shell
	$(BACKEND) python manage.py shell

migrate:  ## Migration'larni qo'llash
	$(BACKEND) python manage.py migrate

makemigrations:  ## Migration yaratish
	$(BACKEND) python manage.py makemigrations

superuser:  ## Superuser yaratish
	$(BACKEND) python manage.py createsuperuser

sync-endpoints:  ## Barcha API endpointlarni bazaga yozish
	$(BACKEND) python manage.py sync_endpoints

collectstatic:  ## Static fayllarni yig'ish
	$(BACKEND) python manage.py collectstatic --noinput

loaddata:  ## Fixture yuklash (recipes.json, holidays.json)
	$(BACKEND) python manage.py loaddata recipes holidays

# --- Testing / Quality ---
test:  ## Testlarni ishga tushirish
	$(BACKEND) python manage.py test

lint:  ## Kod stilini tekshirish
	$(BACKEND) ruff check .

format:  ## Kodni format qilish
	$(BACKEND) ruff format .

# --- Local dev (docker'siz) ---
local-install:  ## Lokal virtualenv'ga o'rnatish
	cd backend && poetry install

local-run:  ## Lokal Django serverni ishga tushirish
	cd backend && poetry run python manage.py runserver

local-migrate:
	cd backend && poetry run python manage.py migrate

# --- Production ---
prod-up:  ## Production stack ishga tushirish
	$(COMPOSE_PROD) up -d --build

prod-down:
	$(COMPOSE_PROD) down

prod-logs:
	$(COMPOSE_PROD) logs -f backend

prod-migrate:
	$(COMPOSE_PROD) exec backend python manage.py migrate --noinput

prod-collectstatic:
	$(COMPOSE_PROD) exec backend python manage.py collectstatic --noinput

# --- Database ---
db-backup:  ## Postgres backup (backup.sql)
	$(COMPOSE) exec db pg_dump -U $${DB_USER:-menu_mate} $${DB_NAME:-menu_mate} > backup.sql
	@echo "✅ Backup: backup.sql"

db-restore:  ## backup.sql'dan tiklash
	cat backup.sql | $(COMPOSE) exec -T db psql -U $${DB_USER:-menu_mate} $${DB_NAME:-menu_mate}

# --- Setup (birinchi safar) ---
init: build up migrate sync-endpoints  ## To'liq initial setup
	@echo "\n🎉 Loyiha ishga tayyor!"
	@echo "Superuser yaratish uchun: make superuser"

.PHONY: help up down restart redis-flush restart-fresh build logs logs-all \
        ps clean shell dj-shell migrate makemigrations superuser sync-endpoints \
        collectstatic loaddata test lint format local-install local-run \
        local-migrate prod-up prod-down prod-logs prod-migrate prod-collectstatic \
        db-backup db-restore init
