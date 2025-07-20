import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import dotenv


class Command(BaseCommand):
    help = "Creates a superuser from .env variables"

    def handle(self, *args, **options):
        dotenv_path = Path(__file__).resolve().parent.parent.parent.parent / ".env"
        if dotenv_path.exists():
            dotenv.load_dotenv(dotenv_path)
        else:
            self.stderr.write(self.style.ERROR(f".env file not found at {dotenv_path}"))
            return

        username = os.environ.get("DJANGO_SU_NAME")
        email = os.environ.get("DJANGO_SU_EMAIL")
        password = os.environ.get("DJANGO_SU_PASSWORD")

        if not username:
            raise ValueError("DJANGO_SU_NAME not set")

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f"Superuser '{username}' already exists.")
            )
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                registration_accepted=True,
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created."))
