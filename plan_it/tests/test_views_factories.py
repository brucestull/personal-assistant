# plan_it/tests/test_views_factories.py

import pytest
from datetime import timedelta, date
from django.urls import reverse

from plan_it.models import Activity
from plan_it.tests.factories import (
    StorageLocationFactory,
    ActivityLocationFactory,
    ItemFactory,
    ActivityTypeFactory,
    ActivityFactory,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def client_logged_in(client, accepted_user):
    client.force_login(accepted_user)
    return client


@pytest.fixture
def setup_data(accepted_user):
    storage_location = StorageLocationFactory(user=accepted_user)
    activity_location = ActivityLocationFactory(user=accepted_user)
    item = ItemFactory(user=accepted_user, storage_location=storage_location)
    activity_type = ActivityTypeFactory(user=accepted_user)

    overdue = ActivityFactory(
        user=accepted_user,
        type=activity_type,
        target_item=item,
        activity_location=activity_location,
        due_date=date.today() - timedelta(days=2),
    )
    today = ActivityFactory(
        user=accepted_user,
        type=activity_type,
        target_item=item,
        activity_location=activity_location,
        due_date=date.today(),
    )
    upcoming = ActivityFactory(
        user=accepted_user,
        type=activity_type,
        target_item=item,
        activity_location=activity_location,
        due_date=date.today() + timedelta(days=2),
    )

    return {
        "user": accepted_user,
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
    user = setup_data["user"]

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
    assert Activity.objects.filter(user=user, name="Factory Created Task").exists()


def test_dashboard_locations_displayed(client_logged_in, setup_data):
    response = client_logged_in.get(reverse("plan_it:dashboard"))
    content = response.content.decode()

    assert setup_data["activity_location"].name in content
