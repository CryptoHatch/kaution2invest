"""
Tests for URL parameter handling in the Kaution2Invest application.
"""

import pytest
from app import get_url_params
import streamlit as st

def test_valid_url_params(monkeypatch):
    """Test handling of valid URL parameters."""
    # Mock query parameters
    mock_params = {
        "lang": "de",
        "profile": "conservative",
        "return": "1"
    }
    monkeypatch.setattr(st, "query_params", mock_params)
    
    # Get and validate parameters
    lang, profile, return_rate = get_url_params()
    
    assert lang == "de"
    assert profile == "conservative"
    assert return_rate == 1

def test_invalid_url_params(monkeypatch):
    """Test handling of invalid URL parameters."""
    # Mock invalid query parameters
    mock_params = {
        "lang": "invalid",
        "profile": "invalid",
        "return": "invalid"
    }
    monkeypatch.setattr(st, "query_params", mock_params)
    
    # Get and validate parameters
    lang, profile, return_rate = get_url_params()
    
    # Should fall back to defaults
    assert lang == "de"
    assert profile is None
    assert return_rate is None

def test_missing_url_params(monkeypatch):
    """Test handling of missing URL parameters."""
    # Mock empty query parameters
    mock_params = {}
    monkeypatch.setattr(st, "query_params", mock_params)
    
    # Get and validate parameters
    lang, profile, return_rate = get_url_params()
    
    # Should fall back to defaults
    assert lang == "de"
    assert profile is None
    assert return_rate is None

def test_partial_url_params(monkeypatch):
    """Test handling of partial URL parameters."""
    # Mock partial query parameters
    mock_params = {
        "lang": "en",
        "profile": "growth"
        # return_rate is missing
    }
    monkeypatch.setattr(st, "query_params", mock_params)
    
    # Get and validate parameters
    lang, profile, return_rate = get_url_params()
    
    assert lang == "en"
    assert profile == "growth"
    assert return_rate is None

def test_valid_return_rates(monkeypatch):
    """Test handling of different valid return rates."""
    valid_returns = ["1", "3", "5"]
    
    for rate in valid_returns:
        mock_params = {"return": rate}
        monkeypatch.setattr(st, "query_params", mock_params)
        
        # Get and validate parameters
        _, _, return_rate = get_url_params()
        assert return_rate == int(rate)

def test_invalid_return_rates(monkeypatch):
    """Test handling of invalid return rates."""
    invalid_returns = ["0", "2", "4", "6", "abc", "-1"]
    
    for rate in invalid_returns:
        mock_params = {"return": rate}
        monkeypatch.setattr(st, "query_params", mock_params)
        
        # Get and validate parameters
        _, _, return_rate = get_url_params()
        assert return_rate is None 