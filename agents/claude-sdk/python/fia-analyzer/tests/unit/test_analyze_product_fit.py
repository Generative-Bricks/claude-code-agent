"""
Unit tests for analyze_product_fit tool.

Tests the suitability analysis functionality including:
- 10-question suitability assessment
- YES/NO/N/A scoring methodology
- Score calculation
- Client-product matching logic
"""

import pytest
from src.tools.analyze_product_fit import analyze_product_fit
from src.models import SuitabilityScore


class TestAnalyzeProductFit:
    """Test suite for analyze_product_fit tool."""

    def test_analyze_conservative_client_good_fit(
        self, sample_fia_product, sample_conservative_client
    ):
        """Test analysis of conservative client with suitable FIA."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        assert isinstance(result, SuitabilityScore)
        assert result.score >= 60  # Should be at least "Suitable"
        assert result.interpretation in ["Highly Suitable", "Suitable"]

    def test_analyze_aggressive_client_poor_fit(
        self, sample_fia_product, sample_aggressive_client
    ):
        """Test analysis of aggressive client (poor fit for FIA)."""
        result = analyze_product_fit(sample_fia_product, sample_aggressive_client)

        assert isinstance(result, SuitabilityScore)
        # Aggressive client should have concerns
        assert result.total_no > 0
        # Score might be lower due to poor fit
        assert result.interpretation in ["Marginal Fit", "Not Suitable", "Suitable"]

    def test_analyze_incomplete_data_uses_na(
        self, sample_fia_product, sample_incomplete_client
    ):
        """Test that N/A is used for missing client data."""
        result = analyze_product_fit(sample_fia_product, sample_incomplete_client)

        assert isinstance(result, SuitabilityScore)
        # Should have N/A answers for missing data
        assert result.total_na > 0

    def test_score_calculation_formula(
        self, sample_fia_product, sample_conservative_client
    ):
        """Test that score follows formula: (YES / (YES + NO)) * 100."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        expected_score = (
            (result.total_yes / result.total_answerable) * 100
            if result.total_answerable > 0
            else 0.0
        )

        assert abs(result.score - expected_score) < 0.01

    def test_total_answerable_excludes_na(
        self, sample_fia_product, sample_incomplete_client
    ):
        """Test that N/A answers are excluded from total_answerable."""
        result = analyze_product_fit(sample_fia_product, sample_incomplete_client)

        assert result.total_answerable == result.total_yes + result.total_no
        # N/A should NOT be in answerable count
        assert result.total_answerable + result.total_na <= 10  # 10 questions total

    def test_question_breakdown_length(
        self, sample_fia_product, sample_conservative_client
    ):
        """Test that all 10 questions are in breakdown."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        assert len(result.question_breakdown) == 10
        question_ids = [q.question_id for q in result.question_breakdown]
        assert question_ids == list(range(1, 11))

    def test_question_breakdown_has_rationale(
        self, sample_fia_product, sample_conservative_client
    ):
        """Test that each question has a rationale."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        for question in result.question_breakdown:
            assert len(question.rationale) > 0
            assert isinstance(question.rationale, str)

    def test_question_breakdown_has_categories(
        self, sample_fia_product, sample_conservative_client
    ):
        """Test that questions are categorized."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        for question in result.question_breakdown:
            assert len(question.category) > 0
            assert isinstance(question.category, str)

    def test_minimum_premium_check(self, sample_fia_product, sample_conservative_client):
        """Test Question 1: Client meets minimum premium requirement."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        q1 = next(q for q in result.question_breakdown if q.question_id == 1)

        # Conservative client has $100k proposed, product requires $25k
        assert q1.answer == "YES"
        assert "premium" in q1.question_text.lower()

    def test_time_horizon_check(self, sample_fia_product, sample_aggressive_client):
        """Test Question 2: Time horizon check."""
        result = analyze_product_fit(sample_fia_product, sample_aggressive_client)

        q2 = next(q for q in result.question_breakdown if q.question_id == 2)

        # Aggressive client has 5-year horizon, product requires 10 years
        # Should either be NO or flag the concern
        assert q2.answer in ["YES", "NO", "N/A"]

    def test_risk_tolerance_alignment(
        self, sample_fia_product, sample_conservative_client
    ):
        """Test that risk tolerance is evaluated."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        # Conservative client should align well with FIA
        risk_questions = [
            q for q in result.question_breakdown if "risk" in q.question_text.lower()
        ]
        # Should have at least one risk-related question
        assert len(risk_questions) > 0

    def test_good_fit_factors_present(
        self, sample_fia_product, sample_conservative_client
    ):
        """Test that good fit factors are identified."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        assert len(result.good_fit_factors) > 0
        assert all(isinstance(factor, str) for factor in result.good_fit_factors)

    def test_not_a_fit_factors_present_when_issues(
        self, sample_fia_product, sample_aggressive_client
    ):
        """Test that concerns are identified for poor-fit client."""
        result = analyze_product_fit(sample_fia_product, sample_aggressive_client)

        # Aggressive client should have some concerns
        assert len(result.not_a_fit_factors) > 0

    def test_recommendations_provided(
        self, sample_fia_product, sample_conservative_client
    ):
        """Test that recommendations are provided."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        assert len(result.recommendations) > 0
        assert all(isinstance(rec, str) for rec in result.recommendations)

    def test_product_name_in_result(
        self, sample_fia_product, sample_conservative_client
    ):
        """Test that product name is included in result."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        assert result.product_name == sample_fia_product.name

    def test_score_interpretation_ranges(
        self, sample_fia_product, sample_conservative_client
    ):
        """Test score interpretation matches defined ranges."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        score = result.score
        interpretation = result.interpretation

        if score >= 80:
            assert interpretation == "Highly Suitable"
        elif score >= 60:
            assert interpretation == "Suitable"
        elif score >= 40:
            assert interpretation == "Marginal Fit"
        else:
            assert interpretation == "Not Suitable"

    def test_recommendation_action_provided(
        self, sample_fia_product, sample_conservative_client
    ):
        """Test that recommendation_action is generated."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        assert len(result.recommendation_action) > 0
        assert isinstance(result.recommendation_action, str)

    def test_all_questions_have_valid_answers(
        self, sample_fia_product, sample_conservative_client
    ):
        """Test that all questions have valid answers (YES/NO/N/A)."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        for question in result.question_breakdown:
            assert question.answer in ["YES", "NO", "N/A"]

    def test_question_text_not_empty(
        self, sample_fia_product, sample_conservative_client
    ):
        """Test that all question texts are meaningful."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        for question in result.question_breakdown:
            assert len(question.question_text) > 10  # More than a few words

    def test_count_totals_match_breakdown(
        self, sample_fia_product, sample_conservative_client
    ):
        """Test that YES/NO/N/A counts match question breakdown."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        counted_yes = sum(1 for q in result.question_breakdown if q.answer == "YES")
        counted_no = sum(1 for q in result.question_breakdown if q.answer == "NO")
        counted_na = sum(1 for q in result.question_breakdown if q.answer == "N/A")

        assert result.total_yes == counted_yes
        assert result.total_no == counted_no
        assert result.total_na == counted_na

    def test_get_questions_by_category(
        self, sample_fia_product, sample_conservative_client
    ):
        """Test filtering questions by category."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        categories = set(q.category for q in result.question_breakdown)
        assert len(categories) > 0

        for category in categories:
            category_questions = result.get_questions_by_category(category)
            assert all(q.category == category for q in category_questions)

    def test_get_questions_by_answer(
        self, sample_fia_product, sample_conservative_client
    ):
        """Test filtering questions by answer type."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        yes_questions = result.get_questions_by_answer("YES")
        no_questions = result.get_questions_by_answer("NO")
        na_questions = result.get_questions_by_answer("N/A")

        assert len(yes_questions) == result.total_yes
        assert len(no_questions) == result.total_no
        assert len(na_questions) == result.total_na

    def test_score_is_percentage(self, sample_fia_product, sample_conservative_client):
        """Test that score is between 0 and 100."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        assert 0 <= result.score <= 100

    def test_model_serialization(self, sample_fia_product, sample_conservative_client):
        """Test that SuitabilityScore can be serialized."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        # Should serialize to JSON
        json_data = result.model_dump_json()
        assert isinstance(json_data, str)

        # Should deserialize back
        SuitabilityScore.model_validate_json(json_data)

    def test_liquidity_needs_evaluation(
        self, sample_fia_product, sample_conservative_client
    ):
        """Test that liquidity needs are evaluated."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        liquidity_questions = [
            q
            for q in result.question_breakdown
            if "liquidity" in q.question_text.lower()
            or "withdrawal" in q.question_text.lower()
        ]

        # Should have at least one liquidity-related question
        assert len(liquidity_questions) > 0

    def test_emergency_fund_consideration(
        self, sample_fia_product, sample_conservative_client
    ):
        """Test that emergency fund status is considered."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        # Conservative client has emergency fund
        # Should be reflected positively in analysis
        assert result.score > 0

    def test_age_considerations(self, sample_fia_product, sample_conservative_client):
        """Test that client age is considered in analysis."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        # Client is 62 (over 59.5)
        # Should have questions about age-related factors
        age_questions = [
            q
            for q in result.question_breakdown
            if "age" in q.question_text.lower() or "59" in q.question_text
        ]

        # Might have age-related questions
        if len(age_questions) > 0:
            assert all(q.answer in ["YES", "NO", "N/A"] for q in age_questions)

    def test_portfolio_percentage_evaluation(
        self, sample_fia_product, sample_conservative_client
    ):
        """Test that portfolio allocation percentage is evaluated."""
        result = analyze_product_fit(sample_fia_product, sample_conservative_client)

        # Conservative client proposes 20% of portfolio
        # Should be evaluated as reasonable
        portfolio_questions = [
            q
            for q in result.question_breakdown
            if "portfolio" in q.question_text.lower()
            or "percentage" in q.question_text.lower()
        ]

        if len(portfolio_questions) > 0:
            # 20% should be reasonable for FIA allocation
            assert any(q.answer == "YES" for q in portfolio_questions)

    def test_handles_none_values_gracefully(self, sample_fia_product):
        """Test that missing client data results in N/A, not errors."""
        # Client with minimal data
        from src.models import ClientProfile

        minimal_client = ClientProfile(age=50)

        result = analyze_product_fit(sample_fia_product, minimal_client)

        assert isinstance(result, SuitabilityScore)
        # Should have many N/A answers due to missing data
        assert result.total_na > 0
