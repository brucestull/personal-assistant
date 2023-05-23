from django.db import models
from django.urls import reverse

from config.settings.common import AUTH_USER_MODEL


class Journal(models.Model):
    """
    Model for a User's Journal.

    Attributes:
        author (ForeignKey): The user that owns the journal.
        title (CharField): The title of the journal.
        content (TextField): The content of the journal.
        created (DateTimeField): The date and time the journal was created.
    """
    
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="journals",
    )
    title = models.CharField(
        max_length=100,
        help_text="Optional - 100 characters or fewer",
        verbose_name="Journal Title",
        null=True,
        blank=True,
    )
    content = models.TextField(
        help_text="Required",
        verbose_name="Journal Content",
    )
    created = models.DateTimeField(
        help_text="The date and time the journal was created.",
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        help_text="The date and time the journal was last updated.",
        auto_now=True,
    )

    def __str__(self):
        return self.author.username + " : " + str(self.id) + (
            # If title is not `None`, then add it to the string.
            (" - " + self.title[:24]) if self.title else ""
        )

    def get_absolute_url(self):
        return reverse("journal_detail", args=[str(self.id)])
