# packing_list/models.py

from django.conf import settings
from django.db import models


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

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    is_packed = models.BooleanField(default=False)
    is_essential = models.BooleanField(default=False)
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name="packing_items"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="packing_items"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ["activity", "name"]
