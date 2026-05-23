from rest_framework import permissions


class RegistrationAcceptedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and getattr(request.user, "registration_accepted", False)
        )
