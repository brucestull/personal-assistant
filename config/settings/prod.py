# config/settings/prod.py
#
# Production settings (Heroku)

from __future__ import annotations

import os

from .base import *  # noqa: F403, F401

DEBUG = False

# In prod, SECRET_KEY must exist
SECRET_KEY = os.environ["SECRET_KEY"]

# Hosts: prefer env var; otherwise fall back to known hosts
if not ALLOWED_HOSTS:  # noqa: F405
    ALLOWED_HOSTS = [
        "flynnt-knapp-8e0b83ab9b88.herokuapp.com",
        "dev.quarterdeck.flynntknapp.com",
    ]

# Database: require DATABASE_URL in prod
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL is required in prod; refusing to start without Postgres.")

DATABASES = postgres_from_database_url(database_url)  # noqa: F405

# -----------------------------------------------------------------------------
# Security / HTTPS (Heroku proxy)
# -----------------------------------------------------------------------------

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
REFERRER_POLICY = "same-origin"
