# money_wise/tests/test_models.py

from decimal import Decimal

from django.test import TestCase

from money_wise.models import BankAccount, Transaction, TransactionUpload


class BankAccountModelTest(TestCase):
    """Tests for the BankAccount model."""

    @classmethod
    def setUpTestData(cls):
        cls.account = BankAccount.objects.create(
            name="Chase Checking",
            institution="Chase Bank",
            account_type=BankAccount.AccountType.CHECKING,
            account_number_last4="1234",
            currency="USD",
        )

    def test_str_includes_name_and_institution(self):
        self.assertIn("Chase Checking", str(self.account))
        self.assertIn("Chase Bank", str(self.account))

    def test_str_includes_last4_when_set(self):
        self.assertIn("1234", str(self.account))

    def test_balance_is_zero_with_no_transactions(self):
        self.assertEqual(self.account.balance, 0)

    def test_balance_sums_transactions(self):
        Transaction.objects.create(
            bank_account=self.account,
            date="2024-01-01",
            description="Paycheck",
            amount=Decimal("1000.00"),
            transaction_type=Transaction.TransactionType.CREDIT,
        )
        Transaction.objects.create(
            bank_account=self.account,
            date="2024-01-02",
            description="Grocery",
            amount=Decimal("-50.00"),
            transaction_type=Transaction.TransactionType.DEBIT,
        )
        self.assertEqual(self.account.balance, Decimal("950.00"))

    def test_default_currency_is_usd(self):
        account = BankAccount.objects.create(
            name="Test",
            institution="Test Bank",
        )
        self.assertEqual(account.currency, "USD")

    def test_default_account_type_is_checking(self):
        account = BankAccount.objects.create(
            name="Test",
            institution="Test Bank",
        )
        self.assertEqual(account.account_type, BankAccount.AccountType.CHECKING)

    def test_is_active_default_true(self):
        self.assertTrue(self.account.is_active)

    def test_meta_ordering(self):
        ordering = BankAccount._meta.ordering
        self.assertEqual(ordering, ["institution", "name"])


class TransactionModelTest(TestCase):
    """Tests for the Transaction model."""

    @classmethod
    def setUpTestData(cls):
        cls.account = BankAccount.objects.create(
            name="Savings",
            institution="Test Bank",
        )
        cls.transaction = Transaction.objects.create(
            bank_account=cls.account,
            date="2024-03-15",
            description="Amazon Purchase",
            amount=Decimal("-29.99"),
            category="Shopping",
            transaction_type=Transaction.TransactionType.DEBIT,
        )

    def test_str_contains_date_description_amount(self):
        result = str(self.transaction)
        self.assertIn("Amazon Purchase", result)
        self.assertIn("-29.99", result)

    def test_meta_ordering(self):
        ordering = Transaction._meta.ordering
        self.assertIn("-date", ordering)

    def test_transaction_type_choices(self):
        choices = [c[0] for c in Transaction.TransactionType.choices]
        self.assertIn("debit", choices)
        self.assertIn("credit", choices)
        self.assertIn("transfer", choices)

    def test_optional_fields_blank_by_default(self):
        txn = Transaction.objects.create(
            bank_account=self.account,
            date="2024-04-01",
            description="Test",
            amount=Decimal("10.00"),
        )
        self.assertEqual(txn.category, "")
        self.assertEqual(txn.memo, "")
        self.assertEqual(txn.check_number, "")
        self.assertIsNone(txn.balance_after)

    def test_foreign_key_bank_account(self):
        self.assertEqual(self.transaction.bank_account, self.account)
        self.assertIn(self.transaction, self.account.transactions.all())
