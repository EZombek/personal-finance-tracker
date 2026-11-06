from decimal import Decimal

from django.db.models import Sum
from django.shortcuts import render, redirect

from .forms import TransactionForm
from .models import Transaction

def dashboard(request):
    from datetime import date
    today = date.today()

    selected_month = request.GET.get("month", today.strftime("%Y-%m"))

    try:
        year, month = map(int, selected_month.split("-"))
        selected_date = date(year, month, 1)
    except (ValueError, TypeError):
        selected_date = today.replace(day=1)

    selected_month = selected_date.strftime("%Y-%m")
    monthly_transactions = Transaction.objects.filter(
        date__year=selected_date.year, date__month=selected_date.month
    )

    income = (monthly_transactions.filter(transaction_type="income").aggregate(total=Sum("amount"))["total"] or Decimal("0.00"))

    expenses = (monthly_transactions.filter(transaction_type="expense").aggregate(total=Sum("amount"))["total"] or Decimal("0.00"))

    remaining = income - expenses

    category_totals = monthly_transactions.filter(transaction_type="expense").values("category").annotate(total=Sum("amount")).order_by("-total")

    category_choices = dict(Transaction.CATEGORIES)

    spending_categories = [
        {
            "name": category_choices.get(item["category"], item["category"]),
            "amount": item["total"],
            "percentage": (item["total"] / expenses * 100) if expenses > 0 else Decimal("0.00"),
        }
        for item in category_totals
    ]

    transactions = monthly_transactions.order_by("-date", "-id")

    context = {
        'income': income,
        'expenses': expenses,
        'remaining': remaining,
        'transactions': transactions,
        'selected_month': selected_month,
        'spending_categories': spending_categories,
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