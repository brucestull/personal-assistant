from django import forms

from .models import BehavioralInterviewQuestion, Skill


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


class BehavioralInterviewQuestionForm(forms.ModelForm):
    """
    Form for the `BehavioralInterviewQuestion` model.
    """

    class Meta:
        model = BehavioralInterviewQuestion
        fields = [
            # "user",
            "text",
        ]
