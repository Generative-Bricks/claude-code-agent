"""
Rank opportunities tool for OpportunityIQ Client Matcher.

Ranks and prioritizes opportunities using composite scoring.

SERVE Principle: Clear prioritization helps advisors focus on best opportunities.
"""

import logging
from typing import Literal, Callable, Optional

from ..models import Opportunity

logger = logging.getLogger(__name__)


def rank_opportunities(
    opportunities: list[Opportunity],
    ranking_strategy: Literal["revenue", "match_score", "composite", "priority"] = "composite",
    match_weight: float = 0.4,
    revenue_weight: float = 0.6,
    descending: bool = True,
    limit: Optional[int] = None
) -> list[Opportunity]:
    """
    Rank and prioritize opportunities.

    Assigns rank numbers to opportunities based on chosen strategy.

    Args:
        opportunities: List of opportunities to rank
        ranking_strategy: Strategy to use for ranking:
            - "revenue": Rank by estimated revenue only
            - "match_score": Rank by match score only
            - "composite": Weighted combination of match and revenue (default)
            - "priority": Rank by scenario priority (high > medium > low)
        match_weight: Weight for match score in composite (0.0-1.0, default 0.4)
        revenue_weight: Weight for revenue in composite (0.0-1.0, default 0.6)
        descending: True for highest first, False for lowest first

    Returns:
        List of opportunities with rank and composite_score assigned

    Raises:
        ValueError: If weights don't sum to 1.0 or opportunities is empty

    Example:
        >>> opportunities = match_clients_to_scenarios(clients, scenarios)
        >>> ranked = rank_opportunities(opportunities, ranking_strategy="composite")
        >>> for opp in ranked[:5]:
        ...     print(f"{opp.rank}. {opp.scenario_name}: ${opp.estimated_revenue:,.0f}")
    """
    if not opportunities:
        raise ValueError("Cannot rank empty opportunities list")

    # Validate weights for composite strategy
    if ranking_strategy == "composite":
        if not abs((match_weight + revenue_weight) - 1.0) < 0.001:
            raise ValueError(
                f"match_weight and revenue_weight must sum to 1.0 "
                f"(got {match_weight + revenue_weight})"
            )

    logger.info(
        f"Ranking {len(opportunities)} opportunities using '{ranking_strategy}' strategy"
    )

    # Choose ranking function
    if ranking_strategy == "revenue":
        score_func = lambda opp: opp.estimated_revenue
    elif ranking_strategy == "match_score":
        score_func = lambda opp: opp.match_score
    elif ranking_strategy == "composite":
        score_func = lambda opp: _calculate_composite_score(
            opp, match_weight, revenue_weight
        )
    elif ranking_strategy == "priority":
        score_func = lambda opp: _priority_to_score(opp.priority)
    else:
        raise ValueError(f"Unsupported ranking strategy: {ranking_strategy}")

    # Calculate scores and sort
    for opp in opportunities:
        if ranking_strategy == "composite":
            opp.composite_score = score_func(opp)

    sorted_opps = sorted(
        opportunities,
        key=score_func,
        reverse=descending
    )

    # Assign ranks
    for rank, opp in enumerate(sorted_opps, start=1):
        opp.rank = rank

    logger.info(
        f"Ranking complete. Top opportunity: {sorted_opps[0].scenario_name} "
        f"for {sorted_opps[0].client_name}"
    )

    # Apply limit if specified
    if limit is not None and limit > 0:
        sorted_opps = sorted_opps[:limit]
        logger.info(f"Applied limit: returning top {len(sorted_opps)} opportunities")

    return sorted_opps


def filter_opportunities(
    opportunities: list[Opportunity],
    min_match_score: Optional[float] = None,
    min_revenue: Optional[float] = None,
    max_time_hours: Optional[float] = None,
    priorities: Optional[list[str]] = None,
    categories: Optional[list[str]] = None,
    quick_wins_only: bool = False,
    high_value_only: bool = False,
    revenue_threshold: float = 5000.0
) -> list[Opportunity]:
    """
    Filter opportunities based on various criteria.

    Applies filters to narrow down opportunity list.

    Args:
        opportunities: List of opportunities to filter
        min_match_score: Minimum match score (0-100)
        min_revenue: Minimum estimated revenue
        max_time_hours: Maximum estimated time in hours
        priorities: List of priorities to include (e.g., ["high", "medium"])
        categories: List of categories to include (e.g., ["annuity", "tax"])
        quick_wins_only: Only include quick win opportunities
        high_value_only: Only include high-value opportunities
        revenue_threshold: Revenue threshold for high-value filter (default $5,000)

    Returns:
        Filtered list of opportunities

    Example:
        >>> # Get high-priority opportunities with good match scores
        >>> filtered = filter_opportunities(
        ...     opportunities,
        ...     min_match_score=70.0,
        ...     priorities=["high"]
        ... )
        >>> # Get quick wins
        >>> quick_wins = filter_opportunities(opportunities, quick_wins_only=True)
    """
    logger.info(f"Filtering {len(opportunities)} opportunities")

    filtered = opportunities.copy()

    # Apply filters
    if min_match_score is not None:
        filtered = [opp for opp in filtered if opp.match_score >= min_match_score]
        logger.debug(f"After min_match_score filter: {len(filtered)} opportunities")

    if min_revenue is not None:
        filtered = [opp for opp in filtered if opp.estimated_revenue >= min_revenue]
        logger.debug(f"After min_revenue filter: {len(filtered)} opportunities")

    if max_time_hours is not None:
        filtered = [
            opp for opp in filtered
            if opp.estimated_time_hours is not None and
            opp.estimated_time_hours <= max_time_hours
        ]
        logger.debug(f"After max_time_hours filter: {len(filtered)} opportunities")

    if priorities is not None:
        filtered = [opp for opp in filtered if opp.priority in priorities]
        logger.debug(f"After priorities filter: {len(filtered)} opportunities")

    if categories is not None:
        filtered = [opp for opp in filtered if opp.scenario_category in categories]
        logger.debug(f"After categories filter: {len(filtered)} opportunities")

    if quick_wins_only:
        filtered = [opp for opp in filtered if opp.is_quick_win()]
        logger.debug(f"After quick_wins filter: {len(filtered)} opportunities")

    if high_value_only:
        filtered = [opp for opp in filtered if opp.is_high_value(revenue_threshold)]
        logger.debug(f"After high_value filter: {len(filtered)} opportunities")

    logger.info(
        f"Filtering complete: {len(filtered)} opportunities remaining "
        f"({len(opportunities) - len(filtered)} filtered out)"
    )

    return filtered


def get_top_opportunities(
    opportunities: list[Opportunity],
    top_n: int = 10,
    ranking_strategy: Literal["revenue", "match_score", "composite", "priority"] = "composite"
) -> list[Opportunity]:
    """
    Get the top N opportunities.

    Convenience function that ranks and returns top opportunities.

    Args:
        opportunities: List of opportunities
        top_n: Number of top opportunities to return
        ranking_strategy: Strategy to use for ranking

    Returns:
        List of top N ranked opportunities

    Example:
        >>> top_10 = get_top_opportunities(opportunities, top_n=10)
        >>> for opp in top_10:
        ...     print(f"{opp.rank}. {opp.scenario_name}")
    """
    if not opportunities:
        logger.warning("No opportunities to rank")
        return []

    logger.info(f"Getting top {top_n} opportunities from {len(opportunities)} total")

    ranked = rank_opportunities(opportunities, ranking_strategy=ranking_strategy)

    return ranked[:top_n]


def group_opportunities_by_client(
    opportunities: list[Opportunity]
) -> dict[str, list[Opportunity]]:
    """
    Group opportunities by client.

    Args:
        opportunities: List of opportunities

    Returns:
        Dictionary mapping client_id to list of opportunities

    Example:
        >>> by_client = group_opportunities_by_client(opportunities)
        >>> for client_id, opps in by_client.items():
        ...     print(f"Client {client_id}: {len(opps)} opportunities")
    """
    logger.info(f"Grouping {len(opportunities)} opportunities by client")

    grouped = {}

    for opp in opportunities:
        if opp.client_id not in grouped:
            grouped[opp.client_id] = []
        grouped[opp.client_id].append(opp)

    logger.info(f"Grouped into {len(grouped)} clients")

    return grouped


# Private helper functions

def _calculate_composite_score(
    opportunity: Opportunity,
    match_weight: float,
    revenue_weight: float
) -> float:
    """
    Calculate composite score from match score and revenue.

    Normalizes revenue to 0-100 scale based on max revenue in dataset,
    then combines with match score.

    Args:
        opportunity: Opportunity to score
        match_weight: Weight for match score
        revenue_weight: Weight for revenue

    Returns:
        Composite score (0-100 scale)
    """
    # Match score is already 0-100
    match_component = opportunity.match_score * match_weight

    # Normalize revenue to 0-100 scale
    # Use a reasonable max (e.g., $50,000) for normalization
    max_revenue = 50000.0
    revenue_normalized = min(
        (opportunity.estimated_revenue / max_revenue) * 100,
        100.0
    )
    revenue_component = revenue_normalized * revenue_weight

    composite = match_component + revenue_component

    return composite


def _priority_to_score(priority: str) -> int:
    """
    Convert priority level to numeric score for sorting.

    Args:
        priority: Priority level ("high", "medium", "low")

    Returns:
        Numeric score (higher = better)
    """
    priority_map = {
        "high": 3,
        "medium": 2,
        "low": 1
    }
    return priority_map.get(priority, 0)
