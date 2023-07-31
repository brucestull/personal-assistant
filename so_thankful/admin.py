from django.contrib import admin

from .models import Strength
from .models import Gratitude
from .models import LovedOne


@admin.register(Strength)
class StrengthAdmin(admin.ModelAdmin):
    list_display = ("description", "user")
    list_filter = ("user",)
    search_fields = ("description",)
    ordering = ("user", "description")


@admin.register(Gratitude)
class GratitudeAdmin(admin.ModelAdmin):
    list_display = ("description", "user")
    list_filter = ("user",)
    search_fields = ("description",)
    ordering = ("user", "description")


@admin.register(LovedOne)
class LovedOneAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    list_filter = ("user",)
    search_fields = ("name",)
    ordering = ("user", "name")
