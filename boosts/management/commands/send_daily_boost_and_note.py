# boosts/management/commands/send_daily_boost_and_note.py
"""
Management command: send_daily_boost_and_note

Manually trigger sending a daily boost (Inspirational) and note
(UnimportantNote) to a specified user or all users with email addresses.

Usage:
    python manage.py send_daily_boost_and_note --user-id 1
    python manage.py send_daily_boost_and_note --all-users
    python manage.py send_daily_boost_and_note --username testuser

This command is useful for:
- Testing the email functionality
- Manually triggering daily emails outside of the scheduled task
- Debugging email delivery issues
"""

from django.core.management.base import BaseCommand, CommandError

from accounts.models import CustomUser
from boosts.tasks import send_daily_boost_and_note


class Command(BaseCommand):
    help = (
        "Send a daily boost and note to a user or all users. "
        "Specify --user-id, --username, or --all-users."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--user-id",
            type=int,
            help="Send to a specific user by ID",
        )
        parser.add_argument(
            "--username",
            type=str,
            help="Send to a specific user by username",
        )
        parser.add_argument(
            "--all-users",
            action="store_true",
            help="Send to all users with email addresses",
        )

    def handle(self, *args, **options):
        user_id = options.get("user_id")
        username = options.get("username")
        all_users = options.get("all_users")

        # Validate that exactly one option is provided
        options_count = sum([bool(user_id), bool(username), bool(all_users)])
        if options_count == 0:
            raise CommandError(
                "You must specify one of: --user-id, --username, or --all-users"
            )
        if options_count > 1:
            raise CommandError(
                "You can only specify one of: --user-id, --username, or --all-users"
            )

        if user_id:
            self._send_to_user_by_id(user_id)
        elif username:
            self._send_to_user_by_username(username)
        elif all_users:
            self._send_to_all_users()

    def _send_to_user_by_id(self, user_id):
        """Send to a specific user by ID."""
        try:
            user = CustomUser.objects.get(pk=user_id)
            self.stdout.write(
                f"Sending daily boost and note to user: {user.username} "
                f"(ID: {user.id})"
            )
            send_daily_boost_and_note.delay(user.id)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Task queued successfully for user {user.username}"
                )
            )
        except CustomUser.DoesNotExist:
            raise CommandError(f"User with ID {user_id} does not exist")

    def _send_to_user_by_username(self, username):
        """Send to a specific user by username."""
        try:
            user = CustomUser.objects.get(username=username)
            self.stdout.write(
                f"Sending daily boost and note to user: {user.username} "
                f"(ID: {user.id})"
            )
            send_daily_boost_and_note.delay(user.id)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Task queued successfully for user {user.username}"
                )
            )
        except CustomUser.DoesNotExist:
            raise CommandError(f"User with username '{username}' does not exist")

    def _send_to_all_users(self):
        """Send to all users with email addresses."""
        users = CustomUser.objects.exclude(email="").exclude(email__isnull=True)
        count = users.count()

        if count == 0:
            self.stdout.write(
                self.style.WARNING("No users with email addresses found")
            )
            return

        self.stdout.write(
            f"Queueing daily boost and note tasks for {count} user(s)..."
        )

        for user in users:
            send_daily_boost_and_note.delay(user.id)
            self.stdout.write(f"  - Queued for {user.username} (ID: {user.id})")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully queued tasks for {count} user(s)"
            )
        )
