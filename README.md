# Personal Assistant

## Table of Contents


## Run `flake8` With Coverage Locally

```bash
flake8 --exclude=migrations,settings.py,urls.py,wsgi.py,manage.py --statistics --count
```

```bash
flake8 --exclude=venv*,migrations,settings.py,wsgi.py,manage.py --statistics --ignore=E501
```

## Development Links

- <http://localhost:8000/vitals/>
- <http://localhost:8000/vitals/bloodpressures/>

## Production Links

* [Personal Assistant](https://flynnt-knapp-8e0b83ab9b88.herokuapp.com/)

## Applications and Models

### `Accounts` - `accounts` Application
- `CustomUser` Model
    - Fields:
        - `registration_accepted`
    - Methods:
        - `get_blood_pressure_range`
        - `get_average_and_median_blood_pressure`

### `App Tracker` - `app_tracker` Application
- `LanguageFrameworkSystem` Model
    - Fields:
        - `name`
    - Meta:
        - `verbose_name_plural`
- `Project`
    - Fields:
        - `name`
        - `owner`
        - `description`
- `Application`
    - Fields:
        - `project`
        - `name`
        - `description`
        - `production_url`
        - `repository_url`
        - `reference_repository_url`
        - `is_official_repository`
        - `is_archive_repository`
        - `project_board_url`
        - `is_favorite`
        - `has_custom_user`
        - `has_sticky_footer`
        - `has_prod_deployment`
        - `has_email_sending`
        - `repository_is_public`
        - `settings_in_enviroment`
        - `settings_in_dot_env_file`
        - `settings_in_dot_yml_file`
        - `is_template_repository`
        - `TESTING_LEVEL_CHOICES`
        - `testing_level`
        - `language_framework_systems`
- `Note`
    - Fields:
        - `title`
        - `content`
        - `application`
- `DjangoModel`
    - Fields:
        - `name`
        - `description`
        - `is_current_model`
        - `application`

### `base` Package
- `CreatedUpdatedBase` Model
    - Fields:
        - `created`
        - `updated`
    - Meta:
        - `abstract`

### `Career Organizerator` - `career_organizerator` Application
- `BulletPoint` Model
    - Fields:
        - `user`
        - `text`
    - Meta:
        - `verbose_name_plural`
- `ElevatorSpeech` Model
    - Fields:
        - `user`
        - `theme`
        - `bullet_points`
    - Meta:
        - `verbose_name_plural`

### `CBT` - `cbt` Application
- `CognativeDistortion` Model
    - Fields:
        - `name`
        - `description`
    - Meta:
        - `ordering`
        - `verbose_name`
        - `verbose_name_plural`
- `Thought` Model
    - Fields:
        - `user`
        - `cognative_distortion`
        - `name`
        - `description`
    - Meta:
        - `ordering`
        - `verbose_name`
        - `verbose_name_plural`

### `Self Enquiry` - `self_enquiry` Application
- `Journal` Model
    - Fields:
        - `author`
        - `title`
        - `content`
    - Methods:
        - `get_absolute_url`
        - `display_content`
- `GrowthOpportunity` Model
    - Fields:
        - `author`
        - `question`
    - Meta:
        - `verbose_name`
        - `verbose_name_plural`

### `Vitals` - `vitals` Application
- `BloodPressure` Model
    - Fields:
        - `user`
        - `systolic`
        - `diastolic`
    - Methods:
        - `get_average_and_median`
    - Meta:
        - `verbose_name_plural`
- `Pulse` Model
    - Fields:
        - `user`
        - `bpm`
    - Meta:
        - `verbose_name`
        - `verbose_name_plural`

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
