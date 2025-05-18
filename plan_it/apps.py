# plan_it/apps.py

from django.apps import AppConfig


class PlanItConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "plan_it"
    verbose_name = "Plan It"
