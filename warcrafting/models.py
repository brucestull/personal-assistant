# warcrafting/models.py

from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator


# ---------------------------------------------------------------------------
# Choices
# ---------------------------------------------------------------------------

PROFESSION_NAME_CHOICES = [
    # Crafting professions
    ("Alchemy", "Alchemy"),
    ("Blacksmithing", "Blacksmithing"),
    ("Enchanting", "Enchanting"),
    ("Engineering", "Engineering"),
    ("Inscription", "Inscription"),
    ("Jewelcrafting", "Jewelcrafting"),
    ("Leatherworking", "Leatherworking"),
    ("Tailoring", "Tailoring"),
    # Gathering professions
    ("Fishing", "Fishing"),
    ("Herbalism", "Herbalism"),
    ("Mining", "Mining"),
    ("Skinning", "Skinning"),
    # Secondary professions
    ("Archaeology", "Archaeology"),
    ("Cooking", "Cooking"),
]


class TimeStampedModel(models.Model):
    """Abstract base model for created/updated timestamps."""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profession(TimeStampedModel):
    """
    Base profession type: Mining, Herbalism, Blacksmithing, etc.
    Expansion-specific tiers hang off this via ProfessionTier.
    """

    name = models.CharField(
        max_length=64,
        unique=True,
        choices=PROFESSION_NAME_CHOICES,
        help_text="Select a World of Warcraft profession.",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    @property
    def tier_names(self) -> str:
        """
        Convenience summary of expansion tiers, e.g.
        'Classic, Burning Crusade, Wrath of the Lich King'.
        """
        tiers = self.tiers.order_by("expansion_label").values_list(
            "expansion_label", flat=True
        )
        return ", ".join(tiers)


class ProfessionTier(TimeStampedModel):
    """
    Expansion-specific "section" of a profession, e.g. 'Cataclysm Mining'.

    Example:
        Profession(name="Mining")
        ProfessionTier(profession=Mining, expansion_label="Cataclysm")
        -> "Cataclysm Mining"
    """

    class ExpansionLabel(models.TextChoices):
        CLASSIC = "Classic", "Classic"
        BURNING_CRUSADE = "Burning Crusade", "The Burning Crusade"
        WRATH = "Wrath of the Lich King", "Wrath of the Lich King"
        CATACLYSM = "Cataclysm", "Cataclysm"
        MISTS = "Mists of Pandaria", "Mists of Pandaria"
        WARLORDS = "Warlords of Draenor", "Warlords of Draenor"
        LEGION = "Legion", "Legion"
        BFA = "Battle for Azeroth", "Battle for Azeroth"
        SHADOWLANDS = "Shadowlands", "Shadowlands"
        DRAGONFLIGHT = "Dragonflight", "Dragonflight"
        WAR_WITHIN = "The War Within", "The War Within"

    # Default max skill per expansion tier
    EXPANSION_MAX_SKILLS = {
        "Classic": 300,
        "Burning Crusade": 75,
        "Wrath of the Lich King": 75,
        "Cataclysm": 75,
        "Mists of Pandaria": 75,
        "Warlords of Draenor": 100,
        "Legion": 100,
        "Battle for Azeroth": 175,
        "Shadowlands": 150,
        "Dragonflight": 100,
        "The War Within": 100,
    }

    profession = models.ForeignKey(
        Profession,
        on_delete=models.CASCADE,
        related_name="tiers",
    )
    expansion_label = models.CharField(
        max_length=64,
        choices=ExpansionLabel.choices,
        help_text="Expansion that introduced this tier.",
    )
    max_skill = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Max skill for this tier (auto-filled if left blank).",
    )

    class Meta:
        unique_together = ("profession", "expansion_label")
        ordering = ["profession__name", "expansion_label"]

    def save(self, *args, **kwargs):
        """Auto-fill max_skill from expansion defaults when not provided."""
        if self.max_skill is None:
            self.max_skill = self.EXPANSION_MAX_SKILLS.get(self.expansion_label)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.expansion_label} {self.profession.name}"


class Character(TimeStampedModel):
    class WowClass(models.TextChoices):
        WARRIOR = "warrior", "Warrior"
        PALADIN = "paladin", "Paladin"
        HUNTER = "hunter", "Hunter"
        ROGUE = "rogue", "Rogue"
        PRIEST = "priest", "Priest"
        DEATH_KNIGHT = "death_knight", "Death Knight"
        SHAMAN = "shaman", "Shaman"
        MAGE = "mage", "Mage"
        WARLOCK = "warlock", "Warlock"
        MONK = "monk", "Monk"
        DRUID = "druid", "Druid"
        DEMON_HUNTER = "demon_hunter", "Demon Hunter"
        EVOKER = "evoker", "Evoker"

    class WowRace(models.TextChoices):
        # Original races
        HUMAN = "human", "Human"
        ORC = "orc", "Orc"
        NIGHT_ELF = "night_elf", "Night Elf"
        UNDEAD = "undead", "Undead"
        TAUREN = "tauren", "Tauren"
        TROLL = "troll", "Troll"
        GNOME = "gnome", "Gnome"
        DWARF = "dwarf", "Dwarf"
        # The Burning Crusade
        BLOOD_ELF = "blood_elf", "Blood Elf"
        DRAENEI = "draenei", "Draenei"
        # Cataclysm
        GOBLIN = "goblin", "Goblin"
        WORGEN = "worgen", "Worgen"
        # Mists of Pandaria
        PANDAREN = "pandaren", "Pandaren"
        # Battle for Azeroth - Allied Races
        VOID_ELF = "void_elf", "Void Elf"
        LIGHTFORGED_DRAENEI = "lightforged_draenei", "Lightforged Draenei"
        HIGHMOUNTAIN_TAUREN = "highmountain_tauren", "Highmountain Tauren"
        NIGHTBORNE = "nightborne", "Nightborne"
        DARK_IRON_DWARF = "dark_iron_dwarf", "Dark Iron Dwarf"
        MAGHAR_ORC = "maghar_orc", "Mag'har Orc"
        ZANDALARI_TROLL = "zandalari_troll", "Zandalari Troll"
        KUL_TIRAN = "kul_tiran", "Kul Tiran"
        MECHAGNOME = "mechagnome", "Mechagnome"
        VULPERA = "vulpera", "Vulpera"
        # Dragonflight
        DRACTHYR = "dracthyr", "Dracthyr"
        # The War Within
        EARTHEN = "earthen", "Earthen"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wow_characters",
    )
    name = models.CharField(max_length=64)
    wow_class = models.CharField(
        max_length=32,
        choices=WowClass.choices,
        help_text="Character class (Warrior, Mage, etc.).",
    )
    race = models.CharField(
        max_length=32,
        choices=WowRace.choices,
        help_text="Character race.",
    )
    level = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Current character level.",
    )

    professions = models.ManyToManyField(
        ProfessionTier,
        through="CharacterProfession",
        related_name="characters",
        blank=True,
        help_text="Expansion-specific professions for this character.",
    )

    class Meta:
        ordering = ["owner__username", "name"]
        unique_together = ("owner", "name")

    def __str__(self) -> str:
        return f"{self.name} ({self.owner})"

    def profession_summary(self) -> str:
        """
        Comma-separated summary of this character's profession tiers with
        current skill levels, or 'No professions' if none.
        """
        char_profs = self.character_professions.select_related(
            "profession_tier__profession"
        )
        if not char_profs.exists():
            return "No professions"
        parts = []
        for cp in char_profs:
            tier = cp.profession_tier
            if tier.max_skill:
                skill_info = f"{cp.current_skill}/{tier.max_skill}"
            else:
                skill_info = str(cp.current_skill)
            parts.append(f"{tier} ({skill_info})")
        return ", ".join(parts)

    profession_summary.short_description = "Professions"

    def total_gold(self) -> int:
        gold_assets = self.assets.filter(
            category=Asset.Category.GOLD  # type: ignore[name-defined]
        )
        return sum(a.quantity for a in gold_assets)

    total_gold.short_description = "Gold (g)"

    @property
    def profile_line(self) -> str:
        """
        Nicely formatted 'armory-style' summary.

        Example:
            '70 Night Elf Druid'
        """
        return f"{self.level} {self.get_race_display()} {self.get_wow_class_display()}"


class CharacterProfession(TimeStampedModel):
    """
    Through model for Character <-> ProfessionTier M2M.
    Stores the character's current skill level in a specific profession tier.
    """

    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name="character_professions",
    )
    profession_tier = models.ForeignKey(
        ProfessionTier,
        on_delete=models.CASCADE,
        related_name="character_professions",
    )
    current_skill = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Your current skill level in this expansion tier.",
    )

    class Meta:
        unique_together = ("character", "profession_tier")
        ordering = ["character__name", "profession_tier__profession__name"]

    def __str__(self) -> str:
        return (
            f"{self.character.name} - {self.profession_tier} "
            f"({self.current_skill})"
        )

    @property
    def skill_percentage(self):
        """Percentage progress toward max skill, or None if max is unknown."""
        if self.profession_tier.max_skill:
            return round(
                (self.current_skill / self.profession_tier.max_skill) * 100, 1
            )
        return None


class Asset(TimeStampedModel):
    """
    Track per-character assets that are not meant to be shared:
    - Gold (per character)
    - Soulbound items
    - Unique mounts/pets you want to track at a character level
    """

    class Category(models.TextChoices):
        GOLD = "gold", "Gold"
        CURRENCY = "currency", "Currency"
        GEAR = "gear", "Gear"
        MOUNT = "mount", "Mount"
        PET = "pet", "Pet"
        OTHER = "other", "Other"

    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name="assets",
    )
    name = models.CharField(
        max_length=128,
        help_text="E.g. 'Gold', 'Ashes of Al'ar', 'Timewarped Badge'.",
    )
    category = models.CharField(
        max_length=16,
        choices=Category.choices,
        default=Category.OTHER,
    )
    quantity = models.PositiveIntegerField(
        default=0,
        help_text=(
            "For GOLD, treat this as 'whole gold pieces'. "
            "For items, use count (e.g. 1 for a unique mount)."
        ),
    )
    is_unique = models.BooleanField(
        default=False,
        help_text="Check if this is meant to be a unique/soulbound thing.",
    )
    notes = models.TextField(
        blank=True,
        help_text="Optional notes (where it dropped, why it matters, etc.).",
    )

    class Meta:
        ordering = ["character__owner__username", "character__name", "name"]
        unique_together = ("character", "name", "category")

    def __str__(self) -> str:
        return f"{self.name} ({self.character.name})"
