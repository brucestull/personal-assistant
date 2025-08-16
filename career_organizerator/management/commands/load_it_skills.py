import json
import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from career_organizerator.models import Skill


class Command(BaseCommand):
    help = "Load IT Automation skills into the database for a given user."

    def add_arguments(self, parser):
        parser.add_argument(
            "--user-id",
            type=int,
            required=True,
            help="User ID to associate the skills with.",
        )
        parser.add_argument(
            "--json-path",
            type=str,
            default="career_organizerator/data/it_automation_skills.json",
            help="Path to the JSON file containing skill names.",
        )

    def handle(self, *args, **options):
        user_id = options["user_id"]
        json_path = options["json_path"]

        # Load the skill names from the JSON file
        if not os.path.exists(json_path):
            self.stderr.write(self.style.ERROR(f"JSON file not found at {json_path}"))
            return

        with open(json_path, "r", encoding="utf-8") as f:
            try:
                skill_names = json.load(f)
            except json.JSONDecodeError as e:
                self.stderr.write(self.style.ERROR(f"Invalid JSON format: {e}"))
                return

        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            self.stderr.write(
                self.style.ERROR(f"User with ID {user_id} does not exist.")
            )
            return

        created_count = 0
        skipped_count = 0

        for index, skill_name in enumerate(skill_names):
            skill, created = Skill.objects.get_or_create(
                user=user,
                name=skill_name,
                defaults={"order": index},
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"✅ Added: {skill_name}"))
            else:
                skipped_count += 1
                self.stdout.write(f"⚠️ Skipped (already exists): {skill_name}")

        self.stdout.write(
            self.style.NOTICE(
                f"\nSummary:\n  ➕ Created: {created_count}\n  🔁 Skipped: {skipped_count}"  # noqa: E501
            )
        )
