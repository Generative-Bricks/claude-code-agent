"""
OpportunityIQ Client Matcher - Tools

Exports all tool functions for use by the agent.
"""

from .load_scenarios import (
    load_scenarios,
    load_all_scenario_files
)
from .match_clients import (
    match_client_to_scenarios,
    match_clients_to_scenarios
)
from .calculate_revenue import (
    calculate_revenue,
    calculate_revenues_batch,
    estimate_total_revenue
)
from .rank_opportunities import (
    rank_opportunities,
    filter_opportunities,
    get_top_opportunities,
    group_opportunities_by_client
)
from .generate_report import (
    generate_report,
    generate_client_report,
    generate_summary_statistics,
    export_opportunities_csv
)

__all__ = [
    # Load scenarios
    "load_scenarios",
    "load_all_scenario_files",
    # Match clients
    "match_client_to_scenarios",
    "match_clients_to_scenarios",
    # Calculate revenue
    "calculate_revenue",
    "calculate_revenues_batch",
    "estimate_total_revenue",
    # Rank opportunities
    "rank_opportunities",
    "filter_opportunities",
    "get_top_opportunities",
    "group_opportunities_by_client",
    # Generate reports
    "generate_report",
    "generate_client_report",
    "generate_summary_statistics",
    "export_opportunities_csv",
]
