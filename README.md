# BudgetPy

A Python package for personal budget management, inspired by the R package `budgetr`.

## Installation

```bash
pip install budgetpy
```

## Usage

Here's a simple example of how to use BudgetPy:

```python
from datetime import date
from budgetpy import Item, Schedule, Budget

# Create income items
paycheck = Item(
    name="Paycheck",
    amount=1000,
    day="2023-01-01",
    recurring="monthly"
)

# Create expense items
rent = Item(
    name="Rent",
    amount=-500,
    day="2023-01-05",
    recurring="monthly"
)

# Create a schedule
my_schedule = Schedule(paycheck, rent)

# Create a budget
my_budget = Budget(
    schedule=my_schedule,
    start="2023-01-01",
    end="2023-12-31",
    initial=1000
)

# Get the balance on a specific date
balance = my_budget.get_balance("2023-01-15")
print(f"Balance on January 15th: ${balance:.2f}")

# Plot the budget balance over time
my_budget.plot()
```

## Features

- Create budget items with recurring patterns (daily, weekly, monthly, yearly)
- Manage multiple items in a schedule
- Track balance over time
- Visualize budget with matplotlib plots
- Flexible date handling (supports both string dates and datetime.date objects)

## License

MIT License 