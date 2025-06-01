# care_craft/models.py

from django.db import models
from django.urls import reverse

from base.models import CreatedUpdatedBase, Note
from config.settings import AUTH_USER_MODEL


class CareCraftNote(Note):
    """
    A note specifically for care craft concepts.
    Inherits from the base Note model.
    """

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="care_craft_notes",
    )

    def get_absolute_url(self):
        return reverse("care_craft:note_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Care Craft Note"
        verbose_name_plural = "Care Craft Notes"
        ordering = ["-created"]
        # permissions = [
        #     ("view_care_craft_note", "Can view care craft note"),
        #     ("edit_care_craft_note", "Can edit care craft note"),
        # ]


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
