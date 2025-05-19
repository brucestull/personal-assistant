# plan_it/views.py

from collections import defaultdict
from datetime import date

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic

from base.decorators import registration_accepted_required
from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME

from .models import (
    Activity,
    ActivityInstance,
    ActivityLocation,
    ActivityType,
    Item,
    StorageLocation,
)


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

    recent_completions = ActivityInstance.objects.filter(user=request.user).order_by(
        "-completed_at"
    )[:5]

    return render(
        request,
        "plan_it/dashboard.html",
        {
            "grouped_activities": grouped_activities,
            "top_locations": top_locations,
            "items": items,
            "recent_completions": recent_completions,
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
    extra_context = {
        "page_title": "Storage Locations",
        "the_site_name": THE_SITE_NAME,
    }


class StorageLocationCreateView(
    RegistrationAcceptedMixin, UserAssignMixin, generic.CreateView
):
    model = StorageLocation
    fields = ["name", "parent_location"]
    extra_context = {
        "page_title": "Create Storage Location",
        "the_site_name": THE_SITE_NAME,
        "mode": "create",
    }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["parent_location"].queryset = StorageLocation.objects.filter(
            user=self.request.user
        )
        return form


class StorageLocationUpdateView(StorageLocationCreateView, generic.UpdateView):
    extra_context = {
        "page_title": "Update Storage Location",
        "the_site_name": THE_SITE_NAME,
        "mode": "update",
    }


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
    extra_context = {
        "page_title": "Activity Locations",
        "the_site_name": THE_SITE_NAME,
    }


class ActivityLocationCreateView(
    RegistrationAcceptedMixin, UserAssignMixin, generic.CreateView
):
    model = ActivityLocation
    fields = ["name", "parent_location"]
    extra_context = {
        "page_title": "Create Activity Location",
        "the_site_name": THE_SITE_NAME,
        "mode": "create",
    }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["parent_location"].queryset = ActivityLocation.objects.filter(
            user=self.request.user
        )
        return form


class ActivityLocationUpdateView(ActivityLocationCreateView, generic.UpdateView):
    extra_context = {
        "page_title": "Update Activity Location",
        "the_site_name": THE_SITE_NAME,
        "mode": "update",
    }


class ActivityLocationDeleteView(
    RegistrationAcceptedMixin, UserQuerySetMixin, generic.DeleteView
):
    model = ActivityLocation
    extra_context = {
        "page_title": "Delete Activity Location",
        "the_site_name": THE_SITE_NAME,
        "mode": "delete",
    }
    success_url = reverse_lazy("plan_it:activity_location_list")


# ---- Item Views ----
class ItemListView(RegistrationAcceptedMixin, UserQuerySetMixin, generic.ListView):
    model = Item
    extra_context = {
        "page_title": "Items",
        "the_site_name": THE_SITE_NAME,
    }


class ItemCreateView(RegistrationAcceptedMixin, UserAssignMixin, generic.CreateView):
    model = Item
    fields = ["name", "storage_location", "description"]
    extra_context = {
        "page_title": "Create Item",
        "the_site_name": THE_SITE_NAME,
        "mode": "create",
    }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["storage_location"].queryset = StorageLocation.objects.filter(
            user=self.request.user
        )
        return form


class ItemUpdateView(ItemCreateView, generic.UpdateView):
    extra_context = {
        "page_title": "Update Item",
        "the_site_name": THE_SITE_NAME,
        "mode": "update",
    }


class ItemDeleteView(RegistrationAcceptedMixin, UserQuerySetMixin, generic.DeleteView):
    model = Item
    success_url = reverse_lazy("plan_it:item_list")


# ---- ActivityType Views ----
class ActivityTypeListView(
    RegistrationAcceptedMixin, UserQuerySetMixin, generic.ListView
):
    model = ActivityType
    extra_context = {
        "page_title": "Activity Types",
        "the_site_name": THE_SITE_NAME,
    }


class ActivityTypeCreateView(
    RegistrationAcceptedMixin, UserAssignMixin, generic.CreateView
):
    model = ActivityType
    fields = ["name"]
    extra_context = {
        "page_title": "Create Activity Type",
        "the_site_name": THE_SITE_NAME,
        "mode": "create",
    }


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
    extra_context = {
        "page_title": "Activities",
        "the_site_name": THE_SITE_NAME,
    }


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
    extra_context = {
        "page_title": "Create Activity",
        "the_site_name": THE_SITE_NAME,
        "mode": "create",
    }

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
    extra_context = {
        "page_title": "Delete Activity",
        "the_site_name": THE_SITE_NAME,
        "mode": "delete",
    }
    success_url = reverse_lazy("plan_it:activity_list")


@registration_accepted_required
def mark_activity_completed(request, pk):
    activity = get_object_or_404(Activity, pk=pk, user=request.user)

    if request.method == "POST":
        instance = activity.record_completion(user=request.user)  # noqa F841
        messages.success(request, f"Activity '{activity.name}' marked as completed.")
        return redirect("plan_it:dashboard")

    return redirect("plan_it:activity_list")
