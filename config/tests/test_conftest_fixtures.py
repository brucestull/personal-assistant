import pytest


@pytest.mark.django_db
def test_basic_user_fixtures(user, another_user):
    assert user.registration_accepted is True
    assert another_user.registration_accepted is True
    assert user.username != another_user.username


@pytest.mark.django_db
def test_factory_user_fixtures(accepted_user, rejected_user):
    assert accepted_user.registration_accepted is True
    assert rejected_user.registration_accepted is False
