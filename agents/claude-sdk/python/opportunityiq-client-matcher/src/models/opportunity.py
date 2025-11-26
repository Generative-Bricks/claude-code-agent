"""
Opportunity data models for OpportunityIQ Client Matcher.

Defines matched opportunities and their associated data (match scores,
revenue calculations, rankings).

EXCELLENCE Principle: Structured output ensures reliable downstream processing.
"""

from typing import Optional, Literal, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class MatchDetail(BaseModel):
    """
    Details of how a criterion was matched.

    Provides transparency into the matching process for each criterion.
    """
    criterion_field: str = Field(..., description="Field that was evaluated")
    operator: str = Field(..., description="Operator used for comparison")
    expected_value: Any = Field(..., description="Value the criterion expected")
    actual_value: Any = Field(..., description="Actual value from client profile")
    matched: bool = Field(..., description="Whether the criterion was met")
    weight: float = Field(..., ge=0.0, le=1.0, description="Weight of this criterion")
    points_earned: float = Field(..., ge=0.0, description="Points earned from this criterion")


class RevenueCalculation(BaseModel):
    """
    Detailed breakdown of revenue calculation.

    Shows how estimated revenue was computed for transparency.
    """
    formula_type: str = Field(..., description="Type of formula used")
    base_rate: float = Field(..., description="Base rate applied")
    multiplier_value: Optional[float] = Field(None, description="Value used as multiplier")
    calculated_amount: float = Field(..., ge=0.0, description="Raw calculated revenue")
    final_amount: float = Field(..., ge=0.0, description="Final revenue after min/max adjustments")
    min_applied: bool = Field(default=False, description="Whether minimum revenue was applied")
    max_applied: bool = Field(default=False, description="Whether maximum revenue cap was applied")


class Opportunity(BaseModel):
    """
    A matched opportunity for a specific client and scenario.

    Represents the complete matching result including scores, revenue,
    and ranking information.
    """
    opportunity_id: str = Field(..., description="Unique identifier for this opportunity")
    client_id: str = Field(..., description="Client identifier")
    client_name: str = Field(..., description="Client name for display")
    scenario_id: str = Field(..., description="Scenario identifier")
    scenario_name: str = Field(..., description="Scenario name for display")
    scenario_category: str = Field(..., description="Scenario category")

    # Match scoring
    match_score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Match score as percentage (0-100)"
    )
    match_details: list[MatchDetail] = Field(
        ...,
        description="Detailed breakdown of criterion matching"
    )
    total_criteria: int = Field(..., ge=1, description="Total number of criteria evaluated")
    criteria_met: int = Field(..., ge=0, description="Number of criteria that were met")

    # Revenue estimation
    estimated_revenue: float = Field(..., ge=0.0, description="Estimated revenue in USD")
    revenue_calculation: RevenueCalculation = Field(
        ...,
        description="Detailed revenue calculation breakdown"
    )

    # Ranking and priority
    priority: Literal["high", "medium", "low"] = Field(
        ...,
        description="Priority level from scenario"
    )
    rank: Optional[int] = Field(
        None,
        ge=1,
        description="Rank within result set (1 = highest priority)"
    )
    composite_score: Optional[float] = Field(
        None,
        ge=0.0,
        description="Composite score combining match and revenue for ranking"
    )

    # Additional metadata
    estimated_time_hours: Optional[float] = Field(
        None,
        ge=0.0,
        description="Estimated advisor time required"
    )
    required_licenses: Optional[list[str]] = Field(
        None,
        description="Required licenses to execute opportunity"
    )
    compliance_notes: Optional[str] = Field(
        None,
        description="Compliance considerations"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when opportunity was created"
    )

    @field_validator("match_score")
    @classmethod
    def validate_match_score_range(cls, v: float) -> float:
        """Ensure match score is between 0 and 100."""
        if not 0.0 <= v <= 100.0:
            raise ValueError("Match score must be between 0 and 100")
        return v

    @field_validator("criteria_met")
    @classmethod
    def validate_criteria_met(cls, v: int, info) -> int:
        """Ensure criteria_met doesn't exceed total_criteria."""
        total = info.data.get("total_criteria", 0)
        if v > total:
            raise ValueError("criteria_met cannot exceed total_criteria")
        return v

    def is_high_value(self, revenue_threshold: float = 5000.0) -> bool:
        """
        Determine if this is a high-value opportunity.

        Args:
            revenue_threshold: Minimum revenue to be considered high-value

        Returns:
            True if estimated revenue exceeds threshold
        """
        return self.estimated_revenue >= revenue_threshold

    def is_quick_win(
        self,
        time_threshold: float = 2.0,
        score_threshold: float = 80.0
    ) -> bool:
        """
        Determine if this is a quick win opportunity.

        Quick wins are high-match, low-effort opportunities.

        Args:
            time_threshold: Maximum hours to qualify as quick
            score_threshold: Minimum match score to qualify

        Returns:
            True if meets quick win criteria
        """
        if self.estimated_time_hours is None:
            return False
        return (
            self.match_score >= score_threshold and
            self.estimated_time_hours <= time_threshold
        )
