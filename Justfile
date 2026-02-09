# Justfile
# Run `just` or `just help` to see tasks.

set shell := ["bash", "-euc"]
set dotenv-load := true

PYTHON := "python"
MANAGE := PYTHON + " manage.py"

# ------------------------------------------------------------
# Core helper: run any manage.py command
# Example: just manage createsuperuser
# Example: just manage test boosts.tests.TestThing
manage *ARGS:
  {{MANAGE}} {{ARGS}}

# ------------------------------------------------------------
# Housekeeping

clean:
  find . -type d -name "__pycache__" -exec rm -r {} +
  find . -type d -name ".pytest_cache" -exec rm -r {} +
  find . -type d -name "htmlcov" -exec rm -r {} +
  find . -type f -name "*.pyc" -delete
  find . -type f -name "*.coverage" -delete
  echo "Cleaned __pycache__, .pytest_cache, and htmlcov directories and .pyc, .coverage files."

# ------------------------------------------------------------
# Testing

# Django test runner (optionally pass app/test labels)
# Example: just test boosts
# Example: just test boosts.tests.TestFoo
test *ARGS="":
  {{MANAGE}} test {{ARGS}}

# Pytest runner (optionally pass paths/markers/etc.)
# Example: just pytest
# Example: just pytest -k "server" -q
pytest *ARGS="":
  pytest {{ARGS}}

# Pytest with coverage (requires pytest-cov)
# Example: just pytestcov
# Example: just pytestcov -k "api" --cov-report=term-missing
pytestcov *ARGS="":
  pytest --cov=. --cov-report=term-missing {{ARGS}}

# Django tests with coverage + HTML report
coverage *ARGS="":
  coverage run manage.py test {{ARGS}} && \
  coverage report && \
  coverage html

# ------------------------------------------------------------
# Migrations / DB

makemigrations *ARGS="":
  {{MANAGE}} makemigrations {{ARGS}}

migrate *ARGS="":
  {{MANAGE}} migrate {{ARGS}}

makemigrate: makemigrations migrate

delete_db:
  rm -f db.sqlite3
  echo "Database deleted."

resetdb: delete_db makemigrate createuser
  echo "Database reset, migrated, and superuser created."

# ------------------------------------------------------------
# Dev server / shell / users

runserver *ARGS="":
  {{MANAGE}} runserver {{ARGS}}

createuser:
  {{MANAGE}} create_user

shell *ARGS="":
  {{MANAGE}} shell {{ARGS}}

# ------------------------------------------------------------
# Static / deployment-ish helpers

# Collect static files (default --noinput, but override if you want)
# Example: just collectstatic
# Example: just collectstatic --clear
collectstatic *ARGS="--noinput":
  {{MANAGE}} collectstatic {{ARGS}}

# ------------------------------------------------------------
# Linting / formatting

# Auto-format Python (black + isort)
format:
  black .
  isort .

# Check formatting only (CI-friendly)
formatcheck:
  black --check .
  isort --check-only .

flake8:
  flake8

mypy:
  mypy .

# Optional Ruff (comment out if you’re not using Ruff)
ruff:
  ruff check .

rufffix:
  ruff check . --fix

# Umbrella lint target
# If you don't use ruff, remove it from deps.
lint: formatcheck flake8 mypy ruff
  echo "Lint checks passed."

# ------------------------------------------------------------
# Help / default

help:
  @just --list

default: help
