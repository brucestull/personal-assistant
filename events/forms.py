# events/forms.py

from django import forms

from events.models import CalendarEvent


class EventForm(forms.ModelForm):
    """
    Form for creating a calendar event.
    Only exposes the fields required for a minimal Google Calendar event:
    summary (title), start_datetime, and end_datetime.
    """

    class Meta:
        model = CalendarEvent
        fields = ["summary", "start_datetime", "end_datetime"]
        widgets = {
            "start_datetime": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_datetime": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_datetime"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["end_datetime"].input_formats = ["%Y-%m-%dT%H:%M"]
