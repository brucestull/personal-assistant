from django.db import models

from base.models import CreatedUpdatedBase
from config.settings import AUTH_USER_MODEL


class Note(CreatedUpdatedBase):
    """
    A note.
    """

    title = models.CharField(
        "Title",
        max_length=255,
        help_text="The title of this note.",
    )
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notes",
    )
    content = models.TextField(
        "Content",
        help_text="The content of this note.",
    )

    def display_content(self):
        """
        This function returns a truncated version of the note's content.
        This can be used in the admin panel and other places where the full
        content is not needed.
        """
        return self.content[:50] + ("..." if len(self.content) > 50 else "")

    def __str__(self):
        return f"{self.title}\n{self.content}"

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        ordering = ("-created",)
