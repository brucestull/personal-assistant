# plan_it/models.py

from datetime import date

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class StorageLocation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="storage_locations"
    )
    name = models.CharField(max_length=100)
    parent_location = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="sublocations",
        on_delete=models.CASCADE,
    )

    def get_absolute_url(self):
        return reverse("plan_it:storage_location_list")

    def __str__(self):
        return (
            self.name
            if not self.parent_location
            else f"{self.parent_location} > {self.name}"
        )


class ActivityLocation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="activity_locations"
    )
    name = models.CharField(max_length=100)
    parent_location = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="sublocations",
        on_delete=models.CASCADE,
    )

    def get_absolute_url(self):
        return reverse("plan_it:activity_location_list")

    def __str__(self):
        return (
            self.name
            if not self.parent_location
            else f"{self.parent_location} > {self.name}"
        )

    @property
    def depth(self):
        level = 0
        current = self.parent_location
        while current:
            level += 1
            current = current.parent_location
        return level


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=100)
    storage_location = models.ForeignKey(StorageLocation, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("plan_it:item_list")

    def __str__(self):
        return self.name


class ActivityType(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="plan_it_activity_types"
    )
    name = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse("plan_it:activity_type_list")

    def __str__(self):
        return self.name


class Activity(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="plan_it_activities"
    )
    name = models.CharField(max_length=100)
    type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)
    target_item = models.ForeignKey(
        Item, null=True, blank=True, on_delete=models.CASCADE
    )
    activity_location = models.ForeignKey(
        ActivityLocation, null=True, blank=True, on_delete=models.CASCADE
    )
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    is_recurring = models.BooleanField(default=False)
    last_completed = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse("plan_it:activity_list")

    def __str__(self):
        return f"{self.name}[{self.activity_location}]"

    def due_status(self):
        if not self.due_date:
            return "none"
        today = date.today()
        if self.due_date < today:
            return "overdue"
        elif self.due_date == today:
            return "today"
        else:
            return "upcoming"

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
