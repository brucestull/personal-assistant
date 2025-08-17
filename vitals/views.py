# vitals/views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from base.decorators import registration_accepted_required
from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME
from vitals.models import BloodPressure, BodyWeight

from vitals.forms import BodyWeightForm, BloodPressureForm


def home(request):
    """
    View function for the home page of the `vitals` app.
    """
    return render(
        request,
        "vitals/home.html",
        {
            "the_site_name": THE_SITE_NAME,
            "page_title": "Vitals Home",
        },
    )


class BloodPressureListView(RegistrationAcceptedMixin, LoginRequiredMixin, ListView):
    model = BloodPressure
    ordering = "-created"
    paginate_by = 10
    PER_PAGE_OPTIONS = (10, 25, 50, 100)

    def get_paginate_by(self, queryset):
        # allow ?per_page=XX; clamp between 1 and 100
        try:
            per_page = int(self.request.GET.get("per_page", self.paginate_by))
            return max(1, min(per_page, 100))
        except (TypeError, ValueError):
            return self.paginate_by

    def get_queryset(self):
        return BloodPressure.objects.for_user(self.request.user).order_by(self.ordering)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        summary = qs.summary()

        ctx["user_averages_and_medians"] = {
            "systolic_average": summary["systolic_average"],
            "diastolic_average": summary["diastolic_average"],
            "systolic_median": summary["systolic_median"],
            "diastolic_median": summary["diastolic_median"],
        }
        ctx["user_pressure_range"] = {
            "systolic_min": summary["systolic_min"],
            "diastolic_min": summary["diastolic_min"],
            "systolic_max": summary["systolic_max"],
            "diastolic_max": summary["diastolic_max"],
        }

        # expose per-page controls
        ctx["per_page_options"] = self.PER_PAGE_OPTIONS
        # make it an int so template comparisons are easy
        try:
            ctx["current_per_page"] = int(
                self.request.GET.get("per_page", self.get_paginate_by(None))
            )
        except (TypeError, ValueError):
            ctx["current_per_page"] = self.paginate_by
        return ctx


class BloodPressureCreateView(
    RegistrationAcceptedMixin, LoginRequiredMixin, CreateView
):
    """
    Create form for a new blood pressure measurement.
    """

    model = BloodPressure
    form_class = BloodPressureForm
    success_url = reverse_lazy("vitals:bloodpressure-list")  # use named URL
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Create Blood Pressure",
    }

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def _ensure_can_edit(request, obj: BodyWeight):
    # Allow the subject themself or staff to edit/delete
    if not (request.user.is_staff or obj.subject_id == request.user.id):
        raise Http404("Not found")


@login_required
@registration_accepted_required
def bodyweight_list(request):
    """
    List view with simple search + pagination.
    """
    q = request.GET.get("q", "").strip()
    qs = BodyWeight.objects.select_related("subject").order_by("-created")

    # Non-staff see only their own records
    if not request.user.is_staff:
        qs = qs.filter(subject=request.user)

    if q:
        qs = qs.filter(Q(subject__username__icontains=q) | Q(measurement__icontains=q))

    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request, "vitals/bodyweight_list.html", {"page_obj": page_obj, "q": q}
    )


@login_required
@registration_accepted_required
def bodyweight_detail(request, pk):
    obj = get_object_or_404(BodyWeight.objects.select_related("subject"), pk=pk)
    if not request.user.is_staff and obj.subject_id != request.user.id:
        raise Http404("Not found")
    return render(request, "vitals/bodyweight_detail.html", {"object": obj})


@login_required
@registration_accepted_required
def bodyweight_create(request):
    """
    If the user is not staff, force subject = request.user and hide field in template.
    Staff can choose any subject.
    """
    if request.method == "POST":
        form = BodyWeightForm(request.POST)
        if not request.user.is_staff:
            # enforce subject = current user
            form.data = form.data.copy()
            form.data["subject"] = str(request.user.pk)

        if form.is_valid():
            obj = form.save()
            messages.success(request, "Body weight saved.")
            return redirect("vitals:bodyweight_detail", pk=obj.pk)
    else:
        initial = {}
        if not request.user.is_staff:
            initial["subject"] = request.user.pk
        form = BodyWeightForm(initial=initial)

    return render(
        request,
        "vitals/bodyweight_form.html",
        {"form": form, "is_create": True, "force_subject": not request.user.is_staff},
    )


@login_required
@registration_accepted_required
def bodyweight_update(request, pk):
    obj = get_object_or_404(BodyWeight, pk=pk)
    _ensure_can_edit(request, obj)

    if request.method == "POST":
        form = BodyWeightForm(request.POST, instance=obj)
        if not request.user.is_staff:
            # Lock subject to the owner
            form.data = form.data.copy()
            form.data["subject"] = str(request.user.pk)

        if form.is_valid():
            obj = form.save()
            messages.success(request, "Body weight updated.")
            return redirect("vitals:bodyweight_detail", pk=obj.pk)
    else:
        form = BodyWeightForm(instance=obj)

    return render(
        request,
        "vitals/bodyweight_form.html",
        {
            "form": form,
            "object": obj,
            "is_create": False,
            "force_subject": not request.user.is_staff,
        },
    )


@login_required
@registration_accepted_required
def bodyweight_delete(request, pk):
    obj = get_object_or_404(BodyWeight, pk=pk)
    _ensure_can_edit(request, obj)

    if request.method == "POST":
        obj.delete()
        messages.success(request, "Body weight deleted.")
        return redirect("vitals:bodyweight_list")

    return render(request, "vitals/bodyweight_confirm_delete.html", {"object": obj})
