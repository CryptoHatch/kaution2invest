import streamlit as st
import pandas as pd
import numpy as np
from urllib.parse import parse_qs

# Import utility functions
from utils.calculations import calculate_investment_growth, generate_growth_data
from utils.visualization import create_growth_comparison_chart
from utils.i18n import get_text

# Set page config
st.set_page_config(
    page_title="Kaution2Invest",
    page_icon="💰",
    layout="wide"
)

# URL parameter handling
def get_url_params():
    """Get and validate URL parameters."""
    params = st.query_params
    
    # Language parameter
    lang = params.get("lang")
    if lang not in ['de', 'en']:
        lang = 'de'  # Default to German
    
    # Risk profile parameter
    profile = params.get("profile")
    if profile not in ['conservative', 'balanced', 'growth']:
        profile = None
    
    # Return rate is determined by profile
    return_rate = None
    if profile == 'conservative':
        return_rate = 1
    elif profile == 'balanced':
        return_rate = 3
    elif profile == 'growth':
        return_rate = 5
    
    return lang, profile, return_rate

# Initialize session state
def init_session_state():
    """Initialize or update session state from URL parameters."""
    lang, profile, return_rate = get_url_params()
    
    # Initialize language
    if 'language' not in st.session_state:
        st.session_state.language = lang
    
    # Initialize risk profile
    if 'risk_profile' not in st.session_state:
        st.session_state.risk_profile = profile or 'balanced'  # Default to balanced
    
    # Initialize return rate based on profile or URL parameter
    if 'return_rate' not in st.session_state:
        if return_rate is not None:
            st.session_state.return_rate = return_rate
        elif profile == 'conservative':
            st.session_state.return_rate = 1
        elif profile == 'growth':
            st.session_state.return_rate = 5
        else:  # balanced or None
            st.session_state.return_rate = 3

# Initialize session state
init_session_state()

# Function to change language
def change_language():
    st.session_state.language = st.session_state.lang_selection
    st.query_params["lang"] = st.session_state.language

# Function to change risk profile
def change_risk_profile():
    """Update risk profile and associated return rate."""
    profile = st.session_state.risk_profile_selection
    st.session_state.risk_profile = profile
    
    # Set return rate based on profile
    if profile == 'conservative':
        st.session_state.return_rate = 1
    elif profile == 'balanced':
        st.session_state.return_rate = 3
    elif profile == 'growth':
        st.session_state.return_rate = 5
    
    # Update URL parameters
    st.query_params["profile"] = profile
    st.query_params["return"] = str(st.session_state.return_rate)

# Current language
lang = st.session_state.language

# App title and description
title_col, lang_col = st.columns([4, 1])
with title_col:
    st.title(get_text('app_title', lang))
with lang_col:
    st.selectbox(
        "",
        options=['de', 'en'],
        format_func=lambda x: get_text(f'language_{x}', lang),
        index=0 if lang == 'de' else 1,
        key='lang_selection',
        on_change=change_language,
        label_visibility="collapsed"
    )

st.markdown(get_text('app_description', lang))

# User input section
st.subheader(get_text('input_section_title', lang))

# Risk profile and return rate selection
col1, col2, col3 = st.columns(3)

with col1:
    st.selectbox(
        get_text('risk_profile_label', lang),
        options=['conservative', 'balanced', 'growth'],
        format_func=lambda x: get_text(f'risk_profile_{x}', lang),
        index=['conservative', 'balanced', 'growth'].index(st.session_state.risk_profile),
        key='risk_profile_selection',
        on_change=change_risk_profile,
        help=get_text('risk_profile_help', lang)
    )

with col2:
    rent_amount = st.number_input(
        get_text('rent_amount_label', lang),
        min_value=0,
        value=1800,
        step=100,
        help=get_text('rent_amount_help', lang)
    )

with col3:
    deposit_months = st.number_input(
        get_text('deposit_months_label', lang),
        min_value=0,
        value=3,
        step=1,
        help=get_text('deposit_months_help', lang)
    )

# Calculate the initial deposit amount
deposit_amount = rent_amount * deposit_months

# Display the initial deposit amount
st.markdown(f"**{get_text('total_deposit_amount', lang, amount=deposit_amount)}**")

# Add explanation about compound interest in a collapsible section
with st.expander(get_text('compound_interest_title', lang)):
    st.markdown(get_text('compound_interest_text', lang))

# Time horizons for calculation
time_horizons = [1, 5, 10, 15, 20]  # years - added 20 years

# Use return rate from session state (set by risk profile)
return_rate = st.session_state.return_rate

# Generate growth data
results = generate_growth_data(deposit_amount, return_rate, time_horizons)

# Translate column headers for the dataframe
results_df = pd.DataFrame(results)
results_df = results_df.rename(columns={
    "Years": get_text('years_column', lang),
    "0% Return (CHF)": get_text('zero_return_column', lang),
    f"{return_rate}% Return (CHF)": get_text('selected_return_column', lang, rate=return_rate),
    "Difference (CHF)": get_text('difference_column', lang),
    "Growth (%)": get_text('growth_column', lang)
})

# Define a styling function for the dataframe
def highlight_columns(df):
    # Create a style object
    styled = df.style.format({
        get_text('zero_return_column', lang): "{:,.2f}",
        get_text('selected_return_column', lang, rate=return_rate): "{:,.2f}",
        get_text('difference_column', lang): "{:,.2f}",
        get_text('growth_column', lang): "{:.2f}%"
    })
    
    # Apply background colors to specific columns
    # Light red for 0% return column
    styled = styled.set_properties(
        subset=[get_text('zero_return_column', lang)],
        **{'background-color': '#ffebee', 'color': '#000000'}  # Very light red with black text
    )
    
    # Light blue for return rate column
    styled = styled.set_properties(
        subset=[get_text('selected_return_column', lang, rate=return_rate)],
        **{'background-color': '#e3f2fd', 'color': '#000000'}  # Very light blue with black text
    )
    
    return styled

# Display the results table with styling
st.subheader(get_text('results_title', lang))
st.dataframe(
    highlight_columns(results_df),
    use_container_width=True
)

# Create visualization
st.subheader(get_text('chart_title', lang))

# Pass language parameter to chart creation function
# Note: We'll need to update the visualization.py file later to support internationalization
chart = create_growth_comparison_chart(deposit_amount, return_rate)
st.plotly_chart(chart, use_container_width=True)

# Add collapsible explanation section
with st.expander(get_text('explanation_title', lang)):
    st.markdown(get_text('explanation_subtitle', lang))
    st.markdown(get_text('explanation_text', lang))

# Add a footer
st.markdown("---")
st.markdown(get_text('footer_text', lang)) 