# money_wise/apps.py

from django.apps import AppConfig


class MoneyWiseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "money_wise"
    verbose_name = "Money Wise"
