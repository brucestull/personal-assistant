# tests/test_views.py

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from warcrafting.models import Character


User = get_user_model()


@pytest.mark.django_db
def test_character_list_redirects_when_not_logged_in(client):
    url = reverse("warcrafting:character_list")
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith("/accounts/login/") or "login" in response.url


@pytest.mark.django_db
def test_character_detail_redirects_when_not_logged_in(client):
    user = User.objects.create_user(username="testuser", password="secret")
    char = Character.objects.create(
        owner=user,
        name="TestChar",
        wow_class=Character.WowClass.WARRIOR,
        race=Character.WowRace.HUMAN,
        level=10,
    )
    url = reverse("warcrafting:character_detail", args=[char.pk])
    response = client.get(url)
    assert response.status_code == 302
    assert "login" in response.url


@pytest.mark.django_db
def test_character_list_shows_only_logged_in_users_characters(client):
    user1 = User.objects.create_user(username="user1", password="secret")
    user2 = User.objects.create_user(username="user2", password="secret")

    char1 = Character.objects.create(
        owner=user1,
        name="User1Char",
        wow_class=Character.WowClass.MAGE,
        race=Character.WowRace.HUMAN,
        level=60,
    )
    Character.objects.create(
        owner=user2,
        name="User2Char",
        wow_class=Character.WowClass.ROGUE,
        race=Character.WowRace.ORC,
        level=60,
    )

    client.force_login(user1)
    url = reverse("warcrafting:character_list")
    response = client.get(url)

    assert response.status_code == 200
    assert "characters" in response.context

    characters = list(response.context["characters"])
    assert characters == [char1]  # only user1's character


@pytest.mark.django_db
def test_character_detail_only_allows_owner(client):
    owner = User.objects.create_user(username="owner", password="secret")
    other_user = User.objects.create_user(username="other", password="secret")

    owned_char = Character.objects.create(
        owner=owner,
        name="OwnedChar",
        wow_class=Character.WowClass.DRUID,
        race=Character.WowRace.NIGHT_ELF,
        level=70,
    )

    other_char = Character.objects.create(
        owner=other_user,
        name="OtherChar",
        wow_class=Character.WowClass.HUNTER,
        race=Character.WowRace.ORC,
        level=50,
    )

    # Owner can see their character
    client.force_login(owner)
    url_owned = reverse("warcrafting:character_detail", args=[owned_char.pk])
    resp_owned = client.get(url_owned)
    assert resp_owned.status_code == 200
    assert resp_owned.context["character"] == owned_char

    # Owner should NOT see other's character (404)
    url_other = reverse("warcrafting:character_detail", args=[other_char.pk])
    resp_other = client.get(url_other)
    assert resp_other.status_code == 404


@pytest.mark.django_db
def test_character_list_uses_correct_template_and_context_name(client):
    user = User.objects.create_user(username="templateguy", password="secret")
    Character.objects.create(
        owner=user,
        name="TemplateChar",
        wow_class=Character.WowClass.MONK,
        race=Character.WowRace.PANDAREN,
        level=30,
    )

    client.force_login(user)
    url = reverse("warcrafting:character_list")
    response = client.get(url)

    assert response.status_code == 200
    assert "characters" in response.context
    assert "TemplateChar" in response.content.decode()


@pytest.mark.django_db
def test_character_detail_uses_correct_template_and_shows_profile_line(client):
    user = User.objects.create_user(username="detailuser", password="secret")
    char = Character.objects.create(
        owner=user,
        name="DetailChar",
        wow_class=Character.WowClass.SHAMAN,
        race=Character.WowRace.ORC,
        level=42,
    )

    client.force_login(user)
    url = reverse("warcrafting:character_detail", args=[char.pk])
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode()
    assert "DetailChar" in content
    assert char.profile_line in content
