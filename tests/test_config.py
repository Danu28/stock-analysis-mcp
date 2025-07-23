"""
Comprehensive tests for the new configuration-based MCP server.
"""

import pytest
from unittest.mock import patch, MagicMock


def test_config_manager_import():
    """Test that config manager can be imported."""
    from config_manager import config_manager
    assert config_manager is not None


def test_config_manager_basic_functions():
    """Test basic config manager functionality."""
    from config_manager import config_manager
    
    # Test server config
    server_config = config_manager.get_server_config()
    assert isinstance(server_config, dict)
    
    # Test market config
    market_config = config_manager.get_market_config()
    assert isinstance(market_config, dict)
    
    # Test default exchange
    exchange = config_manager.get_default_exchange()
    assert exchange in ["NS", "BO"]
    
    # Test currency
    currency = config_manager.get_currency()
    assert currency == "INR"


def test_watchlists():
    """Test watchlist functionality."""
    from config_manager import config_manager
    
    # Test getting all watchlists
    watchlists = config_manager.get_all_watchlists()
    assert isinstance(watchlists, dict)
    assert len(watchlists) > 0
    
    # Test specific watchlist
    if "nifty50" in watchlists:
        nifty50 = config_manager.get_watchlist("nifty50")
        assert isinstance(nifty50, list)
        assert len(nifty50) > 0
        assert "RELIANCE" in nifty50


def test_custom_portfolios():
    """Test custom portfolio functionality."""
    from config_manager import config_manager
    
    # Test getting all portfolios
    portfolios = config_manager.get_all_custom_portfolios()
    assert isinstance(portfolios, dict)
    
    # Test specific portfolio if it exists
    if "conservative" in portfolios:
        conservative = config_manager.get_custom_portfolio("conservative")
        assert isinstance(conservative, dict)
        assert "stocks" in conservative


def test_normalize_symbol_with_config():
    """Test that symbol normalization uses config."""
    from main import normalize_symbol
    
    # Test normalization
    result = normalize_symbol("RELIANCE")
    assert result == "RELIANCE.NS"  # Should use default NS from config
    
    # Test already normalized symbols
    result = normalize_symbol("RELIANCE.BO")
    assert result == "RELIANCE.BO"


def test_new_mcp_tools_import():
    """Test that new MCP tools can be imported."""
    from main import (
        get_watchlist, list_available_watchlists, 
        get_custom_portfolio, get_server_info
    )
    
    # Just test that they can be imported
    assert callable(get_watchlist)
    assert callable(list_available_watchlists)
    assert callable(get_custom_portfolio)
    assert callable(get_server_info)


def test_get_server_info():
    """Test the get_server_info function."""
    from main import get_server_info
    
    result = get_server_info()
    assert result["status"] == "success"
    assert "server" in result
    assert "market" in result
    assert "capabilities" in result


def test_list_available_watchlists():
    """Test listing available watchlists."""
    from main import list_available_watchlists
    
    result = list_available_watchlists()
    assert result["status"] == "success"
    assert "watchlists" in result
    assert isinstance(result["watchlists"], dict)


def test_get_watchlist_function():
    """Test getting a specific watchlist."""
    from main import get_watchlist
    
    # Test with a watchlist that should exist
    result = get_watchlist("nifty50")
    if result["status"] == "success":
        assert "stocks" in result
        assert isinstance(result["stocks"], list)
        assert result["count"] > 0
    
    # Test with non-existent watchlist
    result = get_watchlist("nonexistent")
    assert result["status"] == "error"


def test_get_custom_portfolio_function():
    """Test getting a custom portfolio."""
    from main import get_custom_portfolio
    
    # Test with portfolio that should exist
    result = get_custom_portfolio("conservative")
    if result["status"] == "success":
        assert "stocks" in result
        assert isinstance(result["stocks"], list)
    
    # Test with non-existent portfolio
    result = get_custom_portfolio("nonexistent")
    assert result["status"] == "error"


def test_main_module_imports():
    """Test that main module imports correctly with config."""
    import main
    
    # Test that the module loaded
    assert hasattr(main, 'mcp')
    assert hasattr(main, 'config_manager')
    
    # Test that config manager is accessible
    assert main.config_manager is not None


if __name__ == "__main__":
    # Run tests manually
    print("🧪 Running comprehensive tests...\n")
    
    test_functions = [
        test_config_manager_import,
        test_config_manager_basic_functions,
        test_watchlists,
        test_custom_portfolios,
        test_normalize_symbol_with_config,
        test_new_mcp_tools_import,
        test_get_server_info,
        test_list_available_watchlists,
        test_get_watchlist_function,
        test_get_custom_portfolio_function,
        test_main_module_imports
    ]
    
    passed = 0
    for test_func in test_functions:
        try:
            test_func()
            print(f"✅ {test_func.__name__}")
            passed += 1
        except Exception as e:
            print(f"❌ {test_func.__name__}: {e}")
    
    print(f"\n📊 Results: {passed}/{len(test_functions)} tests passed")
