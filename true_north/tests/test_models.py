# true_north/tests/test_models.py

from __future__ import annotations

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from true_north.models import CoreValue, Goal, Milestone, Task, GoalStatus, TaskStatus
from true_north.tests.factories import (
    CustomUserFactory,
    CoreValueFactory,
    GoalFactory,
    MilestoneFactory,
    TaskFactory,
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
    CoreValueFactory(user=tiny_user, name="Zulu", order=2)
    CoreValueFactory(user=tiny_user, name="Alpha", order=2)
    CoreValueFactory(user=tiny_user, name="Bravo", order=1)

    qs = CoreValue.objects.filter(user=tiny_user).values_list("name", flat=True)
    assert list(qs) == ["Bravo", "Alpha", "Zulu"]


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
    value = CoreValueFactory(user=tiny_user)

    GoalFactory(user=tiny_user, value=value, title="Zulu", order=2)
    GoalFactory(user=tiny_user, value=value, title="Alpha", order=2)
    GoalFactory(user=tiny_user, value=value, title="Bravo", order=1)

    qs = Goal.objects.filter(user=tiny_user).values_list("title", flat=True)
    assert list(qs) == ["Bravo", "Alpha", "Zulu"]


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

    milestone = Milestone(user=user_b, goal=goal_a, description="Mismatch", slug="mismatch")

    with pytest.raises(ValidationError) as exc:
        milestone.save()

    assert "goal" in exc.value.message_dict


def test_milestone_unique_slug_per_goal_per_user_enforced_via_full_clean_validationerror():
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
    MilestoneFactory(goal=goal, user=goal.user, description="Zulu", order=2)
    MilestoneFactory(goal=goal, user=goal.user, description="Alpha", order=2)
    MilestoneFactory(goal=goal, user=goal.user, description="Bravo", order=1)

    qs = Milestone.objects.filter(goal=goal).values_list("description", flat=True)
    assert list(qs) == ["Bravo", "Alpha", "Zulu"]


# -------------------------
# Task
# -------------------------

def test_task_defaults_status_todo():
    task = TaskFactory()
    assert task.status == TaskStatus.TODO


def test_task_cross_user_linking_raises_validationerror():
    user_a = CustomUserFactory()
    user_b = CustomUserFactory()

    value_a = CoreValueFactory(user=user_a)
    goal_a = GoalFactory(user=user_a, value=value_a)
    milestone_a = MilestoneFactory(user=user_a, goal=goal_a)

    task = Task(user=user_b, milestone=milestone_a, content="Mismatch content")

    with pytest.raises(ValidationError) as exc:
        task.save()

    assert "milestone" in exc.value.message_dict


def test_task_syncs_user_from_milestone_if_user_missing():
    milestone = MilestoneFactory()
    task = Task(milestone=milestone, user=None, content="Do it")
    task.save()

    assert task.user_id == milestone.user_id


def test_task_str_truncates_long_content():
    milestone = MilestoneFactory()
    long_text = "x" * 200
    task = Task(milestone=milestone, user=milestone.user, content=long_text)
    task.save()

    s = str(task)
    assert s.endswith("…")
    assert len(s) <= 61  # 60 + ellipsis


def test_task_str_short_content_no_ellipsis():
    task = TaskFactory(content="Short line")
    assert str(task) == "Short line"


def test_task_meta_ordering_is_order_then_id():
    milestone = MilestoneFactory()
    t1 = TaskFactory(milestone=milestone, user=milestone.user, order=5)
    t2 = TaskFactory(milestone=milestone, user=milestone.user, order=5)
    t3 = TaskFactory(milestone=milestone, user=milestone.user, order=1)

    qs = Task.objects.filter(milestone=milestone).values_list("id", flat=True)
    assert list(qs) == [t3.id, t1.id, t2.id]
