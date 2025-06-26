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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        # 1. show only this user's activities
        self.fields["activity"].queryset = Activity.objects.filter(user=user)

        # 2. if we're editing an existing item, pre-select its activity
        if self.instance and self.instance.pk and self.instance.activity_id:
            self.fields["activity"].initial = self.instance.activity_id
