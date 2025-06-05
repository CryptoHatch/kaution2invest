import streamlit as st
import pandas as pd
import numpy as np

# Import utility functions
from utils.calculations import calculate_investment_growth, generate_growth_data
from utils.visualization import create_growth_comparison_chart

# Set page config
st.set_page_config(
    page_title="Kaution2Invest - Swiss Deposit Investment Calculator",
    page_icon="💰",
    layout="wide"
)

# App title and description
st.title("Swiss Deposit Investment Calculator")
st.markdown("""
This tool helps you visualize how your rental deposit could grow if invested over time,
compared to leaving it as a standard 0% deposit.
""")

# User input section
st.subheader("Enter Your Details")

col1, col2, col3 = st.columns(3)

with col1:
    rent_amount = st.number_input(
        "Monthly Rent (CHF)",
        min_value=0,
        value=1800,
        step=100,
        help="Your current monthly rent in Swiss Francs"
    )

with col2:
    deposit_months = st.number_input(
        "Deposit Duration (months)",
        min_value=0,
        value=3,
        step=1,
        help="Number of months your deposit covers (typically 3 months in Switzerland)"
    )

with col3:
    return_rate = st.selectbox(
        "Annual Return Rate",
        options=[1, 3, 5],
        index=1,  # Default to 3%
        format_func=lambda x: f"{x}%",
        help="Expected annual return rate on your investment"
    )

# Calculate the initial deposit amount
deposit_amount = rent_amount * deposit_months

# Display the initial deposit amount
st.markdown(f"**Total Deposit Amount: {deposit_amount:,.2f} CHF**")

# Add explanation about compound interest
st.info("""
💡 **Understanding Compound Interest**

With compound interest, your investment grows not just on the initial amount, but also on the accumulated interest 
over time. This creates an accelerating growth effect:

- **Year 1**: You earn interest only on your initial deposit
- **Year 2+**: You earn interest on both your initial deposit AND previous interest

This is why the investment growth curve bends upward over longer time periods.
""")

# Time horizons for calculation
time_horizons = [1, 5, 10, 15, 20]  # years - added 20 years

# Generate growth data
results = generate_growth_data(deposit_amount, return_rate, time_horizons)

# Create a dataframe for the results table
results_df = pd.DataFrame(results)

# Define a styling function for the dataframe
def highlight_columns(df):
    # Create a style object
    styled = df.style.format({
        "0% Return (CHF)": "{:,.2f}",
        f"{return_rate}% Return (CHF)": "{:,.2f}",
        "Difference (CHF)": "{:,.2f}",
        "Growth (%)": "{:.2f}%"
    })
    
    # Apply background colors to specific columns
    # Light red for 0% return column
    styled = styled.set_properties(
        subset=["0% Return (CHF)"],
        **{'background-color': '#ffebee', 'color': '#000000'}  # Very light red with black text
    )
    
    # Light blue for return rate column
    styled = styled.set_properties(
        subset=[f"{return_rate}% Return (CHF)"],
        **{'background-color': '#e3f2fd', 'color': '#000000'}  # Very light blue with black text
    )
    
    return styled

# Display the results table with styling
st.subheader("Investment Growth Comparison")
st.dataframe(
    highlight_columns(results_df),
    use_container_width=True
)

# Create visualization
st.subheader("Growth Visualization")

# Create and display chart
chart = create_growth_comparison_chart(deposit_amount, return_rate)
st.plotly_chart(chart, use_container_width=True)

# Add explanation
st.markdown("""
### How to Interpret These Results

- The **0% Return** (red line) represents your deposit if left in a standard rental deposit account with no interest.
- The **Investment Return** (blue line with markers) shows how your money could grow if invested at the selected rate.
- Notice how the blue line curves upward over time - this is the **compound interest effect** in action.
- In later years, your investment grows faster because you're earning interest on previously earned interest.

**Example calculation:** For an initial deposit of 5,400 CHF at 3% annual return:
- After 1 year: 5,400 CHF × (1 + 0.03) = 5,562 CHF
- After 2 years: 5,400 CHF × (1 + 0.03)² = 5,729 CHF (not just 5,724 CHF)

**Note:** This is a simplified calculation that assumes consistent annual returns and does not account for inflation, taxes, or investment fees.
""") 