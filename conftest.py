# conftest.py

import pytest
from django.contrib.auth import get_user_model

from plan_it.tests.factories import UserFactory


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
