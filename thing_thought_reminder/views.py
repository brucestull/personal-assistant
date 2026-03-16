from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from base.mixins import RegistrationAcceptedMixin, SiteContextMixin

from .forms import ReminderScheduleForm, ThingForm, ThoughtForm
from .models import ReminderSchedule, Thing, Thought
from .tasks import send_reminder_email


# ─────────────────────────────────────────────────────────────────────────────
# Dashboard


class DashboardView(SiteContextMixin, RegistrationAcceptedMixin, TemplateView):
    template_name = "thing_thought_reminder/dashboard.html"
    page_title = "Thing & Thought Reminders"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["thing_count"] = Thing.objects.filter(user=user).count()
        context["thought_count"] = Thought.objects.filter(user=user).count()
        context["schedule_count"] = ReminderSchedule.objects.filter(user=user).count()
        context["recent_things"] = Thing.objects.filter(user=user)[:5]
        context["recent_thoughts"] = Thought.objects.filter(user=user)[:5]
        return context


# ─────────────────────────────────────────────────────────────────────────────
# Thing CRUD


class ThingListView(SiteContextMixin, RegistrationAcceptedMixin, ListView):
    model = Thing
    template_name = "thing_thought_reminder/thing_list.html"
    page_title = "My Things"
    paginate_by = 20

    def get_queryset(self):
        return Thing.objects.filter(user=self.request.user)


class ThingDetailView(SiteContextMixin, RegistrationAcceptedMixin, DetailView):
    model = Thing
    template_name = "thing_thought_reminder/thing_detail.html"
    page_title = "Thing Detail"

    def get_queryset(self):
        return Thing.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reminder_schedules"] = self.object.reminder_schedules.all()
        context["reminder_form"] = ReminderScheduleForm(
            user=self.request.user,
            initial={"thing": self.object},
        )
        return context


class ThingCreateView(SiteContextMixin, RegistrationAcceptedMixin, CreateView):
    model = Thing
    form_class = ThingForm
    template_name = "thing_thought_reminder/thing_form.html"
    success_url = reverse_lazy("thing_thought_reminder:thing-list")
    page_title = "Add Thing"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Thing saved.")
        return super().form_valid(form)


class ThingUpdateView(
    SiteContextMixin, RegistrationAcceptedMixin, UserPassesTestMixin, UpdateView
):
    model = Thing
    form_class = ThingForm
    template_name = "thing_thought_reminder/thing_form.html"
    success_url = reverse_lazy("thing_thought_reminder:thing-list")

    def get_page_title(self):
        return "Edit Thing"

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Thing updated.")
        return super().form_valid(form)


class ThingDeleteView(
    SiteContextMixin, RegistrationAcceptedMixin, UserPassesTestMixin, DeleteView
):
    model = Thing
    template_name = "thing_thought_reminder/thing_confirm_delete.html"
    success_url = reverse_lazy("thing_thought_reminder:thing-list")
    page_title = "Delete Thing"

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Thing deleted.")
        return super().form_valid(form)


# ─────────────────────────────────────────────────────────────────────────────
# Thought CRUD


class ThoughtListView(SiteContextMixin, RegistrationAcceptedMixin, ListView):
    model = Thought
    template_name = "thing_thought_reminder/thought_list.html"
    page_title = "My Thoughts"
    paginate_by = 20

    def get_queryset(self):
        return Thought.objects.filter(user=self.request.user)


class ThoughtDetailView(SiteContextMixin, RegistrationAcceptedMixin, DetailView):
    model = Thought
    template_name = "thing_thought_reminder/thought_detail.html"
    page_title = "Thought Detail"

    def get_queryset(self):
        return Thought.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reminder_schedules"] = self.object.reminder_schedules.all()
        context["reminder_form"] = ReminderScheduleForm(
            user=self.request.user,
            initial={"thought": self.object},
        )
        return context


class ThoughtCreateView(SiteContextMixin, RegistrationAcceptedMixin, CreateView):
    model = Thought
    form_class = ThoughtForm
    template_name = "thing_thought_reminder/thought_form.html"
    success_url = reverse_lazy("thing_thought_reminder:thought-list")
    page_title = "Add Thought"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Thought saved.")
        return super().form_valid(form)


class ThoughtUpdateView(
    SiteContextMixin, RegistrationAcceptedMixin, UserPassesTestMixin, UpdateView
):
    model = Thought
    form_class = ThoughtForm
    template_name = "thing_thought_reminder/thought_form.html"
    success_url = reverse_lazy("thing_thought_reminder:thought-list")

    def get_page_title(self):
        return "Edit Thought"

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Thought updated.")
        return super().form_valid(form)


class ThoughtDeleteView(
    SiteContextMixin, RegistrationAcceptedMixin, UserPassesTestMixin, DeleteView
):
    model = Thought
    template_name = "thing_thought_reminder/thought_confirm_delete.html"
    success_url = reverse_lazy("thing_thought_reminder:thought-list")
    page_title = "Delete Thought"

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Thought deleted.")
        return super().form_valid(form)


# ─────────────────────────────────────────────────────────────────────────────
# ReminderSchedule CRUD


class ReminderScheduleListView(SiteContextMixin, RegistrationAcceptedMixin, ListView):
    model = ReminderSchedule
    template_name = "thing_thought_reminder/reminderschedule_list.html"
    page_title = "Reminder Schedules"
    paginate_by = 20

    def get_queryset(self):
        return ReminderSchedule.objects.filter(user=self.request.user).select_related(
            "thing", "thought"
        )


class ReminderScheduleDetailView(
    SiteContextMixin, RegistrationAcceptedMixin, DetailView
):
    model = ReminderSchedule
    template_name = "thing_thought_reminder/reminderschedule_detail.html"
    page_title = "Reminder Schedule Detail"

    def get_queryset(self):
        return ReminderSchedule.objects.filter(user=self.request.user)


class ReminderScheduleCreateView(
    SiteContextMixin, RegistrationAcceptedMixin, CreateView
):
    model = ReminderSchedule
    form_class = ReminderScheduleForm
    template_name = "thing_thought_reminder/reminderschedule_form.html"
    success_url = reverse_lazy("thing_thought_reminder:reminder-list")
    page_title = "Schedule a Reminder"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        # Pre-select a thing or thought if passed as a query param
        thing_id = self.request.GET.get("thing")
        thought_id = self.request.GET.get("thought")
        if thing_id:
            initial["thing"] = thing_id
        if thought_id:
            initial["thought"] = thought_id
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.next_send = form.instance.compute_next_send()
        messages.success(self.request, "Reminder schedule created.")
        return super().form_valid(form)


class ReminderScheduleUpdateView(
    SiteContextMixin, RegistrationAcceptedMixin, UserPassesTestMixin, UpdateView
):
    model = ReminderSchedule
    form_class = ReminderScheduleForm
    template_name = "thing_thought_reminder/reminderschedule_form.html"
    success_url = reverse_lazy("thing_thought_reminder:reminder-list")

    def get_page_title(self):
        return "Edit Reminder Schedule"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Reminder schedule updated.")
        return super().form_valid(form)


class ReminderScheduleDeleteView(
    SiteContextMixin, RegistrationAcceptedMixin, UserPassesTestMixin, DeleteView
):
    model = ReminderSchedule
    template_name = "thing_thought_reminder/reminderschedule_confirm_delete.html"
    success_url = reverse_lazy("thing_thought_reminder:reminder-list")
    page_title = "Delete Reminder Schedule"

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Reminder schedule deleted.")
        return super().form_valid(form)


class ReminderScheduleSendNowView(
    SiteContextMixin, RegistrationAcceptedMixin, UserPassesTestMixin, DetailView
):
    """
    POST to this view to immediately send a reminder email for this schedule.
    """

    model = ReminderSchedule
    template_name = "thing_thought_reminder/reminderschedule_send_now.html"
    page_title = "Send Reminder Now"
    http_method_names = ["get", "post"]

    def get_queryset(self):
        return ReminderSchedule.objects.filter(user=self.request.user)

    def test_func(self):
        return self.get_object().user == self.request.user

    def post(self, request, *args, **kwargs):
        from django.shortcuts import redirect

        schedule = self.get_object()
        # Dispatch Celery task for immediate send
        send_reminder_email.delay(schedule.pk)
        # Optimistically update next_send
        schedule.next_send = schedule.compute_next_send()
        schedule.last_sent = timezone.now()
        schedule.save(update_fields=["next_send", "last_sent"])
        messages.success(request, "Reminder email queued for sending.")
        return redirect("thing_thought_reminder:reminder-detail", pk=schedule.pk)

