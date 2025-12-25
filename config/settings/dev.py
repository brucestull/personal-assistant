# config/settings/dev.py
#
# Development settings (local machine)

from __future__ import annotations

import os

from .base import *  # noqa: F403, F401

DEBUG = True

if not ALLOWED_HOSTS:  # noqa: F405
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# SQLite for local dev simplicity
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

# Uncollected static files location (optional, but matches your current pattern)
STATICFILES_DIRS = [BASE_DIR / "static"]  # noqa: F405

# Dev email: print to console
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
