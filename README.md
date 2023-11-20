# Personal Assistant

[![CircleCI](https://dl.circleci.com/status-badge/img/circleci/Y1ZCzLfk7VvFxn1NaACyjS/FZvaTruzWGoti9qPSq8dwz/tree/main.svg?style=shield&circle-token=32275bd7053ab434c1bc1e8db9c3774469e0837c)](https://dl.circleci.com/status-badge/redirect/circleci/Y1ZCzLfk7VvFxn1NaACyjS/FZvaTruzWGoti9qPSq8dwz/tree/main)

## Table of Contents

## Templates
- [accounts/templates/403.html](https://github.com/brucestull/personal-assistant/blob/main/accounts/templates/403.html)

## Interesting Features

- Custom [accounts/templates/403.html](https://github.com/brucestull/personal-assistant/blob/main/accounts/templates/403.html) (This template is currently in `accounts` application, but may be moved to root level).
- Moved `created` and `updated` fields to `DateTimeBase` model.
    - I first extracted a base class `DateTimeBase` in the same module, but then moved it to the `base` package for use in any application.

## Features to Add
- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/)

## New Knowledge

## PyPI Packages
- Currently Installed Packages:
    - <https://pypi.org/project/pipenv/>
    - <https://pypi.org/project/asgiref/>
    - <https://pypi.org/project/coverage/>
    - <https://pypi.org/project/Django/>
    - <https://pypi.org/project/docutils/>
    - <https://pypi.org/project/gunicorn/>
    - <https://pypi.org/project/Pillow/>
    - <https://pypi.org/project/pip/>
    - <https://pypi.org/project/psycopg2/>
    - <https://pypi.org/project/python-dotenv/>
    - <https://pypi.org/project/setuptools/>
    - <https://pypi.org/project/sqlparse/>
    - <https://pypi.org/project/tzdata/>
    - <https://pypi.org/project/wheel/>
    - <https://pypi.org/project/whitenoise/>
- Packages for Expansion:
    - <https://pypi.org/project/django-debug-toolbar/>

## Resources
- [Django Best Practices: Custom User Model](https://learndjango.com/tutorials/django-custom-user-model)
- [The Django admin documentation generator](https://docs.djangoproject.com/en/4.2/ref/contrib/admin/admindocs/)
- [Configuring Django Settings for Production](https://thinkster.io/tutorials/configuring-django-settings-for-production)
- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/)
- [Continuous Integration With Python: An Introduction - realpython.com](https://realpython.com/python-continuous-integration/)
