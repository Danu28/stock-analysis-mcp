# Stock Analysis Tool

A comprehensive stock analysis tool that provides portfolio optimization, technical analysis, and real-time stock price data for NSE (India) listed stocks.

## Features

- **Portfolio Optimization**: Optimize portfolio allocation using Modern Portfolio Theory
- **Real-time Stock Prices**: Get current stock prices for NSE listed companies
- **Historical Data**: Fetch and analyze historical stock data
- **Technical Analysis**: Generate technical analysis prompts and insights
- **Stock Comparison**: Compare multiple stocks side by side
- **MCP Server**: Built as a Model Context Protocol server for integration with AI assistants

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
# Windows
uv venv
.venv\Scripts\activate

# Linux/macOS
uv venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
uv pip sync requirements.txt
```

4. For development, install development dependencies:
```bash
uv pip sync requirements-dev.txt
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
