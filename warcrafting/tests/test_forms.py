# tests/test_forms.py

import pytest
from django.contrib.auth import get_user_model

from warcrafting.forms import CharacterForm, CharacterProfessionForm
from warcrafting.models import Character, Profession, ProfessionTier

User = get_user_model()


# ---------------------------------------------------------------------------
# CharacterForm
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_character_form_valid():
    data = {
        "name": "TestHero",
        "wow_class": Character.WowClass.MAGE,
        "race": Character.WowRace.HUMAN,
        "level": 70,
    }
    form = CharacterForm(data=data)
    assert form.is_valid()


@pytest.mark.django_db
def test_character_form_invalid_missing_name():
    data = {
        "wow_class": Character.WowClass.MAGE,
        "race": Character.WowRace.HUMAN,
        "level": 70,
    }
    form = CharacterForm(data=data)
    assert not form.is_valid()
    assert "name" in form.errors


# ---------------------------------------------------------------------------
# CharacterProfessionForm
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_character_profession_form_valid():
    prof = Profession.objects.create(name="Mining")
    tier = ProfessionTier.objects.create(
        profession=prof,
        expansion_label=ProfessionTier.ExpansionLabel.CLASSIC,
        max_skill=300,
    )
    data = {"profession_tier": tier.pk, "current_skill": 200}
    form = CharacterProfessionForm(data=data)
    assert form.is_valid()


@pytest.mark.django_db
def test_character_profession_form_skill_exceeds_max():
    prof = Profession.objects.create(name="Herbalism")
    tier = ProfessionTier.objects.create(
        profession=prof,
        expansion_label=ProfessionTier.ExpansionLabel.CLASSIC,
        max_skill=300,
    )
    data = {"profession_tier": tier.pk, "current_skill": 999}
    form = CharacterProfessionForm(data=data)
    assert not form.is_valid()
    assert "current_skill" in form.errors


@pytest.mark.django_db
def test_character_profession_form_invalid_missing_tier():
    data = {"current_skill": 50}
    form = CharacterProfessionForm(data=data)
    assert not form.is_valid()
    assert "profession_tier" in form.errors


@pytest.mark.django_db
def test_character_profession_form_no_max_skill_allows_any_value():
    """Tiers without max_skill should not block any skill value."""
    prof = Profession.objects.create(name="Fishing")
    tier = ProfessionTier.objects.create(
        profession=prof, expansion_label="Custom", max_skill=None
    )
    data = {"profession_tier": tier.pk, "current_skill": 9999}
    form = CharacterProfessionForm(data=data)
    assert form.is_valid()
