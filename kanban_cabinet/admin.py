from django.contrib import admin

from .models import Location, StockItem


class StockItemInline(admin.TabularInline):
    model = StockItem
    extra = 0
    fields = (
        "name",
        "is_physical",
        "unit_name",
        "quantity_on_hand",
        "target_quantity",
        "quantity_to_restock_display",
        "is_active",
    )
    readonly_fields = ("quantity_to_restock_display",)

    def quantity_to_restock_display(self, obj):
        return obj.quantity_to_restock

    quantity_to_restock_display.short_description = "To restock"


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "owner__username")
    inlines = [StockItemInline]


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "owner",
        "location",
        "quantity_on_hand",
        "target_quantity",
        "quantity_to_restock_display",
        "is_physical",
        "unit_name",
        "is_active",
    )
    list_filter = ("is_physical", "is_active", "location")
    search_fields = ("name", "slug", "location__name", "owner__username")
    autocomplete_fields = ("owner", "location")
    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
        "quantity_to_restock_display",
    )

    def quantity_to_restock_display(self, obj):
        return obj.quantity_to_restock

    quantity_to_restock_display.short_description = "To restock"
