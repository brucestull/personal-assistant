# RUNBOOK: Run “Prod-like” Celery + Redis locally

This repo uses:
- Redis as the Celery **broker** and **result backend**
- Celery worker(s) to execute tasks async
- django-celery-beat as the **scheduler**, using the DB table-backed scheduler

Your current settings read Redis from **REDISCLOUD_URL**:
- CELERY_BROKER_URL = REDISCLOUD_URL (fallback: redis://localhost:6379/0)
- CELERY_RESULT_BACKEND = REDISCLOUD_URL (fallback: redis://localhost:6379/0)

So on your machine, set:
- `REDISCLOUD_URL=redis://localhost:6379/0`

---

## 0) Prereqs

### A) Confirm `.env` has the right knobs

Minimum to run prod-like locally:

```env
DJANGO_SETTINGS_MODULE=config.settings
ENVIRONMENT=dev
CELERY_TASK_ALWAYS_EAGER=false
REDISCLOUD_URL=redis://localhost:6379/0

# Email must be real if you want real outbound messages:
EMAIL_HOST=...
EMAIL_PORT=587
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
DEFAULT_FROM_EMAIL=...
TEST_EMAIL_ADDRESS=you@yourdomain.com
````

Important:

* `CELERY_TASK_ALWAYS_EAGER=false` is what makes tasks go to Redis instead of running immediately in-process.
* Your code does NOT read `REDIS_URL` for Celery. It reads `REDISCLOUD_URL`.

---

## 1) Start Redis locally

Pick ONE method.

### Option A: Docker (most consistent)

```bash
docker run --rm --name pa-redis -p 6379:6379 redis:7
```

### Option B: Ubuntu/WSL (system install)

```bash
sudo apt update
sudo apt install -y redis-server
sudo service redis-server start
redis-cli ping   # expect: PONG
```

### Option C: macOS (Homebrew)

```bash
brew install redis
brew services start redis
redis-cli ping   # expect: PONG
```

---

## 2) Migrate DB (includes django-celery-beat tables)

From the repo root:

```bash
python manage.py migrate
```

If you have never created a superuser on this machine:

```bash
python manage.py create_user
# (your Makefile target uses .env values)
```

---

## 3) Start Django (dev server)

```bash
python manage.py runserver
```

Leave this running.

---

## 4) Start Celery

### Recommended: run worker and beat as separate processes (clearer + closer to real ops)

Open a NEW terminal:

#### 4a) Start Celery worker

```bash
celery -A config worker --loglevel=info
```

Open ANOTHER terminal:

#### 4b) Start Celery beat (DB-backed scheduler)

```bash
celery -A config beat --loglevel=info \
  --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### “Match the Procfile” mode: worker + beat in ONE process

Your Procfile does this:

```bash
celery -A config worker --beat --loglevel=info \
  --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

This is convenient for local dev, but separating them is easier to debug.

---

## 5) Verify it’s actually “prod-like”

### A) Confirm tasks are NOT eager

In a Django shell:

```bash
python manage.py shell
```

Then:

```python
from django.conf import settings
settings.CELERY_TASK_ALWAYS_EAGER
```

Expect: `False`

### B) Confirm Redis is reachable from Celery

In the celery worker terminal, you should NOT see connection-refused errors.
If you do, your Redis URL is wrong or Redis is not running.

### C) Confirm beat is scheduling from the database

Because you configured:

* `django_celery_beat.schedulers:DatabaseScheduler`

…beat will schedule what’s in the DB tables.

Go to Django admin:

* `/admin/`
* “Periodic tasks” (django-celery-beat section)

Create/enable a periodic task (or ensure your app creates them).
If you create one, beat should log that it picked up the schedule.

---

## 6) Common problems + fixes

### Problem: Celery keeps trying to connect to a hosted Redis URL

Cause: your `.env` has `REDISCLOUD_URL` set to the cloud add-on value.
Fix: set it to local:

```env
REDISCLOUD_URL=redis://localhost:6379/0
```

### Problem: `Error: Connection refused` / `ConnectionError: [Errno 111]`

Cause: Redis not running OR wrong port.
Fix: run `redis-cli ping` and confirm `PONG`.
If using Docker, confirm the container is running and port 6379 mapped.

### Problem: Beat starts but does not schedule anything

Cause: no periodic tasks exist in DB OR beat tables not migrated.
Fix:

```bash
python manage.py migrate django_celery_beat
```

Then add a Periodic Task in admin and watch beat logs.

### Problem: Tasks never execute, even though beat logs scheduling

Cause: worker not running, or worker can’t import tasks.
Fix:

* ensure `celery -A config worker ...` is running
* ensure your tasks are inside `tasks.py` files or discovered by `app.autodiscover_tasks()`

### Problem: Emails don’t send

Cause: SMTP creds not set or provider blocking.
Fix:

* confirm `EMAIL_BACKEND` is SMTP in non-test (your settings do that)
* verify `EMAIL_HOST_USER/PASSWORD`, and try a simple Django send_mail test
* check provider logs (Mailgun/SendGrid) if applicable

---

## 7) Fast “daily dev” command set (copy/paste)

Terminal 1 (Redis via Docker):

```bash
docker run --rm --name pa-redis -p 6379:6379 redis:7
```

Terminal 2 (Django):

```bash
python manage.py migrate
python manage.py runserver
```

Terminal 3 (Worker):

```bash
celery -A config worker --loglevel=info
```

Terminal 4 (Beat):

```bash
celery -A config beat --loglevel=info \
  --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
