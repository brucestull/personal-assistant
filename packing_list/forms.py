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
        # pull out our custom kwargs so the base class never sees them
        user = kwargs.pop("user", None)
        activity = kwargs.pop("activity", None)

        # now call the parent __init__
        super().__init__(*args, **kwargs)

        # if the caller gave us a user, limit the activity choices
        if user is not None:
            self.fields["activity"].queryset = Activity.objects.filter(user=user)

        # if the caller gave us an activity (either ID or instance),
        # pre-fill it and hide it so they can’t change it
        if activity is not None:
            # if they passed an ID, Django will still accept it as initial
            self.fields["activity"].initial = activity
            self.fields["activity"].widget = forms.HiddenInput()
