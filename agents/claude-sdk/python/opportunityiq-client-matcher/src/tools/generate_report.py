"""
Generate report tool for OpportunityIQ Client Matcher.

Creates formatted reports from matched and ranked opportunities.

SERVE Principle: Clear, actionable reports that help advisors make decisions.
"""

import logging
from typing import Literal, Optional
from pathlib import Path

from ..models import Opportunity
from ..services.report_generator import ReportGenerator

logger = logging.getLogger(__name__)


def generate_report(
    opportunities: list[Opportunity],
    format: Literal["markdown", "text", "json", "summary"] = "markdown",
    output_file: Optional[str] = None
) -> str:
    """
    Generate a formatted report from opportunities.

    Creates a report in the specified format and optionally saves to file.

    Args:
        opportunities: List of opportunities to report on
        format: Output format (markdown, text, json, summary)
        output_file: Optional path to save report to file

    Returns:
        Formatted report as string

    Raises:
        ValueError: If opportunities is empty or format is unsupported

    Example:
        >>> opportunities = rank_opportunities(matched_opportunities)
        >>> report = generate_report(opportunities, format="markdown")
        >>> print(report)

        >>> # Save to file
        >>> generate_report(
        ...     opportunities,
        ...     format="markdown",
        ...     output_file="reports/opportunities_2024.md"
        ... )
    """
    if not opportunities:
        raise ValueError("Cannot generate report from empty opportunities list")

    logger.info(
        f"Generating {format} report for {len(opportunities)} opportunities"
    )

    # Generate report
    generator = ReportGenerator()
    report = generator.generate_report(opportunities, format=format)

    # Save to file if requested
    if output_file:
        try:
            output_path = Path(output_file)

            # Create parent directory if needed
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write report
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(report)

            logger.info(f"Report saved to: {output_file}")

        except Exception as e:
            logger.error(f"Error saving report to {output_file}: {e}", exc_info=True)
            raise

    return report


def generate_client_report(
    client_id: str,
    opportunities: list[Opportunity],
    format: Literal["markdown", "text", "json", "summary"] = "markdown",
    output_file: Optional[str] = None
) -> str:
    """
    Generate a report for a specific client.

    Filters opportunities for the specified client and generates report.

    Args:
        client_id: Client ID to generate report for
        opportunities: List of all opportunities
        format: Output format
        output_file: Optional path to save report

    Returns:
        Formatted report for the client

    Raises:
        ValueError: If no opportunities found for client

    Example:
        >>> report = generate_client_report(
        ...     "CLT-2024-001",
        ...     all_opportunities,
        ...     format="markdown"
        ... )
    """
    # Filter opportunities for client
    client_opps = [opp for opp in opportunities if opp.client_id == client_id]

    if not client_opps:
        raise ValueError(f"No opportunities found for client: {client_id}")

    logger.info(
        f"Generating report for client {client_id}: "
        f"{len(client_opps)} opportunities"
    )

    return generate_report(client_opps, format=format, output_file=output_file)


def generate_summary_statistics(
    opportunities: list[Opportunity]
) -> dict:
    """
    Generate summary statistics from opportunities.

    Provides key metrics and aggregations.

    Args:
        opportunities: List of opportunities

    Returns:
        Dictionary with summary statistics

    Example:
        >>> stats = generate_summary_statistics(opportunities)
        >>> print(f"Total revenue: ${stats['total_revenue']:,.2f}")
        >>> print(f"Average match: {stats['avg_match_score']:.1f}%")
    """
    if not opportunities:
        logger.warning("No opportunities for statistics")
        return {
            "total_opportunities": 0,
            "total_revenue": 0.0,
            "avg_match_score": 0.0,
            "avg_revenue": 0.0,
            "high_priority_count": 0,
            "quick_wins_count": 0,
            "high_value_count": 0,
            "unique_clients": 0,
            "unique_scenarios": 0
        }

    logger.info(f"Generating statistics for {len(opportunities)} opportunities")

    # Calculate metrics
    total_revenue = sum(opp.estimated_revenue for opp in opportunities)
    avg_match_score = sum(opp.match_score for opp in opportunities) / len(opportunities)
    avg_revenue = total_revenue / len(opportunities)
    high_priority = sum(1 for opp in opportunities if opp.priority == "high")
    quick_wins = sum(1 for opp in opportunities if opp.is_quick_win())
    high_value = sum(1 for opp in opportunities if opp.is_high_value())
    unique_clients = len(set(opp.client_id for opp in opportunities))
    unique_scenarios = len(set(opp.scenario_id for opp in opportunities))

    stats = {
        "total_opportunities": len(opportunities),
        "total_revenue": total_revenue,
        "avg_match_score": avg_match_score,
        "avg_revenue": avg_revenue,
        "high_priority_count": high_priority,
        "quick_wins_count": quick_wins,
        "high_value_count": high_value,
        "unique_clients": unique_clients,
        "unique_scenarios": unique_scenarios,
        "by_priority": _count_by_field(opportunities, "priority"),
        "by_category": _count_by_field(opportunities, "scenario_category"),
        "revenue_by_priority": _sum_revenue_by_field(opportunities, "priority"),
        "revenue_by_category": _sum_revenue_by_field(opportunities, "scenario_category"),
    }

    logger.info(
        f"Statistics generated: ${total_revenue:,.2f} total revenue, "
        f"{avg_match_score:.1f}% avg match"
    )

    return stats


def export_opportunities_csv(
    opportunities: list[Opportunity],
    output_file: str
) -> None:
    """
    Export opportunities to CSV format.

    Creates a CSV file with key opportunity data for spreadsheet analysis.

    Args:
        opportunities: List of opportunities to export
        output_file: Path to save CSV file

    Raises:
        ValueError: If opportunities is empty

    Example:
        >>> export_opportunities_csv(
        ...     opportunities,
        ...     "reports/opportunities_2024.csv"
        ... )
    """
    if not opportunities:
        raise ValueError("Cannot export empty opportunities list")

    import csv

    logger.info(f"Exporting {len(opportunities)} opportunities to CSV: {output_file}")

    # Create output directory if needed
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Define CSV columns
    columns = [
        "rank",
        "client_id",
        "client_name",
        "scenario_id",
        "scenario_name",
        "category",
        "priority",
        "match_score",
        "estimated_revenue",
        "criteria_met",
        "total_criteria",
        "estimated_time_hours",
        "composite_score",
        "is_quick_win",
        "is_high_value"
    ]

    try:
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()

            for opp in opportunities:
                writer.writerow({
                    "rank": opp.rank,
                    "client_id": opp.client_id,
                    "client_name": opp.client_name,
                    "scenario_id": opp.scenario_id,
                    "scenario_name": opp.scenario_name,
                    "category": opp.scenario_category,
                    "priority": opp.priority,
                    "match_score": f"{opp.match_score:.2f}",
                    "estimated_revenue": f"{opp.estimated_revenue:.2f}",
                    "criteria_met": opp.criteria_met,
                    "total_criteria": opp.total_criteria,
                    "estimated_time_hours": opp.estimated_time_hours or "",
                    "composite_score": f"{opp.composite_score:.2f}" if opp.composite_score else "",
                    "is_quick_win": opp.is_quick_win(),
                    "is_high_value": opp.is_high_value()
                })

        logger.info(f"CSV export complete: {output_file}")

    except Exception as e:
        logger.error(f"Error exporting CSV to {output_file}: {e}", exc_info=True)
        raise


# Private helper functions

def _count_by_field(opportunities: list[Opportunity], field: str) -> dict[str, int]:
    """Count opportunities by a field value."""
    counts = {}
    for opp in opportunities:
        value = getattr(opp, field)
        counts[value] = counts.get(value, 0) + 1
    return counts


def _sum_revenue_by_field(opportunities: list[Opportunity], field: str) -> dict[str, float]:
    """Sum revenue by a field value."""
    totals = {}
    for opp in opportunities:
        value = getattr(opp, field)
        totals[value] = totals.get(value, 0.0) + opp.estimated_revenue
    return totals
