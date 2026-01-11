"""Views for the successes app."""

from datetime import date, timedelta

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from base.decorators import registration_accepted_required
from base.mixins import RegistrationAcceptedMixin, SiteContextMixin

from .models import Success, WhatWentWell


@registration_accepted_required
def dashboard(request):
    """
    Dashboard view showing success statistics and recent entries.

    Displays:
    - Recent successes
    - Recent What Went Well entries
    - Statistics (counts, streaks)
    - Encouragement for daily reflection
    """
    user = request.user
    today = date.today()
    week_ago = today - timedelta(days=7)

    # Get recent successes
    recent_successes = Success.objects.filter(user=user).order_by("-created")[:10]

    # Get recent What Went Wells
    recent_wwws = WhatWentWell.objects.filter(user=user).order_by("-created")[:10]

    # Calculate statistics
    total_successes = Success.objects.filter(user=user).count()
    total_wwws = WhatWentWell.objects.filter(user=user).count()

    # This week's counts
    successes_this_week = Success.objects.filter(
        user=user, created__gte=week_ago
    ).count()

    wwws_this_week = WhatWentWell.objects.filter(
        user=user, created__gte=week_ago
    ).count()

    # Today's counts
    wwws_today = WhatWentWell.objects.filter(user=user, created__date=today).count()

    # Check if user has completed 3 What Went Wells today (goal)
    daily_goal_met = wwws_today >= 3
    wwws_remaining = max(0, 3 - wwws_today)

    context = {
        "recent_successes": recent_successes,
        "recent_wwws": recent_wwws,
        "total_successes": total_successes,
        "total_wwws": total_wwws,
        "successes_this_week": successes_this_week,
        "wwws_this_week": wwws_this_week,
        "wwws_today": wwws_today,
        "daily_goal_met": daily_goal_met,
        "wwws_remaining": wwws_remaining,
        "the_site_name": "Personal Assistant",
        "page_title": "Daily Successes Dashboard",
    }

    return render(request, "successes/dashboard.html", context)


# --- Success CRUD Views ---
class SuccessListView(RegistrationAcceptedMixin, SiteContextMixin, ListView):
    model = Success
    page_title = "All Successes"

    def get_queryset(self):
        return Success.objects.filter(user=self.request.user)


class SuccessDetailView(RegistrationAcceptedMixin, SiteContextMixin, DetailView):
    model = Success
    page_title = "Success Detail"

    def get_queryset(self):
        return Success.objects.filter(user=self.request.user)


class SuccessCreateView(RegistrationAcceptedMixin, SiteContextMixin, CreateView):
    model = Success
    fields = ["text"]
    success_url = reverse_lazy("successes:success_list")
    page_title = "Add Success"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SuccessUpdateView(RegistrationAcceptedMixin, SiteContextMixin, UpdateView):
    model = Success
    fields = ["text"]
    success_url = reverse_lazy("successes:success_list")
    page_title = "Edit Success"

    def get_queryset(self):
        return Success.objects.filter(user=self.request.user)


class SuccessDeleteView(RegistrationAcceptedMixin, SiteContextMixin, DeleteView):
    model = Success
    success_url = reverse_lazy("successes:success_list")
    page_title = "Delete Success"

    def get_queryset(self):
        return Success.objects.filter(user=self.request.user)


# --- WhatWentWell CRUD Views ---
class WhatWentWellListView(RegistrationAcceptedMixin, SiteContextMixin, ListView):
    model = WhatWentWell
    page_title = "What Went Well Entries"

    def get_queryset(self):
        return WhatWentWell.objects.filter(user=self.request.user)


class WhatWentWellDetailView(RegistrationAcceptedMixin, SiteContextMixin, DetailView):
    model = WhatWentWell
    page_title = "What Went Well Detail"

    def get_queryset(self):
        return WhatWentWell.objects.filter(user=self.request.user)


class WhatWentWellCreateView(RegistrationAcceptedMixin, SiteContextMixin, CreateView):
    model = WhatWentWell
    fields = ["what_went_well", "how_i_made_it_happen"]
    success_url = reverse_lazy("successes:whatwentwell_list")
    page_title = "Add What Went Well"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WhatWentWellUpdateView(RegistrationAcceptedMixin, SiteContextMixin, UpdateView):
    model = WhatWentWell
    fields = ["what_went_well", "how_i_made_it_happen"]
    success_url = reverse_lazy("successes:whatwentwell_list")
    page_title = "Edit What Went Well"

    def get_queryset(self):
        return WhatWentWell.objects.filter(user=self.request.user)


class WhatWentWellDeleteView(RegistrationAcceptedMixin, SiteContextMixin, DeleteView):
    model = WhatWentWell
    success_url = reverse_lazy("successes:whatwentwell_list")
    page_title = "Delete What Went Well"

    def get_queryset(self):
        return WhatWentWell.objects.filter(user=self.request.user)
