# true_north/tests/test_views.py

import pytest
from django.urls import reverse

from true_north.tests.factories import (
    CoreValueFactory,
    CustomUserFactory,
    GoalFactory,
    MilestoneFactory,
    ValueActionFactory,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _login(client, user, password="password123"):
    user.registration_accepted = True
    user.save()
    client.login(username=user.username, password=password)
    return user


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
