from base.models import Note


class UnimportantNote(Note):
    """
    Model for `UnimportantNote`.
    """

    class Meta:
        # These `Meta` options are used to configure the behavior of this child model.
        verbose_name = "Unimportant Note"
        verbose_name_plural = "Unimportant Notes"
        ordering = ("-created",)
