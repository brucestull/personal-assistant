# thoughts/tests/test_views.py

import pytest
from django.urls import reverse

from thoughts.models import Thought
from thoughts.tests.factories import CustomUserFactory, ThoughtFactory

pytestmark = pytest.mark.django_db


def _login(client, user, password="password123"):
    client.login(username=user.username, password=password)
    return user


# --- Dashboard ---

def test_dashboard_requires_login(client):
    url = reverse("thoughts:dashboard")
    response = client.get(url)
    assert response.status_code in (302, 403)


def test_dashboard_accessible_to_authenticated_user(client):
    user = CustomUserFactory()
    _login(client, user)
    url = reverse("thoughts:dashboard")
    response = client.get(url)
    assert response.status_code == 200


def test_dashboard_shows_thought_count(client):
    user = CustomUserFactory()
    _login(client, user)
    ThoughtFactory(user=user)
    ThoughtFactory(user=user)
    url = reverse("thoughts:dashboard")
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["total_thoughts"] == 2


# --- List ---

def test_thought_list_requires_login(client):
    url = reverse("thoughts:thought-list")
    response = client.get(url)
    assert response.status_code in (302, 403)


def test_thought_list_shows_user_thoughts(client):
    user = CustomUserFactory()
    other = CustomUserFactory()
    _login(client, user)
    my_thought = ThoughtFactory(user=user)
    ThoughtFactory(user=other)  # should not appear
    url = reverse("thoughts:thought-list")
    response = client.get(url)
    assert response.status_code == 200
    assert my_thought.text.encode() in response.content


def test_thought_list_does_not_show_other_user_thoughts(client):
    user = CustomUserFactory()
    other = CustomUserFactory()
    _login(client, user)
    other_thought = ThoughtFactory(user=other, text="Other person's private thought")
    url = reverse("thoughts:thought-list")
    response = client.get(url)
    assert other_thought.text.encode() not in response.content


# --- Create ---

def test_thought_create_requires_login(client):
    url = reverse("thoughts:thought-create")
    response = client.get(url)
    assert response.status_code in (302, 403)


def test_thought_create_post(client):
    user = CustomUserFactory()
    _login(client, user)
    url = reverse("thoughts:thought-create")
    response = client.post(url, {"text": "A brand new thought"})
    assert response.status_code == 302
    assert Thought.objects.filter(user=user, text="A brand new thought").exists()


# --- Update ---

def test_thought_update_requires_login(client):
    thought = ThoughtFactory()
    url = reverse("thoughts:thought-update", kwargs={"pk": thought.pk})
    response = client.get(url)
    assert response.status_code in (302, 403)


def test_thought_update_by_owner(client):
    user = CustomUserFactory()
    _login(client, user)
    thought = ThoughtFactory(user=user, text="Original text")
    url = reverse("thoughts:thought-update", kwargs={"pk": thought.pk})
    response = client.post(url, {"text": "Updated text"})
    assert response.status_code == 302
    thought.refresh_from_db()
    assert thought.text == "Updated text"


def test_thought_update_denied_for_non_owner(client):
    user = CustomUserFactory()
    other = CustomUserFactory()
    _login(client, user)
    thought = ThoughtFactory(user=other, text="Other's thought")
    url = reverse("thoughts:thought-update", kwargs={"pk": thought.pk})
    response = client.post(url, {"text": "Hacked"})
    assert response.status_code == 403


# --- Delete ---

def test_thought_delete_requires_login(client):
    thought = ThoughtFactory()
    url = reverse("thoughts:thought-delete", kwargs={"pk": thought.pk})
    response = client.get(url)
    assert response.status_code in (302, 403)


def test_thought_delete_by_owner(client):
    user = CustomUserFactory()
    _login(client, user)
    thought = ThoughtFactory(user=user)
    url = reverse("thoughts:thought-delete", kwargs={"pk": thought.pk})
    response = client.post(url)
    assert response.status_code == 302
    assert not Thought.objects.filter(pk=thought.pk).exists()


def test_thought_delete_denied_for_non_owner(client):
    user = CustomUserFactory()
    other = CustomUserFactory()
    _login(client, user)
    thought = ThoughtFactory(user=other)
    url = reverse("thoughts:thought-delete", kwargs={"pk": thought.pk})
    response = client.post(url)
    assert response.status_code == 403
    assert Thought.objects.filter(pk=thought.pk).exists()
