from django.conf import settings
from django.db import models
from django.urls import reverse

from base.models import CreatedUpdatedBase


class Thought(CreatedUpdatedBase):
    text = models.TextField(
        "Thought",
        help_text="Your thought.",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bus_drive_thoughts",
        verbose_name="User",
        help_text="The user who created this thought.",
    )

    def __str__(self):
        return self.text[:50]

    def get_absolute_url(self):
        return reverse("bus_drive:thought-detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("-created",)
        verbose_name = "Thought"
        verbose_name_plural = "Thoughts"
