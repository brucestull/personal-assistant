"""Project-level pytest fixtures.

Why imports are inside fixtures:
Pytest imports conftest.py during collection. Importing Django models or factories
at module import time can run before pytest-django initializes Django, causing
AppRegistryNotReady/settings errors.
"""

import pytest


@pytest.fixture
def user(db):
    """A default *accepted* user for permission/auth tests."""
    from django.contrib.auth import get_user_model

    User = get_user_model()
    return User.objects.create_user(
        username="user1",
        email="user1@example.com",
        password="testpass123",
        registration_accepted=True,
    )


@pytest.fixture
def another_user(db):
    """A second accepted user."""
    from django.contrib.auth import get_user_model

    User = get_user_model()
    return User.objects.create_user(
        username="user2",
        email="user2@example.com",
        password="testpass123",
        registration_accepted=True,
    )


@pytest.fixture
def accepted_user(db):
    """FactoryBoy user with registration accepted."""
    from true_north.tests.factories import CustomUserFactory

    return CustomUserFactory(registration_accepted=True)


@pytest.fixture
def rejected_user(db):
    """FactoryBoy user with registration NOT accepted."""
    from true_north.tests.factories import CustomUserFactory

    return CustomUserFactory(registration_accepted=False)
