#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

import environ


def main():
    """Run administrative tasks."""
    BASE_DIR = Path(__file__).resolve().parent

    env = environ.Env()

    env_path = BASE_DIR / ".env"
    if not env_path.exists():
        env_path = BASE_DIR.parent / ".env"

    if env_path.exists():
        environ.Env.read_env(env_path)

    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        env.str("DJANGO_SETTINGS_MODULE", "core.settings.dev")
    )

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
