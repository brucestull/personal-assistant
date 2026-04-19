# true_north/admin.py

from django.contrib import admin
from django.utils import timezone

from .models import CoreValue, CoreValueEmailSchedule, Goal, Milestone, ValueAction


class GoalInline(admin.TabularInline):
    model = Goal
    extra = 0
    fields = ("order", "title", "slug", "status", "is_active", "target_date")
    show_change_link = True
    ordering = ("order", "title")


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "is_active", "order", "created", "updated")
    list_filter = ("is_active", "user")
    search_fields = ("name", "definition", "slug", "user__username")
    ordering = ("order", "name")
    readonly_fields = ("created", "updated")

    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("user",)
    inlines = [GoalInline]
    actions = (
        "activate_selected",
        "deactivate_selected",
        "normalize_order_for_selected_users",
    )

    @admin.action(description="Activate selected core values")
    def activate_selected(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Deactivate selected core values")
    def deactivate_selected(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Normalize order for selected users")
    def normalize_order_for_selected_users(self, request, queryset):
        for user_id in queryset.values_list("user_id", flat=True).distinct():
            CoreValue.reorder_all(user_id=user_id)


class MilestoneInline(admin.TabularInline):
    model = Milestone
    extra = 0
    fields = ("order", "description", "slug", "due_date", "is_completed")
    show_change_link = True
    ordering = ("order", "description")


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
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
    actions = (
        "activate_selected",
        "deactivate_selected",
        "normalize_order_for_selected_scopes",
    )

    @admin.action(description="Activate selected goals")
    def activate_selected(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Deactivate selected goals")
    def deactivate_selected(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Normalize order for selected goal scopes")
    def normalize_order_for_selected_scopes(self, request, queryset):
        for user_id, value_id in queryset.values_list("user_id", "value_id").distinct():
            Goal.reorder_all(user_id=user_id, value_id=value_id)


class ValueActionInline(admin.TabularInline):
    model = ValueAction
    extra = 0
    fields = ("order", "status", "is_completed", "due_date", "content")
    ordering = ("order", "id")


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = (
        "id",
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
    inlines = [ValueActionInline]
    actions = (
        "mark_completed",
        "mark_pending",
        "normalize_order_for_selected_scopes",
    )

    @admin.action(description="Mark selected milestones as completed")
    def mark_completed(self, request, queryset):
        queryset.update(is_completed=True, completed_at=timezone.now())

    @admin.action(description="Mark selected milestones as pending")
    def mark_pending(self, request, queryset):
        queryset.update(is_completed=False, completed_at=None)

    @admin.action(description="Normalize order for selected goal scopes")
    def normalize_order_for_selected_scopes(self, request, queryset):
        for user_id, goal_id in queryset.values_list("user_id", "goal_id").distinct():
            Milestone.reorder_all(user_id=user_id, goal_id=goal_id)


@admin.register(ValueAction)
class ValueActionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
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
    actions = (
        "mark_done",
        "mark_todo",
        "normalize_order_for_selected_scopes",
    )

    @admin.action(description="Mark selected value actions as done")
    def mark_done(self, request, queryset):
        queryset.update(
            status="done",
            is_completed=True,
            completed_at=timezone.now(),
        )

    @admin.action(description="Mark selected value actions as to do")
    def mark_todo(self, request, queryset):
        queryset.update(
            status="todo",
            is_completed=False,
            completed_at=None,
        )

    @admin.action(description="Normalize order for selected milestone scopes")
    def normalize_order_for_selected_scopes(self, request, queryset):
        for user_id, milestone_id in queryset.values_list(
            "user_id", "milestone_id"
        ).distinct():
            ValueAction.reorder_all(user_id=user_id, milestone_id=milestone_id)


@admin.register(CoreValueEmailSchedule)
class CoreValueEmailScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "core_value",
        "frequency",
        "send_time",
        "days_of_week",
        "is_active",
        "next_send",
        "last_sent",
        "created",
    )
    list_filter = ("frequency", "is_active", "user")
    search_fields = ("core_value__name", "user__username")
    ordering = ("-created",)
    readonly_fields = ("created", "updated", "last_sent", "next_send")
    autocomplete_fields = ("user", "core_value")
