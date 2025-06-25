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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        activity_id = kwargs.pop("activity", None)
        super().__init__(*args, **kwargs)

        # 1. always scope to this user
        qs = Activity.objects.filter(user=user)

        if activity_id:
            # 2a. further restrict to the single activity
            qs = qs.filter(pk=activity_id)
            # 2b. pre-select it
            self.fields["activity"].initial = activity_id
            # 2c. optionally hide the widget so they can’t swap it
            # self.fields["activity"].widget = forms.HiddenInput()

        self.fields["activity"].queryset = qs
