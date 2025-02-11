from django.db import models
from django.urls import reverse

from base.models import Note
from config.settings import AUTH_USER_MODEL


class NoteTag(models.Model):
    """
    A tag for a note.
    """

    name = models.CharField(
        "Name",
        max_length=255,
        help_text="The name of this tag.",
    )
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name="Author",
        help_text="The author of this tag.",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Note Tag"
        verbose_name_plural = "Note Tags"
        ordering = ("name",)


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
    tag = models.ManyToManyField(
        NoteTag,
        verbose_name="Tags",
        help_text="Tags for this note.",
        blank=True,
        related_name="unimportant_notes",
    )

    def display_tags(self):
        """
        Display the tags for this note.
        """
        return ", ".join([tag.name for tag in self.tag.all()])

    def get_absolute_url(self):
        return reverse("unimportant_notes:note_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        # These `Meta` options are used to configure the behavior of this child model.
        verbose_name = "Unimportant Note"
        verbose_name_plural = "Unimportant Notes"
        ordering = ("-created",)
