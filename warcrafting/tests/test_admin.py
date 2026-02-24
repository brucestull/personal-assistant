# tests/test_admin.py

import pytest
from django.contrib import admin
from django.contrib.auth import get_user_model

from warcrafting.admin import (
    AssetAdmin,
    CharacterAdmin,
    CharacterProfessionAdmin,
    ProfessionAdmin,
    ProfessionTierAdmin,
)
from warcrafting.models import (
    Asset,
    Character,
    CharacterProfession,
    Profession,
    ProfessionTier,
)


User = get_user_model()


@pytest.mark.django_db
def test_profession_admin_registered():
    assert Profession in admin.site._registry
    assert isinstance(admin.site._registry[Profession], ProfessionAdmin)


@pytest.mark.django_db
def test_profession_admin_tier_count_and_tier_names_short_empty():
    prof = Profession.objects.create(name="Mining")
    model_admin = ProfessionAdmin(Profession, admin.site)

    assert model_admin.tier_count(prof) == 0
    assert model_admin.tier_names_short(prof) == "—"


@pytest.mark.django_db
def test_profession_admin_tier_names_short_with_few_tiers():
    prof = Profession.objects.create(name="Herbalism")
    ProfessionTier.objects.create(
        profession=prof,
        expansion_label=ProfessionTier.ExpansionLabel.CLASSIC,
    )
    ProfessionTier.objects.create(
        profession=prof,
        expansion_label=ProfessionTier.ExpansionLabel.CATACLYSM,
    )

    model_admin = ProfessionAdmin(Profession, admin.site)
    short = model_admin.tier_names_short(prof)

    assert "Classic" in short
    assert "Cataclysm" in short
    assert "(+1 more)" not in short


@pytest.mark.django_db
def test_profession_admin_tier_names_short_with_many_tiers():
    prof = Profession.objects.create(name="Alchemy")
    for label in [
        ProfessionTier.ExpansionLabel.CLASSIC,
        ProfessionTier.ExpansionLabel.BURNING_CRUSADE,
        ProfessionTier.ExpansionLabel.WRATH,
        ProfessionTier.ExpansionLabel.CATACLYSM,
    ]:
        ProfessionTier.objects.create(profession=prof, expansion_label=label)

    model_admin = ProfessionAdmin(Profession, admin.site)
    short = model_admin.tier_names_short(prof)

    assert "Classic" in short
    assert "(+1 more)" in short


@pytest.mark.django_db
def test_profession_tier_admin_registered():
    assert ProfessionTier in admin.site._registry
    assert isinstance(admin.site._registry[ProfessionTier], ProfessionTierAdmin)


@pytest.mark.django_db
def test_character_profession_admin_registered():
    assert CharacterProfession in admin.site._registry
    assert isinstance(
        admin.site._registry[CharacterProfession], CharacterProfessionAdmin
    )


@pytest.mark.django_db
def test_character_profession_admin_skill_percentage():
    user = User.objects.create_user(username="cpct", password="secret")
    char = Character.objects.create(
        owner=user,
        name="CPAdmin",
        wow_class=Character.WowClass.ROGUE,
        race=Character.WowRace.HUMAN,
        level=70,
    )
    prof = Profession.objects.create(name="Skinning")
    tier = ProfessionTier.objects.create(
        profession=prof,
        expansion_label=ProfessionTier.ExpansionLabel.CLASSIC,
        max_skill=300,
    )
    cp = CharacterProfession.objects.create(
        character=char, profession_tier=tier, current_skill=150
    )

    model_admin = CharacterProfessionAdmin(CharacterProfession, admin.site)
    assert model_admin.skill_percentage(cp) == "50.0%"


@pytest.mark.django_db
def test_character_profession_admin_skill_percentage_no_max():
    user = User.objects.create_user(username="cpnomax", password="secret")
    char = Character.objects.create(
        owner=user,
        name="NoMaxChar",
        wow_class=Character.WowClass.MAGE,
        race=Character.WowRace.GNOME,
        level=70,
    )
    prof = Profession.objects.create(name="Fishing")
    tier = ProfessionTier.objects.create(
        profession=prof, expansion_label="Custom", max_skill=None
    )
    cp = CharacterProfession.objects.create(
        character=char, profession_tier=tier, current_skill=50
    )

    model_admin = CharacterProfessionAdmin(CharacterProfession, admin.site)
    assert model_admin.skill_percentage(cp) == "—"


@pytest.mark.django_db
def test_character_admin_registered_and_formatted_gold_and_profession_summary():
    assert Character in admin.site._registry
    model_admin = CharacterAdmin(Character, admin.site)

    user = User.objects.create_user(username="anduin", password="secret")
    char = Character.objects.create(
        owner=user,
        name="Anduin",
        wow_class=Character.WowClass.PRIEST,
        race=Character.WowRace.HUMAN,
        level=70,
    )

    # No assets yet
    assert model_admin.formatted_gold(char) == "0 g"

    # Add some gold
    Asset.objects.create(
        character=char,
        name="Gold",
        category=Asset.Category.GOLD,
        quantity=1000,
    )

    assert model_admin.formatted_gold(char) == "1,000 g"

    # profession_summary is delegated to model method
    assert model_admin.profession_summary(char) == char.profession_summary()


@pytest.mark.django_db
def test_asset_admin_registered_and_get_owner():
    assert Asset in admin.site._registry
    model_admin = AssetAdmin(Asset, admin.site)

    user = User.objects.create_user(username="varian", password="secret")
    char = Character.objects.create(
        owner=user,
        name="Varian",
        wow_class=Character.WowClass.WARRIOR,
        race=Character.WowRace.HUMAN,
        level=80,
    )
    asset = Asset.objects.create(
        character=char,
        name="Gold",
        category=Asset.Category.GOLD,
        quantity=10,
    )

    assert model_admin.get_owner(asset) == user
    assert AssetAdmin.get_owner.short_description == "Owner"
    assert AssetAdmin.get_owner.admin_order_field == "character__owner__username"
