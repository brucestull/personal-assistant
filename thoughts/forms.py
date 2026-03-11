# thoughts/forms.py

from django import forms

from .models import Thought

_FORM_CONTROL_WIDGETS = (
    forms.TextInput,
    forms.Textarea,
)


def _add_bootstrap_classes(form):
    """Add Bootstrap CSS classes to all fields on a form."""
    for field in form.fields.values():
        widget = field.widget
        if isinstance(widget, _FORM_CONTROL_WIDGETS):
            widget.attrs.setdefault("class", "form-control")


class ThoughtForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _add_bootstrap_classes(self)

    class Meta:
        model = Thought
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4}),
        }
