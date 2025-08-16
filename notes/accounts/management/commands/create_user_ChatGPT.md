# `create_user.py` Management Command

- [Expand user creation functionality - ChatGPT - Private](https://chatgpt.com/c/68a054a8-69d8-8324-b00c-d0a52f89c98a)
- [Expand user creation functionality - ChatGPT - Shared](https://chatgpt.com/share/68a05be9-f888-8002-839d-1b6de4f8b084)

I have a Django management command `accounts/management/commands/createsu.py`:

```python
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
```

I want to expand it's functionality to be able to use the following env variables for a regular user for testing.

DJANGO_USER_NAME
DJANGO_USER_EMAIL
DJANGO_USER_PASSWORD

What is a best-practice way to do that?

---

Nice and clean way to do it:

1. keep the command idempotent (safe to re-run),
2. make it explicit what you want to create (su, user, or both),
3. let you optionally **update** an existing user’s password/email (useful in dev/CI),
4. pull creds from `.env` with clear prefixes.

Here’s a drop-in upgrade for your command.

```python
# accounts/management/commands/createsu.py
import os
from pathlib import Path
from typing import Tuple, Dict

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.db import transaction
import dotenv


ENV_ROOT = Path(__file__).resolve().parents[4]  # project root guess
DOTENV_PATH = ENV_ROOT / ".env"

# Environment variable names
SU_VARS = {
    "username": "DJANGO_SU_NAME",
    "email": "DJANGO_SU_EMAIL",
    "password": "DJANGO_SU_PASSWORD",
}
USER_VARS = {
    "username": "DJANGO_USER_NAME",
    "email": "DJANGO_USER_EMAIL",
    "password": "DJANGO_USER_PASSWORD",
    # Optional toggles for your custom fields in dev
    "accepted": "DJANGO_USER_ACCEPTED",  # "1" or "0"
    "staff": "DJANGO_USER_IS_STAFF",     # "1" or "0"
}


class Command(BaseCommand):
    help = "Create users from .env variables (superuser and/or regular user)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--create",
            choices=["su", "user", "both"],
            default="both",
            help="What to create from env vars (default: both).",
        )
        parser.add_argument(
            "--update-existing",
            action="store_true",
            help="If user already exists, update email and password from env.",
        )
        parser.add_argument(
            "--dotenv",
            default=str(DOTENV_PATH),
            help="Path to .env (default: project_root/.env).",
        )

    def handle(self, *args, **options):
        # Load .env
        dotenv_path = Path(options["dotenv"])
        if dotenv_path.exists():
            dotenv.load_dotenv(dotenv_path)
        else:
            raise CommandError(f".env file not found at {dotenv_path}")

        created_anything = False

        if options["create"] in ("su", "both"):
            created_anything |= self._create_superuser(update_existing=options["update_existing"])

        if options["create"] in ("user", "both"):
            created_anything |= self._create_regular_user(update_existing=options["update_existing"])

        if not created_anything:
            self.stdout.write(self.style.WARNING("Nothing to do."))

    # ──────────────────────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────────────────────
    def _read_env(self, mapping: Dict[str, str]) -> Tuple[str, str, str, Dict]:
        """
        Return (username, email, password, extras)
        Raises CommandError if username missing.
        """
        username = os.getenv(mapping["username"]) or ""
        email = os.getenv(mapping["email"]) or ""
        password = os.getenv(mapping["password"]) or ""
        if not username:
            raise CommandError(f"{mapping['username']} not set")

        extras = {}
        # Optional toggles for regular users
        if "accepted" in mapping:
            extras["registration_accepted"] = (os.getenv(mapping["accepted"], "1") == "1")
        if "staff" in mapping:
            extras["is_staff"] = (os.getenv(mapping["staff"], "0") == "1")

        return username, email, password, extras

    @transaction.atomic
    def _ensure_user(self, *, username: str, email: str, password: str, update_existing: bool, **extra_fields):
        User = get_user_model()
        qs = User.objects.filter(username=username)
        if qs.exists():
            user = qs.get()
            if update_existing:
                # update only provided values
                changed = False
                if email and user.email != email:
                    user.email = email
                    changed = True
                # Update booleans if provided in extra_fields
                for k, v in extra_fields.items():
                    if v is not None and getattr(user, k, None) != v:
                        setattr(user, k, v)
                        changed = True
                if password:
                    user.set_password(password)
                    changed = True
                if changed:
                    user.save(update_fields=None)  # save all touched fields
                    self.stdout.write(self.style.SUCCESS(f"Updated existing user '{username}'"))
                else:
                    self.stdout.write(self.style.WARNING(f"No changes for existing user '{username}'"))
            else:
                self.stdout.write(self.style.WARNING(f"User '{username}' already exists. (use --update-existing to modify)"))
            return False  # not created
        else:
            # Create new user
            user = User.objects.create_user(
                username=username,
                email=email or "",
                password=password or None,
                **extra_fields,
            )
            # If you have required fields in a custom user, set them here via extra_fields
            self.stdout.write(self.style.SUCCESS(f"Created user '{username}'"))
            return True  # created

    def _create_superuser(self, *, update_existing: bool) -> bool:
        username, email, password, extras = self._read_env(SU_VARS)
        # Ensure superuser flags
        extras.update({"is_superuser": True, "is_staff": True, "registration_accepted": True})
        # If already exists but isn’t a superuser, --update-existing will elevate it
        return self._ensure_user(
            username=username,
            email=email,
            password=password,
            update_existing=update_existing,
            **extras,
        )

    def _create_regular_user(self, *, update_existing: bool) -> bool:
        username, email, password, extras = self._read_env(USER_VARS)
        # Ensure regular flags (explicitly clear su)
        extras.update({"is_superuser": False})
        # If your CustomUser defaults handle accepted/staff, extras may omit them
        return self._ensure_user(
            username=username,
            email=email,
            password=password,
            update_existing=update_existing,
            **extras,
        )
```

### Why this is “best-practicey”

* **Explicit**: `--create su|user|both` makes intent clear; no surprises.
* **Idempotent**: safe to run in dev/CI; won’t duplicate users.
* **Configurable**: `--update-existing` lets you rotate credentials in CI or local dev without manual DB edits.
* **Small blast radius**: regular users are created with `is_superuser=False`; you can also set `registration_accepted` or `is_staff` via optional envs for test scenarios.
* **Transactional**: each create/update runs in a transaction to avoid partial writes.

### .env keys you can use

* Superuser (unchanged):
  `DJANGO_SU_NAME`, `DJANGO_SU_EMAIL`, `DJANGO_SU_PASSWORD`
* Regular user (new):
  `DJANGO_USER_NAME`, `DJANGO_USER_EMAIL`, `DJANGO_USER_PASSWORD`
  Optional: `DJANGO_USER_ACCEPTED=1|0`, `DJANGO_USER_IS_STAFF=1|0`

### Example usage

```bash
# Create both from .env (default behavior)
python manage.py createsu

# Only create the regular user
python manage.py createsu --create user

# Re-run and update password/email/flags if the users already exist
python manage.py createsu --update-existing

# Custom .env path
python manage.py createsu --dotenv ./config/.env.local
```

### Quick security note

Storing passwords in `.env` is fine for **local dev/CI**. For real environments:

* Prefer fixtures/FactoryBoy for test users.
* For CI, inject creds via secret manager (GitHub Actions/Cloud) and use `--update-existing`.
* Never commit the `.env` file. Add it to `.gitignore`.

If you want this to also **create groups** or assign permissions for the test user, say the word and I’ll add a tiny `--group`/`--perm` option.

---
