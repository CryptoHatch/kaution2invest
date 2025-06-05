"""
Utility functions for financial calculations in the Kaution2Invest application.
"""

def calculate_investment_growth(principal, annual_rate, years):
    """
    Calculate the future value of an investment with compound interest.
    
    This function uses the compound interest formula: P * (1 + r)^t
    - P: principal (initial investment)
    - r: annual interest rate (as decimal)
    - t: time in years
    
    The compound effect accelerates growth over time as interest is earned
    not just on the principal, but also on the accumulated interest.
    
    Args:
        principal (float): Initial investment amount in CHF
        annual_rate (float): Annual interest rate (in percentage)
        years (int): Investment duration in years
        
    Returns:
        float: Future value of the investment
    """
    rate_decimal = annual_rate / 100
    future_value = principal * (1 + rate_decimal) ** years
    return future_value

def generate_growth_data(deposit_amount, return_rate, time_horizons):
    """
    Generate investment growth data for comparison between 0% and selected return rate.
    
    This function compares two scenarios for each time horizon:
    1. No growth (0% interest) - The deposit amount remains constant
    2. Compound growth - The deposit grows with compound interest at the selected rate
    
    Args:
        deposit_amount (float): Initial deposit amount in CHF
        return_rate (float): Selected annual return rate (in percentage)
        time_horizons (list): List of years to calculate for
        
    Returns:
        list: List of dictionaries containing calculated values for each time horizon
    """
    results = []
    for years in time_horizons:
        zero_growth = deposit_amount  # 0% growth (constant)
        investment_growth = calculate_investment_growth(deposit_amount, return_rate, years)
        absolute_difference = investment_growth - zero_growth
        percentage_difference = (absolute_difference / zero_growth) * 100
        
        results.append({
            "Years": years,
            "0% Return (CHF)": zero_growth,
            f"{return_rate}% Return (CHF)": investment_growth,
            "Difference (CHF)": absolute_difference,
            "Growth (%)": percentage_difference
        })
    
    return results 