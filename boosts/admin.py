from django.contrib import admin

from boosts.models import Inspirational, InspirationalSent, RandomInspirationalEmailSend


@admin.register(Inspirational)
class InspirationalAdmin(admin.ModelAdmin):
    list_display = (
        "body",
        "author",
        "created",
    )

    list_filter = ("author",)


@admin.register(InspirationalSent)
class InspirationalSentAdmin(admin.ModelAdmin):
    list_display = (
        "inspirational_text",
        "sender",
        "beastie",
        "sent_at",
    )

    readonly_fields = (
        "inspirational",
        "inspirational_text",
        "sender",
        "beastie",
        "sent_at",
    )

    list_filter = (
        "sender",
        "beastie",
    )


@admin.register(RandomInspirationalEmailSend)
class RandomInspirationalEmailSendAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "status",
        "created",
        "sent_at",
    )

    readonly_fields = (
        "created",
        "sent_at",
    )

    list_filter = (
        "user",
        "status",
    )
