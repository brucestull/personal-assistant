from django import forms

from .models import BehavioralInterviewQuestion, BulletPoint, Skill


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


class BulletPointForm(forms.ModelForm):
    """
    Form for the `BulletPoint` model.
    """

    class Meta:
        model = BulletPoint
        fields = [
            # "user",
            "text",
        ]
