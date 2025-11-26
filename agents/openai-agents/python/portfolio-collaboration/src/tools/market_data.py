"""
Market Data Tools for Portfolio Analysis.

This module provides clean Python interfaces to fetch real-time and historical
market data from Yahoo Finance. It supports both:
1. Yahoo Finance MCP Server (preferred) - for agent-based workflows
2. Direct yfinance library calls (fallback) - when MCP server is unavailable

Key Functions:
- fetch_current_price() - Get current stock price
- fetch_historical_data() - Get historical OHLCV data for analysis
- fetch_stock_info() - Get company fundamentals and metrics
- fetch_dividend_data() - Get dividend history
- fetch_financial_statement() - Get income statement, balance sheet, or cashflow

Biblical Principle: TRUTH - Providing accurate, real-time market data for informed decisions.
Biblical Principle: SERVE - Simple API that abstracts complexity of data retrieval.
Biblical Principle: PERSEVERE - Graceful fallback when primary data source is unavailable.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union

import pandas as pd
import yfinance as yf
from pydantic import BaseModel, Field

# ============================================================================
# Logging Configuration
# ============================================================================

logger = logging.getLogger(__name__)

# ============================================================================
# Pydantic Models for Structured Outputs
# ============================================================================


class StockPrice(BaseModel):
    """Current stock price information."""

    ticker: str = Field(..., description="Stock ticker symbol")
    price: float = Field(..., description="Current price")
    currency: str = Field(default="USD", description="Currency of the price")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Time of price quote"
    )
    previous_close: Optional[float] = Field(
        None, description="Previous closing price"
    )
    day_high: Optional[float] = Field(None, description="Day's high price")
    day_low: Optional[float] = Field(None, description="Day's low price")
    volume: Optional[int] = Field(None, description="Trading volume")


class HistoricalData(BaseModel):
    """Historical stock price data."""

    ticker: str = Field(..., description="Stock ticker symbol")
    start_date: str = Field(..., description="Start date of data")
    end_date: str = Field(..., description="End date of data")
    data_points: int = Field(..., description="Number of data points")
    df: Optional[pd.DataFrame] = Field(
        None, description="Pandas DataFrame with OHLCV data"
    )

    class Config:
        arbitrary_types_allowed = True


class CompanyInfo(BaseModel):
    """Company fundamental information and metrics."""

    ticker: str = Field(..., description="Stock ticker symbol")
    name: str = Field(..., description="Company name")
    sector: Optional[str] = Field(None, description="Business sector")
    industry: Optional[str] = Field(None, description="Industry classification")
    market_cap: Optional[float] = Field(None, description="Market capitalization")
    pe_ratio: Optional[float] = Field(None, description="Price-to-earnings ratio")
    dividend_yield: Optional[float] = Field(None, description="Dividend yield %")
    beta: Optional[float] = Field(None, description="Beta (volatility measure)")
    fifty_two_week_high: Optional[float] = Field(None, description="52-week high")
    fifty_two_week_low: Optional[float] = Field(None, description="52-week low")
    description: Optional[str] = Field(None, description="Company description")


class DividendData(BaseModel):
    """Dividend payment history."""

    ticker: str = Field(..., description="Stock ticker symbol")
    dividend_count: int = Field(..., description="Number of dividend payments")
    total_dividends: float = Field(..., description="Total dividends paid")
    latest_dividend: Optional[float] = Field(None, description="Most recent dividend")
    latest_dividend_date: Optional[str] = Field(
        None, description="Date of latest dividend"
    )
    df: Optional[pd.DataFrame] = Field(
        None, description="Pandas DataFrame with dividend history"
    )

    class Config:
        arbitrary_types_allowed = True


# ============================================================================
# Core Market Data Functions
# ============================================================================


def fetch_current_price(ticker: str, use_mcp: bool = False) -> StockPrice:
    """
    Fetch the current stock price for a given ticker.

    This function provides current market data including price, volume, and
    day range. It first attempts to use the MCP server if requested, then
    falls back to direct yfinance calls.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "MSFT")
        use_mcp: If True, attempt to use Yahoo Finance MCP server first
                 (default: False, use direct yfinance)

    Returns:
        StockPrice: Structured current price information

    Raises:
        ValueError: If ticker is invalid or data cannot be fetched

    Example:
        >>> price = fetch_current_price("AAPL")
        >>> print(f"Current price: ${price.price:.2f}")
        Current price: $178.45
    """
    logger.info(f"Fetching current price for {ticker} (use_mcp={use_mcp})")

    # For now, we'll use direct yfinance calls
    # TODO: Implement MCP server integration when needed
    if use_mcp:
        logger.warning("MCP server integration not yet implemented, using direct call")

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Extract current price
        current_price = info.get("currentPrice") or info.get("regularMarketPrice")
        if current_price is None:
            raise ValueError(f"Unable to fetch current price for {ticker}")

        return StockPrice(
            ticker=ticker,
            price=current_price,
            currency=info.get("currency", "USD"),
            previous_close=info.get("previousClose"),
            day_high=info.get("dayHigh"),
            day_low=info.get("dayLow"),
            volume=info.get("volume"),
        )

    except Exception as e:
        logger.error(f"Error fetching current price for {ticker}: {e}")
        raise ValueError(f"Failed to fetch price for {ticker}: {e}")


def fetch_historical_data(
    ticker: str,
    period: str = "1mo",
    interval: str = "1d",
    use_mcp: bool = False,
) -> HistoricalData:
    """
    Fetch historical stock price data for analysis.

    This function retrieves historical OHLCV (Open, High, Low, Close, Volume)
    data which is essential for calculating volatility, returns, and other
    risk metrics.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "MSFT")
        period: Data period - valid values: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
                (default: "1mo")
        interval: Data interval - valid values: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
                  (default: "1d")
        use_mcp: If True, attempt to use Yahoo Finance MCP server first
                 (default: False, use direct yfinance)

    Returns:
        HistoricalData: Structured historical price data with DataFrame

    Raises:
        ValueError: If ticker is invalid or data cannot be fetched

    Example:
        >>> hist = fetch_historical_data("AAPL", period="1y", interval="1d")
        >>> print(f"Retrieved {hist.data_points} days of data")
        >>> print(hist.df[["Close", "Volume"]].head())
    """
    logger.info(
        f"Fetching historical data for {ticker} (period={period}, interval={interval}, use_mcp={use_mcp})"
    )

    # For now, we'll use direct yfinance calls
    # TODO: Implement MCP server integration when needed
    if use_mcp:
        logger.warning("MCP server integration not yet implemented, using direct call")

    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)

        if df.empty:
            raise ValueError(f"No historical data found for {ticker}")

        # Get date range
        start_date = df.index[0].strftime("%Y-%m-%d")
        end_date = df.index[-1].strftime("%Y-%m-%d")
        data_points = len(df)

        return HistoricalData(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            data_points=data_points,
            df=df,
        )

    except Exception as e:
        logger.error(f"Error fetching historical data for {ticker}: {e}")
        raise ValueError(f"Failed to fetch historical data for {ticker}: {e}")


def fetch_stock_info(ticker: str, use_mcp: bool = False) -> CompanyInfo:
    """
    Fetch comprehensive company information and fundamental metrics.

    This function retrieves company details, financial metrics, and ratios
    used for valuation analysis, suitability assessment, and sector allocation.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "MSFT")
        use_mcp: If True, attempt to use Yahoo Finance MCP server first
                 (default: False, use direct yfinance)

    Returns:
        CompanyInfo: Structured company information and metrics

    Raises:
        ValueError: If ticker is invalid or data cannot be fetched

    Example:
        >>> info = fetch_stock_info("AAPL")
        >>> print(f"{info.name} - Sector: {info.sector}")
        >>> print(f"P/E Ratio: {info.pe_ratio:.2f}")
        Apple Inc. - Sector: Technology
        P/E Ratio: 28.45
    """
    logger.info(f"Fetching stock info for {ticker} (use_mcp={use_mcp})")

    # For now, we'll use direct yfinance calls
    # TODO: Implement MCP server integration when needed
    if use_mcp:
        logger.warning("MCP server integration not yet implemented, using direct call")

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Extract key information
        return CompanyInfo(
            ticker=ticker,
            name=info.get("longName", info.get("shortName", ticker)),
            sector=info.get("sector"),
            industry=info.get("industry"),
            market_cap=info.get("marketCap"),
            pe_ratio=info.get("trailingPE") or info.get("forwardPE"),
            dividend_yield=info.get("dividendYield"),
            beta=info.get("beta"),
            fifty_two_week_high=info.get("fiftyTwoWeekHigh"),
            fifty_two_week_low=info.get("fiftyTwoWeekLow"),
            description=info.get("longBusinessSummary"),
        )

    except Exception as e:
        logger.error(f"Error fetching stock info for {ticker}: {e}")
        raise ValueError(f"Failed to fetch stock info for {ticker}: {e}")


def fetch_dividend_data(ticker: str, use_mcp: bool = False) -> DividendData:
    """
    Fetch dividend payment history for a stock.

    This function retrieves dividend payment data which is important for
    income-focused portfolios and retirement planning.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "MSFT")
        use_mcp: If True, attempt to use Yahoo Finance MCP server first
                 (default: False, use direct yfinance)

    Returns:
        DividendData: Structured dividend payment history

    Raises:
        ValueError: If ticker is invalid or data cannot be fetched

    Example:
        >>> div = fetch_dividend_data("AAPL")
        >>> print(f"Total dividends paid: {div.dividend_count}")
        >>> print(f"Latest dividend: ${div.latest_dividend:.2f}")
        Total dividends paid: 87
        Latest dividend: $0.24
    """
    logger.info(f"Fetching dividend data for {ticker} (use_mcp={use_mcp})")

    # For now, we'll use direct yfinance calls
    # TODO: Implement MCP server integration when needed
    if use_mcp:
        logger.warning("MCP server integration not yet implemented, using direct call")

    try:
        stock = yf.Ticker(ticker)
        dividends = stock.dividends

        if dividends.empty:
            # Stock doesn't pay dividends
            return DividendData(
                ticker=ticker,
                dividend_count=0,
                total_dividends=0.0,
                latest_dividend=None,
                latest_dividend_date=None,
                df=dividends,
            )

        # Calculate metrics
        dividend_count = len(dividends)
        total_dividends = dividends.sum()
        latest_dividend = dividends.iloc[-1]
        latest_dividend_date = dividends.index[-1].strftime("%Y-%m-%d")

        return DividendData(
            ticker=ticker,
            dividend_count=dividend_count,
            total_dividends=float(total_dividends),
            latest_dividend=float(latest_dividend),
            latest_dividend_date=latest_dividend_date,
            df=dividends,
        )

    except Exception as e:
        logger.error(f"Error fetching dividend data for {ticker}: {e}")
        raise ValueError(f"Failed to fetch dividend data for {ticker}: {e}")


def fetch_financial_statement(
    ticker: str,
    statement_type: str = "income_stmt",
    quarterly: bool = False,
    use_mcp: bool = False,
) -> pd.DataFrame:
    """
    Fetch financial statements (income, balance sheet, cashflow).

    This function retrieves company financial statements for fundamental
    analysis and financial health assessment.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "MSFT")
        statement_type: Type of statement - valid values:
                        - "income_stmt" (income statement)
                        - "balance_sheet" (balance sheet)
                        - "cashflow" (cash flow statement)
        quarterly: If True, fetch quarterly statements; if False, fetch annual
                   (default: False)
        use_mcp: If True, attempt to use Yahoo Finance MCP server first
                 (default: False, use direct yfinance)

    Returns:
        pd.DataFrame: Financial statement data

    Raises:
        ValueError: If ticker is invalid or statement type is unknown

    Example:
        >>> income = fetch_financial_statement("AAPL", "income_stmt")
        >>> print(income.loc["Total Revenue"])
        2023-09-30    3.835e+11
        2022-09-30    3.658e+11
        2021-09-30    3.659e+11
    """
    logger.info(
        f"Fetching {statement_type} for {ticker} (quarterly={quarterly}, use_mcp={use_mcp})"
    )

    # For now, we'll use direct yfinance calls
    # TODO: Implement MCP server integration when needed
    if use_mcp:
        logger.warning("MCP server integration not yet implemented, using direct call")

    try:
        stock = yf.Ticker(ticker)

        # Map statement types to yfinance attributes
        if statement_type == "income_stmt":
            df = stock.quarterly_income_stmt if quarterly else stock.income_stmt
        elif statement_type == "balance_sheet":
            df = stock.quarterly_balance_sheet if quarterly else stock.balance_sheet
        elif statement_type == "cashflow":
            df = stock.quarterly_cashflow if quarterly else stock.cashflow
        else:
            raise ValueError(
                f"Unknown statement type: {statement_type}. "
                "Valid types: income_stmt, balance_sheet, cashflow"
            )

        if df.empty:
            raise ValueError(f"No {statement_type} data found for {ticker}")

        return df

    except Exception as e:
        logger.error(f"Error fetching {statement_type} for {ticker}: {e}")
        raise ValueError(f"Failed to fetch {statement_type} for {ticker}: {e}")


# ============================================================================
# Batch Operations
# ============================================================================


def fetch_multiple_prices(
    tickers: List[str], use_mcp: bool = False
) -> Dict[str, StockPrice]:
    """
    Fetch current prices for multiple tickers efficiently.

    Args:
        tickers: List of stock ticker symbols
        use_mcp: If True, attempt to use Yahoo Finance MCP server first

    Returns:
        Dict mapping ticker symbols to StockPrice objects

    Example:
        >>> prices = fetch_multiple_prices(["AAPL", "MSFT", "GOOGL"])
        >>> for ticker, price in prices.items():
        ...     print(f"{ticker}: ${price.price:.2f}")
        AAPL: $178.45
        MSFT: $378.91
        GOOGL: $141.23
    """
    logger.info(f"Fetching prices for {len(tickers)} tickers")

    prices = {}
    for ticker in tickers:
        try:
            prices[ticker] = fetch_current_price(ticker, use_mcp=use_mcp)
        except Exception as e:
            logger.warning(f"Failed to fetch price for {ticker}: {e}")
            # Continue with other tickers even if one fails

    return prices


def fetch_multiple_stock_info(
    tickers: List[str], use_mcp: bool = False
) -> Dict[str, CompanyInfo]:
    """
    Fetch company info for multiple tickers efficiently.

    Args:
        tickers: List of stock ticker symbols
        use_mcp: If True, attempt to use Yahoo Finance MCP server first

    Returns:
        Dict mapping ticker symbols to CompanyInfo objects

    Example:
        >>> info_dict = fetch_multiple_stock_info(["AAPL", "MSFT"])
        >>> for ticker, info in info_dict.items():
        ...     print(f"{ticker} ({info.name}) - {info.sector}")
        AAPL (Apple Inc.) - Technology
        MSFT (Microsoft Corporation) - Technology
    """
    logger.info(f"Fetching stock info for {len(tickers)} tickers")

    info_dict = {}
    for ticker in tickers:
        try:
            info_dict[ticker] = fetch_stock_info(ticker, use_mcp=use_mcp)
        except Exception as e:
            logger.warning(f"Failed to fetch info for {ticker}: {e}")
            # Continue with other tickers even if one fails

    return info_dict


# ============================================================================
# Utility Functions
# ============================================================================


def calculate_returns(historical_data: HistoricalData) -> pd.Series:
    """
    Calculate daily returns from historical price data.

    Args:
        historical_data: HistoricalData object with OHLCV DataFrame

    Returns:
        pd.Series: Daily percentage returns

    Example:
        >>> hist = fetch_historical_data("AAPL", period="1mo")
        >>> returns = calculate_returns(hist)
        >>> print(f"Average daily return: {returns.mean():.4f}%")
    """
    if historical_data.df is None or historical_data.df.empty:
        raise ValueError("Historical data DataFrame is empty")

    close_prices = historical_data.df["Close"]
    returns = close_prices.pct_change().dropna() * 100  # Convert to percentage
    return returns


def calculate_volatility(historical_data: HistoricalData, annualized: bool = True) -> float:
    """
    Calculate volatility (standard deviation of returns).

    Args:
        historical_data: HistoricalData object with OHLCV DataFrame
        annualized: If True, annualize the volatility (multiply by sqrt(252))

    Returns:
        float: Volatility as a percentage

    Example:
        >>> hist = fetch_historical_data("AAPL", period="1y")
        >>> vol = calculate_volatility(hist, annualized=True)
        >>> print(f"Annualized volatility: {vol:.2f}%")
        Annualized volatility: 24.53%
    """
    returns = calculate_returns(historical_data)
    volatility = returns.std()

    if annualized:
        # Annualize using sqrt(252) - 252 trading days per year
        volatility = volatility * (252 ** 0.5)

    return volatility
