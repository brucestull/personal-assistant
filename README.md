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

### `Career Organizerator` - `career_organizerator` Application

### `CBT` - `cbt` Application

### `Self Enquiry` - `self_enquiry` Application

### `Vitals` - `vitals` Application
- `DateTimeBase` Model
    - Fields:
        - `created`
        - `updated`
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

- `Gratitude` Model
- `Strength` Model

## Templates

## Interesting Features

- Custom 403 template (This template is currently in `accounts` application, but may be moved to root level)
- Moved `created` and `updated` fields to `DateTimeBase` model
    - I first extracted a base class in the same module, but then moved it to the `base` package in some of the applications
    - TODO: Move `DateTimeBase` to `base.CreatedUpdatedBase` in all applications

## New Knowledge

## PyPI Packages
