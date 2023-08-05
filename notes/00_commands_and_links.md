# Useful Commands and Links

## Development server web links

* Applications:
  * <http://localhost:8000/journals/list/>
  * [HTML](http://localhost:8000/valued-goals/html/)
  * [Goals](http://localhost:8000/valued-goals/goals/)
  * [Goals Create](http://localhost:8000/valued-goals/goals/create/)
  * [App Tracker](http://localhost:8000/app-tracker/)
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

## Commands

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

## Production deployment links

* Dashboard:
* Server Root:
* Create user:
* Django Admin:
* Django Admin Documentation:

## Repository Links

* Repository [`README.md`](../README.md).
