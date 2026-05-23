from rest_framework import permissions, viewsets

from base.permissions import RegistrationAcceptedPermission

from .models import Thought
from .serializers import ThoughtSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class ThoughtViewSet(viewsets.ModelViewSet):
    serializer_class = ThoughtSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        RegistrationAcceptedPermission,
        IsOwner,
    ]

    def get_queryset(self):
        return Thought.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
