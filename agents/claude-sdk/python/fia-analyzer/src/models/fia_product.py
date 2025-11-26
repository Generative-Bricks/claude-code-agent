"""
Fixed Indexed Annuity Product Model

This module defines the Pydantic model for representing a complete FIA product
with all features, rates, riders, and company information.

Biblical Principle: TRUTH - All product data is explicit, observable, and verifiable.
"""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class SurrenderCharge(BaseModel):
    """Surrender charge for a specific year."""

    year: int = Field(description="Year number (1-based)")
    percentage: float = Field(description="Surrender charge percentage (e.g., 9.0 for 9%)")


class IndexOption(BaseModel):
    """An available index allocation option."""

    name: str = Field(description="Full index name (e.g., 'S&P 500 Price Return')")
    description: str = Field(description="Brief description of the index")
    crediting_methods: List[str] = Field(
        description="Available crediting methods (e.g., 'Annual Point-to-Point', 'Monthly Sum')"
    )
    characteristics: List[str] = Field(
        default_factory=list,
        description="Index characteristics (e.g., 'volatility-controlled', 'diversified')"
    )
    is_affiliated: bool = Field(
        default=False,
        description="True if index is affiliated with carrier (e.g., PIMCO-Allianz)"
    )


class CurrentRate(BaseModel):
    """Current rate for a specific index and crediting method."""

    index_name: str = Field(description="Index name this rate applies to")
    crediting_method: str = Field(description="Crediting method (e.g., 'Annual Point-to-Point')")
    cap_rate: Optional[float] = Field(
        default=None,
        description="Cap rate percentage (e.g., 5.5 for 5.5%)"
    )
    participation_rate: Optional[float] = Field(
        default=None,
        description="Participation rate percentage (e.g., 100.0 for 100%)"
    )
    fixed_rate: Optional[float] = Field(
        default=None,
        description="Fixed interest rate percentage (e.g., 3.0 for 3%)"
    )


class Rider(BaseModel):
    """A rider (benefit option) available with the product."""

    name: str = Field(description="Rider name")
    description: str = Field(description="What the rider provides")
    is_built_in: bool = Field(
        default=False,
        description="True if included at no additional cost"
    )
    cost: Optional[str] = Field(
        default=None,
        description="Cost description (e.g., '0.95% annually' or 'No cost')"
    )
    withdrawal_percentages: Optional[dict] = Field(
        default=None,
        description="Withdrawal percentages by age (e.g., {'60': 4.0, '65': 5.0})"
    )


class CommissionStructure(BaseModel):
    """Commission information for the product."""

    typical_range: str = Field(
        description="Typical commission range (e.g., '5-7%')"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Additional commission notes"
    )


class CompanyInfo(BaseModel):
    """Information about the issuing company."""

    issuer: str = Field(description="Issuing insurance company name")
    parent_company: Optional[str] = Field(
        default=None,
        description="Parent company if different from issuer"
    )
    financial_strength_ratings: Optional[dict] = Field(
        default=None,
        description="Ratings by agency (e.g., {'AM Best': 'A+', 'S&P': 'AA'})"
    )
    years_in_business: Optional[int] = Field(
        default=None,
        description="Number of years the company has been in business"
    )
    market_position: Optional[str] = Field(
        default=None,
        description="Market position description"
    )


class FIAProduct(BaseModel):
    """
    Complete Fixed Indexed Annuity product model.

    This model represents all essential data points for a FIA product across
    the 9 data categories defined in the FIA Analysis Skill framework.

    Example:
        ```python
        product = FIAProduct(
            name="Allianz Benefit Control",
            product_type="Fixed Indexed Annuity",
            issuer=CompanyInfo(issuer="Allianz Life Insurance Company of North America"),
            contract_term=10,
            minimum_premium=25000,
            surrender_charges=[
                SurrenderCharge(year=1, percentage=9.0),
                SurrenderCharge(year=2, percentage=8.5),
                # ... etc
            ],
            # ... other fields
        )
        ```
    """

    # === Basic Product Information ===
    name: str = Field(description="Full product name")
    product_type: str = Field(
        default="Fixed Indexed Annuity",
        description="Product type (FIA, RILA, etc.)"
    )
    contract_term: int = Field(description="Contract term/surrender period in years")
    minimum_premium: float = Field(description="Minimum initial premium required")
    premium_payment_options: List[str] = Field(
        default_factory=lambda: ["Single Premium"],
        description="Available premium payment options"
    )

    # === Surrender Charges & Fees ===
    surrender_charges: List[SurrenderCharge] = Field(
        description="Surrender charge schedule by year"
    )
    has_mvа: bool = Field(
        default=False,
        description="True if Market Value Adjustment applies"
    )
    allocation_charges: Optional[dict] = Field(
        default=None,
        description="Allocation charges (e.g., {'current': 0.0, 'maximum': 2.0})"
    )
    free_withdrawal_provision: Optional[str] = Field(
        default="10% annually after year 1",
        description="Free withdrawal provisions"
    )

    # === Index Options ===
    index_options: List[IndexOption] = Field(
        description="All available index allocation options"
    )

    # === Crediting Methods ===
    available_crediting_methods: List[str] = Field(
        description="All crediting methods available (e.g., 'Annual Point-to-Point')"
    )
    minimum_guaranteed_rate: Optional[float] = Field(
        default=None,
        description="Minimum guaranteed interest rate (e.g., 1.0 for 1%)"
    )

    # === Current Rates ===
    current_rates: List[CurrentRate] = Field(
        default_factory=list,
        description="Current caps, participation rates, and fixed rates"
    )
    rates_as_of_date: Optional[date] = Field(
        default=None,
        description="Date when rate information was last verified"
    )

    # === Riders & Benefits ===
    riders: List[Rider] = Field(
        default_factory=list,
        description="All available riders (built-in and optional)"
    )

    # === Special Features ===
    special_features: List[str] = Field(
        default_factory=list,
        description="Unique product differentiators and special features"
    )
    bonus_structures: Optional[str] = Field(
        default=None,
        description="Bonus structure description if applicable"
    )

    # === Commission Structure ===
    commission: Optional[CommissionStructure] = Field(
        default=None,
        description="Commission structure information"
    )

    # === Company Information ===
    issuer: CompanyInfo = Field(description="Issuing company information")

    # === Metadata ===
    data_collected_date: date = Field(
        default_factory=date.today,
        description="Date when product information was collected"
    )
    data_source: Optional[str] = Field(
        default=None,
        description="Source of product information (e.g., 'carrier website', 'rate sheet')"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "name": "Allianz Benefit Control",
                "product_type": "Fixed Indexed Annuity",
                "contract_term": 10,
                "minimum_premium": 25000,
                "surrender_charges": [
                    {"year": 1, "percentage": 9.0},
                    {"year": 2, "percentage": 8.5},
                ],
                "index_options": [
                    {
                        "name": "S&P 500 Price Return",
                        "description": "Tracks S&P 500 without dividends",
                        "crediting_methods": ["Annual Point-to-Point"],
                        "characteristics": ["widely-tracked"],
                        "is_affiliated": False
                    }
                ],
                "issuer": {
                    "issuer": "Allianz Life Insurance Company of North America",
                    "financial_strength_ratings": {"AM Best": "A+"}
                }
            }
        }
