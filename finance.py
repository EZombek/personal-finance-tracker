from decimal import Decimal

# My first income tracker

income = Decimal("5000.00")
expenses = Decimal("3250.00")

remaining = income - expenses

print("PERSONAL FINANCE TRACKER")
print("------------------------")
print(f"Income: ${income:,.2f}")
print(f"Expenses: ${expenses:,.2f}")
print(f"Remaining: ${remaining:,.2f}")