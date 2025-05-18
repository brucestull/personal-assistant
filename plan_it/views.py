# plan_it/views.py

from collections import defaultdict
from datetime import date

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from base.decorators import registration_accepted_required
from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME

from .models import (Activity, ActivityLocation, ActivityType, Item,
                     StorageLocation)


@registration_accepted_required
def dashboard(request):
    today = date.today()

    all_activities = (
        Activity.objects.filter(user=request.user)
        .select_related("activity_location", "target_item")
        .order_by("due_date")
    )

    grouped_activities = defaultdict(list)
    for activity in all_activities:
        loc = activity.activity_location
        grouped_activities[loc].append(activity)

    top_locations = ActivityLocation.objects.filter(
        user=request.user, parent_location__isnull=True
    ).prefetch_related("sublocations")

    items = Item.objects.filter(user=request.user).select_related("storage_location")[
        :10
    ]

    return render(
        request,
        "plan_it/dashboard.html",
        {
            "grouped_activities": grouped_activities,
            "top_locations": top_locations,
            "items": items,
            "today": today,
            "page_title": "Plan It Dashboard",
            "the_site_name": THE_SITE_NAME,
        },
    )


# Generic mixins
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
    success_url = reverse_lazy("plan_it:storage_location_list")


# ---- ActivityLocation Views ----
class ActivityLocationListView(
    RegistrationAcceptedMixin, UserQuerySetMixin, generic.ListView
):
    model = ActivityLocation


class ActivityLocationCreateView(
    RegistrationAcceptedMixin, UserAssignMixin, generic.CreateView
):
    model = ActivityLocation
    fields = ["name", "parent_location"]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["parent_location"].queryset = ActivityLocation.objects.filter(
            user=self.request.user
        )
        return form


class ActivityLocationUpdateView(ActivityLocationCreateView, generic.UpdateView):
    pass


class ActivityLocationDeleteView(
    RegistrationAcceptedMixin, UserQuerySetMixin, generic.DeleteView
):
    model = ActivityLocation
    success_url = reverse_lazy("plan_it:activity_location_list")


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
    success_url = reverse_lazy("plan_it:item_list")


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
    success_url = reverse_lazy("plan_it:activity_type_list")


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
        "activity_location",
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
        form.fields["activity_location"].queryset = ActivityLocation.objects.filter(
            user=self.request.user
        )
        return form


class ActivityUpdateView(ActivityCreateView, generic.UpdateView):
    pass


class ActivityDeleteView(
    RegistrationAcceptedMixin, UserQuerySetMixin, generic.DeleteView
):
    model = Activity
    success_url = reverse_lazy("plan_it:activity_list")
