from django.db import models

from base.models import CreatedUpdatedBase


class Activity(CreatedUpdatedBase):
    description = models.TextField(
        "Description",
        help_text="A description of the activity.",
    )

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        ordering = ["-created"]
