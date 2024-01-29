from base.models import Note


class UnimportantNote(Note):
    """
    Model for `UnimportantNote`.
    """

    class Meta:
        # Other `Meta` options are inherited from `Note`.
        verbose_name = "Unimportant Note"
        verbose_name_plural = "Unimportant Notes"
        ordering = ("-created",)
