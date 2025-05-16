import pytest
from django.urls import reverse
from datetime import timedelta, date

from plan_it.models import Activity
from plan_it.tests.factories import (
    UserFactory,
    StorageLocationFactory,
    ItemFactory,
    ActivityTypeFactory,
    ActivityFactory,
)


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def client_logged_in(client, user):
    client.login(username=user.username, password="testpass")
    return client


@pytest.fixture
def setup_data(user):
    location = StorageLocationFactory(user=user)
    item = ItemFactory(user=user, storage_location=location)
    activity_type = ActivityTypeFactory(user=user)

    overdue = ActivityFactory(
        user=user,
        type=activity_type,
        name="Overdue Task",
        due_date=date.today() - timedelta(days=2),
    )
    today = ActivityFactory(
        user=user, type=activity_type, name="Today's Task", due_date=date.today()
    )
    upcoming = ActivityFactory(
        user=user,
        type=activity_type,
        name="Future Task",
        due_date=date.today() + timedelta(days=2),
    )

    return location, item, activity_type, overdue, today, upcoming


def test_dashboard(client_logged_in, setup_data):
    response = client_logged_in.get(reverse("plan_it:dashboard"))
    assert response.status_code == 200
    assert "Overdue Task" in response.content.decode()
    assert "Today's Task" in response.content.decode()
    assert "Future Task" in response.content.decode()


def test_activity_create(client_logged_in, setup_data):
    activity_type = setup_data[2]
    response = client_logged_in.post(
        reverse("plan_it:activity_add"),
        {
            "name": "Factory Created Task",
            "type": activity_type.id,
            "due_date": date.today(),
        },
    )
    assert response.status_code == 302
    assert Activity.objects.filter(name="Factory Created Task").exists()
