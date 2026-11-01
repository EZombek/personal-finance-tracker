from django.db import models

# Create your models here.
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(
        max_length=7, choices=TRANSACTION_TYPES
    )

    date = models.DateField()

    def __str__(self):
        return self.description