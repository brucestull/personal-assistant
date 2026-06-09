# money_wise/admin.py

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from money_wise import models


# ---------------------------------------------------------------------------
# Inlines
# ---------------------------------------------------------------------------


class TransactionInline(admin.TabularInline):
    """Inline for Transactions on the BankAccount admin."""

    model = models.Transaction
    extra = 0
    fields = ("date", "description", "amount", "transaction_type", "category")
    ordering = ("-date",)
    show_change_link = True


class TransactionUploadInline(admin.TabularInline):
    """Inline for TransactionUploads on the BankAccount admin."""

    model = models.TransactionUpload
    extra = 0
    fields = ("csv_file", "status", "rows_processed", "rows_created", "created")
    readonly_fields = ("rows_processed", "rows_created", "created")
    show_change_link = True


class ReceiptInline(admin.TabularInline):
    """Inline for Receipts on the BankAccount admin."""

    model = models.Receipt
    extra = 0
    fields = ("image", "description", "purchased_on", "created")
    readonly_fields = ("created",)
    show_change_link = True


# ---------------------------------------------------------------------------
# Admin classes
# ---------------------------------------------------------------------------


@admin.register(models.BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    """Admin for BankAccount."""

    list_display = (
        "name",
        "institution",
        "account_type",
        "account_number_last4",
        "currency",
        "is_active",
        "transaction_count",
        "created",
    )
    list_filter = ("account_type", "is_active", "institution", "currency")
    search_fields = ("name", "institution", "account_number_last4", "notes")
    ordering = ("institution", "name")
    readonly_fields = ("created", "updated")
    inlines = [TransactionInline, TransactionUploadInline, ReceiptInline]
    fieldsets = (
        (
            _("Account Details"),
            {
                "fields": (
                    "name",
                    "institution",
                    "account_type",
                    "account_number_last4",
                    "routing_number",
                    "currency",
                    "is_active",
                    "notes",
                )
            },
        ),
        (
            _("Dates"),
            {
                "fields": ("created", "updated"),
                "classes": ("collapse",),
            },
        ),
    )

    def transaction_count(self, obj):
        return obj.transactions.count()

    transaction_count.short_description = "Transactions"


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin for Transaction."""

    list_display = (
        "date",
        "description_short",
        "amount",
        "transaction_type",
        "category",
        "bank_account",
        "created",
    )
    list_filter = (
        "transaction_type",
        "category",
        "bank_account",
        "date",
    )
    search_fields = (
        "description",
        "memo",
        "category",
        "reference_number",
        "check_number",
        "bank_account__name",
        "bank_account__institution",
    )
    date_hierarchy = "date"
    ordering = ("-date",)
    readonly_fields = ("created", "updated")
    autocomplete_fields = ("bank_account",)
    list_select_related = ("bank_account",)
    fieldsets = (
        (
            _("Transaction Details"),
            {
                "fields": (
                    "bank_account",
                    "date",
                    "post_date",
                    "description",
                    "amount",
                    "balance_after",
                    "transaction_type",
                    "category",
                )
            },
        ),
        (
            _("Reference"),
            {
                "fields": ("memo", "check_number", "reference_number"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Dates"),
            {
                "fields": ("created", "updated"),
                "classes": ("collapse",),
            },
        ),
    )

    def description_short(self, obj):
        return (obj.description[:60] + "…") if len(obj.description) > 60 else obj.description

    description_short.short_description = "Description"


@admin.register(models.TransactionUpload)
class TransactionUploadAdmin(admin.ModelAdmin):
    """Admin for TransactionUpload."""

    list_display = (
        "bank_account",
        "original_filename",
        "status",
        "rows_processed",
        "rows_created",
        "rows_skipped",
        "uploaded_by",
        "created",
    )
    list_filter = ("status", "bank_account")
    search_fields = (
        "original_filename",
        "bank_account__name",
        "bank_account__institution",
        "error_message",
    )
    ordering = ("-created",)
    readonly_fields = ("created", "updated", "original_filename")
    list_select_related = ("bank_account", "uploaded_by")
    fieldsets = (
        (
            _("Upload Details"),
            {
                "fields": (
                    "bank_account",
                    "csv_file",
                    "original_filename",
                    "status",
                    "notes",
                )
            },
        ),
        (
            _("Processing Results"),
            {
                "fields": (
                    "rows_processed",
                    "rows_created",
                    "rows_skipped",
                    "error_message",
                    "uploaded_by",
                ),
            },
        ),
        (
            _("Dates"),
            {
                "fields": ("created", "updated"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(models.Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    """Admin for Receipt."""

    list_display = ("bank_account", "description", "purchased_on", "created")
    list_filter = ("bank_account", "purchased_on", "created")
    search_fields = (
        "description",
        "bank_account__name",
        "bank_account__institution",
    )
    ordering = ("-created",)
    readonly_fields = ("created", "updated")
    list_select_related = ("bank_account",)
    fieldsets = (
        (
            _("Receipt Details"),
            {
                "fields": (
                    "bank_account",
                    "image",
                    "description",
                    "purchased_on",
                )
            },
        ),
        (
            _("Dates"),
            {
                "fields": ("created", "updated"),
                "classes": ("collapse",),
            },
        ),
    )
