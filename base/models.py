from django.db import models


class CreatedUpdatedBase(models.Model):
    """
    An abstract base class model that provides self-updating `created` and
    `updated` fields.
    """

    created = models.DateTimeField(
        "Created",
        auto_now_add=True,
        help_text="The date and time this object was created.",
    )
    updated = models.DateTimeField(
        "Updated",
        auto_now=True,
        help_text="The date and time this object was last updated.",
    )

    class Meta:
        abstract = True
