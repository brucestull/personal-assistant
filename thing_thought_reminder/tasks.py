from __future__ import annotations

import smtplib
from typing import Optional

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

logger = get_task_logger(__name__)

DEFAULT_FROM_EMAIL = getattr(settings, "DEFAULT_FROM_EMAIL", None)

RETRY_KW = dict(
    bind=True,
    autoretry_for=(smtplib.SMTPException, ConnectionError, TimeoutError),
    retry_backoff=30,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=5,
)


def _send_email(
    subject: str,
    text_body: str,
    to: list,
    *,
    from_email: Optional[str] = None,
) -> None:
    """Send a single email."""
    if not to:
        logger.warning("Email not sent: empty recipient list.")
        return

    sender = from_email or DEFAULT_FROM_EMAIL
    if not sender:
        raise ValueError(
            "No from_email could be resolved. "
            "Set settings.DEFAULT_FROM_EMAIL or pass from_email explicitly."
        )

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=sender,
        to=list(to),
    )
    msg.send(fail_silently=False)


@shared_task(**RETRY_KW)
def send_reminder_email(self, schedule_id: int) -> dict:
    """
    Send a single reminder email for the given ReminderSchedule ID.
    Updates last_sent and computes next_send after successful send.
    """
    from django.utils import timezone

    from .models import ReminderSchedule

    try:
        schedule = ReminderSchedule.objects.select_related(
            "user", "thing", "thought"
        ).get(pk=schedule_id)
    except ReminderSchedule.DoesNotExist:
        logger.warning("ReminderSchedule %s not found", schedule_id)
        return {"ok": False, "reason": "schedule_not_found"}

    user = schedule.user
    if not getattr(user, "email", None):
        logger.warning(
            "User %s has no email; skipping reminder %s", user.pk, schedule_id
        )
        return {"ok": False, "reason": "no_user_email"}

    subject = schedule.get_subject()
    body = (
        f"Hey {user.username},\n\n"
        f"Here is your reminder:\n\n"
        f"{schedule.get_content()}\n\n"
        f"— {getattr(settings, 'THE_SITE_NAME', 'Personal Assistant')}"
    )

    resolved_from = DEFAULT_FROM_EMAIL or getattr(
        settings, "EMAIL_HOST_USER", None
    ) or user.email

    try:
        _send_email(subject, body, [user.email], from_email=resolved_from)
    except (smtplib.SMTPException, ConnectionError, TimeoutError) as exc:
        logger.warning(
            "SMTP error while sending reminder %s — will retry: %s", schedule_id, exc
        )
        raise

    now = timezone.now()
    schedule.last_sent = now
    schedule.next_send = schedule.compute_next_send()
    schedule.save(update_fields=["last_sent", "next_send"])

    logger.info("Sent reminder %s to %s (%s)", schedule_id, user.pk, user.email)
    return {"ok": True, "schedule_id": schedule_id, "user_id": user.pk}


@shared_task
def process_due_reminders() -> dict:
    """
    Periodic task: find all active reminder schedules that are due and dispatch
    send_reminder_email tasks for each.
    Should be scheduled via django-celery-beat (e.g. every hour or every 15 minutes).
    """
    from django.utils import timezone

    from .models import ReminderSchedule

    now = timezone.now()
    due_qs = ReminderSchedule.objects.filter(
        is_active=True,
        next_send__lte=now,
    ).values_list("id", flat=True)

    dispatched = 0
    for schedule_id in due_qs:
        send_reminder_email.delay(schedule_id)
        dispatched += 1

    logger.info("process_due_reminders: dispatched %s reminder task(s)", dispatched)
    return {"dispatched": dispatched}
