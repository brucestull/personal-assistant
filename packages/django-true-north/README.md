# django-true-north

A reusable Django app for tracking **Core Values**, **Goals**, **Milestones**, and **Value Actions** — your personal "True North" compass.

## Features

- Core Values management (with slug auto-generation)
- Goals linked to Core Values, with status tracking
- Milestones linked to Goals
- Value Actions (tasks) linked to Milestones
- Dashboard with filtering by status, completion, and active items
- Django Admin integration with inlines
- Management command: `seed_true_north_demo` for sample data

## Requirements

- Python >= 3.11
- Django >= 4.1
- The host project must include the `base` app (provides `CreatedUpdatedBase`, `OrderableMixin`, `RegistrationAcceptedMixin`, `SiteContextMixin`)

## Installation

### As an editable local package (development)

From the root of the host project:

```bash
pipenv install -e ./packages/django-true-north
```

Or add to your `Pipfile` manually:

```ini
[packages]
django-true-north = {editable = true, path = "./packages/django-true-north"}
```

Then run `pipenv install`.

## Setup

1. Add `"true_north.apps.TrueNorthConfig"` to `INSTALLED_APPS` in your Django settings.
2. Include the app URLs in your project's URL configuration:

```python
# config/urls.py
from django.urls import include, path

urlpatterns = [
    ...
    path("true-north/", include("true_north.urls")),
]
```

3. Run migrations:

```bash
python manage.py migrate
```

4. (Optional) Seed demo data:

```bash
python manage.py seed_true_north_demo --username admin
```

## App Structure

```
true_north/
├── admin.py          # Django Admin registrations with inlines
├── apps.py           # AppConfig
├── forms.py          # ModelForms with Bootstrap classes
├── management/
│   └── commands/
│       └── seed_true_north_demo.py
├── migrations/       # Database migrations
├── models.py         # CoreValue, Goal, Milestone, ValueAction
├── templates/
│   └── true_north/   # HTML templates for all CRUD views + dashboard
├── tests/            # pytest tests and factory-boy factories
├── urls.py           # URL patterns (app_name = "true_north")
└── views.py          # Class-based views (ListView, CreateView, etc.)
```

## License

MIT
