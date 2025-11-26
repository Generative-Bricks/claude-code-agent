"""
Agents package for Multi-Agent Portfolio Collaboration System.

Exports all specialist agents and the Portfolio Manager for easy importing.
"""

from .compliance_officer import (
    analyze_compliance,
    calculate_bond_percentage,
    check_concentration_limits,
    check_suitability,
    compliance_officer_agent,
    get_largest_holding_percentage,
    identify_required_disclosures,
    perform_compliance_check,
)
from .equity_specialist import (
    calculate_sector_allocations,
    calculate_valuation_metrics,
    classify_growth_vs_value,
    equity_specialist_agent,
    generate_detailed_analysis,
    generate_equity_recommendations,
    generate_sector_analysis,
    perform_equity_deep_dive,
)
from .performance_analyst import (
    analyze_portfolio_performance,
    calculate_alpha,
    calculate_holding_return,
    calculate_percentile_rank,
    calculate_sector_attribution,
    calculate_sharpe_ratio,
    calculate_total_return,
    create_performance_analyst_tool,
    identify_bottom_performers,
    identify_top_performers,
    performance_analyst_agent,
    perform_performance_analysis,
)
from .portfolio_manager import (
    portfolio_manager_agent,
    run_comprehensive_analysis,
    generate_client_report,
)
from .risk_analyst import (
    analyze_portfolio_risk,
    calculate_beta,
    calculate_concentration_score,
    calculate_var_95,
    calculate_volatility,
    determine_risk_rating,
    perform_risk_analysis,
    risk_analyst_agent,
)

__all__ = [
    # Portfolio Manager Agent (Orchestrator)
    "portfolio_manager_agent",
    "run_comprehensive_analysis",
    "generate_client_report",
    # Risk Analyst Agent
    "risk_analyst_agent",
    "analyze_portfolio_risk",
    "perform_risk_analysis",
    # Risk calculation functions
    "calculate_volatility",
    "calculate_var_95",
    "calculate_beta",
    "calculate_concentration_score",
    "determine_risk_rating",
    # Compliance Officer Agent
    "compliance_officer_agent",
    "perform_compliance_check",
    "analyze_compliance",
    # Compliance check functions
    "check_suitability",
    "check_concentration_limits",
    "identify_required_disclosures",
    "calculate_bond_percentage",
    "get_largest_holding_percentage",
    # Performance Analyst Agent
    "performance_analyst_agent",
    "create_performance_analyst_tool",
    "analyze_portfolio_performance",
    "perform_performance_analysis",
    # Performance calculation functions
    "calculate_holding_return",
    "calculate_total_return",
    "calculate_sector_attribution",
    "calculate_sharpe_ratio",
    "calculate_alpha",
    "calculate_percentile_rank",
    "identify_top_performers",
    "identify_bottom_performers",
    # Equity Specialist Agent
    "equity_specialist_agent",
    "perform_equity_deep_dive",
    # Equity analysis functions
    "calculate_sector_allocations",
    "generate_sector_analysis",
    "calculate_valuation_metrics",
    "classify_growth_vs_value",
    "generate_equity_recommendations",
    "generate_detailed_analysis",
]
