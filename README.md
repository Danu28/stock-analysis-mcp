# Stock Analysis MCP Server

A comprehensive **Model Context Protocol (MCP) server** for stock analysis, portfolio optimization, and technical analysis focused on Indian stock markets (NSE/BSE). Built with configurable JSON files for easy customization and deployment.

## 🚀 Features

- **📊 Portfolio Optimization**: Modern Portfolio Theory with Sharpe ratio optimization
- **💰 Real-time Stock Prices**: Current prices for NSE/BSE listed companies  
- **📈 Historical Data Analysis**: Fetch and analyze historical stock data
- **🔍 Technical Analysis**: Generate detailed technical analysis reports
- **📋 Predefined Watchlists**: Nifty50, BankNifty, IT stocks, Pharma stocks, and more
- **⚙️ JSON Configuration**: Easy customization via config files
- **🤖 MCP Integration**: Seamless integration with AI assistants like Claude
- **🔄 Caching**: LRU caching for improved performance

## 📦 Quick Start

### Installation
```bash
git clone <your-repo-url>
cd stock-analysis-mcp
pip install -e .[dev]
```

### MCP Client Setup (Claude Desktop)
Add to your `claude_desktop_config.json`:
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

### Basic Usage
```python
# Get stock price
get_stock_price("RELIANCE")

# Analyze portfolio  
analyze_portfolio(["RELIANCE", "TCS", "HDFCBANK"])

# Use predefined watchlist
get_watchlist("nifty50")

# Technical analysis
technical_analysis(["RELIANCE", "TCS"], "3mo")
```

## ⚙️ Configuration

The server uses JSON files for easy configuration:

### `config.json` - Server Settings
```json
{
  "server": {
    "name": "Stock_Analysis_MCP",
    "description": "Stock analysis server"
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
```

### `portfolios.json` - Watchlists & Portfolios
```json
{
  "watchlists": {
    "nifty50": ["RELIANCE", "TCS", "HDFCBANK", "..."],
    "custom_tech": ["TCS", "INFY", "WIPRO"]
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

## 🛠️ Available Tools

| Tool | Description |
|------|-------------|
| `get_stock_price(symbol)` | Get current stock price |
| `get_stock_history(symbol, period)` | Get historical data |
| `analyze_portfolio(symbols)` | Optimize portfolio allocation |
| `get_watchlist(name)` | Get predefined watchlist |
| `technical_analysis(symbols, period)` | Technical analysis |
| `compare_stocks(symbol1, symbol2)` | Compare two stocks |
| `get_server_info()` | Server capabilities |

## 📊 Predefined Watchlists

- **nifty50**: Top 50 NSE stocks
- **banknifty**: Banking sector stocks  
- **it_stocks**: IT/Technology companies
- **pharma_stocks**: Pharmaceutical companies

## 🎯 Example Use Cases

### With Claude Desktop
- *"Analyze my portfolio with Reliance, TCS, and HDFC Bank"*
- *"What's the current price of Infosys?"*
- *"Compare Reliance and TCS stocks"*
- *"Show me the Nifty50 watchlist"*

### Portfolio Optimization
```python
# Custom portfolio
analyze_portfolio(["RELIANCE", "TCS", "HDFCBANK", "INFY", "HINDUNILVR"])

# Predefined portfolio
analyze_predefined_portfolio("conservative")
```

### Technical Analysis
```python
# Multi-stock analysis
technical_analysis(["RELIANCE", "TCS"], "3mo")

# Comparison analysis  
compare_stocks_prompt("RELIANCE", "TCS")
```

## Installation

### Prerequisites

- Python 3.10 or higher

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stock-analysis.git
cd stock-analysis
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python -m venv .venv
source .venv/bin/activate
```

3. Install the package in development mode:
```bash
pip install -e .[dev]
```

## Usage

### Running the MCP Server

```bash
python main.py
```

### Using as a Library

```python
import main

# Get current stock price
price_data = main.get_stock_price("RELIANCE")

# Analyze portfolio
portfolio_result = main.analyze_portfolio(["RELIANCE", "TCS", "INFY"])

# Get historical data
historical_data = main.get_stock_history("RELIANCE", period="1y")
```

## Development

### Running Tests

This project uses pytest for testing:

```bash
# Run tests
uv pip run pytest

# Run tests with coverage report
uv pip run pytest --cov=main --cov-report=term-missing
```

### Code Formatting and Linting

```bash
# Format code with black
uv pip run black .

# Sort imports with isort
uv pip run isort .

# Lint with flake8
uv pip run flake8 .

# Type check with mypy
uv pip run mypy main.py
```

## GitHub Workflow

This project includes a GitHub Actions workflow that automatically:

1. Runs tests on multiple Python versions (3.9, 3.10, 3.11)
2. Checks code formatting with Black
3. Sorts imports with isort
4. Performs linting with flake8
5. Runs type checking with mypy
6. Generates test coverage reports

The workflow runs on every push to the main branch, on pull requests, and weekly for regular checks.

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

### Prerequisites

- Python 3.9 or higher
- uv package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stock-analysis.git
cd stock-analysis
```

2. Create and activate a virtual environment with uv:
```bash
uv venv
# On Windows
.venv\Scripts\activate
# On Unix/MacOS
source .venv/bin/activate
```

3. Install dependencies:
```bash
uv sync
```

4. Install development dependencies:
```bash
uv sync --extra dev
```

## Usage

### Running the MCP Server

```bash
python -m stock_analysis.main
```

### Using the Analysis Functions

```python
from stock_analysis.core import StockAnalyzer

analyzer = StockAnalyzer()

# Get current stock price
price_data = analyzer.get_stock_price("RELIANCE")

# Analyze portfolio
portfolio_result = analyzer.analyze_portfolio(["RELIANCE", "TCS", "INFY"])

# Get historical data
historical_data = analyzer.get_stock_history("RELIANCE", period="1y")
```

## API Reference

### Main Functions

- `get_stock_price(symbol: str)` - Get current stock price
- `analyze_portfolio(symbols: list)` - Optimize portfolio allocation
- `get_stock_history(symbol: str, period: str)` - Get historical data
- `compare_stocks(symbol1: str, symbol2: str)` - Compare two stocks
- `technical_analysis(symbols: list, period: str)` - Generate technical analysis

### Stock Symbol Format

All stock symbols are automatically normalized to NSE format (e.g., "RELIANCE" becomes "RELIANCE.NS").

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=stock_analysis

# Run specific test file
uv run pytest tests/test_core.py
```

### Code Formatting

```bash
# Format code with black
uv run black stock_analysis tests

# Sort imports with isort
uv run isort stock_analysis tests

# Run linting
uv run flake8 stock_analysis tests

# Type checking
uv run mypy stock_analysis
```

### Pre-commit Hooks

Install pre-commit hooks to ensure code quality:

```bash
uv run pre-commit install
```

## Project Structure

```
stock-analysis/
├── stock_analysis/           # Main package
│   ├── __init__.py
│   ├── main.py              # MCP server entry point
│   ├── core.py              # Core analysis functions
│   └── utils.py             # Utility functions
├── tests/                   # Test files
│   ├── __init__.py
│   ├── test_core.py
│   └── test_utils.py
├── .github/workflows/       # GitHub Actions
│   └── ci.yml
├── pyproject.toml          # Project configuration
├── README.md
└── LICENSE
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational and research purposes only. Always consult with a qualified financial advisor before making investment decisions. The authors are not responsible for any financial losses incurred using this tool.
