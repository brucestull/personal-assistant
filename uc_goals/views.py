from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView

from base.decorators import registration_accepted_required
from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME
from uc_goals.models import Goal


class GoalCreateView(RegistrationAcceptedMixin, CreateView):
    model = Goal
    fields = [
        "name",
        "is_ultimate_concern",
        "description",
        "due_date",
        "completed",
        "parent",
    ]
    # template_name = "uc_goals/goal_form.html"
    # success_url = reverse_lazy("uc_goals:uc_list")

    def form_valid(self, form):
        form.instance.user = self.request.user  # Assign the logged-in user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Create a Goal"
        context["the_site_name"] = THE_SITE_NAME
        return context


class GoalDetailView(RegistrationAcceptedMixin, DetailView):
    model = Goal
    # template_name = "uc_goals/goal_detail.html"
    # context_object_name = "goal"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["the_site_name"] = THE_SITE_NAME
        return context


class GoalUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = Goal
    fields = [
        "name",
        "is_ultimate_concern",
        "description",
        "due_date",
        "completed",
        "parent",
    ]
    # template_name = "uc_goals/goal_form.html"
    # How to route back to the goal detail page after updating?

    # success_url = reverse_lazy("uc_goals:goal_detail")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = get_object_or_404(Goal, pk=self.kwargs["pk"]).name
        context["the_site_name"] = THE_SITE_NAME
        return context


@registration_accepted_required
def ultimate_concerns(request):
    """
    Goals which are ultimate concerns and owned by the user.
    """
    goals = Goal.objects.filter(is_ultimate_concern=True, user=request.user)
    return render(
        request,
        "uc_goals/goal_list.html",
        {
            "goals": goals,
            "the_site_name": THE_SITE_NAME,
            "page_title": "Ultimate Concerns",
        },
    )


@registration_accepted_required
def orphan_goals(request):
    """
    Goals which are not ultimate concerns but are owned by the user.
    """
    goals = Goal.objects.filter(
        is_ultimate_concern=False, parent__isnull=True, user=request.user
    )
    return render(
        request,
        "uc_goals/goal_list.html",
        {
            "goals": goals,
            "the_site_name": THE_SITE_NAME,
            "page_title": "Orphan Goals",
        },
    )
