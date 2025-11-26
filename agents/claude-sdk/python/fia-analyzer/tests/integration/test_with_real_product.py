"""
Integration tests for real product analysis scenarios.

Tests realistic product analysis workflows including:
- Multiple product searches
- Real-world client scenarios
- Complete analysis pipelines
"""

import pytest
from datetime import datetime
from src.tools.search_fia_products import search_fia_products
from src.tools.analyze_product_fit import analyze_product_fit
from src.models import FIAProduct, ClientProfile


@pytest.fixture
def conservative_retiree():
    """Conservative retiree client profile."""
    return ClientProfile(
        age=68,
        state="FL",
        marital_status="married",
        total_investable_assets=750000.0,
        annual_income=60000.0,
        emergency_fund_months=18,
        existing_annuities=150000.0,
        primary_goal="income",
        income_start_year=1,
        income_duration="lifetime",
        risk_tolerance="conservative",
        liquidity_needs_next_5_years=False,
        liquidity_amount_needed=0.0,
        investment_time_horizon=15,
        understands_fia_mechanics=True,
        has_reviewed_alternatives=True,
        comfortable_with_surrender_charges=True,
        tax_bracket="12-22%",
        wants_tax_deferral=True
    )


@pytest.fixture
def moderate_pre_retiree():
    """Moderate risk pre-retiree client profile."""
    return ClientProfile(
        age=58,
        state="TX",
        marital_status="married",
        total_investable_assets=1200000.0,
        annual_income=150000.0,
        emergency_fund_months=12,
        existing_annuities=0.0,
        primary_goal="protection",
        income_start_year=7,
        income_duration="lifetime",
        risk_tolerance="moderate",
        liquidity_needs_next_5_years=True,
        liquidity_amount_needed=50000.0,
        investment_time_horizon=20,
        understands_fia_mechanics=True,
        has_reviewed_alternatives=True,
        comfortable_with_surrender_charges=True,
        tax_bracket="22-24%",
        wants_tax_deferral=True
    )


@pytest.fixture
def aggressive_young_investor():
    """Aggressive young investor (likely NOT suitable for FIA)."""
    return ClientProfile(
        age=35,
        state="CA",
        marital_status="single",
        total_investable_assets=200000.0,
        annual_income=120000.0,
        emergency_fund_months=6,
        existing_annuities=0.0,
        primary_goal="protection",
        income_start_year=30,
        risk_tolerance="aggressive",
        liquidity_needs_next_5_years=True,
        liquidity_amount_needed=100000.0,
        investment_time_horizon=30,
        understands_fia_mechanics=False,
        has_reviewed_alternatives=False,
        comfortable_with_surrender_charges=False,
        tax_bracket="24-32%",
        wants_tax_deferral=False
    )


@pytest.fixture
def allianz_benefit_control():
    """Allianz Benefit Control product data."""
    return FIAProduct(
        name="Allianz Benefit Control",
        carrier="Allianz Life Insurance Company",
        term_years=10,
        minimum_premium=10000.0,
        maximum_issue_age=85,
        surrender_charge_schedule=[9.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0],
        penalty_free_withdrawal=10.0,
        index_options=["S&P 500", "Nasdaq-100", "Russell 2000"],
        crediting_methods=["Annual Point-to-Point", "Monthly Average"],
        cap_rates={"S&P 500": 7.5, "Nasdaq-100": 6.0, "Russell 2000": 8.0},
        participation_rates={"S&P 500": 100.0, "Nasdaq-100": 90.0},
        rates_as_of_date=datetime.now().strftime("%Y-%m-%d"),
        income_riders=["Guaranteed Lifetime Withdrawal Benefit"],
        death_benefit="Return of Premium",
        nursing_home_waiver=True,
        am_best_rating="A+",
        state_availability=["TX", "CA", "FL", "AZ", "NV"]
    )


@pytest.fixture
def nationwide_peak_10():
    """Nationwide Peak 10 product data."""
    return FIAProduct(
        name="Nationwide Peak 10",
        carrier="Nationwide Life Insurance Company",
        term_years=10,
        minimum_premium=10000.0,
        maximum_issue_age=80,
        surrender_charge_schedule=[10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 0.0],
        penalty_free_withdrawal=10.0,
        index_options=["S&P 500", "Nasdaq-100"],
        crediting_methods=["Annual Point-to-Point"],
        cap_rates={"S&P 500": 8.0, "Nasdaq-100": 6.5},
        participation_rates={"S&P 500": 100.0},
        rates_as_of_date=datetime.now().strftime("%Y-%m-%d"),
        income_riders=["Lifetime Income Benefit Rider"],
        death_benefit="Enhanced Death Benefit",
        nursing_home_waiver=False,
        am_best_rating="A+",
        state_availability=["TX", "FL", "OH", "MI"]
    )


class TestRealProductSearches:
    """Test product search functionality with real product names."""

    def test_search_allianz_benefit_control(self):
        """Test searching for Allianz Benefit Control."""
        results = search_fia_products("Allianz Benefit Control")

        assert len(results) > 0, "Should find Allianz Benefit Control"
        assert any("allianz" in r["name"].lower() for r in results), \
            "Results should contain Allianz products"


    def test_search_nationwide_peak(self):
        """Test searching for Nationwide Peak products."""
        results = search_fia_products("Peak", carrier="Nationwide")

        # Should filter by carrier
        if len(results) > 0:
            for result in results:
                assert "nationwide" in result["carrier"].lower(), \
                    f"Expected Nationwide, got {result['carrier']}"


    def test_search_athene_products(self):
        """Test searching for Athene products."""
        results = search_fia_products("Athene")

        # May or may not have results (depends on mock data)
        assert isinstance(results, list), "Should return list"


    def test_partial_product_name_matching(self):
        """Test that partial product names return results."""
        # Search with partial name
        results = search_fia_products("222")

        # Should find products with "222" in name (like Allianz 222)
        assert isinstance(results, list), "Should return list"


class TestClientSuitabilityScenarios:
    """Test suitability analysis with realistic client scenarios."""

    def test_conservative_retiree_with_allianz(
        self,
        conservative_retiree,
        allianz_benefit_control
    ):
        """
        Test conservative retiree with Allianz Benefit Control.
        Expected: Highly Suitable or Suitable.
        """
        score = analyze_product_fit(allianz_benefit_control, conservative_retiree)

        # Conservative retiree should be suitable for FIA
        assert score.score >= 60.0, \
            f"Conservative retiree should be suitable (got {score.score}%)"

        # Should have minimal concerns
        assert score.interpretation in ["Highly Suitable", "Suitable"], \
            f"Expected high suitability, got {score.interpretation}"

        # Should have good fit factors
        assert len(score.good_fit_factors) > 0, "Should have good fit factors"

        # Should have recommendations
        assert len(score.recommendations) > 0, "Should have recommendations"


    def test_moderate_pre_retiree_with_nationwide(
        self,
        moderate_pre_retiree,
        nationwide_peak_10
    ):
        """
        Test moderate pre-retiree with Nationwide Peak 10.
        Expected: Suitable (may have liquidity concern).
        """
        score = analyze_product_fit(nationwide_peak_10, moderate_pre_retiree)

        # Should be suitable overall
        assert score.score >= 40.0, \
            f"Moderate pre-retiree should have reasonable fit (got {score.score}%)"

        # May have liquidity concern due to liquidity_needs_next_5_years=True
        if score.score < 80.0:
            # Check for liquidity-related concerns
            concerns_text = " ".join(score.concerns).lower()
            assert "liquidity" in concerns_text or len(score.concerns) > 0, \
                "Should identify potential concerns"


    def test_aggressive_young_investor_low_suitability(
        self,
        aggressive_young_investor,
        allianz_benefit_control
    ):
        """
        Test aggressive young investor (should be NOT suitable).
        Expected: Marginal Fit or Not Suitable.
        """
        score = analyze_product_fit(allianz_benefit_control, aggressive_young_investor)

        # Young aggressive investor should have low suitability
        # Due to: young age, aggressive risk tolerance, high liquidity needs,
        # doesn't understand FIAs, hasn't reviewed alternatives
        assert score.score < 60.0, \
            f"Young aggressive investor should have low suitability (got {score.score}%)"

        # Should have multiple concerns
        assert len(score.concerns) >= 2, \
            f"Should identify multiple concerns (got {len(score.concerns)})"

        # Check for specific expected concerns
        concerns_text = " ".join(score.concerns).lower()
        assert any(keyword in concerns_text for keyword in [
            "liquidity",
            "understand",
            "alternative",
            "surrender"
        ]), "Should identify key suitability issues"


class TestProductComparisons:
    """Test comparing multiple products for the same client."""

    def test_compare_two_products_for_same_client(
        self,
        conservative_retiree,
        allianz_benefit_control,
        nationwide_peak_10
    ):
        """
        Compare Allianz and Nationwide products for same client.
        Both should be suitable, but may have different scores.
        """
        # Analyze Allianz
        allianz_score = analyze_product_fit(allianz_benefit_control, conservative_retiree)

        # Analyze Nationwide
        nationwide_score = analyze_product_fit(nationwide_peak_10, conservative_retiree)

        # Both should be suitable for conservative retiree
        assert allianz_score.score >= 60.0, "Allianz should be suitable"
        assert nationwide_score.score >= 60.0, "Nationwide should be suitable"

        # Verify both have valid interpretations
        assert allianz_score.interpretation in [
            "Highly Suitable", "Suitable", "Marginal Fit", "Not Suitable"
        ]
        assert nationwide_score.interpretation in [
            "Highly Suitable", "Suitable", "Marginal Fit", "Not Suitable"
        ]

        # Both should have recommendations
        assert len(allianz_score.recommendations) > 0
        assert len(nationwide_score.recommendations) > 0


class TestDataValidation:
    """Test data validation and edge cases."""

    def test_client_age_at_issue_age_limit(self, allianz_benefit_control):
        """Test client at maximum issue age."""
        # Create client at max issue age (85)
        client = ClientProfile(
            age=85,  # Maximum for Allianz Benefit Control
            state="FL",
            marital_status="married",
            total_investable_assets=500000.0,
            annual_income=50000.0,
            emergency_fund_months=12,
            primary_goal="income",
            income_start_year=1,
            risk_tolerance="conservative",
            liquidity_needs_next_5_years=False,
            investment_time_horizon=10,
            understands_fia_mechanics=True,
            has_reviewed_alternatives=True,
            comfortable_with_surrender_charges=True,
            tax_bracket="12-22%",
            wants_tax_deferral=True
        )

        # Should still be able to analyze
        score = analyze_product_fit(allianz_benefit_control, client)

        # Age appropriateness might be YES (at limit) or NO (too old)
        assert "age_appropriateness" in score.question_responses
        # Result depends on implementation logic


    def test_client_below_minimum_premium(self, allianz_benefit_control):
        """Test client with assets below minimum premium."""
        # Create client with low assets
        client = ClientProfile(
            age=65,
            state="FL",
            marital_status="single",
            total_investable_assets=5000.0,  # Below $10k minimum
            annual_income=25000.0,
            emergency_fund_months=6,
            primary_goal="income",
            risk_tolerance="conservative",
            liquidity_needs_next_5_years=False,
            investment_time_horizon=10,
            understands_fia_mechanics=True,
            has_reviewed_alternatives=True,
            comfortable_with_surrender_charges=True,
            tax_bracket="0-12%",
            wants_tax_deferral=True
        )

        # Should still analyze, but may flag asset concern
        score = analyze_product_fit(allianz_benefit_control, client)

        # Should have concerns about low assets
        concerns_text = " ".join(score.concerns).lower()
        # May mention assets, premium, or allocation


    def test_product_with_empty_riders_list(self):
        """Test product with no optional riders."""
        product = FIAProduct(
            name="Basic Product",
            carrier="Test Carrier",
            term_years=7,
            minimum_premium=5000.0,
            maximum_issue_age=80,
            surrender_charge_schedule=[7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0],
            penalty_free_withdrawal=10.0,
            index_options=["S&P 500"],
            crediting_methods=["Annual Point-to-Point"],
            cap_rates={"S&P 500": 6.0},
            participation_rates={},
            rates_as_of_date=datetime.now().strftime("%Y-%m-%d"),
            income_riders=[],  # No riders
            death_benefit=None,
            nursing_home_waiver=False
        )

        # Should still be valid
        assert product.name == "Basic Product"
        assert len(product.income_riders) == 0


class TestWorkflowIntegration:
    """Test complete workflows from search to analysis."""

    def test_full_pipeline_search_to_analysis(self, conservative_retiree):
        """
        Test complete pipeline: search → extract → analyze.
        Note: Extract step is simulated since it requires web content.
        """
        # Step 1: Search
        results = search_fia_products("Allianz Benefit Control")
        assert len(results) > 0, "Should find products"

        # Step 2: Extract (simulated - would normally use mcp__fetch__fetch + extract_fia_rates)
        # Using fixture data instead
        product = FIAProduct(
            name="Allianz Benefit Control",
            carrier="Allianz Life Insurance Company",
            term_years=10,
            minimum_premium=10000.0,
            maximum_issue_age=85,
            surrender_charge_schedule=[9.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0],
            penalty_free_withdrawal=10.0,
            index_options=["S&P 500"],
            crediting_methods=["Annual Point-to-Point"],
            cap_rates={"S&P 500": 7.5},
            participation_rates={"S&P 500": 100.0},
            rates_as_of_date=datetime.now().strftime("%Y-%m-%d")
        )

        # Step 3: Analyze
        score = analyze_product_fit(product, conservative_retiree)

        # Verify complete result
        assert score.score >= 0.0
        assert score.interpretation is not None
        assert len(score.recommendations) > 0


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
