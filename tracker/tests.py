from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Transaction

class TransactionModelTest(TestCase):
    def test_transaction_creation(self):
        transaction = Transaction.objects.create(
            description="Groceries",
            amount=Decimal("75.50"),
            transaction_type="expense",
            date=date.today()
        )
        self.assertEqual(transaction.description, "Groceries")
        self.assertEqual(transaction.amount, Decimal("75.50"))
        self.assertEqual(transaction.transaction_type, "expense")

    def test_transaction_string_representation(self):
        transaction = Transaction.objects.create(
            description="Paycheck",
            amount=Decimal("2000.00"),
            transaction_type="income",
            date=date.today()
        )
        self.assertEqual(str(transaction), "Paycheck")

class DashboardTests(TestCase):
    def test_dashboard_loads(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tracker/dashboard.html")

    def test_dashboard_calculates_balances(self):
        Transaction.objects.create(
            description="Paycheck",
            amount=Decimal("3000.00"),
            transaction_type="income",
            date=date.today()
        )
        Transaction.objects.create(
            description="Rent",
            amount=Decimal("1200.00"),
            transaction_type="expense",
            date=date.today()
        )
        response = self.client.get(reverse("dashboard"), {"month": "2026-11"})
        self.assertEqual(response.context["income"], Decimal("3000.00"))
        self.assertEqual(response.context["expenses"], Decimal("1200.00"))
        self.assertEqual(response.context["remaining"], Decimal("1800.00"))  # Remaining balance

    def test_dashboard_with_no_transactions(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.context["remaining"], Decimal("0.00"))

    def test_dashboard_filters_by_month(self):
        Transaction.objects.create(
            description="October Paycheck",
            amount=Decimal("2000.00"),
            transaction_type="income",
            date=date(2026, 10, 15)
        )
        Transaction.objects.create(
            description="November Paycheck",
            amount=Decimal("3000.00"),
            transaction_type="income",
            date=date(2026, 11, 1)
        )
        response = self.client.get(reverse("dashboard"), {"month": "2026-11"})
        self.assertEqual(response.context["income"], Decimal("3000.00"))
        self.assertEqual(response.context["transactions"].count(),1)  # One transaction in November

class TransactionFormTests(TestCase):
    def test_add_transaction_page_loads(self):
        response = self.client.get(reverse("add_transaction"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tracker/add_transaction.html")

    def test_valid_transaction_is_saved(self):
        response = self.client.post(reverse("add_transaction"), {
            "description": "Gas",
            "amount": "50.00",
            "transaction_type": "expense",
            "date": date.today()
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful save
        self.assertRedirects(response, reverse("dashboard"))
        self.assertEqual(Transaction.objects.count(), 1)

        transaction = Transaction.objects.first()
        self.assertEqual(transaction.description, "Gas")
        self.assertEqual(transaction.amount, Decimal("50.00"))

    def test_invalid_transaction_is_not_saved(self):
        response = self.client.post(reverse("add_transaction"), {
            "description": "",  # Invalid: description is required
            "amount": "50.00",
            "transaction_type": "expense",
            "date": date.today()
        })
        self.assertEqual(response.status_code, 200)  # Form re-rendered with errors
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertContains(response, "This field is required.")  # Check for error message