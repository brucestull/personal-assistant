# true_north/models.py

from __future__ import annotations

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

    The user picks a CoreValue and a frequency; the Celery periodic task
    ``process_due_corevalue_reminders`` dispatches
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
        help_text="How often to receive a reminder email for this Core Value.",
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

    def compute_next_send(self):
        """Return the datetime of the next send based on frequency."""
        from datetime import timedelta

        now = timezone.now()
        delta_map = {
            self.TWICE_DAILY: timedelta(hours=12),
            self.DAILY: timedelta(days=1),
            self.THREE_PER_WEEK: timedelta(days=2),
            self.WEEKLY: timedelta(weeks=1),
            self.BIWEEKLY: timedelta(weeks=2),
            self.MONTHLY: timedelta(days=30),
        }
        return now + delta_map.get(self.frequency, timedelta(days=1))

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
