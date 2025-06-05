"""
Visualization utilities for the Kaution2Invest application.
"""

import numpy as np
import plotly.graph_objects as go
from utils.calculations import calculate_investment_growth

def create_growth_comparison_chart(deposit_amount, return_rate, years_range=None):
    """
    Create a line chart comparing 0% growth vs. selected investment return rate.
    
    Args:
        deposit_amount (float): Initial deposit amount in CHF
        return_rate (float): Selected annual return rate (in percentage)
        years_range (list, optional): Range of years to plot. Defaults to 0-20 years.
        
    Returns:
        plotly.graph_objects.Figure: Plotly figure object containing the chart
    """
    if years_range is None:
        # Extend to 20 years to make compound effect more visible
        years_range = np.arange(0, 21)
    
    # Calculate values for each year
    zero_growth_values = [deposit_amount] * len(years_range)
    investment_values = [calculate_investment_growth(deposit_amount, return_rate, year) for year in years_range]
    
    # Create a Plotly line chart
    fig = go.Figure()
    
    # Add 0% return line (red)
    fig.add_trace(
        go.Scatter(
            x=years_range,
            y=zero_growth_values,
            mode='lines',
            name='0% Return',
            line=dict(color='red', width=2)
        )
    )
    
    # Add investment return line with markers to highlight compounding effect
    fig.add_trace(
        go.Scatter(
            x=years_range,
            y=investment_values,
            mode='lines+markers',
            name=f'{return_rate}% Return',
            line=dict(color='blue', width=2),
            marker=dict(size=6, symbol='circle')
        )
    )
    
    # Add annotation to explain compound interest
    fig.add_annotation(
        x=years_range[-5],  
        y=investment_values[-5],
        text="Compound interest<br>accelerates growth<br>over time",
        showarrow=True,
        arrowhead=1,
        ax=-50,
        ay=-40
    )
    
    # Update layout
    fig.update_layout(
        title=f"Deposit Growth: 0% vs {return_rate}% Annual Return",
        xaxis_title="Years",
        yaxis_title="Value (CHF)",
        legend_title="Scenario",
        hovermode="x unified",
        height=500,
        # Set y-axis to start at 0
        yaxis=dict(
            range=[0, max(investment_values) * 1.1],  # Start from 0 with some padding at top
            zeroline=True,
            zerolinecolor='#ccc',
            zerolinewidth=1
        )
    )
    
    return fig 