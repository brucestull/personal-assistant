# Personal Assistant

## Table of Contents

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


### Misc Models

## Templates

## Interesting Features

- Custom [403 template](accounts\templates\403.html) (This template is currently in `accounts` application, but may be moved to root level).
- Moved `created` and `updated` fields to `DateTimeBase` model.
    - I first extracted a base class `DateTimeBase` in the same module, but then moved it to the `base` package for use in any application.

## New Knowledge

## PyPI Packages
