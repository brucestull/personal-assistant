from django import forms

from .models import CognitiveDistortion, Thought


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


class ThoughtForm(forms.ModelForm):
    """
    Form for the `Thought` model.
    """

    class Meta:
        model = Thought
        fields = [
            # "user",
            "name",
            "description",
            "cognitive_distortion",
        ]
        optional_fields = [
            "cognitive_distortion",
        ]
