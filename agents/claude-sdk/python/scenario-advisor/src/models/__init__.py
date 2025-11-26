"""
Scenario Advisor models package.

Exports:
- Base scenario models (Scenario, MatchCriterion, RevenueFormula)
- Client profile models (ClientProfile, Portfolio, Holdings)
- Opportunity models (Opportunity, MatchDetail, RevenueCalculation)
- Enriched scenario models (EnrichedScenario, SourceProvenance, TemporalContext, ConfidenceScore, ActionabilityMetrics)
"""

from .scenario import MatchCriterion, RevenueFormula, Scenario, ScenarioCategory
from .client_profile import Holdings, Portfolio, ClientProfile
from .opportunity import MatchDetail, RevenueCalculation, Opportunity
from .enriched import (
    SourceProvenance,
    TemporalContext,
    ConfidenceScore,
    ActionabilityMetrics,
    EnrichedScenario,
)

__all__ = [
    # Base scenario models
    "MatchCriterion",
    "RevenueFormula",
    "Scenario",
    "ScenarioCategory",
    # Client profile models
    "Holdings",
    "Portfolio",
    "ClientProfile",
    # Opportunity models
    "MatchDetail",
    "RevenueCalculation",
    "Opportunity",
    # Enriched scenario models
    "SourceProvenance",
    "TemporalContext",
    "ConfidenceScore",
    "ActionabilityMetrics",
    "EnrichedScenario",
]
