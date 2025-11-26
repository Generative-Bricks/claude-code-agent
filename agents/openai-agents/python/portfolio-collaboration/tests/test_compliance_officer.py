"""
Unit Tests for Compliance Officer Agent.

Tests cover:
- Suitability checks
- Concentration limit compliance
- Required disclosures
- Overall compliance assessment
"""

import pytest

from src.agents.compliance_officer import (
    analyze_compliance,
    calculate_bond_percentage,
    check_concentration_limits,
    check_suitability,
    get_largest_holding_percentage,
    identify_required_disclosures,
)
from src.models.schemas import (
    AssetClass,
    ClientProfile,
    ComplianceStatus,
    Holding,
    Portfolio,
    RiskTolerance,
)


# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def conservative_client():
    """Conservative 68-year-old client."""
    return ClientProfile(
        client_id="COMP-001",
        name="Conservative Senior",
        age=68,
        risk_tolerance=RiskTolerance.conservative,
        investment_goals=["income", "capital_preservation"],
        time_horizon_years=5,
        income_needs=60000,
    )


@pytest.fixture
def aggressive_young_client():
    """Aggressive 32-year-old client."""
    return ClientProfile(
        client_id="COMP-002",
        name="Aggressive Youth",
        age=32,
        risk_tolerance=RiskTolerance.aggressive,
        investment_goals=["growth", "wealth_accumulation"],
        time_horizon_years=30,
    )


@pytest.fixture
def balanced_portfolio():
    """Balanced 60/40 equity/bond portfolio."""
    return Portfolio(
        portfolio_name="Balanced",
        holdings=[
            Holding(
                ticker="SPY",
                name="S&P 500 ETF",
                quantity=150,
                value=60000,
                asset_class=AssetClass.equity,
                sector="Diversified",
            ),
            Holding(
                ticker="BND",
                name="Total Bond ETF",
                quantity=400,
                value=40000,
                asset_class=AssetClass.bond,
                sector="Fixed Income",
            ),
        ],
    )


@pytest.fixture
def aggressive_portfolio():
    """100% equity portfolio."""
    return Portfolio(
        portfolio_name="Aggressive",
        holdings=[
            Holding(
                ticker="AAPL",
                name="Apple Inc.",
                quantity=200,
                value=35000,
                asset_class=AssetClass.equity,
                sector="Technology",
            ),
            Holding(
                ticker="NVDA",
                name="NVIDIA Corporation",
                quantity=150,
                value=65000,
                asset_class=AssetClass.equity,
                sector="Technology",
            ),
        ],
    )


@pytest.fixture
def concentrated_portfolio():
    """Highly concentrated single-stock portfolio."""
    return Portfolio(
        portfolio_name="Concentrated",
        holdings=[
            Holding(
                ticker="TSLA",
                name="Tesla Inc.",
                quantity=400,
                value=90000,
                asset_class=AssetClass.equity,
                sector="Technology",
            ),
            Holding(
                ticker="BND",
                name="Bonds",
                quantity=100,
                value=10000,
                asset_class=AssetClass.bond,
                sector="Fixed Income",
            ),
        ],
    )


# ============================================================================
# Test Bond Percentage Calculation
# ============================================================================


def test_calculate_bond_percentage_balanced(balanced_portfolio):
    """Test bond percentage calculation with 60/40 portfolio."""
    bond_pct = calculate_bond_percentage(balanced_portfolio)

    # Should be 40% bonds
    assert 39.0 <= bond_pct <= 41.0  # Allow small floating point variance


def test_calculate_bond_percentage_all_equity(aggressive_portfolio):
    """Test bond percentage with 100% equity portfolio."""
    bond_pct = calculate_bond_percentage(aggressive_portfolio)

    # Should be 0% bonds
    assert bond_pct == 0.0


def test_calculate_bond_percentage_all_bonds():
    """Test bond percentage with 100% bond portfolio."""
    portfolio = Portfolio(
        portfolio_name="All Bonds",
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

    bond_pct = calculate_bond_percentage(portfolio)

    # Should be 100% bonds
    assert bond_pct == 100.0


# ============================================================================
# Test Largest Holding Percentage
# ============================================================================


def test_get_largest_holding_percentage_balanced(balanced_portfolio):
    """Test largest holding percentage with balanced portfolio."""
    largest_pct = get_largest_holding_percentage(balanced_portfolio)

    # Largest should be 60% (SPY)
    assert 59.0 <= largest_pct <= 61.0


def test_get_largest_holding_percentage_concentrated(concentrated_portfolio):
    """Test largest holding percentage with concentrated portfolio."""
    largest_pct = get_largest_holding_percentage(concentrated_portfolio)

    # Largest should be 90% (TSLA)
    assert 89.0 <= largest_pct <= 91.0


def test_get_largest_holding_single_stock():
    """Test largest holding percentage with single stock."""
    portfolio = Portfolio(
        portfolio_name="Single",
        holdings=[
            Holding(
                ticker="AAPL",
                name="Apple",
                quantity=100,
                value=100000,
                asset_class=AssetClass.equity,
                sector="Technology",
            )
        ],
    )

    largest_pct = get_largest_holding_percentage(portfolio)

    # Should be 100%
    assert largest_pct == 100.0


# ============================================================================
# Test Suitability Checks
# ============================================================================


def test_check_suitability_conservative_match(conservative_client, balanced_portfolio):
    """Test suitability check for well-matched conservative client."""
    is_suitable, reason = check_suitability(balanced_portfolio, conservative_client)

    # Conservative client with 40% bonds should be suitable
    assert is_suitable is True
    assert "suitable" in reason.lower()


def test_check_suitability_conservative_mismatch(
    conservative_client, aggressive_portfolio
):
    """Test suitability check for mismatched conservative client."""
    is_suitable, reason = check_suitability(aggressive_portfolio, conservative_client)

    # Conservative senior with 0% bonds should NOT be suitable
    assert is_suitable is False
    assert "bond" in reason.lower() or "conservative" in reason.lower()


def test_check_suitability_aggressive_match(
    aggressive_young_client, aggressive_portfolio
):
    """Test suitability check for matched aggressive client."""
    is_suitable, reason = check_suitability(aggressive_portfolio, aggressive_young_client)

    # Young aggressive client with 100% equity should be suitable
    assert is_suitable is True
    assert "suitable" in reason.lower()


def test_check_suitability_time_horizon():
    """Test suitability check considers time horizon."""
    # Short time horizon client
    short_horizon_client = ClientProfile(
        client_id="SHORT-001",
        name="Short Horizon",
        age=50,
        risk_tolerance=RiskTolerance.moderate,
        investment_goals=["income"],
        time_horizon_years=3,  # Very short
    )

    aggressive_portfolio = Portfolio(
        portfolio_name="Aggressive",
        holdings=[
            Holding(
                ticker="NVDA",
                name="NVIDIA",
                quantity=100,
                value=100000,
                asset_class=AssetClass.equity,
                sector="Technology",
            )
        ],
    )

    is_suitable, reason = check_suitability(aggressive_portfolio, short_horizon_client)

    # Short time horizon with aggressive portfolio should flag concerns
    assert "time horizon" in reason.lower() or "short" in reason.lower()


# ============================================================================
# Test Concentration Limit Checks
# ============================================================================


def test_check_concentration_limits_pass(balanced_portfolio):
    """Test concentration limits check with well-diversified portfolio."""
    passes, issues = check_concentration_limits(balanced_portfolio)

    # Balanced portfolio should pass concentration checks
    assert passes is True
    assert len(issues) == 0


def test_check_concentration_limits_fail(concentrated_portfolio):
    """Test concentration limits check with concentrated portfolio."""
    passes, issues = check_concentration_limits(concentrated_portfolio)

    # Concentrated portfolio (90% in one holding) should fail
    assert passes is False
    assert len(issues) > 0
    assert any("concentration" in issue.lower() for issue in issues)


def test_check_concentration_limits_boundary():
    """Test concentration limits at boundary (exactly 30%)."""
    portfolio = Portfolio(
        portfolio_name="Boundary Test",
        holdings=[
            Holding(
                ticker="AAPL",
                name="Apple",
                quantity=100,
                value=30000,
                asset_class=AssetClass.equity,
                sector="Technology",
            ),
            Holding(
                ticker="MSFT",
                name="Microsoft",
                quantity=100,
                value=70000,
                asset_class=AssetClass.equity,
                sector="Technology",
            ),
        ],
    )

    passes, issues = check_concentration_limits(portfolio)

    # 30% should pass (threshold is typically > 30%)
    assert passes is True


# ============================================================================
# Test Required Disclosures
# ============================================================================


def test_identify_required_disclosures_high_risk(concentrated_portfolio):
    """Test required disclosures for high-risk portfolio."""
    disclosures = identify_required_disclosures(concentrated_portfolio)

    # High concentration should require disclosures
    assert len(disclosures) > 0
    assert any("concentration" in d.lower() for d in disclosures)


def test_identify_required_disclosures_low_risk(balanced_portfolio):
    """Test required disclosures for low-risk portfolio."""
    disclosures = identify_required_disclosures(balanced_portfolio)

    # Balanced portfolio might have minimal disclosures
    # But should still have standard risk disclosure
    assert isinstance(disclosures, list)


def test_identify_required_disclosures_sector_concentration():
    """Test disclosures for sector concentration."""
    tech_heavy_portfolio = Portfolio(
        portfolio_name="Tech Heavy",
        holdings=[
            Holding(
                ticker="AAPL",
                name="Apple",
                quantity=100,
                value=40000,
                asset_class=AssetClass.equity,
                sector="Technology",
            ),
            Holding(
                ticker="MSFT",
                name="Microsoft",
                quantity=100,
                value=40000,
                asset_class=AssetClass.equity,
                sector="Technology",
            ),
            Holding(
                ticker="NVDA",
                name="NVIDIA",
                quantity=50,
                value=20000,
                asset_class=AssetClass.equity,
                sector="Technology",
            ),
        ],
    )

    disclosures = identify_required_disclosures(tech_heavy_portfolio)

    # 100% technology should require sector concentration disclosure
    assert any("sector" in d.lower() for d in disclosures)


# ============================================================================
# Test Complete Compliance Analysis
# ============================================================================


def test_analyze_compliance_compliant(conservative_client, balanced_portfolio):
    """Test full compliance analysis with compliant portfolio."""
    report = analyze_compliance(balanced_portfolio, conservative_client)

    # Should be compliant
    assert report.overall_status == ComplianceStatus.compliant
    assert len(report.compliance_issues) == 0


def test_analyze_compliance_non_compliant(conservative_client, concentrated_portfolio):
    """Test full compliance analysis with non-compliant portfolio."""
    report = analyze_compliance(concentrated_portfolio, conservative_client)

    # Should have compliance issues
    assert report.overall_status in [
        ComplianceStatus.needs_review,
        ComplianceStatus.non_compliant,
    ]
    assert len(report.compliance_issues) > 0


def test_analyze_compliance_fields_populated(aggressive_young_client, aggressive_portfolio):
    """Test that all compliance report fields are properly populated."""
    report = analyze_compliance(aggressive_portfolio, aggressive_young_client)

    # Verify all fields exist
    assert report.is_suitable is not None
    assert report.suitability_notes is not None
    assert report.concentration_compliant is not None
    assert isinstance(report.concentration_issues, list)
    assert isinstance(report.required_disclosures, list)
    assert report.overall_status in [
        ComplianceStatus.compliant,
        ComplianceStatus.needs_review,
        ComplianceStatus.non_compliant,
    ]


def test_analyze_compliance_conservative_senior():
    """Test compliance for conservative senior citizen."""
    senior_client = ClientProfile(
        client_id="SENIOR-001",
        name="Senior Citizen",
        age=75,
        risk_tolerance=RiskTolerance.conservative,
        investment_goals=["income", "capital_preservation"],
        time_horizon_years=5,
        income_needs=50000,
    )

    # Portfolio with insufficient bonds for senior
    risky_portfolio = Portfolio(
        portfolio_name="Too Risky",
        holdings=[
            Holding(
                ticker="NVDA",
                name="NVIDIA",
                quantity=100,
                value=80000,
                asset_class=AssetClass.equity,
                sector="Technology",
            ),
            Holding(
                ticker="BND",
                name="Bonds",
                quantity=200,
                value=20000,
                asset_class=AssetClass.bond,
                sector="Fixed Income",
            ),
        ],
    )

    report = analyze_compliance(risky_portfolio, senior_client)

    # Should flag suitability issues for senior
    assert report.is_suitable is False or report.overall_status != ComplianceStatus.compliant


# ============================================================================
# Test Edge Cases
# ============================================================================


def test_compliance_empty_portfolio():
    """Test compliance check with empty portfolio."""
    empty_portfolio = Portfolio(portfolio_name="Empty", holdings=[])

    client = ClientProfile(
        client_id="TEST",
        name="Test",
        age=50,
        risk_tolerance=RiskTolerance.moderate,
        investment_goals=["growth"],
        time_horizon_years=10,
    )

    # Should handle gracefully
    with pytest.raises(Exception):
        analyze_compliance(empty_portfolio, client)


def test_compliance_consistency():
    """Test that compliance analysis is consistent across runs."""
    client = ClientProfile(
        client_id="CONSIST",
        name="Consistency Test",
        age=45,
        risk_tolerance=RiskTolerance.moderate,
        investment_goals=["growth", "income"],
        time_horizon_years=15,
    )

    portfolio = Portfolio(
        portfolio_name="Moderate",
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

    # Run analysis twice
    report1 = analyze_compliance(portfolio, client)
    report2 = analyze_compliance(portfolio, client)

    # Results should be identical
    assert report1.is_suitable == report2.is_suitable
    assert report1.concentration_compliant == report2.concentration_compliant
    assert report1.overall_status == report2.overall_status
    assert len(report1.compliance_issues) == len(report2.compliance_issues)
