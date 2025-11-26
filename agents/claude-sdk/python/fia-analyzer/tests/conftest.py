"""
Pytest configuration and shared fixtures for FIA Analyzer tests.

Biblical Principle: EXCELLENCE - Reusable, well-structured test fixtures.
"""

import pytest
from datetime import date
from src.models import FIAProduct, ClientProfile, SuitabilityScore, QuestionResult
from src.models.fia_product import (
    SurrenderCharge,
    IndexOption,
    CurrentRate,
    Rider,
    CompanyInfo,
)


# ==================== FIA Product Fixtures ====================

@pytest.fixture
def sample_surrender_charges():
    """Sample surrender charge schedule."""
    return [
        SurrenderCharge(year=1, percentage=9.0),
        SurrenderCharge(year=2, percentage=8.5),
        SurrenderCharge(year=3, percentage=8.0),
        SurrenderCharge(year=4, percentage=7.0),
        SurrenderCharge(year=5, percentage=6.0),
        SurrenderCharge(year=6, percentage=5.0),
        SurrenderCharge(year=7, percentage=4.0),
        SurrenderCharge(year=8, percentage=3.0),
        SurrenderCharge(year=9, percentage=2.0),
        SurrenderCharge(year=10, percentage=1.0),
    ]


@pytest.fixture
def sample_index_options():
    """Sample index options for a FIA product."""
    return [
        IndexOption(
            name="S&P 500 Price Return",
            description="Tracks S&P 500 without dividends",
            crediting_methods=["Annual Point-to-Point"],
            characteristics=["widely-tracked", "low-volatility"],
            is_affiliated=False,
        ),
        IndexOption(
            name="PIMCO Tactical Balanced",
            description="Multi-asset tactical allocation index",
            crediting_methods=["Annual Point-to-Point", "Monthly Sum"],
            characteristics=["volatility-controlled", "diversified"],
            is_affiliated=True,
        ),
    ]


@pytest.fixture
def sample_current_rates():
    """Sample current rates for index options."""
    return [
        CurrentRate(
            index_name="S&P 500 Price Return",
            crediting_method="Annual Point-to-Point",
            cap_rate=5.5,
            participation_rate=None,
        ),
        CurrentRate(
            index_name="PIMCO Tactical Balanced",
            crediting_method="Annual Point-to-Point",
            cap_rate=None,
            participation_rate=100.0,
        ),
    ]


@pytest.fixture
def sample_riders():
    """Sample riders for a FIA product."""
    return [
        Rider(
            name="Guaranteed Lifetime Withdrawal Benefit (GLWB)",
            description="Provides guaranteed income for life",
            is_built_in=False,
            cost="0.95% annually",
            withdrawal_percentages={"60": 4.0, "65": 5.0, "70": 6.0},
        ),
        Rider(
            name="Death Benefit",
            description="Pays higher of account value or premium to beneficiary",
            is_built_in=True,
            cost="No cost",
        ),
    ]


@pytest.fixture
def sample_company_info():
    """Sample company information."""
    return CompanyInfo(
        issuer="Allianz Life Insurance Company of North America",
        parent_company="Allianz SE",
        financial_strength_ratings={"AM Best": "A+", "S&P": "AA"},
        years_in_business=125,
        market_position="Top 5 FIA provider in US market",
    )


@pytest.fixture
def sample_fia_product(
    sample_surrender_charges,
    sample_index_options,
    sample_current_rates,
    sample_riders,
    sample_company_info,
):
    """Complete sample FIA product for testing."""
    return FIAProduct(
        name="Allianz Benefit Control",
        product_type="Fixed Indexed Annuity",
        contract_term=10,
        minimum_premium=25000.0,
        premium_payment_options=["Single Premium"],
        surrender_charges=sample_surrender_charges,
        has_mva=False,
        free_withdrawal_provision="10% annually after year 1",
        index_options=sample_index_options,
        available_crediting_methods=[
            "Annual Point-to-Point",
            "Monthly Sum",
            "Monthly Average",
        ],
        minimum_guaranteed_rate=1.0,
        current_rates=sample_current_rates,
        rates_as_of_date=date(2024, 1, 15),
        riders=sample_riders,
        special_features=[
            "Income Base bonus of 10% in year 1",
            "Step-up provision every 5 years",
        ],
        issuer=sample_company_info,
        data_collected_date=date.today(),
        data_source="carrier website",
    )


# ==================== Client Profile Fixtures ====================

@pytest.fixture
def sample_conservative_client():
    """Sample conservative client profile."""
    return ClientProfile(
        age=62,
        state="Texas",
        total_investable_assets=500000,
        annual_income=80000,
        has_emergency_fund=True,
        proposed_premium_amount=100000,
        percentage_of_portfolio=20.0,
        can_afford_surrender_charges=True,
        primary_investment_objective="Retirement income with principal protection",
        seeks_principal_protection=True,
        seeks_tax_deferral=True,
        wants_guaranteed_lifetime_income=True,
        comfortable_with_expected_returns=True,
        risk_tolerance="Conservative",
        uncomfortable_with_market_volatility=True,
        prioritizes_safety_over_growth=True,
        accepts_limited_upside_for_protection=True,
        needs_large_lump_sum_withdrawals=False,
        comfortable_with_structured_withdrawals=True,
        has_other_liquid_assets=True,
        needs_liquidity_near_term=False,
        can_commit_funds_for_term=True,
        time_horizon_years=20,
        expects_to_benefit_from_lifetime_income=True,
        understands_not_direct_market_investment=True,
        comfortable_with_index_complexity=True,
        understands_surrender_charges=True,
        is_in_good_health=True,
        is_over_59_and_half=True,
    )


@pytest.fixture
def sample_aggressive_client():
    """Sample aggressive client profile (poor fit for FIA)."""
    return ClientProfile(
        age=35,
        state="California",
        total_investable_assets=200000,
        annual_income=150000,
        has_emergency_fund=True,
        proposed_premium_amount=50000,
        percentage_of_portfolio=25.0,
        primary_investment_objective="Aggressive growth",
        risk_tolerance="Aggressive",
        needs_aggressive_growth=True,
        uncomfortable_with_market_volatility=False,
        prioritizes_safety_over_growth=False,
        needs_liquidity_near_term=True,
        time_horizon_years=5,
    )


@pytest.fixture
def sample_incomplete_client():
    """Client profile with missing data (tests N/A handling)."""
    return ClientProfile(
        age=55,
        state="Florida",
        total_investable_assets=300000,
        # Most fields intentionally missing to test N/A scoring
    )


# ==================== Mock Data Fixtures ====================

@pytest.fixture
def sample_markdown_content():
    """Sample markdown content for rate extraction testing."""
    return """
# Allianz Benefit Control

## Product Overview
Contract Term: 10 years
Minimum Premium: $25,000

## Current Rates (as of January 15, 2024)

### S&P 500 Price Return
- Annual Point-to-Point: 5.5% cap rate

### PIMCO Tactical Balanced
- Annual Point-to-Point: 100% participation rate

## Surrender Charges
Year 1: 9%
Year 2: 8.5%
Year 3: 8%
Year 4: 7%
Year 5: 6%
Year 6: 5%
Year 7: 4%
Year 8: 3%
Year 9: 2%
Year 10: 1%

## Riders Available
- Guaranteed Lifetime Withdrawal Benefit: 0.95% annually
  - Age 60: 4% withdrawal rate
  - Age 65: 5% withdrawal rate
  - Age 70: 6% withdrawal rate

## Company Information
Issuer: Allianz Life Insurance Company of North America
Financial Strength: A+ (AM Best), AA (S&P)
"""


@pytest.fixture
def sample_search_results():
    """Sample search results from search_fia_products tool."""
    return {
        "products": [
            {
                "name": "Allianz Benefit Control",
                "carrier": "Allianz Life",
                "url": "https://www.allianzlife.com/products/annuities/benefit-control",
                "summary": "Fixed indexed annuity with 10-year term...",
            }
        ]
    }


# ==================== Suitability Score Fixtures ====================

@pytest.fixture
def sample_question_results():
    """Sample question results for suitability testing."""
    return [
        QuestionResult(
            question_id=1,
            question_text="Client has sufficient assets for minimum premium",
            answer="YES",
            rationale="Client has $500,000 total assets",
            category="Financial Capacity",
        ),
        QuestionResult(
            question_id=2,
            question_text="Can commit funds for full 10-year term",
            answer="YES",
            rationale="Client confirmed 20-year time horizon",
            category="Time Horizon",
        ),
        QuestionResult(
            question_id=3,
            question_text="Needs aggressive growth (8-10%+ annually)",
            answer="NO",
            rationale="Client seeks conservative income, not aggressive growth",
            category="Risk Tolerance",
        ),
        QuestionResult(
            question_id=4,
            question_text="Has documented health insurance",
            answer="N/A",
            rationale="Insufficient data",
            category="Health Status",
        ),
    ]


@pytest.fixture
def sample_suitability_score(sample_question_results):
    """Sample suitability score for testing."""
    return SuitabilityScore(
        total_yes=2,
        total_no=1,
        total_na=1,
        question_breakdown=sample_question_results,
        good_fit_factors=[
            "Client seeks principal protection",
            "Conservative risk tolerance aligns with FIA structure",
            "Has adequate emergency reserves",
        ],
        not_a_fit_factors=["Client may need liquidity in near term"],
        recommendations=[
            "Discuss surrender charge schedule in detail",
            "Ensure free withdrawal provision is understood",
        ],
        product_name="Allianz Benefit Control",
        client_name="John Doe",
    )
