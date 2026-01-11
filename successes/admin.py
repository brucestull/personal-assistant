"""Admin configuration for the successes app."""

from django.contrib import admin

from .models import Success, WhatWentWell


@admin.register(Success)
class SuccessAdmin(admin.ModelAdmin):
    list_display = (
        "display_text",
        "user",
        "created",
        "updated",
    )
    list_filter = (
        "user",
        "created",
    )
    search_fields = (
        "text",
        "user__username",
    )
    ordering = ("-created",)
    readonly_fields = ("created", "updated")
    
    fieldsets = (
        (None, {
            "fields": ("user", "text")
        }),
        ("Timestamps", {
            "fields": ("created", "updated"),
            "classes": ("collapse",),
        }),
    )

    def display_text(self, obj):
        """Display truncated text in admin list."""
        return obj.text[:75] + ("..." if len(obj.text) > 75 else "")
    
    display_text.short_description = "Success"


@admin.register(WhatWentWell)
class WhatWentWellAdmin(admin.ModelAdmin):
    list_display = (
        "display_what_went_well",
        "user",
        "created",
        "updated",
    )
    list_filter = (
        "user",
        "created",
    )
    search_fields = (
        "what_went_well",
        "how_i_made_it_happen",
        "user__username",
    )
    ordering = ("-created",)
    readonly_fields = ("created", "updated")
    
    fieldsets = (
        (None, {
            "fields": ("user", "what_went_well", "how_i_made_it_happen")
        }),
        ("Timestamps", {
            "fields": ("created", "updated"),
            "classes": ("collapse",),
        }),
    )

    def display_what_went_well(self, obj):
        """Display truncated what went well text in admin list."""
        return obj.what_went_well[:75] + ("..." if len(obj.what_went_well) > 75 else "")
    
    display_what_went_well.short_description = "What Went Well"
