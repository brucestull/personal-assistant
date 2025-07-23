# packing_list/forms.py

from django import forms

from .models import Activity, Item


class ActivityForm(forms.ModelForm):
    """
    A simple form for creating or editing an Activity.
    """

    class Meta:
        model = Activity
        fields = ["name", "description"]


class ItemForm(forms.ModelForm):
    """
    A form for creating or editing an Item.

    Includes a custom ManyToMany field to associate the item with multiple activities,
    with behavior tailored for the logged-in user.
    """

    class Meta:
        model = Item
        fields = [
            "name",
            "description",
            "quantity",
            "is_packed",
            "is_essential",
            "activities",  # 👈 This is a ManyToManyField now
        ]

    def __init__(self, *args, **kwargs):
        # 👇 Pull out custom kwargs before calling super().__init__
        user = kwargs.pop("user", None)
        activity = kwargs.pop("activity", None)

        super().__init__(*args, **kwargs)

        # 👇 Redefine the field completely for more control
        self.fields["activities"] = forms.ModelMultipleChoiceField(
            queryset=Activity.objects.none(),  # start empty
            widget=forms.CheckboxSelectMultiple(),  # 👈 Use checkboxes instead of default multiselect # noqa: E501
            required=False,
            label="Linked Activities",  # 👈 User-friendly label
        )

        # 👇 Limit activities to only those created by the logged-in user
        if user is not None:
            self.fields["activities"].queryset = Activity.objects.filter(user=user)

        # 👇 If a specific activity is preselected, hide the field and set it
        if activity is not None:
            self.fields["activities"].initial = [activity]  # M2M needs a list
            self.fields["activities"].widget = forms.MultipleHiddenInput()
