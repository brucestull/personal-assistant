# storager/views.py

from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from base.mixins import RegistrationAcceptedMixin

from .models import Item, SortDecision, StorageArea, Type


# Storage Type Views
class TypeListView(RegistrationAcceptedMixin, ListView):
    model = Type


class TypeDetailView(RegistrationAcceptedMixin, DetailView):
    model = Type


class TypeCreateView(RegistrationAcceptedMixin, CreateView):
    model = Type
    fields = ["name", "description"]
    success_url = reverse_lazy("storager:type_list")


class TypeUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = Type
    fields = ["name", "description"]
    success_url = reverse_lazy("storager:type_list")


class TypeDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = Type
    success_url = reverse_lazy("storager:type_list")


# StorageArea Views
class StorageAreaListView(RegistrationAcceptedMixin, ListView):
    model = StorageArea


class StorageAreaDetailView(RegistrationAcceptedMixin, DetailView):
    model = StorageArea


class StorageAreaCreateView(RegistrationAcceptedMixin, CreateView):
    model = StorageArea
    fields = ["name", "description", "type"]
    success_url = reverse_lazy("storager:storagearea_list")


class StorageAreaUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = StorageArea
    fields = ["name", "description", "type"]
    success_url = reverse_lazy("storager:storagearea_list")


class StorageAreaDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = StorageArea
    success_url = reverse_lazy("storager:storagearea_list")


# SortDecision Views
class SortDecisionListView(RegistrationAcceptedMixin, ListView):
    model = SortDecision


class SortDecisionDetailView(RegistrationAcceptedMixin, DetailView):
    model = SortDecision


class SortDecisionCreateView(RegistrationAcceptedMixin, CreateView):
    model = SortDecision
    fields = ["text"]
    success_url = reverse_lazy("storager:sortdecision_list")


class SortDecisionUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = SortDecision
    fields = ["text"]
    success_url = reverse_lazy("storager:sortdecision_list")


class SortDecisionDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = SortDecision
    success_url = reverse_lazy("storager:sortdecision_list")


# Item Views
class ItemListView(RegistrationAcceptedMixin, ListView):
    model = Item

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)


class ItemDetailView(RegistrationAcceptedMixin, DetailView):
    model = Item

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)


class ItemCreateView(RegistrationAcceptedMixin, CreateView):
    model = Item
    fields = ["name", "description", "notes"]
    success_url = reverse_lazy("storager:item_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ItemUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = Item
    fields = ["name", "description", "notes"]
    success_url = reverse_lazy("storager:item_list")

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)


class ItemDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = Item
    success_url = reverse_lazy("storager:item_list")

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)
