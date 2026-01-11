"""Tests for successes app models."""

import pytest
from django.contrib.auth import get_user_model

from successes.models import Success, WhatWentWell

User = get_user_model()


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
        registration_accepted=True,
    )


@pytest.fixture
def success(db, user):
    """Create a test success."""
    return Success.objects.create(
        user=user,
        text="I completed a challenging task today!",
    )


@pytest.fixture
def what_went_well(db, user):
    """Create a test What Went Well entry."""
    return WhatWentWell.objects.create(
        user=user,
        what_went_well="Had a productive meeting with the team",
        how_i_made_it_happen="I prepared an agenda and asked good questions",
    )


@pytest.mark.django_db
class TestSuccessModel:
    """Test cases for the Success model."""

    def test_success_creation(self, user):
        """Test creating a success."""
        success = Success.objects.create(
            user=user,
            text="Completed the project ahead of schedule",
        )
        assert success.user == user
        assert success.text == "Completed the project ahead of schedule"
        assert success.created is not None
        assert success.updated is not None

    def test_success_str_short_text(self, user):
        """Test __str__ method with short text."""
        success = Success.objects.create(
            user=user,
            text="Short success",
        )
        str_repr = str(success)
        assert "Short success" in str_repr
        assert "..." not in str_repr

    def test_success_str_long_text(self, user):
        """Test __str__ method with long text."""
        long_text = (
            "This is a very long success text that exceeds fifty "
            "characters and should be truncated"
        )
        success = Success.objects.create(
            user=user,
            text=long_text,
        )
        str_repr = str(success)
        assert "..." in str_repr
        assert len(str_repr.split("...")[0]) <= 50

    def test_success_ordering(self, user):
        """Test that successes are ordered by created descending."""
        success1 = Success.objects.create(user=user, text="First")
        success2 = Success.objects.create(user=user, text="Second")
        success3 = Success.objects.create(user=user, text="Third")

        successes = Success.objects.all()
        assert list(successes) == [success3, success2, success1]

    def test_success_user_relationship(self, user):
        """Test the user relationship."""
        success = Success.objects.create(user=user, text="Test success")
        assert success in user.successes.all()

    def test_success_cascade_delete(self, user):
        """Test that successes are deleted when user is deleted."""
        Success.objects.create(user=user, text="Test")
        user_id = user.id
        user.delete()
        assert Success.objects.filter(user_id=user_id).count() == 0


@pytest.mark.django_db
class TestWhatWentWellModel:
    """Test cases for the WhatWentWell model."""

    def test_what_went_well_creation(self, user):
        """Test creating a What Went Well entry."""
        www = WhatWentWell.objects.create(
            user=user,
            what_went_well="Finished coding feature",
            how_i_made_it_happen="Focused time, broke it into steps",
        )
        assert www.user == user
        assert www.what_went_well == "Finished coding feature"
        assert www.how_i_made_it_happen == "Focused time, broke it into steps"
        assert www.created is not None
        assert www.updated is not None

    def test_what_went_well_str_short_text(self, user):
        """Test __str__ method with short text."""
        www = WhatWentWell.objects.create(
            user=user,
            what_went_well="Short entry",
            how_i_made_it_happen="I did it",
        )
        str_repr = str(www)
        assert "Short entry" in str_repr
        assert "..." not in str_repr

    def test_what_went_well_str_long_text(self, user):
        """Test __str__ method with long text."""
        long_text = (
            "This is a very long what went well text that exceeds "
            "fifty characters and should be truncated"
        )
        www = WhatWentWell.objects.create(
            user=user,
            what_went_well=long_text,
            how_i_made_it_happen="I did it",
        )
        str_repr = str(www)
        assert "..." in str_repr
        assert len(str_repr.split("...")[0]) <= 50

    def test_what_went_well_ordering(self, user):
        """Test that What Went Wells are ordered by created descending."""
        www1 = WhatWentWell.objects.create(
            user=user,
            what_went_well="First",
            how_i_made_it_happen="How 1",
        )
        www2 = WhatWentWell.objects.create(
            user=user,
            what_went_well="Second",
            how_i_made_it_happen="How 2",
        )
        www3 = WhatWentWell.objects.create(
            user=user,
            what_went_well="Third",
            how_i_made_it_happen="How 3",
        )

        wwws = WhatWentWell.objects.all()
        assert list(wwws) == [www3, www2, www1]

    def test_what_went_well_user_relationship(self, user):
        """Test the user relationship."""
        www = WhatWentWell.objects.create(
            user=user,
            what_went_well="Test",
            how_i_made_it_happen="Did it",
        )
        assert www in user.what_went_wells.all()

    def test_what_went_well_cascade_delete(self, user):
        """Test that What Went Wells are deleted when user is deleted."""
        WhatWentWell.objects.create(
            user=user,
            what_went_well="Test",
            how_i_made_it_happen="Did it",
        )
        user_id = user.id
        user.delete()
        assert WhatWentWell.objects.filter(user_id=user_id).count() == 0

    def test_verbose_names(self):
        """Test model verbose names."""
        assert WhatWentWell._meta.verbose_name == "What Went Well"
        assert WhatWentWell._meta.verbose_name_plural == "What Went Wells"
