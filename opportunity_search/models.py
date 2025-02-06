from django.db import models

from base.models import CreatedUpdatedBase


class WorkSearchActivity(CreatedUpdatedBase):
    """
    Model for `WorkSearchActivity`
    """

    description = models.TextField()

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Work Search Activity"
        verbose_name_plural = "Work Search Activities"
