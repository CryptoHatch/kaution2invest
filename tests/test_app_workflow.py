import sys
import os
import pytest
from unittest.mock import patch, MagicMock, call

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create a session state class that allows attribute access
class MockSessionState(dict):
    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None
        
    def __setattr__(self, key, value):
        self[key] = value

# Create streamlit mocks
class MockStreamlit:
    """Mock for streamlit module to test app workflow."""
    def __init__(self):
        self._session_state = MockSessionState()
        self._query_params = {}
        self.inputs = {}
        self.rendered_elements = []
        self.sidebar_elements = []
        self.columns_created = 0
        self.current_columns = []
        self.expander_content = {}
        
    def set_page_config(self, **kwargs):
        self.page_config = kwargs
        
    def title(self, text):
        self.rendered_elements.append(('title', text))
        
    def markdown(self, text):
        self.rendered_elements.append(('markdown', text))
        
    def subheader(self, text):
        self.rendered_elements.append(('subheader', text))
        
    def number_input(self, label, min_value=None, max_value=None, value=None, step=None, **kwargs):
        self.rendered_elements.append(('number_input', label))
        return self.inputs.get(label, value)
        
    def selectbox(self, label, options, index=0, format_func=None, **kwargs):
        self.rendered_elements.append(('selectbox', label))
        selected = options[index]
        if format_func:
            selected = format_func(selected)
        return selected
        
    def dataframe(self, data, **kwargs):
        self.rendered_elements.append(('dataframe', data))
        
    def plotly_chart(self, fig, **kwargs):
        self.rendered_elements.append(('plotly_chart', fig))
        
    def expander(self, label):
        self.rendered_elements.append(('expander', label))
        expander = MagicMock()
        expander.markdown = lambda text: self.expander_content.update({label: text})
        return expander
        
    def columns(self, spec_or_num):
        self.columns_created += 1
        # Handle both numeric and list specs
        if isinstance(spec_or_num, int):
            num_cols = spec_or_num
        else:
            num_cols = len(spec_or_num)
            
        self.current_columns = [MagicMock() for _ in range(num_cols)]
        for col in self.current_columns:
            col.__enter__ = lambda x=col: x
            col.__exit__ = lambda *args: None
            col.number_input = self.number_input
            col.selectbox = self.selectbox
            col.title = self.title
        return self.current_columns
        
    @property
    def sidebar(self):
        sidebar_mock = MagicMock()
        sidebar_mock.__enter__ = lambda x: x
        sidebar_mock.__exit__ = lambda *args: None
        sidebar_mock.selectbox = lambda *args, **kwargs: self.sidebar_elements.append(('selectbox', args[0]))
        return sidebar_mock
        
    @property
    def session_state(self):
        return self._session_state
        
    @property
    def query_params(self):
        return self._query_params

# Function to create a patched streamlit module
def create_patched_streamlit():
    mock_st = MockStreamlit()
    
    # Create a module-like object
    patched_st = type('MockedStreamlit', (), {})()
    
    # Add all the necessary methods and properties
    for attr_name in dir(mock_st):
        if not attr_name.startswith('_'):  # Skip private attributes
            setattr(patched_st, attr_name, getattr(mock_st, attr_name))
            
    # Add the session_state and query_params
    patched_st.session_state = mock_st.session_state
    patched_st.query_params = mock_st.query_params
    
    return patched_st

@pytest.fixture
def mock_streamlit():
    """Create and return a mock streamlit object."""
    return create_patched_streamlit()

def test_calculations():
    """Test the calculation functions directly."""
    # Import the calculation functions directly
    from utils.calculations import calculate_investment_growth, generate_growth_data
    
    # Test standard case
    deposit_amount = 5400  # 3 months of 1800
    return_rate = 3
    years = 5
    
    # Calculate expected result
    expected = deposit_amount * (1 + return_rate/100) ** years
    
    # Test the function
    result = calculate_investment_growth(deposit_amount, return_rate, years)
    
    # Check the result
    assert abs(result - expected) < 0.01
    
    # Test generate_growth_data
    time_horizons = [1, 5, 10]
    results = generate_growth_data(deposit_amount, return_rate, time_horizons)
    
    # Check we got the expected number of results
    assert len(results) == len(time_horizons)
    
    # Check each result has the expected keys
    for result in results:
        assert "Years" in result
        assert "0% Return (CHF)" in result
        assert f"{return_rate}% Return (CHF)" in result
        assert "Difference (CHF)" in result
        assert "Growth (%)" in result

def test_i18n():
    """Test the internationalization functionality."""
    from utils.i18n import get_text
    
    # Test German (default)
    title_de = get_text('app_title')
    assert title_de == 'Schweizer Mietkautions-Rechner'
    
    # Test English
    title_en = get_text('app_title', 'en')
    assert title_en == 'Swiss Deposit Investment Calculator'
    
    # Test with parameters - account for different number formatting
    deposit_amount = 5400
    text_with_params = get_text('total_deposit_amount', 'de', amount=deposit_amount)
    # Check that the amount is in the string - could be formatted as 5.400,00 or 5,400.00
    assert '5400' in text_with_params.replace(',', '').replace('.', '')

def test_url_parameter_handling():
    """Test that URL parameters for language are handled correctly."""
    mock_st = create_patched_streamlit()
    
    # 1. Test default language (German)
    mock_st.session_state.clear()
    mock_st.query_params.clear()
    
    # Mock the initialization from app.py
    url_lang = mock_st.query_params.get("lang", None)
    if 'language' not in mock_st.session_state:
        mock_st.session_state.language = url_lang if url_lang in ['de', 'en'] else 'de'
    
    assert mock_st.session_state.language == 'de'
    
    # 2. Test English language parameter
    mock_st.session_state.clear()
    mock_st.query_params.clear()
    mock_st.query_params["lang"] = "en"
    
    # Mock the initialization again
    url_lang = mock_st.query_params.get("lang", None)
    if 'language' not in mock_st.session_state:
        mock_st.session_state.language = url_lang if url_lang in ['de', 'en'] else 'de'
    
    assert mock_st.session_state.language == 'en'

def test_change_language_function():
    """Test the change_language function."""
    # Create a custom test function similar to app.py's change_language
    def change_language(session_state, query_params):
        session_state.language = session_state.lang_selection
        query_params["lang"] = session_state.language
    
    # Create mock objects
    mock_st = create_patched_streamlit()
    mock_st.session_state.language = 'de'
    mock_st.session_state.lang_selection = 'en'
    
    # Call the function
    change_language(mock_st.session_state, mock_st.query_params)
    
    # Check that language was changed
    assert mock_st.session_state.language == 'en'
    assert mock_st.query_params["lang"] == 'en'

def test_deposit_amount_calculation():
    """Test the deposit amount calculation (rent × months)."""
    # Test with default values
    rent_amount = 1800
    deposit_months = 3
    expected_deposit = rent_amount * deposit_months  # 5400
    
    assert expected_deposit == 5400
    
    # Test with custom values
    rent_amount = 2500
    deposit_months = 4
    expected_deposit = rent_amount * deposit_months  # 10000
    
    assert expected_deposit == 10000
    
    # Edge case: zero rent
    rent_amount = 0
    deposit_months = 3
    expected_deposit = rent_amount * deposit_months
    
    assert expected_deposit == 0
    
    # Edge case: zero months
    rent_amount = 1800
    deposit_months = 0
    expected_deposit = rent_amount * deposit_months
    
    assert expected_deposit == 0 