# plan_it/models.py

from django.db import models

from django.contrib.auth import get_user_model


class StorageLocation(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="storage_locations",
    )
    name = models.CharField(max_length=100)
    parent_location = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="sublocations",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return (
            self.name
            if not self.parent_location
            else f"{self.parent_location} > {self.name}"
        )


class Item(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="items",
    )
    name = models.CharField(max_length=100)
    storage_location = models.ForeignKey(StorageLocation, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ActivityType(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="plan_it_activity_types",
    )
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Activity(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="plan_it_activities",
    )
    name = models.CharField(max_length=100)
    type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)
    target_item = models.ForeignKey(
        Item, null=True, blank=True, on_delete=models.CASCADE
    )
    target_location = models.ForeignKey(
        StorageLocation, null=True, blank=True, on_delete=models.CASCADE
    )
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    is_recurring = models.BooleanField(default=False)
    last_completed = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        # ordering = ["due_date"]
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
