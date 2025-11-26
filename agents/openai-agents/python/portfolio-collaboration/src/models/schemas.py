"""
Pydantic models for Multi-Agent Portfolio Collaboration System.

This module defines all data structures used across the multi-agent system,
ensuring type safety and data validation throughout the workflow.

Biblical Principle: TRUTH - All data structures are explicitly defined and validated.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ============================================================================
# Base Model Configuration
# ============================================================================


class BaseModelWithConfig(BaseModel):
    """
    Base model with configuration for OpenAI Agents SDK compatibility.

    The OpenAI Agents SDK requires strict JSON schemas without additionalProperties.
    This configuration ensures Pydantic v2 models are compatible.
    """

    model_config = ConfigDict(
        extra='forbid',  # Don't allow extra fields
        use_enum_values=False,  # Keep enum objects, not values
    )

    @classmethod
    def model_json_schema(cls, **kwargs):
        """Override to remove additionalProperties from schema."""
        schema = super().model_json_schema(**kwargs)

        # Remove additionalProperties from the schema
        def remove_additional_properties(obj):
            if isinstance(obj, dict):
                obj.pop('additionalProperties', None)
                for value in obj.values():
                    remove_additional_properties(value)
            elif isinstance(obj, list):
                for item in obj:
                    remove_additional_properties(item)

        remove_additional_properties(schema)
        return schema


# ============================================================================
# Enumerations
# ============================================================================


class RiskTolerance(str, Enum):
    """Client risk tolerance levels."""

    CONSERVATIVE = "Conservative"
    MODERATE = "Moderate"
    AGGRESSIVE = "Aggressive"


class AssetClass(str, Enum):
    """Asset class categories."""

    EQUITY = "Equity"
    FIXED_INCOME = "Fixed Income"
    CASH = "Cash"
    ALTERNATIVES = "Alternatives"


class ComplianceStatus(str, Enum):
    """Compliance check status."""

    PASS = "PASS"
    FAIL = "FAIL"
    REVIEW = "REVIEW"


class RiskRating(str, Enum):
    """Portfolio risk rating."""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    VERY_HIGH = "Very High"


class SuitabilityRating(str, Enum):
    """Client-portfolio suitability rating."""

    HIGHLY_SUITABLE = "Highly Suitable"
    SUITABLE = "Suitable"
    MARGINAL_FIT = "Marginal Fit"
    NOT_SUITABLE = "Not Suitable"


# ============================================================================
# Client & Portfolio Models
# ============================================================================


class ClientProfile(BaseModelWithConfig):
    """
    Client profile containing demographics, risk tolerance, and investment objectives.

    Used in Stage 1: Client Discovery
    """

    client_id: str = Field(..., description="Unique client identifier")
    age: int = Field(..., ge=18, le=120, description="Client age")
    risk_tolerance: RiskTolerance = Field(
        ..., description="Risk tolerance level (Conservative/Moderate/Aggressive)"
    )
    investment_goals: List[str] = Field(
        ..., min_length=1, description="List of investment objectives"
    )
    time_horizon: int = Field(
        ..., ge=1, description="Investment time horizon in years"
    )
    constraints: Optional[List[str]] = Field(
        default=None, description="Investment constraints or restrictions"
    )
    annual_income: Optional[float] = Field(
        default=None, ge=0, description="Annual income in USD"
    )
    net_worth: Optional[float] = Field(
        default=None, ge=0, description="Total net worth in USD"
    )
    liquidity_needs: Optional[str] = Field(
        default=None,
        description="Liquidity requirements (e.g., 'Emergency fund', 'High')",
    )

    @field_validator("investment_goals")
    @classmethod
    def validate_goals(cls, v: List[str]) -> List[str]:
        """Ensure investment goals are not empty strings."""
        if any(not goal.strip() for goal in v):
            raise ValueError("Investment goals cannot be empty strings")
        return v


class PortfolioHolding(BaseModelWithConfig):
    """
    Individual holding within a portfolio.
    """

    ticker: str = Field(..., description="Stock ticker symbol")
    company_name: Optional[str] = Field(default=None, description="Company name")
    shares: float = Field(..., gt=0, description="Number of shares held")
    current_price: float = Field(..., gt=0, description="Current price per share")
    market_value: float = Field(..., gt=0, description="Total market value")
    asset_class: AssetClass = Field(default=AssetClass.EQUITY, description="Asset class")
    sector: Optional[str] = Field(default=None, description="Sector classification")
    cost_basis: Optional[float] = Field(
        default=None, gt=0, description="Original purchase price"
    )


class Portfolio(BaseModelWithConfig):
    """
    Complete portfolio with holdings and metadata.

    Used throughout the multi-agent workflow.
    """

    portfolio_id: str = Field(..., description="Unique portfolio identifier")
    client_id: str = Field(..., description="Associated client ID")
    holdings: List[PortfolioHolding] = Field(
        ..., min_length=1, description="List of portfolio holdings"
    )
    total_value: float = Field(..., gt=0, description="Total portfolio value")
    as_of_date: datetime = Field(
        default_factory=datetime.now, description="Portfolio valuation date"
    )
    benchmark: Optional[str] = Field(
        default="SPY", description="Benchmark ticker for comparison"
    )


# ============================================================================
# Agent Analysis Output Models
# ============================================================================


class RiskAnalysis(BaseModelWithConfig):
    """
    Risk analysis output from Risk Analyst Agent.

    Produced in Stage 2: Parallel Analysis
    """

    volatility: float = Field(
        ..., ge=0, le=100, description="Annualized volatility (standard deviation)"
    )
    var_95: float = Field(
        ..., description="95% Value at Risk (potential loss)"
    )
    beta: float = Field(..., description="Portfolio beta vs benchmark")
    concentration_score: float = Field(
        ..., ge=0, le=100, description="Concentration risk score (0=diversified, 100=concentrated)"
    )
    max_drawdown: Optional[float] = Field(
        default=None, description="Maximum historical drawdown percentage"
    )
    risk_rating: RiskRating = Field(..., description="Overall risk rating")
    concerns: List[str] = Field(
        default_factory=list, description="Identified risk concerns"
    )
    recommendations: List[str] = Field(
        default_factory=list, description="Risk mitigation recommendations"
    )


class ComplianceReport(BaseModelWithConfig):
    """
    Compliance analysis output from Compliance Officer Agent.

    Produced in Stage 2: Parallel Analysis
    """

    overall_status: ComplianceStatus = Field(..., description="Overall compliance status")
    checks_performed: List[str] = Field(
        ..., min_length=1, description="List of compliance checks performed"
    )
    violations: List[str] = Field(
        default_factory=list, description="Identified compliance violations"
    )
    warnings: List[str] = Field(
        default_factory=list, description="Compliance warnings (non-violations)"
    )
    required_disclosures: List[str] = Field(
        default_factory=list, description="Required regulatory disclosures"
    )
    suitability_pass: bool = Field(..., description="Client suitability check passed")
    concentration_limits_pass: bool = Field(
        ..., description="Concentration limits check passed"
    )
    notes: Optional[str] = Field(default=None, description="Additional compliance notes")


class PerformanceReport(BaseModelWithConfig):
    """
    Performance analysis output from Performance Analyst Agent.

    Produced in Stage 2: Parallel Analysis
    """

    total_return: float = Field(..., description="Total portfolio return (%)")
    benchmark_return: float = Field(..., description="Benchmark return (%)")
    excess_return: float = Field(..., description="Return vs benchmark (%)")
    sharpe_ratio: float = Field(..., description="Risk-adjusted return (Sharpe ratio)")
    alpha: Optional[float] = Field(default=None, description="Portfolio alpha")
    percentile_rank: Optional[int] = Field(
        default=None, ge=1, le=100, description="Peer percentile ranking"
    )
    attribution: Dict[str, float] = Field(
        default_factory=dict,
        description="Performance attribution by sector/asset class",
    )
    top_performers: List[str] = Field(
        default_factory=list, description="Top performing holdings"
    )
    bottom_performers: List[str] = Field(
        default_factory=list, description="Bottom performing holdings"
    )


# ============================================================================
# Synthesis & Suitability Models
# ============================================================================


class SuitabilityScore(BaseModelWithConfig):
    """
    Client-portfolio suitability scoring.

    Calculated in Stage 3: Synthesis & Suitability Scoring
    """

    overall_score: float = Field(
        ..., ge=0, le=100, description="Overall suitability score (0-100)"
    )
    risk_fit: float = Field(
        ..., ge=0, le=100, description="Risk tolerance fit score"
    )
    compliance_fit: float = Field(
        ..., ge=0, le=100, description="Compliance suitability score"
    )
    performance_fit: float = Field(
        ..., ge=0, le=100, description="Performance expectation fit score"
    )
    time_horizon_fit: float = Field(
        ..., ge=0, le=100, description="Time horizon alignment score"
    )
    interpretation: SuitabilityRating = Field(
        ..., description="Suitability interpretation"
    )
    explanation: str = Field(
        ..., description="Detailed explanation of suitability scoring"
    )

    @field_validator("overall_score")
    @classmethod
    def validate_overall_score(cls, v: float) -> float:
        """Ensure overall score is within valid range."""
        if not 0 <= v <= 100:
            raise ValueError("Overall score must be between 0 and 100")
        return round(v, 2)


# ============================================================================
# Final Recommendations Model
# ============================================================================


class PortfolioRecommendations(BaseModelWithConfig):
    """
    Complete portfolio analysis with recommendations.

    Final output from Portfolio Manager Agent (Stage 4-5)
    """

    portfolio_id: str = Field(..., description="Portfolio identifier")
    client_id: str = Field(..., description="Client identifier")
    analysis_date: datetime = Field(
        default_factory=datetime.now, description="Analysis timestamp"
    )

    # Specialist outputs
    suitability_score: SuitabilityScore = Field(
        ..., description="Client-portfolio suitability analysis"
    )
    risk_analysis: RiskAnalysis = Field(..., description="Risk analysis results")
    compliance_report: ComplianceReport = Field(
        ..., description="Compliance check results"
    )
    performance_report: PerformanceReport = Field(
        ..., description="Performance analysis results"
    )

    # Manager synthesis
    recommendations: List[str] = Field(
        ..., min_length=1, description="Actionable portfolio recommendations"
    )
    action_items: List[str] = Field(
        default_factory=list, description="Immediate action items for client/advisor"
    )
    next_review_date: Optional[datetime] = Field(
        default=None, description="Recommended next review date"
    )

    # Summary
    executive_summary: str = Field(
        ..., description="Executive summary of analysis and recommendations"
    )


# ============================================================================
# Tool Input/Output Models
# ============================================================================


class ParallelAnalysisInput(BaseModelWithConfig):
    """Input for parallel specialist execution."""

    portfolio: Portfolio
    client_profile: ClientProfile


class ParallelAnalysisOutput(BaseModelWithConfig):
    """Output from parallel specialist execution."""

    risk_analysis: RiskAnalysis
    compliance_report: ComplianceReport
    performance_report: PerformanceReport
    execution_time_seconds: float


# ============================================================================
# Equity Specialist Models (Handoff Agent)
# ============================================================================


class EquityDeepDiveRequest(BaseModelWithConfig):
    """
    Request for equity specialist deep dive analysis.

    Used when handing off to Equity Specialist Agent
    """

    portfolio: Portfolio
    client_profile: ClientProfile
    focus_areas: List[str] = Field(
        ..., description="Specific areas for deep dive (e.g., 'Valuation', 'Sector allocation')"
    )
    questions: Optional[List[str]] = Field(
        default=None, description="Specific questions from client/manager"
    )


class EquityDeepDiveReport(BaseModelWithConfig):
    """
    Equity specialist deep dive analysis output.

    Returned from Equity Specialist Agent handoff
    """

    focus_areas_analyzed: List[str]
    sector_analysis: Dict[str, str] = Field(
        default_factory=dict, description="Sector-by-sector analysis"
    )
    valuation_metrics: Dict[str, float] = Field(
        default_factory=dict, description="Portfolio-level valuation metrics (P/E, P/B, etc.)"
    )
    growth_vs_value_split: Dict[str, float] = Field(
        default_factory=dict, description="Growth vs Value allocation"
    )
    recommendations: List[str] = Field(
        default_factory=list, description="Equity-specific recommendations"
    )
    detailed_analysis: str = Field(..., description="Comprehensive equity analysis narrative")
