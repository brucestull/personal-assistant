from django import forms

from .models import ReminderSchedule, Thing, Thought

_FORM_CONTROL_WIDGETS = (
    forms.TextInput,
    forms.Textarea,
    forms.Select,
)


def _add_bootstrap_classes(form):
    """Add Bootstrap CSS classes to all fields on a form."""
    for field in form.fields.values():
        widget = field.widget
        if isinstance(widget, forms.CheckboxInput):
            widget.attrs.setdefault("class", "form-check-input")
        elif isinstance(widget, _FORM_CONTROL_WIDGETS):
            widget.attrs.setdefault("class", "form-control")


class ThingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _add_bootstrap_classes(self)

    class Meta:
        model = Thing
        fields = ["name", "content", "type"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 5}),
        }


class ThoughtForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _add_bootstrap_classes(self)

    class Meta:
        model = Thought
        fields = ["name", "content", "realm"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 5}),
        }


class ReminderScheduleForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        _add_bootstrap_classes(self)
        if user is not None:
            # Limit thing/thought choices to the current user's objects
            self.fields["thing"].queryset = Thing.objects.filter(user=user)
            self.fields["thought"].queryset = Thought.objects.filter(user=user)

    class Meta:
        model = ReminderSchedule
        fields = ["thing", "thought", "frequency", "is_active"]

    def clean(self):
        cleaned_data = super().clean()
        thing = cleaned_data.get("thing")
        thought = cleaned_data.get("thought")
        if not thing and not thought:
            raise forms.ValidationError(
                "Please select either a Thing or a Thought for this reminder."
            )
        if thing and thought:
            raise forms.ValidationError(
                "Please select either a Thing or a Thought, not both."
            )
        return cleaned_data
