from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView

from base.decorators import registration_accepted_required
from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME
from uc_goals.models import Goal

from .forms import GoalForm


class GoalCreateView(RegistrationAcceptedMixin, CreateView):
    model = Goal
    form_class = GoalForm
    # fields = [
    #     "parent",
    #     "name",
    #     "is_ultimate_concern",
    #     "description",
    #     "due_date",
    #     "completed",
    #     "is_archived",
    # ]
    # template_name = "uc_goals/goal_form.html"
    # success_url = reverse_lazy("uc_goals:uc_list")

    def form_valid(self, form):
        form.instance.user = self.request.user  # Assign the logged-in user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Create a Goal"
        context["the_site_name"] = THE_SITE_NAME
        context["mode"] = "create"
        return context


class GoalDetailView(RegistrationAcceptedMixin, DetailView):
    model = Goal
    # These attributes are optional. If not provided, the view will use the default.
    # template_name = "uc_goals/goal_detail.html"
    # context_object_name = "goal"

    def get_queryset(self):
        """
        Return only the goals owned by the authenticated user. This queryset will be
        refined by the DetailView class.
        """
        queryset = Goal.objects.filter(user=self.request.user)
        # Remember to study this queryset.query to understand how Django ORM works.
        # print("print(queryset.query): ", queryset.query)
        # print("print(queryset): ", queryset)
        return queryset

    # def get_object(self, queryset=None):
    #     """
    #     Returns the object the view is displaying. The queryset is passed as an
    #     argument and the super-class method returns the single object from that
    #     queryset.

    #     We are not adding any functionality here. We are just printing the object.

    #     Uncomment this method to see that this view returns only a single object.
    #     """
    #     obj = super().get_object(queryset)
    #     print("print(obj): ", obj)
    #     return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # `DetailView` provides the object as `self.object`. This can be used to get
        # the object name.
        context["page_title"] = self.object.name
        context["the_site_name"] = THE_SITE_NAME
        return context


class GoalUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = Goal
    fields = [
        "parent",
        "name",
        "is_ultimate_concern",
        "description",
        "due_date",
        "completed",
        "is_archived",
    ]
    # template_name = "uc_goals/goal_form.html"
    # How to route back to the goal detail page after updating?

    # success_url = reverse_lazy("uc_goals:goal_detail")

    def get_queryset(self):
        """
        Return only the goals owned by the authenticated user. This queryset will be
        refined by the UpdateView class.
        """
        queryset = Goal.objects.filter(user=self.request.user)
        # print(queryset.query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # `UpdateView` provides the object as `self.object`. This can be used to get
        # the object name.
        context["page_title"] = f"Edit: {self.object.name}"
        context["the_site_name"] = THE_SITE_NAME
        context["mode"] = "update"
        return context


@registration_accepted_required
def ultimate_concerns(request):
    """
    Goals which are ultimate concerns (top level goals) and owned by the user.
    """
    goals = Goal.objects.filter(is_ultimate_concern=True, user=request.user)
    return render(
        request,
        "uc_goals/goal_list.html",
        {
            "goals": goals,
            "the_site_name": THE_SITE_NAME,
            "page_title": "Top-Level Goals, BOI!",
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
