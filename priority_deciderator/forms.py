from django import forms
from .models import Reminder, ReminderSchedule


class ReminderForm(forms.ModelForm):
    """Form for creating and editing Reminders."""
    
    class Meta:
        model = Reminder
        fields = ["name", "description", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ReminderScheduleForm(forms.ModelForm):
    """Form for creating and editing Reminder Schedules."""
    
    class Meta:
        model = ReminderSchedule
        fields = ["frequency", "time", "day_of_week", "day_of_month", "is_active"]
        widgets = {
            "frequency": forms.Select(attrs={"class": "form-control"}),
            "time": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"},
                format="%H:%M",
            ),
            "day_of_week": forms.Select(attrs={"class": "form-control"}),
            "day_of_month": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 31}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make day fields optional by default
        self.fields["day_of_week"].required = False
        self.fields["day_of_month"].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        frequency = cleaned_data.get("frequency")
        day_of_week = cleaned_data.get("day_of_week")
        day_of_month = cleaned_data.get("day_of_month")
        
        # Validate that weekly schedules have day_of_week
        if frequency == "weekly" and day_of_week is None:
            self.add_error("day_of_week", "Day of week is required for weekly reminders")
        
        # Validate that monthly schedules have day_of_month
        if frequency == "monthly" and not day_of_month:
            self.add_error("day_of_month", "Day of month is required for monthly reminders")
        
        return cleaned_data
