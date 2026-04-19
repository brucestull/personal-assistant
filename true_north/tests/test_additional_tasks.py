from unittest.mock import patch
from datetime import timedelta

import pytest

from true_north.tests.factories import (
    CoreValueEmailScheduleFactory,
    CoreValueFactory,
    CustomUserFactory,
)

pytestmark = pytest.mark.django_db


def test_get_email_subject_and_body_default_branch():
    from true_north.tasks import _get_email_subject_and_body

    class Unknown:
        def __str__(self):
            return "unknown item"

    subject, body = _get_email_subject_and_body(Unknown())
    assert "True North Item" in subject
    assert body == "unknown item"


def test_send_email_helper_empty_and_missing_sender():
    from true_north.tasks import _send_email

    _send_email("s", "b", [])
    with patch("true_north.tasks.DEFAULT_FROM_EMAIL", None):
        with pytest.raises(ValueError):
            _send_email("s", "b", ["to@example.com"])


def test_send_true_north_email_branches():
    from true_north.tasks import send_true_north_email

    unknown = send_true_north_email("BogusModel", 1)
    assert unknown == {"ok": False, "reason": "unknown_model"}

    user = CustomUserFactory(email="tn@example.com")
    core = CoreValueFactory(user=user, name="Integrity")
    missing_obj = send_true_north_email("CoreValue", 999999)
    assert missing_obj["reason"] == "object_not_found"

    user_no_email = CustomUserFactory(email="")
    core_no_email = CoreValueFactory(user=user_no_email)
    no_email = send_true_north_email("CoreValue", core_no_email.id)
    assert no_email["reason"] == "no_user_email"

    with patch("true_north.tasks._send_email") as mock_send:
        ok = send_true_north_email("CoreValue", core.id)
    assert ok["ok"] is True
    mock_send.assert_called_once()


def test_send_corevalue_reminder_branches():
    from true_north.tasks import send_corevalue_reminder_email

    missing = send_corevalue_reminder_email(999999)
    assert missing["reason"] == "schedule_not_found"

    user_no_email = CustomUserFactory(email="")
    schedule_no_email = CoreValueEmailScheduleFactory(user=user_no_email)
    no_email = send_corevalue_reminder_email(schedule_no_email.id)
    assert no_email["reason"] == "no_user_email"

    schedule = CoreValueEmailScheduleFactory(
        user=CustomUserFactory(email="cv@example.com")
    )
    with patch("true_north.tasks._send_email") as mock_send:
        result = send_corevalue_reminder_email(schedule.id)
    assert result["ok"] is True
    mock_send.assert_called_once()


def test_process_due_corevalue_reminders_dispatches_due_items():
    from django.utils import timezone

    from true_north.tasks import process_due_corevalue_reminders

    due = CoreValueEmailScheduleFactory(next_send=timezone.now())
    CoreValueEmailScheduleFactory(
        next_send=timezone.now(),
        is_active=False,
    )
    CoreValueEmailScheduleFactory(
        next_send=timezone.now() + timedelta(days=3),
    )

    with patch("true_north.tasks.send_corevalue_reminder_email.delay") as mock_delay:
        result = process_due_corevalue_reminders()
    assert result == {"dispatched": 1}
    mock_delay.assert_called_once_with(due.id)
