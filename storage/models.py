# storage/models.py

from django.db import models
from base.models import CreatedUpdatedBase


class Type(CreatedUpdatedBase):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse

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
        from django.urls import reverse

        return reverse("storage:storagearea_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["name"]
        verbose_name = "Storage Area"
        verbose_name_plural = "Storage Areas"
