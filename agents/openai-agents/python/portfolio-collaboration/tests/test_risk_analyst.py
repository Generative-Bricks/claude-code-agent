"""
Unit Tests for Risk Analyst Agent.

Tests cover:
- Risk calculation functions (volatility, VaR, beta, concentration)
- Risk rating classification
- Portfolio risk analysis
- Edge cases and error handling
"""

import pytest

from src.agents.risk_analyst import (
    calculate_beta,
    calculate_concentration_score,
    calculate_var_95,
    calculate_volatility,
    classify_risk_rating,
    perform_risk_analysis,
)
from src.models.schemas import (
    AssetClass,
    ClientProfile,
    Holding,
    Portfolio,
    RiskRating,
    RiskTolerance,
)


# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def conservative_client():
    """Conservative client profile fixture."""
    return ClientProfile(
        client_id="TEST-001",
        name="John Conservative",
        age=68,
        risk_tolerance=RiskTolerance.conservative,
        investment_goals=["income", "capital_preservation"],
        time_horizon_years=5,
        income_needs=50000,
    )


@pytest.fixture
def aggressive_client():
    """Aggressive client profile fixture."""
    return ClientProfile(
        client_id="TEST-002",
        name="Jane Aggressive",
        age=32,
        risk_tolerance=RiskTolerance.aggressive,
        investment_goals=["growth", "wealth_accumulation"],
        time_horizon_years=30,
    )


@pytest.fixture
def diversified_portfolio():
    """Well-diversified portfolio fixture."""
    return Portfolio(
        portfolio_name="Diversified Portfolio",
        holdings=[
            Holding(
                ticker="SPY",
                name="SPDR S&P 500 ETF",
                quantity=100,
                value=45000,
                asset_class=AssetClass.equity,
                sector="Diversified",
            ),
            Holding(
                ticker="BND",
                name="Vanguard Total Bond ETF",
                quantity=500,
                value=35000,
                asset_class=AssetClass.bond,
                sector="Fixed Income",
            ),
            Holding(
                ticker="VNQ",
                name="Vanguard Real Estate ETF",
                quantity=200,
                value=20000,
                asset_class=AssetClass.real_estate,
                sector="Real Estate",
            ),
        ],
    )


@pytest.fixture
def concentrated_portfolio():
    """Highly concentrated portfolio fixture."""
    return Portfolio(
        portfolio_name="Concentrated Portfolio",
        holdings=[
            Holding(
                ticker="AAPL",
                name="Apple Inc.",
                quantity=500,
                value=85000,
                asset_class=AssetClass.equity,
                sector="Technology",
            ),
            Holding(
                ticker="MSFT",
                name="Microsoft Corporation",
                quantity=50,
                value=15000,
                asset_class=AssetClass.equity,
                sector="Technology",
            ),
        ],
    )


# ============================================================================
# Test Volatility Calculation
# ============================================================================


def test_calculate_volatility_diversified(diversified_portfolio):
    """Test volatility calculation with diversified portfolio."""
    volatility = calculate_volatility(diversified_portfolio)

    # Volatility should be a positive number (percentage)
    assert volatility > 0
    assert volatility < 100  # Should be reasonable (less than 100%)

    # Diversified portfolio should have moderate volatility
    assert 5 <= volatility <= 25  # Typically 5-25% for balanced portfolios


def test_calculate_volatility_concentrated(concentrated_portfolio):
    """Test volatility calculation with concentrated portfolio."""
    volatility = calculate_volatility(concentrated_portfolio)

    # Concentrated equity portfolio should have higher volatility
    assert volatility > 0
    assert volatility >= 15  # Should be at least 15% for concentrated equities


# ============================================================================
# Test VaR Calculation
# ============================================================================


def test_calculate_var_95(diversified_portfolio):
    """Test Value at Risk (95% confidence) calculation."""
    volatility = calculate_volatility(diversified_portfolio)
    var_95 = calculate_var_95(diversified_portfolio, volatility)

    # VaR should be a positive dollar amount
    assert var_95 > 0

    # VaR should be less than total portfolio value
    total_value = sum(h.value for h in diversified_portfolio.holdings)
    assert var_95 < total_value

    # For 95% VaR, typically 10-20% of portfolio value for moderate risk
    assert var_95 < total_value * 0.5  # Should be less than 50% of portfolio


def test_var_increases_with_volatility():
    """Test that VaR increases as volatility increases."""
    portfolio = Portfolio(
        portfolio_name="Test",
        holdings=[
            Holding(
                ticker="TEST",
                name="Test Stock",
                quantity=100,
                value=100000,
                asset_class=AssetClass.equity,
                sector="Technology",
            )
        ],
    )

    # Calculate VaR with different volatilities
    var_low = calculate_var_95(portfolio, volatility=10.0)
    var_medium = calculate_var_95(portfolio, volatility=20.0)
    var_high = calculate_var_95(portfolio, volatility=30.0)

    # VaR should increase with volatility
    assert var_low < var_medium < var_high


# ============================================================================
# Test Beta Calculation
# ============================================================================


def test_calculate_beta_equity_portfolio():
    """Test beta calculation for equity portfolio."""
    portfolio = Portfolio(
        portfolio_name="Equity Portfolio",
        holdings=[
            Holding(
                ticker="SPY",
                name="S&P 500 ETF",
                quantity=100,
                value=100000,
                asset_class=AssetClass.equity,
                sector="Diversified",
            )
        ],
    )

    beta = calculate_beta(portfolio)

    # Beta should be close to 1.0 for S&P 500 ETF
    assert beta is not None
    assert 0.8 <= beta <= 1.2  # Should be close to market beta


def test_calculate_beta_bond_portfolio():
    """Test beta calculation for bond portfolio."""
    portfolio = Portfolio(
        portfolio_name="Bond Portfolio",
        holdings=[
            Holding(
                ticker="BND",
                name="Total Bond ETF",
                quantity=1000,
                value=100000,
                asset_class=AssetClass.bond,
                sector="Fixed Income",
            )
        ],
    )

    beta = calculate_beta(portfolio)

    # Bonds should have low beta
    assert beta is not None
    assert beta < 0.5  # Should be significantly less than 1.0


# ============================================================================
# Test Concentration Score
# ============================================================================


def test_concentration_score_diversified(diversified_portfolio):
    """Test concentration score with well-diversified portfolio."""
    concentration = calculate_concentration_score(diversified_portfolio)

    # Concentration should be low for diversified portfolio
    assert 0 <= concentration <= 100
    assert concentration < 60  # Should be less than 60 for good diversification


def test_concentration_score_concentrated(concentrated_portfolio):
    """Test concentration score with concentrated portfolio."""
    concentration = calculate_concentration_score(concentrated_portfolio)

    # Concentration should be high for concentrated portfolio
    assert 0 <= concentration <= 100
    assert concentration > 60  # Should be above 60 for concentrated portfolio


def test_concentration_score_single_holding():
    """Test concentration score with single holding (max concentration)."""
    portfolio = Portfolio(
        portfolio_name="Single Holding",
        holdings=[
            Holding(
                ticker="AAPL",
                name="Apple Inc.",
                quantity=100,
                value=100000,
                asset_class=AssetClass.equity,
                sector="Technology",
            )
        ],
    )

    concentration = calculate_concentration_score(portfolio)

    # Single holding should have maximum concentration
    assert concentration == 100


# ============================================================================
# Test Risk Rating Classification
# ============================================================================


def test_classify_risk_rating_low():
    """Test risk rating classification for low volatility."""
    rating = classify_risk_rating(volatility=8.0)
    assert rating == RiskRating.low


def test_classify_risk_rating_medium():
    """Test risk rating classification for medium volatility."""
    rating = classify_risk_rating(volatility=15.0)
    assert rating == RiskRating.medium


def test_classify_risk_rating_high():
    """Test risk rating classification for high volatility."""
    rating = classify_risk_rating(volatility=25.0)
    assert rating == RiskRating.high


def test_classify_risk_rating_boundary_cases():
    """Test risk rating at boundary values."""
    # Just below medium threshold
    assert classify_risk_rating(volatility=11.99) == RiskRating.low

    # Exactly at medium threshold
    assert classify_risk_rating(volatility=12.0) == RiskRating.medium

    # Just below high threshold
    assert classify_risk_rating(volatility=19.99) == RiskRating.medium

    # Exactly at high threshold
    assert classify_risk_rating(volatility=20.0) == RiskRating.high


# ============================================================================
# Test Complete Risk Analysis
# ============================================================================


def test_perform_risk_analysis_basic(diversified_portfolio):
    """Test complete risk analysis with basic portfolio."""
    risk_analysis = perform_risk_analysis(diversified_portfolio)

    # Verify all fields are populated
    assert risk_analysis.volatility > 0
    assert risk_analysis.var_95 > 0
    assert risk_analysis.beta is not None
    assert 0 <= risk_analysis.concentration_score <= 100
    assert risk_analysis.risk_rating in [
        RiskRating.low,
        RiskRating.medium,
        RiskRating.high,
    ]
    assert len(risk_analysis.risk_factors) > 0


def test_perform_risk_analysis_with_client(diversified_portfolio, conservative_client):
    """Test risk analysis with client profile."""
    risk_analysis = perform_risk_analysis(diversified_portfolio, conservative_client)

    # Should include client-specific risk factors
    assert len(risk_analysis.risk_factors) > 0

    # For conservative client, check if age-related factors are included
    if conservative_client.age > 60:
        risk_factors_text = " ".join(risk_analysis.risk_factors).lower()
        assert "time horizon" in risk_factors_text or "age" in risk_factors_text


def test_risk_analysis_concentrated_portfolio(
    concentrated_portfolio, aggressive_client
):
    """Test risk analysis identifies concentration risk."""
    risk_analysis = perform_risk_analysis(concentrated_portfolio, aggressive_client)

    # Should flag high concentration
    assert risk_analysis.concentration_score > 60

    # Risk factors should mention concentration
    risk_factors_text = " ".join(risk_analysis.risk_factors).lower()
    assert "concentration" in risk_factors_text or "diversif" in risk_factors_text


def test_risk_analysis_consistency():
    """Test that risk analysis produces consistent results."""
    portfolio = Portfolio(
        portfolio_name="Consistent Test",
        holdings=[
            Holding(
                ticker="SPY",
                name="S&P 500",
                quantity=100,
                value=50000,
                asset_class=AssetClass.equity,
                sector="Diversified",
            ),
            Holding(
                ticker="BND",
                name="Bonds",
                quantity=500,
                value=50000,
                asset_class=AssetClass.bond,
                sector="Fixed Income",
            ),
        ],
    )

    # Run analysis multiple times
    result1 = perform_risk_analysis(portfolio)
    result2 = perform_risk_analysis(portfolio)

    # Results should be identical
    assert result1.volatility == result2.volatility
    assert result1.var_95 == result2.var_95
    assert result1.beta == result2.beta
    assert result1.concentration_score == result2.concentration_score
    assert result1.risk_rating == result2.risk_rating


# ============================================================================
# Test Edge Cases
# ============================================================================


def test_empty_portfolio_handling():
    """Test handling of empty portfolio."""
    empty_portfolio = Portfolio(portfolio_name="Empty", holdings=[])

    # Should handle gracefully (though this shouldn't happen in practice)
    with pytest.raises(Exception):
        # Empty portfolio should raise an error or return default values
        perform_risk_analysis(empty_portfolio)


def test_zero_value_holdings():
    """Test handling of holdings with zero value."""
    portfolio = Portfolio(
        portfolio_name="Zero Value Test",
        holdings=[
            Holding(
                ticker="TEST",
                name="Test",
                quantity=0,
                value=0,
                asset_class=AssetClass.equity,
                sector="Technology",
            )
        ],
    )

    # Should handle gracefully
    with pytest.raises(Exception):
        perform_risk_analysis(portfolio)


def test_negative_volatility_input():
    """Test that negative volatility is handled properly."""
    # This shouldn't happen, but test error handling
    with pytest.raises(Exception):
        classify_risk_rating(volatility=-5.0)
