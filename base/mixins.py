# base/mixins.py

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


class UserIsAuthorMixin(AccessMixin):
    """
    Mixin to check if the user is the author of the object.
    """

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is the author of the object
        if not request.user == self.get_object().author:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class OrderableMixin:
    """
    Mixin to add `reorder_all` class method to models with an 'order' field.
    """

    @classmethod
    def reorder_all(cls):
        for index, item in enumerate(cls.objects.all().order_by("order")):
            item.order = index
            item.save()
