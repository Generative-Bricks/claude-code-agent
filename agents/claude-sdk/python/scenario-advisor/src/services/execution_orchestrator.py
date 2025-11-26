"""Execution orchestrator for matching enriched scenarios to clients.

This module coordinates the execution phase: loading clients, matching scenarios
to appropriate clients, calculating revenue potential, and generating reports.
"""

import logging
import json
from pathlib import Path
from typing import Optional

from ..models import (
    EnrichedScenario,
    ClientProfile,
    Opportunity,
    ScenarioCategory
)
from .matching_engine import MatchingEngine
from .revenue_calculator import RevenueCalculator
from .report_generator import ReportGenerator

logger = logging.getLogger(__name__)


class ExecutionOrchestrator:
    """Match enriched scenarios to clients and generate opportunities.

    This orchestrator coordinates the execution phase of the scenario advisor:
    1. Load client profiles
    2. Match scenarios to appropriate clients
    3. Calculate revenue potential
    4. Generate prioritized reports

    Attributes:
        matching_engine: Engine for matching scenarios to clients
        revenue_calculator: Calculator for revenue potential
        report_generator: Generator for opportunity reports
    """

    def __init__(self):
        """Initialize the execution orchestrator with component services."""
        logger.info("Initializing execution orchestrator")
        self.matching_engine = MatchingEngine()
        self.revenue_calculator = RevenueCalculator()
        self.report_generator = ReportGenerator()
        logger.debug("All execution components initialized")

    async def execute(
        self,
        scenarios: list[EnrichedScenario],
        clients_path: str,
        min_match_threshold: float = 60.0
    ) -> list[Opportunity]:
        """Execute scenario matching and generate opportunities.

        Args:
            scenarios: List of enriched scenarios to match
            clients_path: Path to client profiles (JSON or CSV)
            min_match_threshold: Minimum match score (0-100) for inclusion

        Returns:
            List of opportunities sorted by priority (highest revenue potential first)

        Example:
            >>> orchestrator = ExecutionOrchestrator()
            >>> opportunities = await orchestrator.execute(
            ...     scenarios=enriched_scenarios,
            ...     clients_path="data/clients/sample-clients.json",
            ...     min_match_threshold=70.0
            ... )
        """
        logger.info(
            f"Starting execution with {len(scenarios)} scenarios, "
            f"clients path: {clients_path}, threshold: {min_match_threshold}"
        )

        # Load client profiles
        try:
            clients = self._load_clients(clients_path)
            logger.info(f"Loaded {len(clients)} client profiles")
        except Exception as e:
            logger.error(f"Failed to load clients from {clients_path}: {e}", exc_info=True)
            raise

        # Match scenarios to clients
        opportunities = []
        for scenario in scenarios:
            try:
                # Convert enriched scenario to base scenario format for matching
                base_scenario = self._to_base_scenario(scenario)

                # Find matching clients
                matches = await self.matching_engine.match(
                    scenario=base_scenario,
                    clients=clients,
                    min_threshold=min_match_threshold
                )

                logger.debug(
                    f"Scenario '{scenario.title}' matched to {len(matches)} clients"
                )

                # Create opportunities from matches
                for match in matches:
                    opportunity = Opportunity(
                        scenario_id=scenario.metadata.get("id", scenario.title),
                        scenario_title=scenario.title,
                        scenario_description=scenario.description,
                        scenario_category=scenario.category,
                        client_id=match["client_id"],
                        client_name=match["client_name"],
                        match_score=match["match_score"],
                        match_reasons=match["match_reasons"],
                        estimated_revenue=self.revenue_calculator.calculate(
                            scenario=base_scenario,
                            client=match["client_profile"]
                        ),
                        priority_score=self._calculate_priority(
                            match_score=match["match_score"],
                            confidence=scenario.confidence.overall_score,
                            actionability=scenario.actionability.overall_score
                        ),
                        recommended_actions=scenario.metadata.get(
                            "recommended_actions",
                            []
                        ),
                        metadata={
                            "confidence": scenario.confidence.model_dump(),
                            "actionability": scenario.actionability.model_dump(),
                            "temporal": scenario.temporal_context.model_dump(),
                            "sources": scenario.sources.model_dump()
                        }
                    )
                    opportunities.append(opportunity)

            except Exception as e:
                logger.warning(
                    f"Failed to process scenario '{scenario.title}': {e}",
                    exc_info=True
                )

        logger.info(f"Created {len(opportunities)} opportunities from {len(scenarios)} scenarios")

        # Sort by priority score (descending)
        opportunities.sort(key=lambda o: o.priority_score, reverse=True)
        logger.info("Opportunities sorted by priority")

        return opportunities

    def _load_clients(self, path: str) -> list[ClientProfile]:
        """Load client profiles from JSON or CSV file.

        Args:
            path: Path to client data file

        Returns:
            List of validated ClientProfile instances

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file format is unsupported or invalid
        """
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"Client file not found: {path}")

        logger.debug(f"Loading clients from {file_path.suffix} file: {path}")

        # Load JSON file
        if file_path.suffix == ".json":
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)

                # Handle both list of clients and wrapped format
                if isinstance(data, dict) and "clients" in data:
                    clients_data = data["clients"]
                elif isinstance(data, list):
                    clients_data = data
                else:
                    raise ValueError(
                        "Invalid JSON format: expected list or object with 'clients' key"
                    )

                # Validate and create ClientProfile instances
                clients = [ClientProfile(**client) for client in clients_data]
                return clients

            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in client file: {e}")

        # Load CSV file
        elif file_path.suffix == ".csv":
            import csv

            try:
                clients = []
                with open(file_path, "r") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Convert CSV row to ClientProfile format
                        client_data = {
                            "client_id": row["client_id"],
                            "name": row["name"],
                            "age": int(row["age"]),
                            "risk_tolerance": row["risk_tolerance"],
                            "current_assets": float(row.get("current_assets", 0)),
                            "annual_income": float(row.get("annual_income", 0)),
                            "goals": row.get("goals", "").split(";") if row.get("goals") else [],
                            "life_events": row.get("life_events", "").split(";") if row.get("life_events") else [],
                            "current_products": row.get("current_products", "").split(";") if row.get("current_products") else []
                        }
                        clients.append(ClientProfile(**client_data))

                return clients

            except (csv.Error, KeyError, ValueError) as e:
                raise ValueError(f"Invalid CSV format in client file: {e}")

        else:
            raise ValueError(
                f"Unsupported file format: {file_path.suffix}. "
                "Supported formats: .json, .csv"
            )

    def _to_base_scenario(self, enriched: EnrichedScenario) -> dict:
        """Convert EnrichedScenario to base Scenario format.

        The matching engine expects a simpler dictionary format rather than
        the full EnrichedScenario model.

        Args:
            enriched: EnrichedScenario instance

        Returns:
            Dictionary with base scenario fields
        """
        return {
            "title": enriched.title,
            "description": enriched.description,
            "category": enriched.category.value,
            "tags": enriched.tags,
            "confidence": enriched.confidence.overall_score,
            "urgency": enriched.temporal_context.urgency_level,
            "impact": enriched.actionability.impact_score,
            "target_criteria": enriched.metadata.get("target_criteria", {}),
            "recommended_actions": enriched.metadata.get("recommended_actions", [])
        }

    def _calculate_priority(
        self,
        match_score: float,
        confidence: float,
        actionability: float
    ) -> float:
        """Calculate priority score for an opportunity.

        Priority is a weighted combination of:
        - Match score (40%): How well does the scenario fit the client?
        - Confidence (30%): How confident are we in the scenario?
        - Actionability (30%): How actionable is the scenario?

        Args:
            match_score: Client-scenario match score (0-100)
            confidence: Scenario confidence score (0-1)
            actionability: Scenario actionability score (0-1)

        Returns:
            Priority score (0-100)
        """
        # Normalize match_score to 0-1 range
        normalized_match = match_score / 100.0

        # Calculate weighted priority
        priority = (
            normalized_match * 0.40 +
            confidence * 0.30 +
            actionability * 0.30
        ) * 100.0

        return round(priority, 2)
