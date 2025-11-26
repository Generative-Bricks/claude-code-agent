"""
Models package for Multi-Agent Portfolio Collaboration System.

Exports all Pydantic models for easy importing throughout the application.
"""

from .schemas import (
    # Enumerations
    AssetClass,
    ComplianceStatus,
    RiskRating,
    RiskTolerance,
    SuitabilityRating,
    # Client & Portfolio
    ClientProfile,
    Portfolio,
    PortfolioHolding,
    # Analysis Outputs
    ComplianceReport,
    PerformanceReport,
    RiskAnalysis,
    # Suitability & Recommendations
    PortfolioRecommendations,
    SuitabilityScore,
    # Tool Models
    ParallelAnalysisInput,
    ParallelAnalysisOutput,
    # Equity Specialist
    EquityDeepDiveReport,
    EquityDeepDiveRequest,
)

__all__ = [
    # Enumerations
    "AssetClass",
    "ComplianceStatus",
    "RiskRating",
    "RiskTolerance",
    "SuitabilityRating",
    # Client & Portfolio
    "ClientProfile",
    "Portfolio",
    "PortfolioHolding",
    # Analysis Outputs
    "ComplianceReport",
    "PerformanceReport",
    "RiskAnalysis",
    # Suitability & Recommendations
    "PortfolioRecommendations",
    "SuitabilityScore",
    # Tool Models
    "ParallelAnalysisInput",
    "ParallelAnalysisOutput",
    # Equity Specialist
    "EquityDeepDiveReport",
    "EquityDeepDiveRequest",
]
