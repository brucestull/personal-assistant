import smtplib

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

logger = get_task_logger(__name__)

User = get_user_model()

# Retry configuration for email tasks
RETRY_KW = dict(
    bind=True,
    autoretry_for=(smtplib.SMTPException, ConnectionError, TimeoutError),
    retry_backoff=30,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=5,
)


@shared_task(**RETRY_KW)
def send_reminder_email(self, reminder_id: int, schedule_id: int = None) -> dict:
    """
    Send a reminder email to the user.

    Args:
        reminder_id: ID of the Reminder to send
        schedule_id: Optional ID of the ReminderSchedule that triggered this

    Returns:
        dict with status information
    """
    from .models import Reminder

    try:
        reminder = Reminder.objects.select_related("user").get(pk=reminder_id)
    except Reminder.DoesNotExist:
        logger.warning("send_reminder_email: Reminder %s not found", reminder_id)
        return {"ok": False, "reason": "reminder_not_found"}

    # Check if reminder is active
    if not reminder.is_active:
        logger.info("Reminder %s is inactive, skipping email", reminder_id)
        return {"ok": False, "reason": "reminder_inactive"}

    user = reminder.user

    # Check if user has email
    if not user.email:
        logger.warning("User %s has no email address", user.id)
        return {"ok": False, "reason": "user_no_email"}

    # Prepare email content
    site_name = getattr(settings, "THE_SITE_NAME", "Personal Assistant")
    subject = f"{site_name} — Reminder: {reminder.name}"

    message_lines = [
        f"Hello {user.username},",
        "",
        f"This is your reminder: {reminder.name}",
        "",
    ]

    if reminder.description:
        message_lines.extend(
            [
                "Details:",
                reminder.description,
                "",
            ]
        )

    message_lines.extend(
        [
            f"— {site_name}",
        ]
    )

    message = "\n".join(message_lines)

    # Send email
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            recipient_list=[user.email],
            fail_silently=False,
        )
        logger.info(
            "Sent reminder %s to user %s (%s)",
            reminder_id,
            user.id,
            user.email,
        )
        return {
            "ok": True,
            "reminder_id": reminder_id,
            "user_id": user.id,
            "schedule_id": schedule_id,
        }
    except (smtplib.SMTPException, ConnectionError, TimeoutError) as exc:
        logger.warning(
            "SMTP error while sending reminder %s — will retry: %s",
            reminder_id,
            exc,
        )
        raise  # Triggers Celery autoretry
