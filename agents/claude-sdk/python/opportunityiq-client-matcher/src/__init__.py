"""
OpportunityIQ Client Matcher

A financial advisor tool for matching client profiles to opportunity scenarios
and prioritizing revenue-generating actions.

Architecture:
- models/: Pydantic data models (Scenario, ClientProfile, Opportunity)
- services/: Business logic (MatchingEngine, RevenueCalculator, ReportGenerator)
- tools/: Public API functions for agent interaction
"""

__version__ = "1.0.0"

from . import models
from . import tools
from . import services

__all__ = ["models", "tools", "services"]
