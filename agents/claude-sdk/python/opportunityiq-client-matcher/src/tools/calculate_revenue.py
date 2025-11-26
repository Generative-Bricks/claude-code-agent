"""
Calculate revenue tool for OpportunityIQ Client Matcher.

Calculates estimated revenue for client-scenario matches.

EXCELLENCE Principle: Accurate, transparent revenue calculations.
"""

import logging
from typing import Union

from ..models import (
    ClientProfile,
    Scenario,
    RevenueCalculation
)
from ..services.revenue_calculator import RevenueCalculator

logger = logging.getLogger(__name__)


def calculate_revenue(
    client: ClientProfile,
    scenario: Scenario
) -> RevenueCalculation:
    """
    Calculate estimated revenue for a client-scenario match.

    Uses the scenario's revenue formula to estimate potential revenue
    based on client profile data.

    Args:
        client: Client profile
        scenario: Scenario with revenue formula

    Returns:
        RevenueCalculation with detailed breakdown

    Raises:
        ValueError: If formula is invalid or required data is missing

    Example:
        >>> client = ClientProfile(...)
        >>> scenario = load_scenarios("data/scenarios/annuity.json", "annuity_001")
        >>> revenue = calculate_revenue(client, scenario)
        >>> print(f"Estimated revenue: ${revenue.final_amount:,.2f}")
    """
    logger.info(
        f"Calculating revenue for client {client.client_id} "
        f"and scenario {scenario.scenario_id}"
    )

    calculator = RevenueCalculator()

    try:
        revenue_calc = calculator.calculate_revenue(client, scenario)

        logger.info(
            f"Revenue calculated: ${revenue_calc.final_amount:,.2f} "
            f"(formula: {revenue_calc.formula_type})"
        )

        return revenue_calc

    except Exception as e:
        logger.error(
            f"Error calculating revenue for client {client.client_id} "
            f"and scenario {scenario.scenario_id}: {e}",
            exc_info=True
        )
        raise


def calculate_revenues_batch(
    clients: Union[list[ClientProfile], ClientProfile],
    scenarios: Union[list[Scenario], Scenario]
) -> dict[tuple[str, str], RevenueCalculation]:
    """
    Calculate revenues for multiple client-scenario combinations.

    Batch processing for revenue calculations.

    Args:
        clients: Single client or list of clients
        scenarios: Single scenario or list of scenarios

    Returns:
        Dictionary mapping (client_id, scenario_id) to RevenueCalculation

    Example:
        >>> clients = [client1, client2]
        >>> scenarios = [scenario1, scenario2]
        >>> revenues = calculate_revenues_batch(clients, scenarios)
        >>> # Access specific calculation
        >>> calc = revenues[(client1.client_id, scenario1.scenario_id)]
        >>> print(f"Revenue: ${calc.final_amount:,.2f}")
    """
    # Convert to lists if single items
    if isinstance(clients, ClientProfile):
        clients = [clients]
    if isinstance(scenarios, Scenario):
        scenarios = [scenarios]

    logger.info(
        f"Batch calculating revenues for {len(clients)} clients "
        f"and {len(scenarios)} scenarios"
    )

    calculator = RevenueCalculator()
    results = {}
    errors = []

    for client in clients:
        for scenario in scenarios:
            key = (client.client_id, scenario.scenario_id)

            try:
                revenue_calc = calculator.calculate_revenue(client, scenario)
                results[key] = revenue_calc

            except Exception as e:
                error_msg = (
                    f"Error for client {client.client_id} "
                    f"and scenario {scenario.scenario_id}: {e}"
                )
                errors.append(error_msg)
                logger.error(error_msg)

    # Log summary
    logger.info(
        f"Batch calculation complete: {len(results)} successful, "
        f"{len(errors)} errors"
    )

    if errors:
        logger.warning("Revenue calculation errors occurred:")
        for error in errors:
            logger.warning(f"  - {error}")

    return results


def estimate_total_revenue(
    opportunities: list["Opportunity"]
) -> dict[str, float]:
    """
    Calculate total revenue estimates from a list of opportunities.

    Aggregates revenue by various dimensions.

    Args:
        opportunities: List of Opportunity objects

    Returns:
        Dictionary with revenue aggregations:
        - total: Total estimated revenue
        - by_priority: Revenue breakdown by priority level
        - by_category: Revenue breakdown by scenario category
        - by_client: Revenue breakdown by client

    Example:
        >>> opportunities = match_clients_to_scenarios(clients, scenarios)
        >>> totals = estimate_total_revenue(opportunities)
        >>> print(f"Total revenue: ${totals['total']:,.2f}")
        >>> print(f"High priority: ${totals['by_priority']['high']:,.2f}")
    """
    if not opportunities:
        logger.warning("No opportunities provided for revenue estimation")
        return {
            "total": 0.0,
            "by_priority": {},
            "by_category": {},
            "by_client": {}
        }

    logger.info(f"Calculating total revenue from {len(opportunities)} opportunities")

    # Calculate total
    total = sum(opp.estimated_revenue for opp in opportunities)

    # By priority
    by_priority = {}
    for priority in ["high", "medium", "low"]:
        priority_rev = sum(
            opp.estimated_revenue
            for opp in opportunities
            if opp.priority == priority
        )
        if priority_rev > 0:
            by_priority[priority] = priority_rev

    # By category
    by_category = {}
    categories = set(opp.scenario_category for opp in opportunities)
    for category in categories:
        category_rev = sum(
            opp.estimated_revenue
            for opp in opportunities
            if opp.scenario_category == category
        )
        by_category[category] = category_rev

    # By client
    by_client = {}
    client_ids = set(opp.client_id for opp in opportunities)
    for client_id in client_ids:
        client_rev = sum(
            opp.estimated_revenue
            for opp in opportunities
            if opp.client_id == client_id
        )
        by_client[client_id] = client_rev

    result = {
        "total": total,
        "by_priority": by_priority,
        "by_category": by_category,
        "by_client": by_client
    }

    logger.info(f"Total estimated revenue: ${total:,.2f}")

    return result
