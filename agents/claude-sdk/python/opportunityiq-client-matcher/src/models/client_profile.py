"""
Client profile data models for OpportunityIQ Client Matcher.

Defines the structure of client data used for matching against scenarios.

HONOR Principle: Client data is structured for privacy and clear data sovereignty.
"""

from typing import Optional, Literal
from datetime import date
from pydantic import BaseModel, Field, field_validator, computed_field, ConfigDict


class Holdings(BaseModel):
    """
    Individual holdings within a client's portfolio.

    Represents specific assets (stocks, bonds, funds) held by the client.
    """
    symbol: str = Field(..., description="Asset ticker symbol (e.g., 'AAPL', 'VTSAX')")
    asset_type: Literal["stock", "bond", "mutual_fund", "etf", "cash", "alternative"] = Field(
        ...,
        description="Type of asset"
    )
    quantity: float = Field(..., ge=0.0, description="Number of shares or units held")
    current_value: float = Field(..., ge=0.0, description="Current market value of holding")
    cost_basis: Optional[float] = Field(None, ge=0.0, description="Original purchase cost")
    purchase_date: Optional[date] = Field(None, description="Date asset was purchased")

    @computed_field
    @property
    def unrealized_gain_loss(self) -> Optional[float]:
        """Calculate unrealized gain or loss if cost basis is available."""
        if self.cost_basis is not None:
            return self.current_value - self.cost_basis
        return None

    @computed_field
    @property
    def gain_loss_percentage(self) -> Optional[float]:
        """Calculate percentage gain or loss if cost basis is available."""
        if self.cost_basis is not None and self.cost_basis > 0:
            return ((self.current_value - self.cost_basis) / self.cost_basis) * 100
        return None


class Portfolio(BaseModel):
    """
    Client's investment portfolio with holdings and allocation.

    Aggregates all assets and provides portfolio-level metrics.
    """
    total_value: float = Field(..., ge=0.0, description="Total portfolio value in USD")
    cash_value: float = Field(default=0.0, ge=0.0, description="Cash holdings in USD")
    equity_allocation: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Percentage allocated to equities (stocks, ETFs)"
    )
    fixed_income_allocation: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Percentage allocated to bonds"
    )
    alternative_allocation: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Percentage allocated to alternatives"
    )
    holdings: list[Holdings] = Field(
        default_factory=list,
        description="List of individual holdings"
    )
    last_rebalance_date: Optional[date] = Field(
        None,
        description="Date portfolio was last rebalanced"
    )

    @field_validator("equity_allocation", "fixed_income_allocation", "alternative_allocation")
    @classmethod
    def validate_percentage(cls, v: float) -> float:
        """Ensure allocation percentages are between 0 and 100."""
        if not 0.0 <= v <= 100.0:
            raise ValueError("Allocation percentage must be between 0 and 100")
        return v

    @computed_field
    @property
    def total_allocation_percentage(self) -> float:
        """Calculate total allocation percentage (should be close to 100)."""
        return (
            self.equity_allocation +
            self.fixed_income_allocation +
            self.alternative_allocation
        )

    @computed_field
    @property
    def number_of_holdings(self) -> int:
        """Count total number of holdings in portfolio."""
        return len(self.holdings)


class ClientProfile(BaseModel):
    """
    Complete client profile for opportunity matching.

    Contains all relevant client information needed to evaluate
    financial opportunity scenarios.

    Note: Extra fields are allowed to support scenario-specific data
    (e.g., fia_value, cash_percentage, etc.)
    """
    model_config = ConfigDict(extra='allow')

    client_id: str = Field(..., description="Unique client identifier")
    name: str = Field(..., description="Client full name")
    age: int = Field(..., ge=18, le=120, description="Client age in years")
    risk_tolerance: Literal["conservative", "moderate", "aggressive"] = Field(
        ...,
        description="Client's risk tolerance level"
    )
    investment_objective: Literal[
        "growth",
        "income",
        "balanced",
        "capital_preservation"
    ] = Field(..., description="Primary investment objective")
    time_horizon_years: int = Field(
        ...,
        ge=1,
        description="Investment time horizon in years"
    )
    annual_income: float = Field(..., ge=0.0, description="Annual income in USD")
    net_worth: float = Field(..., ge=0.0, description="Total net worth in USD")
    liquidity_needs: Literal["low", "medium", "high"] = Field(
        ...,
        description="Need for liquid assets"
    )
    tax_bracket: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Marginal tax bracket percentage"
    )
    has_estate_plan: bool = Field(
        default=False,
        description="Whether client has an estate plan"
    )
    portfolio: Portfolio = Field(..., description="Client's investment portfolio")
    advisor_notes: Optional[str] = Field(
        None,
        description="Additional advisor notes about client"
    )
    last_review_date: Optional[date] = Field(
        None,
        description="Date of last portfolio review"
    )

    @field_validator("age")
    @classmethod
    def validate_age_range(cls, v: int) -> int:
        """Ensure age is within reasonable range."""
        if not 18 <= v <= 120:
            raise ValueError("Age must be between 18 and 120")
        return v

    @field_validator("tax_bracket")
    @classmethod
    def validate_tax_bracket(cls, v: float) -> float:
        """Ensure tax bracket is between 0 and 100."""
        if not 0.0 <= v <= 100.0:
            raise ValueError("Tax bracket must be between 0 and 100")
        return v

    @computed_field
    @property
    def portfolio_value(self) -> float:
        """Alias for portfolio.total_value for easier access in matching."""
        return self.portfolio.total_value

    @computed_field
    @property
    def retirement_age_estimate(self) -> int:
        """Estimate retirement age based on time horizon."""
        return self.age + self.time_horizon_years
