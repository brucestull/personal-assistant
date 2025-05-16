import pytest
from datetime import date, timedelta
from django.urls import reverse

from plan_it.models import StorageLocation, Item, ActivityType, Activity


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="testuser", password="testpass"
    )


@pytest.fixture
def client_logged_in(client, user):
    client.login(username="testuser", password="testpass")
    return client


@pytest.fixture
def setup_data(user):
    location = StorageLocation.objects.create(user=user, name="Garage")
    item = Item.objects.create(user=user, name="Socket Set", storage_location=location)
    activity_type = ActivityType.objects.create(user=user, name="Cleaning")
    Activity.objects.create(
        user=user,
        name="Overdue Task",
        type=activity_type,
        due_date=date.today() - timedelta(days=2),
    )
    Activity.objects.create(
        user=user, name="Today's Task", type=activity_type, due_date=date.today()
    )
    Activity.objects.create(
        user=user,
        name="Future Task",
        type=activity_type,
        due_date=date.today() + timedelta(days=2),
    )
    return location, item, activity_type


def test_dashboard(client_logged_in, setup_data):
    response = client_logged_in.get(reverse("plan_it:dashboard"))
    assert response.status_code == 200
    assert "Overdue Task" in response.content.decode()
    assert "Today's Task" in response.content.decode()
    assert "Future Task" in response.content.decode()
    assert "Socket Set" in response.content.decode()


def test_storage_location_crud(client_logged_in, user, setup_data):
    location = setup_data[0]
    # Create
    response = client_logged_in.post(
        reverse("plan_it:storage_location_add"), {"name": "Attic"}
    )
    assert response.status_code == 302
    assert StorageLocation.objects.filter(name="Attic", user=user).exists()

    # List
    response = client_logged_in.get(reverse("plan_it:storage_location_list"))
    assert response.status_code == 200
    assert "Garage" in response.content.decode()

    # Update
    response = client_logged_in.post(
        reverse("plan_it:storage_location_edit", args=[location.id]),
        {"name": "Updated Garage"},
    )
    assert response.status_code == 302
    location.refresh_from_db()
    assert location.name == "Updated Garage"

    # Delete
    response = client_logged_in.post(
        reverse("plan_it:storage_location_delete", args=[location.id])
    )
    assert response.status_code == 302
    assert not StorageLocation.objects.filter(id=location.id).exists()


def test_item_crud(client_logged_in, user, setup_data):
    location = setup_data[0]
    response = client_logged_in.post(
        reverse("plan_it:item_add"),
        {"name": "New Item", "storage_location": location.id},
    )
    assert response.status_code == 302
    assert Item.objects.filter(name="New Item", user=user).exists()


def test_activity_type_crud(client_logged_in, user):
    response = client_logged_in.post(
        reverse("plan_it:activity_type_add"), {"name": "Maintenance"}
    )
    assert response.status_code == 302
    assert ActivityType.objects.filter(name="Maintenance", user=user).exists()


def test_activity_crud(client_logged_in, user, setup_data):
    activity_type = setup_data[2]
    response = client_logged_in.post(
        reverse("plan_it:activity_add"),
        {
            "name": "Test Task",
            "type": activity_type.id,
            "due_date": date.today(),
        },
    )
    assert response.status_code == 302
    assert Activity.objects.filter(name="Test Task", user=user).exists()
