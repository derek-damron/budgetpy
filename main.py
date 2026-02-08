"""
End-to-end example: build a budget from items and inspect balances.
Uses the same budget setup as tests/test_budget.py.
"""

from budgetpy.item import Item
from budgetpy.schedule import Schedule
from budgetpy.budget import Budget


def main():
    # Income and expenses (same as test_budget.py complex_schedule)
    paycheck = Item(
        name="Paycheck",
        amount=1000,
        day="2016-01-01",
        recurring="monthly"
    )
    rent = Item(
        name="Rent",
        amount=-500,
        day="2016-01-05",
        recurring="monthly"
    )
    groceries = Item(
        name="Groceries",
        amount=-100,
        day="2015-12-15",
        recurring="2 weeks"
    )
    xmas_gifts = Item(
        name="Christmas Gifts",
        amount=-500,
        day="2015-12-20"
    )

    schedule = Schedule(paycheck, rent, groceries, xmas_gifts)
    budget = Budget(
        schedule=schedule,
        start="2015-12-15",
        end="2016-03-02",
        initial=1000
    )

    print(budget)
    print()
    print("Balance at sample dates:")
    for d in ["2015-12-15", "2016-01-01", "2016-01-27", "2016-03-01"]:
        print(f"  {d}: {budget.get_balance(d):,.2f}")
    print()
    print("Transactions:")
    print(budget.df.to_string(index=False))


if __name__ == "__main__":
    main()
