# Useful Commands and Links

## Celery Commands

- `python -m celery worker`
- `python -m celery -A config worker`
- `python -m celery -A config worker -l info`

## Redis Commands

- `redis-server`
- `redis-cli`

## The Three Services
1. Producer: Your Django app
1. Message Broker: The Redis server
1. Consumer: Your Celery app

## Running the Services

1. `python manage.py runserver`
1. `redis-server`
1. `python -m celery -A config worker -l debug`
1. `python -m celery -A config beat -l debug --scheduler django_celery_beat.schedulers:DatabaseScheduler`
  - Uses the Django database to store the schedule


## Using `CELERY_BEAT_SCHEDULE`:

```python
from datetime import timedelta
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'task-name': {
        'task': 'myapp.tasks.my_task',
        'schedule': timedelta(minutes=5),
        'args': (16, 16)
    },
    'another-task-name': {
        'task': 'myapp.tasks.another_task',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
    },
    # You can add as many tasks as you want here
}
```

- `python -m celery -A config beat`
  - `python -m celery -A config beat -l debug`


## Inspecting Celery Registered Tasks
- `celery -A config inspect registered`

## Commands

### This Project

1. `pipenv install`
1. `pipenv shell`
1. `python manage.py migrate`
1. `python manage.py createsuperuser --email FlynntKnapp@email.app --username FlynntKnapp`

### Django Create `SECRET_KEY`

* `python manage.py shell`
* `from django.core.management.utils import get_random_secret_key`
* `print(get_random_secret_key())`

### Heroku

* `heroku run python manage.py createsuperuser --email admin@email.app --username admin`
* `heroku run python manage.py createsuperuser --email FlynntKnapp@email.app --username FlynntKnapp`
* `heroku login`

## Development Server Links

* Server Root:
  * <http://localhost:8000/>
* Boosts:
  * <http://localhost:8000/boosts/>
  * <http://localhost:8000/boosts/inspirationals/>
* API:
  * <http://localhost:8000/api/v1/>

## Production deployment links

* Server Root:

## Repository Links

* Repository [`README.md`](../README.md)
