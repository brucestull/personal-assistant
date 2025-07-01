# Adding Celery Beat for Periodic Tasks

To add Celery Beat for handling periodic tasks in a Django application, we need to update several components:

1. **Install Required Packages**:
    ```shell
    pipenv install django-celery-beat
    ```
1. **Update [`config/celery.py`](../config/celery.py)**:

    Add the following lines to configure Celery Beat to use the Django database scheduler:

    ```python
    # config/celery.py
    # ...
    # Use django-celery-beat's database scheduler:
    app.conf.beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"
    # ...
    ```
1. **Update [`Procfile`](../Procfile)**:

   Add a `beat` process to handle periodic tasks.

   ```Procfile
   ...
   beat: celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
   ```

### Current `Procfile`
```
web: gunicorn config.wsgi
release: python manage.py migrate accounts && python manage.py migrate
worker: celery -A config worker --loglevel=info
```

We need to add a `beat` process to handle periodic tasks. The updated `Procfile` will look like this:
```
web: gunicorn config.wsgi
release: python manage.py migrate accounts && python manage.py migrate
worker: celery -A config worker --loglevel=info
beat: celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
