# story_line/apps.py

from django.apps import AppConfig


class StoryLineConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "story_line"
    verbose_name = "Story Line"
