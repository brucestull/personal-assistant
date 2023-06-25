from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView

from .models import ValuedGoal, CoreValue


# This `@user_passes_test` decorator ensures that only staff users (is_staff == True) can access this view.
@user_passes_test(lambda u: u.is_staff)
def html_response(request):
    return HttpResponse(
        f"Hello, world. You're at the valued_goals html response."
        f"<br>"
        f"<a href='/'>Home</a>"
        f"<br>"
        f"<a href='/valued-goals/goals/'>Goals</a>"
        f"<br>"
        f"<a href='/admin/valued_goals/corevalue/'>Core Values: Django Admin</a>"
        f"<br>"
        f"<a href='/admin/valued_goals/valuedgoal/'>Valued Goal: Django Admin</a>"
    )


@login_required
def goals(request):
    goals = ValuedGoal.objects.filter(user=request.user)
    return render(
        request,
        "valued_goals/goals.html",
        {"goals": goals},
    )


class GoalsCreateView(CreateView):
    """
    View for creating a valued goal.
    """

    model = ValuedGoal
    fields = ["name", "description"]
    success_url = reverse_lazy("valued_goals:goals-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class GoalsUpdateView(UpdateView):
    """
    View for updating a valued goal.
    """

    model = ValuedGoal
    fields = ["name", "description"]
    success_url = reverse_lazy(
        "valued_goals:goals-detail",
        kwargs={"pk": 1},
    )

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class GoalsDetailView(DetailView):
    """
    View for displaying a valued goal.
    """

    model = ValuedGoal
