from django import forms

from .models import Item, StorageLocation

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


class StorageLocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _add_bootstrap_classes(self)

    class Meta:
        model = StorageLocation
        fields = ["name", "type"]


class ItemForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        _add_bootstrap_classes(self)
        if user is not None:
            self.fields["location"].queryset = StorageLocation.objects.filter(
                user=user
            )

    class Meta:
        model = Item
        fields = ["name", "type", "location"]
