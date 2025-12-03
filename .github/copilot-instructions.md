# Copilot Instructions for Personal Assistant

This document provides context and guidelines to help Copilot understand and work effectively with this repository.

## Project Overview

Personal Assistant is a Django-based web application that provides various personal productivity tools. The application includes multiple Django apps for different functionality areas such as task management, note-taking, career organization, and more.

## Technology Stack

- **Python**: 3.11
- **Django**: 4.1.7
- **Database**: SQLite (development), PostgreSQL (production)
- **Task Queue**: Celery with Redis
- **Static Files**: WhiteNoise (production), Django staticfiles (development)
- **Cloud Storage**: AWS S3 (for media files)
- **CI/CD**: CircleCI
- **Deployment**: Heroku

## Project Structure

The project follows a standard Django project layout:

- `config/` - Main Django project configuration (settings, URLs, WSGI/ASGI)
- `accounts/` - Custom user model and authentication
- `base/` - Shared base models and utilities (e.g., `DateTimeBase` model)
- `templates/` - Root-level templates

### Django Applications

Each app is self-contained with its own models, views, templates, and tests:

- `app_tracker` - Application tracking
- `boosts` - Boost management
- `career_organizerator` - Career organization tools
- `decide` - Decision-making tools
- `notes` - Note-taking functionality
- `packing_list` - Packing list management
- `plan_it` - Planning tools
- `pomodo` - Pomodoro timer functionality
- `sonic_text` - Text utilities
- `story_line` - Story/timeline management
- `tasks` - Task management
- `uc_goals` - Goal tracking
- `unimportant_notes` - Casual notes
- `vitals` - Health/vitals tracking
- `warcrafting` - Gaming-related features

## Development Setup

### Prerequisites

- Python 3.11
- pipenv for dependency management

### Common Commands

Use `make` or `just` to run common tasks:

```bash
# Run tests
make test
# or
just test

# Run linter
just flake8

# Format code
just format

# Run with coverage
make coverage
# or
just coverage

# Database operations
make makemigrations
make migrate
make resetdb

# Run development server
make runserver
```

## Testing

- Tests use Django's built-in test framework
- pytest is also available (`just pytest`)
- Coverage reports are generated with `coverage` package
- Configuration is in `pyproject.toml` under `[tool.pytest.ini_options]` and `[tool.coverage.*]`

### Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test app_name

# Run with coverage
coverage run manage.py test && coverage report
```

## Code Style

This project uses multiple tools for code quality:

- **Black**: Code formatting (line length: 88)
- **isort**: Import sorting (profile: black)
- **Flake8**: Linting (config in `.flake8`)
- **Ruff**: Fast Python linter
- **mypy**: Static type checking

### Formatting Guidelines

- Line length: 88 characters
- Use Black-compatible formatting
- Imports should be sorted with isort
- Follow Django conventions for model definitions, views, and templates

### Running Linters

```bash
# Format code
just format

# Check formatting
just formatcheck

# Run all linters
just lint
```

## Django Conventions

### Models

- Use the `DateTimeBase` abstract model from `base` for `created` and `updated` timestamps
- Use `BigAutoField` as the default primary key
- Custom user model is `accounts.CustomUser`

### Views

- Follow Django class-based views (CBV) patterns where appropriate
- Use function-based views (FBV) for simple operations

### Templates

- Root templates are in `templates/`
- App-specific templates are in `<app_name>/templates/`
- Custom 403 template is in `accounts/templates/403.html`

### URLs

- Main URL configuration is in `config/urls.py`
- App-specific URLs should be included from each app's `urls.py`

## Environment Variables

Key environment variables (see `.env.example`):

- `ENVIRONMENT` - Set to "production" for production settings
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - PostgreSQL connection URL (production)
- `AWS_*` - AWS S3 configuration
- `EMAIL_*` - Email configuration
- `REDISCLOUD_URL` - Redis URL for Celery

## CI/CD

- CircleCI configuration is in `.circleci/config.yml`
- Pipeline runs linting, tests, and coverage
- Deployment to Heroku on successful builds to `main` branch

## Best Practices for Contributing

1. **Follow existing patterns**: Look at existing code in similar apps for guidance
2. **Write tests**: Add tests for new functionality
3. **Run linters**: Ensure code passes `just lint` before committing
4. **Keep apps modular**: Each Django app should be self-contained
5. **Use migrations**: Always create migrations for model changes
6. **Document changes**: Update relevant documentation when adding features
