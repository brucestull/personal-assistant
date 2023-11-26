from django.contrib import admin

from cbt.models import (
    CognitiveDistortion,
    Thought,
)


@admin.register(CognitiveDistortion)
class CognativeDistortionAdmin(admin.ModelAdmin):

    """
    Admin class for the `CognitiveDistortion` model.
    """

    list_display = ["name", "truncated_description"]
    list_filter = ["name"]
    search_fields = ["name", "description"]
    readonly_fields = ["created", "updated"]
    fieldsets = (
        (
            "Cognative Distortion",
            {
                "fields": (
                    "name",
                    "description",
                )
            },
        ),
        (
            "Dates/Metadata",
            {
                "fields": (
                    "created",
                    "updated",
                )
            },
        ),
    )
    ordering = ["name", "description"]

    def truncated_description(self, obj):
        return (
            obj.description[:57] + "..."
            if len(obj.description) > 57
            else obj.description
        )

    truncated_description.short_description = "Description"

    # Additional options:
    """
    save_on_top = True
    save_as = True
    list_per_page = 25
    actions_on_top = True
    actions_on_bottom = True
    empty_value_display = "-empty-"
    date_hierarchy = "created"
    readonly_fields = ["created", "updated"]
    autocomplete_fields = []
    inlines = []
    exclude = []
    raw_id_fields = []
    radio_fields = {}
    prepopulated_fields = {}
    formfield_overrides = {}
    filter_horizontal = []
    filter_vertical = []
    list_select_related = []
    list_display_links = ["name"]
    """


@admin.register(Thought)
class ThoughtAdmin(admin.ModelAdmin):
    """
    Admin class for the `Thought` model.
    """

    list_display = ["user", "name", "truncated_description"]
    list_filter = ["user", "name"]
    search_fields = ["user", "name", "description"]
    readonly_fields = ["created", "updated"]
    fieldsets = (
        (
            "Thought",
            {
                "fields": (
                    "user",
                    "name",
                    "cognitive_distortion",
                    "description",
                )
            },
        ),
        (
            "Dates/Metadata",
            {
                "fields": (
                    "created",
                    "updated",
                )
            },
        ),
    )
    ordering = ["name", "description"]

    def truncated_description(self, obj):
        return (
            obj.description[:57] + "..."
            if len(obj.description) > 57
            else obj.description
        )

    truncated_description.short_description = "Description"

    # Additional options:
    """
    save_on_top = True
    save_as = True
    list_per_page = 25
    actions_on_top = True
    actions_on_bottom = True
    empty_value_display = "-empty-"
    date_hierarchy = "created"
    readonly_fields = ["created", "updated"]
    autocomplete_fields = []
    inlines = []
    exclude = []
    raw_id_fields = []
    radio_fields = {}
    prepopulated_fields = {}
    formfield_overrides = {}
    filter_horizontal = []
    filter_vertical = []
    list_select_related = []
    list_display_links = ["name"]
    """
