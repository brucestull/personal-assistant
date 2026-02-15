# true_north/management/commands/seed_true_north_demo.py

from __future__ import annotations

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from true_north.models import (
    CoreValue,
    Goal,
    Milestone,
    ValueAction,
    GoalStatus,
    ValueActionStatus,
)  # noqa E501


DEMO_PREFIX = "demo-"  # used for slugs so we can safely delete/reseed


class Command(BaseCommand):
    help = "Seed True North demo data for the existing user 'admin'."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            default="admin",
            help="Username to attach demo data to (default: admin).",
        )
        parser.add_argument(
            "--purge",
            action="store_true",
            help="Delete existing demo data for the user first (recommended).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        username: str = options["username"]
        purge: bool = bool(options["purge"])

        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as exc:
            raise CommandError(
                f"User '{username}' does not exist. Create it first (e.g. createsuperuser)."  # noqa E501
            ) from exc

        if purge:
            self._purge_demo(user)

        # If any demo CoreValues already exist, assume seed has been run.
        if CoreValue.objects.filter(user=user, slug__startswith=DEMO_PREFIX).exists():
            self.stdout.write(
                self.style.WARNING(
                    "Demo data already appears to exist (demo- slugs found). "
                    "Re-run with --purge to recreate."
                )
            )
            return

        now = timezone.now()
        today = timezone.localdate()

        # --- Core Values (3) ---
        core_values_spec = [
            ("Integrity", "Doing what’s right even when it’s hard."),
            ("Growth", "Learning, improving, and building skills over time."),
            ("Care", "Showing up for people and responsibilities with consistency."),
        ]

        core_values: list[CoreValue] = []
        for order, (name, definition) in enumerate(core_values_spec, start=1):
            cv = CoreValue.objects.create(
                user=user,
                name=name,
                slug=f"{DEMO_PREFIX}{order}-{name.lower().replace(' ', '-')}",
                definition=definition,
                is_active=True,
                order=order,
            )
            core_values.append(cv)

        # --- Goals (8) distributed across values ---
        # 3 + 3 + 2 = 8
        goals_spec = [
            # Integrity (3)
            (core_values[0], "Keep promises (small + big)", GoalStatus.ACTIVE),
            (
                core_values[0],
                "Reduce avoidance: do the hard thing first",
                GoalStatus.ACTIVE,
            ),
            (core_values[0], "Build a weekly review habit", GoalStatus.PAUSED),
            # Growth (3)
            (
                core_values[1],
                "Ship a small Django feature every week",
                GoalStatus.ACTIVE,
            ),
            (core_values[1], "Improve testing: pytest + factories", GoalStatus.ACTIVE),
            (core_values[1], "Learn one new concept per month", GoalStatus.DRAFT),
            # Care (2)
            (core_values[2], "Support Mom with reliable routines", GoalStatus.ACTIVE),
            (
                core_values[2],
                "Strengthen relationships with consistent check-ins",
                GoalStatus.ACTIVE,
            ),
        ]

        goals: list[Goal] = []
        for idx, (value, title, status) in enumerate(goals_spec, start=1):
            g = Goal.objects.create(
                user=user,
                value=value,
                title=title,
                slug=f"{DEMO_PREFIX}goal-{idx}-{_slug_piece(title)}",
                description=f"Demo goal for '{value.name}'.",
                status=status,
                start_date=today - timedelta(days=14),
                target_date=today + timedelta(days=90),
                is_active=True,
                order=idx,
            )
            goals.append(g)

        # --- Milestones (16) => 2 per goal ---
        milestones: list[Milestone] = []
        milestone_counter = 0

        for goal_index, goal in enumerate(goals, start=1):
            for j in range(1, 3):  # 2 milestones each
                milestone_counter += 1
                desc = f"Milestone {j} for Goal {goal_index}: {goal.title}"
                is_completed = milestone_counter % 5 == 0  # some completed
                ms = Milestone.objects.create(
                    user=user,
                    goal=goal,
                    description=desc,
                    slug=f"{DEMO_PREFIX}ms-{milestone_counter}-{_slug_piece(desc)[:60]}",  # noqa E501
                    notes="Demo milestone notes.",
                    due_date=today + timedelta(days=7 * j),
                    is_completed=is_completed,
                    completed_at=(now - timedelta(days=3)) if is_completed else None,
                    order=j,
                )
                milestones.append(ms)

        # --- Value Actions (64) => 4 per milestone ---
        # This yields exactly 16 * 4 = 64
        task_templates = [
            "Define what 'done' means for this milestone.",
            "Do the smallest next step (15 minutes).",
            "Capture blockers and a workaround.",
            "Mark progress and leave a short note.",
        ]

        tasks_created = 0
        for ms_index, ms in enumerate(milestones, start=1):
            for k, template in enumerate(task_templates, start=1):
                tasks_created += 1
                content = f"[{ms_index}.{k}] {template}"
                completed = tasks_created % 7 == 0  # some completed
                status = (
                    ValueActionStatus.DONE
                    if completed
                    else (ValueActionStatus.DOING if k == 2 else ValueActionStatus.TODO)
                )

                ValueAction.objects.create(
                    user=user,
                    milestone=ms,
                    content=content,
                    status=status,
                    due_date=today + timedelta(days=(k + (ms_index % 5))),
                    is_completed=completed,
                    completed_at=(now - timedelta(days=1)) if completed else None,
                    order=k,
                )

        # --- Summary ---
        self.stdout.write(
            self.style.SUCCESS("Seeded True North demo data for user: %s" % username)
        )
        self.stdout.write(
            "Created: "
            f"{CoreValue.objects.filter(user=user, slug__startswith=DEMO_PREFIX).count()} CoreValues, "  # noqa E501
            f"{Goal.objects.filter(user=user, slug__startswith=DEMO_PREFIX).count()} Goals, "  # noqa E501
            f"{Milestone.objects.filter(user=user, slug__startswith=DEMO_PREFIX).count()} Milestones, "  # noqa E501
            f"{ValueAction.objects.filter(user=user).filter(milestone__slug__startswith=DEMO_PREFIX).count()} Value Actions"  # noqa E501
        )

    def _purge_demo(self, user):
        """
        Delete previously-seeded demo objects for the user.
        We identify demo data via DEMO_PREFIX in slugs.
        """
        # Delete leaf-to-root to avoid FK issues
        ValueAction.objects.filter(
            user=user, milestone__slug__startswith=DEMO_PREFIX
        ).delete()
        Milestone.objects.filter(user=user, slug__startswith=DEMO_PREFIX).delete()
        Goal.objects.filter(user=user, slug__startswith=DEMO_PREFIX).delete()
        CoreValue.objects.filter(user=user, slug__startswith=DEMO_PREFIX).delete()

        self.stdout.write(
            self.style.WARNING(
                "Purged existing demo data for user '%s'." % user.username
            )
        )


def _slug_piece(text: str) -> str:
    # tiny helper: keep it deterministic and readable
    return (
        "".join(ch.lower() if ch.isalnum() else "-" for ch in text)
        .strip("-")
        .replace("--", "-")
    )
