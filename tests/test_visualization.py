import sys
import os
import pytest
import plotly.graph_objects as go
import streamlit as st

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.visualization import create_growth_comparison_chart

# Set up session state for testing
if 'language' not in st.session_state:
    st.session_state.language = 'de'

def test_chart_creation():
    """Test that the chart creation function returns a valid Plotly figure."""
    deposit_amount = 5400
    return_rate = 3
    
    # Create chart
    chart = create_growth_comparison_chart(deposit_amount, return_rate)
    
    # Basic validation
    assert isinstance(chart, go.Figure)
    assert len(chart.data) >= 3  # At least 3 traces: 0% line, return% line, and area

def test_chart_data_validation():
    """Test that the chart contains the expected data series."""
    deposit_amount = 5400
    return_rate = 3
    
    # Create chart with German language
    st.session_state.language = 'de'
    chart_de = create_growth_comparison_chart(deposit_amount, return_rate)
    
    # Check that we have the right traces with German names
    trace_names_de = [trace.name for trace in chart_de.data if trace.name]
    assert any("0% Rendite" in name for name in trace_names_de)
    assert any(f"{return_rate}% Rendite" in name for name in trace_names_de)
    
    # Create chart with English language
    st.session_state.language = 'en'
    chart_en = create_growth_comparison_chart(deposit_amount, return_rate)
    
    # Check that we have the right traces with English names
    trace_names_en = [trace.name for trace in chart_en.data if trace.name]
    assert any("0% Return" in name for name in trace_names_en)
    assert any(f"{return_rate}% Return" in name for name in trace_names_en)
    
    # Reset to German for other tests
    st.session_state.language = 'de'

def test_chart_calculation():
    """Test that the chart data points are calculated correctly."""
    deposit_amount = 5400
    return_rate = 3
    
    # Create chart
    chart = create_growth_comparison_chart(deposit_amount, return_rate)
    
    # Find the trace for 0% return (should be the first one)
    zero_trace = next(trace for trace in chart.data if "0%" in trace.name)
    
    # Find the trace for selected return (should be the second one)
    return_trace = next(trace for trace in chart.data if f"{return_rate}%" in trace.name and "markers" in trace.mode)
    
    # Check initial values
    assert zero_trace.y[0] == deposit_amount
    assert return_trace.y[0] == deposit_amount
    
    # Check 5-year values
    assert zero_trace.y[5] == deposit_amount  # No change for 0%
    expected_5yr = deposit_amount * (1 + return_rate/100) ** 5
    assert abs(return_trace.y[5] - expected_5yr) < 0.01
    
    # Check that return values are always higher than 0% values
    for i in range(1, len(zero_trace.y)):
        assert return_trace.y[i] > zero_trace.y[i]

def test_chart_annotations():
    """Test that the chart has the expected annotations."""
    deposit_amount = 5400
    return_rate = 3
    
    # Create chart
    chart = create_growth_comparison_chart(deposit_amount, return_rate)
    
    # Check for average rental duration annotation (7 years)
    annotations = chart.layout.annotations
    assert annotations is not None
    assert len(annotations) > 0
    
    # At least one annotation should have text about 7 years
    assert any("7" in (ann.text or "") for ann in annotations)
    
    # Check for shapes (should have vertical line)
    shapes = chart.layout.shapes
    assert shapes is not None
    assert len(shapes) > 0
    
    # At least one shape should be a vertical line at x=7
    assert any(shape.x0 == 7 and shape.x1 == 7 for shape in shapes)

def test_chart_hover_templates():
    """Test that the chart hover templates are correctly formatted."""
    deposit_amount = 5400
    return_rate = 3
    
    # Create chart
    chart = create_growth_comparison_chart(deposit_amount, return_rate)
    
    # Get the traces
    zero_trace = next(trace for trace in chart.data if "0%" in trace.name)
    return_trace = next(trace for trace in chart.data if f"{return_rate}%" in trace.name and "markers" in trace.mode)
    
    # Check that hover templates exist
    assert hasattr(zero_trace, 'hovertemplate')
    assert hasattr(return_trace, 'hovertemplate')
    
    # Check hover template format
    assert "%{x}" in zero_trace.hovertemplate  # Should have year
    assert "%{y" in zero_trace.hovertemplate   # Should have value
    
    # Return trace should also have custom data for gain
    assert "%{customdata" in return_trace.hovertemplate
    
    # Check that gain/difference data is included
    assert hasattr(return_trace, 'customdata')
    assert len(return_trace.customdata) > 0 