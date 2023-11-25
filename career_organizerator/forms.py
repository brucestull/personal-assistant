from django import forms

from .models import (
    BehavioralInterviewQuestion,
    BulletPoint,
    Purpose,
    QuestionResponse,
    Skill,
)


class PurposeForm(forms.ModelForm):
    """
    Form for the `Purpose` model.
    """

    class Meta:
        model = Purpose
        fields = [
            # "user",
            "text",
        ]


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


class QuestionResponseForm(forms.ModelForm):
    """
    Form for the `QuestionResponse` model.
    """

    class Meta:
        model = QuestionResponse
        fields = [
            # "user",
            "question",
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
