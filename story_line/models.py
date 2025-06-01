# story_line/models.py

from django.db import models
from django.urls import reverse

from base.models import Note
from config.settings import AUTH_USER_MODEL


class StoryLineNote(Note):
    """
    A note specifically for Story Line concepts.
    Inherits from the base Note model.
    """

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="story_line_notes",
    )

    def get_absolute_url(self):
        return reverse("story_line:note_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Story Line Note"
        verbose_name_plural = "Story Line Notes"
        ordering = ["-created"]
        # permissions = [
        #     ("view_story_line_note", "Can view story line note"),
        #     ("edit_story_line_note", "Can edit story line note"),
        # ]
