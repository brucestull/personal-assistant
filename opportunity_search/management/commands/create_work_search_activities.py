import json

from django.core.management.base import BaseCommand

from opportunity_search.models import WorkSearchActivity


class Command(BaseCommand):
    help = "Create some work search activities"

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating Work Search Activities...")

        with open("dicts/work_search_activities.json") as f:
            data = json.load(f)

            descriptions = data["descriptions"]
            for description in descriptions:
                WorkSearchActivity.objects.create(description=description)

        self.stdout.write(self.style.SUCCESS("Created Work Search Activities."))
