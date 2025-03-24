import json
from django.core.management.base import BaseCommand
from uc_goals.models import Virtue, VIACharacterStrength


class Command(BaseCommand):
    help = "Load VIA Character Strengths from via_character_strengths.json"

    def handle(self, *args, **kwargs):
        with open(
            "uc_goals/dicts/via_character_strengths.json", "r", encoding="utf-8"
        ) as f:
            strengths_data = json.load(f)

        for strength_data in strengths_data:
            try:
                virtue = Virtue.objects.get(name=strength_data["virtue"])
            except Virtue.DoesNotExist:
                self.stderr.write(
                    self.style.ERROR(f"Virtue not found: {strength_data['virtue']}")
                )
                continue

            strength, created = VIACharacterStrength.objects.get_or_create(
                name=strength_data["title"],
                defaults={
                    "description": strength_data["description"],
                    "virtue": virtue,
                },
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created strength: {strength.name}")
                )
            else:
                self.stdout.write(f"Strength already exists: {strength.name}")
