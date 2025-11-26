"""
Scenario model definitions for revenue opportunity matching.

This module defines the structure of scenarios that can be matched against client profiles
to identify revenue opportunities. Each scenario contains matching criteria and revenue formulas.
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field

# Type alias for scenario categories
ScenarioCategory = Literal[
    "annuity",
    "insurance",
    "investment",
    "planning",
    "tax_strategy",
    "estate_planning",
    "other"
]


class MatchCriterion(BaseModel):
    """
    Defines a single matching criterion for a scenario.

    A criterion specifies a field to check, an operator for comparison,
    the expected value, and a weight for scoring.
    """

    field: str = Field(
        ...,
        description="The client profile field to evaluate (e.g., 'age', 'risk_tolerance')"
    )
    operator: Literal["eq", "gt", "gte", "lt", "lte", "contains", "in_range"] = Field(
        ...,
        description="Comparison operator to apply"
    )
    value: str | int | float | List[str | int | float] = Field(
        ...,
        description="The expected value or range to match against"
    )
    weight: float = Field(
        default=1.0,
        ge=0.0,
        le=10.0,
        description="Weight for this criterion in scoring (0-10)"
    )


class RevenueTier(BaseModel):
    """
    Defines a tier in a tiered revenue calculation.

    Used for scenarios where revenue rates change based on thresholds
    (e.g., different commission rates for different portfolio sizes).
    """

    threshold_min: float = Field(
        ...,
        ge=0.0,
        description="Minimum value for this tier (inclusive)"
    )
    threshold_max: Optional[float] = Field(
        default=None,
        ge=0.0,
        description="Maximum value for this tier (exclusive), None for unlimited"
    )
    rate: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Revenue rate for this tier (as decimal, e.g., 0.05 for 5%)"
    )


class RevenueFormula(BaseModel):
    """
    Defines how to calculate revenue for a matched scenario.

    Supports multiple formula types including fixed amounts, percentages,
    tiered calculations, and multiplier-based calculations.
    """

    formula_type: Literal["fixed", "percentage", "tiered", "multiplier"] = Field(
        ...,
        description="Type of revenue calculation to perform"
    )
    base_rate: Optional[float] = Field(
        default=None,
        ge=0.0,
        description="Base rate for percentage or multiplier formulas"
    )
    fixed_amount: Optional[float] = Field(
        default=None,
        ge=0.0,
        description="Fixed revenue amount (used when formula_type is 'fixed')"
    )
    min_revenue: Optional[float] = Field(
        default=None,
        ge=0.0,
        description="Minimum revenue cap"
    )
    max_revenue: Optional[float] = Field(
        default=None,
        ge=0.0,
        description="Maximum revenue cap"
    )
    tiers: Optional[List[RevenueTier]] = Field(
        default=None,
        description="Tiers for tiered revenue calculations"
    )
    multiplier_field: Optional[str] = Field(
        default=None,
        description="Client field to use as multiplier (e.g., 'portfolio.total_value')"
    )


class Scenario(BaseModel):
    """
    Represents a revenue opportunity scenario.

    A scenario defines the criteria for matching clients and the formula
    for calculating potential revenue from the opportunity.
    """

    scenario_id: str = Field(
        ...,
        description="Unique identifier for this scenario"
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Human-readable name for the scenario"
    )
    description: str = Field(
        ...,
        min_length=1,
        description="Detailed description of the opportunity"
    )
    category: Literal[
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
    criteria: List[MatchCriterion] = Field(
        ...,
        min_length=1,
        description="List of criteria that must be evaluated for matching"
    )
    revenue_formula: RevenueFormula = Field(
        ...,
        description="Formula for calculating potential revenue"
    )
    priority: Literal["high", "medium", "low"] = Field(
        default="medium",
        description="Priority level for this opportunity"
    )
    required_licenses: Optional[List[str]] = Field(
        default=None,
        description="Required licenses or certifications to pursue this opportunity"
    )
    compliance_notes: Optional[str] = Field(
        default=None,
        description="Important compliance or regulatory notes"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "scenario_id": "fia_conservative_growth",
                "name": "Conservative Growth FIA",
                "description": "Fixed Indexed Annuity for conservative investors seeking growth with protection",
                "category": "annuity",
                "criteria": [
                    {
                        "field": "risk_tolerance",
                        "operator": "eq",
                        "value": "conservative",
                        "weight": 3.0
                    },
                    {
                        "field": "age",
                        "operator": "gte",
                        "value": 55,
                        "weight": 2.0
                    }
                ],
                "revenue_formula": {
                    "formula_type": "percentage",
                    "base_rate": 0.05,
                    "multiplier_field": "portfolio.total_value",
                    "min_revenue": 1000.0,
                    "max_revenue": 50000.0
                },
                "priority": "high",
                "required_licenses": ["Series 6", "State Insurance License"],
                "compliance_notes": "Ensure suitability documentation is complete"
            }
        }
