"""
Schedule module for BudgetPy
"""

from datetime import date
from typing import List, Optional, Union
import pandas as pd
from .item import Item


class Schedule:
    """
    A class representing a collection of budget items with their recurrence patterns.
    """
    
    def __init__(self, *items: Item):
        """
        Initialize a schedule with one or more budget items.
        
        Args:
            *items: One or more Item objects to include in the schedule
        """
        self.items = []
        for item in items:
            if not isinstance(item, Item):
                raise ValueError("All arguments must be Item objects")
            self.items.append(item)
    
    def add_item(self, item: Item) -> None:
        """
        Add an item to the schedule.
        
        Args:
            item: The Item object to add
        """
        if not isinstance(item, Item):
            raise ValueError("Argument must be an Item object")
        self.items.append(item)
    
    def get_items(self) -> List[Item]:
        """
        Get all items in the schedule.
        
        Returns:
            List of Item objects in the schedule
        """
        return self.items
    
    def extend_items(self, start_date: date, end_date: date) -> pd.DataFrame:
        """
        Extend all items in the schedule to cover the specified date range.
        
        Args:
            start_date: The start date for the schedule
            end_date: The end date for the schedule
            
        Returns:
            DataFrame containing all occurrences of items within the date range
        """
        if not isinstance(start_date, date) or not isinstance(end_date, date):
            raise ValueError("start_date and end_date must be date objects")
        if start_date >= end_date:
            raise ValueError("end_date must be after start_date")
            
        data = []
        for item in self.items:
            current_date = item.get_next_date(start_date)
            while current_date is not None and current_date <= end_date:
                data.append({
                    'date': current_date,
                    'name': item.name,
                    'amount': item.amount
                })
                current_date = item.get_next_date(current_date + pd.Timedelta(days=1))
        
        if not data:
            return pd.DataFrame(columns=['date', 'name', 'amount'])
            
        df = pd.DataFrame(data)
        df = df.sort_values('date')
        df.reset_index(drop=True, inplace=True)
        return df
    
    def __repr__(self) -> str:
        """Return a string representation of the schedule."""
        items_str = ", ".join(repr(item) for item in self.items)
        return f"Schedule({items_str})" 