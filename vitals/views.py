# vitals/views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView

from base.decorators import registration_accepted_required
from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME
from vitals.models import BloodPressure

from .forms import BodyWeightForm
from .models import BodyWeight


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


class BloodPressureListView(RegistrationAcceptedMixin, ListView):
    """
    `ListView` for a user's blood pressure measurements.
    """

    """
    The model attribute `model = BloodPressure` is not needed because the
    `get_queryset` method is defined.
    model = BloodPressure

    The template_name attribute `template_name =
    "vitals/bloodpressure_list.html"` is not needed since Django will use
    the default template name.
    template_name = "vitals/bloodpressure_list.html"

    The context_object_name attribute `context_object_name =
    "bloodpressure_list"` is not needed since Django will use the default
    context object name.
    context_object_name = "bloodpressure_list"

    This attribute `paginate_by = 10` will be implemented in the future.
    paginate_by = 10
    """

    def get_context_data(self, **kwargs):
        """
        Override the `get_context_data` method to add
        `user_averages_and_medians`.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Get the average and median of the current user's blood pressure
        # measurements.
        user_blood_pressure_averages_and_medians = (
            user.get_average_and_median_blood_pressure()
        )
        user_blood_pressure_range = user.get_blood_pressure_range()
        if user_blood_pressure_averages_and_medians is None:
            context["user_averages_and_medians"] = {
                "systolic_average": None,
                "diastolic_average": None,
                "systolic_median": None,
                "diastolic_median": None,
            }
        else:
            context["user_averages_and_medians"] = (
                user_blood_pressure_averages_and_medians
            )
            context["user_pressure_range"] = user_blood_pressure_range
        return context

    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Blood Pressures",
    }

    def get_queryset(self):
        """
        Override the `get_queryset` method to return a `QuerySet` of
        `BloodPressure` objects for the current user.
        """
        return BloodPressure.objects.filter(
            user=self.request.user,
        ).order_by("-created")


# Check if user is logged in and then check if the user has
# "registration_accepted" set to "True".
# TODO: Check if the order of the mixins matters. Order does matter:
# It's best practice to use mixins from more general to more specific.
class BloodPressureCreateView(
    RegistrationAcceptedMixin,
    CreateView,
):
    """
    `CreateView` for a user to create a blood pressure measurement.
    """

    model = BloodPressure
    # Redirect to the list of blood pressure measurements after a successful
    # creation.
    success_url = "/vitals/bloodpressures/"
    # TODO: Understand why this test doesn't work as expected.
    # success_url = reverse("vitals:bloodpressures")
    # Template name is not needed since we are using Django,s default template
    # naming convention `bloodpressure_form.html`.

    fields = [
        "systolic",
        "diastolic",
        "pulse",
    ]

    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Create Blood Pressure",
    }

    def form_valid(self, form):
        """
        Override the `form_valid` method to add the current user to the
        `BloodPressure` object.
        """
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
