"""
MCP Integration Tests for Yahoo Finance Data.

These tests verify:
- Market data fetching via yfinance library
- Historical data retrieval for volatility calculations
- Stock information for company fundamentals
- Dividend data for income analysis
- Error handling and fallback mechanisms

Note: These tests use real market data from Yahoo Finance via the yfinance library.
They may be slower and can fail if Yahoo Finance is unavailable.
"""

import pytest

from src.tools.market_data import (
    fetch_current_price,
    fetch_historical_data,
    fetch_stock_info,
    fetch_dividend_data,
    fetch_multiple_prices,
    calculate_returns,
    calculate_volatility,
)


# ============================================================================
# Basic Market Data Fetching Tests
# ============================================================================


@pytest.mark.mcp
@pytest.mark.slow
def test_fetch_current_price_real_data():
    """
    MCP Integration: Fetch current price for a real ticker.

    Tests actual Yahoo Finance API integration.
    """
    # Use a stable, well-known ticker
    ticker = "SPY"  # S&P 500 ETF

    # Fetch current price
    price = fetch_current_price(ticker)

    # Verify price object structure
    assert price.ticker == ticker
    assert price.price > 0
    assert price.currency == "USD"

    # Verify optional fields
    assert price.previous_close is not None
    assert price.day_high is not None
    assert price.day_low is not None
    assert price.volume is not None and price.volume > 0

    # Sanity check: SPY should be in reasonable range
    assert 100 < price.price < 1000  # SPY typically trades 300-600


@pytest.mark.mcp
@pytest.mark.slow
def test_fetch_historical_data_real_data():
    """
    MCP Integration: Fetch historical data for volatility analysis.

    Tests historical data retrieval needed for risk calculations.
    """
    ticker = "AAPL"  # Apple Inc.
    period = "1mo"  # 1 month of data
    interval = "1d"  # Daily data

    # Fetch historical data
    hist = fetch_historical_data(ticker, period=period, interval=interval)

    # Verify structure
    assert hist.ticker == ticker
    assert hist.data_points > 0
    assert hist.df is not None
    assert not hist.df.empty

    # Verify DataFrame has expected columns
    assert "Close" in hist.df.columns
    assert "Volume" in hist.df.columns
    assert "High" in hist.df.columns
    assert "Low" in hist.df.columns

    # Verify data sanity
    assert all(hist.df["Close"] > 0)
    assert all(hist.df["Volume"] >= 0)


@pytest.mark.mcp
@pytest.mark.slow
def test_fetch_stock_info_real_data():
    """
    MCP Integration: Fetch company information and fundamentals.

    Tests company info retrieval for compliance and suitability checks.
    """
    ticker = "MSFT"  # Microsoft

    # Fetch stock info
    info = fetch_stock_info(ticker)

    # Verify structure
    assert info.ticker == ticker
    assert info.name is not None
    assert len(info.name) > 0

    # Verify fundamentals (most should be present for large cap stocks)
    assert info.sector is not None
    assert info.industry is not None
    assert info.market_cap is not None and info.market_cap > 0

    # Verify optional metrics (may not all be present)
    # At least one of these should exist
    has_metrics = any([
        info.pe_ratio is not None,
        info.beta is not None,
        info.dividend_yield is not None,
    ])
    assert has_metrics


@pytest.mark.mcp
@pytest.mark.slow
def test_fetch_dividend_data_real_data():
    """
    MCP Integration: Fetch dividend history for income analysis.

    Tests dividend data retrieval for income-focused portfolios.
    """
    ticker = "JNJ"  # Johnson & Johnson - known dividend payer

    # Fetch dividend data
    div = fetch_dividend_data(ticker)

    # Verify structure
    assert div.ticker == ticker

    # JNJ pays dividends regularly, should have data
    assert div.dividend_count > 0
    assert div.total_dividends > 0
    assert div.latest_dividend is not None
    assert div.latest_dividend > 0
    assert div.latest_dividend_date is not None

    # Verify DataFrame
    assert div.df is not None
    assert not div.df.empty


# ============================================================================
# Batch Operations Tests
# ============================================================================


@pytest.mark.mcp
@pytest.mark.slow
def test_fetch_multiple_prices_real_data():
    """
    MCP Integration: Fetch prices for multiple tickers efficiently.

    Tests batch price fetching for portfolio analysis.
    """
    tickers = ["AAPL", "MSFT", "GOOGL"]

    # Fetch multiple prices
    prices = fetch_multiple_prices(tickers)

    # Should get prices for all tickers (or most)
    assert len(prices) >= 2  # Allow for potential failures

    # Verify each price
    for ticker, price in prices.items():
        assert price.ticker == ticker
        assert price.price > 0
        assert price.currency == "USD"


# ============================================================================
# Calculation Tests with Real Data
# ============================================================================


@pytest.mark.mcp
@pytest.mark.slow
def test_calculate_returns_from_real_data():
    """
    MCP Integration: Calculate returns from real historical data.

    Tests return calculation pipeline with actual market data.
    """
    ticker = "SPY"
    period = "3mo"

    # Fetch data
    hist = fetch_historical_data(ticker, period=period)

    # Calculate returns
    returns = calculate_returns(hist)

    # Verify returns structure
    assert len(returns) > 0
    assert returns.dtype.name.startswith("float")

    # Returns should be in reasonable range (-10% to +10% daily is extreme)
    assert returns.min() > -50.0  # Extreme daily loss
    assert returns.max() < 50.0   # Extreme daily gain

    # Most returns should be small (< 5% daily)
    assert (returns.abs() < 5.0).sum() > len(returns) * 0.8


@pytest.mark.mcp
@pytest.mark.slow
def test_calculate_volatility_from_real_data():
    """
    MCP Integration: Calculate volatility from real historical data.

    Tests volatility calculation used in risk analysis.
    """
    ticker = "NVDA"  # NVIDIA - typically more volatile
    period = "1y"

    # Fetch data
    hist = fetch_historical_data(ticker, period=period)

    # Calculate annualized volatility
    volatility = calculate_volatility(hist, annualized=True)

    # Volatility should be positive and in reasonable range
    assert volatility > 0
    assert volatility < 200  # Even very volatile stocks rarely exceed 200% annualized

    # Tech stocks typically have 20-60% annualized volatility
    assert 5 < volatility < 150


# ============================================================================
# Error Handling Tests
# ============================================================================


@pytest.mark.mcp
def test_fetch_invalid_ticker():
    """
    MCP Integration: Test error handling for invalid ticker.

    Verifies graceful handling of non-existent tickers.
    """
    ticker = "INVALID_TICKER_XYZ123"

    # Should raise an error
    with pytest.raises(Exception):
        fetch_current_price(ticker)


@pytest.mark.mcp
def test_fetch_non_dividend_stock():
    """
    MCP Integration: Test dividend fetching for non-dividend stock.

    Some stocks don't pay dividends - should handle gracefully.
    """
    ticker = "TSLA"  # Tesla historically hasn't paid dividends

    # Should complete without error
    div = fetch_dividend_data(ticker)

    # Should return empty result, not crash
    assert div.ticker == ticker
    # May have zero dividends
    assert div.dividend_count >= 0


# ============================================================================
# Integration with Risk Analysis
# ============================================================================


@pytest.mark.mcp
@pytest.mark.slow
def test_real_data_integration_with_risk_analysis():
    """
    MCP Integration: Use real market data in risk analysis workflow.

    Tests complete integration: fetch data → calculate metrics → risk analysis.
    """
    from src.agents.risk_analyst import calculate_volatility as calc_vol_risk
    from src.models.schemas import Holding, Portfolio, AssetClass

    ticker = "AAPL"

    # Fetch real historical data
    hist = fetch_historical_data(ticker, period="6mo")

    # Calculate volatility from real data
    volatility = calculate_volatility(hist, annualized=True)

    # Create portfolio with real price data
    current_price_data = fetch_current_price(ticker)

    portfolio = Portfolio(
        portfolio_name="Real Data Test",
        holdings=[
            Holding(
                ticker=ticker,
                name=current_price_data.ticker,
                quantity=100,
                value=current_price_data.price * 100,
                asset_class=AssetClass.equity,
                sector="Technology",
            )
        ],
    )

    # Calculate risk metrics
    portfolio_volatility = calc_vol_risk(portfolio)

    # Both volatility calculations should be positive
    assert volatility > 0
    assert portfolio_volatility > 0


# ============================================================================
# MCP Server Tests (if server is running)
# ============================================================================


@pytest.mark.mcp
@pytest.mark.slow
@pytest.mark.skip(reason="MCP server integration requires manual setup")
def test_mcp_server_connection():
    """
    MCP Integration: Test connection to Yahoo Finance MCP server.

    NOTE: This test is skipped by default. To run it:
    1. Start the Yahoo Finance MCP server
    2. Remove the @pytest.mark.skip decorator
    3. Run: pytest -m mcp tests/test_mcp_integration.py::test_mcp_server_connection
    """
    # This would test actual MCP server connection
    # when use_mcp=True parameter is implemented
    ticker = "SPY"

    # Try fetching with MCP server
    price = fetch_current_price(ticker, use_mcp=True)

    assert price.ticker == ticker
    assert price.price > 0


# ============================================================================
# Performance Tests
# ============================================================================


@pytest.mark.mcp
@pytest.mark.slow
def test_market_data_fetch_performance():
    """
    MCP Integration: Test market data fetching performance.

    Ensures data fetching completes in reasonable time.
    """
    import time

    ticker = "AAPL"

    # Test current price fetching speed
    start = time.time()
    price = fetch_current_price(ticker)
    price_time = time.time() - start

    # Should complete in reasonable time (< 5 seconds)
    assert price_time < 5.0, f"Price fetch took {price_time:.2f}s (expected < 5s)"

    # Test historical data fetching speed
    start = time.time()
    hist = fetch_historical_data(ticker, period="1mo")
    hist_time = time.time() - start

    # Should complete in reasonable time (< 10 seconds)
    assert hist_time < 10.0, f"Historical data fetch took {hist_time:.2f}s (expected < 10s)"


# ============================================================================
# Data Quality Tests
# ============================================================================


@pytest.mark.mcp
@pytest.mark.slow
def test_market_data_quality_checks():
    """
    MCP Integration: Verify quality of fetched market data.

    Ensures data meets quality standards for analysis.
    """
    ticker = "SPY"
    period = "1y"

    # Fetch historical data
    hist = fetch_historical_data(ticker, period=period)

    # Quality check 1: No missing data
    assert not hist.df["Close"].isnull().any(), "Historical data has missing Close prices"

    # Quality check 2: Positive prices
    assert (hist.df["Close"] > 0).all(), "Historical data has non-positive prices"

    # Quality check 3: Reasonable price ranges (no obvious data errors)
    price_mean = hist.df["Close"].mean()
    price_std = hist.df["Close"].std()

    # No price should be more than 10 standard deviations from mean (data error check)
    outliers = hist.df[abs(hist.df["Close"] - price_mean) > 10 * price_std]
    assert len(outliers) == 0, f"Found {len(outliers)} potential data errors"

    # Quality check 4: Sufficient data points
    # For 1 year of daily data, should have ~250 trading days
    assert hist.data_points >= 200, f"Insufficient data points: {hist.data_points} (expected ~250)"


# ============================================================================
# Fallback Mechanism Tests
# ============================================================================


@pytest.mark.mcp
def test_fallback_to_direct_yfinance():
    """
    MCP Integration: Test fallback to direct yfinance when MCP unavailable.

    Verifies system can work without MCP server.
    """
    ticker = "AAPL"

    # Explicitly use direct yfinance (use_mcp=False)
    price = fetch_current_price(ticker, use_mcp=False)

    # Should work via fallback
    assert price.ticker == ticker
    assert price.price > 0


# ============================================================================
# Multi-Ticker Analysis Tests
# ============================================================================


@pytest.mark.mcp
@pytest.mark.slow
def test_portfolio_level_market_data_integration():
    """
    MCP Integration: Test market data integration at portfolio level.

    Verifies fetching data for multiple holdings in a portfolio.
    """
    from src.models.schemas import Holding, Portfolio, AssetClass

    # Define portfolio tickers
    tickers = ["AAPL", "MSFT", "GOOGL", "SPY", "BND"]

    # Fetch prices for all holdings
    prices = fetch_multiple_prices(tickers)

    # Should get most or all prices
    assert len(prices) >= 4  # Allow for one potential failure

    # Create portfolio with real market data
    holdings = []
    for ticker in prices.keys():
        price_data = prices[ticker]
        holdings.append(
            Holding(
                ticker=ticker,
                name=ticker,
                quantity=100,
                value=price_data.price * 100,
                asset_class=AssetClass.equity if ticker != "BND" else AssetClass.bond,
                sector="Diversified",
            )
        )

    portfolio = Portfolio(
        portfolio_name="Real Market Data Portfolio",
        holdings=holdings,
    )

    # Verify portfolio creation succeeded
    assert len(portfolio.holdings) >= 4
    assert all(h.value > 0 for h in portfolio.holdings)
