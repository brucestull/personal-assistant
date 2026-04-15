# true_north/forms.py

from django import forms

from true_north.models import CoreValue, CoreValueEmailSchedule, Goal, Milestone, ValueAction  # noqa E501

_FORM_CONTROL_WIDGETS = (
    forms.TextInput,
    forms.Textarea,
    forms.Select,
    forms.DateInput,
    forms.NumberInput,
)

MINUTE_CHOICES = [(str(i), f":{i:02d}") for i in range(0, 60, 5)]
HOUR_CHOICES = [(str(i), f"{i:02d}:00") for i in range(0, 24)]
DOW_CHOICES = [
    ("*", "Every day"),
    ("1", "Monday"),
    ("2", "Tuesday"),
    ("3", "Wednesday"),
    ("4", "Thursday"),
    ("5", "Friday"),
    ("6", "Saturday"),
    ("0", "Sunday"),
]


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


class CoreValueEmailScheduleForm(forms.ModelForm):
    """Form for creating/editing a CoreValueEmailSchedule."""

    # Override days_of_week so we can render it as a checkbox list instead of
    # a plain text input.
    days_of_week = forms.MultipleChoiceField(
        choices=CoreValueEmailSchedule.DAYS_OF_WEEK_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text=(
            "Select one or more days on which to receive reminders. "
            "When days are selected the Frequency field is ignored and "
            "the email is sent at the chosen Time of day instead."
        ),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["core_value"].queryset = CoreValue.objects.filter(
                user=user, is_active=True
            ).order_by("order", "name")
        else:
            self.fields["core_value"].queryset = CoreValue.objects.none()

        # Pre-populate the checkbox list from the stored comma-separated string.
        if self.instance and self.instance.days_of_week:
            self.initial["days_of_week"] = [
                d.strip()
                for d in self.instance.days_of_week.split(",")
                if d.strip()
            ]

        _add_bootstrap_classes(self)
        # CheckboxSelectMultiple doesn't need form-control class.
        self.fields["days_of_week"].widget.attrs.pop("class", None)

    def clean_days_of_week(self):
        """Convert the selected list back to a comma-separated string."""
        days = self.cleaned_data.get("days_of_week") or []
        # Sort numerically for canonical storage order (Mon → Sun).
        return ",".join(sorted(days, key=int))

    class Meta:
        model = CoreValueEmailSchedule
        fields = ["core_value", "frequency", "send_time", "days_of_week", "is_active"]
        widgets = {
            "send_time": forms.TimeInput(attrs={"type": "time"}),
        }


class ObjectEmailScheduleForm(forms.Form):
    hour = forms.ChoiceField(
        choices=HOUR_CHOICES,
        initial="9",
        label="Hour",
        help_text="Eastern time",
    )
    minute = forms.ChoiceField(
        choices=MINUTE_CHOICES,
        initial="0",
        label="Minute",
    )
    day_of_week = forms.ChoiceField(
        choices=DOW_CHOICES,
        initial="*",
        label="Day of week",
    )
    enabled = forms.BooleanField(
        required=False,
        initial=True,
        label="Active",
        help_text="Uncheck to pause without deleting",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _add_bootstrap_classes(self)
