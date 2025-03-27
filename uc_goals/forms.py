from django import forms

from .models import Goal


class GoalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        Override the __init__ method to filter the queryset for the parent field. This
        prevents a goal from being its own parent.
        """
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # If updating an existing instance
            self.fields["parent"].queryset = Goal.objects.exclude(pk=self.instance.pk)
            # Set initial values for the M2M field from related objects
            self.fields["character_strengths"].initial = (
                self.instance.character_strengths.all()
            )

    class Meta:
        model = Goal
        fields = [
            "parent",
            "name",
            "is_ultimate_concern",
            "description",
            "due_date",
            "completed",
            "is_archived",
            "character_strengths",  # Include the M2M field in the form
        ]
        labels = {
            "parent": "Parent",
            "name": "Name",
            "is_ultimate_concern": "Is Ultimate Concern",
            "description": "Description",
            "due_date": "Due Date",
            "completed": "Completed",
            "is_archived": "Is Archived",
            "character_strengths": "Character Strengths",
        }
        widgets = {
            "parent": forms.Select(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "is_ultimate_concern": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "style": "resize: both;",
                }
            ),
            "due_date": forms.DateInput(attrs={"class": "form-control"}),
            "completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_archived": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "character_strengths": forms.SelectMultiple(
                attrs={"class": "form-control"}
            ),
        }
        help_texts = {
            "parent": "The parent goal of this goal.",
            "name": "The name of this goal.",
            "is_ultimate_concern": "Is this goal an ultimate concern?",
            "description": "The description of this goal.",
            "due_date": "The due date of this goal.",
            "completed": "Is this goal completed?",
            "is_archived": "Is this goal archived?",
        }
        error_messages = {
            "name": {
                "required": "The name of the goal is required.",
            },
        }
