# money_wise/urls.py

from django.urls import path

from money_wise import views

app_name = "money_wise"

urlpatterns = [
    # Dashboard
    path("", views.dashboard, name="dashboard"),
    # BankAccount CRUD
    path(
        "accounts/",
        views.BankAccountListView.as_view(),
        name="bankaccount_list",
    ),
    path(
        "accounts/<int:pk>/",
        views.BankAccountDetailView.as_view(),
        name="bankaccount_detail",
    ),
    path(
        "accounts/add/",
        views.BankAccountCreateView.as_view(),
        name="bankaccount_create",
    ),
    path(
        "accounts/<int:pk>/edit/",
        views.BankAccountUpdateView.as_view(),
        name="bankaccount_update",
    ),
    path(
        "accounts/<int:pk>/delete/",
        views.BankAccountDeleteView.as_view(),
        name="bankaccount_delete",
    ),
    # Transaction CRUD
    path(
        "transactions/",
        views.TransactionListView.as_view(),
        name="transaction_list",
    ),
    path(
        "transactions/<int:pk>/",
        views.TransactionDetailView.as_view(),
        name="transaction_detail",
    ),
    path(
        "transactions/add/",
        views.TransactionCreateView.as_view(),
        name="transaction_create",
    ),
    path(
        "transactions/<int:pk>/edit/",
        views.TransactionUpdateView.as_view(),
        name="transaction_update",
    ),
    path(
        "transactions/<int:pk>/delete/",
        views.TransactionDeleteView.as_view(),
        name="transaction_delete",
    ),
    # TransactionUpload CRUD
    path(
        "uploads/",
        views.TransactionUploadListView.as_view(),
        name="upload_list",
    ),
    path(
        "uploads/<int:pk>/",
        views.TransactionUploadDetailView.as_view(),
        name="upload_detail",
    ),
    path(
        "uploads/add/",
        views.TransactionUploadCreateView.as_view(),
        name="upload_create",
    ),
    path(
        "uploads/<int:pk>/delete/",
        views.TransactionUploadDeleteView.as_view(),
        name="upload_delete",
    ),
]
