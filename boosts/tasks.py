# boosts/tasks.py
from __future__ import annotations

import smtplib
from typing import Iterable, Optional

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection

from .models import Inspirational
from unimportant_notes.models import UnimportantNote

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


@shared_task(**RETRY_KW)
def send_daily_boost_and_note(
    self,
    user_id: int,
) -> None:
    """
    Send a random Inspirational and UnimportantNote to a user.

    This task selects a random Inspirational and a random UnimportantNote
    from the database and sends them to the specified user via email.
    """
    from accounts.models import CustomUser

    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        logger.warning("User not found", extra={"user_id": user_id})
        return

    if not getattr(user, "email", None):
        logger.warning(
            "User has no email; skipping send", extra={"user_id": user_id}
        )
        return

    # Get a random Inspirational
    inspirational = Inspirational.objects.select_related("author").order_by("?").first()

    # Get a random UnimportantNote
    unimportant_note = UnimportantNote.objects.select_related("author").order_by("?").first()

    if not inspirational and not unimportant_note:
        logger.info(
            "No inspirational or unimportant note found to send",
            extra={"user_id": user_id},
        )
        return

    # Build email body
    body_parts = []

    if inspirational:
        body_parts.append("=== Your Daily Inspirational Quote ===\n")
        body_parts.append(f"{inspirational.body}\n")
        body_parts.append(f"- {inspirational.author.username}\n")

    if unimportant_note:
        body_parts.append("\n=== Your Daily Unimportant Note ===\n")
        body_parts.append(f"Title: {unimportant_note.title}\n")
        if unimportant_note.content:
            body_parts.append(f"\n{unimportant_note.content}\n")
        if unimportant_note.url:
            body_parts.append(f"\nURL: {unimportant_note.url}\n")

    subject = "Your Daily Boost and Note"
    body = "".join(body_parts)

    if not DEFAULT_FROM_EMAIL:
        logger.error(
            "DEFAULT_FROM_EMAIL not configured; cannot send email",
            extra={"user_id": user_id},
        )
        return

    try:
        _send_email(
            subject,
            body,
            [user.email],
            from_email=DEFAULT_FROM_EMAIL,
        )
        logger.info(
            "Sent daily boost and note",
            extra={
                "user_id": user_id,
                "inspirational_id": (
                    inspirational.pk if inspirational else None
                ),
                "unimportant_note_id": (
                    unimportant_note.pk if unimportant_note else None
                ),
            },
        )
    except (smtplib.SMTPException, ConnectionError, TimeoutError) as exc:
        logger.exception(
            "SMTP error while sending daily boost and note — retrying"
        )
        raise self.retry(exc=exc)
