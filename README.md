# Personal Assistant

[![CircleCI](https://dl.circleci.com/status-badge/img/circleci/Y1ZCzLfk7VvFxn1NaACyjS/FZvaTruzWGoti9qPSq8dwz/tree/main.svg?style=shield&circle-token=32275bd7053ab434c1bc1e8db9c3774469e0837c)](https://dl.circleci.com/status-badge/redirect/circleci/Y1ZCzLfk7VvFxn1NaACyjS/FZvaTruzWGoti9qPSq8dwz/tree/main)

## Introduction
A brief description of what the application does and the problem it solves. Include a couple of key features or benefits.

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation
### Prerequisites
- Python 3.x
- Django 4.x
### Setup
Instructions for setting up the development environment.

## Quick Start
Step-by-step guide for getting a basic implementation up and running.

## Features
An outline of the core features and any unique selling points of the application.

## Known Issues
List any known bugs or non-optimal code sections here.

## Contributing
Outline how users can contribute. Provide links to contribution guidelines and the code of conduct if available.

## License
Information about the project's license (e.g., MIT, GPL, etc.).

## Contact
Your contact information or that of the project maintainer for users to reach out.

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

6- Packages for Expansion:
    - <https://pypi.org/project/django-debug-toolbar/>

## Resources
- [Django Best Practices: Custom User Model](https://learndjango.com/tutorials/django-custom-user-model)
- [The Django admin documentation generator](https://docs.djangoproject.com/en/4.2/ref/contrib/admin/admindocs/)
- [Configuring Django Settings for Production](https://thinkster.io/tutorials/configuring-django-settings-for-production)
- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/)
- [Continuous Integration With Python: An Introduction - realpython.com](https://realpython.com/python-continuous-integration/)
