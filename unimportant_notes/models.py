from base.models import Note
from django.db import models


class UnimportantNote(Note):
    """
    Model for `UnimportantNote`.
    """

    main_image = models.ImageField(
        verbose_name="Main Image",
        help_text="Add an image for the note.",
        # `upload_to` is a required argument for `ImageField`.
        # It specifies the path to which the uploaded file will be saved.
        upload_to="unimportant_notes/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        # These `Meta` options are used to configure the behavior of this child model.
        verbose_name = "Unimportant Note"
        verbose_name_plural = "Unimportant Notes"
        ordering = ("-created",)
