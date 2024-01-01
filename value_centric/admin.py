from django.contrib import admin

from value_centric.models import PersonalValue


@admin.register(PersonalValue)
class PersonalValueAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    list_filter = ("user",)
    search_fields = ("name", "description")
