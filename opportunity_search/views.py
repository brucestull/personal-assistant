from django.views.generic import ListView

from base.mixins import RegistrationAcceptedMixin

from .models import WorkSearchActivity


class WorkSearchActivityListView(RegistrationAcceptedMixin, ListView):
    model = WorkSearchActivity
