# money_wise/views.py

from decimal import Decimal

from django.db.models import Count, Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from base.decorators import registration_accepted_required
from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME

from money_wise.models import BankAccount, Transaction, TransactionUpload


@registration_accepted_required
def dashboard(request):
    """
    Dashboard view for the Money Wise app.
    """
    accounts = BankAccount.objects.filter(is_active=True)
    total_accounts = accounts.count()
    total_transactions = Transaction.objects.count()
    total_uploads = TransactionUpload.objects.count()

    # Recent transactions
    recent_transactions = Transaction.objects.select_related("bank_account").order_by(
        "-date"
    )[:10]

    # Spending by category (debit transactions)
    category_totals = (
        Transaction.objects.filter(amount__lt=0)
        .exclude(category="")
        .values("category")
        .annotate(total=Sum("amount"), count=Count("id"))
        .order_by("total")[:10]
    )

    # Per-account balances — single query using annotation to avoid N+1
    accounts_annotated = accounts.annotate(
        annotated_balance=Sum("transactions__amount"),
        transaction_count=Count("transactions"),
    )
    account_balances = [
        {
            "account": acct,
            "balance": acct.annotated_balance or Decimal("0"),
            "transaction_count": acct.transaction_count,
        }
        for acct in accounts_annotated
    ]

    context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Money Wise Dashboard",
        "total_accounts": total_accounts,
        "total_transactions": total_transactions,
        "total_uploads": total_uploads,
        "recent_transactions": recent_transactions,
        "category_totals": category_totals,
        "account_balances": account_balances,
    }
    return render(request, "money_wise/dashboard.html", context)


# ---------------------------------------------------------------------------
# BankAccount CRUD
# ---------------------------------------------------------------------------


class BankAccountListView(RegistrationAcceptedMixin, ListView):
    model = BankAccount
    context_object_name = "bank_accounts"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["the_site_name"] = THE_SITE_NAME
        ctx["page_title"] = "Bank Accounts"
        return ctx


class BankAccountDetailView(RegistrationAcceptedMixin, DetailView):
    model = BankAccount

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["the_site_name"] = THE_SITE_NAME
        ctx["page_title"] = str(self.object)
        ctx["recent_transactions"] = self.object.transactions.order_by("-date")[:20]
        ctx["uploads"] = self.object.uploads.order_by("-created")[:5]
        return ctx


class BankAccountCreateView(RegistrationAcceptedMixin, CreateView):
    model = BankAccount
    fields = [
        "name",
        "institution",
        "account_type",
        "account_number_last4",
        "routing_number",
        "currency",
        "is_active",
        "notes",
    ]
    success_url = reverse_lazy("money_wise:bankaccount_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["the_site_name"] = THE_SITE_NAME
        ctx["page_title"] = "Add Bank Account"
        return ctx


class BankAccountUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = BankAccount
    fields = [
        "name",
        "institution",
        "account_type",
        "account_number_last4",
        "routing_number",
        "currency",
        "is_active",
        "notes",
    ]
    success_url = reverse_lazy("money_wise:bankaccount_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["the_site_name"] = THE_SITE_NAME
        ctx["page_title"] = f"Edit {self.object}"
        return ctx


class BankAccountDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = BankAccount
    success_url = reverse_lazy("money_wise:bankaccount_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["the_site_name"] = THE_SITE_NAME
        ctx["page_title"] = f"Delete {self.object}"
        return ctx


# ---------------------------------------------------------------------------
# Transaction CRUD
# ---------------------------------------------------------------------------


class TransactionListView(RegistrationAcceptedMixin, ListView):
    model = Transaction
    context_object_name = "transactions"
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset().select_related("bank_account")
        account_id = self.request.GET.get("account")
        if account_id:
            qs = qs.filter(bank_account_id=account_id)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["the_site_name"] = THE_SITE_NAME
        ctx["page_title"] = "Transactions"
        ctx["bank_accounts"] = BankAccount.objects.only("id", "name", "institution")
        ctx["selected_account"] = self.request.GET.get("account", "")
        return ctx


class TransactionDetailView(RegistrationAcceptedMixin, DetailView):
    model = Transaction

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["the_site_name"] = THE_SITE_NAME
        ctx["page_title"] = str(self.object)
        return ctx


class TransactionCreateView(RegistrationAcceptedMixin, CreateView):
    model = Transaction
    fields = [
        "bank_account",
        "date",
        "post_date",
        "description",
        "amount",
        "transaction_type",
        "category",
        "memo",
        "check_number",
        "reference_number",
        "balance_after",
    ]
    success_url = reverse_lazy("money_wise:transaction_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["the_site_name"] = THE_SITE_NAME
        ctx["page_title"] = "Add Transaction"
        return ctx


class TransactionUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = Transaction
    fields = [
        "bank_account",
        "date",
        "post_date",
        "description",
        "amount",
        "transaction_type",
        "category",
        "memo",
        "check_number",
        "reference_number",
        "balance_after",
    ]
    success_url = reverse_lazy("money_wise:transaction_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["the_site_name"] = THE_SITE_NAME
        ctx["page_title"] = f"Edit Transaction"
        return ctx


class TransactionDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy("money_wise:transaction_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["the_site_name"] = THE_SITE_NAME
        ctx["page_title"] = "Delete Transaction"
        return ctx


# ---------------------------------------------------------------------------
# TransactionUpload CRUD
# ---------------------------------------------------------------------------


class TransactionUploadListView(RegistrationAcceptedMixin, ListView):
    model = TransactionUpload
    context_object_name = "uploads"

    def get_queryset(self):
        return super().get_queryset().select_related("bank_account", "uploaded_by")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["the_site_name"] = THE_SITE_NAME
        ctx["page_title"] = "CSV Uploads"
        return ctx


class TransactionUploadDetailView(RegistrationAcceptedMixin, DetailView):
    model = TransactionUpload

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["the_site_name"] = THE_SITE_NAME
        ctx["page_title"] = str(self.object)
        return ctx


class TransactionUploadCreateView(RegistrationAcceptedMixin, CreateView):
    model = TransactionUpload
    fields = ["bank_account", "csv_file", "notes"]
    success_url = reverse_lazy("money_wise:upload_list")

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["the_site_name"] = THE_SITE_NAME
        ctx["page_title"] = "Upload CSV Transactions"
        return ctx


class TransactionUploadDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = TransactionUpload
    success_url = reverse_lazy("money_wise:upload_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["the_site_name"] = THE_SITE_NAME
        ctx["page_title"] = "Delete Upload"
        return ctx
