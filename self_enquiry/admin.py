from django.contrib import admin

from self_enquiry.models import Journal


@admin.register(Journal)
class SelfEnquiryAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'title',
        'display_content',
        'created',
    )
