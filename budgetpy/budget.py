"""
Budget module for BudgetPy
"""

from datetime import date, datetime
from typing import Union, Optional
import pandas as pd
from .schedule import Schedule
from .item import Item


class Budget:
    """
    A class representing a personal budget with income and expenses over a time period.
    """
    
    def __init__(
        self,
        schedule: Schedule,
        start: Union[str, date] = date.today(),
        end: Optional[Union[str, date]] = None,
        initial: float = 0.0
    ):
        """
        Initialize a budget with a schedule of items.
        
        Args:
            schedule: A Schedule object containing the budget items
            start: The start date for the budget (default: today)
            end: The end date for the budget (default: 90 days after start)
            initial: The initial amount in the budget (default: 0.0)
        """
        if schedule is None:
            raise ValueError("Please provide a schedule for your budget")
        if not isinstance(schedule, Schedule):
            raise ValueError("The object provided is not a schedule")
        self.schedule = schedule
        self.start = self._validate_date(start)
        self.end = self._validate_date(end) if end else self.start + pd.Timedelta(days=90)
        self.initial = self._validate_amount(initial)
        
        if self.start >= self.end:
            raise ValueError("end date must be after start date")
            
        # Create the budget DataFrame
        self.df = self._create_budget_df()
    
    def _validate_date(self, date_value: Union[str, date]) -> date:
        """Validate and convert a date value to a date object."""
        if isinstance(date_value, str):
            try:
                return datetime.strptime(date_value, "%Y-%m-%d").date()
            except ValueError:
                try:
                    return datetime.strptime(date_value, "%Y%m%d").date()
                except ValueError:
                    raise ValueError("Date must be in YYYY-MM-DD format or a date object")
        elif not isinstance(date_value, date):
            raise ValueError("Date must be in YYYY-MM-DD format or a date object")
        return date_value
    
    def _validate_amount(self, amount: Union[int, float, str]) -> float:
        """Validate and convert an amount to float."""
        if not isinstance(amount, (int, float)):
            try:
                amount = float(amount)
            except (ValueError, TypeError):
                raise ValueError("Amount must be a number")
        return float(amount)
    
    def _create_budget_df(self) -> pd.DataFrame:
        """Create the budget DataFrame from the schedule."""
        # Get all items from the schedule
        schedule_df = self.schedule.extend_items(self.start, self.end)
        
        if schedule_df.empty:
            raise ValueError("No items in the schedule apply between start and end dates")
        
        # Add initial amount row
        initial_row = pd.DataFrame({
            'date': [self.start],
            'name': ['Initial Amount'],
            'amount': [self.initial]
        })
        
        # Combine and sort
        df = pd.concat([initial_row, schedule_df], ignore_index=True)
        df = df.sort_values('date')
        
        # Calculate running balance
        df['balance'] = df['amount'].cumsum()
        
        return df
    
    def get_balance(self, date: Optional[Union[str, date]] = None) -> float:
        """
        Get the balance on a specific date.
        
        Args:
            date: The date to get the balance for (default: end date)
            
        Returns:
            The balance on the specified date
        """
        if date is None:
            return self.df['balance'].iloc[-1]
            
        date = self._validate_date(date)
        if date < self.start or date > self.end:
            raise ValueError("Date must be within the budget period")

        # Balance at start date is the initial amount (before same-day transactions)
        if date == self.start:
            return self.initial
            
        # Find the last row with date <= specified date
        mask = self.df['date'] <= date
        if not mask.any():
            return self.initial
            
        return self.df.loc[mask, 'balance'].iloc[-1]
    
    def plot(self) -> None:
        """Plot the budget balance over time."""
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 6))
        plt.plot(self.df['date'], self.df['balance'])
        plt.title('Budget Balance Over Time')
        plt.xlabel('Date')
        plt.ylabel('Balance')
        plt.grid(True)
        plt.show()
    
    def __repr__(self) -> str:
        """Return a string representation of the budget."""
        start_repr = f"datetime.date({self.start.year}, {self.start.month}, {self.start.day})"
        end_repr = f"datetime.date({self.end.year}, {self.end.month}, {self.end.day})"
        return (
            f"Budget(start={start_repr}, end={end_repr}, initial={self.initial}, "
            f"items={len(self.schedule.items)})"
        ) 