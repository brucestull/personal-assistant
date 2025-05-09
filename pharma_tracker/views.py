from django.views.generic import ListView

from base.mixins import RegistrationAcceptedMixin

# We import like this so that we don't have to rely on the package name
# which contains the pharmaceutical model. This makes it easier to add
# this appliation to other projects.
from .models import Pharmaceutical


class PharmaceuticalListView(RegistrationAcceptedMixin, ListView):
    """
    'ListView' for 'Pharmaceutical' model. This view is only accessible
    to users who are authenticated and have 'registration_accepted' set
    to 'True'. The view returns a list of all 'Pharmaceutical' objects
    owned by the user.
    """

    model = Pharmaceutical

    def get_queryset(self):
        """
        This method is used by 'ListView' to determine which objects to
        return. We override it to return only 'Pharmaceutical' objects
        owned by the user.
        """

        user = self.request.user
        return Pharmaceutical.objects.filter(user=user)
