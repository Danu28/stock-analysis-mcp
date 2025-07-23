"""
Configuration management for Stock Analysis MCP Server.
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages configuration loading and validation."""
    
    def __init__(self, config_dir: Optional[str] = None):
        """Initialize configuration manager."""
        self.config_dir = Path(config_dir) if config_dir else Path.cwd()
        self._config = {}
        self._portfolios = {}
        self.load_all_configs()
    
    def load_all_configs(self):
        """Load all configuration files."""
        try:
            self._config = self.load_json_file("config.json")
            self._portfolios = self.load_json_file("portfolios.json")
            logger.info("Successfully loaded all configuration files")
        except Exception as e:
            logger.error(f"Failed to load configurations: {e}")
            self._set_defaults()
    
    def load_json_file(self, filename: str) -> Dict[str, Any]:
        """Load a JSON configuration file."""
        file_path = self.config_dir / filename
        if not file_path.exists():
            logger.warning(f"Configuration file {filename} not found, using defaults")
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {filename}: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")
            return {}
    
    def _set_defaults(self):
        """Set default configuration values."""
        self._config = {
            "server": {
                "name": "Stock_Analysis_MCP",
                "description": "Stock analysis and portfolio optimization",
                "version": "1.0.0"
            },
            "market": {
                "default_exchange": "NS",
                "currency": "INR"
            },
            "analysis": {
                "default_period": "1y",
                "cache_size": 32
            }
        }
        self._portfolios = {"watchlists": {}, "custom_portfolios": {}}
    
    def get_server_config(self) -> Dict[str, Any]:
        """Get server configuration."""
        return self._config.get("server", {})
    
    def get_market_config(self) -> Dict[str, Any]:
        """Get market configuration."""
        return self._config.get("market", {})
    
    def get_analysis_config(self) -> Dict[str, Any]:
        """Get analysis configuration."""
        return self._config.get("analysis", {})
    
    def get_portfolio_config(self) -> Dict[str, Any]:
        """Get portfolio configuration."""
        return self._config.get("portfolio", {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        return self._config.get("logging", {})
    
    def get_watchlist(self, name: str) -> List[str]:
        """Get a specific watchlist."""
        return self._portfolios.get("watchlists", {}).get(name, [])
    
    def get_all_watchlists(self) -> Dict[str, List[str]]:
        """Get all watchlists."""
        return self._portfolios.get("watchlists", {})
    
    def get_custom_portfolio(self, name: str) -> Dict[str, Any]:
        """Get a specific custom portfolio."""
        return self._portfolios.get("custom_portfolios", {}).get(name, {})
    
    def get_all_custom_portfolios(self) -> Dict[str, Dict[str, Any]]:
        """Get all custom portfolios."""
        return self._portfolios.get("custom_portfolios", {})
    
    def get_default_exchange(self) -> str:
        """Get default exchange suffix."""
        return self.get_market_config().get("default_exchange", "NS")
    
    def get_currency(self) -> str:
        """Get default currency."""
        return self.get_market_config().get("currency", "INR")
    
    def get_cache_size(self) -> int:
        """Get cache size for LRU caches."""
        return self.get_analysis_config().get("cache_size", 32)
    
    def get_default_period(self) -> str:
        """Get default analysis period."""
        return self.get_analysis_config().get("default_period", "1y")


# Global configuration manager instance
config_manager = ConfigManager()
