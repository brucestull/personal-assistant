# vitals/forms.py

from django import forms

from .models import BodyWeight, BloodPressure


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


class BloodPressureForm(forms.ModelForm):
    class Meta:
        model = BloodPressure
        fields = ["systolic", "diastolic", "pulse", "note"]
        widgets = {
            "systolic": forms.NumberInput(attrs={"class": "form-control"}),
            "diastolic": forms.NumberInput(attrs={"class": "form-control"}),
            "pulse": forms.NumberInput(attrs={"class": "form-control"}),
            "note": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
