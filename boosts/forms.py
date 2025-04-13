from django import forms
from django.forms import ModelForm

from boosts.models import Inspirational


class InspirationalForm(ModelForm):
    """
    ModelForm for the Inspirational model. This form uses bootstrap.
    """
    class Meta:
        model = Inspirational
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "What's your inspiration for today?",
                    "rows": 3,
                }
            )
        }
        labels = {
            "body": "Inspirational Statement",
        }
