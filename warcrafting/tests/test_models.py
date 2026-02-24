# tests/test_models.py

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from warcrafting.models import (
    Asset,
    Character,
    CharacterProfession,
    Profession,
    ProfessionTier,
)


User = get_user_model()


# ---------------------------------------------------------------------------
# Profession
# ---------------------------------------------------------------------------


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
    ProfessionTier.objects.create(
        profession=prof,
        expansion_label=ProfessionTier.ExpansionLabel.CATACLYSM,
    )
    ProfessionTier.objects.create(
        profession=prof,
        expansion_label=ProfessionTier.ExpansionLabel.CLASSIC,
    )
    ProfessionTier.objects.create(
        profession=prof,
        expansion_label=ProfessionTier.ExpansionLabel.BFA,
    )

    # tier_names should respect explicit order_by("expansion_label")
    tier_names = prof.tier_names
    assert tier_names == "Battle for Azeroth, Cataclysm, Classic"


# ---------------------------------------------------------------------------
# ProfessionTier
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_profession_tier_str_and_unique_together():
    prof = Profession.objects.create(name="Mining")
    tier = ProfessionTier.objects.create(
        profession=prof,
        expansion_label=ProfessionTier.ExpansionLabel.CATACLYSM,
        max_skill=75,
    )
    assert str(tier) == "Cataclysm Mining"
    assert tier.max_skill == 75

    # unique_together(profession, expansion_label) should be enforced
    with pytest.raises(IntegrityError):
        ProfessionTier.objects.create(
            profession=prof,
            expansion_label=ProfessionTier.ExpansionLabel.CATACLYSM,
        )


@pytest.mark.django_db
def test_profession_tier_auto_fills_max_skill():
    """ProfessionTier.save() auto-fills max_skill from EXPANSION_MAX_SKILLS."""
    prof = Profession.objects.create(name="Alchemy")
    tier = ProfessionTier.objects.create(
        profession=prof,
        expansion_label=ProfessionTier.ExpansionLabel.CLASSIC,
    )
    assert tier.max_skill == 300

    tier2 = ProfessionTier.objects.create(
        profession=prof,
        expansion_label=ProfessionTier.ExpansionLabel.BURNING_CRUSADE,
    )
    assert tier2.max_skill == 75


@pytest.mark.django_db
def test_profession_tier_expansion_label_choices():
    """All ExpansionLabel values map to known expansion names."""
    labels = {el.value for el in ProfessionTier.ExpansionLabel}
    expected = {
        "Classic",
        "Burning Crusade",
        "Wrath of the Lich King",
        "Cataclysm",
        "Mists of Pandaria",
        "Warlords of Draenor",
        "Legion",
        "Battle for Azeroth",
        "Shadowlands",
        "Dragonflight",
        "The War Within",
    }
    assert labels == expected


# ---------------------------------------------------------------------------
# Character
# ---------------------------------------------------------------------------


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
def test_character_profession_summary_empty():
    user = User.objects.create_user(username="jaina", password="secret")
    char = Character.objects.create(
        owner=user,
        name="Jaina",
        wow_class=Character.WowClass.MAGE,
        race=Character.WowRace.HUMAN,
        level=70,
    )
    assert char.profession_summary() == "No professions"


@pytest.mark.django_db
def test_character_profession_summary_with_tiers():
    user = User.objects.create_user(username="jaina2", password="secret")
    char = Character.objects.create(
        owner=user,
        name="Jaina",
        wow_class=Character.WowClass.MAGE,
        race=Character.WowRace.HUMAN,
        level=70,
    )

    prof = Profession.objects.create(name="Tailoring")
    classic = ProfessionTier.objects.create(
        profession=prof,
        expansion_label=ProfessionTier.ExpansionLabel.CLASSIC,
    )
    cata = ProfessionTier.objects.create(
        profession=prof,
        expansion_label=ProfessionTier.ExpansionLabel.CATACLYSM,
    )

    CharacterProfession.objects.create(
        character=char, profession_tier=classic, current_skill=150
    )
    CharacterProfession.objects.create(
        character=char, profession_tier=cata, current_skill=50
    )

    summary = char.profession_summary()
    assert "Classic Tailoring" in summary
    assert "Cataclysm Tailoring" in summary
    assert "150" in summary
    assert "50" in summary


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


# ---------------------------------------------------------------------------
# CharacterProfession
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_character_profession_str():
    user = User.objects.create_user(username="cp_user", password="secret")
    char = Character.objects.create(
        owner=user,
        name="Garrosh",
        wow_class=Character.WowClass.WARRIOR,
        race=Character.WowRace.ORC,
        level=70,
    )
    prof = Profession.objects.create(name="Blacksmithing")
    tier = ProfessionTier.objects.create(
        profession=prof,
        expansion_label=ProfessionTier.ExpansionLabel.CLASSIC,
    )
    cp = CharacterProfession.objects.create(
        character=char, profession_tier=tier, current_skill=200
    )
    assert "Garrosh" in str(cp)
    assert "Classic Blacksmithing" in str(cp)
    assert "200" in str(cp)


@pytest.mark.django_db
def test_character_profession_skill_percentage():
    user = User.objects.create_user(username="pct_user", password="secret")
    char = Character.objects.create(
        owner=user,
        name="Velen",
        wow_class=Character.WowClass.PRIEST,
        race=Character.WowRace.DRAENEI,
        level=70,
    )
    prof = Profession.objects.create(name="Alchemy")
    tier = ProfessionTier.objects.create(
        profession=prof,
        expansion_label=ProfessionTier.ExpansionLabel.CLASSIC,
        max_skill=300,
    )
    cp = CharacterProfession.objects.create(
        character=char, profession_tier=tier, current_skill=150
    )
    assert cp.skill_percentage == 50.0


@pytest.mark.django_db
def test_character_profession_skill_percentage_no_max():
    user = User.objects.create_user(username="nomax_user", password="secret")
    char = Character.objects.create(
        owner=user,
        name="Wrathion",
        wow_class=Character.WowClass.ROGUE,
        race=Character.WowRace.DRACTHYR,
        level=70,
    )
    prof = Profession.objects.create(name="Engineering")
    tier = ProfessionTier.objects.create(
        profession=prof,
        expansion_label="Custom Tier",
        max_skill=None,
    )
    cp = CharacterProfession.objects.create(
        character=char, profession_tier=tier, current_skill=50
    )
    assert cp.skill_percentage is None


@pytest.mark.django_db
def test_character_profession_unique_together():
    user = User.objects.create_user(username="uniq_user", password="secret")
    char = Character.objects.create(
        owner=user,
        name="Malfurion",
        wow_class=Character.WowClass.DRUID,
        race=Character.WowRace.NIGHT_ELF,
        level=70,
    )
    prof = Profession.objects.create(name="Herbalism")
    tier = ProfessionTier.objects.create(
        profession=prof,
        expansion_label=ProfessionTier.ExpansionLabel.CLASSIC,
    )
    CharacterProfession.objects.create(
        character=char, profession_tier=tier, current_skill=100
    )
    with pytest.raises(IntegrityError):
        CharacterProfession.objects.create(
            character=char, profession_tier=tier, current_skill=50
        )


# ---------------------------------------------------------------------------
# Asset
# ---------------------------------------------------------------------------


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
