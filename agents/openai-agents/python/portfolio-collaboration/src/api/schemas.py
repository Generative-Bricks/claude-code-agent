"""
API Schemas for Portfolio Collaboration System.

Request and response models for FastAPI endpoints.
Wraps domain models from src.models.schemas for API layer.

Biblical Principle: EXCELLENCE - Well-defined contracts between frontend and backend.
Biblical Principle: TRUTH - Transparent, validated data structures.
"""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.models.schemas import (
    ClientProfile,
    Portfolio,
    PortfolioRecommendations,
    RiskTolerance,
)


# ============================================================================
# Base API Model Configuration
# ============================================================================


class APIBaseModel(BaseModel):
    """
    Base model for API request/response schemas.

    Configured for FastAPI with JSON serialization and validation.
    """

    model_config = ConfigDict(
        # Allow serialization of datetime and other complex types
        json_encoders={datetime: lambda v: v.isoformat()},
        # Populate models by field name (for FastAPI compatibility)
        populate_by_name=True,
        # Use enum values in JSON output
        use_enum_values=True,
    )


# ============================================================================
# Analysis Endpoint Schemas
# ============================================================================


class AnalysisRequest(APIBaseModel):
    """
    Request to analyze a portfolio for a client.

    POST /api/analyze

    Example:
        {
            "client_profile": {
                "client_id": "CLT-2024-001",
                "age": 65,
                "risk_tolerance": "Conservative",
                ...
            },
            "portfolio": {
                "portfolio_id": "PORT-2024-001",
                "client_id": "CLT-2024-001",
                "holdings": [...],
                ...
            }
        }
    """

    client_profile: ClientProfile = Field(
        ..., description="Client profile containing demographics and objectives"
    )
    portfolio: Portfolio = Field(
        ..., description="Portfolio to analyze with complete holdings"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "client_profile": {
                    "client_id": "CLT-2024-001",
                    "age": 65,
                    "risk_tolerance": "Conservative",
                    "investment_goals": ["Income Generation", "Capital Preservation"],
                    "time_horizon": 10,
                    "annual_income": 75000,
                    "net_worth": 850000,
                    "liquidity_needs": "Emergency fund required",
                },
                "portfolio": {
                    "portfolio_id": "PORT-2024-001",
                    "client_id": "CLT-2024-001",
                    "total_value": 500000,
                    "benchmark": "SPY",
                },
            }
        }
    )


class AnalysisResponse(APIBaseModel):
    """
    Response from portfolio analysis.

    POST /api/analyze response

    Contains complete recommendations from all specialist agents including
    suitability scoring, risk analysis, compliance checks, and performance metrics.
    """

    success: bool = Field(..., description="Whether analysis completed successfully")
    recommendations: PortfolioRecommendations = Field(
        ..., description="Complete portfolio analysis and recommendations"
    )
    analysis_id: str = Field(
        ..., description="Unique identifier for this analysis session"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Analysis completion timestamp"
    )
    execution_time_seconds: float = Field(
        ..., ge=0, description="Total analysis execution time in seconds"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "analysis_id": "ANLYS-2025-001-ABC123",
                "timestamp": "2025-01-14T10:30:00",
                "execution_time_seconds": 5.42,
            }
        }
    )


# ============================================================================
# Data Listing Schemas
# ============================================================================


class ClientSummary(APIBaseModel):
    """
    Summary of a client profile for listing purposes.

    Used in GET /api/clients response.
    Lightweight version of ClientProfile for list views.
    """

    client_id: str = Field(..., description="Unique client identifier")
    age: int = Field(..., ge=18, le=120, description="Client age")
    risk_tolerance: str = Field(..., description="Risk tolerance level")
    net_worth: Optional[float] = Field(
        default=None, ge=0, description="Total net worth in USD"
    )
    time_horizon: int = Field(
        ..., ge=1, description="Investment time horizon in years"
    )
    investment_goals_count: int = Field(
        default=0, ge=0, description="Number of investment goals"
    )

    @classmethod
    def from_client_profile(cls, profile: ClientProfile) -> "ClientSummary":
        """
        Create a ClientSummary from a full ClientProfile.

        Args:
            profile: Full client profile

        Returns:
            ClientSummary with essential fields
        """
        return cls(
            client_id=profile.client_id,
            age=profile.age,
            risk_tolerance=profile.risk_tolerance.value,
            net_worth=profile.net_worth,
            time_horizon=profile.time_horizon,
            investment_goals_count=len(profile.investment_goals),
        )


class ClientListResponse(APIBaseModel):
    """
    Response listing all available clients.

    GET /api/clients response
    """

    clients: List[ClientSummary] = Field(
        default_factory=list, description="List of client summaries"
    )
    total: int = Field(..., ge=0, description="Total number of clients")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "clients": [
                    {
                        "client_id": "CLT-2024-001",
                        "age": 65,
                        "risk_tolerance": "Conservative",
                        "net_worth": 850000,
                        "time_horizon": 10,
                        "investment_goals_count": 2,
                    }
                ],
                "total": 1,
            }
        }
    )


class PortfolioSummary(APIBaseModel):
    """
    Summary of a portfolio for listing purposes.

    Used in GET /api/portfolios response.
    Lightweight version of Portfolio for list views.
    """

    portfolio_id: str = Field(..., description="Unique portfolio identifier")
    client_id: str = Field(..., description="Associated client ID")
    total_value: float = Field(..., gt=0, description="Total portfolio value in USD")
    holdings_count: int = Field(..., ge=1, description="Number of holdings in portfolio")
    benchmark: str = Field(default="SPY", description="Benchmark ticker symbol")
    as_of_date: datetime = Field(
        default_factory=datetime.now, description="Portfolio valuation date"
    )

    @classmethod
    def from_portfolio(cls, portfolio: Portfolio) -> "PortfolioSummary":
        """
        Create a PortfolioSummary from a full Portfolio.

        Args:
            portfolio: Full portfolio with holdings

        Returns:
            PortfolioSummary with essential fields
        """
        return cls(
            portfolio_id=portfolio.portfolio_id,
            client_id=portfolio.client_id,
            total_value=portfolio.total_value,
            holdings_count=len(portfolio.holdings),
            benchmark=portfolio.benchmark or "SPY",
            as_of_date=portfolio.as_of_date,
        )


class PortfolioListResponse(APIBaseModel):
    """
    Response listing all available portfolios.

    GET /api/portfolios response
    """

    portfolios: List[PortfolioSummary] = Field(
        default_factory=list, description="List of portfolio summaries"
    )
    total: int = Field(..., ge=0, description="Total number of portfolios")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "portfolios": [
                    {
                        "portfolio_id": "PORT-2024-001",
                        "client_id": "CLT-2024-001",
                        "total_value": 500000,
                        "holdings_count": 12,
                        "benchmark": "SPY",
                        "as_of_date": "2025-01-14T10:30:00",
                    }
                ],
                "total": 1,
            }
        }
    )


# ============================================================================
# Comparison Endpoint Schemas
# ============================================================================


class ComparisonRequest(APIBaseModel):
    """
    Request to compare multiple portfolios for a client.

    POST /api/compare

    Allows comparison of 2-5 portfolios to identify the best fit for a client.
    Each portfolio is analyzed and scored for suitability.
    """

    client_profile: ClientProfile = Field(
        ..., description="Client profile for suitability comparison"
    )
    portfolio_ids: List[str] = Field(
        ...,
        min_length=2,
        max_length=5,
        description="List of 2-5 portfolio IDs to compare",
    )

    @field_validator("portfolio_ids")
    @classmethod
    def validate_portfolio_count(cls, v: List[str]) -> List[str]:
        """
        Validate that portfolio count is within acceptable range.

        Args:
            v: List of portfolio IDs

        Returns:
            Validated list of portfolio IDs

        Raises:
            ValueError: If less than 2 or more than 5 portfolios
        """
        if len(v) < 2:
            raise ValueError("Must compare at least 2 portfolios")
        if len(v) > 5:
            raise ValueError("Cannot compare more than 5 portfolios at once")
        return v

    @field_validator("portfolio_ids")
    @classmethod
    def validate_unique_portfolios(cls, v: List[str]) -> List[str]:
        """
        Ensure all portfolio IDs are unique.

        Args:
            v: List of portfolio IDs

        Returns:
            Validated list of unique portfolio IDs

        Raises:
            ValueError: If duplicate portfolio IDs are found
        """
        if len(v) != len(set(v)):
            raise ValueError("Portfolio IDs must be unique")
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "client_profile": {
                    "client_id": "CLT-2024-001",
                    "age": 45,
                    "risk_tolerance": "Moderate",
                    "investment_goals": ["Retirement", "Growth"],
                    "time_horizon": 20,
                },
                "portfolio_ids": [
                    "PORT-2024-001",
                    "PORT-2024-002",
                    "PORT-2024-003",
                ],
            }
        }
    )


class ComparisonResult(APIBaseModel):
    """
    Analysis result for a single portfolio in comparison.

    Contains the complete analysis and suitability score for one portfolio.
    """

    portfolio_id: str = Field(..., description="Portfolio identifier")
    recommendations: PortfolioRecommendations = Field(
        ..., description="Complete analysis and recommendations for this portfolio"
    )
    suitability_score: float = Field(
        ..., ge=0, le=100, description="Overall suitability score (0-100)"
    )
    suitability_rating: str = Field(
        ..., description="Suitability interpretation (e.g., 'Highly Suitable')"
    )


class ComparisonResponse(APIBaseModel):
    """
    Response from portfolio comparison analysis.

    POST /api/compare response

    Contains analysis results for all compared portfolios, ranked by suitability.
    """

    success: bool = Field(..., description="Whether comparison completed successfully")
    results: List[ComparisonResult] = Field(
        ..., description="Analysis results for each portfolio, sorted by suitability score"
    )
    best_fit_portfolio_id: str = Field(
        ..., description="Portfolio ID with highest suitability score"
    )
    comparison_id: str = Field(
        ..., description="Unique identifier for this comparison session"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Comparison completion timestamp"
    )
    execution_time_seconds: float = Field(
        ..., ge=0, description="Total comparison execution time in seconds"
    )

    @field_validator("results")
    @classmethod
    def validate_results_sorted(cls, v: List[ComparisonResult]) -> List[ComparisonResult]:
        """
        Ensure results are sorted by suitability score (descending).

        Args:
            v: List of comparison results

        Returns:
            Results sorted by suitability score
        """
        return sorted(
            v, key=lambda x: x.suitability_score, reverse=True
        )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "best_fit_portfolio_id": "PORT-2024-002",
                "comparison_id": "CMP-2025-001-XYZ789",
                "timestamp": "2025-01-14T10:35:00",
                "execution_time_seconds": 12.84,
            }
        }
    )


# ============================================================================
# WebSocket Message Schemas
# ============================================================================


class ChatMessage(APIBaseModel):
    """
    Chat message from user in WebSocket conversation.

    WS /api/ws/chat

    Used for interactive portfolio analysis conversations.
    """

    message: str = Field(
        ..., min_length=1, max_length=10000, description="User's message text"
    )
    session_id: Optional[str] = Field(
        default=None, description="Optional session ID for conversation continuity"
    )

    @field_validator("message")
    @classmethod
    def validate_message_not_empty(cls, v: str) -> str:
        """
        Ensure message is not just whitespace.

        Args:
            v: Message text

        Returns:
            Validated message text

        Raises:
            ValueError: If message is empty or only whitespace
        """
        if not v.strip():
            raise ValueError("Message cannot be empty or whitespace only")
        return v.strip()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "What's the risk profile of my conservative portfolio?",
                "session_id": "SESSION-2025-001-ABC",
            }
        }
    )


class AgentStreamEvent(APIBaseModel):
    """
    Streaming event from agent during WebSocket conversation.

    WS /api/ws/chat (server → client)

    Provides real-time updates on agent thinking, tool calls, and responses.
    """

    event_type: Literal["thinking", "tool_call", "response", "complete", "error"] = Field(
        ..., description="Type of streaming event"
    )
    content: str = Field(..., description="Event content or message")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Event timestamp"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Optional event-specific metadata"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "event_type": "tool_call",
                "content": "Analyzing portfolio risk metrics...",
                "timestamp": "2025-01-14T10:30:15",
                "metadata": {"tool": "analyze_risk", "agent": "Risk Analyst"},
            }
        }
    )


# ============================================================================
# Error Response Schema
# ============================================================================


class ErrorResponse(APIBaseModel):
    """
    Standard error response for all API endpoints.

    Provides consistent error structure across the API.
    """

    error: str = Field(..., description="Error category (e.g., 'ValidationError')")
    message: str = Field(..., description="Human-readable error message")
    type: str = Field(..., description="Error type for client-side handling")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Error timestamp"
    )
    details: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional error context and debugging information"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": "ValidationError",
                "message": "Invalid portfolio ID format",
                "type": "INVALID_INPUT",
                "timestamp": "2025-01-14T10:30:00",
                "details": {
                    "field": "portfolio_id",
                    "expected_format": "PORT-YYYY-NNN",
                    "received": "INVALID-ID",
                },
            }
        }
    )


# ============================================================================
# Health Check Schema
# ============================================================================


class HealthCheckResponse(APIBaseModel):
    """
    Health check response for API monitoring.

    GET /api/health response

    Provides system status and component health information.
    """

    status: Literal["healthy", "degraded", "unhealthy"] = Field(
        ..., description="Overall API health status"
    )
    api_version: str = Field(..., description="API version (e.g., '1.0.0')")
    openai_configured: bool = Field(
        ..., description="Whether OpenAI API key is configured"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Health check timestamp"
    )
    checks: Dict[str, bool] = Field(
        default_factory=dict,
        description="Individual component health status (database, agents, etc.)",
    )
    uptime_seconds: Optional[float] = Field(
        default=None, ge=0, description="API uptime in seconds"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "healthy",
                "api_version": "1.0.0",
                "openai_configured": True,
                "timestamp": "2025-01-14T10:30:00",
                "checks": {
                    "database": True,
                    "agents_initialized": True,
                    "market_data_mcp": True,
                },
                "uptime_seconds": 3600.5,
            }
        }
    )


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Analysis endpoints
    "AnalysisRequest",
    "AnalysisResponse",
    # Data listing endpoints
    "ClientSummary",
    "ClientListResponse",
    "PortfolioSummary",
    "PortfolioListResponse",
    # Comparison endpoint
    "ComparisonRequest",
    "ComparisonResult",
    "ComparisonResponse",
    # WebSocket messages
    "ChatMessage",
    "AgentStreamEvent",
    # Error handling
    "ErrorResponse",
    # Health check
    "HealthCheckResponse",
]
