from django import forms

from .models import CognativeDistortion


class CognativeDistortionForm(forms.ModelForm):
    """
    Form for the `CognativeDistortion` model.
    """

    class Meta:
        model = CognativeDistortion
        fields = [
            # "user",
            "name",
            "description",
        ]
