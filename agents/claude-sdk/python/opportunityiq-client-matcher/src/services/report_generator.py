"""
Report generation service for OpportunityIQ Client Matcher.

Creates formatted output reports from matched opportunities.

SERVE Principle: Clear, actionable reports that help advisors make decisions.
"""

import logging
from typing import Literal
from datetime import datetime

from ..models import Opportunity

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Generates formatted reports from opportunity data.

    Supports multiple output formats: markdown, text, json, summary.
    """

    def generate_report(
        self,
        opportunities: list[Opportunity],
        format: Literal["markdown", "text", "json", "summary"] = "markdown"
    ) -> str:
        """
        Generate a formatted report from opportunities.

        Args:
            opportunities: List of matched opportunities
            format: Output format (markdown, text, json, summary)

        Returns:
            Formatted report as string

        Raises:
            ValueError: If format is unsupported or opportunities is empty
        """
        if not opportunities:
            raise ValueError("Cannot generate report from empty opportunities list")

        logger.info(
            f"Generating {format} report for {len(opportunities)} opportunities"
        )

        if format == "markdown":
            return self._generate_markdown(opportunities)
        elif format == "text":
            return self._generate_text(opportunities)
        elif format == "json":
            return self._generate_json(opportunities)
        elif format == "summary":
            return self._generate_summary(opportunities)
        else:
            raise ValueError(f"Unsupported report format: {format}")

    def _generate_markdown(self, opportunities: list[Opportunity]) -> str:
        """
        Generate a markdown formatted report.

        Args:
            opportunities: List of opportunities

        Returns:
            Markdown formatted report
        """
        lines = []

        # Header
        lines.append("# OpportunityIQ Client Matcher Report\n")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        lines.append(f"**Total Opportunities:** {len(opportunities)}\n")
        lines.append("---\n")

        # Summary statistics
        total_revenue = sum(opp.estimated_revenue for opp in opportunities)
        avg_match_score = sum(opp.match_score for opp in opportunities) / len(opportunities)
        high_priority = sum(1 for opp in opportunities if opp.priority == "high")

        lines.append("## Summary Statistics\n")
        lines.append(f"- **Total Estimated Revenue:** ${total_revenue:,.2f}")
        lines.append(f"- **Average Match Score:** {avg_match_score:.1f}%")
        lines.append(f"- **High Priority Opportunities:** {high_priority}")
        lines.append(f"- **Quick Wins:** {sum(1 for opp in opportunities if opp.is_quick_win())}\n")
        lines.append("---\n")

        # Detailed opportunities
        lines.append("## Opportunity Details\n")

        for opp in opportunities:
            lines.append(f"### {opp.rank}. {opp.scenario_name}\n")
            lines.append(f"**Client:** {opp.client_name} (ID: {opp.client_id})")
            lines.append(f"**Category:** {opp.scenario_category}")
            lines.append(f"**Priority:** {opp.priority.upper()}")
            lines.append(f"**Match Score:** {opp.match_score:.1f}%")
            lines.append(f"**Estimated Revenue:** ${opp.estimated_revenue:,.2f}")

            if opp.estimated_time_hours:
                lines.append(f"**Estimated Time:** {opp.estimated_time_hours} hours")

            # Match details
            lines.append(f"\n**Match Details:**")
            lines.append(f"- Criteria Met: {opp.criteria_met} / {opp.total_criteria}")
            for detail in opp.match_details[:3]:  # Show top 3
                status = "✓" if detail.matched else "✗"
                lines.append(
                    f"  - {status} {detail.criterion_field}: "
                    f"{detail.actual_value} {detail.operator} {detail.expected_value}"
                )

            # Revenue breakdown
            lines.append(f"\n**Revenue Calculation:**")
            rev_calc = opp.revenue_calculation
            lines.append(f"- Formula Type: {rev_calc.formula_type}")
            lines.append(f"- Base Rate: {rev_calc.base_rate}")
            if rev_calc.multiplier_value:
                lines.append(f"- Multiplier Value: ${rev_calc.multiplier_value:,.2f}")
            lines.append(f"- Calculated: ${rev_calc.calculated_amount:,.2f}")
            if rev_calc.min_applied or rev_calc.max_applied:
                adjustments = []
                if rev_calc.min_applied:
                    adjustments.append("minimum applied")
                if rev_calc.max_applied:
                    adjustments.append("maximum applied")
                lines.append(f"- Adjustments: {', '.join(adjustments)}")

            # Compliance notes
            if opp.compliance_notes:
                lines.append(f"\n**Compliance:** {opp.compliance_notes}")

            lines.append("\n---\n")

        return "\n".join(lines)

    def _generate_text(self, opportunities: list[Opportunity]) -> str:
        """
        Generate a plain text report.

        Args:
            opportunities: List of opportunities

        Returns:
            Plain text report
        """
        lines = []

        # Header
        lines.append("=" * 70)
        lines.append("OpportunityIQ Client Matcher Report")
        lines.append("=" * 70)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Total Opportunities: {len(opportunities)}")
        lines.append("=" * 70)
        lines.append("")

        # Summary
        total_revenue = sum(opp.estimated_revenue for opp in opportunities)
        avg_match_score = sum(opp.match_score for opp in opportunities) / len(opportunities)

        lines.append("SUMMARY STATISTICS")
        lines.append("-" * 70)
        lines.append(f"Total Estimated Revenue:    ${total_revenue:,.2f}")
        lines.append(f"Average Match Score:        {avg_match_score:.1f}%")
        lines.append(f"High Priority Opportunities: {sum(1 for opp in opportunities if opp.priority == 'high')}")
        lines.append("")

        # Opportunities
        lines.append("OPPORTUNITIES")
        lines.append("-" * 70)

        for opp in opportunities:
            lines.append(f"\n{opp.rank}. {opp.scenario_name}")
            lines.append(f"   Client: {opp.client_name} ({opp.client_id})")
            lines.append(f"   Match Score: {opp.match_score:.1f}% | Revenue: ${opp.estimated_revenue:,.2f}")
            lines.append(f"   Priority: {opp.priority.upper()} | Category: {opp.scenario_category}")
            lines.append(f"   Criteria Met: {opp.criteria_met}/{opp.total_criteria}")

            if opp.estimated_time_hours:
                lines.append(f"   Est. Time: {opp.estimated_time_hours} hours")

            lines.append("")

        lines.append("=" * 70)

        return "\n".join(lines)

    def _generate_json(self, opportunities: list[Opportunity]) -> str:
        """
        Generate a JSON report.

        Args:
            opportunities: List of opportunities

        Returns:
            JSON formatted report
        """
        import json

        # Convert opportunities to dict format
        data = {
            "generated_at": datetime.now().isoformat(),
            "total_opportunities": len(opportunities),
            "total_revenue": sum(opp.estimated_revenue for opp in opportunities),
            "opportunities": [
                opp.model_dump(mode="json") for opp in opportunities
            ]
        }

        return json.dumps(data, indent=2)

    def _generate_summary(self, opportunities: list[Opportunity]) -> str:
        """
        Generate a brief summary report.

        Args:
            opportunities: List of opportunities

        Returns:
            Summary report
        """
        lines = []

        total_revenue = sum(opp.estimated_revenue for opp in opportunities)
        avg_match_score = sum(opp.match_score for opp in opportunities) / len(opportunities)
        high_priority = sum(1 for opp in opportunities if opp.priority == "high")
        quick_wins = sum(1 for opp in opportunities if opp.is_quick_win())

        lines.append("OpportunityIQ Summary")
        lines.append("=" * 50)
        lines.append(f"Total Opportunities: {len(opportunities)}")
        lines.append(f"Estimated Revenue:   ${total_revenue:,.2f}")
        lines.append(f"Avg Match Score:     {avg_match_score:.1f}%")
        lines.append(f"High Priority:       {high_priority}")
        lines.append(f"Quick Wins:          {quick_wins}")
        lines.append("")

        lines.append("Top 5 Opportunities:")
        lines.append("-" * 50)
        for opp in opportunities[:5]:
            lines.append(
                f"{opp.rank}. {opp.client_name} - {opp.scenario_name} "
                f"(${opp.estimated_revenue:,.0f}, {opp.match_score:.0f}%)"
            )

        return "\n".join(lines)
