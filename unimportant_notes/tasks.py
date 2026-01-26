# unimportant_notes/tasks.py

import logging
import random
from typing import Optional

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from .models import NoteTag, UnimportantNote

logger = logging.getLogger("celery")


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_random_unimportant_note_email(
    self,
    user_id: int,
    tag_id: Optional[int] = None,
) -> dict:
    """
    Pick a random UnimportantNote authored by `user_id`.
    If tag_id is provided, only choose notes that have that NoteTag.
    Email it to the same user.
    """
    User = get_user_model()

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logger.warning("send_random_unimportant_note_email: user %s not found", user_id)
        return {"ok": False, "reason": "user_not_found"}

    qs = UnimportantNote.objects.filter(author=user)

    # Optional tag filter
    tag_obj = None
    if tag_id is not None:
        try:
            tag_obj = NoteTag.objects.get(pk=tag_id, author=user)
        except NoteTag.DoesNotExist:
            logger.info(
                "Tag %s not found for user %s; sending unfiltered note", tag_id, user_id
            )
            tag_obj = None
        else:
            qs = qs.filter(tag=tag_obj).distinct()

    if not qs.exists():
        reason = "no_notes_for_tag" if tag_obj else "no_notes"
        logger.info("No UnimportantNotes for user %s (tag=%s)", user_id, tag_id)
        return {"ok": False, "reason": reason}

    ids = list(qs.values_list("id", flat=True))
    note = qs.get(id=random.choice(ids))

    # UnimportantNote inherits from base.Note, which has `title` and `content`.
    title = getattr(note, "title", f"Note #{note.id}")

    # ✅ Prefer `content`, but still be defensive with fallbacks:
    text = (
        getattr(note, "content", None)
        or getattr(note, "body", None)
        or getattr(note, "text", None)
        or ""
    )

    tag_names = ", ".join(note.tag.values_list("name", flat=True))

    subject = (
        f"{getattr(settings, 'THE_SITE_NAME', 'Personal Assistant')} — "
        "Daily Unimportant Note"
    )
    if tag_obj:
        subject += f" [{tag_obj.name}]"

    body_lines = [
        f"Hey {user.username},",
        "",
        "Your daily unimportant note:",
        "",
        f"Title: {title}",
    ]

    # ✅ Actually include note.content in the email body
    if text:
        body_lines += [
            "",
            "Content:",
            text,
        ]

    if tag_names:
        body_lines += ["", f"Tags: {tag_names}"]

    # Include a relative link if available
    try:
        body_lines += ["", f"Open in app: {note.get_absolute_url()}"]
    except Exception:
        pass

    body_lines += ["", f"— {getattr(settings, 'THE_SITE_NAME', 'Personal Assistant')}"]
    body = "\n".join(body_lines)

    send_mail(
        subject=subject,
        message=body,
        from_email=getattr(settings, "EMAIL_HOST_USER", None),
        recipient_list=[user.email],
        fail_silently=False,
    )

    logger.info(
        "Sent UnimportantNote %s to user %s (%s) tag=%s",
        note.id,
        user.id,
        user.email,
        tag_id,
    )
    return {
        "ok": True,
        "note_id": note.id,
        "user_id": user.id,
        "tag_id": tag_id,
    }


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_unimportant_note_email(
    self,
    user_id: int,
    unimportant_note_id: int,
) -> dict:
    """
    Send a specific UnimportantNote (by ID) to a specific user (by ID).
    This is meant for scheduled/triggered sends using kwargs.
    """
    User = get_user_model()

    # ---- User lookup ----
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logger.warning("send_unimportant_note_email: user %s not found", user_id)
        return {"ok": False, "reason": "user_not_found"}

    # ---- Note lookup ----
    try:
        note = UnimportantNote.objects.get(pk=unimportant_note_id, author=user)
    except UnimportantNote.DoesNotExist:
        logger.warning(
            "send_unimportant_note_email: note %s not found for user %s",
            unimportant_note_id,
            user_id,
        )
        return {"ok": False, "reason": "note_not_found_for_user"}

    # ---- Build email content ----
    title = getattr(note, "title", f"Note #{note.id}")

    text = (
        getattr(note, "content", None)
        or getattr(note, "body", None)
        or getattr(note, "text", None)
        or ""
    )

    tag_names = ", ".join(note.tag.values_list("name", flat=True))

    subject = (
        f"{getattr(settings, 'THE_SITE_NAME', 'Personal Assistant')} — "
        "Unimportant Note"
    )

    body_lines = [
        f"Hey {user.username},",
        "",
        "Here is your scheduled unimportant note:",
        "",
        f"Title: {title}",
    ]

    if text:
        body_lines += [
            "",
            "Content:",
            text,
        ]

    if tag_names:
        body_lines += ["", f"Tags: {tag_names}"]

    # Include a relative link if available
    try:
        body_lines += ["", f"Open in app: {note.get_absolute_url()}"]
    except Exception:
        pass

    # NOTE: explicitly do NOT send image content right now
    if getattr(note, "main_image", None):
        body_lines += [
            "",
            "(Note: This email does not include the note image yet, "
            "but we can add image support in the future.)",
        ]

    body_lines += ["", f"— {getattr(settings, 'THE_SITE_NAME', 'Personal Assistant')}"]
    body = "\n".join(body_lines)

    send_mail(
        subject=subject,
        message=body,
        from_email=getattr(settings, "EMAIL_HOST_USER", None),
        recipient_list=[user.email],
        fail_silently=False,
    )

    logger.info(
        "Sent specific UnimportantNote %s to user %s (%s)",
        note.id,
        user.id,
        user.email,
    )
    return {
        "ok": True,
        "note_id": note.id,
        "user_id": user.id,
    }
