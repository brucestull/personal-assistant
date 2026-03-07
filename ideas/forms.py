# ideas/forms.py

from django import forms

from .models import Idea


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ["name", "concept"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Name of your idea",
                }
            ),
            "concept": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Describe your idea...",
                    "rows": 5,
                }
            ),
        }
