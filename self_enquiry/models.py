from django.db import models
from django.urls import reverse

from config.settings import AUTH_USER_MODEL
from base.models import CreatedUpdatedBase


class Journal(CreatedUpdatedBase):
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
        verbose_name="Journal Title",
        help_text="Optional - 100 characters or fewer",
        max_length=100,
        null=True,
        blank=True,
    )
    content = models.TextField(
        verbose_name="Journal Content",
        help_text="Required",
    )

    def __str__(self):
        return (
            f"{self.author.username} : {self.pk}"
            f"{' - ' + self.title[:24] if self.title else ''}"
        )

    def get_absolute_url(self):
        """
        This function returns the absolute URL for a journal. It is used for
        the view which needs to be redirected to after a journal is created or
        updated.
        """
        return reverse("self_enquiry:detail", args=[str(self.pk)])

    def display_content(self):
        """
        This function returns a truncated version of the journal's content.
        This can be used in the admin panel and other places where the full
        content is not needed.
        """
        return self.content[:50] + ("..." if len(self.content) > 50 else "")


class GrowthOpportunity(CreatedUpdatedBase):
    """
    The `GrowthOpportunity` model represents a growth opportunity or
    question that a user is interested in pursuing.

    Attributes:
        author (ForeignKey): The user that owns the growth opportunity.
        question (TextField): The question or growth opportunity.
        created (DateTimeField): The date and time the growth opportunity was
        created.
        updated (DateTimeField): The date and time the growth opportunity was
        last updated.
    """

    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="growth_opportunities",
    )
    question = models.TextField(
        verbose_name="Question",
        help_text="Required",
    )

    def __str__(self):
        return self.question[:24] + ("..." if len(self.question) > 24 else "")

    class Meta:
        verbose_name = "Growth Opportunity"
        verbose_name_plural = "Growth Opportunities"
