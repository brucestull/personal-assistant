from django.contrib import admin

from .models import Goal, GoalRelationship


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    """
    Admin for Goal.
    """

    list_display = (
        "name",
        "description",
        "due_date",
        "completed",
    )
    list_editable = ("completed",)
    search_fields = ("name",)
    fieldsets = (
        (
            "Goal",
            {"fields": ("name", "description", "due_date", "completed")},
        ),
    )


@admin.register(GoalRelationship)
class GoalRelationshipAdmin(admin.ModelAdmin):
    """
    Admin for GoalRelationship.
    """

    list_display = (
        "child_goal",
        "parent_goal",
        "relationship_type",
    )
    search_fields = ("parent_goal__name", "child_goal__name")
    fieldsets = (
        (
            "Goal Relationship",
            {"fields": ("parent_goal", "child_goal", "relationship_type")},
        ),
    )
    raw_id_fields = ("parent_goal", "child_goal")
    autocomplete_fields = ("parent_goal", "child_goal")
    # Some GitHub Copilot suggestions for other attributes to set:
    ####################################################################
    # list_filter = ()
    # date_hierarchy = None
    # save_on_top = False
    # save_as = False
    # list_per_page = 100
    # list_max_show_all = 200
    # actions_on_top = False
    # actions_on_bottom = False
    # actions_selection_counter = False
    # show_full_result_count = False
    # ordering = ()
    # list_select_related = False
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
    # verbose_name = "Goal"
    # verbose_name_plural = "Goals"
    # db_table = "goals_goal"
    # managed = True
    ####################################################################
