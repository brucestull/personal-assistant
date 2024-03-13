from django import forms

from .models import UnimportantNote


class UnimportantNoteForm(forms.ModelForm):
    """
    A form for creating a note.
    """

    class Meta:
        model = UnimportantNote
        fields = ("title", "tag", "content", "url", "main_image")
        # Is the `labals` attribute necessary?
        # labels = {
        #     "title": "Title",
        #     "content": "Content",
        # }
        # Is the `help_texts` attribute necessary?
        # help_texts = {
        #     "title": "The title of this note.",
        #     "content": "The content of this note.",
        # }
        error_messages = {
            "title": {
                "max_length": "This title is too long.",
            },
        }
