import sys
import os
import pytest
import numpy as np

# Add parent directory to path to import from app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.calculations import calculate_investment_growth, generate_growth_data

def test_standard_case():
    """Test a standard case with 3% return over 10 years."""
    principal = 5400  # 1800 CHF × 3 months
    annual_rate = 3
    years = 10
    expected = principal * (1 + annual_rate/100) ** years
    result = calculate_investment_growth(principal, annual_rate, years)
    assert np.isclose(result, expected)
    assert np.isclose(result, 7260.51, rtol=1e-3)  # Approx 7260.51 CHF

def test_edge_case_zero_return():
    """Test with 0% return - should equal principal."""
    principal = 5400
    annual_rate = 0
    years = 5
    result = calculate_investment_growth(principal, annual_rate, years)
    assert result == principal

def test_edge_case_zero_deposit():
    """Test with 0 deposit - should remain 0."""
    principal = 0
    annual_rate = 3
    years = 10
    result = calculate_investment_growth(principal, annual_rate, years)
    assert result == 0

def test_edge_case_one_year():
    """Test with just 1 year of growth."""
    principal = 5400
    annual_rate = 3
    years = 1
    expected = principal * 1.03
    result = calculate_investment_growth(principal, annual_rate, years)
    assert np.isclose(result, expected)

def test_high_return():
    """Test with 5% return over 15 years."""
    principal = 5400
    annual_rate = 5
    years = 15
    expected = principal * (1 + annual_rate/100) ** years
    result = calculate_investment_growth(principal, annual_rate, years)
    assert np.isclose(result, expected)
    # The expected value should be approximately 11226.21
    assert np.isclose(result, 11226.21, rtol=1e-3)

def test_generate_growth_data():
    """Test generate_growth_data function."""
    deposit_amount = 5400
    return_rate = 3
    time_horizons = [1, 5, 10, 15]
    
    results = generate_growth_data(deposit_amount, return_rate, time_horizons)
    
    # Check that we have the correct number of results
    assert len(results) == len(time_horizons)
    
    # Check that the structure is correct
    expected_keys = ["Years", "0% Return (CHF)", f"{return_rate}% Return (CHF)", 
                     "Difference (CHF)", "Growth (%)"]
    for result in results:
        assert all(key in result for key in expected_keys)
    
    # Check calculation for first year
    first_year = next(r for r in results if r["Years"] == 1)
    expected_growth = deposit_amount * 1.03
    assert np.isclose(first_year[f"{return_rate}% Return (CHF)"], expected_growth)
    assert np.isclose(first_year["Difference (CHF)"], expected_growth - deposit_amount)
    assert np.isclose(first_year["Growth (%)"], 3.0) 