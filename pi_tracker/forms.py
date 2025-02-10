from django import forms

from .models import PiDevice


class PiDeviceForm(forms.ModelForm):
    class Meta:
        model = PiDevice
        fields = "__all__"
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
