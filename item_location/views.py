from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from base.mixins import RegistrationAcceptedMixin, SiteContextMixin

from .forms import ItemForm, StorageLocationForm
from .models import Item, StorageLocation


# ─────────────────────────────────────────────────────────────────────────────
# Dashboard


class DashboardView(SiteContextMixin, RegistrationAcceptedMixin, TemplateView):
    template_name = "item_location/dashboard.html"
    page_title = "Item Location"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["location_count"] = StorageLocation.objects.filter(user=user).count()
        context["item_count"] = Item.objects.filter(user=user).count()
        context["recent_locations"] = StorageLocation.objects.filter(user=user)[:5]
        context["recent_items"] = Item.objects.filter(user=user)[:5]
        return context


# ─────────────────────────────────────────────────────────────────────────────
# StorageLocation CRUD


class StorageLocationListView(SiteContextMixin, RegistrationAcceptedMixin, ListView):
    model = StorageLocation
    template_name = "item_location/storagelocation_list.html"
    page_title = "Storage Locations"
    paginate_by = 20

    def get_queryset(self):
        return StorageLocation.objects.filter(user=self.request.user)


class StorageLocationDetailView(
    SiteContextMixin, RegistrationAcceptedMixin, DetailView
):
    model = StorageLocation
    template_name = "item_location/storagelocation_detail.html"
    page_title = "Location Detail"

    def get_queryset(self):
        return StorageLocation.objects.filter(user=self.request.user)


class StorageLocationCreateView(
    SiteContextMixin, RegistrationAcceptedMixin, CreateView
):
    model = StorageLocation
    form_class = StorageLocationForm
    template_name = "item_location/storagelocation_form.html"
    success_url = reverse_lazy("item_location:location-list")
    page_title = "Add Storage Location"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Storage location saved.")
        return super().form_valid(form)


class StorageLocationUpdateView(
    SiteContextMixin, RegistrationAcceptedMixin, UserPassesTestMixin, UpdateView
):
    model = StorageLocation
    form_class = StorageLocationForm
    template_name = "item_location/storagelocation_form.html"
    success_url = reverse_lazy("item_location:location-list")
    page_title = "Edit Storage Location"

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Storage location updated.")
        return super().form_valid(form)


class StorageLocationDeleteView(
    SiteContextMixin, RegistrationAcceptedMixin, UserPassesTestMixin, DeleteView
):
    model = StorageLocation
    template_name = "item_location/storagelocation_confirm_delete.html"
    success_url = reverse_lazy("item_location:location-list")
    page_title = "Delete Storage Location"

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Storage location deleted.")
        return super().form_valid(form)


# ─────────────────────────────────────────────────────────────────────────────
# Item CRUD


class ItemListView(SiteContextMixin, RegistrationAcceptedMixin, ListView):
    model = Item
    template_name = "item_location/item_list.html"
    page_title = "Items"
    paginate_by = 20

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user).select_related("location")


class ItemDetailView(SiteContextMixin, RegistrationAcceptedMixin, DetailView):
    model = Item
    template_name = "item_location/item_detail.html"
    page_title = "Item Detail"

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)


class ItemCreateView(SiteContextMixin, RegistrationAcceptedMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = "item_location/item_form.html"
    success_url = reverse_lazy("item_location:item-list")
    page_title = "Add Item"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Item saved.")
        return super().form_valid(form)


class ItemUpdateView(
    SiteContextMixin, RegistrationAcceptedMixin, UserPassesTestMixin, UpdateView
):
    model = Item
    form_class = ItemForm
    template_name = "item_location/item_form.html"
    success_url = reverse_lazy("item_location:item-list")
    page_title = "Edit Item"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Item updated.")
        return super().form_valid(form)


class ItemDeleteView(
    SiteContextMixin, RegistrationAcceptedMixin, UserPassesTestMixin, DeleteView
):
    model = Item
    template_name = "item_location/item_confirm_delete.html"
    success_url = reverse_lazy("item_location:item-list")
    page_title = "Delete Item"

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Item deleted.")
        return super().form_valid(form)


# ─────────────────────────────────────────────────────────────────────────────
# Vue.js SPA


class SPAView(SiteContextMixin, RegistrationAcceptedMixin, TemplateView):
    template_name = "item_location/spa.html"
    page_title = "Item Location App"
