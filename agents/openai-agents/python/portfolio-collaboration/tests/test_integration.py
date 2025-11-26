"""
Integration Tests for Multi-Agent Portfolio Collaboration System.

These tests verify end-to-end workflows including:
- Complete analysis pipeline (Risk + Compliance + Performance)
- Parallel execution of specialist agents
- Suitability scoring from all specialist outputs
- Report generation from recommendations
- Real-world scenarios with sample data
"""

import pytest

from src.agents.portfolio_manager import (
    run_comprehensive_analysis,
    generate_client_report,
)
from src.data.mock_portfolios import (
    get_conservative_example,
    get_moderate_example,
    get_aggressive_example,
)
from src.models.schemas import (
    ClientProfile,
    ComplianceStatus,
    RiskRating,
    RiskTolerance,
    SuitabilityRating,
)
from src.tools.parallel_execution import run_specialists_parallel_safe
from src.tools.suitability_scoring import calculate_suitability_score


# ============================================================================
# Test Fixtures - Sample Clients
# ============================================================================


@pytest.fixture
def conservative_senior_client():
    """Conservative 68-year-old client."""
    return ClientProfile(
        client_id="CLT-2024-001",
        name="Robert Williams",
        age=68,
        risk_tolerance=RiskTolerance.conservative,
        investment_goals=["income", "capital_preservation"],
        time_horizon_years=8,
        income_needs=50000,
    )


@pytest.fixture
def moderate_midlife_client():
    """Moderate 45-year-old client."""
    return ClientProfile(
        client_id="CLT-2024-002",
        name="Jennifer Martinez",
        age=45,
        risk_tolerance=RiskTolerance.moderate,
        investment_goals=["growth", "income"],
        time_horizon_years=20,
    )


@pytest.fixture
def aggressive_young_client():
    """Aggressive 32-year-old client."""
    return ClientProfile(
        client_id="CLT-2024-003",
        name="Michael Chen",
        age=32,
        risk_tolerance=RiskTolerance.aggressive,
        investment_goals=["growth", "wealth_accumulation"],
        time_horizon_years=33,
    )


# ============================================================================
# Test End-to-End Analysis Pipeline
# ============================================================================


@pytest.mark.integration
def test_conservative_client_conservative_portfolio(conservative_senior_client):
    """
    Integration test: Conservative client with conservative portfolio.

    Expected: High suitability, compliant, low risk.
    """
    # Get conservative portfolio
    portfolio = get_conservative_example()

    # Run comprehensive analysis
    recommendations = run_comprehensive_analysis(portfolio, conservative_senior_client)

    # Verify overall structure
    assert recommendations.client_id == conservative_senior_client.client_id
    assert recommendations.portfolio == portfolio

    # Verify risk analysis
    assert recommendations.risk_analysis is not None
    assert recommendations.risk_analysis.risk_rating in [RiskRating.low, RiskRating.medium]
    assert recommendations.risk_analysis.volatility < 20.0  # Conservative portfolio should have low volatility

    # Verify compliance
    assert recommendations.compliance_report is not None
    assert recommendations.compliance_report.overall_status == ComplianceStatus.compliant
    assert recommendations.compliance_report.is_suitable is True

    # Verify performance
    assert recommendations.performance_report is not None
    assert recommendations.performance_report.total_return is not None

    # Verify suitability - should be highly suitable or suitable
    assert recommendations.suitability_score.overall_score >= 60
    assert recommendations.suitability_score.rating in [
        SuitabilityRating.highly_suitable,
        SuitabilityRating.suitable,
    ]

    # Verify recommendations and actions exist
    assert len(recommendations.recommendations) > 0
    assert len(recommendations.action_items) > 0


@pytest.mark.integration
def test_moderate_client_moderate_portfolio(moderate_midlife_client):
    """
    Integration test: Moderate client with moderate portfolio.

    Expected: Good suitability, compliant, medium risk.
    """
    # Get moderate portfolio
    portfolio = get_moderate_example()

    # Run comprehensive analysis
    recommendations = run_comprehensive_analysis(portfolio, moderate_midlife_client)

    # Verify risk analysis
    assert recommendations.risk_analysis.risk_rating in [RiskRating.medium, RiskRating.low, RiskRating.high]

    # Verify compliance
    assert recommendations.compliance_report.overall_status in [
        ComplianceStatus.compliant,
        ComplianceStatus.needs_review,
    ]

    # Verify suitability - should be suitable
    assert recommendations.suitability_score.overall_score >= 50

    # Verify report generation works
    report = generate_client_report(recommendations)
    assert isinstance(report, str)
    assert len(report) > 1000  # Should be substantial report
    assert "# Portfolio Analysis Report" in report


@pytest.mark.integration
def test_aggressive_client_aggressive_portfolio(aggressive_young_client):
    """
    Integration test: Aggressive client with aggressive portfolio.

    Expected: Good suitability for young aggressive client, higher risk acceptable.
    """
    # Get aggressive portfolio
    portfolio = get_aggressive_example()

    # Run comprehensive analysis
    recommendations = run_comprehensive_analysis(portfolio, aggressive_young_client)

    # Verify risk analysis - aggressive portfolio should have higher risk
    assert recommendations.risk_analysis.risk_rating in [RiskRating.medium, RiskRating.high]
    assert recommendations.risk_analysis.volatility > 10.0  # Should have meaningful volatility

    # Verify compliance - young aggressive client should be suitable
    assert recommendations.compliance_report.is_suitable is True or recommendations.suitability_score.overall_score >= 60

    # Verify suitability - should be good match for aggressive young client
    assert recommendations.suitability_score.overall_score >= 50

    # Verify performance metrics exist
    assert recommendations.performance_report.total_return is not None
    assert recommendations.performance_report.sharpe_ratio is not None


# ============================================================================
# Test Mismatched Scenarios
# ============================================================================


@pytest.mark.integration
def test_conservative_client_aggressive_portfolio_mismatch(conservative_senior_client):
    """
    Integration test: Conservative senior with aggressive portfolio.

    Expected: Lower suitability, potential compliance issues, recommendations for changes.
    """
    # Get aggressive portfolio (mismatch!)
    portfolio = get_aggressive_example()

    # Run comprehensive analysis
    recommendations = run_comprehensive_analysis(portfolio, conservative_senior_client)

    # Should flag mismatch
    # Either low suitability score OR compliance issues OR both
    has_concerns = (
        recommendations.suitability_score.overall_score < 70
        or recommendations.compliance_report.overall_status != ComplianceStatus.compliant
        or len(recommendations.compliance_report.compliance_issues) > 0
    )
    assert has_concerns, "Conservative senior with aggressive portfolio should raise concerns"

    # Should have recommendations for changes
    assert len(recommendations.recommendations) > 0

    # Recommendations should mention risk or suitability
    recs_text = " ".join(recommendations.recommendations).lower()
    assert "risk" in recs_text or "suitable" in recs_text or "conservative" in recs_text


@pytest.mark.integration
def test_aggressive_client_conservative_portfolio_suboptimal(aggressive_young_client):
    """
    Integration test: Aggressive young client with conservative portfolio.

    Expected: Compliant but suboptimal - client could take more risk.
    """
    # Get conservative portfolio (too conservative for young aggressive client)
    portfolio = get_conservative_example()

    # Run comprehensive analysis
    recommendations = run_comprehensive_analysis(portfolio, aggressive_young_client)

    # Should be compliant (conservative is always safe)
    assert recommendations.compliance_report.overall_status == ComplianceStatus.compliant

    # But suitability might be lower (not utilizing client's risk capacity)
    # OR recommendations should suggest more growth-oriented allocation
    recs_text = " ".join(recommendations.recommendations).lower()
    suggests_more_growth = "growth" in recs_text or "equity" in recs_text or "aggressive" in recs_text

    # Either lower suitability OR recommendations for more growth
    assert (
        recommendations.suitability_score.overall_score < 90
        or suggests_more_growth
    )


# ============================================================================
# Test Parallel Execution Integration
# ============================================================================


@pytest.mark.integration
def test_parallel_specialist_execution(moderate_midlife_client):
    """
    Integration test: Parallel execution of all specialist agents.

    Verifies that Risk, Compliance, and Performance agents run in parallel correctly.
    """
    portfolio = get_moderate_example()

    # Run specialists in parallel
    result = run_specialists_parallel_safe(portfolio, moderate_midlife_client)

    # Verify all specialist outputs are present
    assert result.risk_analysis is not None
    assert result.compliance_report is not None
    assert result.performance_report is not None

    # Verify risk analysis completeness
    assert result.risk_analysis.volatility > 0
    assert result.risk_analysis.var_95 > 0
    assert result.risk_analysis.risk_rating in [RiskRating.low, RiskRating.medium, RiskRating.high]

    # Verify compliance completeness
    assert result.compliance_report.is_suitable is not None
    assert result.compliance_report.overall_status in [
        ComplianceStatus.compliant,
        ComplianceStatus.needs_review,
        ComplianceStatus.non_compliant,
    ]

    # Verify performance completeness
    assert result.performance_report.total_return is not None
    assert len(result.performance_report.top_performers) > 0


# ============================================================================
# Test Suitability Scoring Integration
# ============================================================================


@pytest.mark.integration
def test_suitability_scoring_integration(conservative_senior_client):
    """
    Integration test: Suitability scoring from all specialist outputs.

    Verifies that suitability score is calculated correctly from all inputs.
    """
    portfolio = get_conservative_example()

    # Get specialist analysis
    result = run_specialists_parallel_safe(portfolio, conservative_senior_client)

    # Calculate suitability score
    suitability = calculate_suitability_score(
        client_profile=conservative_senior_client,
        risk_analysis=result.risk_analysis,
        compliance_report=result.compliance_report,
        performance_report=result.performance_report,
    )

    # Verify suitability structure
    assert 0 <= suitability.overall_score <= 100
    assert 0 <= suitability.risk_fit_score <= 100
    assert 0 <= suitability.compliance_fit_score <= 100
    assert 0 <= suitability.performance_fit_score <= 100
    assert 0 <= suitability.time_horizon_fit_score <= 100

    # Verify rating matches score
    if suitability.overall_score >= 80:
        assert suitability.rating == SuitabilityRating.highly_suitable
    elif suitability.overall_score >= 60:
        assert suitability.rating == SuitabilityRating.suitable
    elif suitability.overall_score >= 40:
        assert suitability.rating == SuitabilityRating.marginal_fit
    else:
        assert suitability.rating == SuitabilityRating.not_suitable

    # Verify interpretation is present
    assert len(suitability.interpretation) > 0


# ============================================================================
# Test Report Generation Integration
# ============================================================================


@pytest.mark.integration
def test_complete_report_generation(moderate_midlife_client):
    """
    Integration test: Complete report generation from analysis.

    Verifies that markdown report includes all sections.
    """
    portfolio = get_moderate_example()

    # Run full analysis
    recommendations = run_comprehensive_analysis(portfolio, moderate_midlife_client)

    # Generate report
    report = generate_client_report(recommendations)

    # Verify report structure
    assert isinstance(report, str)
    assert len(report) > 500

    # Verify all key sections are present
    assert "# Portfolio Analysis Report" in report
    assert "Risk Analysis" in report
    assert "Compliance" in report
    assert "Performance" in report
    assert "Suitability" in report
    assert "Recommendations" in report
    assert "Action Items" in report or "Actions" in report

    # Verify client information is included
    assert moderate_midlife_client.client_id in report
    assert portfolio.portfolio_name in report

    # Verify metrics are included
    assert str(recommendations.suitability_score.overall_score) in report or f"{recommendations.suitability_score.overall_score:.0f}" in report
    assert recommendations.risk_analysis.risk_rating.value in report.lower()


# ============================================================================
# Test All Three Sample Scenarios
# ============================================================================


@pytest.mark.integration
def test_all_sample_scenarios():
    """
    Integration test: Run analysis for all three sample scenarios.

    Verifies that the system handles all standard risk profiles correctly.
    """
    # Scenario 1: Conservative
    conservative_client = ClientProfile(
        client_id="SAMPLE-001",
        name="Conservative Test",
        age=65,
        risk_tolerance=RiskTolerance.conservative,
        investment_goals=["income"],
        time_horizon_years=10,
    )
    conservative_rec = run_comprehensive_analysis(
        get_conservative_example(), conservative_client
    )
    assert conservative_rec.suitability_score.overall_score >= 60

    # Scenario 2: Moderate
    moderate_client = ClientProfile(
        client_id="SAMPLE-002",
        name="Moderate Test",
        age=50,
        risk_tolerance=RiskTolerance.moderate,
        investment_goals=["growth", "income"],
        time_horizon_years=15,
    )
    moderate_rec = run_comprehensive_analysis(get_moderate_example(), moderate_client)
    assert moderate_rec.suitability_score.overall_score >= 50

    # Scenario 3: Aggressive
    aggressive_client = ClientProfile(
        client_id="SAMPLE-003",
        name="Aggressive Test",
        age=35,
        risk_tolerance=RiskTolerance.aggressive,
        investment_goals=["growth"],
        time_horizon_years=30,
    )
    aggressive_rec = run_comprehensive_analysis(
        get_aggressive_example(), aggressive_client
    )
    assert aggressive_rec.suitability_score.overall_score >= 50

    # Verify all scenarios completed successfully
    assert all([
        conservative_rec.compliance_report is not None,
        moderate_rec.compliance_report is not None,
        aggressive_rec.compliance_report is not None,
    ])


# ============================================================================
# Test Data Flow Consistency
# ============================================================================


@pytest.mark.integration
def test_data_flow_consistency(moderate_midlife_client):
    """
    Integration test: Verify data consistency across the analysis pipeline.

    Ensures that data flows correctly from portfolio → specialist agents →
    suitability scoring → recommendations.
    """
    portfolio = get_moderate_example()

    # Run comprehensive analysis
    recommendations = run_comprehensive_analysis(portfolio, moderate_midlife_client)

    # Verify portfolio data consistency
    assert recommendations.portfolio == portfolio
    assert recommendations.portfolio.portfolio_name == portfolio.portfolio_name
    assert len(recommendations.portfolio.holdings) == len(portfolio.holdings)

    # Verify client data consistency
    assert recommendations.client_id == moderate_midlife_client.client_id

    # Verify specialist outputs are linked correctly
    # Risk analysis should have risk factors if high risk
    if recommendations.risk_analysis.risk_rating == RiskRating.high:
        assert len(recommendations.risk_analysis.risk_factors) > 0

    # Compliance issues should match overall status
    if recommendations.compliance_report.overall_status == ComplianceStatus.non_compliant:
        assert len(recommendations.compliance_report.compliance_issues) > 0

    # Performance top/bottom performers should be from portfolio holdings
    all_tickers = [h.ticker for h in portfolio.holdings]
    for holding, _ in recommendations.performance_report.top_performers:
        assert holding.ticker in all_tickers
    for holding, _ in recommendations.performance_report.bottom_performers:
        assert holding.ticker in all_tickers


# ============================================================================
# Test Performance and Timing
# ============================================================================


@pytest.mark.integration
@pytest.mark.slow
def test_parallel_execution_performance(moderate_midlife_client):
    """
    Integration test: Verify parallel execution performs reasonably.

    Tests that parallel execution completes in reasonable time.
    """
    import time

    portfolio = get_moderate_example()

    # Measure parallel execution time
    start = time.time()
    result = run_specialists_parallel_safe(portfolio, moderate_midlife_client)
    parallel_time = time.time() - start

    # Should complete in reasonable time (< 10 seconds for mock data)
    assert parallel_time < 10.0, f"Parallel execution took {parallel_time:.2f}s (expected < 10s)"

    # Verify all outputs are complete
    assert result.risk_analysis is not None
    assert result.compliance_report is not None
    assert result.performance_report is not None


# ============================================================================
# Test Error Handling in Integration
# ============================================================================


@pytest.mark.integration
def test_integration_handles_missing_cost_basis():
    """
    Integration test: System handles portfolios with missing cost basis gracefully.

    Some holdings may not have cost basis data - system should handle this.
    """
    from src.models.schemas import Holding, Portfolio, AssetClass

    # Create portfolio with one holding missing cost basis
    portfolio = Portfolio(
        portfolio_name="Partial Cost Basis",
        holdings=[
            Holding(
                ticker="AAPL",
                name="Apple Inc.",
                quantity=100,
                value=50000,
                asset_class=AssetClass.equity,
                sector="Technology",
                cost_basis=45000,  # Has cost basis
            ),
            Holding(
                ticker="MSFT",
                name="Microsoft",
                quantity=50,
                value=50000,
                asset_class=AssetClass.equity,
                sector="Technology",
                # No cost_basis - defaults to None
            ),
        ],
    )

    client = ClientProfile(
        client_id="MISSING-CB-001",
        name="Test Client",
        age=50,
        risk_tolerance=RiskTolerance.moderate,
        investment_goals=["growth"],
        time_horizon_years=15,
    )

    # Should complete without errors
    recommendations = run_comprehensive_analysis(portfolio, client)

    # Should still have valid analysis
    assert recommendations.risk_analysis is not None
    assert recommendations.compliance_report is not None
    # Performance might have limited data but should not crash
    assert recommendations.performance_report is not None


# ============================================================================
# Test Integration with Real Sample Data
# ============================================================================


@pytest.mark.integration
def test_integration_with_sample_data_files():
    """
    Integration test: Verify system works with data from sample JSON files.

    This tests the complete workflow using the actual sample data files.
    """
    import json
    from pathlib import Path

    # Load sample data
    project_root = Path(__file__).resolve().parent.parent
    examples_dir = project_root / "examples"

    # Load clients
    with open(examples_dir / "sample_clients.json", "r") as f:
        clients_data = json.load(f)

    # Load portfolios
    with open(examples_dir / "sample_portfolios.json", "r") as f:
        portfolios_data = json.load(f)

    # Test with first client and first portfolio
    if clients_data.get("clients") and portfolios_data.get("portfolios"):
        client_data = clients_data["clients"][0]
        portfolio_data = portfolios_data["portfolios"][0]

        client = ClientProfile(**client_data)
        from src.models.schemas import Portfolio
        portfolio = Portfolio(**portfolio_data)

        # Run analysis
        recommendations = run_comprehensive_analysis(portfolio, client)

        # Should complete successfully
        assert recommendations is not None
        assert recommendations.suitability_score.overall_score >= 0

        # Generate report
        report = generate_client_report(recommendations)
        assert len(report) > 0
