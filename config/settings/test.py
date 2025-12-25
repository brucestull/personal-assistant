# config/settings/test.py
#
# Test settings (fast + deterministic)

from __future__ import annotations

from .dev import *  # noqa: F403, F401

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

CELERY_TASK_ALWAYS_EAGER = True
