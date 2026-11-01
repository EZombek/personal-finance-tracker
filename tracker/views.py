from decimal import Decimal

from django.db.models import Sum
from django.shortcuts import render, redirect

from .forms import TransactionForm
from .models import Transaction

def dashboard(request):
    income = (
        Transaction.objects
        .filter(transaction_type="income")
        .aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    )

    expenses = (
        Transaction.objects
        .filter(transaction_type="expense")
        .aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    )

    remaining = income - expenses

    transactions = Transaction.objects.order_by("-date")[:10]

    context = {
        'income': income,
        'expenses': expenses,
        'remaining': remaining,
        'transactions': transactions
    }

    return render(request, 'tracker/dashboard.html', context)

def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = TransactionForm()

    return render(request, "tracker/add_transaction.html", {"form": form})