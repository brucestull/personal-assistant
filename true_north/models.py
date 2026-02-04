# true_north/models.py

from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
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
    value = models.ForeignKey(
        CoreValue,
        on_delete=models.CASCADE,
        related_name="goals",
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
        # Prevent cross-user linking (Goal.user must match CoreValue.user)
        if self.value_id and self.user_id and self.value.user_id != self.user_id:
            raise ValidationError({"value": "CoreValue belongs to a different user."})

    def save(self, *args, **kwargs):
        # Sync ownership down the chain by default
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


class TaskStatus(models.TextChoices):
    TODO = "todo", "To do"
    DOING = "doing", "In progress"
    DONE = "done", "Done"
    SKIPPED = "skipped", "Skipped"


class Task(UserOwnedBase, OrderableMixin):
    milestone = models.ForeignKey(
        Milestone,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    content = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
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
