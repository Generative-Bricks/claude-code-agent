"""Research agents for scenario discovery.

This module contains specialized research agents that use LLM reasoning
to discover actionable scenarios across different categories:

- AnnuityResearcher: Annuity-related scenarios (surrender periods, rate resets, etc.)
- LifeEventResearcher: Life event scenarios (retirement, inheritance, etc.)
- RevenueResearcher: Revenue opportunity scenarios (cross-sell, consolidation, etc.)

Each agent follows a consistent pattern:
1. Accepts time_range_days parameter
2. Uses Claude API for scenario reasoning
3. Returns list of dicts compatible with EnrichedScenario model
"""

from .annuity_researcher import AnnuityResearcher
from .life_event_researcher import LifeEventResearcher
from .revenue_researcher import RevenueResearcher

__all__ = [
    "AnnuityResearcher",
    "LifeEventResearcher",
    "RevenueResearcher",
]
