from django.db import models

class LanguageFrameworkSystem(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

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
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    testing_level = models.CharField(max_length=6, choices=TESTING_LEVEL_CHOICES)
    language_framework_systems = models.ManyToManyField(LanguageFrameworkSystem)

    def __str__(self):
        return self.name