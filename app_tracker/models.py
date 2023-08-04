from django.db import models


class Application(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    notes = models.TextField()
    current_models = models.TextField()
    future_models = models.TextField()
    repository_url = models.URLField()
    has_python = models.BooleanField()
    has_django = models.BooleanField()
    has_docker = models.BooleanField()
    has_css = models.BooleanField()
    has_custom_user = models.BooleanField()
    has_sticky_footer = models.BooleanField()
    has_prod_deployment = models.BooleanField()
    TESTING_LEVEL_CHOICES = [
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]
    testing_level = models.CharField(
        max_length=6,
        choices=TESTING_LEVEL_CHOICES,
    )
    LANGUAGE_FRAMEWORK_SYSTEM_CHOICES = [
        ("Django", "Django"),
        ("Django REST", "Django REST"),
        ("Vue.js", "Vue.js"),
        ("Python", "Python"),
        ("Docker", "Docker"),
        ("MongoDB", "MongoDB"),
        ("pymongo", "pymongo"),
    ]
    language_framework_system = models.CharField(
        max_length=20,
        choices=LANGUAGE_FRAMEWORK_SYSTEM_CHOICES,
    )
