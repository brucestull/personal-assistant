# true_north/forms.py

from django import forms

from true_north.models import CoreValue, Goal, Milestone, ValueAction

_FORM_CONTROL_WIDGETS = (
    forms.TextInput,
    forms.Textarea,
    forms.Select,
    forms.DateInput,
    forms.NumberInput,
)


def _add_bootstrap_classes(form):
    """Add Bootstrap CSS classes to all fields on a form."""
    for field in form.fields.values():
        widget = field.widget
        if isinstance(widget, forms.CheckboxInput):
            widget.attrs.setdefault("class", "form-check-input")
        elif isinstance(widget, _FORM_CONTROL_WIDGETS):
            widget.attrs.setdefault("class", "form-control")


class CoreValueForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _add_bootstrap_classes(self)

    class Meta:
        model = CoreValue
        fields = ["name", "definition", "is_active", "order"]
        widgets = {
            "definition": forms.Textarea(attrs={"rows": 4}),
        }


class GoalForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["value"].queryset = CoreValue.objects.filter(
                user=user, is_active=True
            ).order_by("order", "name")
        else:
            self.fields["value"].queryset = CoreValue.objects.none()
        _add_bootstrap_classes(self)

    class Meta:
        model = Goal
        fields = [
            "value",
            "title",
            "description",
            "status",
            "start_date",
            "target_date",
            "is_active",
            "order",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "target_date": forms.DateInput(attrs={"type": "date"}),
        }


class MilestoneForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["goal"].queryset = Goal.objects.filter(
                user=user, is_active=True
            ).order_by("order", "title")
        else:
            self.fields["goal"].queryset = Goal.objects.none()
        _add_bootstrap_classes(self)

    class Meta:
        model = Milestone
        fields = [
            "goal",
            "description",
            "notes",
            "due_date",
            "is_completed",
            "order",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }


class ValueActionForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["milestone"].queryset = Milestone.objects.filter(
                user=user
            ).order_by("order", "description")
        else:
            self.fields["milestone"].queryset = Milestone.objects.none()
        _add_bootstrap_classes(self)

    class Meta:
        model = ValueAction
        fields = [
            "milestone",
            "content",
            "status",
            "due_date",
            "order",
        ]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }
