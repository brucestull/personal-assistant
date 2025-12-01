# tests/test_models.py

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from warcrafting.models import Asset, Character, Profession, ProfessionTier


User = get_user_model()


@pytest.mark.django_db
def test_profession_str_and_ordering():
    Profession.objects.create(name="Mining")
    Profession.objects.create(name="Herbalism")
    names = list(Profession.objects.values_list("name", flat=True))
    assert names == sorted(names)  # ordering Meta
    assert str(Profession.objects.get(name="Mining")) == "Mining"


@pytest.mark.django_db
def test_profession_tier_names_property_orders_by_expansion_label():
    prof = Profession.objects.create(name="Mining")
    ProfessionTier.objects.create(profession=prof, expansion_label="Cataclysm")
    ProfessionTier.objects.create(profession=prof, expansion_label="Classic")
    ProfessionTier.objects.create(profession=prof, expansion_label="Battle for Azeroth")

    # tier_names should respect explicit order_by("expansion_label")
    tier_names = prof.tier_names
    assert tier_names == "Battle for Azeroth, Cataclysm, Classic"


@pytest.mark.django_db
def test_profession_tier_str_and_unique_together():
    prof = Profession.objects.create(name="Mining")
    tier = ProfessionTier.objects.create(
        profession=prof,
        expansion_label="Cataclysm",
        max_skill=75,
    )
    assert str(tier) == "Cataclysm Mining"
    assert tier.max_skill == 75

    # unique_together(profession, expansion_label) should be enforced
    with pytest.raises(IntegrityError):
        ProfessionTier.objects.create(
            profession=prof,
            expansion_label="Cataclysm",
        )


@pytest.mark.django_db
def test_character_str_and_unique_together():
    user = User.objects.create_user(username="arthas", password="secret")
    char = Character.objects.create(
        owner=user,
        name="Arthas",
        wow_class=Character.WowClass.PALADIN,
        race=Character.WowRace.HUMAN,
        level=80,
    )
    assert str(char) == "Arthas (arthas)"

    # unique_together(owner, name)
    with pytest.raises(IntegrityError):
        Character.objects.create(
            owner=user,
            name="Arthas",
            wow_class=Character.WowClass.WARRIOR,
            race=Character.WowRace.HUMAN,
            level=1,
        )


@pytest.mark.django_db
def test_character_profession_summary_empty_and_with_tiers():
    user = User.objects.create_user(username="jaina", password="secret")
    char = Character.objects.create(
        owner=user,
        name="Jaina",
        wow_class=Character.WowClass.MAGE,
        race=Character.WowRace.HUMAN,
        level=70,
    )

    # No professions yet
    assert char.profession_summary() == "—"

    # Add some tiers
    prof = Profession.objects.create(name="Tailoring")
    classic = ProfessionTier.objects.create(
        profession=prof,
        expansion_label="Classic",
    )
    cata = ProfessionTier.objects.create(
        profession=prof,
        expansion_label="Cataclysm",
    )

    char.professions.add(classic, cata)

    summary = char.profession_summary()
    # uses __str__ of ProfessionTier, so expansion + profession
    assert "Classic Tailoring" in summary
    assert "Cataclysm Tailoring" in summary


@pytest.mark.django_db
def test_character_total_gold_counts_only_gold_assets():
    user = User.objects.create_user(username="thrall", password="secret")
    char = Character.objects.create(
        owner=user,
        name="Thrall",
        wow_class=Character.WowClass.SHAMAN,
        race=Character.WowRace.ORC,
        level=60,
    )

    # No assets yet
    assert char.total_gold() == 0

    # Add some assets: gold and non-gold
    Asset.objects.create(
        character=char,
        name="Gold",
        category=Asset.Category.GOLD,
        quantity=123,
    )
    Asset.objects.create(
        character=char,
        name="Cool Axe",
        category=Asset.Category.GEAR,
        quantity=1,
    )
    Asset.objects.create(
        character=char,
        name="More Gold",
        category=Asset.Category.GOLD,
        quantity=7,
    )

    assert char.total_gold() == 130  # 123 + 7


@pytest.mark.django_db
def test_character_profile_line_uses_display_values():
    user = User.objects.create_user(username="illidan", password="secret")
    char = Character.objects.create(
        owner=user,
        name="Illidan",
        wow_class=Character.WowClass.DEMON_HUNTER,
        race=Character.WowRace.NIGHT_ELF,
        level=70,
    )

    profile = char.profile_line
    # "70 Night Elf Demon Hunter"
    assert str(char.level) in profile
    assert "Night Elf" in profile
    assert "Demon Hunter" in profile


@pytest.mark.django_db
def test_asset_str_and_unique_together():
    user = User.objects.create_user(username="sylvanas", password="secret")
    char = Character.objects.create(
        owner=user,
        name="Sylvanas",
        wow_class=Character.WowClass.HUNTER,
        race=Character.WowRace.UNDEAD,
        level=70,
    )

    asset = Asset.objects.create(
        character=char,
        name="Bow of the Banshee Queen",
        category=Asset.Category.GEAR,
        quantity=1,
        is_unique=True,
    )

    assert str(asset) == "Bow of the Banshee Queen (Sylvanas)"
    assert asset.is_unique is True

    # unique_together(character, name, category)
    with pytest.raises(IntegrityError):
        Asset.objects.create(
            character=char,
            name="Bow of the Banshee Queen",
            category=Asset.Category.GEAR,
            quantity=1,
        )
