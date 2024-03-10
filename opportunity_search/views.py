from .models import WorkSearchActivity
from django.views.generic import ListView
from base.mixins import RegistrationAcceptedMixin


class WorkSearchActivityListView(RegistrationAcceptedMixin, ListView):
    model = WorkSearchActivity
    # template_name = 'opportunity_search/work_search_activity_list.html'
    # context_object_name = 'work_search_activities'
    # paginate_by = 10

    # def get_queryset(self):
    #     return WorkSearchActivity.objects.filter(user=self.request.user).order_by('-date_created'
