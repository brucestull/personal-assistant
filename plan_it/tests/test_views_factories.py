# plan_it/tests/test_views_factories.py

import pytest
from django.urls import reverse
from datetime import timedelta, date

from plan_it.models import Activity
from plan_it.tests.factories import (
    UserFactory,
    StorageLocationFactory,
    ActivityLocationFactory,
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
    storage_location = StorageLocationFactory(user=user)
    activity_location = ActivityLocationFactory(user=user)
    item = ItemFactory(user=user, storage_location=storage_location)
    activity_type = ActivityTypeFactory(user=user)

    # Activities
    overdue = ActivityFactory(
        user=user,
        type=activity_type,
        activity_location=activity_location,
        due_date=date.today() - timedelta(days=2),
    )
    today = ActivityFactory(
        user=user,
        type=activity_type,
        activity_location=activity_location,
        due_date=date.today(),
    )
    upcoming = ActivityFactory(
        user=user,
        type=activity_type,
        activity_location=activity_location,
        due_date=date.today() + timedelta(days=2),
    )

    return {
        "storage_location": storage_location,
        "activity_location": activity_location,
        "item": item,
        "activity_type": activity_type,
        "overdue": overdue,
        "today": today,
        "upcoming": upcoming,
    }


def test_dashboard(client_logged_in, setup_data):
    response = client_logged_in.get(reverse("plan_it:dashboard"))
    content = response.content.decode()

    assert response.status_code == 200
    assert setup_data["overdue"].name in content
    assert setup_data["today"].name in content
    assert setup_data["upcoming"].name in content


def test_activity_create(client_logged_in, setup_data):
    activity_type = setup_data["activity_type"]
    activity_location = setup_data["activity_location"]

    response = client_logged_in.post(
        reverse("plan_it:activity_add"),
        {
            "name": "Factory Created Task",
            "type": activity_type.id,
            "activity_location": activity_location.id,
            "due_date": date.today(),
        },
    )
    assert response.status_code == 302
    assert Activity.objects.filter(name="Factory Created Task").exists()


def test_dashboard_locations_displayed(client_logged_in, setup_data):
    response = client_logged_in.get(reverse("plan_it:dashboard"))
    content = response.content.decode()

    # Check that the activity location appears on the page
    activity_location_name = setup_data["activity_location"].name
    assert activity_location_name in content
