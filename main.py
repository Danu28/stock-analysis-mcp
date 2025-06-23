"""
Stock Analysis Tool - MCP Server

This module provides stock analysis capabilities through an MCP (Model Context Protocol)
server interface.
"""

import logging
from functools import lru_cache
from typing import Dict, List

import numpy as np
import pandas as pd
from scipy.optimize import minimize
import yfinance as yf
from mcp.server.fastmcp import FastMCP

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create an MCP server with a custom name
mcp = FastMCP("Stock_Price_MCP")


def normalize_symbol(symbol: str) -> str:
    """
    Normalize a stock symbol to reflect NSE notation.
    If a symbol does not have a suffix (e.g., '.NS' or '.BO'), append '.NS' by default.
    """
    if not (symbol.endswith(".NS") or symbol.endswith(".BO")):
        symbol = f"{symbol}.NS"
    return symbol


def normalize_symbols(symbols: list) -> list:
    """
    Normalize a list of stock symbols.
    """
    return [normalize_symbol(s) for s in symbols]


@lru_cache(maxsize=32)
def get_multiple_tickers(symbols: tuple) -> dict:
    """
    Retrieve and cache multiple yfinance Ticker instances.
    Accepts a tuple of already normalized symbols and returns a dictionary mapping symbol -> Ticker object.
    """
    # Ensure the tickers are normalized already
    yf.Tickers(" ".join(symbols))
    ticker_dict = {symbol: yf.Ticker(symbol) for symbol in symbols}
    return ticker_dict


def fetch_historical_data(symbols: list, period: str = "1y") -> pd.DataFrame:
    normalized = normalize_symbols(symbols)
    tickers = get_multiple_tickers(tuple(normalized))
    df_list = []
    for norm_symbol, orig_symbol in zip(normalized, symbols):
        ticker = tickers[norm_symbol]
        data = ticker.history(period=period)["Close"]
        # Rename series with the original symbol (or normalized if preferred)
        data.rename(orig_symbol, inplace=True)
        df_list.append(data)
    prices_df = pd.concat(df_list, axis=1)
    return prices_df


def calculate_returns(price_df: pd.DataFrame) -> pd.DataFrame:
    returns = price_df.pct_change().dropna()
    return returns


def optimize_portfolio(returns: pd.DataFrame) -> dict:
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    num_stocks = len(mean_returns)

    def portfolio_performance(weights):
        portfolio_return = np.dot(weights, mean_returns)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return portfolio_return / portfolio_volatility  # Sharpe Ratio

    constraints = {"type": "eq", "fun": lambda x: np.sum(x) - 1}
    bounds = tuple((0, 1) for _ in range(num_stocks))
    init_guess = np.array([1.0 / num_stocks] * num_stocks)

    result = minimize(
        lambda w: -portfolio_performance(w),
        init_guess,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )

    if result.success:
        optimized_weights = result.x
        expected_return = np.dot(optimized_weights, mean_returns)
        expected_volatility = np.sqrt(
            np.dot(optimized_weights.T, np.dot(cov_matrix, optimized_weights))
        )

        weight_dict = {
            symbol: round(weight, 4)
            for symbol, weight in zip(returns.columns, optimized_weights)
            if weight > 0.01
        }

        return {
            "weights": weight_dict,
            "expected_return": round(expected_return * 100, 2),  # %
            "expected_volatility": round(expected_volatility * 100, 2),  # %
        }
    else:
        raise ValueError("Optimization failed")


@mcp.tool()
def analyze_portfolio(symbols: list) -> dict:
    """
    Analyze a list of stock tickers and return optimized portfolio allocation,
    including expected returns, volatility, and weight distribution.
    All stock symbols are normalized to ensure correct NSE(INDIA) formatting.
    """
    try:
        price_data = fetch_historical_data(symbols)
        returns_data = calculate_returns(price_data)
        best_allocation = optimize_portfolio(returns_data)

        result = {
            "status": "success",
            "optimized_allocation": best_allocation["weights"],
            "expected_return": best_allocation["expected_return"],
            "expected_volatility": best_allocation["expected_volatility"],
            "symbols": symbols,
            "period": "1y",
            "details": "The portfolio has been optimized for the best risk/reward ratio (Sharpe Ratio).",
        }
        return result
    except Exception as e:
        logger.exception("Error optimizing portfolio: %s", str(e))
        return {"status": "error", "message": f"Error optimizing portfolio: {str(e)}"}


@lru_cache(maxsize=32)
def get_ticker(symbol: str) -> yf.Ticker:
    """
    Retrieve and cache a yfinance Ticker instance.
    Normalize the symbol to ensure correct NSE formatting.
    """
    norm_symbol = normalize_symbol(symbol)
    return yf.Ticker(norm_symbol)


@mcp.tool()
def get_stock_price(symbol: str) -> dict:
    """
    Retrieve the current stock price for the given ticker symbol.
    Returns a dictionary with detailed stock price information.
    All stock symbols are normalized to ensure correct NSE(INDIA) formatting.
    """
    try:
        ticker = get_ticker(symbol)
        data = ticker.history(period="1d")

        if not data.empty:
            price = data["Close"].iloc[-1]
            info = ticker.info
            return {
                "status": "success",
                "symbol": symbol,
                "price": float(price),
                "timestamp": str(data.index[-1]),
                "currency": info.get("currency", "INR"),
                "volume": int(data["Volume"].iloc[-1]),
            }
        else:
            info = ticker.info
            price = info.get("regularMarketPrice")
            if price is None:
                logger.error(
                    "No valid regularMarketPrice available for symbol '%s'.", symbol
                )
                return {
                    "status": "error",
                    "message": "No valid market price available.",
                }
            return {
                "status": "success",
                "symbol": symbol,
                "price": float(price),
                "timestamp": str(pd.Timestamp.now()),
                "currency": info.get("currency", "INR"),
                "volume": int(info.get("regularMarketVolume", 0)),
            }
    except Exception as e:
        logger.exception("Error retrieving stock price for %s: %s", symbol, str(e))
        return {
            "status": "error",
            "message": f"Error retrieving stock price for {symbol}: {str(e)}",
        }


@mcp.resource("stock://{symbol}")
def stock_resource(symbol: str) -> str:
    """
    Expose stock price data as a resource.
    Returns a formatted string with the current stock price for the given symbol.
    All stock symbols are normalized to ensure correct NSE(INDIA) formatting.
    """
    data = get_stock_price(symbol)
    if data.get("status") != "success":
        return f"Error: Could not retrieve price for symbol '{symbol}'."
    # Use the INR symbol "₹" for display
    return f"The current price of '{symbol}' is ₹{data['price']:.2f}."


@mcp.tool()
def get_stock_history(symbol: str, period: str = "1mo") -> str:
    """
    Retrieve historical data for a stock given its ticker symbol and period.
    Returns historical data as a CSV formatted string.
    All stock symbols are normalized to ensure correct NSE(INDIA) formatting.
    """
    try:
        ticker = get_ticker(symbol)
        data = ticker.history(period=period)

        if data.empty:
            return f"No historical data found for symbol '{symbol}' with period '{period}'."
        csv_data = data.to_csv()
        return csv_data
    except Exception as e:
        logger.exception("Error fetching historical data for %s: %s", symbol, str(e))
        return f"Error fetching historical data: {str(e)}"


@mcp.prompt()
def compare_stocks_prompt(symbol1: str, symbol2: str) -> str:
    """
    Generate a detailed technical analysis prompt comparing two stock symbols.
    All stock symbols are normalized to ensure correct NSE(INDIA) formatting.
    """
    prompt = f"""
    Please provide a detailed technical analysis comparing {symbol1} and {symbol2} with the following aspects:

    Individual Stock Analysis:
        1. Current price and recent price action
        2. Key technical indicators
        3. Support and resistance levels
        4. Volume analysis
        5. Recent price patterns/trends

    Comparative Analysis:
        1. Relative performance comparison
        2. Risk assessment
        3. Technical strength evaluation
        4. Trading volume comparison
        5. Sector/Industry context (if applicable)

    Final Recommendation:
        1. Which stock is better for buying and why

    Specific entry strategy:
        1. Buy zone
        2. Stop loss levels
        3. Price targets
        4. Suggested time horizon

    Risk Management:
        1. Position sizing

    Please provide data-driven insights and specific price levels where possible.
    """
    return prompt.strip()


@mcp.tool()
def compare_stocks(symbol1: str, symbol2: str) -> str:
    """
    Compare the current stock prices of two ticker symbols.
    Returns a formatted comparison string.
    All stock symbols are normalized to ensure correct NSE(INDIA) formatting.
    """
    data1 = get_stock_price(symbol1)
    data2 = get_stock_price(symbol2)

    # Check for errors in fetching either price
    if data1.get("status") != "success" or data2.get("status") != "success":
        return f"Error: Could not retrieve data for comparison of '{symbol1}' and '{symbol2}'."

    price1 = data1["price"]
    price2 = data2["price"]

    if price1 > price2:
        result = f"{symbol1} (₹{price1:.2f}) is higher than {symbol2} (₹{price2:.2f})."
    elif price1 < price2:
        result = f"{symbol1} (₹{price1:.2f}) is lower than {symbol2} (₹{price2:.2f})."
    else:
        result = f"Both {symbol1} and {symbol2} have the same price (₹{price1:.2f})."
    return result


@mcp.tool()
def technical_analysis(symbols: list, period: str = "3mo") -> dict:
    """
    Perform technical analysis on a list of stock symbols.
    Fetch historical data and generate an analysis prompt for each symbol.
    All stock symbols are normalized to ensure correct NSE(INDIA) formatting.
    """
    try:
        historical_data = {}
        norm_symbols = normalize_symbols(symbols)
        for orig_symbol, norm_symbol in zip(symbols, norm_symbols):
            ticker = yf.Ticker(norm_symbol)
            data = ticker.history(period=period)
            if not data.empty:
                historical_data[orig_symbol] = data
            else:
                logger.warning(f"No historical data found for symbol '{orig_symbol}'.")

        if not historical_data:
            return {
                "status": "error",
                "message": "No historical data available for analysis.",
            }

        analysis_requests = {}
        for symbol, data in historical_data.items():
            latest_close = data["Close"].iloc[-1]
            volume = data["Volume"].iloc[-1]

            prompt = f"""
            Perform a detailed technical analysis for stock: {symbol}
    
            1. Current Price: {latest_close:.2f}
            2. Volume: {volume}
            3. Recent Price Trend: Analyze the last {period} trend.
            4. Key Technical Indicators: Suggest RSI, MACD, and Moving Averages.
            5. Support and Resistance Levels based on historical prices.
            6. Price Pattern Observations (e.g., Head & Shoulders, Double Top, etc.).
            7. Risk and Reward Assessment.
            8. Final Buy/Sell Recommendation with suggested buy range, stop loss, and target price.
            """

            analysis_requests[symbol] = prompt.strip()

        return {
            "status": "success",
            "analysis_prompts": analysis_requests,
            "period": period,
        }

    except Exception as e:
        logger.exception("Error performing technical analysis: %s", str(e))
        return {
            "status": "error",
            "message": f"Error performing technical analysis: {str(e)}",
        }


if __name__ == "__main__":
    mcp.run()
