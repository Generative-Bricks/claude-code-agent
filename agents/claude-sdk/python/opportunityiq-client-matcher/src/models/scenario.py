"""
Scenario data models for OpportunityIQ Client Matcher.

Defines the structure of financial opportunity scenarios that can be matched
against client portfolios.

TRUTH Principle: All scenario attributes are explicit and traceable.
"""

from typing import Literal, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class MatchCriterion(BaseModel):
    """
    Defines a single matching criterion for a scenario.

    Each criterion specifies what client attribute to check and how to evaluate it.
    """
    field: str = Field(..., description="Client profile field to evaluate (e.g., 'age', 'portfolio_value')")
    operator: Literal["gt", "lt", "gte", "lte", "eq", "contains", "in"] = Field(
        ...,
        description="Comparison operator to apply"
    )
    value: Any = Field(..., description="Value to compare against")
    weight: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Weight of this criterion in overall match score (0.0-1.0)"
    )

    @field_validator("weight")
    @classmethod
    def validate_weight(cls, v: float) -> float:
        """Ensure weight is between 0.0 and 1.0."""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Weight must be between 0.0 and 1.0")
        return v


class RevenueFormula(BaseModel):
    """
    Defines how to calculate potential revenue from a scenario.

    Supports different calculation methods based on client data.
    """
    formula_type: Literal["percentage", "flat_fee", "tiered", "aum_based"] = Field(
        ...,
        description="Type of revenue calculation"
    )
    base_rate: float = Field(..., ge=0.0, description="Base rate or percentage for calculation")
    min_revenue: Optional[float] = Field(None, ge=0.0, description="Minimum revenue threshold")
    max_revenue: Optional[float] = Field(None, ge=0.0, description="Maximum revenue cap")
    tiers: Optional[Dict[str, float]] = Field(
        None,
        description="Tiered rates for tiered formula type (e.g., {'0-100000': 0.01, '100000+': 0.005})"
    )
    multiplier_field: Optional[str] = Field(
        None,
        description="Client field to multiply rate by (e.g., 'portfolio_value')"
    )

    @field_validator("max_revenue")
    @classmethod
    def validate_max_greater_than_min(cls, v: Optional[float], info) -> Optional[float]:
        """Ensure max_revenue is greater than min_revenue if both are set."""
        if v is not None and info.data.get("min_revenue") is not None:
            if v < info.data["min_revenue"]:
                raise ValueError("max_revenue must be greater than min_revenue")
        return v


class Scenario(BaseModel):
    """
    A financial opportunity scenario that can be matched to clients.

    Represents a specific advisory opportunity (e.g., annuity allocation,
    tax-loss harvesting) with matching criteria and revenue potential.
    """
    scenario_id: str = Field(..., description="Unique identifier for the scenario")
    name: str = Field(..., description="Human-readable scenario name")
    description: str = Field(..., description="Detailed description of the opportunity")
    category: Literal["annuity", "tax", "rebalance", "alternative_investment", "insurance"] = Field(
        ...,
        description="Category of financial opportunity"
    )
    criteria: list[MatchCriterion] = Field(
        ...,
        min_length=1,
        description="List of criteria for matching clients"
    )
    revenue_formula: RevenueFormula = Field(..., description="How to calculate potential revenue")
    priority: Literal["high", "medium", "low"] = Field(
        default="medium",
        description="Base priority level for this scenario"
    )
    required_licenses: Optional[list[str]] = Field(
        None,
        description="Required advisor licenses (e.g., ['Series 7', 'Series 65'])"
    )
    estimated_time_hours: Optional[float] = Field(
        None,
        ge=0.0,
        description="Estimated advisor time required in hours"
    )
    compliance_notes: Optional[str] = Field(
        None,
        description="Important compliance considerations"
    )

    @field_validator("criteria")
    @classmethod
    def validate_criteria_not_empty(cls, v: list[MatchCriterion]) -> list[MatchCriterion]:
        """Ensure at least one criterion is provided."""
        if not v:
            raise ValueError("At least one match criterion is required")
        return v

    def calculate_base_match_score(self) -> float:
        """
        Calculate the sum of all criterion weights.

        Used as the denominator when calculating match percentages.
        """
        return sum(criterion.weight for criterion in self.criteria)
