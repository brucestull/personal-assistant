# Celery Task Arguments: Admin

- [Celery Task Arguments: Admin - ChatGPT](https://chat.openai.com/share/e31d4235-07f0-4b48-aab0-655c8cf6eaec)

I have a scheduled task in Django app with Celery. I can add the task in Django admin to send a hard-coded email. How can I add positional and keyword arguments in Django admin?

To add positional and keyword arguments to a scheduled task in a Django application using Celery, you typically use Django-Celery-Beat. Django-Celery-Beat provides a way to store the schedule in the database, and it integrates with Django Admin to make managing periodic tasks easy. Here’s a step-by-step guide to achieving this:

### 1. Install Django-Celery-Beat
If you haven't already installed Django-Celery-Beat, you can do so by adding it to your project. Install it via pip:
```bash
pip install django-celery-beat
```

### 2. Update Django Settings
Add `django_celery_beat` to your `INSTALLED_APPS` in your Django settings file:
```python
INSTALLED_APPS = [
    ...
    'django_celery_beat',
]
```

### 3. Migrate Database
Run the migrations to create the necessary tables:
```bash
python manage.py migrate django_celery_beat
```

### 4. Create Periodic Tasks
You can now create and manage periodic tasks directly from the Django admin. To pass arguments to your tasks, follow these steps:

#### a. Access Django Admin
Go to your Django admin panel, usually at `http://<your-domain>/admin`.

#### b. Add a Periodic Task
Navigate to Django Celery Beat > Periodic Tasks and click “Add”. Fill in the details:
- **Name**: A human-readable name for the task.
- **Task (registered task)**: Select the task you want to schedule from the dropdown. This list is populated from the tasks decorated with `@app.task` in your Celery app.

#### c. Add Arguments
In the "Arguments" (args) field, you can add JSON-formatted positional arguments. For example:
```json
[ "arg1", "arg2", "arg3" ]
```

In the "Keyword arguments" (kwargs) field, you can add JSON-formatted keyword arguments. For example:
```json
{ "key1": "value1", "key2": "value2" }
```

#### d. Set the Schedule
Choose how often you want the task to run. You can use the Interval or Crontab schedules:
- **Interval schedule**: Runs at regular intervals (e.g., every 5 minutes).
- **Crontab schedule**: Runs at specific times (e.g., at 2:30 AM every Friday).

#### e. Save the Periodic Task
After setting up your arguments and schedule, save the task.

### 5. Ensure Celery Beat is Running
Make sure that Celery Beat is running alongside your worker. Use this command to start Celery Beat:
```bash
celery -A your_project_name beat -l info
```
It's common to run both the worker and beat processes in production environments.

By using Django-Celery-Beat, you gain the flexibility to manage tasks through the Django admin, including specifying the arguments passed to tasks. This setup is particularly useful for tasks that need to run at varying intervals or need specific parameters passed at runtime.

This is my current `shared_task`:

```python
@shared_task
def send_test_email():
    """
    Sends a test email to the admin.
    """
    send_mail(
        subject="Test Email from Boosts",
        message="This is the test email body.",
        from_email=TEST_EMAIL_ADDRESS,
        recipient_list=[TEST_EMAIL_ADDRESS],
    )
    logger.info("Sent test email.")
```

Help me add one positional argumetn and one keyword argument to the scheduled job for the values to be used in `send_test_email` function?

To modify your `send_test_email` task so that it accepts one positional argument and one keyword argument, and to use these values within the function, follow these steps:

### Step 1: Modify the Task
You'll need to adjust the definition of `send_test_email` to accept additional parameters. Let’s add one positional argument for the recipient's email address, and one keyword argument for the email subject.

```python
from django.core.mail import send_mail
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_test_email(recipient_email, subject="Default Subject"):
    """
    Sends a test email to the specified recipient.
    """
    send_mail(
        subject=subject,
        message="This is the test email body.",
        from_email='your_default_from_email@example.com',  # Use a default or config variable
        recipient_list=[recipient_email],
    )
    logger.info("Sent test email to %s.", recipient_email)
```

### Step 2: Update the Usage in Django Admin
With Django-Celery-Beat, you can now pass the positional and keyword arguments via the Django admin interface when you configure your periodic task. Here's how you would do it:

#### a. Navigate to Django Admin
Go to Django Admin and look for Django Celery Beat, then Periodic Tasks.

#### b. Add or Update a Periodic Task
Create a new task or edit an existing one, selecting `send_test_email` as the task.

#### c. Configure Arguments
In the args field, add the recipient email as a JSON array:
```json
["recipient@example.com"]
```
In the kwargs field, add the subject as a JSON object:
```json
{"subject": "Custom Email Subject"}
```

#### d. Configure Scheduling
Set the schedule according to your needs, using either intervals or crontabs.

#### e. Save the Configuration
Once all fields are correctly filled, save the task. Make sure Celery Beat is running to pick up and schedule the new task.

### Step 3: Running Celery and Celery Beat
Ensure both Celery and Celery Beat are running to handle tasks and scheduling respectively. You might run Celery with a command like:
```bash
celery -A your_project_name worker -l info
```
And for Celery Beat:
```bash
celery -A your_project_name beat -l info
```

### Step 4: Test Your Setup
After setting everything up, Celery Beat should schedule and execute your `send_test_email` task according to the configuration, sending an email with the specified recipient and subject. Check your logs and email backend to confirm that it's working as expected.

This configuration allows you to dynamically manage whom to send emails and customize the email subjects directly from the Django admin, making your application more flexible and easier to manage.
