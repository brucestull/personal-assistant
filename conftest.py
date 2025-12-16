# conftest.py

import pytest
from django.contrib.auth import get_user_model

from core.models import Workspace


@pytest.fixture
def workspace(db):
    return Workspace.objects.create(name="Main Workspace", slug="main-workspace")


@pytest.fixture
def another_workspace(db):
    return Workspace.objects.create(name="Other Workspace", slug="other-workspace")


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="user1",
        email="user1@example.com",
        password="testpass123",
    )


@pytest.fixture
def another_user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="user2",
        email="user2@example.com",
        password="testpass123",
    )
