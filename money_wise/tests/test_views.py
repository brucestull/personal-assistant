# money_wise/tests/test_views.py

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from money_wise.models import BankAccount, Transaction

TEST_PW = "testpass123"


class MoneyWiseViewAccessTest(TestCase):
    """Tests for view access control."""

    def setUp(self):
        self.accepted_user = CustomUser.objects.create_user(
            username="accepted",
            password="testpass123",
            registration_accepted=True,
        )
        self.unaccepted_user = CustomUser.objects.create_user(
            username="unaccepted",
            password="testpass123",
            registration_accepted=False,
        )
        self.account = BankAccount.objects.create(
            name="Test Checking",
            institution="Test Bank",
        )
        self.transaction = Transaction.objects.create(
            bank_account=self.account,
            date="2024-01-01",
            description="Test txn",
            amount=Decimal("100.00"),
        )

    def test_dashboard_requires_auth(self):
        response = self.client.get(reverse("money_wise:dashboard"))
        self.assertIn(response.status_code, [302, 403])

    def test_dashboard_requires_registration_accepted(self):
        self.client.login(username="unaccepted", password="testpass123")
        response = self.client.get(reverse("money_wise:dashboard"))
        self.assertEqual(response.status_code, 403)

    def test_dashboard_accessible_for_accepted_user(self):
        self.client.login(username="accepted", password="testpass123")
        response = self.client.get(reverse("money_wise:dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_bankaccount_list_accessible(self):
        self.client.login(username="accepted", password="testpass123")
        response = self.client.get(reverse("money_wise:bankaccount_list"))
        self.assertEqual(response.status_code, 200)

    def test_bankaccount_detail_accessible(self):
        self.client.login(username="accepted", password="testpass123")
        response = self.client.get(
            reverse("money_wise:bankaccount_detail", args=[self.account.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_transaction_list_accessible(self):
        self.client.login(username="accepted", password="testpass123")
        response = self.client.get(reverse("money_wise:transaction_list"))
        self.assertEqual(response.status_code, 200)

    def test_transaction_detail_accessible(self):
        self.client.login(username="accepted", password="testpass123")
        response = self.client.get(
            reverse("money_wise:transaction_detail", args=[self.transaction.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_upload_list_accessible(self):
        self.client.login(username="accepted", password="testpass123")
        response = self.client.get(reverse("money_wise:upload_list"))
        self.assertEqual(response.status_code, 200)

    def test_transaction_list_filters_by_account(self):
        self.client.login(username="accepted", password="testpass123")
        response = self.client.get(
            reverse("money_wise:transaction_list") + f"?account={self.account.pk}"
        )
        self.assertEqual(response.status_code, 200)


class BankAccountCRUDTest(TestCase):
    """Tests for BankAccount create/update/delete views."""

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="user",
            password="testpass123",
            registration_accepted=True,
        )
        self.client.login(username="user", password="testpass123")

    def test_create_bank_account(self):
        response = self.client.post(
            reverse("money_wise:bankaccount_create"),
            {
                "name": "New Savings",
                "institution": "First Bank",
                "account_type": "savings",
                "currency": "USD",
                "is_active": True,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(BankAccount.objects.filter(name="New Savings").exists())

    def test_delete_bank_account(self):
        account = BankAccount.objects.create(
            name="To Delete",
            institution="Some Bank",
        )
        response = self.client.post(
            reverse("money_wise:bankaccount_delete", args=[account.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(BankAccount.objects.filter(pk=account.pk).exists())
