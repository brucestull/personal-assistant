from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from base.decorators import registration_accepted_required
from base.mixins import RegistrationAcceptedMixin

from .forms import ReminderForm, ReminderScheduleForm
from .models import Reminder, ReminderSchedule


# Dashboard view
class ReminderDashboardView(RegistrationAcceptedMixin, LoginRequiredMixin, ListView):
    """Dashboard showing all reminders for the current user."""
    
    model = Reminder
    template_name = "priority_deciderator/dashboard.html"
    context_object_name = "reminders"
    paginate_by = 20
    
    def get_queryset(self):
        return (
            Reminder.objects.filter(user=self.request.user)
            .prefetch_related("schedules")
            .order_by("-created")
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_count"] = self.get_queryset().filter(is_active=True).count()
        context["inactive_count"] = self.get_queryset().filter(is_active=False).count()
        return context


# Reminder CRUD views
class ReminderListView(RegistrationAcceptedMixin, LoginRequiredMixin, ListView):
    """List all reminders for the current user."""
    
    model = Reminder
    template_name = "priority_deciderator/reminder_list.html"
    context_object_name = "reminders"
    paginate_by = 20
    
    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user).order_by("-created")


class ReminderDetailView(RegistrationAcceptedMixin, LoginRequiredMixin, DetailView):
    """Detail view for a single reminder."""
    
    model = Reminder
    template_name = "priority_deciderator/reminder_detail.html"
    context_object_name = "reminder"
    
    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)


class ReminderCreateView(RegistrationAcceptedMixin, LoginRequiredMixin, CreateView):
    """Create a new reminder."""
    
    model = Reminder
    form_class = ReminderForm
    template_name = "priority_deciderator/reminder_form.html"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("priority_deciderator:reminder_detail", kwargs={"pk": self.object.pk})


class ReminderUpdateView(RegistrationAcceptedMixin, LoginRequiredMixin, UpdateView):
    """Update an existing reminder."""
    
    model = Reminder
    form_class = ReminderForm
    template_name = "priority_deciderator/reminder_form.html"
    
    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse("priority_deciderator:reminder_detail", kwargs={"pk": self.object.pk})


class ReminderDeleteView(RegistrationAcceptedMixin, LoginRequiredMixin, DeleteView):
    """Delete a reminder."""
    
    model = Reminder
    template_name = "priority_deciderator/reminder_confirm_delete.html"
    success_url = reverse_lazy("priority_deciderator:dashboard")
    
    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)


# Schedule views
@registration_accepted_required
def schedule_create(request, reminder_pk):
    """Create a new schedule for a reminder."""
    reminder = get_object_or_404(Reminder, pk=reminder_pk, user=request.user)
    
    if request.method == "POST":
        form = ReminderScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.reminder = reminder
            schedule.save()
            return redirect("priority_deciderator:reminder_detail", pk=reminder.pk)
    else:
        form = ReminderScheduleForm()
    
    return render(
        request,
        "priority_deciderator/schedule_form.html",
        {"form": form, "reminder": reminder},
    )


@registration_accepted_required
def schedule_update(request, pk):
    """Update a schedule."""
    schedule = get_object_or_404(
        ReminderSchedule,
        pk=pk,
        reminder__user=request.user,
    )
    
    if request.method == "POST":
        form = ReminderScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect(
                "priority_deciderator:reminder_detail",
                pk=schedule.reminder.pk,
            )
    else:
        form = ReminderScheduleForm(instance=schedule)
    
    return render(
        request,
        "priority_deciderator/schedule_form.html",
        {"form": form, "reminder": schedule.reminder, "schedule": schedule},
    )


@registration_accepted_required
def schedule_delete(request, pk):
    """Delete a schedule."""
    schedule = get_object_or_404(
        ReminderSchedule,
        pk=pk,
        reminder__user=request.user,
    )
    reminder_pk = schedule.reminder.pk
    
    if request.method == "POST":
        schedule.delete()
        return redirect("priority_deciderator:reminder_detail", pk=reminder_pk)
    
    return render(
        request,
        "priority_deciderator/schedule_confirm_delete.html",
        {"schedule": schedule},
    )
