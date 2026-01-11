"""Models for the successes app.

This app implements Martin Seligman's Positive Psychology principles,
specifically the "What Went Well" (Three Blessings) exercise developed
by Angela Duckworth and others.

The practice involves reflecting on successes and understanding what
contributed to those positive outcomes, helping cultivate autonomy
and recognizing personal agency in creating positive experiences.
"""

from django.db import models

from base.models import CreatedUpdatedBase
from config.settings import AUTH_USER_MODEL


class Success(CreatedUpdatedBase):
    """
    A success or positive event that a user wants to track.

    Can be logged at any time throughout the day. Successes can be
    big or small - the practice is about noticing positive moments.
    """

    text = models.TextField(
        "Success Description",
        help_text="Describe what went well or what you accomplished.",
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="successes",
    )

    class Meta:
        ordering = ["-created"]
        verbose_name_plural = "successes"

    def __str__(self):
        # Return first 50 characters of text
        return (
            f"{self.text[:50]}{'...' if len(self.text) > 50 else ''}"
            f" ({self.created.strftime('%Y-%m-%d')})"
        )


class WhatWentWell(CreatedUpdatedBase):
    """
    A structured reflection on what went well during the day.

    Based on the "What Went Well" (Three Blessings) exercise from
    Positive Psychology. Users are encouraged to identify three things
    each day that went well and reflect on their role in making them happen.

    This practice helps build awareness of personal agency and cultivates
    a growth mindset by recognizing how our thoughts and actions contribute
    to positive outcomes.
    """

    what_went_well = models.TextField(
        "What Went Well",
        help_text="Describe what went well today - big or small.",
    )
    how_i_made_it_happen = models.TextField(
        "How I Made It Happen",
        help_text=(
            "Reflect on what YOU did to make this happen or contribute "
            "to this positive outcome."
        ),
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="what_went_wells",
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "What Went Well"
        verbose_name_plural = "What Went Wells"

    def __str__(self):
        what_text = self.what_went_well[:50]
        ellipsis = "..." if len(self.what_went_well) > 50 else ""
        date_str = self.created.strftime("%Y-%m-%d")
        return f"{what_text}{ellipsis} ({date_str})"
