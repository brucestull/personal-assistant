# thoughts/tasks.py

from __future__ import annotations

import smtplib
from typing import Optional

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse

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


def _build_dashboard_url() -> str:
    """Return an absolute URL for the Thoughts dashboard."""
    path = reverse("thoughts:dashboard")
    site_url = getattr(settings, "SITE_URL", None)
    if site_url:
        return f"{site_url.rstrip('/')}{path}"
    allowed_hosts = getattr(settings, "ALLOWED_HOSTS", [])
    host = allowed_hosts[0] if allowed_hosts else "localhost"
    scheme = "https" if host not in ("localhost", "127.0.0.1") else "http"
    return f"{scheme}://{host}{path}"


def _send_email(
    subject: str,
    text_body: str,
    to: list,
    *,
    from_email: Optional[str] = None,
) -> None:
    """Send a single email."""
    sender = from_email or DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=sender,
        to=to,
    )
    msg.send(fail_silently=False)


@shared_task(**RETRY_KW)
def send_thoughts_dashboard_email(self, user_id: int) -> dict:
    """
    Send an email to the given user with a link to their Thoughts dashboard.

    Accepts the user's PK as the sole argument so it can be scheduled via
    Django Admin's Periodic Tasks (django-celery-beat).
    """
    User = get_user_model()

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logger.warning("send_thoughts_dashboard_email: user %s not found", user_id)
        return {"ok": False, "reason": "user_not_found"}

    if not getattr(user, "email", None):
        logger.warning(
            "send_thoughts_dashboard_email: user %s has no email; skipping",
            user_id,
        )
        return {"ok": False, "reason": "no_user_email"}

    dashboard_url = _build_dashboard_url()
    site_name = getattr(settings, "THE_SITE_NAME", "Personal Assistant")

    subject = f"{site_name} — Review Your Thoughts"
    body = (
        f"Hey {user.username},\n\n"
        f"Here's a quick link to your Thoughts dashboard so you can review "
        f"your thoughts:\n\n"
        f"{dashboard_url}\n\n"
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
            "send_thoughts_dashboard_email: SMTP error for user %s — will retry: %s",
            user_id,
            exc,
        )
        raise

    logger.info(
        "send_thoughts_dashboard_email: sent to user %s (%s)",
        user.pk,
        user.email,
    )
    return {"ok": True, "user_id": user.pk}
