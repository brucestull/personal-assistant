from django.contrib import admin

from .models import Strength
from .models import Gratitude
from .models import LovedOne


@admin.register(Strength)
class StrengthAdmin(admin.ModelAdmin):
    list_display = ("description", "owner")
    list_filter = ("owner",)
    search_fields = ("description",)
    ordering = ("owner", "description")


@admin.register(Gratitude)
class GratitudeAdmin(admin.ModelAdmin):
    list_display = ("description", "owner")
    list_filter = ("owner",)
    search_fields = ("description",)
    ordering = ("owner", "description")


@admin.register(LovedOne)
class LovedOneAdmin(admin.ModelAdmin):
    list_display = ("name", "owner")
    list_filter = ("owner",)
    search_fields = ("name",)
    ordering = ("owner", "name")
