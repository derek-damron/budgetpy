"""
Item module for BudgetPy
"""

from datetime import datetime, date
from typing import Union, Optional
import re
from dateutil.relativedelta import relativedelta


class Item:
    """
    A class representing a budget item with name, amount, date, and optional recurrence pattern.
    """
    
    def __init__(
        self,
        name: str,
        amount: float,
        day: Union[str, date],
        recurring: Optional[str] = None
    ):
        """
        Initialize a budget item.
        
        Args:
            name: The name describing the budget item
            amount: The amount associated with the budget item (positive for income, negative for expenses)
            day: The date associated with the budget item (can be string in YYYY-MM-DD format or date object)
            recurring: Optional recurrence pattern (e.g., "monthly", "weekly", "2 weeks", etc.)
        """
        self.name = self._validate_name(name)
        self.amount = self._validate_amount(amount)
        self.day = self._validate_day(day)
        self.recurring = self._validate_recurring(recurring)
    
    def _validate_name(self, name: str) -> str:
        """Validate and convert the name to string."""
        if not isinstance(name, str):
            try:
                name = str(name)
            except (ValueError, TypeError):
                raise ValueError("Name must be convertible to string")
        return name
    
    def _validate_amount(self, amount: Union[int, float, str]) -> float:
        """Validate and convert the amount to float."""
        if not isinstance(amount, (int, float)):
            try:
                amount = float(amount)
            except (ValueError, TypeError):
                raise ValueError("Amount must be a number")
        return float(amount)
    
    def _validate_day(self, day: Union[str, date]) -> date:
        """Validate and convert the day to date object."""
        if isinstance(day, str):
            try:
                day = datetime.strptime(day, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Day must be in YYYY-MM-DD format or a date object")
        elif not isinstance(day, date):
            raise ValueError("Day must be a string in YYYY-MM-DD format or a date object")
        return day
    
    def _validate_recurring(self, recurring: Optional[str]) -> Optional[str]:
        """Validate the recurring pattern."""
        if recurring is None:
            return None
            
        valid_patterns = {
            r'^daily$|^1 day$': 'daily',
            r'^\d+ days$': 'days',
            r'^weekly$|^1 week$': 'weekly',
            r'^\d+ weeks$': 'weeks',
            r'^monthly$|^1 month$': 'monthly',
            r'^\d+ months$': 'months',
            r'^yearly$|^1 year$': 'yearly',
            r'^\d+ years$': 'years'
        }
        
        for pattern, _ in valid_patterns.items():
            if re.match(pattern, recurring.lower()):
                return recurring.lower()
        
        raise ValueError(
            "Invalid recurring pattern. Must be one of: "
            "daily, weekly, monthly, yearly, or X days/weeks/months/years"
        )
    
    def get_next_date(self, start_date: date) -> Optional[date]:
        """
        Get the next occurrence of this item after the given start date.
        
        Args:
            start_date: The date to start looking from
            
        Returns:
            The next date this item occurs, or None if it's a one-time item
        """
        if self.recurring is None:
            return None if self.day < start_date else self.day
            
        # Parse the recurring pattern
        if self.recurring == 'daily':
            delta = relativedelta(days=1)
        elif self.recurring == 'weekly':
            delta = relativedelta(weeks=1)
        elif self.recurring == 'monthly':
            delta = relativedelta(months=1)
        elif self.recurring == 'yearly':
            delta = relativedelta(years=1)
        else:
            # Handle patterns like "2 weeks", "3 months", etc.
            value, unit = self.recurring.split()
            value = int(value)
            if unit == 'days':
                delta = relativedelta(days=value)
            elif unit == 'weeks':
                delta = relativedelta(weeks=value)
            elif unit == 'months':
                delta = relativedelta(months=value)
            elif unit == 'years':
                delta = relativedelta(years=value)
        
        # Find the next occurrence
        next_date = self.day
        while next_date < start_date:
            next_date += delta
            
        return next_date
    
    def __repr__(self) -> str:
        """Return a string representation of the item."""
        recurring_str = f", recurring='{self.recurring}'" if self.recurring else ""
        return f"Item(name='{self.name}', amount={self.amount}, day={self.day}{recurring_str})" 