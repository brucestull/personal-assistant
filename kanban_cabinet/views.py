from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, Count, F, IntegerField, Q, Sum, When
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .models import Location, StockItem


# ---------------------------------------------------------------------------
# Mixins
# ---------------------------------------------------------------------------


class OwnerQuerySetMixin(LoginRequiredMixin):
    """
    Restrict queryset to the logged‑in user.
    """

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerFormValidMixin:
    """
    Automatically set owner on created/updated objects.
    """

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# StockItem CRUD
# ---------------------------------------------------------------------------


class StockItemListView(OwnerQuerySetMixin, ListView):
    model = StockItem
    paginate_by = 50


class StockItemDetailView(OwnerQuerySetMixin, DetailView):
    model = StockItem


class StockItemCreateView(LoginRequiredMixin, OwnerFormValidMixin, CreateView):
    model = StockItem
    fields = [
        "name",
        "location",
        "description",
        "is_physical",
        "unit_name",
        "quantity_on_hand",
        "target_quantity",
        "is_active",
    ]

    def get_success_url(self):
        return reverse_lazy("kanban_cabinet:stockitem_detail", args=[self.object.pk])


class StockItemUpdateView(OwnerQuerySetMixin, OwnerFormValidMixin, UpdateView):
    model = StockItem
    fields = [
        "name",
        "location",
        "description",
        "is_physical",
        "unit_name",
        "quantity_on_hand",
        "target_quantity",
        "is_active",
    ]

    def get_success_url(self):
        return reverse_lazy("kanban_cabinet:stockitem_detail", args=[self.object.pk])


class StockItemDeleteView(OwnerQuerySetMixin, DeleteView):
    model = StockItem
    success_url = reverse_lazy("kanban_cabinet:stockitem_list")


# ---------------------------------------------------------------------------
# Location CRUD
# ---------------------------------------------------------------------------


class LocationListView(OwnerQuerySetMixin, ListView):
    model = Location
    paginate_by = 50


class LocationDetailView(OwnerQuerySetMixin, DetailView):
    model = Location


class LocationCreateView(LoginRequiredMixin, OwnerFormValidMixin, CreateView):
    model = Location
    fields = ["name", "description", "is_active"]

    def get_success_url(self):
        return reverse_lazy("kanban_cabinet:location_detail", args=[self.object.pk])


class LocationUpdateView(OwnerQuerySetMixin, OwnerFormValidMixin, UpdateView):
    model = Location
    fields = ["name", "description", "is_active"]

    def get_success_url(self):
        return reverse_lazy("kanban_cabinet:location_detail", args=[self.object.pk])


class LocationDeleteView(OwnerQuerySetMixin, DeleteView):
    model = Location
    success_url = reverse_lazy("kanban_cabinet:location_list")


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "kanban_cabinet/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = StockItem.objects.filter(owner=self.request.user, is_active=True)
        qs = qs.annotate(
            quantity_to_restock_annotated=Case(
                When(
                    target_quantity__gt=F("quantity_on_hand"),
                    then=F("target_quantity") - F("quantity_on_hand"),
                ),
                default=0,
                output_field=IntegerField(),
            )
        )

        ctx["items"] = qs.order_by("-quantity_to_restock_annotated", "name")
        ctx["items_needing_restock"] = qs.filter(
            quantity_to_restock_annotated__gt=0
        )
        ctx["summary"] = qs.aggregate(
            total_items=Count("id"),
            total_needing_restock=Count(
                "id", filter=Q(quantity_to_restock_annotated__gt=0)
            ),
            total_units_to_order=Sum(
                "quantity_to_restock_annotated",
                filter=Q(quantity_to_restock_annotated__gt=0),
            ),
        )
        return ctx
