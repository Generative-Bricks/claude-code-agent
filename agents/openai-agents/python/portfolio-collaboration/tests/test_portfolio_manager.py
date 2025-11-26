"""
Unit Tests for Portfolio Manager Agent.

Tests cover:
- Comprehensive analysis orchestration
- Report generation
- Recommendation engine
- Action item generation
- Integration with specialist agents
"""

import pytest

from src.agents.portfolio_manager import (
    _create_action_items,
    _generate_recommendations,
    run_comprehensive_analysis,
    generate_client_report,
)
from src.models.schemas import (
    AssetClass,
    ClientProfile,
    ComplianceStatus,
    Holding,
    Portfolio,
    PortfolioRecommendations,
    RiskRating,
    RiskTolerance,
    SuitabilityRating,
)


# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def conservative_senior():
    """Conservative senior client fixture."""
    return ClientProfile(
        client_id="PM-001",
        name="Conservative Senior",
        age=70,
        risk_tolerance=RiskTolerance.conservative,
        investment_goals=["income", "capital_preservation"],
        time_horizon_years=5,
        income_needs=60000,
    )


@pytest.fixture
def moderate_midlife():
    """Moderate middle-aged client fixture."""
    return ClientProfile(
        client_id="PM-002",
        name="Moderate Midlife",
        age=45,
        risk_tolerance=RiskTolerance.moderate,
        investment_goals=["growth", "income"],
        time_horizon_years=20,
    )


@pytest.fixture
def aggressive_young():
    """Aggressive young client fixture."""
    return ClientProfile(
        client_id="PM-003",
        name="Aggressive Youth",
        age=30,
        risk_tolerance=RiskTolerance.aggressive,
        investment_goals=["growth", "wealth_accumulation"],
        time_horizon_years=35,
    )


@pytest.fixture
def balanced_portfolio():
    """Balanced 60/40 portfolio."""
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
                cost_basis=50000,
            ),
            Holding(
                ticker="BND",
                name="Total Bond ETF",
                quantity=400,
                value=40000,
                asset_class=AssetClass.bond,
                sector="Fixed Income",
                cost_basis=38000,
            ),
        ],
    )


@pytest.fixture
def conservative_portfolio():
    """Conservative 30/70 portfolio."""
    return Portfolio(
        portfolio_name="Conservative",
        holdings=[
            Holding(
                ticker="SPY",
                name="S&P 500 ETF",
                quantity=75,
                value=30000,
                asset_class=AssetClass.equity,
                sector="Diversified",
                cost_basis=28000,
            ),
            Holding(
                ticker="BND",
                name="Total Bond ETF",
                quantity=700,
                value=70000,
                asset_class=AssetClass.bond,
                sector="Fixed Income",
                cost_basis=68000,
            ),
        ],
    )


@pytest.fixture
def aggressive_portfolio():
    """Aggressive 100% equity portfolio."""
    return Portfolio(
        portfolio_name="Aggressive",
        holdings=[
            Holding(
                ticker="NVDA",
                name="NVIDIA",
                quantity=100,
                value=45000,
                asset_class=AssetClass.equity,
                sector="Technology",
                cost_basis=30000,
            ),
            Holding(
                ticker="AAPL",
                name="Apple",
                quantity=200,
                value=35000,
                asset_class=AssetClass.equity,
                sector="Technology",
                cost_basis=28000,
            ),
            Holding(
                ticker="MSFT",
                name="Microsoft",
                quantity=50,
                value=20000,
                asset_class=AssetClass.equity,
                sector="Technology",
                cost_basis=18000,
            ),
        ],
    )


# ============================================================================
# Test Comprehensive Analysis
# ============================================================================


def test_run_comprehensive_analysis_basic(moderate_midlife, balanced_portfolio):
    """Test comprehensive analysis with well-matched client and portfolio."""
    recommendations = run_comprehensive_analysis(balanced_portfolio, moderate_midlife)

    # Verify recommendations object is created
    assert isinstance(recommendations, PortfolioRecommendations)
    assert recommendations.client_id == moderate_midlife.client_id
    assert recommendations.portfolio == balanced_portfolio

    # Verify all specialist analysis results are included
    assert recommendations.risk_analysis is not None
    assert recommendations.compliance_report is not None
    assert recommendations.performance_report is not None

    # Verify suitability score is calculated
    assert recommendations.suitability_score is not None
    assert 0 <= recommendations.suitability_score.overall_score <= 100

    # Verify recommendations and action items are generated
    assert len(recommendations.recommendations) > 0
    assert len(recommendations.action_items) > 0


def test_run_comprehensive_analysis_conservative_match(
    conservative_senior, conservative_portfolio
):
    """Test analysis with conservative client and appropriate portfolio."""
    recommendations = run_comprehensive_analysis(
        conservative_portfolio, conservative_senior
    )

    # Should have high suitability score (good match)
    assert recommendations.suitability_score.overall_score >= 60

    # Compliance should be good
    assert recommendations.compliance_report.overall_status in [
        ComplianceStatus.compliant,
        ComplianceStatus.needs_review,
    ]


def test_run_comprehensive_analysis_mismatch(
    conservative_senior, aggressive_portfolio
):
    """Test analysis with mismatched client and portfolio."""
    recommendations = run_comprehensive_analysis(
        aggressive_portfolio, conservative_senior
    )

    # Should have lower suitability score (poor match)
    assert recommendations.suitability_score.overall_score < 80

    # Should have compliance concerns
    assert len(recommendations.compliance_report.compliance_issues) > 0

    # Should have recommendations for changes
    assert len(recommendations.recommendations) > 0


def test_comprehensive_analysis_fields_complete(aggressive_young, aggressive_portfolio):
    """Test that all fields in recommendations are properly populated."""
    recommendations = run_comprehensive_analysis(
        aggressive_portfolio, aggressive_young
    )

    # Risk analysis fields
    assert recommendations.risk_analysis.volatility > 0
    assert recommendations.risk_analysis.var_95 > 0
    assert recommendations.risk_analysis.risk_rating in [
        RiskRating.low,
        RiskRating.medium,
        RiskRating.high,
    ]

    # Compliance report fields
    assert recommendations.compliance_report.is_suitable is not None
    assert recommendations.compliance_report.overall_status in [
        ComplianceStatus.compliant,
        ComplianceStatus.needs_review,
        ComplianceStatus.non_compliant,
    ]

    # Performance report fields
    assert recommendations.performance_report.total_return is not None
    assert recommendations.performance_report.sharpe_ratio is not None

    # Suitability score fields
    assert recommendations.suitability_score.rating in [
        SuitabilityRating.highly_suitable,
        SuitabilityRating.suitable,
        SuitabilityRating.marginal_fit,
        SuitabilityRating.not_suitable,
    ]


# ============================================================================
# Test Report Generation
# ============================================================================


def test_generate_client_report(moderate_midlife, balanced_portfolio):
    """Test client report generation."""
    # First run analysis
    recommendations = run_comprehensive_analysis(balanced_portfolio, moderate_midlife)

    # Then generate report
    report = generate_client_report(recommendations)

    # Report should be markdown formatted
    assert isinstance(report, str)
    assert len(report) > 0

    # Should contain key sections
    assert "# Portfolio Analysis Report" in report
    assert "Executive Summary" in report or "Summary" in report
    assert "Risk Analysis" in report
    assert "Compliance" in report
    assert "Performance" in report
    assert "Suitability" in report
    assert "Recommendations" in report


def test_report_contains_client_info(conservative_senior, conservative_portfolio):
    """Test that report includes client information."""
    recommendations = run_comprehensive_analysis(
        conservative_portfolio, conservative_senior
    )
    report = generate_client_report(recommendations)

    # Should include client ID
    assert conservative_senior.client_id in report

    # Should include portfolio name
    assert conservative_portfolio.portfolio_name in report


def test_report_markdown_formatting(aggressive_young, aggressive_portfolio):
    """Test that report uses proper markdown formatting."""
    recommendations = run_comprehensive_analysis(
        aggressive_portfolio, aggressive_young
    )
    report = generate_client_report(recommendations)

    # Should have markdown headers
    assert report.count("#") >= 5  # Multiple section headers

    # Should have bullet points
    assert "- " in report or "* " in report

    # Should have bold text
    assert "**" in report


# ============================================================================
# Test Recommendation Generation
# ============================================================================


def test_generate_recommendations_high_risk():
    """Test recommendation generation for high-risk portfolio."""
    from src.models.schemas import RiskAnalysis, ComplianceReport, PerformanceReport, SuitabilityScore

    portfolio = Portfolio(
        portfolio_name="High Risk",
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

    client = ClientProfile(
        client_id="REC-001",
        name="Test",
        age=65,
        risk_tolerance=RiskTolerance.conservative,
        investment_goals=["income"],
        time_horizon_years=5,
        income_needs=50000,
    )

    # Create mock analysis results
    risk_analysis = RiskAnalysis(
        volatility=28.5,
        var_95=25000,
        beta=1.5,
        concentration_score=100,
        risk_rating=RiskRating.high,
        risk_factors=["High volatility", "High concentration"],
    )

    compliance_report = ComplianceReport(
        is_suitable=False,
        suitability_notes="Too risky for conservative client",
        concentration_compliant=False,
        concentration_issues=["100% concentration in single stock"],
        required_disclosures=["High risk disclosure"],
        compliance_issues=["Unsuitable for conservative client"],
        overall_status=ComplianceStatus.non_compliant,
    )

    performance_report = PerformanceReport(
        total_return=50.0,
        sharpe_ratio=1.2,
        alpha=10.0,
        sector_attribution={"Technology": 100.0},
        top_performers=[],
        bottom_performers=[],
        percentile_rank=75,
    )

    suitability_score = SuitabilityScore(
        overall_score=35.0,
        risk_fit_score=20.0,
        compliance_fit_score=30.0,
        performance_fit_score=50.0,
        time_horizon_fit_score=40.0,
        rating=SuitabilityRating.not_suitable,
        interpretation="Not suitable for client goals",
    )

    recommendations = _generate_recommendations(
        portfolio=portfolio,
        client_profile=client,
        risk_analysis=risk_analysis,
        compliance_report=compliance_report,
        performance_report=performance_report,
        suitability_score=suitability_score,
    )

    # Should generate multiple recommendations
    assert len(recommendations) > 0

    # Should mention volatility
    recs_text = " ".join(recommendations).lower()
    assert "volatility" in recs_text or "risk" in recs_text

    # Should mention concentration
    assert "concentration" in recs_text or "diversif" in recs_text


# ============================================================================
# Test Action Item Generation
# ============================================================================


def test_create_action_items_compliant():
    """Test action item creation for compliant portfolio."""
    from src.models.schemas import RiskAnalysis, ComplianceReport, SuitabilityScore

    risk_analysis = RiskAnalysis(
        volatility=12.0,
        var_95=10000,
        beta=1.0,
        concentration_score=40,
        risk_rating=RiskRating.medium,
        risk_factors=[],
    )

    compliance_report = ComplianceReport(
        is_suitable=True,
        suitability_notes="Suitable",
        concentration_compliant=True,
        concentration_issues=[],
        required_disclosures=[],
        compliance_issues=[],
        overall_status=ComplianceStatus.compliant,
    )

    suitability_score = SuitabilityScore(
        overall_score=82.0,
        risk_fit_score=85.0,
        compliance_fit_score=90.0,
        performance_fit_score=75.0,
        time_horizon_fit_score=80.0,
        rating=SuitabilityRating.highly_suitable,
        interpretation="Highly suitable",
    )

    action_items = _create_action_items(
        risk_analysis, compliance_report, suitability_score
    )

    # Should have at least quarterly review item
    assert len(action_items) > 0

    # Should not have urgent items for compliant portfolio
    action_items_text = " ".join(action_items)
    assert "URGENT" not in action_items_text or "No urgent actions" in action_items_text


def test_create_action_items_non_compliant():
    """Test action item creation for non-compliant portfolio."""
    from src.models.schemas import RiskAnalysis, ComplianceReport, SuitabilityScore

    risk_analysis = RiskAnalysis(
        volatility=30.0,
        var_95=40000,
        beta=1.8,
        concentration_score=85,
        risk_rating=RiskRating.high,
        risk_factors=["High risk"],
    )

    compliance_report = ComplianceReport(
        is_suitable=False,
        suitability_notes="Not suitable",
        concentration_compliant=False,
        concentration_issues=["High concentration"],
        required_disclosures=["Risk disclosure", "Concentration disclosure"],
        compliance_issues=["Unsuitable for client"],
        overall_status=ComplianceStatus.non_compliant,
    )

    suitability_score = SuitabilityScore(
        overall_score=25.0,
        risk_fit_score=20.0,
        compliance_fit_score=15.0,
        performance_fit_score=40.0,
        time_horizon_fit_score=25.0,
        rating=SuitabilityRating.not_suitable,
        interpretation="Not suitable",
    )

    action_items = _create_action_items(
        risk_analysis, compliance_report, suitability_score
    )

    # Should have urgent items
    action_items_text = " ".join(action_items)
    assert "🔴" in action_items_text  # Urgent marker


# ============================================================================
# Test Edge Cases
# ============================================================================


def test_comprehensive_analysis_consistency(moderate_midlife, balanced_portfolio):
    """Test that analysis produces consistent results across runs."""
    # Run analysis twice
    rec1 = run_comprehensive_analysis(balanced_portfolio, moderate_midlife)
    rec2 = run_comprehensive_analysis(balanced_portfolio, moderate_midlife)

    # Key metrics should be identical
    assert rec1.suitability_score.overall_score == rec2.suitability_score.overall_score
    assert rec1.risk_analysis.volatility == rec2.risk_analysis.volatility
    assert (
        rec1.compliance_report.overall_status == rec2.compliance_report.overall_status
    )


def test_empty_portfolio_handling():
    """Test handling of empty portfolio."""
    empty_portfolio = Portfolio(portfolio_name="Empty", holdings=[])

    client = ClientProfile(
        client_id="EMPTY-001",
        name="Test",
        age=50,
        risk_tolerance=RiskTolerance.moderate,
        investment_goals=["growth"],
        time_horizon_years=10,
    )

    # Should handle gracefully or raise appropriate error
    with pytest.raises(Exception):
        run_comprehensive_analysis(empty_portfolio, client)
