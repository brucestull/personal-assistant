from django import forms

from .models import Thought

_FORM_CONTROL_WIDGETS = (
    forms.TextInput,
    forms.Textarea,
    forms.Select,
)


def _add_bootstrap_classes(form):
    for field in form.fields.values():
        widget = field.widget
        if isinstance(widget, forms.CheckboxInput):
            widget.attrs.setdefault("class", "form-check-input")
        elif isinstance(widget, _FORM_CONTROL_WIDGETS):
            widget.attrs.setdefault("class", "form-control")


class ThoughtForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _add_bootstrap_classes(self)

    class Meta:
        model = Thought
        fields = ["text"]
