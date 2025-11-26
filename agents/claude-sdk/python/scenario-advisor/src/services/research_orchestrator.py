"""Research orchestrator for coordinating parallel research across specialist agents.

This module manages the parallel execution of annuity, life event, and revenue
research agents, collecting and organizing their findings.
"""

import asyncio
import logging
from typing import Optional

from ..agents.annuity_researcher import AnnuityResearcher
from ..agents.life_event_researcher import LifeEventResearcher
from ..agents.revenue_researcher import RevenueResearcher

logger = logging.getLogger(__name__)


class ResearchOrchestrator:
    """Coordinates parallel research across specialist agents.

    This orchestrator manages the execution of multiple research agents in parallel,
    collecting their findings and organizing them by category.

    Attributes:
        annuity_researcher: Agent for researching annuity-related events
        life_event_researcher: Agent for researching life events
        revenue_researcher: Agent for researching revenue opportunities
    """

    def __init__(self, anthropic_client=None):
        """Initialize the research orchestrator with specialist agents.

        Args:
            anthropic_client: Optional Anthropic client for agent initialization
        """
        logger.info("Initializing research orchestrator")
        self.annuity_researcher = AnnuityResearcher(anthropic_client)
        self.life_event_researcher = LifeEventResearcher(anthropic_client)
        self.revenue_researcher = RevenueResearcher(anthropic_client)
        logger.debug("All specialist agents initialized")

    async def run_parallel_research(
        self,
        research_focus: Optional[list[str]] = None,
        time_range_days: int = 30
    ) -> dict[str, list[dict]]:
        """Run all researchers in parallel using asyncio.gather.

        Executes specified research agents concurrently and collects their findings.
        If a researcher fails, an empty list is returned for that category.

        Args:
            research_focus: List of research types to run. Options: "annuity",
                "life_event", "revenue". If None, runs all researchers.
            time_range_days: Number of days to look back for research

        Returns:
            Dictionary mapping research type to list of findings:
            {
                "annuity_events": [...],
                "life_events": [...],
                "revenue_opportunities": [...]
            }

        Example:
            >>> orchestrator = ResearchOrchestrator()
            >>> results = await orchestrator.run_parallel_research(
            ...     research_focus=["annuity", "life_event"],
            ...     time_range_days=60
            ... )
        """
        logger.info(
            f"Starting parallel research with focus: {research_focus or 'all'}, "
            f"time range: {time_range_days} days"
        )

        tasks = []

        # Build task list based on research focus
        if not research_focus or "annuity" in research_focus:
            logger.debug("Adding annuity research task")
            tasks.append((
                "annuity_events",
                self.annuity_researcher.research(time_range_days)
            ))

        if not research_focus or "life_event" in research_focus:
            logger.debug("Adding life event research task")
            tasks.append((
                "life_events",
                self.life_event_researcher.research(time_range_days)
            ))

        if not research_focus or "revenue" in research_focus:
            logger.debug("Adding revenue research task")
            tasks.append((
                "revenue_opportunities",
                self.revenue_researcher.research(time_range_days)
            ))

        # Execute all research tasks in parallel
        logger.info(f"Executing {len(tasks)} research tasks in parallel")
        results = await asyncio.gather(
            *[task[1] for task in tasks],
            return_exceptions=True
        )

        # Process results and handle errors
        research_results = {}
        for (name, _), result in zip(tasks, results):
            if isinstance(result, Exception):
                logger.error(
                    f"Research task '{name}' failed with error: {result}",
                    exc_info=result
                )
                research_results[name] = []
            else:
                logger.info(f"Research task '{name}' completed with {len(result)} findings")
                research_results[name] = result

        total_findings = sum(len(findings) for findings in research_results.values())
        logger.info(f"Parallel research completed with {total_findings} total findings")

        return research_results
