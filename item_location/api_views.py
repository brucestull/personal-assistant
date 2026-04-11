from rest_framework import permissions, viewsets

from .models import Item, StorageLocation
from .serializers import ItemSerializer, StorageLocationSerializer


class IsOwner(permissions.BasePermission):
    """Only allow owners of an object to access it."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class StorageLocationViewSet(viewsets.ModelViewSet):
    serializer_class = StorageLocationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return StorageLocation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user).select_related("location")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
