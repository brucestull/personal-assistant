# tests/test_views.py

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from warcrafting.models import (
    Character,
    CharacterProfession,
    Profession,
    ProfessionTier,
)


User = get_user_model()

_CLASSIC = ProfessionTier.ExpansionLabel.CLASSIC


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_user(username):
    return User.objects.create_user(username=username, password="secret")


def make_character(owner, name="Hero", level=60):
    return Character.objects.create(
        owner=owner,
        name=name,
        wow_class=Character.WowClass.WARRIOR,
        race=Character.WowRace.HUMAN,
        level=level,
    )


def make_tier(profession_name="Mining", expansion=_CLASSIC):
    prof, _ = Profession.objects.get_or_create(name=profession_name)
    tier, _ = ProfessionTier.objects.get_or_create(
        profession=prof, expansion_label=expansion
    )
    return tier


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_dashboard_redirects_when_not_logged_in(client):
    url = reverse("warcrafting:dashboard")
    response = client.get(url)
    assert response.status_code == 302
    assert "login" in response.url


@pytest.mark.django_db
def test_dashboard_renders_for_logged_in_user(client):
    user = make_user("dashuser")
    make_character(user, name="Dashchar")
    client.force_login(user)
    response = client.get(reverse("warcrafting:dashboard"))
    assert response.status_code == 200
    assert "characters" in response.context
    assert "Dashchar" in response.content.decode()


# ---------------------------------------------------------------------------
# Character List
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_character_list_redirects_when_not_logged_in(client):
    url = reverse("warcrafting:character_list")
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith("/accounts/login/") or "login" in response.url


@pytest.mark.django_db
def test_character_list_shows_only_logged_in_users_characters(client):
    user1 = make_user("user1")
    user2 = make_user("user2")

    char1 = make_character(user1, "User1Char")
    make_character(user2, "User2Char")

    client.force_login(user1)
    response = client.get(reverse("warcrafting:character_list"))

    assert response.status_code == 200
    characters = list(response.context["characters"])
    assert characters == [char1]


@pytest.mark.django_db
def test_character_list_uses_correct_template_and_context_name(client):
    user = make_user("templateguy")
    make_character(user, "TemplateChar")

    client.force_login(user)
    response = client.get(reverse("warcrafting:character_list"))

    assert response.status_code == 200
    assert "characters" in response.context
    assert "TemplateChar" in response.content.decode()


# ---------------------------------------------------------------------------
# Character Detail
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_character_detail_redirects_when_not_logged_in(client):
    user = make_user("testuser")
    char = make_character(user)
    url = reverse("warcrafting:character_detail", args=[char.pk])
    response = client.get(url)
    assert response.status_code == 302
    assert "login" in response.url


@pytest.mark.django_db
def test_character_detail_only_allows_owner(client):
    owner = make_user("owner")
    other = make_user("other")
    owned = make_character(owner, "OwnedChar")
    other_char = make_character(other, "OtherChar")

    client.force_login(owner)
    resp_owned = client.get(
        reverse("warcrafting:character_detail", args=[owned.pk])
    )
    assert resp_owned.status_code == 200
    resp_other = client.get(
        reverse("warcrafting:character_detail", args=[other_char.pk])
    )
    assert resp_other.status_code == 404


@pytest.mark.django_db
def test_character_detail_uses_correct_template_and_shows_profile_line(client):
    user = make_user("detailuser")
    char = Character.objects.create(
        owner=user,
        name="DetailChar",
        wow_class=Character.WowClass.SHAMAN,
        race=Character.WowRace.ORC,
        level=42,
    )

    client.force_login(user)
    response = client.get(reverse("warcrafting:character_detail", args=[char.pk]))

    assert response.status_code == 200
    content = response.content.decode()
    assert "DetailChar" in content
    assert char.profile_line in content


# ---------------------------------------------------------------------------
# Character Create
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_character_create_redirects_when_not_logged_in(client):
    url = reverse("warcrafting:character_create")
    assert client.get(url).status_code == 302


@pytest.mark.django_db
def test_character_create_renders_form(client):
    user = make_user("creator")
    client.force_login(user)
    response = client.get(reverse("warcrafting:character_create"))
    assert response.status_code == 200
    assert "form" in response.context


@pytest.mark.django_db
def test_character_create_post_creates_character(client):
    user = make_user("postcreator")
    client.force_login(user)
    data = {
        "name": "NewHero",
        "wow_class": Character.WowClass.MAGE,
        "race": Character.WowRace.HUMAN,
        "level": 70,
    }
    response = client.post(reverse("warcrafting:character_create"), data)
    assert response.status_code == 302
    assert Character.objects.filter(owner=user, name="NewHero").exists()


@pytest.mark.django_db
def test_character_create_sets_owner_to_logged_in_user(client):
    user = make_user("ownerset")
    client.force_login(user)
    data = {
        "name": "MyChar",
        "wow_class": Character.WowClass.DRUID,
        "race": Character.WowRace.NIGHT_ELF,
        "level": 55,
    }
    client.post(reverse("warcrafting:character_create"), data)
    char = Character.objects.get(name="MyChar")
    assert char.owner == user


# ---------------------------------------------------------------------------
# Character Update
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_character_update_renders_form(client):
    user = make_user("updater")
    char = make_character(user)
    client.force_login(user)
    response = client.get(
        reverse("warcrafting:character_update", args=[char.pk])
    )
    assert response.status_code == 200
    assert "form" in response.context


@pytest.mark.django_db
def test_character_update_saves_changes(client):
    user = make_user("updater2")
    char = make_character(user)
    client.force_login(user)
    data = {
        "name": "UpdatedName",
        "wow_class": Character.WowClass.PALADIN,
        "race": Character.WowRace.HUMAN,
        "level": 80,
    }
    response = client.post(
        reverse("warcrafting:character_update", args=[char.pk]), data
    )
    assert response.status_code == 302
    char.refresh_from_db()
    assert char.name == "UpdatedName"


@pytest.mark.django_db
def test_character_update_blocks_other_user(client):
    owner = make_user("updateowner")
    other = make_user("updateother")
    char = make_character(owner)
    client.force_login(other)
    response = client.get(
        reverse("warcrafting:character_update", args=[char.pk])
    )
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Character Delete
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_character_delete_renders_confirmation(client):
    user = make_user("deleter")
    char = make_character(user)
    client.force_login(user)
    response = client.get(
        reverse("warcrafting:character_delete", args=[char.pk])
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_character_delete_removes_character(client):
    user = make_user("deleter2")
    char = make_character(user)
    pk = char.pk
    client.force_login(user)
    response = client.post(
        reverse("warcrafting:character_delete", args=[pk])
    )
    assert response.status_code == 302
    assert not Character.objects.filter(pk=pk).exists()


@pytest.mark.django_db
def test_character_delete_blocks_other_user(client):
    owner = make_user("delowner")
    other = make_user("delother")
    char = make_character(owner)
    client.force_login(other)
    response = client.get(
        reverse("warcrafting:character_delete", args=[char.pk])
    )
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# CharacterProfession Create
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_character_profession_create_renders_form(client):
    user = make_user("profcreate")
    char = make_character(user)
    client.force_login(user)
    url = reverse("warcrafting:characterprofession_create", args=[char.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["character"] == char


@pytest.mark.django_db
def test_character_profession_create_post(client):
    user = make_user("profcreate2")
    char = make_character(user)
    tier = make_tier()
    client.force_login(user)
    url = reverse("warcrafting:characterprofession_create", args=[char.pk])
    data = {"profession_tier": tier.pk, "current_skill": 100}
    response = client.post(url, data)
    assert response.status_code == 302
    assert CharacterProfession.objects.filter(
        character=char, profession_tier=tier
    ).exists()


@pytest.mark.django_db
def test_character_profession_create_blocks_other_user(client):
    owner = make_user("profowner")
    other = make_user("profother")
    char = make_character(owner)
    client.force_login(other)
    url = reverse("warcrafting:characterprofession_create", args=[char.pk])
    assert client.get(url).status_code == 404


# ---------------------------------------------------------------------------
# CharacterProfession Update
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_character_profession_update_renders_form(client):
    user = make_user("profupdate")
    char = make_character(user)
    tier = make_tier("Herbalism", ProfessionTier.ExpansionLabel.CLASSIC)
    cp = CharacterProfession.objects.create(
        character=char, profession_tier=tier, current_skill=50
    )
    client.force_login(user)
    url = reverse("warcrafting:characterprofession_update", args=[cp.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert "form" in response.context


@pytest.mark.django_db
def test_character_profession_update_saves(client):
    user = make_user("profupdate2")
    char = make_character(user)
    tier = make_tier("Alchemy", ProfessionTier.ExpansionLabel.BFA)
    cp = CharacterProfession.objects.create(
        character=char, profession_tier=tier, current_skill=10
    )
    client.force_login(user)
    url = reverse("warcrafting:characterprofession_update", args=[cp.pk])
    data = {"profession_tier": tier.pk, "current_skill": 100}
    response = client.post(url, data)
    assert response.status_code == 302
    cp.refresh_from_db()
    assert cp.current_skill == 100


@pytest.mark.django_db
def test_character_profession_update_blocks_other_user(client):
    owner = make_user("profupdowner")
    other = make_user("profupdother")
    char = make_character(owner)
    tier = make_tier("Blacksmithing")
    cp = CharacterProfession.objects.create(
        character=char, profession_tier=tier, current_skill=50
    )
    client.force_login(other)
    response = client.get(
        reverse("warcrafting:characterprofession_update", args=[cp.pk])
    )
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# CharacterProfession Delete
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_character_profession_delete_renders_confirmation(client):
    user = make_user("profdel")
    char = make_character(user)
    tier = make_tier("Enchanting", ProfessionTier.ExpansionLabel.SHADOWLANDS)
    cp = CharacterProfession.objects.create(
        character=char, profession_tier=tier, current_skill=70
    )
    client.force_login(user)
    url = reverse("warcrafting:characterprofession_delete", args=[cp.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["character"] == char


@pytest.mark.django_db
def test_character_profession_delete_removes_record(client):
    user = make_user("profdel2")
    char = make_character(user)
    tier = make_tier("Tailoring", ProfessionTier.ExpansionLabel.DRAGONFLIGHT)
    cp = CharacterProfession.objects.create(
        character=char, profession_tier=tier, current_skill=80
    )
    pk = cp.pk
    client.force_login(user)
    response = client.post(
        reverse("warcrafting:characterprofession_delete", args=[pk])
    )
    assert response.status_code == 302
    assert not CharacterProfession.objects.filter(pk=pk).exists()


@pytest.mark.django_db
def test_character_profession_delete_blocks_other_user(client):
    owner = make_user("profdelowner")
    other = make_user("profdelother")
    char = make_character(owner)
    tier = make_tier("Skinning", ProfessionTier.ExpansionLabel.LEGION)
    cp = CharacterProfession.objects.create(
        character=char, profession_tier=tier, current_skill=60
    )
    client.force_login(other)
    response = client.get(
        reverse("warcrafting:characterprofession_delete", args=[cp.pk])
    )
    assert response.status_code == 404
