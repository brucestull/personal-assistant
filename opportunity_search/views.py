from .models import WorkSearchActivity
from django.views.generic import ListView
from base.mixins import RegistrationAcceptedMixin


class WorkSearchActivityListView(RegistrationAcceptedMixin, ListView):
    model = WorkSearchActivity
