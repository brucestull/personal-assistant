# conftest.py

import pytest
from django.contrib.auth import get_user_model

from core.models import Workspace
from plan_it.tests.factories import UserFactory


@pytest.fixture
def workspace(db):
    return Workspace.objects.create(name="Main Workspace", slug="main-workspace")


@pytest.fixture
def another_workspace(db):
    return Workspace.objects.create(name="Other Workspace", slug="other-workspace")


# Keep your existing "user" fixtures, but make them registration-accepted
# so they work with RegistrationAcceptedMixin-protected views.
@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="user1",
        email="user1@example.com",
        password="testpass123",
        registration_accepted=True,
    )


@pytest.fixture
def another_user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="user2",
        email="user2@example.com",
        password="testpass123",
        registration_accepted=True,
    )


# New fixtures (factory-based) for clarity in permission tests
@pytest.fixture
def accepted_user(db):
    return UserFactory(registration_accepted=True)


@pytest.fixture
def rejected_user(db):
    return UserFactory(registration_accepted=False)
