import os

from config.settings.common import *
from config.utils import get_database_config_variables

DEBUG = False

ALLOWED_HOSTS = ['flynnt-knapp-8e0b83ab9b88.herokuapp.com']

MIDDLEWARE = MIDDLEWARE + ['whitenoise.middleware.WhiteNoiseMiddleware']

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_ROOT = BASE_DIR / 'staticfiles'

database_config_variables = get_database_config_variables(
    os.environ.get('DATABASE_URL')
)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': database_config_variables['DATABASE_NAME'],
        'HOST': database_config_variables['DATABASE_HOST'],
        'PORT': database_config_variables['DATABASE_PORT'],
        'USER': database_config_variables['DATABASE_USER'],
        'PASSWORD': database_config_variables['DATABASE_PASSWORD'],
    }
}

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# Create a specific `SECRET_KEY` for production and use it in production only.
SECRET_KEY = os.environ.get('SECRET_KEY')

# To create a new `SECRET_KEY`:
"""
    python manage.py shell
    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())
"""