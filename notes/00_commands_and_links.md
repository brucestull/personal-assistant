# Useful Commands and Links

## Commands

### Starting Services in Order
1. `redis-server`: Start Redis server. It may already be running.
1. `celery -A config worker --loglevel=info`: Start Celery worker with info logging. Keep this running in a separate terminal, if needed.
1. `python manage.py runserver`: Start Django development server.

### Redis
* `redis-server`: Start Redis server.
* `celery -A config worker --loglevel=info`: Start Celery worker with info logging.
* `redis-cli`: Start Redis CLI.
* `redis-cli monitor`: Monitor Redis commands.
* `redis-cli ping`: Check if Redis server is running.

### This Project

1. `pipenv install`
1. `pipenv shell`
1. `python manage.py migrate accounts`
1. `python manage.py makemigrations`
1. `python manage.py migrate`
1. `python manage.py createsuperuser --email admin@email.app --username admin`
1. `python manage.py createsuperuser --email FlynntKnapp@email.app --username FlynntKnapp`

### `pipenv`

* `pipenv install`
  * Create a `pipenv` virtual environment for the current directory.
* `pipenv install django==4.0`
* `pipenv install django==4.1`
* `pipenv install docutils==0.19`
* `pipenv shell`
* `exit`
  * Exit the current `pipenv` virtual environment.

### `pip`

* `pip list`

### Django

* `django-admin startproject config .`
* `python manage.py startapp accounts`
* `python manage.py runserver`
* `<Ctrl+C>`
* `python manage.py makemigrations`
* `python manage.py migrate`
* `python manage.py createsuperuser`
* `python manage.py createsuperuser --email admin@email.app --username admin`
* `python manage.py createsuperuser --email FlynntKnapp@email.app --username FlynntKnapp`
* `python manage.py shell`
  ```python
  from django.conf import settings as s
  print(s.DEBUG)
  print(s.SECRET_KEY)
  print(s.DATABASES)
  print(s.INSTALLED_APPS)
  ```

### Django Create `SECRET_KEY`

* `python manage.py shell`
* `from django.core.management.utils import get_random_secret_key`
* `print(get_random_secret_key())`

### Heroku

* Can't have leading `.\`, which occurs on tab-auto-complete is used in PowerShell, when running command with `heroku run`:
  * `heroku run python manage.py createsuperuser --email admin@email.app --username admin`
  * `heroku run python manage.py createsuperuser --email FlynntKnapp@email.app --username FlynntKnapp`
* `heroku login`
* `heroku create dezzi-diner`

### PowerShell

* `Get-Command python | Format-List *`

### Misc

* `tree /f /a`

### Git

* `git remote -v`

### SQLite

* `sqlite3 db.sqlite3`
* `sqlite3 db.sqlite3 ".tables"`: List all tables in the SQLite database.
* `sqlite3 db.sqlite3 "SELECT * FROM auth_user;"`: List all users in the SQLite database.
* `sqlite3 db.sqlite3 "SELECT * FROM auth_user WHERE username='admin';"`: Get the admin user.
* `sqlite3 db.sqlite3 "SELECT * FROM auth_user WHERE username='FlynntKnapp';"`: Get the FlynntKnapp user.
* `sqlite3 db.sqlite3 ".tables"`
* `sqlite3 db.sqlite3 ".schema app_tracker_project"`


## Development server web links

* Applications:
  * <http://localhost:8000/journals/list/>
  * [HTML](http://localhost:8000/valued-goals/html/)
  * [Goals](http://localhost:8000/valued-goals/goals/)
  * [Goals Create](http://localhost:8000/valued-goals/goals/create/)
  * [App Tracker](http://localhost:8000/app-tracker/)
  * [Unimportant Notes](http://localhost:8000/unimportant-notes/)
  * [Project Manager](http://localhost:8000/project-manager/)
  * [Plan It - Dashboard](http://localhost:8000/plan-it/)
* Create user:
  * <http://localhost:8000/accounts/signup/>
* Server Root:
  * <http://localhost:8000/>
* Django Admin:
  * <http://localhost:8000/admin/>
* Django Admin Documentation:
  * <http://localhost:8000/admin/doc/>
  * <http://localhost:8000/admin/doc/tags/>
  * <http://localhost:8000/admin/doc/filters/>
  * <http://localhost:8000/admin/doc/models/>
  * <http://localhost:8000/admin/doc/models/auth.user/>

## Production deployment links

* Dashboard:
* Server Root:
* Create user:
* Django Admin:
* Django Admin Documentation:

## Repository Links

* Repository [`README.md`](../README.md).
