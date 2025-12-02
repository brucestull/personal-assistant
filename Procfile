web: gunicorn config.wsgi
release: python manage.py migrate accounts && python manage.py migrate
worker: celery -A config worker --beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler

scale_up: python heroku_scale.py up
scale_down: python heroku_scale.py down
