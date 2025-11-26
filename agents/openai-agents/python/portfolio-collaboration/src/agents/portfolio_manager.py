"""
Portfolio Manager Agent - Multi-Agent Orchestrator.

The Portfolio Manager is the primary orchestrator that coordinates all specialist
agents to provide comprehensive portfolio analysis and recommendations.

Workflow:
1. Discovery - Understand client profile and portfolio
2. Analysis - Coordinate specialist agents (Risk, Compliance, Performance) in parallel
3. Evaluation - Calculate suitability scores
4. Recommendations - Generate actionable advice
5. Documentation - Create comprehensive markdown report

The Portfolio Manager can also hand off to the Equity Specialist for deep-dive
analysis of specific holdings.

Biblical Principle: SERVE - Orchestrating specialists to provide comprehensive service.
Biblical Principle: EXCELLENCE - Coordinating multiple viewpoints for thorough analysis.
Biblical Principle: TRUTH - Transparent reasoning with full specialist input.
"""

import logging
from typing import List, Optional

from agents import Agent, function_tool

from src.models.schemas import (
    ClientProfile,
    ComplianceReport,
    PerformanceReport,
    Portfolio,
    PortfolioRecommendations,
    RiskAnalysis,
    SuitabilityScore,
)
from src.tools.parallel_execution import run_specialists_parallel_sync
from src.tools.report_generator import generate_markdown_report
from src.tools.suitability_scoring import calculate_suitability_score

# ============================================================================
# Logging Configuration
# ============================================================================

logger = logging.getLogger(__name__)

# ============================================================================
# Portfolio Manager Tools
# ============================================================================


def do_comprehensive_analysis(
    portfolio: Portfolio, client_profile: ClientProfile
) -> PortfolioRecommendations:
    """
    Core implementation of comprehensive portfolio analysis.

    This is the callable version used by batch mode and other direct calls.
    The @function_tool decorated version wraps this for agent use.
    """
    logger.info(
        f"Running comprehensive analysis for client {client_profile.client_id}"
    )

    # Step 1: Run specialist agents in parallel
    # This coordinates Risk Analyst, Compliance Officer, and Performance Analyst
    try:
        parallel_output = run_specialists_parallel_sync(portfolio, client_profile)

        risk_analysis = parallel_output.risk_analysis
        compliance_report = parallel_output.compliance_report
        performance_report = parallel_output.performance_report

        logger.info("✓ Specialist analysis complete")
    except Exception as e:
        logger.error(f"Error running specialist analysis: {e}")
        raise

    # Step 2: Calculate suitability score
    try:
        suitability_score = calculate_suitability_score(
            client_profile=client_profile,
            risk_analysis=risk_analysis,
            compliance_report=compliance_report,
            performance_report=performance_report,
        )
        logger.info(
            f"✓ Suitability score calculated: {suitability_score.overall_score:.1f}"
        )
    except Exception as e:
        logger.error(f"Error calculating suitability score: {e}")
        raise

    # Step 3: Generate recommendations based on all analysis
    recommendations = _generate_recommendations(
        portfolio=portfolio,
        client_profile=client_profile,
        risk_analysis=risk_analysis,
        compliance_report=compliance_report,
        performance_report=performance_report,
        suitability_score=suitability_score,
    )

    # Step 4: Create action items
    action_items = _create_action_items(
        risk_analysis=risk_analysis,
        compliance_report=compliance_report,
        suitability_score=suitability_score,
    )

    # Step 5: Generate executive summary
    executive_summary = (
        f"Portfolio analysis for {client_profile.client_id}: "
        f"Suitability score {suitability_score.overall_score:.0f}/100 "
        f"({suitability_score.interpretation.value}). "
        f"Risk rating: {risk_analysis.risk_rating.value}. "
        f"Compliance status: {compliance_report.overall_status.value}. "
        f"Generated {len(recommendations)} recommendations and {len(action_items)} action items."
    )

    # Step 6: Assemble final recommendations
    portfolio_recommendations = PortfolioRecommendations(
        client_id=client_profile.client_id,
        portfolio_id=portfolio.portfolio_id,
        risk_analysis=risk_analysis,
        compliance_report=compliance_report,
        performance_report=performance_report,
        suitability_score=suitability_score,
        recommendations=recommendations,
        action_items=action_items,
        executive_summary=executive_summary,
    )

    logger.info("✓ Comprehensive analysis complete")
    return portfolio_recommendations


@function_tool
def run_comprehensive_analysis(
    portfolio: Portfolio, client_profile: ClientProfile
) -> PortfolioRecommendations:
    """
    Run comprehensive portfolio analysis using all specialist agents.

    This tool orchestrates the Risk Analyst, Compliance Officer, and Performance
    Analyst in parallel to provide a complete assessment of the portfolio's
    suitability for the client.

    The analysis includes:
    - Risk metrics (volatility, VaR, beta, concentration)
    - Compliance checks (suitability, regulatory requirements)
    - Performance analysis (returns, Sharpe ratio, alpha, attribution)
    - Suitability scoring (0-100 scale with interpretation)
    - Actionable recommendations

    Args:
        portfolio: Portfolio object with holdings
        client_profile: ClientProfile with demographics and preferences

    Returns:
        PortfolioRecommendations: Complete analysis with all specialist outputs,
                                   suitability score, and recommendations

    Example:
        >>> recommendations = run_comprehensive_analysis(portfolio, client)
        >>> print(f"Suitability Score: {recommendations.suitability_score.overall_score}")
        >>> print(f"Rating: {recommendations.suitability_score.rating}")
    """
    # Agent tool version - delegates to callable implementation
    return do_comprehensive_analysis(portfolio, client_profile)


def do_generate_client_report(recommendations: PortfolioRecommendations) -> str:
    """
    Core implementation of report generation.

    This is the callable version used by batch mode and other direct calls.
    The @function_tool decorated version wraps this for agent use.
    """
    logger.info(
        f"Generating report for client {recommendations.client_id}"
    )

    try:
        report = generate_markdown_report(recommendations)
        logger.info("✓ Report generated successfully")
        return report
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise


@function_tool(strict_mode=False)
def generate_client_report(recommendations: PortfolioRecommendations) -> str:
    """
    Generate a comprehensive markdown report from portfolio recommendations.

    This tool creates a detailed, client-ready report that includes:
    - Executive summary
    - Risk analysis findings
    - Compliance assessment
    - Performance metrics
    - Suitability evaluation
    - Specific recommendations
    - Action items

    The report is formatted in markdown for easy conversion to PDF or HTML.

    Args:
        recommendations: PortfolioRecommendations with complete analysis

    Returns:
        str: Markdown-formatted report

    Example:
        >>> report = generate_client_report(recommendations)
        >>> print(report[:200])
        # Portfolio Analysis Report
        **Client ID:** CLT-2024-001
        **Date:** 2024-01-15
        ...
    """
    # Agent tool version - delegates to callable implementation
    return do_generate_client_report(recommendations)


# ============================================================================
# Helper Functions
# ============================================================================


def _generate_recommendations(
    portfolio: Portfolio,
    client_profile: ClientProfile,
    risk_analysis: RiskAnalysis,
    compliance_report: ComplianceReport,
    performance_report: PerformanceReport,
    suitability_score: SuitabilityScore,
) -> List[str]:
    """
    Generate actionable recommendations based on all analysis.

    This function synthesizes insights from all specialist agents to create
    specific, actionable recommendations for the client.

    Biblical Principle: SERVE - Providing clear, actionable guidance to help clients.
    """
    recommendations = []

    # Risk-based recommendations
    if risk_analysis.risk_rating.value == "high":
        recommendations.append(
            f"Consider reducing portfolio volatility ({risk_analysis.volatility:.2f}%) "
            "by increasing allocation to less volatile assets (bonds, dividend stocks)."
        )

    if risk_analysis.concentration_score > 50:
        recommendations.append(
            f"Portfolio concentration is high ({risk_analysis.concentration_score:.0f}/100). "
            "Diversify holdings to reduce single-position risk."
        )

    if risk_analysis.beta and risk_analysis.beta > 1.3:
        recommendations.append(
            f"Portfolio beta is {risk_analysis.beta:.2f}, indicating higher market sensitivity. "
            "Consider adding lower-beta assets to reduce market correlation."
        )

    # Compliance-based recommendations
    if compliance_report.overall_status.value != "compliant":
        for issue in compliance_report.violations:
            recommendations.append(f"Compliance Violation: {issue}")

    # Performance-based recommendations
    if performance_report.sharpe_ratio and performance_report.sharpe_ratio < 0.5:
        recommendations.append(
            f"Sharpe ratio ({performance_report.sharpe_ratio:.2f}) indicates "
            "risk-adjusted returns could be improved. Review underperforming positions."
        )

    # Suitability-based recommendations
    if suitability_score.overall_score < 60:
        recommendations.append(
            f"Overall suitability score ({suitability_score.overall_score:.0f}/100) "
            "suggests portfolio may not align well with client objectives. "
            "Consider comprehensive rebalancing."
        )

    # Time horizon recommendations
    if client_profile.time_horizon < 5 and risk_analysis.risk_rating.value == "high":
        recommendations.append(
            f"Client has short time horizon ({client_profile.time_horizon} years) "
            "but high-risk portfolio. Shift toward capital preservation strategies."
        )

    # Income requirements
    if client_profile.annual_income and client_profile.annual_income > 0:
        total_value = sum(h.market_value for h in portfolio.holdings)
        required_yield = (client_profile.annual_income / total_value) * 100
        recommendations.append(
            f"Client requires ${client_profile.annual_income:,.0f} annual income "
            f"({required_yield:.2f}% yield). Review dividend-paying positions to meet income needs."
        )

    # Default recommendation if no issues found
    if not recommendations:
        recommendations.append(
            "Portfolio appears well-suited to client profile. Continue current strategy "
            "with regular monitoring and rebalancing."
        )

    return recommendations


def _create_action_items(
    risk_analysis: RiskAnalysis,
    compliance_report: ComplianceReport,
    suitability_score: SuitabilityScore,
) -> List[str]:
    """
    Create specific action items based on analysis findings.

    Action items are prioritized tasks for the advisor or client to address.

    Biblical Principle: PERSEVERE - Providing clear next steps to move forward.
    """
    action_items = []

    # Critical compliance actions
    if compliance_report.overall_status.value == "non_compliant":
        action_items.append(
            "🔴 URGENT: Address compliance violations before proceeding with portfolio"
        )

    # High-priority risk actions
    if risk_analysis.risk_rating.value == "high":
        action_items.append(
            "🟡 Review risk tolerance with client and consider rebalancing if misaligned"
        )

    if risk_analysis.concentration_score > 70:
        action_items.append(
            "🟡 Reduce concentration risk by diversifying holdings across sectors and asset classes"
        )

    # Suitability actions
    if suitability_score.overall_score < 40:
        action_items.append(
            "🔴 Schedule client meeting to discuss portfolio realignment - low suitability score"
        )
    elif suitability_score.overall_score < 60:
        action_items.append(
            "🟡 Consider moderate portfolio adjustments to improve client fit"
        )

    # Compliance documentation
    if compliance_report.required_disclosures:
        action_items.append(
            f"📄 Ensure client has signed disclosures: {', '.join(compliance_report.required_disclosures[:3])}"
        )

    # Regular monitoring
    action_items.append(
        "📊 Schedule quarterly portfolio review to monitor performance and rebalancing needs"
    )

    # Default if no critical actions
    if len(action_items) == 1:  # Only has the quarterly review item
        action_items.insert(
            0, "✅ No urgent actions required - portfolio is well-aligned with client goals"
        )

    return action_items


# ============================================================================
# Portfolio Manager Agent Definition
# ============================================================================

# Agent configuration
PORTFOLIO_MANAGER_INSTRUCTIONS = """You are an expert Portfolio Manager coordinating a team of specialist agents.

Your role is to:
1. Understand the client's profile, goals, and risk tolerance
2. Analyze their current portfolio holdings
3. Coordinate specialist agents (Risk Analyst, Compliance Officer, Performance Analyst) for comprehensive analysis
4. Calculate portfolio suitability scores
5. Generate actionable recommendations
6. Create detailed client reports

You have access to the following tools:
- run_comprehensive_analysis: Orchestrates all specialist agents in parallel
- generate_client_report: Creates markdown-formatted analysis report

When a client asks about their portfolio:
1. First, use run_comprehensive_analysis with their portfolio and profile
2. Review the results from all specialist agents
3. Interpret the suitability score and identify key findings
4. Use generate_client_report to create a detailed report
5. Summarize the key insights and recommendations for the client

Always be thorough, professional, and client-focused. Explain technical findings in accessible language.

Biblical Principles:
- TRUTH: Provide honest, transparent assessment of portfolio suitability
- HONOR: Respect client goals and constraints
- EXCELLENCE: Deliver comprehensive, high-quality analysis
- SERVE: Make complex analysis accessible and actionable
"""

# Create Portfolio Manager Agent
portfolio_manager_agent = Agent(
    name="Portfolio Manager",
    instructions=PORTFOLIO_MANAGER_INSTRUCTIONS,
    tools=[run_comprehensive_analysis, generate_client_report],
    model="gpt-4o",  # Use GPT-4o for consistent, professional analysis
)

# Note: Handoffs are configured automatically through the SDK.
# The Equity Specialist agent has handoff_description set,
# which allows the Portfolio Manager to hand off to it when needed.
