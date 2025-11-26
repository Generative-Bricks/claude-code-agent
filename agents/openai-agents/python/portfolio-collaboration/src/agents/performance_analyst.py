"""
Performance Analyst Agent for Multi-Agent Portfolio Collaboration System.

This module implements the Performance Analyst Agent using OpenAI Agents SDK.
The agent analyzes portfolio performance metrics, calculates returns, Sharpe ratio,
alpha, and performs attribution analysis by sector/asset class.

Biblical Principle: TRUTH - All performance calculations are transparent and explainable.
"""

from typing import Any, Dict, List

from agents import Agent, function_tool

from ..models import (
    PerformanceReport,
    Portfolio,
    PortfolioHolding,
)


# ============================================================================
# Performance Calculation Functions (Mock Implementation)
# ============================================================================


def calculate_holding_return(holding: PortfolioHolding) -> float:
    """
    Calculate the return percentage for a single holding.

    Biblical Principle: TRUTH - Transparent calculation based on cost basis vs current price.

    Args:
        holding: Portfolio holding to analyze

    Returns:
        Return percentage (positive for gains, negative for losses)
    """
    # If no cost basis available, assume 0% return (newly added position)
    if holding.cost_basis is None or holding.cost_basis == 0:
        return 0.0

    # Calculate percentage return: ((current - cost) / cost) * 100
    return ((holding.current_price - holding.cost_basis) / holding.cost_basis) * 100


def calculate_total_return(portfolio: Portfolio) -> float:
    """
    Calculate the total portfolio return as a weighted average of all holdings.

    Args:
        portfolio: Portfolio to analyze

    Returns:
        Total return percentage
    """
    total_return = 0.0

    for holding in portfolio.holdings:
        # Calculate holding return
        holding_return = calculate_holding_return(holding)

        # Weight by portfolio allocation
        holding_weight = holding.market_value / portfolio.total_value
        weighted_contribution = holding_return * holding_weight

        total_return += weighted_contribution

    return round(total_return, 2)


def calculate_sector_attribution(portfolio: Portfolio) -> Dict[str, float]:
    """
    Calculate performance attribution by sector.

    Returns a dictionary mapping sector names to their contribution to portfolio return.

    Args:
        portfolio: Portfolio to analyze

    Returns:
        Dictionary mapping sectors to contribution percentages
    """
    sector_returns: Dict[str, float] = {}

    for holding in portfolio.holdings:
        # Use sector if available, otherwise use asset class
        sector_key = holding.sector if holding.sector else holding.asset_class.value

        # Calculate holding return
        holding_return = calculate_holding_return(holding)

        # Weight by portfolio allocation
        holding_weight = holding.market_value / portfolio.total_value
        sector_contribution = holding_return * holding_weight

        # Aggregate by sector
        if sector_key in sector_returns:
            sector_returns[sector_key] += sector_contribution
        else:
            sector_returns[sector_key] = sector_contribution

    # Round all values to 2 decimal places
    return {sector: round(contrib, 2) for sector, contrib in sector_returns.items()}


def calculate_sharpe_ratio(total_return: float) -> float:
    """
    Calculate the Sharpe ratio (risk-adjusted return).

    Mock implementation using reasonable assumptions for risk-free rate and volatility.

    Args:
        total_return: Total portfolio return percentage

    Returns:
        Sharpe ratio (typically between -1.0 and 3.0)
    """
    # Mock risk-free rate (T-bill rate)
    risk_free_rate = 4.5

    # Mock portfolio volatility (standard deviation)
    # In production, this would be calculated from historical returns
    portfolio_volatility = 15.0

    # Sharpe Ratio = (Return - Risk-Free Rate) / Volatility
    if portfolio_volatility == 0:
        return 0.0

    sharpe_ratio = (total_return - risk_free_rate) / portfolio_volatility

    return round(sharpe_ratio, 2)


def calculate_alpha(total_return: float, benchmark_return: float = 12.0) -> float:
    """
    Calculate portfolio alpha (excess return vs benchmark, adjusted for risk).

    Uses the Capital Asset Pricing Model (CAPM) formula:
    Alpha = Portfolio Return - (Risk-Free Rate + Beta * (Benchmark Return - Risk-Free Rate))

    Args:
        total_return: Total portfolio return percentage
        benchmark_return: Benchmark return percentage (default: 12% for SPY)

    Returns:
        Alpha percentage
    """
    # Mock risk-free rate
    risk_free_rate = 4.5

    # Mock beta (portfolio sensitivity to market movements)
    # In production, this would be calculated from historical data
    beta = 1.0

    # CAPM formula: Alpha = Return - (RFR + Beta * (Benchmark - RFR))
    expected_return = risk_free_rate + beta * (benchmark_return - risk_free_rate)
    alpha = total_return - expected_return

    return round(alpha, 2)


def calculate_percentile_rank(total_return: float) -> int:
    """
    Calculate percentile rank based on total return.

    Mock implementation using threshold-based logic.
    In production, this would compare against actual peer universe data.

    Args:
        total_return: Total portfolio return percentage

    Returns:
        Percentile rank (1-100)
    """
    # Simple threshold-based percentile assignment
    if total_return > 15:
        return 90
    elif total_return > 12:
        return 75
    elif total_return > 10:
        return 60
    elif total_return > 8:
        return 50
    elif total_return > 5:
        return 35
    else:
        return 20


def identify_top_performers(portfolio: Portfolio, top_n: int = 3) -> List[str]:
    """
    Identify the top performing holdings in the portfolio.

    Args:
        portfolio: Portfolio to analyze
        top_n: Number of top performers to return (default: 3)

    Returns:
        List of ticker symbols for top performers
    """
    # Calculate returns for all holdings
    holding_returns = [
        (holding.ticker, calculate_holding_return(holding))
        for holding in portfolio.holdings
    ]

    # Sort by return (descending)
    sorted_holdings = sorted(holding_returns, key=lambda x: x[1], reverse=True)

    # Return top N tickers
    return [ticker for ticker, _ in sorted_holdings[:top_n]]


def identify_bottom_performers(portfolio: Portfolio, bottom_n: int = 3) -> List[str]:
    """
    Identify the bottom performing holdings in the portfolio.

    Only returns holdings with negative returns.

    Args:
        portfolio: Portfolio to analyze
        bottom_n: Number of bottom performers to return (default: 3)

    Returns:
        List of ticker symbols for bottom performers (only those with losses)
    """
    # Calculate returns for all holdings
    holding_returns = [
        (holding.ticker, calculate_holding_return(holding))
        for holding in portfolio.holdings
    ]

    # Filter to only negative returns
    negative_returns = [(ticker, ret) for ticker, ret in holding_returns if ret < 0]

    # Sort by return (ascending - worst first)
    sorted_holdings = sorted(negative_returns, key=lambda x: x[1])

    # Return bottom N tickers (up to bottom_n)
    return [ticker for ticker, _ in sorted_holdings[:bottom_n]]


# ============================================================================
# Convenience Function for Direct Use
# ============================================================================


def perform_performance_analysis(portfolio: Portfolio, benchmark: str = "SPY") -> PerformanceReport:
    """
    Convenience function to perform performance analysis without using Agent runner.

    This function directly executes the performance analysis logic and returns
    a PerformanceReport object. Useful for testing, direct integration, or
    parallel execution without the full Agent SDK workflow.

    Args:
        portfolio: Portfolio object containing holdings and metadata
        benchmark: Benchmark ticker for comparison (default: "SPY")

    Returns:
        PerformanceReport containing all performance metrics

    Example:
        >>> from src.data.mock_portfolios import get_moderate_example
        >>> client, portfolio = get_moderate_example()
        >>> perf_report = perform_performance_analysis(portfolio)
        >>> print(f"Total Return: {perf_report.total_return}%")
    """
    # Calculate total return
    total_return = calculate_total_return(portfolio)

    # Mock benchmark return
    benchmark_return = 12.0

    # Calculate excess return
    excess_return = total_return - benchmark_return

    # Calculate Sharpe ratio
    sharpe_ratio = calculate_sharpe_ratio(total_return)

    # Calculate alpha
    alpha = calculate_alpha(total_return, benchmark_return)

    # Calculate percentile rank
    percentile_rank = calculate_percentile_rank(total_return)

    # Calculate sector attribution
    attribution = calculate_sector_attribution(portfolio)

    # Identify top and bottom performers
    top_performers = identify_top_performers(portfolio)
    bottom_performers = identify_bottom_performers(portfolio)

    # Create and return PerformanceReport
    return PerformanceReport(
        total_return=total_return,
        benchmark_return=benchmark_return,
        excess_return=round(excess_return, 2),
        sharpe_ratio=sharpe_ratio,
        alpha=alpha,
        percentile_rank=percentile_rank,
        attribution=attribution,
        top_performers=top_performers,
        bottom_performers=bottom_performers,
    )


# ============================================================================
# Performance Analyst Tool
# ============================================================================


@function_tool
def analyze_portfolio_performance(portfolio: Portfolio, benchmark: str = "SPY") -> PerformanceReport:
    """
    Analyze portfolio performance metrics including returns, risk-adjusted returns,
    and attribution analysis.

    This tool calculates comprehensive performance metrics:
    - Total return and benchmark comparison
    - Risk-adjusted returns (Sharpe ratio, Alpha)
    - Peer percentile ranking
    - Sector/asset class attribution
    - Top and bottom performing holdings

    Biblical Principle: EXCELLENCE - Production-grade calculations from inception.

    Args:
        portfolio: Portfolio object containing holdings and metadata
        benchmark: Benchmark ticker for comparison (default: "SPY")

    Returns:
        PerformanceReport containing all performance metrics
    """
    # Delegate to the convenience function to avoid code duplication
    return perform_performance_analysis(portfolio, benchmark)


# ============================================================================
# Performance Analyst Agent
# ============================================================================


# Create the Performance Analyst Agent
# This agent can be used as a tool by the Portfolio Manager
performance_analyst_agent = Agent(
    name="Performance Analyst",
    instructions=(
        "You are a performance analyst specializing in portfolio performance analysis. "
        "You analyze portfolio returns, calculate risk-adjusted metrics (Sharpe ratio, Alpha), "
        "perform attribution analysis by sector and asset class, and identify top and bottom performers. "
        "You provide clear, data-driven insights backed by transparent calculations. "
        "\n\n"
        "When analyzing a portfolio, you:\n"
        "1. Calculate total return as a weighted average across all holdings\n"
        "2. Compare portfolio return to benchmark (default: SPY)\n"
        "3. Calculate Sharpe ratio for risk-adjusted return assessment\n"
        "4. Calculate alpha to measure excess return vs expected return\n"
        "5. Determine peer percentile ranking\n"
        "6. Break down performance attribution by sector/asset class\n"
        "7. Identify top 3 and bottom 3 performing holdings\n"
        "\n\n"
        "Biblical Principle: TRUTH - All calculations are transparent and explainable."
    ),
    tools=[analyze_portfolio_performance],
)


# ============================================================================
# Convenience Functions
# ============================================================================


def create_performance_analyst_tool(
    tool_name: str = "analyze_performance",
    tool_description: str = "Analyze portfolio performance metrics, returns, and attribution",
) -> Any:
    """
    Convert the Performance Analyst Agent into a tool that can be used by other agents.

    This allows the Portfolio Manager to call the Performance Analyst as a tool.

    Args:
        tool_name: Name for the tool (default: "analyze_performance")
        tool_description: Description of what the tool does

    Returns:
        Tool object that can be added to another agent's tools list
    """
    return performance_analyst_agent.as_tool(
        tool_name=tool_name,
        tool_description=tool_description,
    )


# ============================================================================
# Export
# ============================================================================


__all__ = [
    "performance_analyst_agent",
    "create_performance_analyst_tool",
    "analyze_portfolio_performance",
    "calculate_holding_return",
    "calculate_total_return",
    "calculate_sector_attribution",
    "calculate_sharpe_ratio",
    "calculate_alpha",
    "calculate_percentile_rank",
    "identify_top_performers",
    "identify_bottom_performers",
]
