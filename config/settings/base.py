# config/settings/base.py
#
# Base settings shared by all environments (dev, test, prod).
# dev.py / prod.py / test.py import from here and override as needed.

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from config.utils import get_database_config_variables

# Loads variables from .env (no-op on Heroku if vars are already set)
load_dotenv()
# Optional: load a separate file for email overrides if you use it locally
# load_dotenv(".env.email")

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# -----------------------------------------------------------------------------
# Core security / environment knobs
# -----------------------------------------------------------------------------

SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_IN_DEV_ONLY")
DEBUG = False

ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()]

THE_SITE_NAME = "Personal Assistant"

MAINTENANCE_MODE = os.environ.get("MAINTENANCE_MODE", "off") == "on"

# -----------------------------------------------------------------------------
# Database helper (shared)
# -----------------------------------------------------------------------------

def postgres_from_database_url(database_url: str):
    """
    Return a Django DATABASES dict for Postgres using your existing
    get_database_config_variables(DATABASE_URL) helper.
    """
    database_config_variables = get_database_config_variables(database_url)

    return {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": database_config_variables["DATABASE_NAME"],
            "HOST": database_config_variables["DATABASE_HOST"],
            "PORT": database_config_variables.get("DATABASE_PORT") or "5432",
            "USER": database_config_variables["DATABASE_USER"],
            "PASSWORD": database_config_variables["DATABASE_PASSWORD"],
        }
    }

# -----------------------------------------------------------------------------
# Application definition
# -----------------------------------------------------------------------------

INSTALLED_APPS = [
    # Put accounts first so its templates override admin defaults
    "accounts.apps.AccountsConfig",

    # Django contrib
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admindocs",

    # Third-party
    "rest_framework",
    "storages",
    "django_celery_beat",

    # Local apps
    "base",
    "app_tracker.apps.AppTrackerConfig",
    "career_organizerator.apps.CareerOrganizeratorConfig",
    "vitals.apps.VitalsConfig",
    "uc_goals.apps.UCGoalsConfig",
    "unimportant_notes.apps.UnimportantNotesConfig",
    "sonic_text.apps.SonicTextConfig",
    "boosts.apps.BoostsConfig",
    "plan_it.apps.PlanItConfig",
    "pomodo.apps.PomodoConfig",
    "story_line.apps.StoryLineConfig",
    "packing_list.apps.PackingListConfig",
    "decide.apps.DecideConfig",
    "tasks.apps.TasksConfig",
    "warcrafting.apps.WarcraftingConfig",
    "kanban_cabinet.apps.KanbanCabinetConfig",
]

# Whitenoise in base so it works everywhere consistently (dev/prod)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    # Your custom maintenance middleware (needs request.user, so after auth)
    "config.middleware.SuperuserMaintenanceMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# -----------------------------------------------------------------------------
# Auth / i18n / defaults
# -----------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

# -----------------------------------------------------------------------------
# Static files
# -----------------------------------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# -----------------------------------------------------------------------------
# Django REST Framework
# -----------------------------------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
}

# -----------------------------------------------------------------------------
# Email
# -----------------------------------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL",
    "Quarterdeck Boosts <no-reply@quarterdeck.flynntknapp.com>",
)
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# -----------------------------------------------------------------------------
# File storage (optional AWS S3 integration)
# -----------------------------------------------------------------------------

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")

if AWS_STORAGE_BUCKET_NAME:
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_S3_OBJECT_PARAMETERS = {
        "ACL": "public-read",
        "CacheControl": "max-age=86400",
    }
    AWS_MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# -----------------------------------------------------------------------------
# Celery
# -----------------------------------------------------------------------------

CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = False

# Prefer Heroku REDIS_URL; fall back to REDISCLOUD_URL; then local dev default
CELERY_BROKER_URL = os.getenv("REDIS_URL") or os.getenv("REDISCLOUD_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL") or os.getenv("REDISCLOUD_URL", "redis://localhost:6379/0")

CELERY_TASK_ALWAYS_EAGER = (os.getenv("CELERY_TASK_ALWAYS_EAGER", "False").lower() == "true")

# -----------------------------------------------------------------------------
# Logging (minimal console)
# -----------------------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "celery": {"handlers": ["console"], "level": "INFO", "propagate": True},
    },
}
