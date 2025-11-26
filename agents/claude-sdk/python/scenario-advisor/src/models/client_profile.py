"""
Client profile model definitions.

This module defines the structure of client profiles including demographics,
financial information, portfolio holdings, and investment preferences.
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class Holdings(BaseModel):
    """
    Represents a single holding in a client's portfolio.

    Includes both the asset details and current valuation information.
    """

    symbol: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Ticker symbol or identifier for the holding"
    )
    asset_type: Literal[
        "stock",
        "bond",
        "mutual_fund",
        "etf",
        "annuity",
        "cash",
        "real_estate",
        "alternative",
        "other"
    ] = Field(
        ...,
        description="Type of asset"
    )
    quantity: float = Field(
        ...,
        ge=0.0,
        description="Number of shares or units held"
    )
    current_value: float = Field(
        ...,
        ge=0.0,
        description="Current market value of the holding"
    )
    cost_basis: Optional[float] = Field(
        default=None,
        ge=0.0,
        description="Original purchase price (for tax purposes)"
    )


class Portfolio(BaseModel):
    """
    Represents a client's complete investment portfolio.

    Includes total value, allocations, and individual holdings.
    """

    total_value: float = Field(
        ...,
        ge=0.0,
        description="Total current value of all holdings"
    )
    cash_value: float = Field(
        default=0.0,
        ge=0.0,
        description="Amount held in cash or cash equivalents"
    )
    equity_allocation: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Percentage allocated to equities (as decimal)"
    )
    fixed_income_allocation: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Percentage allocated to fixed income (as decimal)"
    )
    holdings: List[Holdings] = Field(
        default_factory=list,
        description="Individual holdings in the portfolio"
    )


class ClientProfile(BaseModel):
    """
    Represents a complete client profile.

    Includes demographics, financial information, investment preferences,
    and portfolio details. Optional FIA-specific fields are included for
    annuity-related scenario matching.
    """

    # Required demographic fields
    client_id: str = Field(
        ...,
        description="Unique identifier for the client"
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Client's full name"
    )
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Client's age in years"
    )

    # Investment profile
    risk_tolerance: Literal["conservative", "moderate", "aggressive"] = Field(
        ...,
        description="Client's risk tolerance level"
    )
    investment_objective: Literal[
        "growth",
        "income",
        "preservation",
        "balanced",
        "speculation"
    ] = Field(
        ...,
        description="Primary investment objective"
    )
    time_horizon_years: int = Field(
        ...,
        ge=1,
        le=50,
        description="Investment time horizon in years"
    )

    # Financial information
    annual_income: float = Field(
        ...,
        ge=0.0,
        description="Annual income in dollars"
    )
    net_worth: float = Field(
        ...,
        ge=0.0,
        description="Total net worth in dollars"
    )

    # Portfolio
    portfolio: Portfolio = Field(
        ...,
        description="Client's investment portfolio"
    )

    # Optional FIA-specific fields
    existing_annuities: Optional[List[str]] = Field(
        default=None,
        description="List of existing annuity products the client holds"
    )
    income_start_age: Optional[int] = Field(
        default=None,
        ge=50,
        le=100,
        description="Desired age to start receiving annuity income"
    )
    guaranteed_income_desired: Optional[bool] = Field(
        default=None,
        description="Whether client desires guaranteed lifetime income"
    )
    protection_priority: Optional[Literal["high", "medium", "low"]] = Field(
        default=None,
        description="Priority level for principal protection"
    )
    liquidity_needs: Optional[Literal["high", "medium", "low"]] = Field(
        default=None,
        description="Client's need for liquidity access"
    )
    tax_bracket: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Current tax bracket (as decimal)"
    )
    state: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=2,
        description="State of residence (2-letter code)"
    )

    # Additional metadata
    notes: Optional[str] = Field(
        default=None,
        description="Additional notes about the client"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "client_id": "CLT-001",
                "name": "John Smith",
                "age": 62,
                "risk_tolerance": "conservative",
                "investment_objective": "income",
                "time_horizon_years": 15,
                "annual_income": 85000.0,
                "net_worth": 750000.0,
                "portfolio": {
                    "total_value": 500000.0,
                    "cash_value": 50000.0,
                    "equity_allocation": 0.4,
                    "fixed_income_allocation": 0.5,
                    "holdings": [
                        {
                            "symbol": "VTI",
                            "asset_type": "etf",
                            "quantity": 500,
                            "current_value": 200000.0,
                            "cost_basis": 180000.0
                        }
                    ]
                },
                "guaranteed_income_desired": True,
                "protection_priority": "high",
                "liquidity_needs": "low",
                "tax_bracket": 0.22,
                "state": "TX"
            }
        }
