"""
Report generation for client opportunities.

This module generates reports in various formats (Markdown, JSON, Summary)
summarizing matched opportunities with revenue estimates and match details.
"""

import json
import logging
from pathlib import Path
from typing import Any

from ..models import Opportunity

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Generator for creating opportunity reports in multiple formats.

    Supports:
    - Markdown: Human-readable detailed reports
    - JSON: Machine-readable structured data
    - Summary: Brief overview with key statistics
    """

    def generate(
        self,
        opportunities: list[Opportunity],
        format: str,
        output_file: str | None = None
    ) -> str:
        """
        Generate a report for the given opportunities.

        Args:
            opportunities: List of client opportunities to include
            format: Output format ("markdown", "json", or "summary")
            output_file: Optional file path to write report to

        Returns:
            The generated report as a string

        Example:
            >>> generator = ReportGenerator()
            >>> report = generator.generate(opportunities, "markdown", "report.md")
            >>> print(f"Report written to report.md")
        """
        logger.info(
            f"Generating {format} report for {len(opportunities)} opportunities"
        )

        # Generate report based on format
        if format == "markdown":
            report_content = self._generate_markdown(opportunities)
        elif format == "json":
            report_content = self._generate_json(opportunities)
        elif format == "summary":
            report_content = self._generate_summary(opportunities)
        else:
            logger.warning(f"Unknown format: {format}, defaulting to summary")
            report_content = self._generate_summary(opportunities)

        # Write to file if specified
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(report_content)
            logger.info(f"Report written to {output_file}")

        return report_content

    def _generate_markdown(self, opportunities: list[Opportunity]) -> str:
        """
        Generate a detailed Markdown report.

        Args:
            opportunities: List of opportunities to report on

        Returns:
            Markdown-formatted report string
        """
        lines = [
            "# Client Opportunity Report",
            "",
            f"**Total Opportunities:** {len(opportunities)}",
            ""
        ]

        # Summary statistics
        if opportunities:
            total_revenue = sum(
                opp.estimated_revenue
                for opp in opportunities
            )
            avg_match_score = sum(
                opp.match_score
                for opp in opportunities
            ) / len(opportunities)

            priority_counts = self._count_by_priority(opportunities)

            lines.extend([
                "## Summary",
                "",
                f"- **Total Estimated Revenue:** ${total_revenue:,.2f}",
                f"- **Average Match Score:** {avg_match_score:.1f}%",
                f"- **Priority Breakdown:**",
                f"  - High: {priority_counts.get('high', 0)}",
                f"  - Medium: {priority_counts.get('medium', 0)}",
                f"  - Low: {priority_counts.get('low', 0)}",
                ""
            ])

        # Individual opportunities
        lines.append("## Opportunities")
        lines.append("")

        # Sort by priority and match score
        sorted_opps = sorted(
            opportunities,
            key=lambda x: (
                {"high": 0, "medium": 1, "low": 2}.get(x.priority, 3),
                -x.match_score
            )
        )

        for opp in sorted_opps:
            lines.extend([
                f"### {opp.scenario_name} - {opp.client_name}",
                "",
                f"**Priority:** {opp.priority.upper()}",
                f"**Match Score:** {opp.match_score:.1f}%",
                f"**Estimated Revenue:** ${opp.estimated_revenue:,.2f}",
                "",
                "**Match Details:**",
                ""
            ])

            for detail in opp.match_details:
                status = "✓" if detail.matched else "✗"
                lines.append(
                    f"- {status} **{detail.criterion_field}** "
                    f"(expected: {detail.expected_value}, actual: {detail.actual_value})"
                )

            lines.append("")

        return "\n".join(lines)

    def _generate_json(self, opportunities: list[Opportunity]) -> str:
        """
        Generate a JSON report.

        Args:
            opportunities: List of opportunities to report on

        Returns:
            JSON-formatted report string
        """
        report_data = {
            "summary": {
                "total_opportunities": len(opportunities),
                "total_revenue": sum(
                    opp.estimated_revenue
                    for opp in opportunities
                ),
                "average_match_score": (
                    sum(opp.match_score for opp in opportunities) / len(opportunities)
                    if opportunities else 0
                ),
                "priority_breakdown": self._count_by_priority(opportunities)
            },
            "opportunities": [
                opp.model_dump() for opp in opportunities
            ]
        }

        return json.dumps(report_data, indent=2)

    def _generate_summary(self, opportunities: list[Opportunity]) -> str:
        """
        Generate a brief summary report.

        Args:
            opportunities: List of opportunities to report on

        Returns:
            Summary text string
        """
        if not opportunities:
            return "No opportunities found."

        total_revenue = sum(
            opp.estimated_revenue
            for opp in opportunities
        )
        avg_match_score = sum(
            opp.match_score
            for opp in opportunities
        ) / len(opportunities)

        priority_counts = self._count_by_priority(opportunities)

        lines = [
            "OPPORTUNITY SUMMARY",
            "=" * 50,
            f"Total Opportunities: {len(opportunities)}",
            f"Total Estimated Revenue: ${total_revenue:,.2f}",
            f"Average Match Score: {avg_match_score:.1f}%",
            "",
            "Priority Breakdown:",
            f"  High Priority: {priority_counts.get('high', 0)}",
            f"  Medium Priority: {priority_counts.get('medium', 0)}",
            f"  Low Priority: {priority_counts.get('low', 0)}",
            "",
            "Top 5 Opportunities (by match score):",
            ""
        ]

        # Show top 5 opportunities
        sorted_opps = sorted(
            opportunities,
            key=lambda x: x.match_score,
            reverse=True
        )[:5]

        for i, opp in enumerate(sorted_opps, 1):
            lines.append(
                f"{i}. {opp.scenario_name} - {opp.client_name} "
                f"({opp.match_score:.1f}%, ${opp.estimated_revenue:,.2f})"
            )

        return "\n".join(lines)

    def _count_by_priority(
        self,
        opportunities: list[Opportunity]
    ) -> dict[str, int]:
        """
        Count opportunities by priority level.

        Args:
            opportunities: List of opportunities to count

        Returns:
            Dictionary mapping priority levels to counts
        """
        counts = {"high": 0, "medium": 0, "low": 0}

        for opp in opportunities:
            priority_key = opp.priority.lower()
            if priority_key in counts:
                counts[priority_key] += 1

        return counts
