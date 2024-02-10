from django.contrib import admin

from .models import UnimportantNote


@admin.register(UnimportantNote)
class NoteAdmin(admin.ModelAdmin):
    """
    Admin for Note.
    """

    list_display = ("title", "author", "display_content", "main_image", "updated")
    search_fields = ("title", "content")
    readonly_fields = ("created", "updated")
    fieldsets = (
        (
            "Unimportant Note",
            {
                "fields": (
                    "author",
                    "title",
                    "content",
                    "url",
                    "main_image",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "created",
                    "updated",
                )
            },
        ),
    )
    # Some GitHub Copilot suggestions for other attributes to set:
    ####################################################################
    # list_filter = ("created", "updated")
    # date_hierarchy = "created"
    # save_on_top = True
    # save_as = True
    # list_per_page = 25
    # list_max_show_all = 200
    # actions_on_top = True
    # actions_on_bottom = True
    # actions_selection_counter = True
    # show_full_result_count = True
    # ordering = ("-created",)
    # list_select_related = True
    # raw_id_fields = ()
    # inlines = ()
    # exclude = ()
    # formfield_overrides = {}
    # radio_fields = {}
    # prepopulated_fields = {}
    # autocomplete_fields = {}
    # readonly_fields = ()
    # filter_horizontal = ()
    # filter_vertical = ()
    # verbose_name = "Note"
    # verbose_name_plural = "Notes"
    # db_table = "unimportant_notes_note"
    # managed = True
    ####################################################################
