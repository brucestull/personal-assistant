"""Tests for successes app views."""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

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
def other_user(db):
    """Create another test user."""
    return User.objects.create_user(
        username="otheruser",
        email="other@example.com",
        password="testpass123",
        registration_accepted=True,
    )


@pytest.fixture
def client_logged_in(client, user):
    """Return a logged-in client."""
    client.login(username="testuser", password="testpass123")
    return client


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
class TestDashboardView:
    """Test cases for the dashboard view."""

    def test_dashboard_requires_login(self, client):
        """Test that dashboard requires login."""
        response = client.get(reverse("successes:dashboard"))
        assert response.status_code == 403

    def test_dashboard_requires_registration_accepted(self, client, db):
        """Test that dashboard requires registration_accepted."""
        User.objects.create_user(
            username="unaccepted",
            password="testpass123",
            registration_accepted=False,
        )
        client.login(username="unaccepted", password="testpass123")
        response = client.get(reverse("successes:dashboard"))
        assert response.status_code == 403

    def test_dashboard_success(self, client_logged_in):
        """Test that dashboard loads successfully."""
        response = client_logged_in.get(reverse("successes:dashboard"))
        assert response.status_code == 200
        assert "Daily Successes Dashboard" in response.content.decode()

    def test_dashboard_shows_statistics(self, client_logged_in, user):
        """Test that dashboard shows correct statistics."""
        # Create test data
        Success.objects.create(user=user, text="Success 1")
        Success.objects.create(user=user, text="Success 2")
        WhatWentWell.objects.create(
            user=user,
            what_went_well="WWW 1",
            how_i_made_it_happen="How 1",
        )

        response = client_logged_in.get(reverse("successes:dashboard"))
        content = response.content.decode()

        assert "2" in content  # Total successes
        assert "1" in content  # Total WWWs

    def test_dashboard_daily_goal_progress(self, client_logged_in, user):
        """Test dashboard shows daily goal progress."""
        # Create 3 What Went Wells for today
        for i in range(3):
            WhatWentWell.objects.create(
                user=user,
                what_went_well=f"WWW {i}",
                how_i_made_it_happen=f"How {i}",
            )

        response = client_logged_in.get(reverse("successes:dashboard"))
        content = response.content.decode()

        assert "Congratulations" in content
        assert "completed your daily reflection" in content


@pytest.mark.django_db
class TestSuccessViews:
    """Test cases for Success CRUD views."""

    def test_success_list_requires_login(self, client):
        """Test that success list requires login."""
        response = client.get(reverse("successes:success_list"))
        # RegistrationAcceptedMixin redirects to login page
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_success_list_success(self, client_logged_in, success):
        """Test success list view."""
        response = client_logged_in.get(reverse("successes:success_list"))
        assert response.status_code == 200
        assert success.text in response.content.decode()

    def test_success_list_only_shows_user_successes(
        self, client_logged_in, user, other_user
    ):
        """Test that users only see their own successes."""
        user_success = Success.objects.create(user=user, text="My success")
        other_success = Success.objects.create(user=other_user, text="Other success")

        response = client_logged_in.get(reverse("successes:success_list"))
        content = response.content.decode()

        assert user_success.text in content
        assert other_success.text not in content

    def test_success_detail(self, client_logged_in, success):
        """Test success detail view."""
        response = client_logged_in.get(
            reverse("successes:success_detail", args=[success.pk])
        )
        assert response.status_code == 200
        assert success.text in response.content.decode()

    def test_success_create_get(self, client_logged_in):
        """Test success create GET request."""
        response = client_logged_in.get(reverse("successes:success_create"))
        assert response.status_code == 200
        assert "Add Success" in response.content.decode()

    def test_success_create_post(self, client_logged_in, user):
        """Test success create POST request."""
        data = {"text": "New success!"}
        response = client_logged_in.post(reverse("successes:success_create"), data)

        assert response.status_code == 302  # Redirect after success
        assert Success.objects.filter(user=user, text="New success!").exists()

    def test_success_update_get(self, client_logged_in, success):
        """Test success update GET request."""
        response = client_logged_in.get(
            reverse("successes:success_update", args=[success.pk])
        )
        assert response.status_code == 200
        assert success.text in response.content.decode()

    def test_success_update_post(self, client_logged_in, success):
        """Test success update POST request."""
        data = {"text": "Updated success!"}
        response = client_logged_in.post(
            reverse("successes:success_update", args=[success.pk]), data
        )

        assert response.status_code == 302
        success.refresh_from_db()
        assert success.text == "Updated success!"

    def test_success_delete_get(self, client_logged_in, success):
        """Test success delete GET request."""
        response = client_logged_in.get(
            reverse("successes:success_delete", args=[success.pk])
        )
        assert response.status_code == 200
        assert "Are you sure" in response.content.decode()

    def test_success_delete_post(self, client_logged_in, success):
        """Test success delete POST request."""
        success_pk = success.pk
        response = client_logged_in.post(
            reverse("successes:success_delete", args=[success.pk])
        )

        assert response.status_code == 302
        assert not Success.objects.filter(pk=success_pk).exists()

    def test_cannot_access_other_user_success(self, client_logged_in, other_user):
        """Test that users cannot access other users' successes."""
        other_success = Success.objects.create(user=other_user, text="Other's success")

        # Try to view
        response = client_logged_in.get(
            reverse("successes:success_detail", args=[other_success.pk])
        )
        assert response.status_code == 404


@pytest.mark.django_db
class TestWhatWentWellViews:
    """Test cases for WhatWentWell CRUD views."""

    def test_whatwentwell_list_requires_login(self, client):
        """Test that What Went Well list requires login."""
        response = client.get(reverse("successes:whatwentwell_list"))
        # RegistrationAcceptedMixin redirects to login page
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_whatwentwell_list_success(self, client_logged_in, what_went_well):
        """Test What Went Well list view."""
        response = client_logged_in.get(reverse("successes:whatwentwell_list"))
        assert response.status_code == 200
        assert what_went_well.what_went_well in response.content.decode()

    def test_whatwentwell_list_only_shows_user_entries(
        self, client_logged_in, user, other_user
    ):
        """Test that users only see their own What Went Well entries."""
        user_www = WhatWentWell.objects.create(
            user=user,
            what_went_well="My entry",
            how_i_made_it_happen="I did it",
        )
        other_www = WhatWentWell.objects.create(
            user=other_user,
            what_went_well="Other entry",
            how_i_made_it_happen="They did it",
        )

        response = client_logged_in.get(reverse("successes:whatwentwell_list"))
        content = response.content.decode()

        assert user_www.what_went_well in content
        assert other_www.what_went_well not in content

    def test_whatwentwell_detail(self, client_logged_in, what_went_well):
        """Test What Went Well detail view."""
        response = client_logged_in.get(
            reverse("successes:whatwentwell_detail", args=[what_went_well.pk])
        )
        assert response.status_code == 200
        assert what_went_well.what_went_well in response.content.decode()
        assert what_went_well.how_i_made_it_happen in response.content.decode()

    def test_whatwentwell_create_get(self, client_logged_in):
        """Test What Went Well create GET request."""
        response = client_logged_in.get(reverse("successes:whatwentwell_create"))
        assert response.status_code == 200
        assert "Add What Went Well" in response.content.decode()

    def test_whatwentwell_create_post(self, client_logged_in, user):
        """Test What Went Well create POST request."""
        data = {
            "what_went_well": "Got exercise today",
            "how_i_made_it_happen": "Set my alarm early and went for a run",
        }
        response = client_logged_in.post(reverse("successes:whatwentwell_create"), data)

        assert response.status_code == 302
        assert WhatWentWell.objects.filter(
            user=user, what_went_well="Got exercise today"
        ).exists()

    def test_whatwentwell_update_get(self, client_logged_in, what_went_well):
        """Test What Went Well update GET request."""
        response = client_logged_in.get(
            reverse("successes:whatwentwell_update", args=[what_went_well.pk])
        )
        assert response.status_code == 200
        assert what_went_well.what_went_well in response.content.decode()

    def test_whatwentwell_update_post(self, client_logged_in, what_went_well):
        """Test What Went Well update POST request."""
        data = {
            "what_went_well": "Updated entry",
            "how_i_made_it_happen": "Updated how",
        }
        response = client_logged_in.post(
            reverse("successes:whatwentwell_update", args=[what_went_well.pk]), data
        )

        assert response.status_code == 302
        what_went_well.refresh_from_db()
        assert what_went_well.what_went_well == "Updated entry"
        assert what_went_well.how_i_made_it_happen == "Updated how"

    def test_whatwentwell_delete_get(self, client_logged_in, what_went_well):
        """Test What Went Well delete GET request."""
        response = client_logged_in.get(
            reverse("successes:whatwentwell_delete", args=[what_went_well.pk])
        )
        assert response.status_code == 200
        assert "Are you sure" in response.content.decode()

    def test_whatwentwell_delete_post(self, client_logged_in, what_went_well):
        """Test What Went Well delete POST request."""
        www_pk = what_went_well.pk
        response = client_logged_in.post(
            reverse("successes:whatwentwell_delete", args=[what_went_well.pk])
        )

        assert response.status_code == 302
        assert not WhatWentWell.objects.filter(pk=www_pk).exists()

    def test_cannot_access_other_user_whatwentwell(self, client_logged_in, other_user):
        """Test that users cannot access other users' What Went Well entries."""
        other_www = WhatWentWell.objects.create(
            user=other_user,
            what_went_well="Other's entry",
            how_i_made_it_happen="They did it",
        )

        # Try to view
        response = client_logged_in.get(
            reverse("successes:whatwentwell_detail", args=[other_www.pk])
        )
        assert response.status_code == 404
