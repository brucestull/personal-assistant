.PHONY: clean test coverage covhtml migrate makemigrations makemigrate runserver createsu shell loaddata resetdb

# Clean pyc and __pycache__
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	echo "Cleaned __pycache__ and .pyc files."

# Run pytest only
test:
	pytest --ds=config.settings

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
User.objects.filter(username=username).exists() or User.objects.create_superuser(username, email, password)" && \
echo 'Superuser created or already exists.'

# Start the Django shell
shell:
	python manage.py shell

# Load fixtures (adjust fixture name if needed)
loaddata:
	python manage.py loaddata initial_data.json

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
