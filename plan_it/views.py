# plan_it/views.py

from django.views import generic
from django.shortcuts import render

from base.decorators import registration_accepted_required
from base.mixins import RegistrationAcceptedMixin

from .models import StorageLocation, Item, ActivityType, Activity


@registration_accepted_required
def dashboard(request):
    activities = Activity.objects.filter(user=request.user).order_by("due_date")[:10]
    items = Item.objects.filter(user=request.user)[:10]
    return render(
        request,
        "plan_it/dashboard.html",
        {
            "activities": activities,
            "items": items,
            "page_title": "Plan It Dashboard",
        },
    )


# Generic Mixin pattern to reduce duplication
class UserQuerySetMixin:
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class UserAssignMixin:
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# ---- StorageLocation Views ----
class StorageLocationListView(
    RegistrationAcceptedMixin, UserQuerySetMixin, generic.ListView
):
    model = StorageLocation


class StorageLocationCreateView(
    RegistrationAcceptedMixin, UserAssignMixin, generic.CreateView
):
    model = StorageLocation
    fields = ["name", "parent_location"]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["parent_location"].queryset = StorageLocation.objects.filter(
            user=self.request.user
        )
        return form


class StorageLocationUpdateView(StorageLocationCreateView, generic.UpdateView):
    pass


class StorageLocationDeleteView(
    RegistrationAcceptedMixin, UserQuerySetMixin, generic.DeleteView
):
    model = StorageLocation


# ---- Item Views ----
class ItemListView(RegistrationAcceptedMixin, UserQuerySetMixin, generic.ListView):
    model = Item


class ItemCreateView(RegistrationAcceptedMixin, UserAssignMixin, generic.CreateView):
    model = Item
    fields = ["name", "storage_location", "description"]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["storage_location"].queryset = StorageLocation.objects.filter(
            user=self.request.user
        )
        return form


class ItemUpdateView(ItemCreateView, generic.UpdateView):
    pass


class ItemDeleteView(RegistrationAcceptedMixin, UserQuerySetMixin, generic.DeleteView):
    model = Item


# ---- ActivityType Views ----
class ActivityTypeListView(
    RegistrationAcceptedMixin, UserQuerySetMixin, generic.ListView
):
    model = ActivityType


class ActivityTypeCreateView(
    RegistrationAcceptedMixin, UserAssignMixin, generic.CreateView
):
    model = ActivityType
    fields = ["name"]


class ActivityTypeUpdateView(ActivityTypeCreateView, generic.UpdateView):
    pass


class ActivityTypeDeleteView(
    RegistrationAcceptedMixin, UserQuerySetMixin, generic.DeleteView
):
    model = ActivityType


# ---- Activity Views ----
class ActivityListView(RegistrationAcceptedMixin, UserQuerySetMixin, generic.ListView):
    model = Activity


class ActivityCreateView(
    RegistrationAcceptedMixin, UserAssignMixin, generic.CreateView
):
    model = Activity
    fields = [
        "name",
        "type",
        "target_item",
        "target_location",
        "description",
        "due_date",
        "is_recurring",
        "last_completed",
    ]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["type"].queryset = ActivityType.objects.filter(
            user=self.request.user
        )
        form.fields["target_item"].queryset = Item.objects.filter(
            user=self.request.user
        )
        form.fields["target_location"].queryset = StorageLocation.objects.filter(
            user=self.request.user
        )
        return form


class ActivityUpdateView(ActivityCreateView, generic.UpdateView):
    pass


class ActivityDeleteView(
    RegistrationAcceptedMixin, UserQuerySetMixin, generic.DeleteView
):
    model = Activity
