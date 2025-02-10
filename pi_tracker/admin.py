from django.contrib import admin

from .models import PiDevice


@admin.register(PiDevice)
class PiDeviceAdmin(admin.ModelAdmin):
    list_display = ("name", "host_name", "operating_system", "form_factor", "ram")
    search_fields = ("name", "host_name", "mac_address", "operating_system")
    list_filter = ("form_factor", "operating_system")
    ordering = ("name",)
