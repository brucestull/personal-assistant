# storage/models.py

from django.db import models
from django.contrib.auth import get_user_model

from base.models import CreatedUpdatedBase
from django.urls import reverse


class Type(CreatedUpdatedBase):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("storage:type_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["name"]
        verbose_name = "Type"
        verbose_name_plural = "Types"


class StorageArea(CreatedUpdatedBase):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.ForeignKey(
        Type, on_delete=models.CASCADE, related_name="storage_areas"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("storage:storagearea_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["name"]
        verbose_name = "Storage Area"
        verbose_name_plural = "Storage Areas"


class SortDecision(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:50]  # Short preview for admin/listing

    def get_absolute_url(self):
        return reverse("storage:sortdecision_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["id"]
        verbose_name = "Sort Decision"
        verbose_name_plural = "Sort Decisions"


class Item(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="storage_items"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("storage:item_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["name"]
        verbose_name = "Item"
        verbose_name_plural = "Items"
