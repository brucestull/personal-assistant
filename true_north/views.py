# true_north/views.py

import json

from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from django.views.generic.edit import CreateView
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from base.mixins import RegistrationAcceptedMixin, SiteContextMixin
from true_north.forms import (
    CoreValueEmailScheduleForm,
    CoreValueForm,
    GoalForm,
    MilestoneForm,
    ObjectEmailScheduleForm,
    ValueActionForm,
)
from true_north.models import CoreValue, CoreValueEmailSchedule, Goal, GoalStatus, Milestone, ValueAction, ValueActionStatus  # noqa E501
from true_north.tasks import (
    send_core_value_email,
    send_corevalue_reminder_email,
    send_goal_email,
    send_milestone_email,
    send_true_north_email,
    send_value_action_email,
)
from true_north.utils import periodic_task_name


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


class CoreValueDetailView(
    SiteContextMixin, RegistrationAcceptedMixin, LoginRequiredMixin, DetailView
):
    model = CoreValue
    template_name = "true_north/corevalue_detail.html"
    page_title = "Core Value Detail"

    def get_queryset(self):
        return CoreValue.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["goals"] = self.object.goals.filter(
            user=self.request.user
        ).prefetch_related("milestones").order_by("order", "title")
        ctx["email_schedules"] = self.object.email_schedules.filter(
            user=self.request.user
        ).order_by("-created")
        ctx["schedule_task"] = PeriodicTask.objects.filter(
            name=periodic_task_name("CoreValue", self.object.pk)
        ).first()
        ctx["can_schedule"] = self.request.user.has_perm(
            "django_celery_beat.add_periodictask"
        )
        return ctx


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


class GoalDetailView(
    SiteContextMixin, RegistrationAcceptedMixin, LoginRequiredMixin, DetailView
):
    model = Goal
    template_name = "true_north/goal_detail.html"
    page_title = "Goal Detail"

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["milestones"] = self.object.milestones.filter(
            user=self.request.user
        ).prefetch_related("tasks").order_by("order", "description")
        ctx["schedule_task"] = PeriodicTask.objects.filter(
            name=periodic_task_name("Goal", self.object.pk)
        ).first()
        ctx["can_schedule"] = self.request.user.has_perm(
            "django_celery_beat.add_periodictask"
        )
        return ctx


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


class MilestoneDetailView(
    SiteContextMixin, RegistrationAcceptedMixin, LoginRequiredMixin, DetailView
):
    model = Milestone
    template_name = "true_north/milestone_detail.html"
    page_title = "Milestone Detail"

    def get_queryset(self):
        return Milestone.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["value_actions"] = self.object.tasks.filter(
            user=self.request.user
        ).order_by("order", "id")
        ctx["schedule_task"] = PeriodicTask.objects.filter(
            name=periodic_task_name("Milestone", self.object.pk)
        ).first()
        ctx["can_schedule"] = self.request.user.has_perm(
            "django_celery_beat.add_periodictask"
        )
        return ctx


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


class ValueActionDetailView(
    SiteContextMixin, RegistrationAcceptedMixin, LoginRequiredMixin, DetailView
):
    model = ValueAction
    template_name = "true_north/valueaction_detail.html"
    page_title = "Value Action Detail"

    def get_queryset(self):
        return ValueAction.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["schedule_task"] = PeriodicTask.objects.filter(
            name=periodic_task_name("ValueAction", self.object.pk)
        ).first()
        ctx["can_schedule"] = self.request.user.has_perm(
            "django_celery_beat.add_periodictask"
        )
        return ctx


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


# ---------------------------------------------------------------------------
# Send-Email views (POST only — one per model)
# ---------------------------------------------------------------------------


class CoreValueSendEmailView(
    SiteContextMixin, RegistrationAcceptedMixin, LoginRequiredMixin, DetailView
):
    """POST to queue an email containing this Core Value's details."""

    model = CoreValue
    http_method_names = ["post"]

    def get_queryset(self):
        return CoreValue.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        send_true_north_email.delay("CoreValue", obj.pk)
        messages.success(
            request,
            f'Email for Core Value "{obj.name}" has been queued for sending.',
        )
        return redirect("true_north:core-value-list")


class GoalSendEmailView(
    SiteContextMixin, RegistrationAcceptedMixin, LoginRequiredMixin, DetailView
):
    """POST to queue an email containing this Goal's details."""

    model = Goal
    http_method_names = ["post"]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        send_goal_email.delay(request.user.id, obj.pk)
        messages.success(
            request,
            f'Email for Goal "{obj.title}" has been queued for sending.',
        )
        return redirect("true_north:goal-list")


class MilestoneSendEmailView(
    SiteContextMixin, RegistrationAcceptedMixin, LoginRequiredMixin, DetailView
):
    """POST to queue an email containing this Milestone's details."""

    model = Milestone
    http_method_names = ["post"]

    def get_queryset(self):
        return Milestone.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        send_milestone_email.delay(request.user.id, obj.pk)
        messages.success(
            request,
            f'Email for Milestone "{obj.description[:80]}" '
            "has been queued for sending.",
        )
        return redirect("true_north:milestone-list")


class ValueActionSendEmailView(
    SiteContextMixin, RegistrationAcceptedMixin, LoginRequiredMixin, DetailView
):
    """POST to queue an email containing this Value Action's details."""

    model = ValueAction
    http_method_names = ["post"]

    def get_queryset(self):
        return ValueAction.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        send_value_action_email.delay(request.user.id, obj.pk)
        messages.success(
            request,
            f'Email for Value Action "{obj.content[:80]}" has been queued for sending.',
        )
        return redirect("true_north:value-action-list")


# ---------------------------------------------------------------------------
# PeriodicTask Schedule CRUD + Send-Now
# ---------------------------------------------------------------------------


class SchedulePermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = (
        "django_celery_beat.add_crontabschedule",
        "django_celery_beat.add_periodictask",
        "django_celery_beat.change_periodictask",
        "django_celery_beat.delete_periodictask",
    )
    raise_exception = False

    def handle_no_permission(self):
        messages.error(
            self.request,
            "Your account isn't set up for scheduled emails. "
            "Ask an admin to add you to the ScheduledTaskUsers group.",
        )
        return redirect("true_north:dashboard")


class ObjectScheduleBaseView(
    SiteContextMixin, RegistrationAcceptedMixin, SchedulePermissionMixin, View
):
    model = None
    model_name = ""
    object_type = ""
    detail_url_name = ""
    task_path = ""
    template_name = "true_north/schedule_form.html"
    delete_template_name = "true_north/schedule_confirm_delete.html"

    def get_object(self, request, pk):
        return get_object_or_404(self.model, pk=pk, user=request.user)

    def get_task_name(self, pk):
        return periodic_task_name(self.model_name, pk)

    def get_task(self, pk):
        return PeriodicTask.objects.filter(name=self.get_task_name(pk)).first()

    def get_or_create_crontab(self, data):
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=data["minute"],
            hour=data["hour"],
            day_of_week=data["day_of_week"],
            day_of_month="*",
            month_of_year="*",
        )
        return schedule

    def get_common_context(self, obj, form, editing=False):
        return {
            "form": form,
            "object": obj,
            "object_type": self.object_type,
            "editing": editing,
            "cancel_url": reverse(self.detail_url_name, kwargs={"pk": obj.pk}),
        }


class ObjectScheduleCreateView(ObjectScheduleBaseView):
    def get(self, request, pk):
        obj = self.get_object(request, pk)
        if self.get_task(pk):
            return redirect(self.edit_url_name, pk=pk)
        return render(
            request,
            self.template_name,
            self.get_common_context(obj, ObjectEmailScheduleForm(), editing=False),
        )

    def post(self, request, pk):
        obj = self.get_object(request, pk)
        task_name = self.get_task_name(pk)
        if PeriodicTask.objects.filter(name=task_name).exists():
            return redirect(self.edit_url_name, pk=pk)

        form = ObjectEmailScheduleForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                self.template_name,
                self.get_common_context(obj, form, editing=False),
            )

        data = form.cleaned_data
        schedule = self.get_or_create_crontab(data)
        PeriodicTask.objects.create(
            name=task_name,
            task=self.task_path,
            crontab=schedule,
            enabled=data["enabled"],
            args=json.dumps([request.user.pk, obj.pk]),
        )
        messages.success(request, f'Email schedule created for "{obj}".')
        return redirect(self.detail_url_name, pk=pk)


class ObjectScheduleEditView(ObjectScheduleBaseView):
    def get(self, request, pk):
        obj = self.get_object(request, pk)
        task = get_object_or_404(PeriodicTask, name=self.get_task_name(pk))
        form = ObjectEmailScheduleForm(
            initial={
                "hour": task.crontab.hour if task.crontab else "9",
                "minute": task.crontab.minute if task.crontab else "0",
                "day_of_week": task.crontab.day_of_week if task.crontab else "*",
                "enabled": task.enabled,
            }
        )
        return render(
            request,
            self.template_name,
            self.get_common_context(obj, form, editing=True),
        )

    def post(self, request, pk):
        obj = self.get_object(request, pk)
        task = get_object_or_404(PeriodicTask, name=self.get_task_name(pk))
        form = ObjectEmailScheduleForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                self.template_name,
                self.get_common_context(obj, form, editing=True),
            )

        data = form.cleaned_data
        schedule = self.get_or_create_crontab(data)
        task.crontab = schedule
        task.enabled = data["enabled"]
        task.task = self.task_path
        task.args = json.dumps([request.user.pk, obj.pk])
        task.save(update_fields=["crontab", "enabled", "task", "args"])
        messages.success(request, f'Email schedule updated for "{obj}".')
        return redirect(self.detail_url_name, pk=pk)


class ObjectScheduleDeleteView(ObjectScheduleBaseView):
    def get(self, request, pk):
        obj = self.get_object(request, pk)
        task = get_object_or_404(PeriodicTask, name=self.get_task_name(pk))
        return render(
            request,
            self.delete_template_name,
            {
                "object": obj,
                "object_type": self.object_type,
                "schedule_task": task,
                "cancel_url": reverse(self.detail_url_name, kwargs={"pk": obj.pk}),
            },
        )

    def post(self, request, pk):
        obj = self.get_object(request, pk)
        PeriodicTask.objects.filter(name=self.get_task_name(pk)).delete()
        messages.success(request, f'Email schedule removed for "{obj}".')
        return redirect(self.detail_url_name, pk=pk)


class ObjectScheduleSendNowView(ObjectScheduleBaseView):
    send_task = None

    def post(self, request, pk):
        self.get_object(request, pk)
        self.send_task.delay(request.user.pk, pk)
        messages.success(
            request,
            "Email sent! Check your inbox (or terminal if using console backend).",
        )
        return redirect(self.detail_url_name, pk=pk)


class CoreValueScheduleCreateView(ObjectScheduleCreateView):
    model = CoreValue
    model_name = "CoreValue"
    object_type = "Core Value"
    detail_url_name = "true_north:core-value-detail"
    edit_url_name = "true_north:core-value-schedule-edit"
    task_path = "true_north.tasks.send_core_value_email"


class CoreValueScheduleEditView(ObjectScheduleEditView):
    model = CoreValue
    model_name = "CoreValue"
    object_type = "Core Value"
    detail_url_name = "true_north:core-value-detail"
    task_path = "true_north.tasks.send_core_value_email"


class CoreValueScheduleDeleteView(ObjectScheduleDeleteView):
    model = CoreValue
    model_name = "CoreValue"
    object_type = "Core Value"
    detail_url_name = "true_north:core-value-detail"


class CoreValueScheduleSendNowView(ObjectScheduleSendNowView):
    model = CoreValue
    model_name = "CoreValue"
    object_type = "Core Value"
    detail_url_name = "true_north:core-value-detail"
    send_task = send_core_value_email


class GoalScheduleCreateView(ObjectScheduleCreateView):
    model = Goal
    model_name = "Goal"
    object_type = "Goal"
    detail_url_name = "true_north:goal-detail"
    edit_url_name = "true_north:goal-schedule-edit"
    task_path = "true_north.tasks.send_goal_email"


class GoalScheduleEditView(ObjectScheduleEditView):
    model = Goal
    model_name = "Goal"
    object_type = "Goal"
    detail_url_name = "true_north:goal-detail"
    task_path = "true_north.tasks.send_goal_email"


class GoalScheduleDeleteView(ObjectScheduleDeleteView):
    model = Goal
    model_name = "Goal"
    object_type = "Goal"
    detail_url_name = "true_north:goal-detail"


class GoalScheduleSendNowView(ObjectScheduleSendNowView):
    model = Goal
    model_name = "Goal"
    object_type = "Goal"
    detail_url_name = "true_north:goal-detail"
    send_task = send_goal_email


class MilestoneScheduleCreateView(ObjectScheduleCreateView):
    model = Milestone
    model_name = "Milestone"
    object_type = "Milestone"
    detail_url_name = "true_north:milestone-detail"
    edit_url_name = "true_north:milestone-schedule-edit"
    task_path = "true_north.tasks.send_milestone_email"


class MilestoneScheduleEditView(ObjectScheduleEditView):
    model = Milestone
    model_name = "Milestone"
    object_type = "Milestone"
    detail_url_name = "true_north:milestone-detail"
    task_path = "true_north.tasks.send_milestone_email"


class MilestoneScheduleDeleteView(ObjectScheduleDeleteView):
    model = Milestone
    model_name = "Milestone"
    object_type = "Milestone"
    detail_url_name = "true_north:milestone-detail"


class MilestoneScheduleSendNowView(ObjectScheduleSendNowView):
    model = Milestone
    model_name = "Milestone"
    object_type = "Milestone"
    detail_url_name = "true_north:milestone-detail"
    send_task = send_milestone_email


class ValueActionScheduleCreateView(ObjectScheduleCreateView):
    model = ValueAction
    model_name = "ValueAction"
    object_type = "Value Action"
    detail_url_name = "true_north:value-action-detail"
    edit_url_name = "true_north:value-action-schedule-edit"
    task_path = "true_north.tasks.send_value_action_email"


class ValueActionScheduleEditView(ObjectScheduleEditView):
    model = ValueAction
    model_name = "ValueAction"
    object_type = "Value Action"
    detail_url_name = "true_north:value-action-detail"
    task_path = "true_north.tasks.send_value_action_email"


class ValueActionScheduleDeleteView(ObjectScheduleDeleteView):
    model = ValueAction
    model_name = "ValueAction"
    object_type = "Value Action"
    detail_url_name = "true_north:value-action-detail"


class ValueActionScheduleSendNowView(ObjectScheduleSendNowView):
    model = ValueAction
    model_name = "ValueAction"
    object_type = "Value Action"
    detail_url_name = "true_north:value-action-detail"
    send_task = send_value_action_email


# ---------------------------------------------------------------------------
# CoreValueEmailSchedule CRUD + Send-Now
# ---------------------------------------------------------------------------


class CoreValueEmailScheduleListView(
    SiteContextMixin, RegistrationAcceptedMixin, LoginRequiredMixin, ListView
):
    model = CoreValueEmailSchedule
    template_name = "true_north/corevalue_email_schedule_list.html"
    page_title = "Core Value Email Schedules"
    paginate_by = 20

    def get_queryset(self):
        return CoreValueEmailSchedule.objects.filter(
            user=self.request.user
        ).select_related("core_value").order_by("-created")


class CoreValueEmailScheduleCreateView(
    SiteContextMixin, RegistrationAcceptedMixin, LoginRequiredMixin, CreateView
):
    model = CoreValueEmailSchedule
    form_class = CoreValueEmailScheduleForm
    template_name = "true_north/corevalue_email_schedule_form.html"
    success_url = reverse_lazy("true_north:corevalue-email-schedule-list")
    page_title = "Schedule Core Value Email Reminder"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        core_value_id = self.request.GET.get("core_value")
        if core_value_id:
            initial["core_value"] = core_value_id
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.next_send = form.instance.compute_next_send()
        messages.success(self.request, "Email reminder schedule created.")
        return super().form_valid(form)


class CoreValueEmailScheduleUpdateView(
    SiteContextMixin,
    RegistrationAcceptedMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView,
):
    model = CoreValueEmailSchedule
    form_class = CoreValueEmailScheduleForm
    template_name = "true_north/corevalue_email_schedule_form.html"
    success_url = reverse_lazy("true_north:corevalue-email-schedule-list")
    page_title = "Update Core Value Email Reminder"

    def get_queryset(self):
        return CoreValueEmailSchedule.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        form.instance.next_send = form.instance.compute_next_send()
        messages.success(self.request, "Email reminder schedule updated.")
        return super().form_valid(form)


class CoreValueEmailScheduleDeleteView(
    SiteContextMixin,
    RegistrationAcceptedMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView,
):
    model = CoreValueEmailSchedule
    template_name = "true_north/corevalue_email_schedule_confirm_delete.html"
    success_url = reverse_lazy("true_north:corevalue-email-schedule-list")
    page_title = "Delete Core Value Email Reminder"

    def get_queryset(self):
        return CoreValueEmailSchedule.objects.filter(user=self.request.user)

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Email reminder schedule deleted.")
        return super().form_valid(form)


class CoreValueEmailScheduleSendNowView(
    SiteContextMixin,
    RegistrationAcceptedMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
    DetailView,
):
    """POST to immediately queue a reminder email for this schedule."""

    model = CoreValueEmailSchedule
    http_method_names = ["post"]

    def get_queryset(self):
        return CoreValueEmailSchedule.objects.filter(user=self.request.user)

    def test_func(self):
        return self.get_object().user == self.request.user

    def post(self, request, *args, **kwargs):
        schedule = self.get_object()
        send_corevalue_reminder_email.delay(schedule.pk)
        schedule.next_send = schedule.compute_next_send()
        schedule.last_sent = timezone.now()
        schedule.save(update_fields=["next_send", "last_sent"])
        messages.success(request, "Reminder email queued for sending.")
        return redirect("true_north:corevalue-email-schedule-list")
