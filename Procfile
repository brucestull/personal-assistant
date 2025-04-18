web: gunicorn config.wsgi
release: python manage.py migrate accounts && python manage.py migrate
worker: celery -A config worker --loglevel=info