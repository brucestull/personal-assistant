# packing_list/forms.py

from django import forms

from .models import Activity, Item


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ["name", "description"]


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            "name",
            "description",
            "quantity",
            "is_packed",
            "is_essential",
            "activity",
        ]
