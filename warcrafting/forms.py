# warcrafting/forms.py

from django import forms

from .models import Character, CharacterProfession


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ["name", "wow_class", "race", "level"]


class CharacterProfessionForm(forms.ModelForm):
    class Meta:
        model = CharacterProfession
        fields = ["profession_tier", "current_skill"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["profession_tier"].label = "Profession Tier"
        self.fields["current_skill"].label = "Current Skill Level"

    def clean_current_skill(self):
        skill = self.cleaned_data.get("current_skill")
        if skill is None:
            return skill
        tier = self.cleaned_data.get("profession_tier")
        if tier and tier.max_skill is not None and skill > tier.max_skill:
            raise forms.ValidationError(
                f"Skill cannot exceed the tier maximum of {tier.max_skill}."
            )
        return skill
