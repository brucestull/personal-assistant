from django.db import models
from base.models import CreatedUpdatedBase

from config.settings import AUTH_USER_MODEL


class Pharmaceutical(CreatedUpdatedBase):
    """
    Model for a user's pharmaceutical.
    """

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name="User",
        help_text="Select the user that the pharmaceutical belongs to.",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name="Pharmaceutical Name",
        help_text="Enter the name of the pharmaceutical.",
        max_length=200,
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="Enter a description of the pharmaceutical.",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        verbose_name="Is Active?",
        help_text="Designates if this pharmaceutical is currently active.",
        default=True,
    )
    prescription_required = models.BooleanField(
        verbose_name="Prescription Required?",
        help_text="Designates if this pharmaceutical requires a prescription.",
        default=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Pharmaceutical"
        verbose_name_plural = "Pharmaceuticals"
