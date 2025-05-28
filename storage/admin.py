# storage/admin.py

from django.contrib import admin

from .models import SortDecision, StorageArea, Type


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created", "updated")


@admin.register(StorageArea)
class StorageAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "description", "created", "updated")
    list_display_links = ("name",)


@admin.register(SortDecision)
class SortDecisionAdmin(admin.ModelAdmin):
    list_display = ("text",)
