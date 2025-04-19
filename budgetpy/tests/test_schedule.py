"""
Tests for the Schedule class
"""

import pytest
from datetime import date
import pandas as pd
from budgetpy.item import Item
from budgetpy.schedule import Schedule


class TestScheduleArguments:
    """Test the argument validation in Schedule class"""
    
    def test_empty_schedule(self):
        """Test creating a schedule with no items"""
        with pytest.raises(ValueError, match="All arguments must be Item objects"):
            Schedule()
            
    def test_invalid_items(self):
        """Test creating a schedule with invalid items"""
        paycheck = Item(name="Paycheck", amount=1000, day="2016-01-01")
        
        with pytest.raises(ValueError, match="All arguments must be Item objects"):
            Schedule(paycheck, "not an item")
            
        with pytest.raises(ValueError, match="All arguments must be Item objects"):
            Schedule(paycheck, 123)


class TestScheduleOutput:
    """Test the output/behavior of Schedule class"""
    
    @pytest.fixture
    def sample_items(self):
        """Create sample items for testing"""
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
        return paycheck, rent
    
    def test_schedule_creation(self, sample_items):
        """Test creating a schedule with items"""
        paycheck, rent = sample_items
        schedule = Schedule(paycheck, rent)
        
        assert isinstance(schedule, Schedule)
        assert len(schedule.items) == 2
        assert schedule.items[0].name == "Paycheck"
        assert schedule.items[0].amount == 1000
        assert schedule.items[0].day == date(2016, 1, 1)
        assert schedule.items[0].recurring == "monthly"
        assert schedule.items[1].name == "Rent"
        assert schedule.items[1].amount == -500
        assert schedule.items[1].day == date(2016, 1, 5)
        assert schedule.items[1].recurring == "monthly"
        
    def test_add_item(self, sample_items):
        """Test adding items to a schedule"""
        paycheck, rent = sample_items
        schedule = Schedule(paycheck)
        
        assert len(schedule.items) == 1
        schedule.add_item(rent)
        assert len(schedule.items) == 2
        assert schedule.items[1].name == "Rent"
        
        with pytest.raises(ValueError, match="Argument must be an Item object"):
            schedule.add_item("not an item")
            
    def test_get_items(self, sample_items):
        """Test getting items from a schedule"""
        paycheck, rent = sample_items
        schedule = Schedule(paycheck, rent)
        
        items = schedule.get_items()
        assert len(items) == 2
        assert items[0].name == "Paycheck"
        assert items[1].name == "Rent"
        
    def test_extend_items(self, sample_items):
        """Test extending items in a schedule"""
        paycheck, rent = sample_items
        schedule = Schedule(paycheck, rent)
        
        start_date = date(2016, 1, 1)
        end_date = date(2016, 2, 1)
        df = schedule.extend_items(start_date, end_date)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert all(col in df.columns for col in ['date', 'name', 'amount'])
        assert df['date'].min() >= start_date
        assert df['date'].max() <= end_date
        
        # Test empty schedule
        empty_schedule = Schedule()
        df = empty_schedule.extend_items(start_date, end_date)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0
        assert all(col in df.columns for col in ['date', 'name', 'amount'])
        
    def test_repr(self, sample_items):
        """Test the string representation of Schedule"""
        paycheck, rent = sample_items
        schedule = Schedule(paycheck, rent)
        
        expected = (
            "Schedule(Item(name='Paycheck', amount=1000.0, day=datetime.date(2016, 1, 1), "
            "recurring='monthly'), Item(name='Rent', amount=-500.0, day=datetime.date(2016, 1, 5), "
            "recurring='monthly'))"
        )
        assert repr(schedule) == expected 