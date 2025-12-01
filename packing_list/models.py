# packing_list/models.py

from django.conf import settings
from django.db import models
from django.urls import reverse


class Activity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="packing_activities",
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("packing_list:activity_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"


class ActivityEntry(models.Model):
    """
    Abstract base model for entries associated with an Activity.
    Provides common fields for both Item (packing) and Task models.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name="%(class)ss"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="packing_%(class)ss",
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ["activity", "name"]


class Item(ActivityEntry):
    """
    An item to be packed for an activity.
    Inherits common fields from ActivityEntry.
    """

    quantity = models.PositiveIntegerField(default=1)
    is_packed = models.BooleanField(default=False)
    is_essential = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("packing_list:item_detail", kwargs={"pk": self.pk})

    class Meta(ActivityEntry.Meta):
        verbose_name = "Item"
        verbose_name_plural = "Items"


class Task(ActivityEntry):
    """
    A task to be completed for an activity.
    Inherits common fields from ActivityEntry.
    """

    is_completed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("packing_list:task_detail", kwargs={"pk": self.pk})

    class Meta(ActivityEntry.Meta):
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
