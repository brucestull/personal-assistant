# Running Celery and Celery Beat
Ensure both Celery and Celery Beat are running to handle tasks and scheduling respectively. You might run Celery with a command like:
```bash
celery -A your_project_name worker -l info
```
And for Celery Beat:
```bash
celery -A your_project_name beat -l info
```
