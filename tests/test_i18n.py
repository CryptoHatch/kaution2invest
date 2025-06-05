import sys
import os
import pytest

# Add parent directory to path to import from app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.i18n import get_text, TEXT

def test_get_text_basic():
    """Test basic text retrieval with default language (German)."""
    # Test app title
    german_title = get_text('app_title')
    assert german_title == 'Schweizer Mietkautions-Rechner'
    
    # Test with English explicitly specified
    english_title = get_text('app_title', 'en')
    assert english_title == 'Swiss Deposit Investment Calculator'

def test_get_text_with_parameters():
    """Test text retrieval with format parameters."""
    # Test with parameters
    deposit_amount = 5400
    deposit_text_de = get_text('total_deposit_amount', 'de', amount=deposit_amount)
    assert 'Gesamtbetrag der Kaution: 5.400,00 CHF' in deposit_text_de or 'Gesamtbetrag der Kaution: 5,400.00 CHF' in deposit_text_de
    
    deposit_text_en = get_text('total_deposit_amount', 'en', amount=deposit_amount)
    assert 'Total Deposit Amount: 5,400.00 CHF' in deposit_text_en

def test_get_text_missing_key():
    """Test behavior with missing key."""
    # Test with non-existent key
    missing_key_text = get_text('non_existent_key')
    assert missing_key_text == 'Missing translation: non_existent_key'

def test_get_text_missing_language():
    """Test behavior with missing language (should fall back to German)."""
    # Test with non-existent language
    title_with_invalid_lang = get_text('app_title', 'fr')  # French not supported
    assert title_with_invalid_lang == 'Schweizer Mietkautions-Rechner'  # Should fall back to German

def test_text_dictionary_consistency():
    """Test that all keys have both German and English translations."""
    for key, translations in TEXT.items():
        assert 'de' in translations, f"Missing German translation for '{key}'"
        assert 'en' in translations, f"Missing English translation for '{key}'"

def test_chart_translations():
    """Test that chart-related text translations exist."""
    chart_keys = [
        'chart_title', 'chart_plot_title', 'chart_xaxis_title', 
        'chart_yaxis_title', 'chart_legend_title', 'zero_return_name', 
        'selected_return_name', 'potential_gain_name'
    ]
    
    for key in chart_keys:
        assert key in TEXT, f"Missing chart translation key: {key}"
        assert 'de' in TEXT[key], f"Missing German translation for chart key: {key}"
        assert 'en' in TEXT[key], f"Missing English translation for chart key: {key}"

def test_rate_parameter_formatting():
    """Test that text with rate parameter formats correctly."""
    # Test with rate parameter
    rate = 3
    selected_return_de = get_text('selected_return_column', 'de', rate=rate)
    assert f"{rate}% Rendite (CHF)" == selected_return_de
    
    selected_return_en = get_text('selected_return_column', 'en', rate=rate)
    assert f"{rate}% Return (CHF)" == selected_return_en 