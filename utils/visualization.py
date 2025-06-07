"""
Visualization utilities for the Kaution2Invest application.
"""

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from utils.calculations import calculate_investment_growth
from utils.i18n import get_text

def get_profile_colors(risk_profile):
    """
    Get colors for different risk profiles.
    
    Args:
        risk_profile (str): Risk profile ('conservative', 'balanced', or 'growth')
        
    Returns:
        tuple: (line_color, fill_color) for the investment return line and fill area
    """
    colors = {
        'conservative': ('#2E7D32', 'rgba(46, 125, 50, 0.1)'),  # Green
        'balanced': ('#1976D2', 'rgba(25, 118, 210, 0.1)'),     # Blue
        'growth': ('#C62828', 'rgba(198, 40, 40, 0.1)')         # Red
    }
    return colors.get(risk_profile, colors['balanced'])

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
    # Get current language and risk profile from session state
    lang = st.session_state.language if 'language' in st.session_state else 'de'
    risk_profile = st.session_state.risk_profile if 'risk_profile' in st.session_state else 'balanced'
    
    # Get colors for current risk profile
    line_color, fill_color = get_profile_colors(risk_profile)
    
    if years_range is None:
        # Extend to 20 years to make compound effect more visible
        years_range = np.arange(0, 21)
    
    # Calculate values for each year
    zero_growth_values = [deposit_amount] * len(years_range)
    investment_values = [calculate_investment_growth(deposit_amount, return_rate, year) for year in years_range]
    
    # Calculate difference values
    difference_values = [inv - zero for inv, zero in zip(investment_values, zero_growth_values)]
    
    # Create a Plotly line chart
    fig = go.Figure()
    
    # Add 0% return line (gray)
    fig.add_trace(
        go.Scatter(
            x=years_range,
            y=zero_growth_values,
            mode='lines',
            name=get_text('zero_return_name', lang),
            line=dict(color='#9E9E9E', width=2)  # Changed to gray
        )
    )
    
    # Add investment return line with markers to highlight compounding effect
    fig.add_trace(
        go.Scatter(
            x=years_range,
            y=investment_values,
            mode='lines+markers',
            name=get_text('selected_return_name', lang, rate=return_rate),
            line=dict(color=line_color, width=2),
            marker=dict(size=6, symbol='circle', color=line_color)
        )
    )
    
    # Add filled area between the lines to highlight the difference
    fig.add_trace(
        go.Scatter(
            x=years_range,
            y=investment_values,
            mode='none',
            name=get_text('potential_gain_name', lang),
            fill='tonexty',
            fillcolor=fill_color,
            showlegend=True
        )
    )
    
    # Add average rental duration in Switzerland (approx. 7 years)
    avg_rental_years = 7
    if avg_rental_years < len(years_range):
        avg_rental_value = investment_values[avg_rental_years]
        avg_rental_zero = zero_growth_values[avg_rental_years]
        avg_rental_diff = avg_rental_value - avg_rental_zero
        
        # Add vertical line at average rental duration
        fig.add_shape(
            type="line",
            x0=avg_rental_years,
            y0=0,
            x1=avg_rental_years,
            y1=avg_rental_value,
            line=dict(color="#757575", width=1, dash="dash"),  # Changed to darker gray
        )
        
        # Add annotation for average rental duration
        fig.add_annotation(
            x=avg_rental_years,
            y=avg_rental_value / 2,  # Position in the middle
            text=get_text('avg_rental_annotation', lang, gain=avg_rental_diff),
            showarrow=True,
            arrowhead=1,
            ax=50,
            ay=0,
            bordercolor="#c7c7c7",
            bgcolor="white",
            opacity=0.8
        )
    
    # Update layout
    fig.update_layout(
        title=get_text('chart_plot_title', lang, rate=return_rate),
        xaxis_title=get_text('chart_xaxis_title', lang),
        yaxis_title=get_text('chart_yaxis_title', lang),
        legend_title=get_text('chart_legend_title', lang),
        hovermode="x unified",
        height=500,
        # Set y-axis to start at deposit_amount - 1000 (but never below 0)
        yaxis=dict(
            range=[max(0, deposit_amount - 500), max(investment_values) * 1.1],
            zeroline=True,
            zerolinecolor='#ccc',
            zerolinewidth=1
        )
    )
    
    # Get text templates for hover info
    year_text = get_text('hover_year', lang).replace('{year}', '%{x}')
    value_text = get_text('hover_value', lang).replace('{value}', '%{y:.2f}')
    gain_text = get_text('hover_gain', lang).replace('{gain}', '%{customdata:.2f}')
    
    # Add hover template to show difference at each point
    fig.update_traces(
        hovertemplate=f"{year_text}<br>{value_text}<extra></extra>",
        selector=dict(name=get_text('zero_return_name', lang))
    )
    
    fig.update_traces(
        hovertemplate=f"{year_text}<br>{value_text}<br>{gain_text}<extra></extra>",
        customdata=difference_values,
        selector=dict(name=get_text('selected_return_name', lang, rate=return_rate))
    )
    
    return fig 