from django import forms

from .models import Skill


class SkillForm(forms.ModelForm):
    """
    Form for the `Skill` model.
    """

    class Meta:
        model = Skill
        fields = [
            # "user",
            "name",
        ]
