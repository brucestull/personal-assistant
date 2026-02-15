# true_north/views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from base.mixins import RegistrationAcceptedMixin, SiteContextMixin
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
