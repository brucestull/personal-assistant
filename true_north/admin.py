# true_north/admin.py

from django.contrib import admin

from .models import CoreValue, Goal, Milestone, Task


class GoalInline(admin.TabularInline):
    model = Goal
    extra = 0
    fields = ("order", "title", "slug", "status", "is_active", "target_date")
    show_change_link = True
    ordering = ("order", "title")


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "is_active", "order", "created", "updated")
    list_filter = ("is_active", "user")
    search_fields = ("name", "definition", "slug", "user__username")
    ordering = ("order", "name")
    readonly_fields = ("created", "updated")

    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("user",)
    inlines = [GoalInline]


class MilestoneInline(admin.TabularInline):
    model = Milestone
    extra = 0
    fields = ("order", "description", "slug", "due_date", "is_completed")
    show_change_link = True
    ordering = ("order", "description")


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "value",
        "status",
        "is_active",
        "order",
        "target_date",
        "created",
    )  # noqa E501
    list_filter = ("status", "is_active", "user", "value")
    search_fields = ("title", "description", "slug", "value__name", "user__username")
    ordering = ("order", "title")
    readonly_fields = ("created", "updated")

    autocomplete_fields = ("user", "value")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [MilestoneInline]


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ("order", "status", "is_completed", "due_date", "content")
    ordering = ("order", "id")


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = (
        "description",
        "user",
        "goal",
        "due_date",
        "is_completed",
        "order",
        "created",
    )  # noqa E501
    list_filter = ("is_completed", "user", "goal")
    search_fields = ("description", "slug", "notes", "goal__title", "user__username")
    ordering = ("order", "description")
    readonly_fields = ("created", "updated")

    autocomplete_fields = ("user", "goal")
    prepopulated_fields = {"slug": ("description",)}
    inlines = [TaskInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "milestone",
        "status",
        "is_completed",
        "due_date",
        "order",
        "created",
    )  # noqa E501
    list_filter = ("status", "is_completed", "user")
    search_fields = (
        "content",
        "milestone__description",
        "milestone__goal__title",
        "user__username",
    )
    ordering = ("order", "id")
    readonly_fields = ("created", "updated")

    autocomplete_fields = ("user", "milestone")
