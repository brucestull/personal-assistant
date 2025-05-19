# View Protection Tests

- [View Protection Tests - Private](https://chatgpt.com/c/6829ee16-bd74-8002-8e3c-868f33a1936c)

I don't know if this is overkill or not.

But, I want to have testing of `views.py` to ensure they are using `RegistrationAcceptedMixin` or `registration_accepted_required`.

```python
# base/mixins.py

from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


class RegistrationAcceptedMixin(AccessMixin):
    """
    Mixin to check if the user is authenticated and their registration is accepted.
    """

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated and if registration is accepted
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.registration_accepted:
            raise PermissionDenied("Your registration has not been accepted yet.")
        return super().dispatch(request, *args, **kwargs)


class UserIsAuthorMixin(AccessMixin):
    """
    Mixin to check if the user is the author of the object.
    """

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is the author of the object
        if not request.user == self.get_object().author:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class OrderableMixin:
    """
    Mixin to add `reorder_all` class method to models with an 'order' field.
    """

    @classmethod
    def reorder_all(cls):
        for index, item in enumerate(cls.objects.all().order_by("order")):
            item.order = index
            item.save()
```

```python
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
```

```python
# base/decorators.py

from functools import wraps

from django.shortcuts import render


def registration_accepted_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return render(
                request,
                "403.html",
                {"error": "You must be logged in to access this page."},
                status=403,
            )

        # Check if the user's registration is accepted
        if not getattr(request.user, "registration_accepted", False):
            return render(
                request,
                "403.html",
                {"error": "Your registration has not been accepted."},
                status=403,
            )

        # Call the original view function if checks pass
        return view_func(request, *args, **kwargs)

    return _wrapped_view
```

```python
# accounts/models.py

from statistics import median

from django.contrib.auth.models import AbstractUser
from django.db import models

from vitals.models import BloodPressure


class CustomUser(AbstractUser):
    """
    A `CustomUser` so we can add our own functionality for site users.
    """

    # `registration_accepted` is used to control access to the site.
    registration_accepted = models.BooleanField(
        default=False,
        help_text=("Designates whether this user's registration has " "been accepted."),
    )
    beastie = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def get_blood_pressure_range(self):
        """
        Returns the maximum and minimum systolic and diastolic blood
        pressure readings for the current user.

        Attributes:
        - `self` is the current `CustomUser` object.
        - `systolic_min` is the minimum systolic blood pressure
        reading of all the `BloodPressure` objects for the current user.
        - `diastolic_min` is the minimum diastolic blood pressure
        reading of all the `BloodPressure` objects for the current user.
        - `systolic_max` is the maximum systolic blood pressure
        reading of all the `BloodPressure` objects for the current user.
        - `diastolic_max` is the maximum diastolic blood pressure
        reading of all the `BloodPressure` objects for the current user.
        """
        if BloodPressure.objects.filter(user=self).count() == 0:
            # TODO: Determine if there is a better way to handle this.
            """
            {
                "systolic_min": None,
                "diastolic_min": None,
                "systolic_max": None,
                "diastolic_max": None,
            }
            """
            return None
        else:
            systolic_min = (
                BloodPressure.objects.filter(
                    user=self,
                )
                .order_by("systolic")
                .first()
                .systolic
            )
            diastolic_min = (
                BloodPressure.objects.filter(
                    user=self,
                )
                .order_by("diastolic")
                .first()
                .diastolic
            )
            systolic_max = (
                BloodPressure.objects.filter(
                    user=self,
                )
                .order_by("-systolic")
                .first()
                .systolic
            )
            diastolic_max = (
                BloodPressure.objects.filter(
                    user=self,
                )
                .order_by("-diastolic")
                .first()
                .diastolic
            )
            return {
                "systolic_min": systolic_min,
                "diastolic_min": diastolic_min,
                "systolic_max": systolic_max,
                "diastolic_max": diastolic_max,
            }

    def get_average_and_median_blood_pressure(self):
        """
        Returns the average and median systolic and diastolic blood
        pressure readings for the current user.

        Attributes:
        - `self` is the current `CustomUser` object.
        - `systolic_average` is the average systolic blood pressure
        reading of all the `BloodPressure` objects for the current user.
        - `diastolic_average` is the average diastolic blood pressure
        reading of all the `BloodPressure` objects for the current user.
        - `systolic_median` is the median systolic blood pressure
        reading of all the `BloodPressure` objects for the current user.
        - `diastolic_median` is the median diastolic blood pressure
        reading of all the `BloodPressure` objects for the current user.
        """
        systolic_average = (
            BloodPressure.objects.filter(
                user=self,
            )
            .values_list("systolic", flat=True)
            .aggregate(models.Avg("systolic"))
        )
        diastolic_average = (
            BloodPressure.objects.filter(
                user=self,
            )
            .values_list("diastolic", flat=True)
            .aggregate(models.Avg("diastolic"))
        )
        if BloodPressure.objects.filter(user=self).count() == 0:
            return {
                "systolic_average": None,
                "diastolic_average": None,
                "systolic_median": None,
                "diastolic_median": None,
            }
        else:
            systolic_median = median(
                BloodPressure.objects.filter(
                    user=self,
                ).values_list("systolic", flat=True)
            )
            diastolic_median = median(
                BloodPressure.objects.filter(
                    user=self,
                ).values_list("diastolic", flat=True)
            )
            return {
                "systolic_average": round(
                    systolic_average["systolic__avg"],
                    2,
                ),
                "diastolic_average": round(
                    diastolic_average["diastolic__avg"],
                    2,
                ),
                "systolic_median": systolic_median,
                "diastolic_median": diastolic_median,
            }

    def __str__(self):
        """
        String representation of CustomUser.
        """
        return self.username
```

I want test that check that either `RegistrationAcceptedMixin` or `registration_accepted_required` are used in all views. And I want tests that check that the functionality of `RegistrationAcceptedMixin` or `registration_accepted_required` are doing what is expected.

It’s *not* overkill — this is a **great idea** for enforcing security rules and avoiding regressions. You're testing both:

1. **Structural protection**: Making sure views are decorated with or subclassing access control mechanisms.
2. **Behavioral protection**: Ensuring unauthorized access gets blocked and proper users get through.

---

## ✅ PART 1: Structural Enforcement Tests

These are “meta” tests — they don’t hit views, they **inspect the source code or class structure** to ensure mixins/decorators are used.

### 🔍 Class-Based Views: Check if `RegistrationAcceptedMixin` is inherited

```python
# tests/test_view_protections.py

import inspect
from plan_it import views
from base.mixins import RegistrationAcceptedMixin


def test_all_cbvs_use_registration_accepted_mixin():
    """
    Ensures all class-based views inherit from RegistrationAcceptedMixin.
    """
    violations = []

    for name, cls in inspect.getmembers(views, inspect.isclass):
        # Only check views defined in this module
        if cls.__module__ != views.__name__:
            continue

        # Skip mixins or abstract base classes
        if "Mixin" in name or name.endswith("BaseView"):
            continue

        if not issubclass(cls, RegistrationAcceptedMixin):
            violations.append(name)

    assert not violations, (
        "The following class-based views are missing RegistrationAcceptedMixin: "
        + ", ".join(violations)
    )
```

### 🔍 Function-Based Views: Check if `registration_accepted_required` is applied

```python
import types
from base.decorators import registration_accepted_required


def test_all_fbvs_use_registration_accepted_required():
    """
    Ensures all function-based views have the registration_accepted_required decorator.
    """
    violations = []

    for name, view in inspect.getmembers(views, inspect.isfunction):
        # Only views defined in the module
        if view.__module__ != views.__name__:
            continue

        # Check if the view is wrapped with our decorator
        if getattr(view, "__wrapped__", None) is None:
            violations.append(name)
        elif not getattr(view.__wrapped__, "__name__", "").startswith("dashboard"):
            # if not dashboard, may be okay to skip
            violations.append(name)

    assert not violations, (
        "The following function-based views are missing @registration_accepted_required: "
        + ", ".join(violations)
    )
```

> You can hardcode `dashboard` if that’s your only FBV. Or generalize with a whitelist.

---

## ✅ PART 2: Behavioral Tests

These ensure that access is actually denied or permitted correctly.

### 🧪 Test Mixin Behavior (CBVs)

```python
# tests/test_registration_access.py

import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_cbv_denies_unauthenticated(client):
    response = client.get(reverse("plan_it:storage_location_list"))
    assert response.status_code in (302, 403)


@pytest.mark.django_db
def test_cbv_denies_if_registration_not_accepted(client):
    user = User.objects.create_user(username="notaccepted", password="pass")
    client.login(username="notaccepted", password="pass")
    response = client.get(reverse("plan_it:storage_location_list"))
    assert response.status_code == 403
    assert b"registration has not been accepted" in response.content.lower()


@pytest.mark.django_db
def test_cbv_allows_if_registration_accepted(client):
    user = User.objects.create_user(
        username="accepted", password="pass", registration_accepted=True
    )
    client.login(username="accepted", password="pass")
    response = client.get(reverse("plan_it:storage_location_list"))
    assert response.status_code == 200
```

### 🧪 Test Decorator Behavior (FBV)

```python
@pytest.mark.django_db
def test_dashboard_fbv_denies_if_not_authenticated(client):
    response = client.get(reverse("plan_it:dashboard"))
    assert response.status_code == 403
    assert b"must be logged in" in response.content.lower()


@pytest.mark.django_db
def test_dashboard_fbv_denies_if_not_accepted(client):
    user = User.objects.create_user(username="user", password="pass")
    client.login(username="user", password="pass")
    response = client.get(reverse("plan_it:dashboard"))
    assert response.status_code == 403
    assert b"registration has not been accepted" in response.content.lower()


@pytest.mark.django_db
def test_dashboard_fbv_allows_if_accepted(client):
    user = User.objects.create_user(
        username="gooduser", password="pass", registration_accepted=True
    )
    client.login(username="gooduser", password="pass")
    response = client.get(reverse("plan_it:dashboard"))
    assert response.status_code == 200
    assert b"Plan It Dashboard" in response.content
```

---

## 🧪 Optional: Add Test Coverage for 403 Template

You can even test that `"403.html"` is rendered with the correct context using `TemplateResponse`.

---

## Summary

| Test Type            | What it Ensures           | Example                                         |
| -------------------- | ------------------------- | ----------------------------------------------- |
| Structural (meta)    | Views are protected       | `test_all_cbvs_use_registration_accepted_mixin` |
| Functional (runtime) | Access is blocked/enabled | `test_cbv_denies_if_registration_not_accepted`  |

This level of testing **is not overkill** when:

* You care about securing access at the view level.
* You have more than one developer (or future-you!) making changes.
* You might later introduce `APIView` or `GraphQLView` endpoints that forget these checks.

Let me know if you want this added to a `pytest` suite, Django `unittest`, or a Makefile test target.

