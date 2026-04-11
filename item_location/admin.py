from django.contrib import admin

from .models import Item, StorageLocation


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0
    fields = ("name", "type", "user")
    show_change_link = True
    autocomplete_fields = ("user",)


@admin.register(StorageLocation)
class StorageLocationAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "user", "item_count", "created", "updated")
    list_filter = ("type", "user")
    search_fields = ("name", "type", "user__username")
    ordering = ("name",)
    readonly_fields = ("created", "updated")
    autocomplete_fields = ("user",)
    inlines = [ItemInline]

    @admin.display(description="# Items")
    def item_count(self, obj):
        return obj.items.count()


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "location", "user", "created", "updated")
    list_filter = ("type", "user", "location")
    search_fields = ("name", "type", "user__username", "location__name")
    ordering = ("name",)
    readonly_fields = ("created", "updated")
    autocomplete_fields = ("user", "location")
