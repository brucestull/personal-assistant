# vitals/views.py

from datetime import date, timedelta

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, TemplateView

from base.decorators import registration_accepted_required
from base.mixins import RegistrationAcceptedMixin, SiteContextMixin
from vitals.forms import BloodPressureForm, BodyWeightForm
from vitals.models import BloodPressure, BodyWeight


class BloodPressureListView(
    SiteContextMixin, RegistrationAcceptedMixin, LoginRequiredMixin, ListView
):
    model = BloodPressure
    ordering = "-created"
    paginate_by = 10
    PER_PAGE_OPTIONS = (10, 25, 50, 100)
    page_title = "Blood Pressures"

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
        try:
            ctx["current_per_page"] = int(
                self.request.GET.get("per_page", self.get_paginate_by(None))
            )
        except (TypeError, ValueError):
            ctx["current_per_page"] = self.paginate_by
        return ctx


class BloodPressureCreateView(
    SiteContextMixin, RegistrationAcceptedMixin, LoginRequiredMixin, CreateView
):
    """
    Create form for a new blood pressure measurement.
    """

    model = BloodPressure
    form_class = BloodPressureForm
    success_url = reverse_lazy("vitals:bloodpressure-list")  # use named URL
    page_title = "Create Blood Pressure"

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


class BloodPressureReportView(
    SiteContextMixin, RegistrationAcceptedMixin, LoginRequiredMixin, TemplateView
):
    """
    Report view with week/month/custom filters and summary cards.
    """

    template_name = "vitals/bloodpressure_report.html"
    page_title = "Blood Pressure Report"

    # form used to validate/normalize GET inputs
    class FilterForm(forms.Form):
        PERIOD_ALL = "all"
        PERIOD_WEEK = "week"
        PERIOD_MONTH = "month"
        PERIOD_CUSTOM = "custom"
        PERIOD_CHOICES = (
            (PERIOD_WEEK, "Week"),
            (PERIOD_MONTH, "Month"),
            (PERIOD_CUSTOM, "Custom Range"),
            (PERIOD_ALL, "All Time"),
        )
        period = forms.ChoiceField(choices=PERIOD_CHOICES, required=False)

        # HTML <input type="week"> comes as "YYYY-Www"
        week = forms.CharField(required=False)
        # HTML <input type="month"> comes as "YYYY-MM"
        month = forms.CharField(required=False)

        start = forms.DateField(required=False, input_formats=["%Y-%m-%d"])
        end = forms.DateField(required=False, input_formats=["%Y-%m-%d"])

    def _parse_week_value(self, value: str):
        """
        Accepts strings like '2025-W43' from <input type="week">.
        Returns (start_date, end_date) for that ISO week.
        """
        # Defensive parsing
        # Expected formats: YYYY-Www or YYYY-Www (browser/locale variations)
        if not value:
            return None, None
        try:
            parts = value.split("-W")
            iso_year = int(parts[0])
            iso_week = int(parts[1])
            start = date.fromisocalendar(iso_year, iso_week, 1)
            end = start + timedelta(days=6)
            return start, end
        except Exception:
            return None, None

    def _parse_month_value(self, value: str):
        """
        Accepts strings like '2025-10' from <input type="month">.
        Returns (start_date, end_date) for that month.
        """
        if not value:
            return None, None
        try:
            year_s, month_s = value.split("-")
            y, m = int(year_s), int(month_s)
            from calendar import monthrange

            start = date(y, m, 1)
            end = date(y, m, monthrange(y, m)[1])
            return start, end
        except Exception:
            return None, None

    # vitals/views.py  — inside BloodPressureReportView

    def _compute_window(self, form: forms.Form):
        """
        Decide the date window (start, end, label) from validated GET params.
        Always safe even if the form is unbound/invalid (no cleaned_data).
        """
        cd = getattr(form, "cleaned_data", {}) or {}
        period = cd.get("period") or self.FilterForm.PERIOD_WEEK

        if period == self.FilterForm.PERIOD_WEEK:
            start, end = self._parse_week_value(cd.get("week"))
            if not start:
                today = timezone.localdate()
                iso_year, iso_week, _ = today.isocalendar()
                start = date.fromisocalendar(iso_year, iso_week, 1)
                end = start + timedelta(days=6)
            label = f"Week of {start:%b %d, %Y} – {end:%b %d, %Y}"
            return start, end, label, period

        if period == self.FilterForm.PERIOD_MONTH:
            start, end = self._parse_month_value(cd.get("month"))
            if not start:
                today = timezone.localdate()
                start = today.replace(day=1)
                from calendar import monthrange

                end = start.replace(day=monthrange(start.year, start.month)[1])
            label = f"{start:%B %Y}"
            return start, end, label, period

        if period == self.FilterForm.PERIOD_CUSTOM:
            start = cd.get("start")
            end = cd.get("end")
            if start and not end:
                end = start
            if end and not start:
                start = end
            if start and end and start > end:
                start, end = end, start
            if start and end:
                label = f"{start:%b %d, %Y} – {end:%b %d, %Y}"
                return start, end, label, period
            period = self.FilterForm.PERIOD_ALL  # fall back

        return None, None, "All Time", self.FilterForm.PERIOD_ALL

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # bind/validate GET
        form = self.FilterForm(self.request.GET or None)
        try:
            form.is_valid()  # populate cleaned_data if possible
        finally:
            if not hasattr(form, "cleaned_data"):
                form.cleaned_data = {}

        start, end, label, period = self._compute_window(form)

        # base queryset
        base_qs = BloodPressure.objects.for_user(self.request.user).order_by("-created")

        # filtered qs
        if start and end:
            qs = base_qs.in_date_range(start, end)
        else:
            qs = base_qs

        # summary (your existing QuerySet.summary())
        summary = qs.summary()

        # extras: counts + most recent
        total_count = qs.count()
        latest = qs.first()  # ordered -created

        # pagination (optional here; report often doesn’t need it, but you can keep it)
        per_page = 25
        paginator = Paginator(qs, per_page)
        page_obj = paginator.get_page(self.request.GET.get("page"))

        ctx.update(
            {
                "page_title": self.page_title,
                "filter_form": form,
                "period_start": start,
                "period_end": end,
                "period_label": label,
                "period_choice": period,
                "bp_page_obj": page_obj,
                "bp_summary": {
                    "systolic_average": summary["systolic_average"],
                    "diastolic_average": summary["diastolic_average"],
                    "systolic_median": summary["systolic_median"],
                    "diastolic_median": summary["diastolic_median"],
                    "systolic_min": summary["systolic_min"],
                    "diastolic_min": summary["diastolic_min"],
                    "systolic_max": summary["systolic_max"],
                    "diastolic_max": summary["diastolic_max"],
                    "count": total_count,
                },
                "latest_bp": latest,
                "PERIOD_WEEK": self.FilterForm.PERIOD_WEEK,
                "PERIOD_MONTH": self.FilterForm.PERIOD_MONTH,
                "PERIOD_CUSTOM": self.FilterForm.PERIOD_CUSTOM,
                "PERIOD_ALL": self.FilterForm.PERIOD_ALL,
            }
        )
        return ctx
