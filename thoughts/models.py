# thoughts/models.py

from django.conf import settings
from django.db import models
from django.urls import reverse

from base.models import CreatedUpdatedBase


class Thought(CreatedUpdatedBase):
    """
    A Thought belongs to a User. Stores the user's thought text.
    """

    text = models.TextField(
        "Thought",
        help_text="Your thought.",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="thoughts",
        verbose_name="User",
        help_text="The user who created this thought.",
    )

    def get_absolute_url(self):
        return reverse("thoughts:thought-update", kwargs={"pk": self.pk})

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = "Thought"
        verbose_name_plural = "Thoughts"
        ordering = ("-created",)
