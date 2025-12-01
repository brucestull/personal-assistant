# warcrafting/models.py

from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator


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

    name = models.CharField(max_length=64, unique=True)

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
    Expansion-specific “section” of a profession, e.g. 'Cataclysm Mining'.

    Example:
        Profession(name="Mining")
        ProfessionTier(profession=Mining, expansion_label="Cataclysm")
        -> "Cataclysm Mining"
    """

    profession = models.ForeignKey(
        Profession,
        on_delete=models.CASCADE,
        related_name="tiers",
    )
    expansion_label = models.CharField(
        max_length=64,
        help_text="E.g. 'Classic', 'Cataclysm', 'Battle for Azeroth'.",
    )
    max_skill = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Optional: max skill for this tier (e.g. 75, 150).",
    )

    class Meta:
        unique_together = ("profession", "expansion_label")
        ordering = ["profession__name", "expansion_label"]

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
        HUMAN = "human", "Human"
        ORC = "orc", "Orc"
        NIGHT_ELF = "night_elf", "Night Elf"
        UNDEAD = "undead", "Undead"
        PANDAREN = "pandaren", "Pandaren"
        # Add more races here as needed

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
        Comma-separated summary of this character's profession tiers,
        or '—' if none.
        """
        tiers = self.professions.select_related("profession")
        if not tiers.exists():
            return "—"
        return ", ".join(str(t) for t in tiers)

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
