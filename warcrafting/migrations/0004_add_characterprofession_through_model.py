# Generated migration: add CharacterProfession through model

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("warcrafting", "0003_alter_character_race"),
    ]

    operations = [
        # 1. Update Profession.name field with choices
        migrations.AlterField(
            model_name="profession",
            name="name",
            field=models.CharField(
                choices=[
                    ("Alchemy", "Alchemy"),
                    ("Blacksmithing", "Blacksmithing"),
                    ("Enchanting", "Enchanting"),
                    ("Engineering", "Engineering"),
                    ("Inscription", "Inscription"),
                    ("Jewelcrafting", "Jewelcrafting"),
                    ("Leatherworking", "Leatherworking"),
                    ("Tailoring", "Tailoring"),
                    ("Fishing", "Fishing"),
                    ("Herbalism", "Herbalism"),
                    ("Mining", "Mining"),
                    ("Skinning", "Skinning"),
                    ("Archaeology", "Archaeology"),
                    ("Cooking", "Cooking"),
                ],
                help_text="Select a World of Warcraft profession.",
                max_length=64,
                unique=True,
            ),
        ),
        # 2. Update ProfessionTier.expansion_label field with choices
        migrations.AlterField(
            model_name="professiontier",
            name="expansion_label",
            field=models.CharField(
                choices=[
                    ("Classic", "Classic"),
                    ("Burning Crusade", "The Burning Crusade"),
                    ("Wrath of the Lich King", "Wrath of the Lich King"),
                    ("Cataclysm", "Cataclysm"),
                    ("Mists of Pandaria", "Mists of Pandaria"),
                    ("Warlords of Draenor", "Warlords of Draenor"),
                    ("Legion", "Legion"),
                    ("Battle for Azeroth", "Battle for Azeroth"),
                    ("Shadowlands", "Shadowlands"),
                    ("Dragonflight", "Dragonflight"),
                    ("The War Within", "The War Within"),
                ],
                help_text="Expansion that introduced this tier.",
                max_length=64,
            ),
        ),
        # 3. Update ProfessionTier.max_skill help text
        migrations.AlterField(
            model_name="professiontier",
            name="max_skill",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Max skill for this tier (auto-filled if left blank).",
                null=True,
            ),
        ),
        # 4. Remove the old auto-generated M2M
        migrations.RemoveField(
            model_name="character",
            name="professions",
        ),
        # 5. Create the CharacterProfession through model
        migrations.CreateModel(
            name="CharacterProfession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "current_skill",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Your current skill level in this expansion tier.",
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="character_professions",
                        to="warcrafting.character",
                    ),
                ),
                (
                    "profession_tier",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="character_professions",
                        to="warcrafting.professiontier",
                    ),
                ),
            ],
            options={
                "ordering": ["character__name", "profession_tier__profession__name"],
                "unique_together": {("character", "profession_tier")},
            },
        ),
        # 6. Add the new M2M field with through model
        migrations.AddField(
            model_name="character",
            name="professions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Expansion-specific professions for this character.",
                related_name="characters",
                through="warcrafting.CharacterProfession",
                to="warcrafting.professiontier",
            ),
        ),
    ]
