from __future__ import annotations

import smtplib
from typing import Optional

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

from .models import Thought

logger = get_task_logger(__name__)

DEFAULT_FROM_EMAIL = getattr(settings, "DEFAULT_FROM_EMAIL", None)
MAX_SUBJECT_THOUGHT_LENGTH = 80

CELERY_RETRY_KWARGS = dict(
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
    sender = from_email or DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=sender,
        to=to,
    )
    msg.send(fail_silently=False)


@shared_task(**CELERY_RETRY_KWARGS)
def send_thought_email(self, user_id: int, thought_id: int) -> dict:
    User = get_user_model()

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logger.warning("send_thought_email: user %s not found", user_id)
        return {"ok": False, "reason": "user_not_found"}

    if not getattr(user, "email", None):
        logger.warning(
            "send_thought_email: user %s has no email; skipping Thought pk=%s",
            user.pk,
            thought_id,
        )
        return {"ok": False, "reason": "no_user_email"}

    try:
        thought = Thought.objects.get(pk=thought_id, user=user)
    except Thought.DoesNotExist:
        logger.warning(
            "send_thought_email: Thought %s not found for user %s",
            thought_id,
            user_id,
        )
        return {"ok": False, "reason": "thought_not_found_for_user"}

    site_name = getattr(settings, "THE_SITE_NAME", "Personal Assistant")
    subject = (
        f"{site_name} — Bus Drive Thought: "
        f"{str(thought.text)[:MAX_SUBJECT_THOUGHT_LENGTH]}"
    )
    body = (
        f"Hey {user.username},\n\n"
        "Here is your Bus Drive Thought:\n\n"
        f"{thought.text}\n\n"
        f"Created: {thought.created}\n"
        f"Updated: {thought.updated}\n"
        f"— {site_name}"
    )

    resolved_from = (
        DEFAULT_FROM_EMAIL
        or getattr(settings, "EMAIL_HOST_USER", None)
        or user.email
    )

    try:
        _send_email(subject, body, [user.email], from_email=resolved_from)
    except (smtplib.SMTPException, ConnectionError, TimeoutError) as exc:
        logger.warning(
            "send_thought_email: SMTP error for Thought %s — will retry: %s",
            thought_id,
            exc,
        )
        raise

    logger.info(
        "send_thought_email: sent Thought %s to user %s (%s)",
        thought.id,
        user.id,
        user.email,
    )
    return {
        "ok": True,
        "thought_id": thought.id,
        "user_id": user.id,
    }
