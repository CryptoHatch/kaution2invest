# Kaution2Invest Technology Stack

The Kaution2Invest application leverages the following technology stack to create a clean, interactive, and user-friendly financial visualization tool:

## Core Framework

- **Streamlit** (v1.45.1+): The primary framework that powers our web application, providing interactive widgets, layouts, and data visualization capabilities with minimal boilerplate code.

## Data Processing & Analysis

- **NumPy** (v2.2.6+): Used for numerical operations, especially in our compound interest calculations and data array manipulations.
- **Pandas** (v2.2.3+): Powers our data handling, formatting, and the styled data tables that show investment comparisons.

## Visualization

- **Plotly** (v6.1.2+): Creates our interactive charts with hover effects, annotations, and filled areas that highlight investment differences.
- **Matplotlib** (v3.10.3+): Provides underlying plotting capabilities used by some components.

## UI Components & Features

- **Streamlit Widgets**:
  - Number inputs with validation for rent and deposit duration
  - Selectbox for choosing investment return rates
  - Expanders for collapsible information sections
  - Styled dataframes with custom colors
  - Multi-column layouts for organized input forms

- **Plotly Features**:
  - Custom hover templates showing gain values
  - Filled areas to highlight the difference between scenarios
  - Markers on lines to emphasize data points
  - Vertical reference lines for average rental duration
  - Annotations with contextual information
  - Custom styling for consistent branding (colors, line styles)

## Code Organization

- **Modular Architecture**:
  - Calculation logic in separate utility modules
  - Visualization functions abstracted into dedicated modules
  - Clean separation of concerns between data processing and UI

- **Project Structure**:
  - `/utils`: Contains reusable calculation and visualization functions
  - `/tests`: Houses unit tests for core functions
  - Root directory: Main application and configuration files

## Documentation

- **Comprehensive Docstrings**: Python docstrings documenting function parameters, returns, and behaviors
- **Markdown Documentation**: Supporting documentation for ETF requirements and examples
- **In-App Explanations**: Collapsible sections that explain financial concepts

## Development & Testing

- **pytest**: Testing framework for unit tests
- **Python Type Hints**: Some functions use type hints for better code clarity
- **Virtual Environment**: Isolated dependencies for consistent development

## Design Principles

- **Clean UI**: Minimalist interface with expandable sections for detailed information
- **Color-Coding**: Consistent use of red for 0% returns and blue for investment returns
- **Responsive Layout**: Tables and charts that adjust to viewport size
- **Informative Visualizations**: Charts designed to highlight the key comparison points
- **Swiss Context**: Content tailored to Swiss rental and investment contexts

## Deployment Options

- Local development server
- Potential for cloud deployment on Streamlit Cloud, Heroku, or other Python-compatible hosting

This stack provides a balance of simplicity, interactivity, and powerful visualization capabilities, allowing us to create a professional financial tool with relatively concise code. 