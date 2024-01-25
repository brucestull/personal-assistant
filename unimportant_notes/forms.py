from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    """
    A form for creating a note.
    """

    class Meta:
        model = Note
        fields = ("title", "content")
        labels = {
            "title": "Title",
            "content": "Content",
        }
        help_texts = {
            "title": "The title of this note.",
            "content": "The content of this note.",
        }
        error_messages = {
            "title": {
                "max_length": "This title is too long.",
            },
        }
