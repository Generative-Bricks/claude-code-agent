"""
Opportunity model definitions for matched revenue opportunities.

This module defines the structure of matched opportunities, including
match scoring details and revenue calculations.
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class MatchDetail(BaseModel):
    """
    Details about how a specific criterion was matched.

    Provides transparency into the matching process by showing
    what was expected, what was found, and how it was scored.
    """

    criterion_field: str = Field(
        ...,
        description="The field that was evaluated"
    )
    operator: str = Field(
        ...,
        description="The operator used for comparison"
    )
    expected_value: str | int | float | List[str | int | float] = Field(
        ...,
        description="The value expected by the scenario criterion"
    )
    actual_value: str | int | float | None = Field(
        ...,
        description="The actual value from the client profile"
    )
    matched: bool = Field(
        ...,
        description="Whether the criterion was successfully matched"
    )
    weight: float = Field(
        ...,
        ge=0.0,
        le=10.0,
        description="Weight assigned to this criterion"
    )
    points_earned: float = Field(
        ...,
        ge=0.0,
        description="Points earned from this criterion (0 if not matched)"
    )


class RevenueCalculation(BaseModel):
    """
    Details about how revenue was calculated for an opportunity.

    Provides transparency into the revenue calculation process,
    showing the formula used and the resulting amounts.
    """

    formula_type: Literal["fixed", "percentage", "tiered", "multiplier"] = Field(
        ...,
        description="Type of formula used for calculation"
    )
    base_rate: Optional[float] = Field(
        default=None,
        ge=0.0,
        description="Base rate used in calculation"
    )
    multiplier_value: Optional[float] = Field(
        default=None,
        ge=0.0,
        description="Value used as multiplier (e.g., portfolio value)"
    )
    calculated_amount: float = Field(
        ...,
        ge=0.0,
        description="Raw calculated revenue before caps"
    )
    final_amount: float = Field(
        ...,
        ge=0.0,
        description="Final revenue after applying min/max caps"
    )
    applied_cap: Optional[Literal["min", "max"]] = Field(
        default=None,
        description="Whether a min or max cap was applied"
    )


class Opportunity(BaseModel):
    """
    Represents a matched revenue opportunity for a client.

    Contains complete information about the match including scoring details,
    revenue calculation, and prioritization for advisor action.
    """

    opportunity_id: str = Field(
        ...,
        description="Unique identifier for this opportunity"
    )
    client_id: str = Field(
        ...,
        description="ID of the client this opportunity is for"
    )
    client_name: str = Field(
        ...,
        description="Name of the client for easy reference"
    )
    scenario_id: str = Field(
        ...,
        description="ID of the scenario that was matched"
    )
    scenario_name: str = Field(
        ...,
        description="Name of the scenario for easy reference"
    )
    scenario_category: Literal[
        "annuity",
        "insurance",
        "investment",
        "planning",
        "tax_strategy",
        "estate_planning",
        "other"
    ] = Field(
        ...,
        description="Category of the revenue opportunity"
    )
    match_score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Overall match score (0-100)"
    )
    match_details: List[MatchDetail] = Field(
        ...,
        min_length=1,
        description="Detailed breakdown of how each criterion was matched"
    )
    estimated_revenue: float = Field(
        ...,
        ge=0.0,
        description="Estimated revenue from this opportunity"
    )
    revenue_calculation: RevenueCalculation = Field(
        ...,
        description="Details about how revenue was calculated"
    )
    priority: Literal["high", "medium", "low"] = Field(
        ...,
        description="Priority level for advisor action"
    )
    rank: Optional[int] = Field(
        default=None,
        ge=1,
        description="Rank among all opportunities (1 is highest)"
    )
    required_licenses: Optional[List[str]] = Field(
        default=None,
        description="Licenses required to pursue this opportunity"
    )
    compliance_notes: Optional[str] = Field(
        default=None,
        description="Important compliance or regulatory notes"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "opportunity_id": "OPP-001-SCN-001",
                "client_id": "CLT-001",
                "client_name": "John Smith",
                "scenario_id": "fia_conservative_growth",
                "scenario_name": "Conservative Growth FIA",
                "scenario_category": "annuity",
                "match_score": 85.5,
                "match_details": [
                    {
                        "criterion_field": "risk_tolerance",
                        "operator": "eq",
                        "expected_value": "conservative",
                        "actual_value": "conservative",
                        "matched": True,
                        "weight": 3.0,
                        "points_earned": 3.0
                    }
                ],
                "estimated_revenue": 25000.0,
                "revenue_calculation": {
                    "formula_type": "percentage",
                    "base_rate": 0.05,
                    "multiplier_value": 500000.0,
                    "calculated_amount": 25000.0,
                    "final_amount": 25000.0,
                    "applied_cap": None
                },
                "priority": "high",
                "rank": 1,
                "required_licenses": ["Series 6", "State Insurance License"],
                "compliance_notes": "Ensure suitability documentation is complete"
            }
        }
