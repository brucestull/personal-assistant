from django.views.generic import ListView

from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME

from .models import Goal


class GoalListView(RegistrationAcceptedMixin, ListView):
    """
    A view that displays a list of goals.
    """

    model = Goal
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Goals",
    }

    # def get_queryset(self):
    #     return super().get_queryset().filter(author=self.request.user)
