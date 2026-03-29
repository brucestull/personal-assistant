# true_north/models.py

from __future__ import annotations

from datetime import datetime as _dt
from datetime import time as _time
from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from base.mixins import OrderableMixin
from base.models import CreatedUpdatedBase


class UserOwnedBase(CreatedUpdatedBase):
    """
    Abstract base: ties objects to a user (CustomUser via AUTH_USER_MODEL).

    IMPORTANT:
    related_name includes app_label to avoid collisions with other apps
    that have models with the same class names (e.g. a separate `tasks` app).
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)ss",
    )

    class Meta:
        abstract = True


class CoreValue(UserOwnedBase, OrderableMixin):
    name = models.CharField(
        max_length=100,
        help_text='Short value name (e.g., "Integrity").',
    )
    slug = models.SlugField(
        max_length=120,
        help_text="URL-friendly identifier (auto from name).",
    )
    definition = models.TextField(
        help_text="What this value means to you (your definition).",
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[: self._meta.get_field("slug").max_length]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "slug"],
                name="true_north_corevalue_unique_slug_per_user",
            ),
            models.UniqueConstraint(
                fields=["user", "name"],
                name="true_north_corevalue_unique_name_per_user",
            ),
        ]


class GoalStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    ACTIVE = "active", "Active"
    PAUSED = "paused", "Paused"
    DONE = "done", "Done"
    ARCHIVED = "archived", "Archived"


class Goal(UserOwnedBase, OrderableMixin):
    """
    A user-owned goal. A goal may optionally be linked to a CoreValue.

    Why optional?
    - Allows "draft goals" to be created first, then later either:
      - assigned to a CoreValue, or
      - archived/deleted if not relevant.
    """

    value = models.ForeignKey(
        CoreValue,
        on_delete=models.SET_NULL,
        related_name="goals",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, help_text="Auto from title.")
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=GoalStatus.choices,
        default=GoalStatus.ACTIVE,
    )

    start_date = models.DateField(blank=True, null=True)
    target_date = models.DateField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    def clean(self):
        # If a CoreValue is set, it must belong to the same user.
        if self.value_id and self.user_id and self.value.user_id != self.user_id:
            raise ValidationError({"value": "CoreValue belongs to a different user."})

    def save(self, *args, **kwargs):
        # If user not set, but value is set, infer user from value.
        if self.value_id and not self.user_id:
            self.user = self.value.user

        if not self.slug:
            self.slug = slugify(self.title)[: self._meta.get_field("slug").max_length]

        # NOTE: This makes duplicates raise ValidationError (not IntegrityError)
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order", "title"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "slug"],
                name="true_north_goal_unique_slug_per_user",
            ),
        ]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["user", "value"]),
        ]


class Milestone(UserOwnedBase, OrderableMixin):
    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        related_name="milestones",
    )
    description = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, help_text="Auto from description.")

    notes = models.TextField(blank=True)
    due_date = models.DateField(blank=True, null=True)

    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    order = models.PositiveIntegerField(default=0)

    def clean(self):
        if self.goal_id and self.user_id and self.goal.user_id != self.user_id:
            raise ValidationError({"goal": "Goal belongs to a different user."})

    def save(self, *args, **kwargs):
        if self.goal_id and not self.user_id:
            self.user = self.goal.user

        if not self.slug:
            self.slug = slugify(self.description)[
                : self._meta.get_field("slug").max_length
            ]

        # NOTE: This makes duplicates raise ValidationError (not IntegrityError)
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.goal}: {self.description}"

    class Meta:
        ordering = ["order", "description"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "goal", "slug"],
                name="true_north_milestone_unique_slug_per_goal_per_user",
            ),
        ]
        indexes = [
            models.Index(fields=["user", "goal"]),
            models.Index(fields=["user", "is_completed"]),
        ]


class ValueActionStatus(models.TextChoices):
    TODO = "todo", "To do"
    DOING = "doing", "In progress"
    DONE = "done", "Done"
    SKIPPED = "skipped", "Skipped"


class ValueAction(UserOwnedBase, OrderableMixin):
    milestone = models.ForeignKey(
        Milestone,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    content = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=ValueActionStatus.choices,
        default=ValueActionStatus.TODO,
    )

    due_date = models.DateField(blank=True, null=True)

    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    order = models.PositiveIntegerField(default=0)

    def clean(self):
        if (
            self.milestone_id
            and self.user_id
            and self.milestone.user_id != self.user_id
        ):
            raise ValidationError(
                {"milestone": "Milestone belongs to a different user."}
            )

    def save(self, *args, **kwargs):
        if self.milestone_id and not self.user_id:
            self.user = self.milestone.user

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        short = (self.content or "").strip().replace("\n", " ")
        return short[:60] + ("…" if len(short) > 60 else "")

    class Meta:
        ordering = ["order", "id"]
        indexes = [
            models.Index(fields=["user", "milestone"]),
            models.Index(fields=["user", "status"]),
            models.Index(fields=["user", "is_completed"]),
        ]


class CoreValueEmailSchedule(CreatedUpdatedBase):
    """
    A recurring email schedule that reminds a user of one of their CoreValues.

    The user picks a CoreValue, an optional specific time of day (``send_time``),
    and optional days of the week (``days_of_week``).  When ``days_of_week`` is
    populated the schedule fires on those weekdays at ``send_time`` (ignoring
    ``frequency``).  When only ``send_time`` is set, ``frequency`` controls the
    interval but the email is sent at the specified time of day.  When neither
    is set the original frequency-based behaviour is used.

    The Celery periodic task ``process_due_corevalue_reminders`` dispatches
    ``send_corevalue_reminder_email`` whenever ``next_send`` is in the past.
    """

    TWICE_DAILY = "twice_daily"
    DAILY = "daily"
    THREE_PER_WEEK = "three_per_week"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"

    FREQUENCY_CHOICES = [
        (TWICE_DAILY, "Twice a day (every 12 hours)"),
        (DAILY, "Once a day"),
        (THREE_PER_WEEK, "Three times a week (every 2 days)"),
        (WEEKLY, "Once a week"),
        (BIWEEKLY, "Every two weeks"),
        (MONTHLY, "Once a month"),
    ]

    # Day-of-week constants (compatible with Python's datetime.weekday())
    MON, TUE, WED, THU, FRI, SAT, SUN = 0, 1, 2, 3, 4, 5, 6

    DAYS_OF_WEEK_CHOICES = [
        (str(MON), "Monday"),
        (str(TUE), "Tuesday"),
        (str(WED), "Wednesday"),
        (str(THU), "Thursday"),
        (str(FRI), "Friday"),
        (str(SAT), "Saturday"),
        (str(SUN), "Sunday"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="corevalue_email_schedules",
    )
    core_value = models.ForeignKey(
        CoreValue,
        on_delete=models.CASCADE,
        related_name="email_schedules",
    )
    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default=DAILY,
        help_text=(
            "How often to receive a reminder (used when no specific days are chosen)."
        ),
    )
    send_time = models.TimeField(
        null=True,
        blank=True,
        help_text=(
            "Time of day to receive the reminder (e.g. 09:00). "
            "Leave blank to use the current time when the schedule is created."
        ),
    )
    days_of_week = models.CharField(
        max_length=20,
        blank=True,
        default="",
        help_text=(
            "Comma-separated weekday numbers (0=Mon … 6=Sun) on which to send "
            "reminders.  When set, overrides the Frequency field."
        ),
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to pause this reminder without deleting it.",
    )
    next_send = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the next reminder email will be sent.",
    )
    last_sent = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the most recent reminder email was sent.",
    )

    def clean(self):
        if self.core_value_id and self.user_id:
            if self.core_value.user_id != self.user_id:
                raise ValidationError(
                    {"core_value": "This Core Value belongs to a different user."}
                )
        # Validate days_of_week contents
        if self.days_of_week:
            valid = {str(i) for i in range(7)}
            parts = [p.strip() for p in self.days_of_week.split(",") if p.strip()]
            invalid = [p for p in parts if p not in valid]
            if invalid:
                raise ValidationError(
                    {
                        "days_of_week": (
                            "Invalid day values: %(values)s. "
                            "Use 0 (Monday) through 6 (Sunday)."
                        ),
                    },
                    params={"values": ", ".join(invalid)},
                )

    def get_days_of_week_list(self):
        """Return a list of integer weekday numbers from ``days_of_week``."""
        if not self.days_of_week:
            return []
        return [
            int(d.strip())
            for d in self.days_of_week.split(",")
            if d.strip().isdigit()
        ]

    def compute_next_send(self):
        """Return the datetime of the next reminder send.

        Priority:
        1. If ``days_of_week`` is set – find the next matching weekday at
           ``send_time`` (defaulting to 09:00 when ``send_time`` is blank).
        2. If only ``send_time`` is set – apply the ``frequency`` interval but
           anchor the time component to ``send_time``.
        3. Otherwise – original frequency-based behaviour (add a fixed delta
           to *now*).
        """
        now = timezone.now()
        days = self.get_days_of_week_list()

        if days:
            # Days-of-week mode: fire at send_time on the specified weekdays.
            target_time = self.send_time or _time(9, 0)
            tz = timezone.get_current_timezone()

            # Check today and the following 7 days (8 candidates total) to find
            # the next slot that is still in the future.
            for offset in range(8):
                candidate_date = now.date() + timedelta(days=offset)
                if candidate_date.weekday() in days:
                    candidate_dt = timezone.make_aware(
                        _dt.combine(candidate_date, target_time), tz
                    )
                    if candidate_dt > now:
                        return candidate_dt

            # Fallback – should not happen with a valid days list.
            return now + timedelta(days=7)

        # Frequency-based interval delta map (used by both remaining branches).
        delta_map = {
            self.TWICE_DAILY: timedelta(hours=12),
            self.DAILY: timedelta(days=1),
            self.THREE_PER_WEEK: timedelta(days=2),
            self.WEEKLY: timedelta(weeks=1),
            self.BIWEEKLY: timedelta(weeks=2),
            self.MONTHLY: timedelta(days=30),
        }
        delta = delta_map.get(self.frequency, timedelta(days=1))

        if self.send_time:
            # Frequency + specific time: first check if today's send_time is
            # still in the future; if so return it.  Otherwise advance by one
            # full interval and anchor to send_time on that date.
            tz = timezone.get_current_timezone()
            now_local = now.astimezone(tz)
            candidate_today = timezone.make_aware(
                _dt.combine(now_local.date(), self.send_time), tz
            )
            if candidate_today > now:
                return candidate_today

            next_raw = now + delta
            next_local = next_raw.astimezone(tz)
            next_dt = timezone.make_aware(
                _dt.combine(next_local.date(), self.send_time), tz
            )
            # Guard: if pinning to send_time pushed us back into the past,
            # advance by one more interval.
            if next_dt <= now:
                next_dt += delta
            return next_dt

        # Original behaviour: add a fixed delta to now.
        return now + delta

    def get_subject(self):
        site_name = getattr(settings, "THE_SITE_NAME", "Personal Assistant")
        return f"{site_name} — Core Value Reminder: {self.core_value.name}"

    def get_content(self):
        cv = self.core_value
        return (
            f"Core Value: {cv.name}\n\n"
            f"Definition: {cv.definition or 'N/A'}\n"
            f"Active: {cv.is_active}\n"
        )

    def get_absolute_url(self):
        return reverse(
            "true_north:corevalue-email-schedule-list"
        )

    def __str__(self):
        return (
            f"{self.get_frequency_display()} reminder for "
            f'"{self.core_value.name}" ({self.user})'
        )

    class Meta:
        verbose_name = "Core Value Email Schedule"
        verbose_name_plural = "Core Value Email Schedules"
        ordering = ("-created",)
