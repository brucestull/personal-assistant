# Application Tracker (app_tracker)

## Models and Attributes

* `Application`
    * `name`
    * `description`
    * `notes`
    * `current_models`
    * `future_models`
    * `repository_url`
    * `has_python`
    * `has_django`
    * `has_docker`
    * `has_css`
    * `has_custom_user`
    * `has_sticky_footer`
    * `has_prod_deployment`
    * `testing_level`
        * `high`
        * `medium`
        * `low`
    * `language_framework_system`
        * "Django"
        * "Django REST"
        * "Vue.js"
        * "Python"
        * "Docker"
        * "MongoDB"
        * "pymongo"

## Evolution of Models

```python
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
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    testing_level = models.CharField(max_length=6, choices=TESTING_LEVEL_CHOICES)
    LANGUAGE_FRAMEWORK_SYSTEM_CHOICES = [
        ('Django', 'Django'),
        ('Django REST', 'Django REST'),
        ('Vue.js', 'Vue.js'),
        ('Python', 'Python'),
        ('Docker', 'Docker'),
        ('MongoDB', 'MongoDB'),
        ('pymongo', 'pymongo'),
    ]
    language_framework_system = models.CharField(max_length=20, choices=LANGUAGE_FRAMEWORK_SYSTEM_CHOICES)
```

```python
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
    language_framework_system = models.ForeignKey(LanguageFrameworkSystem, on_delete=models.CASCADE)
```

```python
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
```
