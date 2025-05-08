# config/celery.py
import os

# import django
from celery import Celery
from django.conf import settings

# Define the default Django settings module for the 'celery' app.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# ------------------------------------
# Celery should not need this.
# ------------------------------------
# BAD ACVICE:
# This is a bad practice to set the Django settings module in the Celery app.
# This will ensure that all the Django settings are loaded before Celery starts
# processing tasks. It is crucial for tasks that depend on Django models and other
# settings.

# django.setup()
# ------------------------------------

# Create an instance of the Celery class with a name of 'config'.
# https://docs.celeryq.dev/en/stable/reference/celery.html#celery.Celery
app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
# Set utc false to use local time:
app.conf.enable_utc = False
# Set the timezone to use to convert to and from local time:
app.conf.timezone = settings.TIME_ZONE

app.autodiscover_tasks()
