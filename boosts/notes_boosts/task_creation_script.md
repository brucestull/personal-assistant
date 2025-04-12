# Task Creation Script

```python
from django_celery_beat.models import PeriodicTask, CrontabSchedule

# Create a crontab schedule (12:01 PM every day)
schedule, _ = CrontabSchedule.objects.get_or_create(
    minute='1',
    hour='12',
    day_of_week='*',
    day_of_month='*',
    month_of_year='*',
)

# Schedule the task
PeriodicTask.objects.create(
    crontab=schedule,
    name='Send email at 12:01 PM',
    task='config.tasks.send_test_email'
)
```
