# ideas/models.py

from django.db import models
from django.urls import reverse

from base.models import CreatedUpdatedBase
from config.settings import AUTH_USER_MODEL


class Idea(CreatedUpdatedBase):
    """
    Model for an `Idea`.
    """

    name = models.CharField(
        "Name",
        max_length=255,
        help_text="The name of this idea.",
    )
    concept = models.TextField(
        "Concept",
        help_text="The concept or description of this idea.",
    )
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name="Author",
        help_text="The author of this idea.",
        on_delete=models.CASCADE,
        related_name="ideas",
    )

    def get_absolute_url(self):
        return reverse("ideas:idea_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Idea"
        verbose_name_plural = "Ideas"
        ordering = ("name",)
