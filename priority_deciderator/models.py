import json

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from base.models import CreatedUpdatedBase

User = get_user_model()


class Reminder(CreatedUpdatedBase):
    """
    A reminder that can be scheduled to be sent to a user via email.
    """

    name = models.CharField(
        max_length=255,
        help_text="Name of the reminder",
        verbose_name="Reminder Name",
    )
    description = models.TextField(
        help_text="Detailed description of the reminder",
        verbose_name="Description",
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reminders",
        help_text="User who owns this reminder",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this reminder is active",
        verbose_name="Active",
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "Reminder"
        verbose_name_plural = "Reminders"

    def __str__(self):
        return f"{self.name} - {self.user.username}"

    def get_absolute_url(self):
        return reverse("priority_deciderator:reminder_detail", kwargs={"pk": self.pk})


class ReminderSchedule(CreatedUpdatedBase):
    """
    Schedule for when a reminder should be sent.
    Links to django-celery-beat's PeriodicTask for actual scheduling.
    """

    FREQUENCY_CHOICES = [
        ("once", "Once"),
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("custom", "Custom"),
    ]

    reminder = models.ForeignKey(
        Reminder,
        on_delete=models.CASCADE,
        related_name="schedules",
        help_text="Reminder to send",
    )
    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default="daily",
        help_text="How often to send the reminder",
    )
    time = models.TimeField(
        help_text="Time of day to send the reminder",
        verbose_name="Time",
    )
    day_of_week = models.IntegerField(
        null=True,
        blank=True,
        choices=[
            (0, "Monday"),
            (1, "Tuesday"),
            (2, "Wednesday"),
            (3, "Thursday"),
            (4, "Friday"),
            (5, "Saturday"),
            (6, "Sunday"),
        ],
        help_text="Day of week (for weekly frequency)",
    )
    day_of_month = models.IntegerField(
        null=True,
        blank=True,
        help_text="Day of month (1-31, for monthly frequency)",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this schedule is active",
        verbose_name="Active",
    )
    periodic_task = models.OneToOneField(
        PeriodicTask,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reminder_schedule",
        help_text="Associated Celery Beat periodic task",
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "Reminder Schedule"
        verbose_name_plural = "Reminder Schedules"

    def __str__(self):
        return f"{self.reminder.name} - {self.get_frequency_display()} at {self.time}"

    def save(self, *args, **kwargs):
        """
        Override save to create/update the periodic task in django-celery-beat.
        """
        super().save(*args, **kwargs)

        # Only create/update periodic task if schedule is active
        if self.is_active and self.reminder.is_active:
            self._update_periodic_task()
        elif self.periodic_task:
            # Disable the periodic task if schedule or reminder is inactive
            self.periodic_task.enabled = False
            self.periodic_task.save()

    def _update_periodic_task(self):
        """
        Create or update the django-celery-beat PeriodicTask for this schedule.
        """
        # Create crontab schedule based on frequency
        crontab = self._get_crontab_schedule()

        # Create or update periodic task
        task_name = f"reminder_{self.reminder.id}_schedule_{self.id}"

        if self.periodic_task:
            # Update existing task
            self.periodic_task.name = task_name
            self.periodic_task.crontab = crontab
            self.periodic_task.enabled = self.is_active and self.reminder.is_active
            self.periodic_task.kwargs = json.dumps(
                {
                    "reminder_id": self.reminder.id,
                    "schedule_id": self.id,
                }
            )
            self.periodic_task.save()
        else:
            # Create new task
            self.periodic_task = PeriodicTask.objects.create(
                name=task_name,
                task="priority_deciderator.tasks.send_reminder_email",
                crontab=crontab,
                enabled=self.is_active and self.reminder.is_active,
                kwargs=json.dumps(
                    {
                        "reminder_id": self.reminder.id,
                        "schedule_id": self.id,
                    }
                ),
            )
            # Save again to update the foreign key
            super().save(update_fields=["periodic_task"])

    def _get_crontab_schedule(self):
        """
        Create or get a CrontabSchedule based on this schedule's settings.
        """
        hour = self.time.hour
        minute = self.time.minute

        if self.frequency == "daily":
            crontab, _ = CrontabSchedule.objects.get_or_create(
                minute=str(minute),
                hour=str(hour),
                day_of_week="*",
                day_of_month="*",
                month_of_year="*",
            )
        elif self.frequency == "weekly":
            day = str(self.day_of_week) if self.day_of_week is not None else "0"
            crontab, _ = CrontabSchedule.objects.get_or_create(
                minute=str(minute),
                hour=str(hour),
                day_of_week=day,
                day_of_month="*",
                month_of_year="*",
            )
        elif self.frequency == "monthly":
            day = str(self.day_of_month) if self.day_of_month else "1"
            crontab, _ = CrontabSchedule.objects.get_or_create(
                minute=str(minute),
                hour=str(hour),
                day_of_week="*",
                day_of_month=day,
                month_of_year="*",
            )
        else:  # once or custom - default to daily
            crontab, _ = CrontabSchedule.objects.get_or_create(
                minute=str(minute),
                hour=str(hour),
                day_of_week="*",
                day_of_month="*",
                month_of_year="*",
            )

        return crontab

    def delete(self, *args, **kwargs):
        """
        Override delete to also delete the associated periodic task.
        """
        if self.periodic_task:
            self.periodic_task.delete()
        super().delete(*args, **kwargs)
