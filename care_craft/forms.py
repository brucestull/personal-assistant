from django import forms

from .models import Activity


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ["description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4, "cols": 40}),
        }
