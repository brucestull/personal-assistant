from django import forms

from .models import BodyWeight


class BodyWeightForm(forms.ModelForm):
    class Meta:
        model = BodyWeight
        fields = ["subject", "measurement"]
        widgets = {
            "subject": forms.Select(attrs={"class": "form-select"}),
            "measurement": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
        }

    def clean_measurement(self):
        val = self.cleaned_data["measurement"]
        if val <= 0:
            raise forms.ValidationError("Measurement must be greater than zero.")
        # Optional: add an upper bound sanity check (e.g., 1500 lb)
        if val > 1500:
            raise forms.ValidationError("That value seems unrealistically high.")
        return val
