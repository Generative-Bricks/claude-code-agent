"""
Unit Tests for Performance Analyst Agent.

Tests cover:
- Return calculations (total and holding-level)
- Sharpe ratio calculation
- Alpha calculation
- Sector attribution
- Top/bottom performer identification
- Performance analysis workflow
"""

import pytest

from src.agents.performance_analyst import (
    calculate_alpha,
    calculate_holding_return,
    calculate_percentile_rank,
    calculate_sector_attribution,
    calculate_sharpe_ratio,
    calculate_total_return,
    identify_bottom_performers,
    identify_top_performers,
    perform_performance_analysis,
)
from src.models.schemas import AssetClass, Holding, Portfolio


# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def positive_return_portfolio():
    """Portfolio with positive returns."""
    return Portfolio(
        portfolio_name="Positive Returns",
        holdings=[
            Holding(
                ticker="AAPL",
                name="Apple Inc.",
                quantity=100,
                value=50000,
                asset_class=AssetClass.equity,
                sector="Technology",
                cost_basis=40000,  # 25% gain
            ),
            Holding(
                ticker="MSFT",
                name="Microsoft",
                quantity=50,
                value=30000,
                asset_class=AssetClass.equity,
                sector="Technology",
                cost_basis=25000,  # 20% gain
            ),
            Holding(
                ticker="JNJ",
                name="Johnson & Johnson",
                quantity=200,
                value=20000,
                asset_class=AssetClass.equity,
                sector="Healthcare",
                cost_basis=18000,  # 11.1% gain
            ),
        ],
    )


@pytest.fixture
def mixed_return_portfolio():
    """Portfolio with mixed returns (winners and losers)."""
    return Portfolio(
        portfolio_name="Mixed Returns",
        holdings=[
            Holding(
                ticker="NVDA",
                name="NVIDIA",
                quantity=100,
                value=60000,
                asset_class=AssetClass.equity,
                sector="Technology",
                cost_basis=30000,  # 100% gain (winner)
            ),
            Holding(
                ticker="WMT",
                name="Walmart",
                quantity=200,
                value=25000,
                asset_class=AssetClass.equity,
                sector="Consumer",
                cost_basis=28000,  # -10.7% loss (loser)
            ),
            Holding(
                ticker="BND",
                name="Total Bond ETF",
                quantity=150,
                value=15000,
                asset_class=AssetClass.bond,
                sector="Fixed Income",
                cost_basis=15000,  # 0% (flat)
            ),
        ],
    )


# ============================================================================
# Test Return Calculations
# ============================================================================


def test_calculate_holding_return_positive():
    """Test holding return calculation with positive return."""
    holding = Holding(
        ticker="AAPL",
        name="Apple",
        quantity=100,
        value=50000,
        asset_class=AssetClass.equity,
        sector="Technology",
        cost_basis=40000,
    )

    return_pct = calculate_holding_return(holding)

    # Should be 25% return
    assert 24.9 <= return_pct <= 25.1


def test_calculate_holding_return_negative():
    """Test holding return calculation with negative return."""
    holding = Holding(
        ticker="LOSS",
        name="Losing Stock",
        quantity=100,
        value=30000,
        asset_class=AssetClass.equity,
        sector="Technology",
        cost_basis=40000,
    )

    return_pct = calculate_holding_return(holding)

    # Should be -25% return
    assert -25.1 <= return_pct <= -24.9


def test_calculate_holding_return_zero():
    """Test holding return calculation with zero return."""
    holding = Holding(
        ticker="FLAT",
        name="Flat Stock",
        quantity=100,
        value=50000,
        asset_class=AssetClass.equity,
        sector="Technology",
        cost_basis=50000,
    )

    return_pct = calculate_holding_return(holding)

    # Should be 0% return
    assert return_pct == 0.0


def test_calculate_total_return(positive_return_portfolio):
    """Test total portfolio return calculation."""
    total_return = calculate_total_return(positive_return_portfolio)

    # Portfolio has gains, should be positive
    assert total_return > 0

    # Calculate expected: (50k + 30k + 20k) / (40k + 25k + 18k) - 1 = 20.48%
    assert 19.0 <= total_return <= 22.0


def test_calculate_total_return_mixed(mixed_return_portfolio):
    """Test total return with mixed gains/losses."""
    total_return = calculate_total_return(mixed_return_portfolio)

    # Overall should still be positive (big winner outweighs loser)
    assert total_return > 0


# ============================================================================
# Test Sharpe Ratio
# ============================================================================


def test_calculate_sharpe_ratio_positive():
    """Test Sharpe ratio with positive return."""
    sharpe = calculate_sharpe_ratio(total_return=15.0)  # 15% return

    # With 15% return and typical volatility, Sharpe should be positive
    assert sharpe > 0


def test_calculate_sharpe_ratio_negative():
    """Test Sharpe ratio with negative return."""
    sharpe = calculate_sharpe_ratio(total_return=-5.0)  # -5% return

    # Negative return should give negative Sharpe ratio
    assert sharpe < 0


def test_calculate_sharpe_ratio_zero():
    """Test Sharpe ratio with zero return."""
    sharpe = calculate_sharpe_ratio(total_return=0.0)

    # Zero return should give negative Sharpe (below risk-free rate)
    assert sharpe < 0


# ============================================================================
# Test Alpha Calculation
# ============================================================================


def test_calculate_alpha_outperformance():
    """Test alpha calculation when portfolio outperforms benchmark."""
    alpha = calculate_alpha(
        portfolio_return=20.0,  # 20% return
        benchmark_return=10.0,  # 10% benchmark
    )

    # Alpha should be positive (outperformance)
    assert alpha > 0
    assert 9.0 <= alpha <= 11.0  # Should be around 10%


def test_calculate_alpha_underperformance():
    """Test alpha calculation when portfolio underperforms benchmark."""
    alpha = calculate_alpha(
        portfolio_return=5.0,  # 5% return
        benchmark_return=10.0,  # 10% benchmark
    )

    # Alpha should be negative (underperformance)
    assert alpha < 0
    assert -6.0 <= alpha <= -4.0  # Should be around -5%


def test_calculate_alpha_match():
    """Test alpha when portfolio matches benchmark."""
    alpha = calculate_alpha(
        portfolio_return=10.0,  # 10% return
        benchmark_return=10.0,  # 10% benchmark
    )

    # Alpha should be near zero
    assert -1.0 <= alpha <= 1.0


# ============================================================================
# Test Sector Attribution
# ============================================================================


def test_calculate_sector_attribution_single_sector():
    """Test sector attribution with single sector."""
    portfolio = Portfolio(
        portfolio_name="Single Sector",
        holdings=[
            Holding(
                ticker="AAPL",
                name="Apple",
                quantity=100,
                value=50000,
                asset_class=AssetClass.equity,
                sector="Technology",
            ),
            Holding(
                ticker="MSFT",
                name="Microsoft",
                quantity=50,
                value=50000,
                asset_class=AssetClass.equity,
                sector="Technology",
            ),
        ],
    )

    attribution = calculate_sector_attribution(portfolio)

    # Should have one sector with 100% allocation
    assert len(attribution) == 1
    assert "Technology" in attribution
    assert attribution["Technology"] == 100.0


def test_calculate_sector_attribution_multiple_sectors(positive_return_portfolio):
    """Test sector attribution with multiple sectors."""
    attribution = calculate_sector_attribution(positive_return_portfolio)

    # Should have Technology and Healthcare sectors
    assert "Technology" in attribution
    assert "Healthcare" in attribution

    # Technology should be 80% (80k / 100k), Healthcare 20%
    assert 79.0 <= attribution["Technology"] <= 81.0
    assert 19.0 <= attribution["Healthcare"] <= 21.0

    # Total should sum to 100%
    total = sum(attribution.values())
    assert 99.0 <= total <= 101.0


# ============================================================================
# Test Top/Bottom Performers
# ============================================================================


def test_identify_top_performers(positive_return_portfolio):
    """Test identification of top performing holdings."""
    top_performers = identify_top_performers(positive_return_portfolio, top_n=2)

    # Should return 2 holdings
    assert len(top_performers) == 2

    # First should be AAPL (25% return)
    assert top_performers[0][0].ticker == "AAPL"
    assert 24.0 <= top_performers[0][1] <= 26.0

    # Second should be MSFT (20% return)
    assert top_performers[1][0].ticker == "MSFT"
    assert 19.0 <= top_performers[1][1] <= 21.0


def test_identify_bottom_performers(mixed_return_portfolio):
    """Test identification of bottom performing holdings."""
    bottom_performers = identify_bottom_performers(mixed_return_portfolio, bottom_n=2)

    # Should return 2 holdings
    assert len(bottom_performers) == 2

    # First (worst) should be WMT (-10.7% loss)
    assert bottom_performers[0][0].ticker == "WMT"
    assert bottom_performers[0][1] < 0

    # Second should be BND (0% flat)
    assert bottom_performers[1][0].ticker == "BND"
    assert bottom_performers[1][1] == 0.0


def test_top_performers_all_holdings():
    """Test top performers when requesting more than available."""
    portfolio = Portfolio(
        portfolio_name="Small",
        holdings=[
            Holding(
                ticker="AAPL",
                name="Apple",
                quantity=100,
                value=50000,
                asset_class=AssetClass.equity,
                sector="Technology",
                cost_basis=40000,
            )
        ],
    )

    top_performers = identify_top_performers(portfolio, top_n=5)

    # Should return only available holdings (1)
    assert len(top_performers) == 1


# ============================================================================
# Test Percentile Rank
# ============================================================================


def test_calculate_percentile_rank():
    """Test percentile rank calculation."""
    rank = calculate_percentile_rank(portfolio_return=15.0, benchmark_return=10.0)

    # 15% vs 10% should give a percentile above 50
    assert rank > 50
    assert rank <= 100


def test_calculate_percentile_rank_underperform():
    """Test percentile rank when underperforming."""
    rank = calculate_percentile_rank(portfolio_return=5.0, benchmark_return=10.0)

    # Underperformance should give percentile below 50
    assert rank < 50
    assert rank >= 0


# ============================================================================
# Test Complete Performance Analysis
# ============================================================================


def test_perform_performance_analysis_basic(positive_return_portfolio):
    """Test complete performance analysis with positive returns."""
    report = perform_performance_analysis(positive_return_portfolio, benchmark="SPY")

    # Verify all fields are populated
    assert report.total_return > 0
    assert report.sharpe_ratio is not None
    assert report.alpha is not None
    assert len(report.sector_attribution) > 0
    assert len(report.top_performers) > 0
    assert len(report.bottom_performers) > 0
    assert 0 <= report.percentile_rank <= 100


def test_perform_performance_analysis_mixed(mixed_return_portfolio):
    """Test performance analysis with mixed returns."""
    report = perform_performance_analysis(mixed_return_portfolio, benchmark="SPY")

    # Should still produce valid report
    assert report.total_return is not None
    assert len(report.top_performers) > 0
    assert len(report.bottom_performers) > 0

    # Top performer should be NVDA (100% gain)
    assert report.top_performers[0][0].ticker == "NVDA"

    # Bottom performer should be WMT (loss)
    assert report.bottom_performers[0][0].ticker == "WMT"


def test_performance_analysis_consistency():
    """Test that performance analysis is consistent across runs."""
    portfolio = Portfolio(
        portfolio_name="Consistent",
        holdings=[
            Holding(
                ticker="SPY",
                name="S&P 500",
                quantity=100,
                value=50000,
                asset_class=AssetClass.equity,
                sector="Diversified",
                cost_basis=45000,
            ),
            Holding(
                ticker="BND",
                name="Bonds",
                quantity=500,
                value=50000,
                asset_class=AssetClass.bond,
                sector="Fixed Income",
                cost_basis=48000,
            ),
        ],
    )

    # Run analysis twice
    report1 = perform_performance_analysis(portfolio)
    report2 = perform_performance_analysis(portfolio)

    # Results should be identical
    assert report1.total_return == report2.total_return
    assert report1.sharpe_ratio == report2.sharpe_ratio
    assert report1.alpha == report2.alpha
    assert report1.percentile_rank == report2.percentile_rank


# ============================================================================
# Test Edge Cases
# ============================================================================


def test_performance_analysis_no_cost_basis():
    """Test performance analysis when holdings lack cost basis."""
    portfolio = Portfolio(
        portfolio_name="No Cost Basis",
        holdings=[
            Holding(
                ticker="AAPL",
                name="Apple",
                quantity=100,
                value=50000,
                asset_class=AssetClass.equity,
                sector="Technology",
                # No cost_basis provided
            )
        ],
    )

    # Should handle gracefully (assume 0% return or skip return calculation)
    report = perform_performance_analysis(portfolio)

    # Should still produce a report
    assert report is not None


def test_performance_analysis_empty_portfolio():
    """Test performance analysis with empty portfolio."""
    empty_portfolio = Portfolio(portfolio_name="Empty", holdings=[])

    # Should handle gracefully or raise appropriate error
    with pytest.raises(Exception):
        perform_performance_analysis(empty_portfolio)


def test_holding_return_zero_cost_basis():
    """Test holding return with zero cost basis."""
    holding = Holding(
        ticker="TEST",
        name="Test",
        quantity=100,
        value=50000,
        asset_class=AssetClass.equity,
        sector="Technology",
        cost_basis=0,
    )

    # Should handle division by zero gracefully
    with pytest.raises(Exception):
        calculate_holding_return(holding)
