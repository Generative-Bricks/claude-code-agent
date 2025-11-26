"""
Report Generator Tool for Multi-Agent Portfolio Collaboration System.

This module generates human-readable markdown reports from portfolio analysis results,
combining outputs from all specialist agents into a comprehensive client report.

Biblical Principle: TRUTH - All analysis results are presented clearly and transparently.
Biblical Principle: SERVE - Reports are designed for clarity and actionable insights.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.models.schemas import (
    ComplianceReport,
    PerformanceReport,
    PortfolioRecommendations,
    RiskAnalysis,
    SuitabilityScore,
)


def generate_markdown_report(recommendations: PortfolioRecommendations) -> str:
    """
    Generate complete markdown report from portfolio analysis.

    This is the main entry point for report generation, combining all specialist
    outputs into a comprehensive, well-formatted markdown report.

    Args:
        recommendations: Complete portfolio analysis with all specialist outputs

    Returns:
        Formatted markdown report as string

    Example:
        >>> report = generate_markdown_report(recommendations)
        >>> print(report)
        # Portfolio Analysis Report
        ...
    """
    # Extract portfolio details from embedded analysis
    portfolio_value = _format_currency(
        recommendations.performance_report.total_return
    )  # Will be calculated from holdings
    analysis_date = recommendations.analysis_date.strftime("%Y-%m-%d")

    # Build report sections
    sections = [
        _generate_header(
            recommendations.client_id,
            analysis_date,
            portfolio_value,
            recommendations.risk_analysis,
        ),
        _generate_executive_summary(
            recommendations.executive_summary, recommendations.suitability_score
        ),
        format_risk_section(recommendations.risk_analysis),
        format_compliance_section(recommendations.compliance_report),
        format_performance_section(recommendations.performance_report),
        format_suitability_section(recommendations.suitability_score),
        _generate_recommendations_section(recommendations.recommendations),
        _generate_action_items_section(recommendations.action_items),
        _generate_footer(recommendations.analysis_date),
    ]

    # Combine all sections with double newlines
    return "\n\n".join(sections)


def _generate_header(
    client_id: str, analysis_date: str, portfolio_value: str, risk_analysis: RiskAnalysis
) -> str:
    """
    Generate report header with key portfolio information.

    Args:
        client_id: Client identifier
        analysis_date: Analysis date (YYYY-MM-DD format)
        portfolio_value: Formatted portfolio value
        risk_analysis: Risk analysis for benchmark info

    Returns:
        Formatted header section
    """
    return f"""# Portfolio Analysis Report

**Client:** {client_id} | **Date:** {analysis_date}
**Portfolio Value:** {portfolio_value} | **Benchmark:** SPY

---"""


def _generate_executive_summary(
    executive_summary: str, suitability_score: SuitabilityScore
) -> str:
    """
    Generate executive summary section.

    Args:
        executive_summary: Executive summary text
        suitability_score: Overall suitability scoring

    Returns:
        Formatted executive summary section
    """
    overall_score = int(round(suitability_score.overall_score))
    interpretation = suitability_score.interpretation.value

    return f"""## Executive Summary

{executive_summary}

**Overall Suitability:** {overall_score}/100 - {interpretation}

---"""


def format_risk_section(risk_analysis: RiskAnalysis) -> str:
    """
    Format risk analysis section with metrics table and recommendations.

    Args:
        risk_analysis: Risk analysis output from Risk Analyst Agent

    Returns:
        Formatted markdown section for risk analysis

    Example:
        >>> section = format_risk_section(risk_analysis)
        >>> print(section)
        ## Risk Analysis
        | Metric | Value | Rating |
        ...
    """
    # Format metrics for table
    volatility = f"{risk_analysis.volatility:.1f}%"
    beta = f"{risk_analysis.beta:.2f}"
    var_95 = f"{risk_analysis.var_95:.1f}%"
    concentration = f"{int(round(risk_analysis.concentration_score))}/100"

    # Build metrics table
    metrics_table = f"""| Metric | Value | Rating |
|--------|-------|--------|
| Volatility | {volatility} | {risk_analysis.risk_rating.value} |
| Beta | {beta} | {risk_analysis.risk_rating.value} |
| VaR 95% | {var_95} | {risk_analysis.risk_rating.value} |
| Concentration | {concentration} | {risk_analysis.risk_rating.value} |"""

    # Format concerns list
    concerns_list = (
        "\n".join(f"- {concern}" for concern in risk_analysis.concerns)
        if risk_analysis.concerns
        else "- None identified"
    )

    # Format recommendations list
    recommendations_list = (
        "\n".join(f"- {rec}" for rec in risk_analysis.recommendations)
        if risk_analysis.recommendations
        else "- No specific recommendations at this time"
    )

    return f"""## Risk Analysis

{metrics_table}

**Risk Rating:** {risk_analysis.risk_rating.value.upper()}

**Concerns:**
{concerns_list}

**Recommendations:**
{recommendations_list}

---"""


def format_compliance_section(compliance_report: ComplianceReport) -> str:
    """
    Format compliance review section with status and violations.

    Args:
        compliance_report: Compliance analysis output from Compliance Officer Agent

    Returns:
        Formatted markdown section for compliance review

    Example:
        >>> section = format_compliance_section(compliance_report)
        >>> print(section)
        ## Compliance Review
        **Status:** PASS
        ...
    """
    # Format checks performed
    checks_list = "\n".join(
        f"- {check}" for check in compliance_report.checks_performed
    )

    # Format violations or show none
    violations_text = (
        "\n".join(f"- {violation}" for violation in compliance_report.violations)
        if compliance_report.violations
        else "None"
    )

    # Format required disclosures
    disclosures_list = (
        "\n".join(f"- {disclosure}" for disclosure in compliance_report.required_disclosures)
        if compliance_report.required_disclosures
        else "- None required"
    )

    return f"""## Compliance Review

**Status:** {compliance_report.overall_status.value}

**Checks Performed:**
{checks_list}

**Violations:** {violations_text}

**Required Disclosures:**
{disclosures_list}

---"""


def format_performance_section(performance_report: PerformanceReport) -> str:
    """
    Format performance analysis section with metrics and attribution.

    Args:
        performance_report: Performance analysis output from Performance Analyst Agent

    Returns:
        Formatted markdown section for performance analysis

    Example:
        >>> section = format_performance_section(performance_report)
        >>> print(section)
        ## Performance Analysis
        | Metric | Value |
        ...
    """
    # Format metrics table
    total_return = f"{performance_report.total_return:.1f}%"
    benchmark_return = f"{performance_report.benchmark_return:.1f}%"
    excess_return = _format_signed_percentage(performance_report.excess_return)
    sharpe_ratio = f"{performance_report.sharpe_ratio:.2f}"
    alpha = (
        _format_signed_percentage(performance_report.alpha)
        if performance_report.alpha is not None
        else "N/A"
    )
    percentile = (
        f"{performance_report.percentile_rank}th"
        if performance_report.percentile_rank
        else "N/A"
    )

    metrics_table = f"""| Metric | Value |
|--------|-------|
| Total Return | {total_return} |
| Benchmark Return | {benchmark_return} |
| Excess Return | {excess_return} |
| Sharpe Ratio | {sharpe_ratio} |
| Alpha | {alpha} |
| Percentile Rank | {percentile} |"""

    # Format top performers
    top_performers_list = (
        "\n".join(f"- {performer}" for performer in performance_report.top_performers)
        if performance_report.top_performers
        else "- None specified"
    )

    # Format sector attribution table
    attribution_table = ""
    if performance_report.attribution:
        attribution_table = "\n**Sector Attribution:**\n| Sector | Contribution |\n|--------|-------------|\n"
        for sector, contribution in performance_report.attribution.items():
            formatted_contribution = _format_signed_percentage(contribution)
            attribution_table += f"| {sector} | {formatted_contribution} |\n"

    return f"""## Performance Analysis

{metrics_table}

**Top Performers:**
{top_performers_list}
{attribution_table}
---"""


def format_suitability_section(suitability_score: SuitabilityScore) -> str:
    """
    Format suitability analysis section with component scores.

    Args:
        suitability_score: Suitability scoring from synthesis stage

    Returns:
        Formatted markdown section for suitability analysis

    Example:
        >>> section = format_suitability_section(suitability_score)
        >>> print(section)
        ## Suitability Analysis
        **Overall Score:** 85/100 - Highly Suitable
        ...
    """
    # Format overall score
    overall = int(round(suitability_score.overall_score))
    interpretation = suitability_score.interpretation.value

    # Format component scores
    risk_fit = int(round(suitability_score.risk_fit))
    compliance_fit = int(round(suitability_score.compliance_fit))
    performance_fit = int(round(suitability_score.performance_fit))
    time_horizon_fit = int(round(suitability_score.time_horizon_fit))

    return f"""## Suitability Analysis

**Overall Score:** {overall}/100 - {interpretation}

**Component Scores:**
- Risk Fit: {risk_fit}/100
- Compliance Fit: {compliance_fit}/100
- Performance Fit: {performance_fit}/100
- Time Horizon Fit: {time_horizon_fit}/100

**Explanation:**
{suitability_score.explanation}

---"""


def _generate_recommendations_section(recommendations: list[str]) -> str:
    """
    Generate recommendations section with numbered list.

    Args:
        recommendations: List of portfolio recommendations

    Returns:
        Formatted recommendations section
    """
    recommendations_list = "\n".join(
        f"{i}. {rec}" for i, rec in enumerate(recommendations, start=1)
    )

    return f"""## Recommendations

{recommendations_list}

---"""


def _generate_action_items_section(action_items: list[str]) -> str:
    """
    Generate action items section with bulleted list.

    Args:
        action_items: List of immediate action items

    Returns:
        Formatted action items section
    """
    if not action_items:
        action_items_list = "- No immediate action items"
    else:
        action_items_list = "\n".join(f"- {item}" for item in action_items)

    return f"""## Action Items

{action_items_list}

---"""


def _generate_footer(analysis_date: datetime) -> str:
    """
    Generate report footer with timestamp.

    Args:
        analysis_date: Analysis timestamp

    Returns:
        Formatted footer
    """
    formatted_date = analysis_date.strftime("%Y-%m-%d %H:%M:%S")
    return f"*Report generated on {formatted_date}*"


def _format_currency(value: float) -> str:
    """
    Format value as currency with commas and dollar sign.

    Args:
        value: Numeric value to format

    Returns:
        Formatted currency string

    Example:
        >>> _format_currency(1500000)
        '$1,500,000'
    """
    return f"${value:,.0f}"


def _format_signed_percentage(value: float) -> str:
    """
    Format percentage with sign (+ or -).

    Args:
        value: Percentage value to format

    Returns:
        Formatted percentage string with sign

    Example:
        >>> _format_signed_percentage(5.7)
        '+5.7%'
        >>> _format_signed_percentage(-2.3)
        '-2.3%'
    """
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.1f}%"


def save_report_to_file(
    report_content: str, filename: Optional[str] = None, output_dir: str = "reports"
) -> str:
    """
    Save markdown report to file.

    Creates output directory if it doesn't exist. Generates filename based on
    timestamp if not provided.

    Args:
        report_content: Markdown report content to save
        filename: Optional custom filename (without extension)
        output_dir: Output directory path (relative to project root)

    Returns:
        Absolute path to saved report file

    Example:
        >>> report = generate_markdown_report(recommendations)
        >>> filepath = save_report_to_file(report, "client_123_analysis")
        >>> print(filepath)
        /path/to/project/reports/client_123_analysis.md
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"portfolio_report_{timestamp}"

    # Ensure .md extension
    if not filename.endswith(".md"):
        filename = f"{filename}.md"

    # Full file path
    file_path = output_path / filename

    # Write report to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    # Return absolute path
    return str(file_path.absolute())
