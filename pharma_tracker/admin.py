from django.contrib import admin

from pharma_tracker.models import (
    Pharmaceutical,
)


@admin.register(Pharmaceutical)
class PharmaceuticalAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "is_active",
        "prescription_required",
    )
    list_filter = (
        "user",
        "name",
        "is_active",
        "prescription_required",
    )
    search_fields = (
        "user",
        "name",
    )
