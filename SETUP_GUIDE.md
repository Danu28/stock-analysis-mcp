# Stock Analysis MCP Server - Quick Setup Guide

## 📦 Installation & Setup

### 1. Install the Package
```bash
# Clone the repository
git clone <your-repo-url>
cd stock-analysis-mcp

# Install in development mode
pip install -e .[dev]
```

### 2. Configuration Files

The server uses JSON configuration files for easy customization:

#### `config.json` - Server & Analysis Settings
```json
{
  "server": {
    "name": "Stock_Analysis_MCP",
    "description": "Stock analysis and portfolio optimization for NSE/BSE markets"
  },
  "market": {
    "default_exchange": "NS",  // NS for NSE, BO for BSE
    "currency": "INR"
  },
  "analysis": {
    "default_period": "1y",
    "cache_size": 32
  }
}
```

#### `portfolios.json` - Predefined Watchlists & Portfolios
```json
{
  "watchlists": {
    "nifty50": ["RELIANCE", "TCS", "HDFCBANK", ...],
    "banknifty": ["HDFCBANK", "ICICIBANK", "SBIN", ...]
  },
  "custom_portfolios": {
    "conservative": {
      "description": "Low risk portfolio",
      "stocks": ["HDFCBANK", "TCS", "RELIANCE"],
      "target_allocation": "optimized"
    }
  }
}
```

### 3. MCP Client Configuration

#### For Claude Desktop (claude_desktop_config.json)
```json
{
  "mcpServers": {
    "stock-analysis": {
      "command": "python",
      "args": ["-m", "main"],
      "cwd": "/path/to/stock-analysis-mcp"
    }
  }
}
```

#### For Other MCP Clients
```json
{
  "name": "stock-analysis-mcp",
  "mcpServers": {
    "stock-analysis": {
      "command": "python",
      "args": ["-m", "main"],
      "cwd": ".",
      "env": {}
    }
  }
}
```

## 🚀 Usage Examples

### Basic Stock Operations
```python
# Get current stock price
get_stock_price("RELIANCE")

# Get historical data
get_stock_history("TCS", "3mo")

# Compare two stocks
compare_stocks("RELIANCE", "TCS")
```

### Portfolio Analysis
```python
# Analyze custom portfolio
analyze_portfolio(["RELIANCE", "TCS", "HDFCBANK", "INFY"])

# Use predefined portfolio
analyze_predefined_portfolio("conservative")

# Get watchlist
get_watchlist("nifty50")
```

### Technical Analysis
```python
# Technical analysis for multiple stocks
technical_analysis(["RELIANCE", "TCS"], "3mo")

# Compare stocks with technical prompt
compare_stocks_prompt("RELIANCE", "TCS")
```

### Server Information
```python
# Get server capabilities and configuration
get_server_info()

# List available watchlists
list_available_watchlists()
```

## 🛠️ Customization

### Adding Your Own Watchlists
Edit `portfolios.json`:
```json
{
  "watchlists": {
    "my_stocks": ["STOCK1", "STOCK2", "STOCK3"],
    "tech_favorites": ["TCS", "INFY", "WIPRO"]
  }
}
```

### Creating Custom Portfolios
```json
{
  "custom_portfolios": {
    "my_portfolio": {
      "description": "My investment strategy",
      "stocks": ["RELIANCE", "TCS", "HDFCBANK"],
      "target_allocation": {
        "RELIANCE": 0.4,
        "TCS": 0.35,
        "HDFCBANK": 0.25
      }
    }
  }
}
```

### Changing Market Settings
In `config.json`:
```json
{
  "market": {
    "default_exchange": "BO",  // Change to BSE
    "currency": "INR",
    "timezone": "Asia/Kolkata"
  }
}
```

## 🔧 Advanced Configuration

### Logging Configuration
```json
{
  "logging": {
    "level": "DEBUG",  // DEBUG, INFO, WARNING, ERROR
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "stock_analysis.log"  // Optional log file
  }
}
```

### Analysis Settings
```json
{
  "analysis": {
    "default_period": "1y",
    "cache_size": 64,  // Increase for better performance
    "historical_periods": ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y"],
    "technical_analysis_period": "3mo"
  },
  "portfolio": {
    "optimization_method": "sharpe_ratio",
    "min_weight_threshold": 0.01,
    "max_positions": 10
  }
}
```

## 🤝 Integration with MCP Clients

### Claude Desktop
1. Add the configuration to your Claude Desktop config
2. Restart Claude Desktop
3. Use natural language: "Analyze RELIANCE stock" or "Optimize my portfolio with TCS, RELIANCE, and HDFC Bank"

### Custom MCP Client
```python
import mcp

# Connect to the server
client = mcp.Client()
client.connect("stock-analysis")

# Use the tools
result = client.call_tool("get_stock_price", {"symbol": "RELIANCE"})
print(result)
```

## 📈 Example Workflows

### Portfolio Optimization Workflow
1. `get_watchlist("nifty50")` - Get stocks
2. `analyze_portfolio(stocks)` - Optimize allocation
3. `technical_analysis(top_stocks)` - Technical insights

### Stock Research Workflow
1. `get_stock_price("RELIANCE")` - Current price
2. `get_stock_history("RELIANCE", "6mo")` - Historical data
3. `compare_stocks_prompt("RELIANCE", "TCS")` - Comparison analysis

## 💡 Tips

- **Performance**: Increase `cache_size` for better performance with repeated queries
- **Exchanges**: Use `.NS` suffix for NSE stocks, `.BO` for BSE stocks
- **Periods**: Valid periods are "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
- **Portfolios**: Use "optimized" for Sharpe ratio optimization, or specify custom weights

## 🐛 Troubleshooting

### Common Issues
1. **Import Error**: Make sure you installed with `pip install -e .[dev]`
2. **No Data**: Check if stock symbol is correct and includes exchange suffix
3. **Configuration**: Verify JSON files are valid (use JSON validators)
4. **MCP Connection**: Ensure the path in MCP config points to the correct directory
