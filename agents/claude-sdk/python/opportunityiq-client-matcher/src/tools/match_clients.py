"""
Match clients tool for OpportunityIQ Client Matcher.

Matches client profiles against scenarios using the matching engine.

TRUTH Principle: Every matching decision is transparent and traceable.
"""

import logging
from typing import Union
from datetime import datetime
import uuid

from ..models import (
    ClientProfile,
    Scenario,
    Opportunity,
    MatchDetail
)
from ..services.matching_engine import MatchingEngine
from ..services.revenue_calculator import RevenueCalculator

logger = logging.getLogger(__name__)


def match_client_to_scenarios(
    client: ClientProfile,
    scenarios: Union[list[Scenario], Scenario],
    min_match_threshold: float = 0.0
) -> list[Opportunity]:
    """
    Match a single client against one or more scenarios.

    Evaluates the client profile against scenario criteria and calculates
    revenue estimates for matches that meet the threshold.

    Args:
        client: Client profile to evaluate
        scenarios: Single scenario or list of scenarios to match against
        min_match_threshold: Minimum match score (0-100) to include in results

    Returns:
        List of Opportunity objects for matches above threshold

    Raises:
        ValueError: If min_match_threshold is invalid

    Example:
        >>> client = ClientProfile(...)
        >>> scenarios = load_scenarios("data/scenarios/annuity_scenarios.json")
        >>> opportunities = match_client_to_scenarios(client, scenarios, min_match_threshold=60.0)
        >>> print(f"Found {len(opportunities)} opportunities above 60% match")
    """
    # Validate threshold
    if not 0.0 <= min_match_threshold <= 100.0:
        raise ValueError("min_match_threshold must be between 0.0 and 100.0")

    # Convert single scenario to list
    if isinstance(scenarios, Scenario):
        scenarios = [scenarios]

    logger.info(
        f"Matching client {client.client_id} against {len(scenarios)} scenarios "
        f"(threshold: {min_match_threshold}%)"
    )

    # Initialize engines
    matching_engine = MatchingEngine()
    revenue_calculator = RevenueCalculator()

    opportunities = []

    for scenario in scenarios:
        try:
            # Calculate match score
            match_score, match_details = matching_engine.match_client_to_scenario(
                client, scenario
            )

            # Skip if below threshold
            if match_score < min_match_threshold:
                logger.debug(
                    f"Skipping scenario {scenario.scenario_id}: "
                    f"match score {match_score:.1f}% below threshold"
                )
                continue

            # Calculate revenue
            revenue_calc = revenue_calculator.calculate_revenue(client, scenario)

            # Count criteria met
            criteria_met = sum(1 for d in match_details if d.matched)
            total_criteria = len(match_details)

            # Create opportunity
            opportunity = Opportunity(
                opportunity_id=str(uuid.uuid4()),
                client_id=client.client_id,
                client_name=client.name,
                scenario_id=scenario.scenario_id,
                scenario_name=scenario.name,
                scenario_category=scenario.category,
                match_score=match_score,
                match_details=match_details,
                total_criteria=total_criteria,
                criteria_met=criteria_met,
                estimated_revenue=revenue_calc.final_amount,
                revenue_calculation=revenue_calc,
                priority=scenario.priority,
                estimated_time_hours=scenario.estimated_time_hours,
                required_licenses=scenario.required_licenses,
                compliance_notes=scenario.compliance_notes,
                created_at=datetime.utcnow()
            )

            opportunities.append(opportunity)

            logger.info(
                f"Created opportunity: {scenario.name} for {client.name} "
                f"(match: {match_score:.1f}%, revenue: ${revenue_calc.final_amount:,.2f})"
            )

        except Exception as e:
            logger.error(
                f"Error matching client {client.client_id} to scenario {scenario.scenario_id}: {e}",
                exc_info=True
            )
            # Continue processing other scenarios

    logger.info(
        f"Matched client {client.client_id}: found {len(opportunities)} opportunities"
    )

    return opportunities


def match_clients_to_scenarios(
    clients: Union[list[ClientProfile], ClientProfile],
    scenarios: Union[list[Scenario], Scenario],
    min_match_threshold: float = 0.0
) -> list[Opportunity]:
    """
    Match multiple clients against one or more scenarios.

    Batch processing for matching multiple client profiles.

    Args:
        clients: Single client or list of clients to evaluate
        scenarios: Single scenario or list of scenarios to match against
        min_match_threshold: Minimum match score (0-100) to include in results

    Returns:
        List of all Opportunity objects for all clients above threshold

    Raises:
        ValueError: If min_match_threshold is invalid

    Example:
        >>> clients = [client1, client2, client3]
        >>> scenarios = load_scenarios("data/scenarios/")
        >>> opportunities = match_clients_to_scenarios(clients, scenarios)
        >>> print(f"Found {len(opportunities)} total opportunities")
    """
    # Convert single client to list
    if isinstance(clients, ClientProfile):
        clients = [clients]

    # Convert single scenario to list
    if isinstance(scenarios, Scenario):
        scenarios = [scenarios]

    logger.info(
        f"Batch matching {len(clients)} clients against {len(scenarios)} scenarios"
    )

    all_opportunities = []

    for client in clients:
        try:
            opportunities = match_client_to_scenarios(
                client,
                scenarios,
                min_match_threshold
            )
            all_opportunities.extend(opportunities)

        except Exception as e:
            logger.error(
                f"Error matching client {client.client_id}: {e}",
                exc_info=True
            )
            # Continue processing other clients

    logger.info(
        f"Batch matching complete: {len(all_opportunities)} total opportunities "
        f"from {len(clients)} clients"
    )

    return all_opportunities
