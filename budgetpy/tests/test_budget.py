"""
Tests for the Budget class
"""

import pytest
from datetime import date
import pandas as pd
from budgetpy.item import Item
from budgetpy.schedule import Schedule
from budgetpy.budget import Budget


class TestBudgetArguments:
    """Test the argument validation in Budget class"""
    
    @pytest.fixture
    def sample_schedule(self):
        """Create a sample schedule for testing"""
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
        return Schedule(paycheck, rent)
    
    def test_schedule_validation(self, sample_schedule):
        """Test schedule argument validation"""
        with pytest.raises(ValueError, match="Please provide a schedule for your budget"):
            Budget(schedule=None)
            
        with pytest.raises(ValueError, match="The object provided is not a schedule"):
            Budget(schedule="not a schedule")
            
    def test_start_validation(self, sample_schedule):
        """Test start date validation"""
        with pytest.raises(ValueError, match="Date must be in YYYY-MM-DD format or a date object"):
            Budget(schedule=sample_schedule, start=1)
            
        # Test valid start dates
        valid_dates = [
            date(2016, 1, 1),
            "2016-01-01",
            "20160101"
        ]
        for start_date in valid_dates:
            budget = Budget(schedule=sample_schedule, start=start_date, initial=0)
            assert budget.start == date(2016, 1, 1)
            
    def test_end_validation(self, sample_schedule):
        """Test end date validation"""
        with pytest.raises(ValueError, match="Date must be in YYYY-MM-DD format or a date object"):
            Budget(schedule=sample_schedule, start="2016-01-01", end=1)
            
        with pytest.raises(ValueError, match="end date must be after start date"):
            Budget(schedule=sample_schedule, start="2016-01-02", end="2016-01-01")
            
        # Test valid end dates
        valid_dates = [
            date(2016, 1, 5),
            "2016-01-05",
            "20160105"
        ]
        for end_date in valid_dates:
            budget = Budget(schedule=sample_schedule, start="2016-01-01", end=end_date, initial=0)
            assert budget.end == date(2016, 1, 5)
            
    def test_initial_validation(self, sample_schedule):
        """Test initial amount validation"""
        with pytest.raises(ValueError, match="Amount must be a number"):
            Budget(schedule=sample_schedule, initial="not a number")
            
        # Test valid initial amounts
        valid_amounts = [1000, "1000", 1000.0]
        for amount in valid_amounts:
            budget = Budget(schedule=sample_schedule, start="2016-01-01", end="2016-02-01", initial=amount)
            assert budget.initial == 1000.0


class TestBudgetOutput:
    """Test the output/behavior of Budget class"""
    
    @pytest.fixture
    def complex_schedule(self):
        """Create a complex schedule with multiple items"""
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
        return Schedule(paycheck, rent, groceries, xmas_gifts)
    
    def test_budget_creation(self, complex_schedule):
        """Test creating a budget with multiple items"""
        budget = Budget(
            schedule=complex_schedule,
            start="2015-12-15",
            end="2016-03-02",
            initial=1000
        )
        
        assert isinstance(budget, Budget)
        assert isinstance(budget.df, pd.DataFrame)
        assert len(budget.df) > 0
        assert all(col in budget.df.columns for col in ['date', 'name', 'amount', 'balance'])
        
        # Check some specific values
        assert budget.df.iloc[0]['name'] == "Initial Amount"
        assert budget.df.iloc[0]['amount'] == 1000
        assert budget.df.iloc[0]['balance'] == 1000
        
    def test_get_balance(self, complex_schedule):
        """Test getting balance at specific dates"""
        budget = Budget(
            schedule=complex_schedule,
            start="2015-12-15",
            end="2016-03-02",
            initial=1000
        )
        
        # Test balance at start
        assert budget.get_balance("2015-12-15") == 1000
        
        # Test balance after first paycheck
        assert budget.get_balance("2016-01-01") == 1300
        
        # Test balance after first rent payment
        assert budget.get_balance("2016-01-05") == 800
        
        # Test balance at end
        assert budget.get_balance("2016-03-02") == 1900
        
        # Test invalid date
        with pytest.raises(ValueError, match="Date must be within the budget period"):
            budget.get_balance("2015-12-14")
            
        with pytest.raises(ValueError, match="Date must be within the budget period"):
            budget.get_balance("2016-03-03")
            
    def test_plot(self, complex_schedule):
        """Test the plot method"""
        budget = Budget(
            schedule=complex_schedule,
            start="2015-12-15",
            end="2016-03-02",
            initial=1000
        )
        
        # The plot method should not raise any exceptions
        budget.plot()
        
    def test_repr(self, complex_schedule):
        """Test the string representation of Budget"""
        budget = Budget(
            schedule=complex_schedule,
            start="2015-12-15",
            end="2016-03-02",
            initial=1000
        )
        
        expected = (
            "Budget(start=datetime.date(2015, 12, 15), end=datetime.date(2016, 3, 2), "
            "initial=1000.0, items=4)"
        )
        assert repr(budget) == expected 