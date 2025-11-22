# boosts/tasks.py

from __future__ import annotations

import random
import smtplib
from typing import Iterable, Optional

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives, get_connection

from .models import Inspirational, InspirationalSent

logger = get_task_logger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Config: keep knobs in settings, not in code
DEFAULT_FROM_EMAIL = getattr(settings, "DEFAULT_FROM_EMAIL", None)
BOOSTS_TEST_EMAIL = getattr(
    settings,
    "BOOSTS_TEST_EMAIL",
    (
        getattr(settings, "ADMINS", [(None, None)])[0][1]
        if getattr(settings, "ADMINS", None)
        else DEFAULT_FROM_EMAIL
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# Helpers


def _send_email(
    subject: str,
    text_body: str,
    to: Iterable[str],
    *,
    from_email: Optional[str] = None,
    html_body: Optional[str] = None,
) -> None:
    """
    Send a single email (optionally with HTML alternative).
    Opens no new connection by itself; caller should pass a connection
    if sending in bulk. This helper is for one-offs inside a managed connection.
    """
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
    if html_body:
        msg.attach_alternative(html_body, "text/html")
    msg.send(fail_silently=False)


# ─────────────────────────────────────────────────────────────────────────────
# Tasks
# Using Celery autoretry for transient SMTP issues.
# (Jitter avoids thundering herd if many tasks retry together.)

RETRY_KW = dict(
    bind=True,
    autoretry_for=(smtplib.SMTPException, ConnectionError, TimeoutError),
    retry_backoff=30,  # 30s, 60s, 120s, ...
    retry_backoff_max=600,  # cap at 10min
    retry_jitter=True,
    max_retries=5,
)


@shared_task(**RETRY_KW)
def send_random_inspirational_email(self, user_id: int) -> dict:
    """
    Pick a random Inspirational authored by `user_id` and email it to that user.
    Also records an InspirationalSent with sender=user and beastie=user.
    """
    User = get_user_model()

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logger.warning("send_random_inspirational_email: user %s not found", user_id)
        return {"ok": False, "reason": "user_not_found"}

    qs = Inspirational.objects.filter(author=user)
    if not qs.exists():
        logger.info("No Inspirational objects for user %s", user_id)
        return {"ok": False, "reason": "no_inspirationals"}

    # Random pick without ORDER BY ? (more efficient, still simple)
    ids = list(qs.values_list("id", flat=True))
    inspirational = qs.get(id=random.choice(ids))

    site_name = getattr(settings, "THE_SITE_NAME", "Personal Assistant")
    subject = f"{site_name} — Daily Boost"
    body = (
        f"Hey {user.username},\n\n"
        f"Here’s your daily boost:\n\n"
        f"{inspirational.body}\n\n"
        f"— {site_name}"
    )

    # Prefer configured default sender; fallback to EMAIL_HOST_USER; last resort user.email  # noqa: E501
    resolved_from = (
        DEFAULT_FROM_EMAIL or getattr(settings, "EMAIL_HOST_USER", None) or user.email
    )

    try:
        _send_email(subject, body, [user.email], from_email=resolved_from)
    except (smtplib.SMTPException, ConnectionError, TimeoutError) as exc:
        logger.exception("SMTP error while sending random inspirational — retrying")
        raise self.retry(exc=exc)

    InspirationalSent.objects.create(
        inspirational=inspirational,
        inspirational_text=inspirational.body,
        sender=user,
        beastie=user,
    )

    logger.info(
        "Sent random Inspirational %s to user %s (%s)",
        inspirational.id,
        user.id,
        user.email,
    )
    return {"ok": True, "inspirational_id": inspirational.id, "user_id": user.id}


@shared_task(**RETRY_KW)
def send_inspirational_to_beastie(
    self,
    user_username: str,
    user_email: str,
    user_beastie_email: str,
    user_beastie_username: str,
    message: str,
) -> None:
    """
    Email the user's Beastie, and CC the user in a separate message.
    Uses a single SMTP connection for both sends.
    """
    logger.info(
        "Sending inspirational to Beastie",
        extra={
            "user": user_username,
            "beastie": user_beastie_username,
            "beastie_email": user_beastie_email,
        },
    )

    subject_to_beastie = f"Inspirational Quote from your Beastie: {user_username}"
    subject_to_user = (
        f"You Sent an Inspirational Quote to your Beastie: {user_beastie_username}"
    )

    from_email = user_email or DEFAULT_FROM_EMAIL
    if not from_email:
        raise ValueError(
            "No from_email available: provide user_email or set DEFAULT_FROM_EMAIL."
        )

    # One SMTP connection for both emails
    with get_connection() as conn:
        try:
            msg1 = EmailMultiAlternatives(
                subject=subject_to_beastie,
                body=message,
                from_email=from_email,
                to=[user_beastie_email],
                connection=conn,
            )
            msg2 = EmailMultiAlternatives(
                subject=subject_to_user,
                body=message,
                from_email=from_email,
                to=[user_email],
                connection=conn,
            )
            sent1 = msg1.send(fail_silently=False)
            sent2 = msg2.send(fail_silently=False)
            logger.info(
                "Inspirational emails sent",
                extra={"to_beastie_sent": sent1, "to_user_sent": sent2},
            )
        except (smtplib.SMTPException, ConnectionError, TimeoutError) as exc:
            logger.exception("SMTP error while sending Beastie emails — retrying")
            raise self.retry(exc=exc)


@shared_task(**RETRY_KW)
def send_inspirational_to_self(
    self,
    user_id: int,
    inspirational_id: Optional[int] = None,
) -> None:
    """
    Send an Inspirational to its author.
    - If inspirational_id is provided, use that (and validate ownership).
    - Otherwise, send the author's most recent Inspirational.
    """
    qs = Inspirational.objects.select_related("author").filter(author_id=user_id)

    if inspirational_id is not None:
        qs = qs.filter(pk=inspirational_id)

    # If not specific, pick most recent by creation/PK desc
    inspirational = qs.order_by("-pk").first()

    if not inspirational:
        logger.info(
            "No inspirational found to send",
            extra={"user_id": user_id, "inspirational_id": inspirational_id},
        )
        return

    author = inspirational.author
    if not getattr(author, "email", None):
        logger.warning("Author has no email; skipping send", extra={"user_id": user_id})
        return

    subject = "Your Daily Inspiration"
    body = inspirational.body or ""

    try:
        _send_email(subject, body, [author.email], from_email=author.email)
        logger.info(
            "Sent inspirational to self",
            extra={"user_id": user_id, "inspirational_id": inspirational.pk},
        )
    except (smtplib.SMTPException, ConnectionError, TimeoutError) as exc:
        logger.exception("SMTP error while sending to self — retrying")
        raise self.retry(exc=exc)


@shared_task(**RETRY_KW)
def send_test_email(self) -> None:
    """
    Sends a test email to BOOSTS_TEST_EMAIL (or DEFAULT_FROM_EMAIL/ADMINS fallback).
    """
    if not BOOSTS_TEST_EMAIL:
        raise ValueError(
            "BOOSTS_TEST_EMAIL/DEFAULT_FROM_EMAIL not configured; "
            "set settings.BOOSTS_TEST_EMAIL or settings.DEFAULT_FROM_EMAIL."
        )

    try:
        _send_email(
            subject="Test Email from Boosts",
            text_body="This is the test email body.",
            to=[BOOSTS_TEST_EMAIL],
            from_email=DEFAULT_FROM_EMAIL or BOOSTS_TEST_EMAIL,
        )
        logger.info("Sent test email", extra={"to": BOOSTS_TEST_EMAIL})
    except (smtplib.SMTPException, ConnectionError, TimeoutError) as exc:
        logger.exception("SMTP error while sending test email — retrying")
        raise self.retry(exc=exc)


@shared_task
def log_to_console() -> None:
    logger.info("LOGGER: This is a test.")
