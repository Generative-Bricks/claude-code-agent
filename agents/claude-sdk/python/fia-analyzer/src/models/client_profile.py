"""
Client Profile Model

This module defines the Pydantic model for client information used in the
40-question suitability assessment framework.

Biblical Principle: HONOR - Client data sovereignty and user-first design.
All fields are optional to respect incomplete data scenarios.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ClientProfile(BaseModel):
    """
    Client profile for FIA suitability analysis.

    This model captures all information needed for the 40-question suitability
    framework defined in the FIA Analysis Skill. All fields are optional since
    not all data may be available during initial assessments.

    The framework uses N/A scoring for missing data - questions without data
    are excluded from the suitability score calculation.

    Example:
        ```python
        client = ClientProfile(
            age=62,
            state="Texas",
            total_investable_assets=500000,
            annual_income=80000,
            has_emergency_fund=True,
            primary_investment_objective="Retirement income with principal protection",
            risk_tolerance="Conservative",
            needs_liquidity_near_term=False,
            is_in_good_health=True,
            time_horizon_years=20
        )
        ```
    """

    # === Demographics ===
    age: Optional[int] = Field(
        default=None,
        description="Client's current age"
    )
    state: Optional[str] = Field(
        default=None,
        description="State of residence (affects product availability)"
    )

    # === Financial Situation ===
    total_investable_assets: Optional[float] = Field(
        default=None,
        description="Total investable assets (excluding primary residence)"
    )
    annual_income: Optional[float] = Field(
        default=None,
        description="Annual household income"
    )
    has_emergency_fund: Optional[bool] = Field(
        default=None,
        description="Has 3-6 months emergency reserves outside this investment"
    )
    proposed_premium_amount: Optional[float] = Field(
        default=None,
        description="Amount client is considering investing in FIA"
    )
    percentage_of_portfolio: Optional[float] = Field(
        default=None,
        description="Percentage of total assets this investment represents"
    )
    can_afford_surrender_charges: Optional[bool] = Field(
        default=None,
        description="Can afford surrender charges if early access needed"
    )

    # === Investment Objectives ===
    primary_investment_objective: Optional[str] = Field(
        default=None,
        description="Primary goal (e.g., 'retirement income', 'accumulation', 'legacy')"
    )
    seeks_principal_protection: Optional[bool] = Field(
        default=None,
        description="Prioritizes principal protection from market downturns"
    )
    seeks_tax_deferral: Optional[bool] = Field(
        default=None,
        description="Interested in tax-deferred growth"
    )
    wants_guaranteed_lifetime_income: Optional[bool] = Field(
        default=None,
        description="Wants guaranteed income for life"
    )
    comfortable_with_expected_returns: Optional[bool] = Field(
        default=None,
        description="Comfortable with realistic FIA return expectations (3-6% annually)"
    )

    # === Risk Tolerance ===
    risk_tolerance: Optional[str] = Field(
        default=None,
        description="Risk tolerance level: 'Conservative', 'Moderate', or 'Aggressive'"
    )
    uncomfortable_with_market_volatility: Optional[bool] = Field(
        default=None,
        description="Uncomfortable with stock market volatility"
    )
    prioritizes_safety_over_growth: Optional[bool] = Field(
        default=None,
        description="Prioritizes safety over maximum growth potential"
    )
    accepts_limited_upside_for_protection: Optional[bool] = Field(
        default=None,
        description="Willing to accept limited upside for downside protection"
    )

    # === Liquidity Needs ===
    needs_large_lump_sum_withdrawals: Optional[bool] = Field(
        default=None,
        description="Anticipates needing large lump-sum withdrawals"
    )
    comfortable_with_structured_withdrawals: Optional[bool] = Field(
        default=None,
        description="Comfortable with structured lifetime withdrawal percentages"
    )
    has_other_liquid_assets: Optional[bool] = Field(
        default=None,
        description="Has other liquid assets for unexpected expenses"
    )
    needs_liquidity_near_term: Optional[bool] = Field(
        default=None,
        description="Needs significant liquidity in next 2-3 years"
    )

    # === Time Horizon ===
    can_commit_funds_for_term: Optional[bool] = Field(
        default=None,
        description="Can commit funds for full contract term (e.g., 10 years)"
    )
    time_horizon_years: Optional[int] = Field(
        default=None,
        description="Investment time horizon in years"
    )
    expects_to_benefit_from_lifetime_income: Optional[bool] = Field(
        default=None,
        description="Expects to live long enough to benefit from lifetime income"
    )

    # === Understanding & Complexity ===
    understands_not_direct_market_investment: Optional[bool] = Field(
        default=None,
        description="Understands this is not a direct market investment"
    )
    comfortable_with_index_complexity: Optional[bool] = Field(
        default=None,
        description="Comfortable with complexity of multiple index options"
    )
    understands_bonus_limitations: Optional[bool] = Field(
        default=None,
        description="Understands bonus/income value limitations"
    )
    understands_surrender_charges: Optional[bool] = Field(
        default=None,
        description="Understands surrender charges and fee structure"
    )

    # === Health Status ===
    is_in_good_health: Optional[bool] = Field(
        default=None,
        description="In good health with no immediate terminal diagnoses"
    )
    values_long_term_care_benefits: Optional[bool] = Field(
        default=None,
        description="Values long-term care benefits (if product offers them)"
    )
    concerned_about_outliving_assets: Optional[bool] = Field(
        default=None,
        description="Concerned about outliving retirement assets"
    )

    # === Tax Situation ===
    will_benefit_from_tax_deferral: Optional[bool] = Field(
        default=None,
        description="Will benefit from tax-deferred growth"
    )
    understands_withdrawal_tax_treatment: Optional[bool] = Field(
        default=None,
        description="Understands tax treatment of withdrawals"
    )
    is_over_59_and_half: Optional[bool] = Field(
        default=None,
        description="Age 59½ or older (avoids early withdrawal penalty)"
    )
    willing_to_wait_or_accept_penalty: Optional[bool] = Field(
        default=None,
        description="If under 59½, willing to wait or accept early withdrawal penalty"
    )

    # === Alternative Considerations ===
    rejected_direct_stock_investing: Optional[bool] = Field(
        default=None,
        description="Rejected direct stock investing due to risk concerns"
    )
    compared_alternatives: Optional[bool] = Field(
        default=None,
        description="Compared to alternatives (MYGAs, SPIAs, other FIAs)"
    )
    understands_commission_structure: Optional[bool] = Field(
        default=None,
        description="Understands commission structure and potential conflicts"
    )

    # === Product-Specific Interests ===
    interested_in_unique_features: Optional[bool] = Field(
        default=None,
        description="Interested in product-specific unique features"
    )
    wants_income_start_flexibility: Optional[bool] = Field(
        default=None,
        description="Wants flexibility in when income starts"
    )
    attracted_to_bonus_features: Optional[bool] = Field(
        default=None,
        description="Attracted to bonus features (if applicable)"
    )
    values_accumulation_and_income_combo: Optional[bool] = Field(
        default=None,
        description="Values combination of accumulation and income features"
    )

    # === Disqualifying Factor Checks ===
    needs_aggressive_growth: Optional[bool] = Field(
        default=None,
        description="Needs aggressive growth (8-10%+ annually)"
    )
    planning_major_purchases_near_term: Optional[bool] = Field(
        default=None,
        description="Planning major purchases requiring lump sums in near term"
    )
    views_as_entire_retirement_portfolio: Optional[bool] = Field(
        default=None,
        description="Views this as entire retirement portfolio (not diversified)"
    )

    # === Additional Context ===
    additional_notes: Optional[str] = Field(
        default=None,
        description="Any additional context or notes about the client"
    )
    existing_annuities: Optional[List[str]] = Field(
        default=None,
        description="List of existing annuities the client owns"
    )
    other_retirement_accounts: Optional[List[str]] = Field(
        default=None,
        description="Other retirement accounts (e.g., '401k', 'IRA', 'Pension')"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "age": 62,
                "state": "Texas",
                "total_investable_assets": 500000,
                "annual_income": 80000,
                "has_emergency_fund": True,
                "proposed_premium_amount": 100000,
                "percentage_of_portfolio": 20.0,
                "primary_investment_objective": "Retirement income with principal protection",
                "risk_tolerance": "Conservative",
                "needs_liquidity_near_term": False,
                "is_in_good_health": True,
                "time_horizon_years": 20,
                "understands_not_direct_market_investment": True
            }
        }
