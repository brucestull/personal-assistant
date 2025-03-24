import json
from django.core.management.base import BaseCommand
from uc_goals.models import Virtue


class Command(BaseCommand):
    help = "Load Virtues from virtues.json"

    def handle(self, *args, **kwargs):
        with open("uc_goals/dicts/virtues.json", "r", encoding="utf-8") as f:
            virtues_data = json.load(f)

        for virtue_data in virtues_data:
            virtue, created = Virtue.objects.get_or_create(
                name=virtue_data["name"],
                defaults={"description": virtue_data["description"]},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created virtue: {virtue.name}"))
            else:
                self.stdout.write(f"Virtue already exists: {virtue.name}")
