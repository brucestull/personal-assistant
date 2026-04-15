# true_north/tests/test_views.py

import json

import pytest
from django.contrib.auth.models import Permission
from django.urls import reverse
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from true_north.tests.factories import (
    CoreValueEmailScheduleFactory,
    CoreValueFactory,
    CustomUserFactory,
    GoalFactory,
    MilestoneFactory,
    ValueActionFactory,
)
from true_north.utils import periodic_task_name


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _login(client, user, password="password123"):
    user.registration_accepted = True
    user.save()
    client.login(username=user.username, password=password)
    return user


def _grant_schedule_permissions(user):
    codenames = (
        "add_crontabschedule",
        "view_crontabschedule",
        "add_periodictask",
        "change_periodictask",
        "delete_periodictask",
        "view_periodictask",
    )
    permissions = Permission.objects.filter(
        content_type__app_label="django_celery_beat",
        codename__in=codenames,
    )
    user.user_permissions.add(*permissions)


# ---------------------------------------------------------------------------
# CoreValue CRUD
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_corevalue_list_requires_login(client):
    url = reverse("true_north:core-value-list")
    response = client.get(url)
    assert response.status_code in (302, 403)


@pytest.mark.django_db
def test_corevalue_list_shows_user_values(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    url = reverse("true_north:core-value-list")
    response = client.get(url)
    assert response.status_code == 200
    assert cv.name.encode() in response.content


@pytest.mark.django_db
def test_corevalue_list_hides_other_user_values(client):
    user = CustomUserFactory()
    other = CustomUserFactory()
    _login(client, user)
    cv_other = CoreValueFactory(user=other)
    url = reverse("true_north:core-value-list")
    response = client.get(url)
    assert cv_other.name.encode() not in response.content


@pytest.mark.django_db
def test_corevalue_create(client):
    user = CustomUserFactory()
    _login(client, user)
    url = reverse("true_north:core-value-create")
    response = client.post(url, {"name": "Integrity", "is_active": True, "order": 0})
    assert response.status_code == 302
    from true_north.models import CoreValue

    assert CoreValue.objects.filter(user=user, name="Integrity").exists()


@pytest.mark.django_db
def test_corevalue_update(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    url = reverse("true_north:core-value-update", kwargs={"pk": cv.pk})
    response = client.post(
        url, {"name": "Courage", "is_active": True, "order": 0}
    )
    assert response.status_code == 302
    cv.refresh_from_db()
    assert cv.name == "Courage"


@pytest.mark.django_db
def test_corevalue_update_forbidden_other_user(client):
    user = CustomUserFactory()
    other = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=other)
    url = reverse("true_north:core-value-update", kwargs={"pk": cv.pk})
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_corevalue_delete(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    url = reverse("true_north:core-value-delete", kwargs={"pk": cv.pk})
    response = client.post(url)
    assert response.status_code == 302
    from true_north.models import CoreValue

    assert not CoreValue.objects.filter(pk=cv.pk).exists()


@pytest.mark.django_db
def test_corevalue_delete_forbidden_other_user(client):
    user = CustomUserFactory()
    other = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=other)
    url = reverse("true_north:core-value-delete", kwargs={"pk": cv.pk})
    response = client.post(url)
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Goal CRUD
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_goal_list_shows_user_goals(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    url = reverse("true_north:goal-list")
    response = client.get(url)
    assert response.status_code == 200
    assert goal.title.encode() in response.content


@pytest.mark.django_db
def test_goal_create(client):
    user = CustomUserFactory()
    _login(client, user)
    url = reverse("true_north:goal-create")
    response = client.post(
        url,
        {
            "title": "New Goal",
            "status": "active",
            "is_active": True,
            "order": 0,
        },
    )
    assert response.status_code == 302
    from true_north.models import Goal

    assert Goal.objects.filter(user=user, title="New Goal").exists()


@pytest.mark.django_db
def test_goal_update(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    url = reverse("true_north:goal-update", kwargs={"pk": goal.pk})
    response = client.post(
        url,
        {
            "title": "Updated Goal",
            "status": "paused",
            "is_active": True,
            "order": 0,
        },
    )
    assert response.status_code == 302
    goal.refresh_from_db()
    assert goal.title == "Updated Goal"


@pytest.mark.django_db
def test_goal_delete(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    url = reverse("true_north:goal-delete", kwargs={"pk": goal.pk})
    response = client.post(url)
    assert response.status_code == 302
    from true_north.models import Goal

    assert not Goal.objects.filter(pk=goal.pk).exists()


# ---------------------------------------------------------------------------
# Milestone CRUD
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_milestone_list_shows_user_milestones(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    milestone = MilestoneFactory(goal=goal, user=user)
    url = reverse("true_north:milestone-list")
    response = client.get(url)
    assert response.status_code == 200
    assert milestone.description.encode() in response.content


@pytest.mark.django_db
def test_milestone_create(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    url = reverse("true_north:milestone-create")
    response = client.post(
        url,
        {
            "goal": goal.pk,
            "description": "New Milestone",
            "is_completed": False,
            "order": 0,
        },
    )
    assert response.status_code == 302
    from true_north.models import Milestone

    assert Milestone.objects.filter(user=user, description="New Milestone").exists()


@pytest.mark.django_db
def test_milestone_update(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    milestone = MilestoneFactory(goal=goal, user=user)
    url = reverse("true_north:milestone-update", kwargs={"pk": milestone.pk})
    response = client.post(
        url,
        {
            "goal": goal.pk,
            "description": "Updated Milestone",
            "is_completed": True,
            "order": 0,
        },
    )
    assert response.status_code == 302
    milestone.refresh_from_db()
    assert milestone.description == "Updated Milestone"


@pytest.mark.django_db
def test_milestone_delete(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    milestone = MilestoneFactory(goal=goal, user=user)
    url = reverse("true_north:milestone-delete", kwargs={"pk": milestone.pk})
    response = client.post(url)
    assert response.status_code == 302
    from true_north.models import Milestone

    assert not Milestone.objects.filter(pk=milestone.pk).exists()


# ---------------------------------------------------------------------------
# ValueAction CRUD
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_valueaction_list_shows_user_actions(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    milestone = MilestoneFactory(goal=goal, user=user)
    action = ValueActionFactory(milestone=milestone, user=user)
    url = reverse("true_north:value-action-list")
    response = client.get(url)
    assert response.status_code == 200
    assert action.content[:20].encode() in response.content


@pytest.mark.django_db
def test_valueaction_create(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    milestone = MilestoneFactory(goal=goal, user=user)
    url = reverse("true_north:value-action-create")
    response = client.post(
        url,
        {
            "milestone": milestone.pk,
            "content": "Do the thing",
            "status": "todo",
            "order": 0,
        },
    )
    assert response.status_code == 302
    from true_north.models import ValueAction

    assert ValueAction.objects.filter(user=user, content="Do the thing").exists()


@pytest.mark.django_db
def test_valueaction_update(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    milestone = MilestoneFactory(goal=goal, user=user)
    action = ValueActionFactory(milestone=milestone, user=user)
    url = reverse("true_north:value-action-update", kwargs={"pk": action.pk})
    response = client.post(
        url,
        {
            "milestone": milestone.pk,
            "content": "Updated content",
            "status": "doing",
            "order": 0,
        },
    )
    assert response.status_code == 302
    action.refresh_from_db()
    assert action.content == "Updated content"
    assert action.status == "doing"


@pytest.mark.django_db
def test_valueaction_delete(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    milestone = MilestoneFactory(goal=goal, user=user)
    action = ValueActionFactory(milestone=milestone, user=user)
    url = reverse("true_north:value-action-delete", kwargs={"pk": action.pk})
    response = client.post(url)
    assert response.status_code == 302
    from true_north.models import ValueAction

    assert not ValueAction.objects.filter(pk=action.pk).exists()


# ---------------------------------------------------------------------------
# Detail views
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_corevalue_detail_requires_login(client):
    user = CustomUserFactory()
    cv = CoreValueFactory(user=user)
    url = reverse("true_north:core-value-detail", kwargs={"pk": cv.pk})
    response = client.get(url)
    assert response.status_code in (302, 403)


@pytest.mark.django_db
def test_corevalue_detail_shows_value_and_goals(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    url = reverse("true_north:core-value-detail", kwargs={"pk": cv.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert cv.name.encode() in response.content
    assert goal.title.encode() in response.content


@pytest.mark.django_db
def test_corevalue_detail_hidden_from_other_user(client):
    user = CustomUserFactory()
    other = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=other)
    url = reverse("true_north:core-value-detail", kwargs={"pk": cv.pk})
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_goal_detail_requires_login(client):
    user = CustomUserFactory()
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    url = reverse("true_north:goal-detail", kwargs={"pk": goal.pk})
    response = client.get(url)
    assert response.status_code in (302, 403)


@pytest.mark.django_db
def test_goal_detail_shows_goal_and_milestones(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    milestone = MilestoneFactory(goal=goal, user=user)
    url = reverse("true_north:goal-detail", kwargs={"pk": goal.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert goal.title.encode() in response.content
    assert milestone.description.encode() in response.content


@pytest.mark.django_db
def test_goal_detail_hidden_from_other_user(client):
    user = CustomUserFactory()
    other = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=other)
    goal = GoalFactory(value=cv, user=other)
    url = reverse("true_north:goal-detail", kwargs={"pk": goal.pk})
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_milestone_detail_requires_login(client):
    user = CustomUserFactory()
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    milestone = MilestoneFactory(goal=goal, user=user)
    url = reverse("true_north:milestone-detail", kwargs={"pk": milestone.pk})
    response = client.get(url)
    assert response.status_code in (302, 403)


@pytest.mark.django_db
def test_milestone_detail_shows_milestone_and_actions(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    milestone = MilestoneFactory(goal=goal, user=user)
    action = ValueActionFactory(milestone=milestone, user=user)
    url = reverse("true_north:milestone-detail", kwargs={"pk": milestone.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert milestone.description.encode() in response.content
    assert action.content[:20].encode() in response.content


@pytest.mark.django_db
def test_milestone_detail_hidden_from_other_user(client):
    user = CustomUserFactory()
    other = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=other)
    goal = GoalFactory(value=cv, user=other)
    milestone = MilestoneFactory(goal=goal, user=other)
    url = reverse("true_north:milestone-detail", kwargs={"pk": milestone.pk})
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_valueaction_detail_requires_login(client):
    user = CustomUserFactory()
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    milestone = MilestoneFactory(goal=goal, user=user)
    action = ValueActionFactory(milestone=milestone, user=user)
    url = reverse("true_north:value-action-detail", kwargs={"pk": action.pk})
    response = client.get(url)
    assert response.status_code in (302, 403)


@pytest.mark.django_db
def test_valueaction_detail_shows_action(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    milestone = MilestoneFactory(goal=goal, user=user)
    action = ValueActionFactory(milestone=milestone, user=user)
    url = reverse("true_north:value-action-detail", kwargs={"pk": action.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert action.content.encode() in response.content


@pytest.mark.django_db
def test_valueaction_detail_hidden_from_other_user(client):
    user = CustomUserFactory()
    other = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=other)
    goal = GoalFactory(value=cv, user=other)
    milestone = MilestoneFactory(goal=goal, user=other)
    action = ValueActionFactory(milestone=milestone, user=other)
    url = reverse("true_north:value-action-detail", kwargs={"pk": action.pk})
    response = client.get(url)
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Send-Email views
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_corevalue_send_email_queues_task(client, mailoutbox):
    user = CustomUserFactory(email="user@example.com")
    _login(client, user)
    cv = CoreValueFactory(user=user)
    url = reverse("true_north:core-value-send-email", kwargs={"pk": cv.pk})
    response = client.post(url)
    assert response.status_code == 302
    assert response["Location"] == reverse("true_north:core-value-list")
    # With CELERY_TASK_ALWAYS_EAGER the task runs synchronously; check email sent.
    assert len(mailoutbox) == 1
    assert cv.name in mailoutbox[0].subject


@pytest.mark.django_db
def test_corevalue_send_email_forbidden_other_user(client):
    user = CustomUserFactory()
    other = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=other)
    url = reverse("true_north:core-value-send-email", kwargs={"pk": cv.pk})
    response = client.post(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_goal_send_email_queues_task(client, mailoutbox):
    user = CustomUserFactory(email="user@example.com")
    _login(client, user)
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    url = reverse("true_north:goal-send-email", kwargs={"pk": goal.pk})
    response = client.post(url)
    assert response.status_code == 302
    assert response["Location"] == reverse("true_north:goal-list")
    assert len(mailoutbox) == 1
    assert goal.title in mailoutbox[0].subject


@pytest.mark.django_db
def test_goal_send_email_forbidden_other_user(client):
    user = CustomUserFactory()
    other = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=other)
    goal = GoalFactory(value=cv, user=other)
    url = reverse("true_north:goal-send-email", kwargs={"pk": goal.pk})
    response = client.post(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_milestone_send_email_queues_task(client, mailoutbox):
    user = CustomUserFactory(email="user@example.com")
    _login(client, user)
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    milestone = MilestoneFactory(goal=goal, user=user)
    url = reverse("true_north:milestone-send-email", kwargs={"pk": milestone.pk})
    response = client.post(url)
    assert response.status_code == 302
    assert response["Location"] == reverse("true_north:milestone-list")
    assert len(mailoutbox) == 1
    assert milestone.description[:20] in mailoutbox[0].subject


@pytest.mark.django_db
def test_milestone_send_email_forbidden_other_user(client):
    user = CustomUserFactory()
    other = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=other)
    goal = GoalFactory(value=cv, user=other)
    milestone = MilestoneFactory(goal=goal, user=other)
    url = reverse("true_north:milestone-send-email", kwargs={"pk": milestone.pk})
    response = client.post(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_valueaction_send_email_queues_task(client, mailoutbox):
    user = CustomUserFactory(email="user@example.com")
    _login(client, user)
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    milestone = MilestoneFactory(goal=goal, user=user)
    action = ValueActionFactory(milestone=milestone, user=user)
    url = reverse("true_north:value-action-send-email", kwargs={"pk": action.pk})
    response = client.post(url)
    assert response.status_code == 302
    assert response["Location"] == reverse("true_north:value-action-list")
    assert len(mailoutbox) == 1
    assert action.content[:20] in mailoutbox[0].subject


@pytest.mark.django_db
def test_valueaction_send_email_forbidden_other_user(client):
    user = CustomUserFactory()
    other = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=other)
    goal = GoalFactory(value=cv, user=other)
    milestone = MilestoneFactory(goal=goal, user=other)
    action = ValueActionFactory(milestone=milestone, user=other)
    url = reverse("true_north:value-action-send-email", kwargs={"pk": action.pk})
    response = client.post(url)
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# CoreValueEmailSchedule CRUD
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_corevalue_email_schedule_list_requires_login(client):
    url = reverse("true_north:corevalue-email-schedule-list")
    response = client.get(url)
    assert response.status_code in (302, 403)


@pytest.mark.django_db
def test_corevalue_email_schedule_list_shows_user_schedules(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    schedule = CoreValueEmailScheduleFactory(user=user, core_value=cv)
    url = reverse("true_north:corevalue-email-schedule-list")
    response = client.get(url)
    assert response.status_code == 200
    assert schedule.get_frequency_display().encode() in response.content


@pytest.mark.django_db
def test_corevalue_email_schedule_list_hides_other_user_schedules(client):
    user = CustomUserFactory()
    other = CustomUserFactory()
    _login(client, user)
    cv_other = CoreValueFactory(user=other)
    CoreValueEmailScheduleFactory(user=other, core_value=cv_other)
    url = reverse("true_north:corevalue-email-schedule-list")
    response = client.get(url)
    assert cv_other.name.encode() not in response.content


@pytest.mark.django_db
def test_corevalue_email_schedule_create(client):
    from true_north.models import CoreValueEmailSchedule

    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    url = reverse("true_north:corevalue-email-schedule-create")
    response = client.post(
        url, {"core_value": cv.pk, "frequency": "daily", "is_active": True}
    )
    assert response.status_code == 302
    assert CoreValueEmailSchedule.objects.filter(user=user, core_value=cv).exists()


@pytest.mark.django_db
def test_corevalue_email_schedule_create_prefills_core_value(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    url = reverse("true_north:corevalue-email-schedule-create") + f"?core_value={cv.pk}"
    response = client.get(url)
    assert response.status_code == 200
    assert str(cv.pk).encode() in response.content


@pytest.mark.django_db
def test_corevalue_email_schedule_update(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    schedule = CoreValueEmailScheduleFactory(user=user, core_value=cv)
    url = reverse(
        "true_north:corevalue-email-schedule-update", kwargs={"pk": schedule.pk}
    )
    response = client.post(
        url, {"core_value": cv.pk, "frequency": "weekly", "is_active": True}
    )
    assert response.status_code == 302
    schedule.refresh_from_db()
    assert schedule.frequency == "weekly"


@pytest.mark.django_db
def test_corevalue_email_schedule_update_forbidden_other_user(client):
    user = CustomUserFactory()
    other = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=other)
    schedule = CoreValueEmailScheduleFactory(user=other, core_value=cv)
    url = reverse(
        "true_north:corevalue-email-schedule-update", kwargs={"pk": schedule.pk}
    )
    response = client.post(
        url, {"core_value": cv.pk, "frequency": "weekly", "is_active": True}
    )
    assert response.status_code in (403, 404)


@pytest.mark.django_db
def test_corevalue_email_schedule_delete(client):
    from true_north.models import CoreValueEmailSchedule

    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    schedule = CoreValueEmailScheduleFactory(user=user, core_value=cv)
    url = reverse(
        "true_north:corevalue-email-schedule-delete", kwargs={"pk": schedule.pk}
    )
    response = client.post(url)
    assert response.status_code == 302
    assert not CoreValueEmailSchedule.objects.filter(pk=schedule.pk).exists()


@pytest.mark.django_db
def test_corevalue_email_schedule_delete_forbidden_other_user(client):
    from true_north.models import CoreValueEmailSchedule

    user = CustomUserFactory()
    other = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=other)
    schedule = CoreValueEmailScheduleFactory(user=other, core_value=cv)
    url = reverse(
        "true_north:corevalue-email-schedule-delete", kwargs={"pk": schedule.pk}
    )
    response = client.post(url)
    assert response.status_code in (403, 404)
    assert CoreValueEmailSchedule.objects.filter(pk=schedule.pk).exists()


@pytest.mark.django_db
def test_corevalue_detail_shows_schedule_button(client):
    user = CustomUserFactory()
    _login(client, user)
    _grant_schedule_permissions(user)
    cv = CoreValueFactory(user=user)
    url = reverse("true_north:core-value-detail", kwargs={"pk": cv.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert b"Set up email schedule" in response.content


@pytest.mark.django_db
def test_corevalue_email_schedule_send_now_forbidden_other_user(client):
    user = CustomUserFactory()
    other = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=other)
    schedule = CoreValueEmailScheduleFactory(user=other, core_value=cv)
    url = reverse(
        "true_north:corevalue-email-schedule-send-now", kwargs={"pk": schedule.pk}
    )
    response = client.post(url)
    assert response.status_code in (403, 404)


@pytest.mark.django_db
def test_corevalue_schedule_create_requires_permissions(client):
    user = CustomUserFactory()
    _login(client, user)
    cv = CoreValueFactory(user=user)
    url = reverse("true_north:core-value-schedule-create", kwargs={"pk": cv.pk})
    response = client.post(
        url,
        {"hour": "9", "minute": "0", "day_of_week": "*", "enabled": True},
    )
    assert response.status_code == 302
    assert response["Location"] == reverse("true_north:dashboard")
    assert not PeriodicTask.objects.filter(
        name=periodic_task_name("CoreValue", cv.pk)
    ).exists()


@pytest.mark.django_db
def test_corevalue_schedule_create_with_permissions(client):
    user = CustomUserFactory()
    _login(client, user)
    _grant_schedule_permissions(user)
    cv = CoreValueFactory(user=user)
    url = reverse("true_north:core-value-schedule-create", kwargs={"pk": cv.pk})
    response = client.post(
        url,
        {"hour": "10", "minute": "15", "day_of_week": "1", "enabled": True},
    )
    assert response.status_code == 302
    assert response["Location"] == reverse(
        "true_north:core-value-detail",
        kwargs={"pk": cv.pk},
    )

    task = PeriodicTask.objects.get(name=periodic_task_name("CoreValue", cv.pk))
    assert task.task == "true_north.tasks.send_core_value_email"
    assert json.loads(task.args) == [user.pk, cv.pk]
    assert task.crontab.hour == "10"
    assert task.crontab.minute == "15"
    assert task.crontab.day_of_week == "1"


@pytest.mark.django_db
def test_corevalue_schedule_edit_with_permissions(client):
    user = CustomUserFactory()
    _login(client, user)
    _grant_schedule_permissions(user)
    cv = CoreValueFactory(user=user)
    schedule = CrontabSchedule.objects.create(
        minute="0",
        hour="9",
        day_of_week="*",
        day_of_month="*",
        month_of_year="*",
    )
    task = PeriodicTask.objects.create(
        name=periodic_task_name("CoreValue", cv.pk),
        task="true_north.tasks.send_core_value_email",
        crontab=schedule,
        args=json.dumps([user.pk, cv.pk]),
    )
    url = reverse("true_north:core-value-schedule-edit", kwargs={"pk": cv.pk})
    response = client.post(
        url,
        {"hour": "7", "minute": "5", "day_of_week": "2", "enabled": False},
    )
    assert response.status_code == 302
    task.refresh_from_db()
    assert task.enabled is False
    assert task.crontab.hour == "7"
    assert task.crontab.minute == "5"
    assert task.crontab.day_of_week == "2"
    assert json.loads(task.args) == [user.pk, cv.pk]


@pytest.mark.django_db
def test_corevalue_schedule_delete_keeps_crontab(client):
    user = CustomUserFactory()
    _login(client, user)
    _grant_schedule_permissions(user)
    cv = CoreValueFactory(user=user)
    schedule = CrontabSchedule.objects.create(
        minute="0",
        hour="9",
        day_of_week="*",
        day_of_month="*",
        month_of_year="*",
    )
    PeriodicTask.objects.create(
        name=periodic_task_name("CoreValue", cv.pk),
        task="true_north.tasks.send_core_value_email",
        crontab=schedule,
        args=json.dumps([user.pk, cv.pk]),
    )
    url = reverse("true_north:core-value-schedule-delete", kwargs={"pk": cv.pk})
    response = client.post(url)
    assert response.status_code == 302
    assert not PeriodicTask.objects.filter(
        name=periodic_task_name("CoreValue", cv.pk)
    ).exists()
    assert CrontabSchedule.objects.filter(pk=schedule.pk).exists()


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("kind", "url_name", "model_name", "task_path"),
    [
        (
            "goal",
            "true_north:goal-schedule-create",
            "Goal",
            "true_north.tasks.send_goal_email",
        ),
        (
            "milestone",
            "true_north:milestone-schedule-create",
            "Milestone",
            "true_north.tasks.send_milestone_email",
        ),
        (
            "value_action",
            "true_north:value-action-schedule-create",
            "ValueAction",
            "true_north.tasks.send_value_action_email",
        ),
    ],
)
def test_schedule_create_for_other_models(
    client,
    kind,
    url_name,
    model_name,
    task_path,
):
    user = CustomUserFactory()
    _login(client, user)
    _grant_schedule_permissions(user)
    cv = CoreValueFactory(user=user)
    goal = GoalFactory(value=cv, user=user)
    milestone = MilestoneFactory(goal=goal, user=user)

    if kind == "goal":
        obj = goal
    elif kind == "milestone":
        obj = milestone
    else:
        obj = ValueActionFactory(milestone=milestone, user=user)

    response = client.post(
        reverse(url_name, kwargs={"pk": obj.pk}),
        {"hour": "8", "minute": "20", "day_of_week": "3", "enabled": True},
    )
    assert response.status_code == 302

    task = PeriodicTask.objects.get(name=periodic_task_name(model_name, obj.pk))
    assert task.task == task_path
    assert json.loads(task.args) == [user.pk, obj.pk]
