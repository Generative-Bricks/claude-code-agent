"""
Integration tests for the full FIA Analyzer workflow.

Tests end-to-end functionality including:
- Product search
- Product extraction
- Suitability analysis
- Error handling
"""

import pytest
import json
from pathlib import Path
from src.agent import FIAAnalyzerAgent
from src.models import ClientProfile


# Test data directory
TEST_DATA_DIR = Path(__file__).parent.parent.parent / "examples"


@pytest.fixture
def sample_client_profile():
    """Load sample client profile from examples directory."""
    client_file = TEST_DATA_DIR / "sample_client.json"

    if not client_file.exists():
        # Create minimal test client profile
        return ClientProfile(
            age=65,
            state="TX",
            marital_status="married",
            total_investable_assets=500000.0,
            annual_income=80000.0,
            emergency_fund_months=12,
            primary_goal="income",
            income_start_year=2,
            risk_tolerance="conservative",
            liquidity_needs_next_5_years=False,
            investment_time_horizon=10,
            understands_fia_mechanics=True,
            has_reviewed_alternatives=True,
            comfortable_with_surrender_charges=True,
            tax_bracket="22-24%",
            wants_tax_deferral=True
        )

    with open(client_file, 'r') as f:
        data = json.load(f)

    return ClientProfile(**data)


@pytest.fixture
def agent():
    """Create FIA Analyzer Agent instance for testing."""
    # Note: This will require ANTHROPIC_API_KEY in environment
    # For true integration tests, use a real API key
    # For CI/CD, mock the Anthropic client
    try:
        return FIAAnalyzerAgent()
    except Exception as e:
        pytest.skip(f"Cannot initialize agent (likely missing API key): {e}")


class TestFullWorkflow:
    """Test complete end-to-end workflows."""

    def test_basic_product_search_workflow(self):
        """
        Test basic product search without suitability analysis.

        Workflow:
        1. Search for product by name
        2. Verify search returns results
        3. Verify result structure
        """
        from src.tools.search_fia_products import search_fia_products

        # Search for known product
        results = search_fia_products("Allianz Benefit Control")

        # Verify results
        assert len(results) > 0, "Should find at least one product"
        assert isinstance(results, list), "Results should be a list"

        # Verify result structure
        first_result = results[0]
        assert "name" in first_result, "Result should have 'name' field"
        assert "carrier" in first_result, "Result should have 'carrier' field"
        assert "url" in first_result, "Result should have 'url' field"
        assert "summary" in first_result, "Result should have 'summary' field"

        # Verify product name matches
        assert "allianz" in first_result["name"].lower(), "Product name should contain 'allianz'"


    def test_product_not_found_handling(self):
        """
        Test error handling when product is not found.

        Expected behavior:
        - Search returns empty list for non-existent product
        - No exceptions raised
        """
        from src.tools.search_fia_products import search_fia_products

        # Search for non-existent product
        results = search_fia_products("NonExistentProduct12345")

        # Should return empty list, not raise exception
        assert isinstance(results, list), "Should return list even when no results"
        assert len(results) == 0, "Should return empty list for non-existent product"


    def test_search_with_carrier_filter(self):
        """
        Test product search with carrier filtering.

        Workflow:
        1. Search with carrier filter
        2. Verify all results match carrier
        """
        from src.tools.search_fia_products import search_fia_products

        # Search with carrier filter
        results = search_fia_products("Peak", carrier="Nationwide")

        # Verify results are filtered by carrier
        if len(results) > 0:
            for result in results:
                assert "nationwide" in result["carrier"].lower(), \
                    f"Expected Nationwide carrier, got {result['carrier']}"


    def test_suitability_analysis_workflow(self, sample_client_profile):
        """
        Test complete suitability analysis workflow.

        Workflow:
        1. Search for product
        2. Create mock product data
        3. Analyze suitability for client
        4. Verify scoring and recommendations
        """
        from src.tools.search_fia_products import search_fia_products
        from src.tools.analyze_product_fit import analyze_product_fit
        from src.models import FIAProduct
        from datetime import datetime

        # Step 1: Search for product
        results = search_fia_products("Allianz Benefit Control")
        assert len(results) > 0, "Should find product"

        # Step 2: Create product instance (in real workflow, would use extract tool)
        product = FIAProduct(
            name="Allianz Benefit Control",
            carrier="Allianz Life",
            term_years=10,
            minimum_premium=10000.0,
            maximum_issue_age=85,
            surrender_charge_schedule=[9.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0],
            penalty_free_withdrawal=10.0,
            index_options=["S&P 500", "Nasdaq-100"],
            crediting_methods=["Annual Point-to-Point", "Monthly Average"],
            cap_rates={"S&P 500": 7.5, "Nasdaq-100": 6.0},
            participation_rates={"S&P 500": 100.0},
            rates_as_of_date=datetime.now().strftime("%Y-%m-%d"),
            income_riders=["Guaranteed Lifetime Withdrawal Benefit"],
            death_benefit="Return of Premium",
            nursing_home_waiver=True,
            am_best_rating="A+",
            state_availability=["TX", "CA", "FL"]
        )

        # Step 3: Analyze suitability
        score = analyze_product_fit(product, sample_client_profile)

        # Step 4: Verify scoring
        assert score.score >= 0.0, "Score should be non-negative"
        assert score.score <= 100.0, "Score should not exceed 100%"
        assert score.interpretation in [
            "Highly Suitable",
            "Suitable",
            "Marginal Fit",
            "Not Suitable"
        ], f"Invalid interpretation: {score.interpretation}"

        # Verify score components
        assert isinstance(score.good_fit_factors, list), "Good fit factors should be a list"
        assert isinstance(score.concerns, list), "Concerns should be a list"
        assert isinstance(score.recommendations, list), "Recommendations should be a list"

        # Verify question responses
        assert len(score.question_responses) > 0, "Should have question responses"
        for question_id, response in score.question_responses.items():
            assert response in ["YES", "NO", "N/A"], \
                f"Invalid response '{response}' for question {question_id}"


    def test_extract_rates_from_markdown(self):
        """
        Test extracting product rates from markdown content.

        Workflow:
        1. Create sample markdown content
        2. Extract product data
        3. Verify extracted fields
        """
        from src.tools.extract_fia_rates import extract_fia_rates

        # Sample markdown content (minimal valid structure)
        markdown_content = """
# Allianz Benefit Control

**Carrier:** Allianz Life Insurance Company
**Product Type:** Fixed Indexed Annuity
**Term:** 10 years
**Minimum Premium:** $10,000
**Maximum Issue Age:** 85

## Surrender Charges

| Year | Surrender Charge |
|------|-----------------|
| 1-2  | 9%              |
| 3    | 8%              |
| 4    | 7%              |
| 5    | 6%              |
| 6    | 5%              |
| 7    | 4%              |
| 8    | 3%              |
| 9    | 2%              |
| 10   | 1%              |

**Penalty-Free Withdrawal:** 10% annually

## Index Options and Rates

| Index | Crediting Method | Cap Rate | Participation Rate |
|-------|-----------------|----------|-------------------|
| S&P 500 | Annual Point-to-Point | 7.5% | 100% |
| Nasdaq-100 | Monthly Average | 6.0% | 90% |

**Rates as of:** 2025-01-15

## Riders

- Guaranteed Lifetime Withdrawal Benefit (GLWB)
- Enhanced Death Benefit

## Features

- **Death Benefit:** Return of Premium
- **Nursing Home Waiver:** Yes
- **A.M. Best Rating:** A+
- **State Availability:** All states except NY
"""

        # Extract product data
        product = extract_fia_rates(markdown_content, "Allianz Benefit Control")

        # Verify extracted data
        assert product.name == "Allianz Benefit Control"
        assert product.carrier == "Allianz Life Insurance Company"
        assert product.term_years == 10
        assert product.minimum_premium == 10000.0
        assert product.maximum_issue_age == 85

        # Verify surrender charges
        assert len(product.surrender_charge_schedule) == 10
        assert product.surrender_charge_schedule[0] == 9.0
        assert product.surrender_charge_schedule[-1] == 1.0

        # Verify rates
        assert "S&P 500" in product.cap_rates
        assert product.cap_rates["S&P 500"] == 7.5

        # Verify optional fields
        assert product.nursing_home_waiver is True
        assert product.am_best_rating == "A+"


    def test_missing_required_fields_raises_error(self):
        """
        Test that extract tool raises ValueError for missing required fields.

        This is correct production behavior - fail fast with clear error.
        """
        from src.tools.extract_fia_rates import extract_fia_rates

        # Incomplete markdown (missing surrender charges)
        incomplete_markdown = """
# Test Product

**Carrier:** Test Carrier
**Term:** 10 years
**Minimum Premium:** $10,000
"""

        # Should raise ValueError for missing required fields
        with pytest.raises(ValueError) as exc_info:
            extract_fia_rates(incomplete_markdown, "Test Product")

        # Verify error message is helpful
        assert "required" in str(exc_info.value).lower() or \
               "missing" in str(exc_info.value).lower() or \
               "surrender" in str(exc_info.value).lower(), \
               "Error message should mention missing required field"


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_client_profile_edge_cases(self):
        """Test ClientProfile validation with edge case values."""
        from src.models import ClientProfile

        # Test minimum valid age
        client = ClientProfile(
            age=18,  # Minimum valid age
            state="TX",
            marital_status="single",
            total_investable_assets=1000.0,
            annual_income=20000.0,
            emergency_fund_months=1,
            primary_goal="tax_deferral",
            risk_tolerance="conservative",
            liquidity_needs_next_5_years=False,
            investment_time_horizon=1,
            understands_fia_mechanics=True,
            has_reviewed_alternatives=True,
            comfortable_with_surrender_charges=True,
            tax_bracket="0-12%",
            wants_tax_deferral=True
        )
        assert client.age == 18

        # Test maximum valid age
        client.age = 100
        assert client.age == 100

        # Test zero assets (valid but unusual)
        client.total_investable_assets = 0.0
        assert client.total_investable_assets == 0.0


    def test_suitability_score_with_all_na_responses(self):
        """Test suitability scoring when all questions are N/A."""
        from src.models import SuitabilityScore
        from datetime import datetime

        # Create score with all N/A responses
        score = SuitabilityScore(
            score=0.0,
            interpretation="Not Suitable",
            question_responses={
                "q1": "N/A",
                "q2": "N/A",
                "q3": "N/A"
            },
            good_fit_factors=[],
            concerns=["All questions answered N/A - insufficient data for analysis"],
            recommendations=["Gather more client information and re-evaluate"],
            analysis_date=datetime.now().strftime("%Y-%m-%d")
        )

        # Verify score is valid even with all N/A
        assert score.score == 0.0
        assert len(score.concerns) > 0


    def test_product_with_minimal_data(self):
        """Test FIAProduct creation with only required fields."""
        from src.models import FIAProduct
        from datetime import datetime

        # Create product with minimal required data
        product = FIAProduct(
            name="Minimal Product",
            carrier="Test Carrier",
            term_years=5,
            minimum_premium=5000.0,
            maximum_issue_age=80,
            surrender_charge_schedule=[5.0, 4.0, 3.0, 2.0, 1.0],
            penalty_free_withdrawal=10.0,
            index_options=["S&P 500"],
            crediting_methods=["Annual Point-to-Point"],
            cap_rates={"S&P 500": 5.0},
            participation_rates={},
            rates_as_of_date=datetime.now().strftime("%Y-%m-%d")
        )

        # Verify creation succeeds
        assert product.name == "Minimal Product"
        assert product.term_years == 5

        # Verify optional fields have defaults
        assert product.income_riders == []
        assert product.death_benefit is None
        assert product.nursing_home_waiver is False


class TestAgentIntegration:
    """Test agent integration (requires API key)."""

    @pytest.mark.skip(reason="Requires valid ANTHROPIC_API_KEY and makes real API calls")
    def test_agent_initialization(self, agent):
        """Test that agent initializes correctly with skills container."""
        assert agent is not None
        # Additional assertions would go here if we want to verify
        # skills container setup, but that requires inspecting agent internals


    @pytest.mark.skip(reason="Requires valid ANTHROPIC_API_KEY and makes real API calls")
    def test_agent_basic_conversation(self, agent):
        """Test basic agent conversation flow."""
        # This would test actual agent execution
        # Skipped to avoid real API calls in automated tests
        pass


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
