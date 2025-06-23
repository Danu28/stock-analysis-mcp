"""
Basic tests for stock analysis functionality.
"""

import pytest
from unittest.mock import patch, MagicMock


def test_normalize_symbol():
    """Test that stock symbols are properly normalized."""
    from main import normalize_symbol

    # Test cases
    assert normalize_symbol("RELIANCE") == "RELIANCE.NS"
    assert normalize_symbol("RELIANCE.NS") == "RELIANCE.NS"
    assert normalize_symbol("RELIANCE.BO") == "RELIANCE.BO"


def test_normalize_symbols():
    """Test that lists of stock symbols are properly normalized."""
    from main import normalize_symbols

    symbols = ["RELIANCE", "TCS", "INFY.NS"]
    expected = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

    assert normalize_symbols(symbols) == expected


@patch("main.get_ticker")
def test_get_stock_price_success(mock_get_ticker):
    """Test successful stock price retrieval."""
    from main import get_stock_price

    # Create mock ticker with history data
    mock_ticker = MagicMock()
    mock_history = MagicMock()
    mock_history.__getitem__.return_value = MagicMock()
    mock_history.__getitem__.return_value.iloc = [-1]
    mock_history.empty = False
    mock_ticker.history.return_value = mock_history
    mock_ticker.info = {"currency": "INR"}

    # Set up the mock
    mock_get_ticker.return_value = mock_ticker

    # Test the function
    result = get_stock_price("RELIANCE")

    # Verify expected behavior
    assert result["status"] == "success"
    assert result["symbol"] == "RELIANCE"
    assert "price" in result
    assert "timestamp" in result
    assert result["currency"] == "INR"


@patch("main.get_ticker")
def test_get_stock_price_failure(mock_get_ticker):
    """Test stock price retrieval with an exception."""
    from main import get_stock_price

    # Set up the mock to raise an exception
    mock_get_ticker.side_effect = Exception("Test exception")

    # Test the function
    result = get_stock_price("INVALID")

    # Verify expected behavior
    assert result["status"] == "error"
    assert "message" in result
    assert "Test exception" in result["message"]
