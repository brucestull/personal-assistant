# Heroku Celery Setup

- [Heroku Celery Setup Guide](https://chat.openai.com/share/94e43bf6-d614-4d10-b3dd-d259965ffff0)

Implementing Celery with Celery Beat on Heroku for a Django application involves a few steps to ensure that both Celery workers and the Celery Beat scheduler are running properly in the Heroku environment. Here's a step-by-step guide:

### 1. Set Up Redis on Heroku

Heroku does not provide Redis by default, so you'll need to add a Redis add-on. You can use Heroku Redis or any other Redis provider available on Heroku.

1. **Add Redis to Your Heroku App:**
   - Use the Heroku CLI or the Heroku Dashboard to add a Redis add-on. For example, with the CLI:
     ```bash
     heroku addons:create heroku-redis:hobby-dev -a your-app-name
     ```
   - This command adds a free Redis instance to your app.

2. **Configure Redis URL in Your App:**
   - Heroku sets the Redis URL in an environment variable (e.g., `REDIS_URL`). Make sure your Django app is configured to use this variable for Celery.

### 2. Configure Celery in Django for Heroku

1. **Update Celery Configuration:**
   - In your Django settings, ensure Celery is configured to use the Redis URL from the environment variable:
     ```python
     import os
     CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
     ```

### 3. Procfile for Worker and Beat

Heroku uses a `Procfile` to run your application and any other processes.

1. **Create/Update the Procfile:**
   - Add entries for the Celery worker and beat. Your `Procfile` might look like this:
     ```
     web: gunicorn your_project.wsgi
     worker: celery -A your_project worker --loglevel=info
     beat: celery -A your_project beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
     ```
   - Replace `your_project` with your Django project name.

### 4. Deploy to Heroku

1. **Push Your Code:**
   - After configuring the `Procfile`, push your code to Heroku:
     ```bash
     git push heroku main
     ```

2. **Scale Dynos:**
   - Make sure to scale your worker and beat dynos:
     ```bash
     heroku ps:scale worker=1 beat=1
     ```

### 5. Monitor and Debug

- After deployment, monitor your application using Heroku logs to ensure that both the Celery worker and beat are running correctly:
  ```bash
  heroku logs --tail
  ```

### Notes

- **Environment Variables:** Ensure all required environment variables are set in your Heroku app's settings.
- **Resource Allocation:** Be aware of the resources your Redis add-on provides and how many dynos you need based on your workload.
- **Security:** Ensure your Redis instance is properly secured, especially if using a third-party add-on.

This should get your Celery and Celery Beat running on Heroku. Be sure to test thoroughly to ensure everything is working as expected in the Heroku environment.