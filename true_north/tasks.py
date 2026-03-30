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

_MODEL_REGISTRY = {
    "CoreValue": ("true_north", "CoreValue"),
    "Goal": ("true_north", "Goal"),
    "Milestone": ("true_north", "Milestone"),
    "ValueAction": ("true_north", "ValueAction"),
}


def _get_email_subject_and_body(obj) -> tuple[str, str]:
    """Return (subject, body) for a True North model instance.

    Supported types: CoreValue, Goal, Milestone, ValueAction.
    For any other type, returns a generic subject and str(obj) as the body.
    """
    site_name = getattr(settings, "THE_SITE_NAME", "Personal Assistant")
    class_name = obj.__class__.__name__

    if class_name == "CoreValue":
        subject = f"{site_name} — Core Value: {obj.name}"
        body = (
            f"Core Value: {obj.name}\n\n"
            f"Definition: {obj.definition or 'N/A'}\n"
            f"Active: {obj.is_active}\n"
            f"Order: {obj.order}\n"
        )
    elif class_name == "Goal":
        subject = f"{site_name} — Goal: {obj.title}"
        body = (
            f"Goal: {obj.title}\n\n"
            f"Core Value: {obj.value or 'N/A'}\n"
            f"Description: {obj.description or 'N/A'}\n"
            f"Status: {obj.get_status_display()}\n"
            f"Start Date: {obj.start_date or 'N/A'}\n"
            f"Target Date: {obj.target_date or 'N/A'}\n"
        )
    elif class_name == "Milestone":
        subject = f"{site_name} — Milestone: {str(obj.description)[:80]}"
        body = (
            f"Milestone: {obj.description}\n\n"
            f"Goal: {obj.goal.title}\n"
            f"Notes: {obj.notes or 'N/A'}\n"
            f"Completed: {obj.is_completed}\n"
            f"Due Date: {obj.due_date or 'N/A'}\n"
        )
    elif class_name == "ValueAction":
        subject = f"{site_name} — Value Action: {str(obj.content)[:80]}"
        body = (
            f"Value Action: {obj.content}\n\n"
            f"Milestone: {obj.milestone.description}\n"
            f"Status: {obj.get_status_display()}\n"
            f"Due Date: {obj.due_date or 'N/A'}\n"
            f"Completed: {obj.is_completed}\n"
        )
    else:
        subject = f"{site_name} — True North Item"
        body = str(obj)

    return subject, body


def _send_email(
    subject: str,
    text_body: str,
    to: list,
    *,
    from_email: Optional[str] = None,
) -> None:
    """Send a single plain-text email.

    Args:
        subject: Email subject line.
        text_body: Plain-text email body.
        to: List of recipient email address strings.
        from_email: Sender address. Falls back to ``DEFAULT_FROM_EMAIL``
            from settings when not provided.

    Raises:
        ValueError: If no sender address can be resolved.
        smtplib.SMTPException: On SMTP-level errors (propagated to caller).
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
    msg.send(fail_silently=False)


@shared_task(**RETRY_KW)
def send_true_north_email(self, model_name: str, pk: int) -> dict:
    """
    Send an email containing the details of a True North model instance
    to the owning user's email address.
    """
    from django.apps import apps

    if model_name not in _MODEL_REGISTRY:
        logger.warning("send_true_north_email: unknown model_name %r", model_name)
        return {"ok": False, "reason": "unknown_model"}

    app_label, model_class_name = _MODEL_REGISTRY[model_name]
    ModelClass = apps.get_model(app_label, model_class_name)

    try:
        obj = ModelClass.objects.select_related("user").get(pk=pk)
    except ModelClass.DoesNotExist:
        logger.warning(
            "send_true_north_email: %s pk=%s not found", model_name, pk
        )
        return {"ok": False, "reason": "object_not_found"}

    user = obj.user
    if not getattr(user, "email", None):
        logger.warning(
            "send_true_north_email: user %s has no email; skipping %s pk=%s",
            user.pk,
            model_name,
            pk,
        )
        return {"ok": False, "reason": "no_user_email"}

    subject, body_content = _get_email_subject_and_body(obj)
    body = (
        f"Hey {user.username},\n\n"
        f"Here are the details for your {model_name}:\n\n"
        f"{body_content}\n"
        f"— {getattr(settings, 'THE_SITE_NAME', 'Personal Assistant')}"
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
            "send_true_north_email: SMTP error for %s pk=%s — will retry: %s",
            model_name,
            pk,
            exc,
        )
        raise

    logger.info(
        "send_true_north_email: sent %s (pk=%s) to user %s (%s)",
        model_name,
        pk,
        user.pk,
        user.email,
    )
    return {"ok": True, "model_name": model_name, "pk": pk, "user_id": user.pk}


@shared_task(**RETRY_KW)
def send_corevalue_reminder_email(self, schedule_id: int) -> dict:
    """
    Send a reminder email for the given CoreValueEmailSchedule ID.
    Updates ``last_sent`` and ``next_send`` on the schedule after a successful send.
    """
    from django.utils import timezone

    from .models import CoreValueEmailSchedule

    try:
        schedule = CoreValueEmailSchedule.objects.select_related(
            "user", "core_value"
        ).get(pk=schedule_id)
    except CoreValueEmailSchedule.DoesNotExist:
        logger.warning("CoreValueEmailSchedule %s not found", schedule_id)
        return {"ok": False, "reason": "schedule_not_found"}

    user = schedule.user
    if not getattr(user, "email", None):
        logger.warning(
            "User %s has no email; skipping CoreValue reminder %s",
            user.pk,
            schedule_id,
        )
        return {"ok": False, "reason": "no_user_email"}

    subject = schedule.get_subject()
    body = (
        f"Hey {user.username},\n\n"
        f"Here is your Core Value reminder:\n\n"
        f"{schedule.get_content()}\n"
        f"— {getattr(settings, 'THE_SITE_NAME', 'Personal Assistant')}"
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
            "send_corevalue_reminder_email: SMTP error for schedule %s"
            " — will retry: %s",
            schedule_id,
            exc,
        )
        raise

    now = timezone.now()
    schedule.last_sent = now
    schedule.next_send = schedule.compute_next_send()
    schedule.save(update_fields=["last_sent", "next_send"])

    logger.info(
        "send_corevalue_reminder_email: sent schedule %s to user %s (%s)",
        schedule_id,
        user.pk,
        user.email,
    )
    return {"ok": True, "schedule_id": schedule_id, "user_id": user.pk}


@shared_task(**RETRY_KW)
def send_core_value_email(self, user_id: int, core_value_id: int) -> dict:
    """
    Send a specific CoreValue (by ID) to a specific user (by ID).
    This is meant for scheduled/triggered sends using kwargs.
    """
    from django.contrib.auth import get_user_model

    from .models import CoreValue

    User = get_user_model()

    # ---- User lookup ----
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logger.warning("send_core_value_email: user %s not found", user_id)
        return {"ok": False, "reason": "user_not_found"}

    if not getattr(user, "email", None):
        logger.warning(
            "send_core_value_email: user %s has no email; skipping CoreValue pk=%s",
            user.pk,
            core_value_id,
        )
        return {"ok": False, "reason": "no_user_email"}

    # ---- CoreValue lookup ----
    try:
        core_value = CoreValue.objects.get(pk=core_value_id, user=user)
    except CoreValue.DoesNotExist:
        logger.warning(
            "send_core_value_email: CoreValue %s not found for user %s",
            core_value_id,
            user_id,
        )
        return {"ok": False, "reason": "core_value_not_found_for_user"}

    # ---- Build email content ----
    subject, body_content = _get_email_subject_and_body(core_value)
    body = (
        f"Hey {user.username},\n\n"
        f"Here is your Core Value:\n\n"
        f"{body_content}\n"
        f"— {getattr(settings, 'THE_SITE_NAME', 'Personal Assistant')}"
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
            "send_core_value_email: SMTP error for CoreValue %s — will retry: %s",
            core_value_id,
            exc,
        )
        raise

    logger.info(
        "send_core_value_email: sent CoreValue %s to user %s (%s)",
        core_value.id,
        user.id,
        user.email,
    )
    return {
        "ok": True,
        "core_value_id": core_value.id,
        "user_id": user.id,
    }


@shared_task(**RETRY_KW)
def send_goal_email(self, user_id: int, goal_id: int) -> dict:
    """
    Send a specific Goal (by ID) to a specific user (by ID).
    This is meant for scheduled/triggered sends using kwargs.
    """
    from django.contrib.auth import get_user_model

    from .models import Goal

    User = get_user_model()

    # ---- User lookup ----
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logger.warning("send_goal_email: user %s not found", user_id)
        return {"ok": False, "reason": "user_not_found"}

    if not getattr(user, "email", None):
        logger.warning(
            "send_goal_email: user %s has no email; skipping Goal pk=%s",
            user.pk,
            goal_id,
        )
        return {"ok": False, "reason": "no_user_email"}

    # ---- Goal lookup ----
    try:
        goal = Goal.objects.get(pk=goal_id, user=user)
    except Goal.DoesNotExist:
        logger.warning(
            "send_goal_email: Goal %s not found for user %s",
            goal_id,
            user_id,
        )
        return {"ok": False, "reason": "goal_not_found_for_user"}

    # ---- Build email content ----
    subject, body_content = _get_email_subject_and_body(goal)
    body = (
        f"Hey {user.username},\n\n"
        f"Here is your Goal:\n\n"
        f"{body_content}\n"
        f"— {getattr(settings, 'THE_SITE_NAME', 'Personal Assistant')}"
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
            "send_goal_email: SMTP error for Goal %s — will retry: %s",
            goal_id,
            exc,
        )
        raise

    logger.info(
        "send_goal_email: sent Goal %s to user %s (%s)",
        goal.id,
        user.id,
        user.email,
    )
    return {
        "ok": True,
        "goal_id": goal.id,
        "user_id": user.id,
    }


@shared_task(**RETRY_KW)
def send_milestone_email(self, user_id: int, milestone_id: int) -> dict:
    """
    Send a specific Milestone (by ID) to a specific user (by ID).
    This is meant for scheduled/triggered sends using kwargs.
    """
    from django.contrib.auth import get_user_model

    from .models import Milestone

    User = get_user_model()

    # ---- User lookup ----
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logger.warning("send_milestone_email: user %s not found", user_id)
        return {"ok": False, "reason": "user_not_found"}

    if not getattr(user, "email", None):
        logger.warning(
            "send_milestone_email: user %s has no email; skipping Milestone pk=%s",
            user.pk,
            milestone_id,
        )
        return {"ok": False, "reason": "no_user_email"}

    # ---- Milestone lookup ----
    try:
        milestone = Milestone.objects.select_related("goal").get(
            pk=milestone_id, user=user
        )
    except Milestone.DoesNotExist:
        logger.warning(
            "send_milestone_email: Milestone %s not found for user %s",
            milestone_id,
            user_id,
        )
        return {"ok": False, "reason": "milestone_not_found_for_user"}

    # ---- Build email content ----
    subject, body_content = _get_email_subject_and_body(milestone)
    body = (
        f"Hey {user.username},\n\n"
        f"Here is your Milestone:\n\n"
        f"{body_content}\n"
        f"— {getattr(settings, 'THE_SITE_NAME', 'Personal Assistant')}"
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
            "send_milestone_email: SMTP error for Milestone %s — will retry: %s",
            milestone_id,
            exc,
        )
        raise

    logger.info(
        "send_milestone_email: sent Milestone %s to user %s (%s)",
        milestone.id,
        user.id,
        user.email,
    )
    return {
        "ok": True,
        "milestone_id": milestone.id,
        "user_id": user.id,
    }


@shared_task(**RETRY_KW)
def send_value_action_email(self, user_id: int, value_action_id: int) -> dict:
    """
    Send a specific ValueAction (by ID) to a specific user (by ID).
    This is meant for scheduled/triggered sends using kwargs.
    """
    from django.contrib.auth import get_user_model

    from .models import ValueAction

    User = get_user_model()

    # ---- User lookup ----
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logger.warning("send_value_action_email: user %s not found", user_id)
        return {"ok": False, "reason": "user_not_found"}

    if not getattr(user, "email", None):
        logger.warning(
            "send_value_action_email: user %s has no email; skipping ValueAction pk=%s",
            user.pk,
            value_action_id,
        )
        return {"ok": False, "reason": "no_user_email"}

    # ---- ValueAction lookup ----
    try:
        value_action = ValueAction.objects.select_related("milestone").get(
            pk=value_action_id, user=user
        )
    except ValueAction.DoesNotExist:
        logger.warning(
            "send_value_action_email: ValueAction %s not found for user %s",
            value_action_id,
            user_id,
        )
        return {"ok": False, "reason": "value_action_not_found_for_user"}

    # ---- Build email content ----
    subject, body_content = _get_email_subject_and_body(value_action)
    body = (
        f"Hey {user.username},\n\n"
        f"Here is your Value Action:\n\n"
        f"{body_content}\n"
        f"— {getattr(settings, 'THE_SITE_NAME', 'Personal Assistant')}"
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
            "send_value_action_email: SMTP error for ValueAction %s — will retry: %s",
            value_action_id,
            exc,
        )
        raise

    logger.info(
        "send_value_action_email: sent ValueAction %s to user %s (%s)",
        value_action.id,
        user.id,
        user.email,
    )
    return {
        "ok": True,
        "value_action_id": value_action.id,
        "user_id": user.id,
    }


@shared_task
def process_due_corevalue_reminders() -> dict:
    """
    Periodic task: find all active CoreValueEmailSchedule records that are due
    and dispatch ``send_corevalue_reminder_email`` for each.

    Register this in django-celery-beat (e.g. every 15 minutes or every hour).
    """
    from django.utils import timezone

    from .models import CoreValueEmailSchedule

    now = timezone.now()
    due_ids = CoreValueEmailSchedule.objects.filter(
        is_active=True,
        next_send__lte=now,
    ).values_list("id", flat=True)

    dispatched = 0
    for schedule_id in due_ids:
        send_corevalue_reminder_email.delay(schedule_id)
        dispatched += 1

    logger.info(
        "process_due_corevalue_reminders: dispatched %s task(s)", dispatched
    )
    return {"dispatched": dispatched}
