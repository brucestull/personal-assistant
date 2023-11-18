from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


class RegistrationAcceptedMixin(AccessMixin):
    """
    Mixin to check if the user is authenticated and their registration is accepted.
    """

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated and if registration is accepted
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.registration_accepted:
            raise PermissionDenied("Your registration has not been accepted yet.")
        return super().dispatch(request, *args, **kwargs)
