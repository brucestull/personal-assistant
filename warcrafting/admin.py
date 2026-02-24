# warcrafting/admin.py

from django.contrib import admin

from .models import Asset, Character, CharacterProfession, Profession, ProfessionTier


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ("name", "tier_count", "tier_names_short")
    search_fields = ("name",)

    def tier_count(self, obj):
        return obj.tiers.count()

    tier_count.short_description = "Expansion tiers"

    def tier_names_short(self, obj):
        names = list(obj.tiers.values_list("expansion_label", flat=True))
        if not names:
            return "—"
        if len(names) > 3:
            return ", ".join(names[:3]) + f" (+{len(names) - 3} more)"
        return ", ".join(names)

    tier_names_short.short_description = "Expansions"


@admin.register(ProfessionTier)
class ProfessionTierAdmin(admin.ModelAdmin):
    list_display = ("profession", "expansion_label", "max_skill")
    list_filter = ("expansion_label", "profession")
    search_fields = ("profession__name", "expansion_label")
    autocomplete_fields = ("profession",)
    ordering = ("profession__name", "expansion_label")


class CharacterProfessionInline(admin.TabularInline):
    """Inline to manage a character's profession skill levels."""

    model = CharacterProfession
    extra = 1
    fields = ("profession_tier", "current_skill")
    autocomplete_fields = ("profession_tier",)


@admin.register(CharacterProfession)
class CharacterProfessionAdmin(admin.ModelAdmin):
    list_display = ("character", "profession_tier", "current_skill", "skill_percentage")
    list_filter = ("profession_tier__expansion_label", "profession_tier__profession")
    search_fields = (
        "character__name",
        "character__owner__username",
        "profession_tier__profession__name",
    )
    autocomplete_fields = ("character", "profession_tier")
    ordering = ("character__owner__username", "character__name")

    def skill_percentage(self, obj):
        pct = obj.skill_percentage
        return f"{pct}%" if pct is not None else "—"

    skill_percentage.short_description = "Progress"


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "wow_class",
        "race",
        "level",
        "profession_summary",
        "formatted_gold",
    )
    list_filter = (
        "wow_class",
        "race",
        "owner",
    )
    search_fields = (
        "name",
        "owner__username",
        "owner__email",
    )
    autocomplete_fields = ("owner",)
    ordering = ("owner__username", "name")
    inlines = [CharacterProfessionInline]

    def formatted_gold(self, obj: Character) -> str:
        total = obj.total_gold()
        # Simple formatting: "1,234 g"
        return f"{total:,} g"

    formatted_gold.short_description = "Gold"

    # Delegate to model method, but keep a separate admin method so we can
    # customize description if needed.
    def profession_summary(self, obj: Character) -> str:  # type: ignore[override]
        return obj.profession_summary()

    profession_summary.short_description = (
        Character.profession_summary.short_description
    )


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "character",
        "get_owner",
        "category",
        "quantity",
        "is_unique",
    )
    list_filter = ("category", "is_unique", "character__owner")
    search_fields = (
        "name",
        "character__name",
        "character__owner__username",
        "character__owner__email",
    )
    autocomplete_fields = ("character",)
    ordering = (
        "character__owner__username",
        "character__name",
        "category",
        "name",
    )

    def get_owner(self, obj: Asset):
        return obj.character.owner

    get_owner.short_description = "Owner"
    get_owner.admin_order_field = "character__owner__username"
