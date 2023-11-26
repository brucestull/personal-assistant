from django import forms

from .models import CognitiveDistortion


class CognitiveDistortionForm(forms.ModelForm):
    """
    Form for the `CognitiveDistortion` model.
    """

    class Meta:
        model = CognitiveDistortion
        fields = [
            # "user",
            "name",
            "description",
        ]
