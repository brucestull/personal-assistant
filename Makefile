.PHONY: clean test coverage covhtml migrate makemigrations makemigrate runserver createsu shell loaddata resetdb

# Clean python, pytest, and coverage files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.coverage" -delete
	echo "Cleaned __pycache__, .pytest_cache, and htmlcov directories and .pyc, .coverage files."

# Run pytest only
pytest:
	pytest --ds=config.settings

# Run unit tests
test:
	python manage.py test

# Run pytest with coverage
coverage:
	pytest --ds=config.settings --cov=plan_it --cov-report=term-missing --cov-report=html

# Open the HTML coverage report (Linux/Mac)
covhtml:
	xdg-open htmlcov/index.html || open htmlcov/index.html || echo "Please open htmlcov/index.html manually."

# Run makemigrations
makemigrations:
	python manage.py makemigrations

# Run migrate
migrate:
	python manage.py migrate

# Run makemigrations and migrate
makemigrate: makemigrations migrate

# Run the development server
runserver:
	python manage.py runserver

# Create superuser from .env values
createsu:
	@python manage.py shell -c "import dotenv, os; \
	dotenv.load_dotenv(); \
	from django.contrib.auth import get_user_model; \
	User = get_user_model(); \
	username = os.environ.get('DJANGO_SU_NAME'); \
	email = os.environ.get('DJANGO_SU_EMAIL'); \
	password = os.environ.get('DJANGO_SU_PASSWORD'); \
	User.objects.filter(username=username).exists() or User.objects.create_superuser(username=username, email=email, password=password, registration_accepted=True)" && \
	echo 'Superuser created or already exists.'

# Start the Django shell
shell:
	python manage.py shell

# Load fixtures (adjust fixture name if needed)
loaddata:
	python manage.py loaddata initial_data.json

# Load Storage Sort model data
load_storage_sort:
	python manage.py loaddata storage/fixtures/sort_decisions.json && echo "Storage SortDecision data loaded."

# Reset the database and reload initial data
resetdb:
	rm -f db.sqlite3
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc" -delete
	echo "Database and migrations cleared."
	make makemigrate
	make loaddata

# Load demo fixture data
seed:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py loaddata plan_it/fixtures/demo_data.json && echo "Database seeded with demo data."

# Show this help
help:
	@echo "Available targets:"
	@awk '/^[a-zA-Z0-9_%-]+:/ { \
		if (match(prev, /^# (.+)/, desc)) { \
			printf "  \033[1m%-15s\033[0m %s\n", $$1, desc[1]; \
		} else { \
			printf "  \033[1m%-15s\033[0m\n", $$1; \
		} \
	} { prev = $$0 }' $(MAKEFILE_LIST)
