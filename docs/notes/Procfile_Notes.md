# Heroku `Procfile` Notes

## What is a Procfile?

A `Procfile` is a text file used by Heroku to declare what command should be executed to start your application. It is essential for defining the processes that run on Heroku.
## Basic Structure
A `Procfile` consists of one or more lines, each defining a process type and the command to run. The format is:
```
<process_type>: <command>
```

## Example One
For a typical web application, a `Procfile` might look like this:
```
web: python app.py
worker: python worker.py
```
In this example:
- `web` is the process type that Heroku will use to serve web requests.
- `worker` is another process type that might handle background tasks.

## Example Two

```
web: gunicorn config.wsgi
release: python manage.py migrate accounts && python manage.py migrate
worker: celery -A config worker --loglevel=info
```
In this example:
- `web` uses `gunicorn` to serve the Django application.
    - Gunicorn runs `config.wsgi`, which is the WSGI application entry point for Django.
- `release` runs database migrations before the release.
    - It executes `python manage.py migrate accounts` and `python manage.py migrate` to apply migrations for the `accounts` app and the rest of the project.
- `worker` starts a Celery worker for handling asynchronous tasks.
    - The worker is responsible for executing tasks in the background, such as sending emails or processing data.

## Example Three

```
web: gunicorn config.wsgi
worker: celery -A config worker --loglevel=info
beat: celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
In this example:
- `web` serves the Django application using `gunicorn`.
- `worker` starts a Celery worker.
- `beat` runs the Celery beat scheduler, which is responsible for scheduling periodic tasks.

## Updating `Procfile` to Include `beat` for Periodic Tasks

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
