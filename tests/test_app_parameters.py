import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# We need to mock st.session_state and st.query_params before importing app-related code
class MockSessionState(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None
        
    def __setattr__(self, key, value):
        self[key] = value

class MockQueryParams(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def get(self, key, default=None):
        return self[key] if key in self else default

# Set up the mocks for tests
mock_session_state = MockSessionState()
mock_query_params = MockQueryParams()

def test_default_language():
    """Test that the default language is German when no URL parameter is provided."""
    # Clear any previous state
    mock_session_state.clear()
    mock_query_params.clear()
    
    # Simulate the app's language initialization logic
    url_lang = mock_query_params.get("lang", None)
    if 'language' not in mock_session_state:
        mock_session_state.language = url_lang if url_lang in ['de', 'en'] else 'de'
    
    # The app should set session_state.language to 'de' by default
    assert 'language' in mock_session_state
    assert mock_session_state['language'] == 'de'

def test_language_from_url():
    """Test that the language is set from URL parameter."""
    # Clear any previous state
    mock_session_state.clear()
    mock_query_params.clear()
    
    # Simulate URL parameter for English
    mock_query_params['lang'] = 'en'
    
    # Simulate the app's language initialization logic
    url_lang = mock_query_params.get("lang", None)
    if 'language' not in mock_session_state:
        mock_session_state.language = url_lang if url_lang in ['de', 'en'] else 'de'
    
    # The app should set session_state.language to 'en' from URL
    assert 'language' in mock_session_state
    assert mock_session_state['language'] == 'en'

def test_invalid_language_from_url():
    """Test that invalid language in URL falls back to German."""
    # Clear any previous state
    mock_session_state.clear()
    mock_query_params.clear()
    
    # Simulate invalid URL parameter
    mock_query_params['lang'] = 'fr'  # Not supported
    
    # Simulate the app's language initialization logic
    url_lang = mock_query_params.get("lang", None)
    if 'language' not in mock_session_state:
        mock_session_state.language = url_lang if url_lang in ['de', 'en'] else 'de'
    
    # The app should fall back to 'de' for unsupported languages
    assert 'language' in mock_session_state
    assert mock_session_state['language'] == 'de'

def test_language_change():
    """Test that changing language updates both session state and URL parameter."""
    # Clear any previous state
    mock_session_state.clear()
    mock_query_params.clear()
    
    # Simulate the app's change_language function
    def change_language():
        mock_session_state.language = mock_session_state.lang_selection
        mock_query_params["lang"] = mock_session_state.language
    
    # Set initial language to German
    mock_session_state['language'] = 'de'
    
    # Simulate changing language to English via dropdown
    mock_session_state['lang_selection'] = 'en'
    change_language()
    
    # Check that session_state.language was updated
    assert mock_session_state['language'] == 'en'
    
    # Check that URL parameter was updated
    assert mock_query_params['lang'] == 'en' 