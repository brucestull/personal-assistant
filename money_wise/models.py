# money_wise/models.py

from django.db import models

from base.models import CreatedUpdatedBase


class BankAccount(CreatedUpdatedBase):
    """
    Represents a bank account whose transactions are tracked.
    """

    class AccountType(models.TextChoices):
        CHECKING = "checking", "Checking"
        SAVINGS = "savings", "Savings"
        CREDIT = "credit", "Credit Card"
        INVESTMENT = "investment", "Investment"
        LOAN = "loan", "Loan"
        OTHER = "other", "Other"

    name = models.CharField(
        max_length=200,
        help_text="Friendly name for this account (e.g. 'Chase Checking').",
    )
    institution = models.CharField(
        max_length=200,
        help_text="Bank or financial institution name.",
    )
    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
        default=AccountType.CHECKING,
    )
    account_number_last4 = models.CharField(
        max_length=4,
        blank=True,
        help_text="Last 4 digits of the account number.",
    )
    routing_number = models.CharField(
        max_length=20,
        blank=True,
        help_text="Routing number (optional).",
    )
    currency = models.CharField(
        max_length=3,
        default="USD",
        help_text="ISO 4217 currency code, e.g. USD.",
    )
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["institution", "name"]

    def __str__(self):
        suffix = f" ···{self.account_number_last4}" if self.account_number_last4 else ""
        return f"{self.name}{suffix} ({self.institution})"

    @property
    def balance(self):
        """Return the sum of all transaction amounts for this account."""
        result = self.transactions.aggregate(total=models.Sum("amount"))
        return result["total"] or 0


class Transaction(CreatedUpdatedBase):
    """
    A single financial transaction, matching the standard fields
    found in bank-exported CSV files.
    """

    class TransactionType(models.TextChoices):
        DEBIT = "debit", "Debit"
        CREDIT = "credit", "Credit"
        TRANSFER = "transfer", "Transfer"
        FEE = "fee", "Fee"
        INTEREST = "interest", "Interest"
        OTHER = "other", "Other"

    bank_account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    # Core CSV fields
    date = models.DateField(help_text="Transaction date.")
    post_date = models.DateField(
        null=True,
        blank=True,
        help_text="Settlement / posting date.",
    )
    description = models.CharField(
        max_length=500,
        help_text="Merchant or transaction description.",
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Positive = credit, Negative = debit.",
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
        default=TransactionType.DEBIT,
        blank=True,
    )
    category = models.CharField(
        max_length=200,
        blank=True,
        help_text="Category assigned by bank or user (e.g. 'Groceries').",
    )
    memo = models.TextField(blank=True, help_text="Additional memo or notes.")
    check_number = models.CharField(max_length=20, blank=True)
    reference_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="Bank reference / confirmation number.",
    )
    balance_after = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Running account balance after this transaction.",
    )

    class Meta:
        ordering = ["-date", "-created"]

    def __str__(self):
        return f"{self.date} | {self.description[:60]} | {self.amount}"


def receipt_upload_path(instance, filename):
    """Store receipt images under money_wise/receipts/<account_id>/filename."""
    return f"money_wise/receipts/{instance.bank_account_id}/{filename}"


class Receipt(CreatedUpdatedBase):
    """
    A receipt image linked to a bank account so users can upload and view it later.
    """

    bank_account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        related_name="receipts",
    )
    image = models.ImageField(
        upload_to=receipt_upload_path,
        help_text="Upload an image of your receipt.",
    )
    description = models.CharField(max_length=255, blank=True)
    purchased_on = models.DateField(
        null=True,
        blank=True,
        help_text="Date shown on the receipt.",
    )

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.description or f"Receipt #{self.pk}"


def csv_upload_path(instance, filename):
    """Store CSV uploads under money_wise/csv_uploads/<account_id>/filename."""
    return f"money_wise/csv_uploads/{instance.bank_account_id}/{filename}"


class TransactionUpload(CreatedUpdatedBase):
    """
    Represents a CSV file upload for a given bank account.
    The file is stored in the configured storage backend (S3 in production).
    """

    class UploadStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSED = "processed", "Processed"
        FAILED = "failed", "Failed"

    bank_account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        related_name="uploads",
    )
    csv_file = models.FileField(
        upload_to=csv_upload_path,
        help_text="CSV file exported from your bank.",
    )
    original_filename = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=20,
        choices=UploadStatus.choices,
        default=UploadStatus.PENDING,
    )
    rows_processed = models.PositiveIntegerField(default=0)
    rows_created = models.PositiveIntegerField(default=0)
    rows_skipped = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(
        "accounts.CustomUser",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="transaction_uploads",
    )

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.bank_account} — {self.original_filename or self.csv_file.name} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if self.csv_file and not self.original_filename:
            import os

            self.original_filename = os.path.basename(self.csv_file.name)
        super().save(*args, **kwargs)
