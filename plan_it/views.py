# plan_it/views.py

from datetime import date

from django.shortcuts import render
from django.views import generic

from base.decorators import registration_accepted_required
from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME

from .models import Activity, ActivityType, Item, StorageLocation


@registration_accepted_required
def dashboard(request):
    today = date.today()
    overdue_activities = Activity.objects.filter(
        user=request.user, due_date__lt=today
    ).order_by("due_date")
    today_activities = Activity.objects.filter(
        user=request.user, due_date=today
    ).order_by("due_date")
    upcoming_activities = Activity.objects.filter(
        user=request.user, due_date__gt=today
    ).order_by("due_date")[:10]

    items = Item.objects.filter(user=request.user)[:10]

    return render(
        request,
        "plan_it/dashboard.html",
        {
            "overdue_activities": overdue_activities,
            "today_activities": today_activities,
            "upcoming_activities": upcoming_activities,
            "items": items,
            "today": today,
            "page_title": "Plan It Dashboard",
            "the_site_name": THE_SITE_NAME,
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
    # template_name = "plan_it/object_list.html"


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
    success_url = "/plan-it/locations/"  # Redirect to the list view after deletion


# ---- Item Views ----
class ItemListView(RegistrationAcceptedMixin, UserQuerySetMixin, generic.ListView):
    model = Item
    # template_name = "plan_it/object_list.html"


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
    success_url = "/plan-it/items/"  # Redirect to the list view after deletion


# ---- ActivityType Views ----
class ActivityTypeListView(
    RegistrationAcceptedMixin, UserQuerySetMixin, generic.ListView
):
    model = ActivityType
    # template_name = "plan_it/object_list.html"


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
    success_url = "/plan-it/activity-types/"  # Redirect to the list view after deletion


# ---- Activity Views ----
class ActivityListView(RegistrationAcceptedMixin, UserQuerySetMixin, generic.ListView):
    model = Activity
    # template_name = "plan_it/object_list.html"


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
    success_url = "/plan-it/activities/"  # Redirect to the list view after deletion
