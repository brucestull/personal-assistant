from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from base.models import CreatedUpdatedBase


class Thing(CreatedUpdatedBase):
    """
    A Thing belongs to a User. Stores a named item with content and a type label.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="things",
        verbose_name="User",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Name",
        help_text="A short name for this thing.",
    )
    content = models.TextField(
        verbose_name="Content",
        help_text="The main content or description of this thing.",
    )
    type = models.CharField(
        max_length=100,
        verbose_name="Type",
        help_text="A label for the type or category of this thing.",
    )

    def get_absolute_url(self):
        return reverse("thing_thought_reminder:thing-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.name} ({self.type})"

    class Meta:
        verbose_name = "Thing"
        verbose_name_plural = "Things"
        ordering = ("-created",)


class Thought(CreatedUpdatedBase):
    """
    A Thought belongs to a User. Stores a named thought with content and a realm label.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ttr_thoughts",
        verbose_name="User",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Name",
        help_text="A short name for this thought.",
    )
    content = models.TextField(
        verbose_name="Content",
        help_text="The main content of this thought.",
    )
    realm = models.CharField(
        max_length=100,
        verbose_name="Realm",
        help_text="A label for the realm or category of this thought.",
    )

    def get_absolute_url(self):
        return reverse("thing_thought_reminder:thought-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.name} ({self.realm})"

    class Meta:
        verbose_name = "Thought"
        verbose_name_plural = "Thoughts"
        ordering = ("-created",)


class ReminderSchedule(CreatedUpdatedBase):
    """
    A ReminderSchedule belongs to a User and references either a Thing or a Thought.
    It represents a routine email reminder that the user wants to receive.
    """

    FREQUENCY_DAILY = "daily"
    FREQUENCY_WEEKLY = "weekly"
    FREQUENCY_MONTHLY = "monthly"

    FREQUENCY_CHOICES = [
        (FREQUENCY_DAILY, "Daily"),
        (FREQUENCY_WEEKLY, "Weekly"),
        (FREQUENCY_MONTHLY, "Monthly"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reminder_schedules",
        verbose_name="User",
    )
    thing = models.ForeignKey(
        Thing,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reminder_schedules",
        verbose_name="Thing",
    )
    thought = models.ForeignKey(
        Thought,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reminder_schedules",
        verbose_name="Thought",
    )
    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default=FREQUENCY_DAILY,
        verbose_name="Frequency",
        help_text="How often to send this reminder.",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Whether this reminder schedule is currently active.",
    )
    next_send = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Next Send",
        help_text="When the next reminder will be sent.",
    )
    last_sent = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Last Sent",
        help_text="When the last reminder was sent.",
    )

    def clean(self):
        if not self.thing and not self.thought:
            raise ValidationError(
                "A reminder schedule must reference either a Thing or a Thought."
            )
        if self.thing and self.thought:
            raise ValidationError(
                "A reminder schedule can reference either a Thing or a Thought,"
                " not both."
            )

    def get_subject(self):
        """Return the email subject for this reminder."""
        from django.conf import settings as django_settings

        site_name = getattr(django_settings, "THE_SITE_NAME", "Personal Assistant")
        if self.thing:
            return f"{site_name} — Thing Reminder: {self.thing.name}"
        if self.thought:
            return f"{site_name} — Thought Reminder: {self.thought.name}"
        return f"{site_name} — Reminder"

    def get_content(self):
        """Return the email body content for this reminder."""
        if self.thing:
            return (
                f"Thing: {self.thing.name}\n"
                f"Type: {self.thing.type}\n\n"
                f"{self.thing.content}"
            )
        if self.thought:
            return (
                f"Thought: {self.thought.name}\n"
                f"Realm: {self.thought.realm}\n\n"
                f"{self.thought.content}"
            )
        return ""

    def compute_next_send(self):
        """Compute and return the next send time based on frequency."""
        from datetime import timedelta

        now = timezone.now()
        if self.frequency == self.FREQUENCY_DAILY:
            return now + timedelta(days=1)
        elif self.frequency == self.FREQUENCY_WEEKLY:
            return now + timedelta(weeks=1)
        elif self.frequency == self.FREQUENCY_MONTHLY:
            return now + timedelta(days=30)
        return now + timedelta(days=1)

    def get_absolute_url(self):
        return reverse(
            "thing_thought_reminder:reminder-detail", kwargs={"pk": self.pk}
        )

    def __str__(self):
        target = self.thing or self.thought
        return f"{self.frequency.capitalize()} reminder for {target} ({self.user})"

    class Meta:
        verbose_name = "Reminder Schedule"
        verbose_name_plural = "Reminder Schedules"
        ordering = ("-created",)
