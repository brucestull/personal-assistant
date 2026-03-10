# true_north/views.py

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, TemplateView, UpdateView
from django.views.generic.edit import CreateView

from base.mixins import RegistrationAcceptedMixin, SiteContextMixin
from true_north.forms import CoreValueForm, GoalForm, MilestoneForm, ValueActionForm
from true_north.models import CoreValue, Goal, GoalStatus, Milestone, ValueAction, ValueActionStatus  # noqa E501


class DashboardView(
    SiteContextMixin, RegistrationAcceptedMixin, LoginRequiredMixin, TemplateView
):
    """
    Dashboard view for True North app showing Core Values, Goals, Milestones, and Value Actions.  # noqa E501
    Includes filtering by status, completion, and active items.
    """

    template_name = "true_north/dashboard.html"
    page_title = "True North Dashboard"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        # Get filter parameters
        goal_status_filter = self.request.GET.get("goal_status", "active")
        task_status_filter = self.request.GET.get("task_status", "todo")
        show_completed_milestones = (
            self.request.GET.get("show_completed", "false") == "true"
        )

        # Base querysets for the user with optimized prefetching
        core_values = CoreValue.objects.filter(
            user=user, is_active=True
        ).prefetch_related(
            "goals",
            "goals__milestones",
            "goals__milestones__tasks"
        ).order_by("order", "name")

        # Filter goals based on selected status
        goals_qs = Goal.objects.filter(user=user, is_active=True)
        if goal_status_filter and goal_status_filter != "all":
            goals_qs = goals_qs.filter(status=goal_status_filter)
        goals = goals_qs.order_by("order", "title")

        # Filter milestones
        milestones_qs = Milestone.objects.filter(user=user)
        if not show_completed_milestones:
            milestones_qs = milestones_qs.filter(is_completed=False)
        milestones = milestones_qs.order_by("order", "description")

        # Filter tasks
        tasks_qs = ValueAction.objects.filter(user=user)
        if task_status_filter and task_status_filter != "all":
            tasks_qs = tasks_qs.filter(status=task_status_filter)
        tasks = tasks_qs.order_by("order", "id")

        # Calculate statistics
        stats = {
            "total_core_values": core_values.count(),
            "total_goals": goals.count(),
            "active_goals": Goal.objects.filter(
                user=user, is_active=True, status=GoalStatus.ACTIVE
            ).count(),
            "total_milestones": Milestone.objects.filter(user=user).count(),
            "completed_milestones": Milestone.objects.filter(
                user=user, is_completed=True
            ).count(),
            "pending_milestones": Milestone.objects.filter(
                user=user, is_completed=False
            ).count(),
            "total_tasks": ValueAction.objects.filter(user=user).count(),
            "todo_tasks": ValueAction.objects.filter(
                user=user, status=ValueActionStatus.TODO
            ).count(),
            "doing_tasks": ValueAction.objects.filter(
                user=user, status=ValueActionStatus.DOING
            ).count(),
            "done_tasks": ValueAction.objects.filter(
                user=user, status=ValueActionStatus.DONE
            ).count(),
        }

        # Build hierarchical structure for the dashboard
        core_values_data = []
        for cv in core_values:
            cv_goals = goals.filter(value=cv)

            goals_data = []
            for goal in cv_goals:
                goal_milestones = milestones.filter(goal=goal)

                milestones_data = []
                for milestone in goal_milestones:
                    milestone_tasks = tasks.filter(milestone=milestone)
                    # Get count before slicing to avoid double evaluation
                    total_tasks = milestone_tasks.count()
                    milestones_data.append({
                        "milestone": milestone,
                        "tasks": milestone_tasks[:5],  # Show first 5 tasks
                        "total_tasks": total_tasks,
                    })

                goals_data.append({
                    "goal": goal,
                    "milestones": milestones_data,
                })

            core_values_data.append({
                "core_value": cv,
                "goals": goals_data,
            })

        # Add context
        ctx.update({
            "core_values_data": core_values_data,
            "stats": stats,
            "goal_status_filter": goal_status_filter,
            "task_status_filter": task_status_filter,
            "show_completed_milestones": show_completed_milestones,
            "goal_status_choices": GoalStatus.choices,
            "task_status_choices": ValueActionStatus.choices,
        })

        return ctx


# ---------------------------------------------------------------------------
# CoreValue CRUD
# ---------------------------------------------------------------------------


class CoreValueListView(SiteContextMixin, RegistrationAcceptedMixin, ListView):
    model = CoreValue
    template_name = "true_north/corevalue_list.html"
    page_title = "Core Values"
    paginate_by = 20

    def get_queryset(self):
        return CoreValue.objects.filter(user=self.request.user).order_by(
            "order", "name"
        )


class CoreValueCreateView(SiteContextMixin, RegistrationAcceptedMixin, CreateView):
    model = CoreValue
    form_class = CoreValueForm
    template_name = "true_north/corevalue_form.html"
    success_url = reverse_lazy("true_north:core-value-list")
    page_title = "Create Core Value"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Core Value created successfully.")
        return super().form_valid(form)


class CoreValueUpdateView(SiteContextMixin, RegistrationAcceptedMixin, UpdateView):
    model = CoreValue
    form_class = CoreValueForm
    template_name = "true_north/corevalue_form.html"
    success_url = reverse_lazy("true_north:core-value-list")
    page_title = "Update Core Value"

    def get_queryset(self):
        return CoreValue.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Core Value updated successfully.")
        return super().form_valid(form)


class CoreValueDeleteView(SiteContextMixin, RegistrationAcceptedMixin, DeleteView):
    model = CoreValue
    template_name = "true_north/corevalue_confirm_delete.html"
    success_url = reverse_lazy("true_north:core-value-list")
    page_title = "Delete Core Value"

    def get_queryset(self):
        return CoreValue.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Core Value deleted.")
        return super().form_valid(form)
# ---------------------------------------------------------------------------


class GoalListView(SiteContextMixin, RegistrationAcceptedMixin, ListView):
    model = Goal
    template_name = "true_north/goal_list.html"
    page_title = "Goals"
    paginate_by = 20

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user).order_by("order", "title")


class GoalCreateView(SiteContextMixin, RegistrationAcceptedMixin, CreateView):
    model = Goal
    form_class = GoalForm
    template_name = "true_north/goal_form.html"
    success_url = reverse_lazy("true_north:goal-list")
    page_title = "Create Goal"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Goal created successfully.")
        return super().form_valid(form)


class GoalUpdateView(SiteContextMixin, RegistrationAcceptedMixin, UpdateView):
    model = Goal
    form_class = GoalForm
    template_name = "true_north/goal_form.html"
    success_url = reverse_lazy("true_north:goal-list")
    page_title = "Update Goal"

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Goal updated successfully.")
        return super().form_valid(form)


class GoalDeleteView(SiteContextMixin, RegistrationAcceptedMixin, DeleteView):
    model = Goal
    template_name = "true_north/goal_confirm_delete.html"
    success_url = reverse_lazy("true_north:goal-list")
    page_title = "Delete Goal"

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Goal deleted.")
        return super().form_valid(form)
# ---------------------------------------------------------------------------


class MilestoneListView(SiteContextMixin, RegistrationAcceptedMixin, ListView):
    model = Milestone
    template_name = "true_north/milestone_list.html"
    page_title = "Milestones"
    paginate_by = 20

    def get_queryset(self):
        return Milestone.objects.filter(user=self.request.user).order_by(
            "order", "description"
        )


class MilestoneCreateView(SiteContextMixin, RegistrationAcceptedMixin, CreateView):
    model = Milestone
    form_class = MilestoneForm
    template_name = "true_north/milestone_form.html"
    success_url = reverse_lazy("true_north:milestone-list")
    page_title = "Create Milestone"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Milestone created successfully.")
        return super().form_valid(form)


class MilestoneUpdateView(SiteContextMixin, RegistrationAcceptedMixin, UpdateView):
    model = Milestone
    form_class = MilestoneForm
    template_name = "true_north/milestone_form.html"
    success_url = reverse_lazy("true_north:milestone-list")
    page_title = "Update Milestone"

    def get_queryset(self):
        return Milestone.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Milestone updated successfully.")
        return super().form_valid(form)


class MilestoneDeleteView(SiteContextMixin, RegistrationAcceptedMixin, DeleteView):
    model = Milestone
    template_name = "true_north/milestone_confirm_delete.html"
    success_url = reverse_lazy("true_north:milestone-list")
    page_title = "Delete Milestone"

    def get_queryset(self):
        return Milestone.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Milestone deleted.")
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# ValueAction CRUD
# ---------------------------------------------------------------------------


class ValueActionListView(SiteContextMixin, RegistrationAcceptedMixin, ListView):
    model = ValueAction
    template_name = "true_north/valueaction_list.html"
    page_title = "Value Actions"
    paginate_by = 20

    def get_queryset(self):
        return ValueAction.objects.filter(user=self.request.user).order_by(
            "order", "id"
        )


class ValueActionCreateView(SiteContextMixin, RegistrationAcceptedMixin, CreateView):
    model = ValueAction
    form_class = ValueActionForm
    template_name = "true_north/valueaction_form.html"
    success_url = reverse_lazy("true_north:value-action-list")
    page_title = "Create Value Action"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Value Action created successfully.")
        return super().form_valid(form)


class ValueActionUpdateView(SiteContextMixin, RegistrationAcceptedMixin, UpdateView):
    model = ValueAction
    form_class = ValueActionForm
    template_name = "true_north/valueaction_form.html"
    success_url = reverse_lazy("true_north:value-action-list")
    page_title = "Update Value Action"

    def get_queryset(self):
        return ValueAction.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Value Action updated successfully.")
        return super().form_valid(form)


class ValueActionDeleteView(SiteContextMixin, RegistrationAcceptedMixin, DeleteView):
    model = ValueAction
    template_name = "true_north/valueaction_confirm_delete.html"
    success_url = reverse_lazy("true_north:value-action-list")
    page_title = "Delete Value Action"

    def get_queryset(self):
        return ValueAction.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Value Action deleted.")
        return super().form_valid(form)
