from django.db import models

# Create your models here.
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    CATEGORIES = [
        ("housing", "Housing"),
        ("groceries", "Groceries"),
        ("transportation", "Transportation"),
        ("utilities", "Utilities"),
        ("debt", "Debt"),
        ("healthcare", "Healthcare"),
        ("children", "Children"),
        ("entertainment", "Entertainment"),
        ("savings", "Savings"),
        ("salary", "Salary"),
        ("business", "Business"),
        ("other", "Other"),
    ]

    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=20, choices=CATEGORIES, default="other")

    date = models.DateField()

    def __str__(self):
        return self.description