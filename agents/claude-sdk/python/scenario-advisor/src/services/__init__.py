"""
Service layer for scenario-advisor.

This module exports the core business logic services:
- MatchingEngine: Client-scenario matching and scoring
- RevenueCalculator: Revenue estimation with multiple formula types
- ReportGenerator: Report generation in multiple formats
- ResearchOrchestrator: Coordinates parallel research across specialists
- ScenarioSynthesizer: Merges, validates, and enriches scenarios
- ExecutionOrchestrator: Matches scenarios to clients and generates reports
"""

from .matching_engine import MatchingEngine
from .revenue_calculator import RevenueCalculator
from .report_generator import ReportGenerator
from .research_orchestrator import ResearchOrchestrator
from .scenario_synthesizer import ScenarioSynthesizer
from .execution_orchestrator import ExecutionOrchestrator

__all__ = [
    "MatchingEngine",
    "RevenueCalculator",
    "ReportGenerator",
    "ResearchOrchestrator",
    "ScenarioSynthesizer",
    "ExecutionOrchestrator",
]
