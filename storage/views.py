# storage/views.py

from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from base.mixins import RegistrationAcceptedMixin

from .models import StorageArea, Type


# Storage Type Views
class TypeListView(RegistrationAcceptedMixin, ListView):
    model = Type


class TypeDetailView(RegistrationAcceptedMixin, DetailView):
    model = Type


class TypeCreateView(RegistrationAcceptedMixin, CreateView):
    model = Type
    fields = ["name", "description"]
    success_url = reverse_lazy("type_list")


class TypeUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = Type
    fields = ["name", "description"]
    success_url = reverse_lazy("type_list")


class TypeDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = Type
    success_url = reverse_lazy("type_list")


# StorageArea Views
class StorageAreaListView(RegistrationAcceptedMixin, ListView):
    model = StorageArea


class StorageAreaDetailView(RegistrationAcceptedMixin, DetailView):
    model = StorageArea


class StorageAreaCreateView(RegistrationAcceptedMixin, CreateView):
    model = StorageArea
    fields = ["name", "description", "type"]
    success_url = reverse_lazy("storagearea_list")


class StorageAreaUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = StorageArea
    fields = ["name", "description", "type"]
    success_url = reverse_lazy("storagearea_list")


class StorageAreaDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = StorageArea
    success_url = reverse_lazy("storagearea_list")
