"""
Tests for the Item class
"""

import pytest
from datetime import date
from budgetpy.item import Item


class TestItemArguments:
    """Test the argument validation in Item class"""
    
    def test_name_validation(self):
        """Test name argument validation"""
        # Test missing name
        with pytest.raises(ValueError, match="Name must be convertible to string"):
            Item(name=None, amount=1000, day="2016-01-01")
            
        # Test non-string name
        with pytest.raises(ValueError, match="Name must be convertible to string"):
            Item(name=object(), amount=1000, day="2016-01-01")
            
        # Test numeric name (should be converted to string)
        item = Item(name=1, amount=1000, day="2016-01-01")
        assert item.name == "1"
        
    def test_amount_validation(self):
        """Test amount argument validation"""
        # Test missing amount
        with pytest.raises(ValueError, match="Amount must be a number"):
            Item(name="Paycheck", amount=None, day="2016-01-01")
            
        # Test non-numeric amount
        with pytest.raises(ValueError, match="Amount must be a number"):
            Item(name="Paycheck", amount="not a number", day="2016-01-01")
            
        # Test string amount (should be converted to float)
        item = Item(name="Paycheck", amount="1000", day="2016-01-01")
        assert item.amount == 1000.0
        
    def test_day_validation(self):
        """Test day argument validation"""
        # Test missing day
        with pytest.raises(ValueError, match="Day must be in YYYY-MM-DD format or a date object"):
            Item(name="Paycheck", amount=1000, day=None)
            
        # Test invalid date string
        with pytest.raises(ValueError, match="Day must be in YYYY-MM-DD format or a date object"):
            Item(name="Paycheck", amount=1000, day="invalid date")
            
        # Test date object
        test_date = date(2016, 1, 1)
        item = Item(name="Paycheck", amount=1000, day=test_date)
        assert item.day == test_date
        
        # Test date string
        item = Item(name="Paycheck", amount=1000, day="2016-01-01")
        assert item.day == date(2016, 1, 1)
        
    def test_recurring_validation(self):
        """Test recurring argument validation"""
        # Test no recurring (should be None)
        item = Item(name="Paycheck", amount=1000, day="2016-01-01")
        assert item.recurring is None
        
        # Test invalid recurring pattern
        with pytest.raises(ValueError, match="Invalid recurring pattern"):
            Item(name="Paycheck", amount=1000, day="2016-01-01", recurring="invalid")
            
        # Test valid recurring patterns
        valid_patterns = [
            "daily", "1 day", "2 days",
            "weekly", "1 week", "2 weeks",
            "monthly", "1 month", "2 months",
            "yearly", "1 year", "2 years"
        ]
        for pattern in valid_patterns:
            item = Item(name="Paycheck", amount=1000, day="2016-01-01", recurring=pattern)
            assert item.recurring == pattern.lower()


class TestItemOutput:
    """Test the output/behavior of Item class"""
    
    def test_item_creation(self):
        """Test successful item creation"""
        item = Item(
            name="Paycheck",
            amount=1000,
            day="2016-01-01",
            recurring="monthly"
        )
        
        assert isinstance(item, Item)
        assert item.name == "Paycheck"
        assert item.amount == 1000.0
        assert item.day == date(2016, 1, 1)
        assert item.recurring == "monthly"
        
    def test_get_next_date(self):
        """Test the get_next_date method"""
        # Test one-time item
        item = Item(name="One-time", amount=1000, day="2016-01-01")
        assert item.get_next_date(date(2015, 12, 1)) == date(2016, 1, 1)
        assert item.get_next_date(date(2016, 1, 2)) is None
        
        # Test monthly recurring
        item = Item(name="Monthly", amount=1000, day="2016-01-01", recurring="monthly")
        assert item.get_next_date(date(2015, 12, 1)) == date(2016, 1, 1)
        assert item.get_next_date(date(2016, 1, 1)) == date(2016, 1, 1)
        assert item.get_next_date(date(2016, 1, 2)) == date(2016, 2, 1)
        
        # Test weekly recurring
        item = Item(name="Weekly", amount=1000, day="2016-01-01", recurring="weekly")
        assert item.get_next_date(date(2015, 12, 25)) == date(2016, 1, 1)
        assert item.get_next_date(date(2016, 1, 1)) == date(2016, 1, 1)
        assert item.get_next_date(date(2016, 1, 2)) == date(2016, 1, 8)

        # Test multi-interval recurring patterns
        daily_item = Item(name="Every 2 days", amount=100, day="2016-01-01", recurring="2 days")
        assert daily_item.get_next_date(date(2015, 12, 31)) == date(2016, 1, 1)
        # After the base date, next occurrences should be spaced by 2 days
        assert daily_item.get_next_date(date(2016, 1, 2)) == date(2016, 1, 3)

        weekly_item = Item(name="Every 2 weeks", amount=100, day="2016-01-01", recurring="2 weeks")
        assert weekly_item.get_next_date(date(2015, 12, 25)) == date(2016, 1, 1)
        assert weekly_item.get_next_date(date(2016, 1, 2)) == date(2016, 1, 15)

        monthly_item = Item(name="Every 2 months", amount=100, day="2016-01-01", recurring="2 months")
        assert monthly_item.get_next_date(date(2015, 12, 1)) == date(2016, 1, 1)
        assert monthly_item.get_next_date(date(2016, 1, 2)) == date(2016, 3, 1)

        yearly_item = Item(name="Every 2 years", amount=100, day="2016-01-01", recurring="2 years")
        assert yearly_item.get_next_date(date(2015, 1, 1)) == date(2016, 1, 1)
        assert yearly_item.get_next_date(date(2016, 1, 2)) == date(2018, 1, 1)
        
    def test_repr(self):
        """Test the string representation of Item"""
        # Test without recurring
        item = Item(name="One-time", amount=1000, day="2016-01-01")
        assert repr(item) == "Item(name='One-time', amount=1000.0, day=datetime.date(2016, 1, 1))"
        
        # Test with recurring
        item = Item(name="Monthly", amount=1000, day="2016-01-01", recurring="monthly")
        assert repr(item) == "Item(name='Monthly', amount=1000.0, day=datetime.date(2016, 1, 1), recurring='monthly')" 