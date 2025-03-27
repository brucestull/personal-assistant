from django.contrib import admin

from .models import Goal, Virtue, VIACharacterStrength


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "parent",
        "display_character_strengths",  # Custom method to display M2M field
        "user",
        "is_ultimate_concern",
        "completed",
    )

    def display_character_strengths(self, obj):
        return ", ".join([str(cs) for cs in obj.character_strengths.all()])

    display_character_strengths.short_description = "Character Strengths"

    search_fields = ("name",)
    list_filter = ("parent",)
    ordering = (
        "user",
        "parent",
        "name",
    )


class VIACharacterStrengthInline(admin.TabularInline):
    model = VIACharacterStrength
    extra = 1
    fields = ("name", "description")
    show_change_link = True


@admin.register(Virtue)
class VirtueAdmin(admin.ModelAdmin):
    list_display = ("name", "short_description")
    search_fields = ("name", "description")
    ordering = ("name",)
    inlines = [VIACharacterStrengthInline]

    def short_description(self, obj):
        if len(obj.description) > 45:
            return f"{obj.description[:45]}..."
        return obj.description

    short_description.short_description = "Description"

    class Meta:
        verbose_name = "Virtue"
        verbose_name_plural = "Virtues"


@admin.register(VIACharacterStrength)
class VIACharacterStrengthAdmin(admin.ModelAdmin):
    list_display = ("name", "virtue", "short_description")
    search_fields = ("name", "description")
    ordering = (
        "virtue",
        "name",
    )

    def short_description(self, obj):
        if len(obj.description) > 45:
            return f"{obj.description[:45]}..."
        return obj.description

    short_description.short_description = "Description"

    class Meta:
        verbose_name = "VIA Character Strength"
        verbose_name_plural = "VIA Character Strengths"
