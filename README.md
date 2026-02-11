# budgetpy

A Python package for personal budget management, inspired by the R package `budgetr`.

## Installation

**Requirements:** Python 3.14+

From [PyPI](https://pypi.org/project/budgetpy/) (when published):

```bash
pip install budgetpy
```

With [uv](https://github.com/astral-sh/uv): `uv pip install budgetpy`

From source (development):

```bash
git clone https://github.com/yourusername/budgetpy.git
cd budgetpy
pip install -e .
```

With uv: `uv pip install -e .`

Dependencies (pandas, matplotlib, python-dateutil) are installed automatically with the package.

## Usage

Here's a simple example of how to use budgetpy. For a fuller example with one-time items, "2 weeks" recurrence, and inspecting the transaction table, see [main.py](main.py).

```python
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

# Get end-date balance (omit the date argument)
print(f"Final balance: ${my_budget.get_balance():.2f}")

# Inspect the transaction table (date, name, amount, balance)
print(my_budget.df)

# Plot the budget balance over time
my_budget.plot()
```

## Features

- Create budget items with recurring patterns (daily, weekly, monthly, yearly) or N-unit patterns (e.g. "2 weeks", "3 months")
- One-time (non-recurring) items for single expenses or income
- Manage multiple items in a schedule
- Track balance over time
- Inspect or export the transaction table as a pandas DataFrame (`Budget.df`)
- Visualize budget with matplotlib plots
- Flexible date handling (string dates in YYYY-MM-DD or YYYYMMDD format, or `datetime.date` objects)

## Development

Install in editable mode with dev dependencies (pytest, pytest-cov), then run the test suite:

```bash
pip install -e ".[dev]"
pytest
```

With [uv](https://github.com/astral-sh/uv): `uv pip install -e ".[dev]"` and `uv run pytest`.

Run tests with coverage: `pytest --cov=budgetpy` (or `uv run pytest --cov=budgetpy`). For an HTML report: `pytest --cov=budgetpy --cov-report=html` (output in `htmlcov/`).

## License

MIT License 