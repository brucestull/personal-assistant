from django.contrib import admin

from .models import ReminderSchedule, Thing, Thought
from .tasks import send_reminder_email


class ReminderScheduleInline(admin.TabularInline):
    model = ReminderSchedule
    extra = 0
    fields = ("frequency", "is_active", "next_send", "last_sent")
    readonly_fields = ("last_sent",)
    show_change_link = True


@admin.action(description="Send reminder email now for selected schedules")
def admin_send_reminder_now(modeladmin, request, queryset):
    count = 0
    for schedule in queryset:
        send_reminder_email.delay(schedule.pk)
        count += 1
    modeladmin.message_user(request, f"Queued {count} reminder email(s).")


@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "user", "created", "updated")
    list_filter = ("type", "user")
    search_fields = ("name", "content", "type", "user__username")
    ordering = ("-created",)
    readonly_fields = ("created", "updated")
    autocomplete_fields = ("user",)
    inlines = [ReminderScheduleInline]


@admin.register(Thought)
class ThoughtAdmin(admin.ModelAdmin):
    list_display = ("name", "realm", "user", "created", "updated")
    list_filter = ("realm", "user")
    search_fields = ("name", "content", "realm", "user__username")
    ordering = ("-created",)
    readonly_fields = ("created", "updated")
    autocomplete_fields = ("user",)
    inlines = [ReminderScheduleInline]


@admin.register(ReminderSchedule)
class ReminderScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "frequency",
        "is_active",
        "next_send",
        "last_sent",
        "created",
    )
    list_filter = ("frequency", "is_active", "user")
    search_fields = (
        "user__username",
        "thing__name",
        "thought__name",
    )
    ordering = ("-created",)
    readonly_fields = ("created", "updated", "last_sent")
    autocomplete_fields = ("user",)
    actions = [admin_send_reminder_now]

