# true_north/tests/test_models.py

from __future__ import annotations

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.utils import timezone

from true_north.models import (  # noqa E501
    CoreValue,
    CoreValueEmailSchedule,
    Goal,
    GoalStatus,
    Milestone,
    ValueAction,
    ValueActionStatus,
)
from true_north.tests.factories import (
    CoreValueEmailScheduleFactory,
    CoreValueFactory,
    CustomUserFactory,
    GoalFactory,
    MilestoneFactory,
    ValueActionFactory,
)

pytestmark = pytest.mark.django_db


# -------------------------
# CoreValue
# -------------------------


def test_corevalue_slug_autogenerates_when_blank():
    tiny_user = CustomUserFactory()
    grits_and_gravy = CoreValue(user=tiny_user, name="Deep Integrity", slug="")
    grits_and_gravy.save()

    assert grits_and_gravy.slug == "deep-integrity"


@pytest.mark.django_db(transaction=True)
def test_corevalue_unique_slug_per_user_enforced():
    tiny_user = CustomUserFactory()
    CoreValueFactory(user=tiny_user, name="Integrity", slug="integrity")

    with pytest.raises(IntegrityError):
        with transaction.atomic():
            CoreValueFactory(user=tiny_user, name="Something else", slug="integrity")


@pytest.mark.django_db(transaction=True)
def test_corevalue_unique_name_per_user_enforced():
    tiny_user = CustomUserFactory()
    CoreValueFactory(user=tiny_user, name="Integrity", slug="integrity")

    with pytest.raises(IntegrityError):
        with transaction.atomic():
            CoreValueFactory(user=tiny_user, name="Integrity", slug="integrity-2")


def test_corevalue_str_is_name():
    grits_and_gravy = CoreValueFactory(name="Accountability")
    assert str(grits_and_gravy) == "Accountability"


def test_corevalue_meta_ordering_is_order_then_name():
    tiny_user = CustomUserFactory()
    CoreValueFactory(user=tiny_user, name="Zulu", order=3)
    CoreValueFactory(user=tiny_user, name="Alpha", order=2)
    CoreValueFactory(user=tiny_user, name="Bravo", order=1)

    qs = CoreValue.objects.filter(user=tiny_user).values_list("name", flat=True)
    assert list(qs) == ["Bravo", "Alpha", "Zulu"]


def test_corevalue_order_auto_appends_on_create_when_zero():
    tiny_user = CustomUserFactory()
    CoreValueFactory(user=tiny_user, order=4)
    grits_and_gravy = CoreValueFactory(user=tiny_user, order=0)
    assert grits_and_gravy.order == 5


@pytest.mark.django_db(transaction=True)
def test_corevalue_unique_order_per_user_enforced():
    tiny_user = CustomUserFactory()
    CoreValueFactory(user=tiny_user, order=3)
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            CoreValueFactory(user=tiny_user, order=3)


# -------------------------
# Goal
# -------------------------


def test_goal_defaults_status_active():
    goal = GoalFactory()
    assert goal.status == GoalStatus.ACTIVE


def test_goal_syncs_user_from_value_if_user_missing():
    core_value = CoreValueFactory()
    goal = Goal(value=core_value, title="Learn to kayak", slug="")
    goal.save()

    assert goal.user_id == core_value.user_id
    assert goal.slug == "learn-to-kayak"


def test_goal_cross_user_linking_raises_validationerror():
    user_a = CustomUserFactory()
    user_b = CustomUserFactory()
    value_a = CoreValueFactory(user=user_a)

    goal = Goal(user=user_b, value=value_a, title="Mismatch", slug="mismatch")

    with pytest.raises(ValidationError) as exc:
        goal.save()

    assert "value" in exc.value.message_dict


def test_goal_unique_slug_per_user_enforced_via_full_clean_validationerror():
    """
    Because Goal.save() calls full_clean(), duplicates are caught before DB write,
    so we get ValidationError instead of IntegrityError.
    """
    tiny_user = CustomUserFactory()
    value = CoreValueFactory(user=tiny_user)

    GoalFactory(user=tiny_user, value=value, title="One", slug="same-slug")

    with pytest.raises(ValidationError) as exc:
        GoalFactory(user=tiny_user, value=value, title="Two", slug="same-slug")

    assert "__all__" in exc.value.message_dict


def test_goal_str_is_title():
    goal = GoalFactory(title="Be consistent")
    assert str(goal) == "Be consistent"


def test_goal_meta_ordering_is_order_then_title():
    tiny_user = CustomUserFactory()
    value_one = CoreValueFactory(user=tiny_user)
    value_two = CoreValueFactory(user=tiny_user, name="Service", slug="")

    GoalFactory(user=tiny_user, value=value_one, title="Zulu", order=2)
    GoalFactory(user=tiny_user, value=value_two, title="Alpha", order=2)
    GoalFactory(user=tiny_user, value=value_one, title="Bravo", order=1)

    qs = Goal.objects.filter(user=tiny_user).values_list("title", flat=True)
    assert list(qs) == ["Bravo", "Alpha", "Zulu"]


def test_goal_order_auto_appends_on_create_when_zero():
    tiny_user = CustomUserFactory()
    value = CoreValueFactory(user=tiny_user)
    GoalFactory(user=tiny_user, value=value, order=2)
    goal = GoalFactory(user=tiny_user, value=value, order=0)
    assert goal.order == 3


def test_goal_unique_order_per_value_enforced():
    tiny_user = CustomUserFactory()
    value = CoreValueFactory(user=tiny_user)
    GoalFactory(user=tiny_user, value=value, order=7)
    with pytest.raises(ValidationError):
        GoalFactory(user=tiny_user, value=value, order=7)


def test_goal_unique_order_without_value_enforced():
    tiny_user = CustomUserFactory()
    GoalFactory(user=tiny_user, value=None, order=7)
    with pytest.raises(ValidationError):
        GoalFactory(user=tiny_user, value=None, order=7)


# -------------------------
# Milestone
# -------------------------


def test_milestone_syncs_user_from_goal_if_user_missing_and_autoslugs():
    goal = GoalFactory()
    milestone = Milestone(goal=goal, description="First checkpoint", slug="")
    milestone.save()

    assert milestone.user_id == goal.user_id
    assert milestone.slug == "first-checkpoint"


def test_milestone_cross_user_linking_raises_validationerror():
    user_a = CustomUserFactory()
    user_b = CustomUserFactory()

    value_a = CoreValueFactory(user=user_a)
    goal_a = GoalFactory(user=user_a, value=value_a)

    milestone = Milestone(
        user=user_b, goal=goal_a, description="Mismatch", slug="mismatch"
    )

    with pytest.raises(ValidationError) as exc:
        milestone.save()

    assert "goal" in exc.value.message_dict


def test_milestone_unique_slug_per_goal_per_user_enforced_via_full_clean_validationerror():  # noqa E501
    """
    Because Milestone.save() calls full_clean(), duplicates are caught before DB write,
    so we get ValidationError instead of IntegrityError.
    """
    goal = GoalFactory()
    MilestoneFactory(user=goal.user, goal=goal, description="One", slug="same")

    with pytest.raises(ValidationError) as exc:
        MilestoneFactory(user=goal.user, goal=goal, description="Two", slug="same")

    assert "__all__" in exc.value.message_dict


def test_milestone_str_includes_goal_and_description():
    milestone = MilestoneFactory(description="Do the thing")
    s = str(milestone)
    assert "Do the thing" in s
    assert str(milestone.goal) in s


def test_milestone_meta_ordering_is_order_then_description():
    goal = GoalFactory()
    other_goal = GoalFactory(user=goal.user, value=CoreValueFactory(user=goal.user))
    MilestoneFactory(goal=goal, user=goal.user, description="Zulu", order=2)
    MilestoneFactory(goal=other_goal, user=goal.user, description="Alpha", order=2)
    MilestoneFactory(goal=goal, user=goal.user, description="Bravo", order=1)

    qs = Milestone.objects.filter(user=goal.user).values_list("description", flat=True)
    assert list(qs) == ["Bravo", "Alpha", "Zulu"]


def test_milestone_order_auto_appends_on_create_when_zero():
    goal = GoalFactory()
    MilestoneFactory(goal=goal, user=goal.user, order=8)
    milestone = MilestoneFactory(goal=goal, user=goal.user, order=0)
    assert milestone.order == 9


def test_milestone_unique_order_per_goal_enforced():
    goal = GoalFactory()
    MilestoneFactory(goal=goal, user=goal.user, order=4)
    with pytest.raises(ValidationError):
        MilestoneFactory(goal=goal, user=goal.user, order=4)


# -------------------------
# ValueAction
# -------------------------


def test_task_defaults_status_todo():
    task = ValueActionFactory()
    assert task.status == ValueActionStatus.TODO


def test_task_cross_user_linking_raises_validationerror():
    user_a = CustomUserFactory()
    user_b = CustomUserFactory()

    value_a = CoreValueFactory(user=user_a)
    goal_a = GoalFactory(user=user_a, value=value_a)
    milestone_a = MilestoneFactory(user=user_a, goal=goal_a)

    task = ValueAction(user=user_b, milestone=milestone_a, content="Mismatch content")

    with pytest.raises(ValidationError) as exc:
        task.save()

    assert "milestone" in exc.value.message_dict


def test_task_syncs_user_from_milestone_if_user_missing():
    milestone = MilestoneFactory()
    task = ValueAction(milestone=milestone, user=None, content="Do it")
    task.save()

    assert task.user_id == milestone.user_id


def test_task_str_truncates_long_content():
    milestone = MilestoneFactory()
    long_text = "x" * 200
    task = ValueAction(milestone=milestone, user=milestone.user, content=long_text)
    task.save()

    s = str(task)
    assert s.endswith("…")
    assert len(s) <= 61  # 60 + ellipsis


def test_task_str_short_content_no_ellipsis():
    task = ValueActionFactory(content="Short line")
    assert str(task) == "Short line"


def test_task_meta_ordering_is_order_then_id():
    milestone = MilestoneFactory()
    other_milestone = MilestoneFactory(
        user=milestone.user,
        goal=GoalFactory(
            user=milestone.user, value=CoreValueFactory(user=milestone.user)
        ),
    )
    t1 = ValueActionFactory(milestone=milestone, user=milestone.user, order=5)
    t2 = ValueActionFactory(milestone=other_milestone, user=milestone.user, order=5)
    t3 = ValueActionFactory(milestone=milestone, user=milestone.user, order=1)

    qs = ValueAction.objects.filter(user=milestone.user).values_list("id", flat=True)
    assert list(qs) == [t3.id, t1.id, t2.id]


def test_task_order_auto_appends_on_create_when_zero():
    milestone = MilestoneFactory()
    ValueActionFactory(milestone=milestone, user=milestone.user, order=1)
    task = ValueActionFactory(milestone=milestone, user=milestone.user, order=0)
    assert task.order == 2


def test_task_unique_order_per_milestone_enforced():
    milestone = MilestoneFactory()
    ValueActionFactory(milestone=milestone, user=milestone.user, order=3)
    with pytest.raises(ValidationError):
        ValueActionFactory(milestone=milestone, user=milestone.user, order=3)


# -------------------------
# CoreValueEmailSchedule
# -------------------------


def test_schedule_clean_rejects_mismatched_user():
    user_a = CustomUserFactory()
    user_b = CustomUserFactory()
    cv = CoreValueFactory(user=user_a)

    schedule = CoreValueEmailSchedule(
        user=user_b,
        core_value=cv,
        frequency=CoreValueEmailSchedule.DAILY,
    )
    with pytest.raises(ValidationError) as exc:
        schedule.clean()
    assert "core_value" in exc.value.message_dict


def test_schedule_clean_rejects_invalid_days_of_week():
    user = CustomUserFactory()
    cv = CoreValueFactory(user=user)

    schedule = CoreValueEmailSchedule(
        user=user,
        core_value=cv,
        days_of_week="0,7,3",  # 7 is invalid
    )
    with pytest.raises(ValidationError) as exc:
        schedule.clean()
    assert "days_of_week" in exc.value.message_dict


def test_get_days_of_week_list_parses_comma_separated():
    schedule = CoreValueEmailScheduleFactory.build(days_of_week="0,2,4")
    assert schedule.get_days_of_week_list() == [0, 2, 4]


def test_get_days_of_week_list_empty_string_returns_empty():
    schedule = CoreValueEmailScheduleFactory.build(days_of_week="")
    assert schedule.get_days_of_week_list() == []


def test_compute_next_send_frequency_only_adds_delta():
    """With no days_of_week or send_time, next_send is now + frequency delta."""
    from datetime import timedelta

    schedule = CoreValueEmailScheduleFactory.build(
        frequency=CoreValueEmailSchedule.DAILY,
        send_time=None,
        days_of_week="",
    )
    before = timezone.now()
    result = schedule.compute_next_send()
    after = timezone.now()

    assert before + timedelta(days=1) <= result <= after + timedelta(days=1, seconds=5)


def test_compute_next_send_send_time_anchors_time_of_day():
    """When send_time is set (no days_of_week), next_send lands on send_time."""
    from datetime import time

    schedule = CoreValueEmailScheduleFactory.build(
        frequency=CoreValueEmailSchedule.DAILY,
        send_time=time(8, 30),
        days_of_week="",
    )
    result = schedule.compute_next_send()
    tz = timezone.get_current_timezone()
    local_result = result.astimezone(tz)
    assert local_result.hour == 8
    assert local_result.minute == 30


def test_compute_next_send_days_of_week_returns_future_weekday():
    """When days_of_week is set, next_send falls on one of those weekdays."""
    from datetime import time

    # Schedule for every day of the week at 09:00.
    schedule = CoreValueEmailScheduleFactory.build(
        frequency=CoreValueEmailSchedule.DAILY,
        send_time=time(9, 0),
        days_of_week="0,1,2,3,4,5,6",  # all days
    )
    result = schedule.compute_next_send()
    assert result > timezone.now()
    tz = timezone.get_current_timezone()
    local_result = result.astimezone(tz)
    assert local_result.hour == 9
    assert local_result.minute == 0


def test_compute_next_send_days_of_week_ignores_frequency():
    """With days_of_week set the frequency field is not used for timing."""
    from datetime import time

    # Pick a specific weekday to ensure a deterministic result.
    # We find next Monday (weekday 0).
    schedule = CoreValueEmailScheduleFactory.build(
        frequency=CoreValueEmailSchedule.MONTHLY,  # would be 30 days otherwise
        send_time=time(7, 0),
        days_of_week="0",  # Monday only
    )
    result = schedule.compute_next_send()
    tz = timezone.get_current_timezone()
    local_result = result.astimezone(tz)

    # Must be in the future and be a Monday.
    assert result > timezone.now()
    assert local_result.weekday() == 0
    assert local_result.hour == 7


def test_compute_next_send_send_time_today_when_still_in_future():
    """A schedule created before send_time should fire TODAY, not tomorrow."""
    from datetime import datetime as _dt
    from datetime import time  # noqa: F401
    from unittest.mock import patch

    tz = timezone.get_current_timezone()
    # Simulate "now" as 08:53 local time so that 09:00 is still in the future.
    now_local_date = timezone.now().astimezone(tz).date()
    now_utc = timezone.make_aware(_dt.combine(now_local_date, time(8, 53, 0)), tz)

    send_time = time(9, 0)
    schedule = CoreValueEmailScheduleFactory.build(
        frequency=CoreValueEmailSchedule.DAILY,
        send_time=send_time,
        days_of_week="",
    )

    with patch("true_north.models.timezone") as mock_tz:
        mock_tz.now.return_value = now_utc
        mock_tz.get_current_timezone.return_value = tz
        mock_tz.make_aware.side_effect = timezone.make_aware
        result = schedule.compute_next_send()

    local_result = result.astimezone(tz)
    # Should be TODAY at 09:00, not tomorrow.
    assert local_result.date() == now_local_date
    assert local_result.hour == 9
    assert local_result.minute == 0
