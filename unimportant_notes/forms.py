from django import forms

from .models import NoteTag, UnimportantNote


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

    def __init__(self, *args, **kwargs):
        # Pop the 'user' argument from the kwargs dictionary.
        # The 'user' needs to be passed when instantiating this form in the view.
        user = kwargs.pop("user", None)
        super(UnimportantNoteForm, self).__init__(*args, **kwargs)

        if user is not None:
            # Filter the queryset for the 'tag' field to only include NoteTags
            # where the current user is the author.
            self.fields["tag"].queryset = NoteTag.objects.filter(author=user)
