"""
Test Market Data Tools.

This script demonstrates the market data fetching capabilities including:
- Current stock prices
- Historical data for volatility analysis
- Company information
- Dividend history

Run this script to verify Yahoo Finance integration is working correctly.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.tools.market_data import (
    fetch_current_price,
    fetch_historical_data,
    fetch_stock_info,
    fetch_dividend_data,
    fetch_multiple_prices,
    calculate_returns,
    calculate_volatility,
)


def test_current_price():
    """Test fetching current stock price."""
    print("\n" + "=" * 80)
    print("TEST: Fetch Current Price")
    print("=" * 80)

    ticker = "AAPL"
    print(f"\nFetching current price for {ticker}...")

    try:
        price = fetch_current_price(ticker)
        print(f"\n✓ Success!")
        print(f"  Ticker: {price.ticker}")
        print(f"  Current Price: ${price.price:.2f}")
        print(f"  Currency: {price.currency}")
        print(f"  Previous Close: ${price.previous_close:.2f}")
        print(f"  Day High: ${price.day_high:.2f}")
        print(f"  Day Low: ${price.day_low:.2f}")
        print(f"  Volume: {price.volume:,}")
        return True
    except Exception as e:
        print(f"\n✗ Failed: {e}")
        return False


def test_historical_data():
    """Test fetching historical data."""
    print("\n" + "=" * 80)
    print("TEST: Fetch Historical Data")
    print("=" * 80)

    ticker = "MSFT"
    period = "3mo"
    print(f"\nFetching {period} historical data for {ticker}...")

    try:
        hist = fetch_historical_data(ticker, period=period, interval="1d")
        print(f"\n✓ Success!")
        print(f"  Ticker: {hist.ticker}")
        print(f"  Period: {hist.start_date} to {hist.end_date}")
        print(f"  Data Points: {hist.data_points}")
        print(f"\n  Recent Prices:")
        print(hist.df[["Close", "Volume"]].tail())

        # Calculate returns and volatility
        returns = calculate_returns(hist)
        volatility = calculate_volatility(hist, annualized=True)
        print(f"\n  Average Daily Return: {returns.mean():.4f}%")
        print(f"  Annualized Volatility: {volatility:.2f}%")
        return True
    except Exception as e:
        print(f"\n✗ Failed: {e}")
        return False


def test_stock_info():
    """Test fetching company information."""
    print("\n" + "=" * 80)
    print("TEST: Fetch Company Information")
    print("=" * 80)

    ticker = "GOOGL"
    print(f"\nFetching company info for {ticker}...")

    try:
        info = fetch_stock_info(ticker)
        print(f"\n✓ Success!")
        print(f"  Ticker: {info.ticker}")
        print(f"  Name: {info.name}")
        print(f"  Sector: {info.sector}")
        print(f"  Industry: {info.industry}")
        print(f"  Market Cap: ${info.market_cap:,.0f}")
        print(f"  P/E Ratio: {info.pe_ratio:.2f}")
        print(f"  Beta: {info.beta:.2f}")
        print(f"  52-Week High: ${info.fifty_two_week_high:.2f}")
        print(f"  52-Week Low: ${info.fifty_two_week_low:.2f}")
        if info.dividend_yield:
            print(f"  Dividend Yield: {info.dividend_yield * 100:.2f}%")
        print(f"\n  Description: {info.description[:200]}...")
        return True
    except Exception as e:
        print(f"\n✗ Failed: {e}")
        return False


def test_dividend_data():
    """Test fetching dividend history."""
    print("\n" + "=" * 80)
    print("TEST: Fetch Dividend Data")
    print("=" * 80)

    ticker = "JNJ"  # Johnson & Johnson - known dividend payer
    print(f"\nFetching dividend data for {ticker}...")

    try:
        div = fetch_dividend_data(ticker)
        print(f"\n✓ Success!")
        print(f"  Ticker: {div.ticker}")
        print(f"  Total Dividends Paid: {div.dividend_count}")
        print(f"  Sum of Dividends: ${div.total_dividends:.2f}")
        if div.latest_dividend:
            print(f"  Latest Dividend: ${div.latest_dividend:.2f}")
            print(f"  Latest Dividend Date: {div.latest_dividend_date}")
            print(f"\n  Recent Dividend History:")
            print(div.df.tail())
        return True
    except Exception as e:
        print(f"\n✗ Failed: {e}")
        return False


def test_multiple_prices():
    """Test fetching prices for multiple tickers."""
    print("\n" + "=" * 80)
    print("TEST: Fetch Multiple Prices")
    print("=" * 80)

    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
    print(f"\nFetching prices for {len(tickers)} tickers: {', '.join(tickers)}")

    try:
        prices = fetch_multiple_prices(tickers)
        print(f"\n✓ Success! Retrieved {len(prices)} prices")
        print(f"\n  {'Ticker':<8} {'Price':<12} {'Day High':<12} {'Day Low':<12}")
        print(f"  {'-' * 8} {'-' * 12} {'-' * 12} {'-' * 12}")
        for ticker, price in prices.items():
            print(
                f"  {ticker:<8} ${price.price:<11.2f} ${price.day_high:<11.2f} ${price.day_low:<11.2f}"
            )
        return True
    except Exception as e:
        print(f"\n✗ Failed: {e}")
        return False


def main():
    """Run all market data tests."""
    print("\n" + "=" * 80)
    print("MARKET DATA TOOLS TEST SUITE")
    print("=" * 80)
    print(
        "\nTesting Yahoo Finance integration with real-time market data fetching..."
    )

    tests = [
        ("Current Price", test_current_price),
        ("Historical Data", test_historical_data),
        ("Company Info", test_stock_info),
        ("Dividend Data", test_dividend_data),
        ("Multiple Prices", test_multiple_prices),
    ]

    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n✗ Test '{name}' crashed: {e}")
            results.append((name, False))

    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {status} - {name}")

    print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.0f}%)")

    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())
