FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# System deps — psycopg2 needs libpq, gettext for i18n compilemessages
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gettext \
        curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==${POETRY_VERSION}"

# ---- Dependencies layer (cached separately) ----
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --without dev || poetry install --no-root

# ---- App code ----
COPY . .

# Collect static (safe to run at build; overridable env)
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

# Default: gunicorn in prod. Override via docker-compose for dev.
CMD ["gunicorn", "core.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
