from django.contrib import admin

from self_enquiry.models import Journal, GrowthOpportunity


@admin.register(Journal)
class SelfEnquiryAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel for
    the `Journal` model.
    """

    # The `list_display` attribute controls which fields are displayed on the
    # list page for the model.
    list_display = (
        "author",
        "title",
        "display_content",
        "created",
    )
    # The `ordering` attribute controls the order in which the objects are
    # displayed on the list page for the model.
    ordering = ("-created",)
    # The `list_filter` attribute controls which fields are displayed in the
    # filter sidebar on the list page for the model.
    list_filter = (
        "author",
        "created",
    )
    # The `search_fields` attribute controls which fields are searched when
    # the user uses the search bar on the list page for the model.
    search_fields = (
        "author__username",
        "title",
        "content",
    )
    # The `readonly_fields` attribute controls which fields are displayed as
    # read-only on the update page for the model.
    readonly_fields = (
        "updated",
        "created",
    )
    # The `fieldsets` attribute controls how the fields are grouped on the
    # update page for the model.
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "author",
                    "title",
                    "content",
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


@admin.register(GrowthOpportunity)
class GrowthOpportunityAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel for
    the `GrowthOpportunity` model.
    """

    # The `list_display` attribute controls which fields are displayed on the
    # list page for the model.
    list_display = (
        "__str__",
        "author",
        "created",
    )
    # The `ordering` attribute controls the order in which the objects are
    # displayed on the list page for the model.
    ordering = ("-created",)
    # The `ordering` attribute controls the order in which the objects are
    # displayed on the list page for the model.
    list_filter = (
        "author",
        "created",
    )
    # The `search_fields` attribute controls which fields are searched when
    # the user uses the search bar on the list page for the model.
    search_fields = (
        "question",
        "author__username",
    )
    # The `readonly_fields` attribute controls which fields are displayed as
    # read-only on the update page for the model.
    readonly_fields = (
        "created",
        "updated",
    )
    # The `fieldsets` attribute controls how the fields are grouped on the
    # update page for the model.
    fieldsets = (
        (
            "Content",
            {
                "fields": (
                    "question",
                    "author",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "created",
                    "updated",
                )
            },
        ),
    )
