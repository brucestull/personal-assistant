# How & Why Celery + Redis are used in this app

This app uses Celery to run work **outside the web request/response cycle**, so your site stays responsive and you can run scheduled/background jobs reliably.

---

## The “parts” and what each does

### 1) Django (the web app)
- Handles HTTP requests: pages, admin, APIs, etc.
- Triggers background work by **queuing a task** instead of doing everything inline.
- Example motivation: sending email inside a request can be slow and fragile.

### 2) Celery task (your code)
A Celery task is just a Python function that Celery can run later.

In practice, you write tasks in your Django apps (commonly in `tasks.py`).
Your `config/celery.py` calls `app.autodiscover_tasks()`, so Celery finds tasks across your installed apps.

Why tasks exist:
- send emails
- run periodic reminders
- generate reports
- sync external APIs
- cleanup jobs

### 3) Redis (the broker)
Redis stores the “to-do list” of tasks (messages) that need to run.

In your settings:
- `CELERY_BROKER_URL = REDISCLOUD_URL` (fallback `redis://localhost:6379/0`)

Why Redis is used as broker:
- simple, fast, widely supported
- good fit for dev + small/medium queues
- easy to run locally and as a hosted add-on (Heroku)

### 4) Celery worker (the doer)
A worker is a long-running process that:
1) listens to Redis for queued tasks
2) imports your Django project
3) executes tasks

Think: “the worker is the employee doing the jobs.”

If the worker is not running:
- tasks can be queued successfully
- but nothing will execute

### 5) Celery Beat (the scheduler)
Beat is a long-running process that:
- decides **when** to enqueue periodic tasks

In your setup, beat uses **django-celery-beat** with a DB-backed scheduler:
- `app.conf.beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"`

That means schedules are stored in your Django database:
- editable via Django admin
- persistent across restarts
- easy to enable/disable jobs without code changes

Think: “beat is the manager assigning recurring work into the queue.”

### 6) Result backend (optional, but you configured it)
Your settings also set:
- `CELERY_RESULT_BACKEND = REDISCLOUD_URL`

This is where Celery stores task results/status (if you use them).
Many apps don’t need results for fire-and-forget tasks (like sending an email),
but it can be useful for:
- debugging failures
- admin dashboards
- workflows that depend on task output

### 7) “Always eager” (dev shortcut you *turned off*)
You support:
- `CELERY_TASK_ALWAYS_EAGER`

When `true`, Celery runs tasks immediately in-process (no Redis, no worker).
When `false`, tasks are queued and run by worker(s) (prod-like).

For your “prod-like local” workflow:
- keep it `false` so you validate the full chain: Django → Redis → Worker → Email.

---

## How it flows in your app

### A) Request-triggered task (typical async)
1. User hits a view / you call code inside Django
2. Django calls `some_task.delay(...)`
3. Celery publishes a message to Redis (broker)
4. Worker pulls message and runs the task
5. Task sends email using Django email settings (SMTP in your dev)

### B) Scheduled task (periodic)
1. Celery Beat reads schedules from DB (django-celery-beat tables)
2. On schedule, beat enqueues a task into Redis
3. Worker executes it

---

## Why you might want “prod-like” locally (your exact reason)

Because it catches the real-world failures that eager-mode hides, such as:
- wrong Redis URL / wrong environment variables
- tasks not being discovered/imported correctly
- beat schedule not present/migrated
- SMTP creds missing or provider blocking
- tasks that rely on “running in a separate process” behavior

When you can run the full chain locally, you get confidence that:
- the same change will work on Heroku with workers/Redis add-on enabled

---

## Your repo’s current “gotchas” (good to remember)

### 1) Celery reads `REDISCLOUD_URL` (not `REDIS_URL`)
Your settings use:
- `os.environ.get("REDISCLOUD_URL", "redis://localhost:6379/0")`

So for local, set:
- `REDISCLOUD_URL=redis://localhost:6379/0`

### 2) Procfile runs worker with `--beat`
Your Procfile line:
- `celery -A config worker --beat ... --scheduler django_celery_beat...`

This is fine for convenience, but in real deployments you often split:
- one process for worker(s)
- one process for beat

Locally, splitting them makes debugging easier.

### 3) Emails in local dev are “real”
In non-test environments your settings use:
- `django.core.mail.backends.smtp.EmailBackend`

So if you put real SMTP creds in `.env`, your tasks can send real mail.
(That’s exactly what you want when validating “prod-like” behavior.)

---

## Mental model cheat sheet

- **Django**: web app
- **Task**: unit of background work
- **Redis (broker)**: queue storage / message bus
- **Worker**: executes tasks
- **Beat**: schedules periodic tasks
- **django-celery-beat**: stores schedules in DB + admin UI
- **Result backend**: stores task state/results (optional)
- **Always eager**: bypasses queue + worker (fast but not prod-like)