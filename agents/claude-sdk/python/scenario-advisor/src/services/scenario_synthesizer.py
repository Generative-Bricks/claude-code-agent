"""Scenario synthesizer for merging and enriching research findings.

This module combines findings from multiple research agents, deduplicates similar
scenarios, cross-references for confidence boosting, and calculates actionability scores.
"""

import logging
import uuid
from datetime import datetime
from typing import Optional, Any
from collections import defaultdict

from ..models import (
    EnrichedScenario,
    ConfidenceScore,
    TemporalContext,
    ActionabilityMetrics,
    SourceProvenance,
    ScenarioCategory,
    MatchCriterion,
    RevenueFormula
)

logger = logging.getLogger(__name__)


class ScenarioSynthesizer:
    """Merge, validate, and enrich scenarios from multiple researchers.

    This synthesizer processes raw research findings, deduplicates similar scenarios,
    applies cross-reference confidence boosts, calculates actionability scores,
    and returns validated, enriched scenarios.

    The synthesis process:
    1. Deduplicate similar scenarios across sources
    2. Cross-reference for confidence boosting
    3. Calculate actionability scores (specificity, urgency, impact, feasibility)
    4. Validate against Pydantic models
    5. Sort by actionability
    """

    def __init__(self):
        """Initialize the scenario synthesizer."""
        logger.info("Initializing scenario synthesizer")

    def synthesize(
        self,
        research_results: dict[str, list[dict]],
        min_confidence: float = 0.6
    ) -> list[EnrichedScenario]:
        """Synthesize research results into enriched scenarios.

        Args:
            research_results: Dictionary mapping research type to findings
            min_confidence: Minimum confidence score (0.0-1.0) for inclusion

        Returns:
            List of enriched scenarios sorted by actionability (highest first)

        Example:
            >>> synthesizer = ScenarioSynthesizer()
            >>> results = {
            ...     "annuity_events": [...],
            ...     "life_events": [...],
            ...     "revenue_opportunities": [...]
            ... }
            >>> scenarios = synthesizer.synthesize(results, min_confidence=0.7)
        """
        logger.info(
            f"Starting synthesis with {sum(len(v) for v in research_results.values())} "
            f"raw findings, min confidence: {min_confidence}"
        )

        # Convert raw findings to EnrichedScenarios
        enriched_scenarios = []
        category_map = {
            "annuity_events": "annuity",
            "life_events": "life_event",
            "revenue_opportunities": "revenue_opportunity"
        }

        for research_type, findings in research_results.items():
            category = category_map.get(research_type, "other")
            logger.debug(f"Processing {len(findings)} findings from {research_type}")

            for finding in findings:
                try:
                    scenario = self._create_enriched_scenario(finding, category)
                    enriched_scenarios.append(scenario)
                except Exception as e:
                    logger.warning(
                        f"Failed to create enriched scenario from finding: {e}",
                        exc_info=True
                    )

        logger.info(f"Created {len(enriched_scenarios)} enriched scenarios")

        # Deduplicate similar scenarios
        enriched_scenarios = self._deduplicate_scenarios(enriched_scenarios)
        logger.info(f"After deduplication: {len(enriched_scenarios)} scenarios")

        # Apply cross-reference confidence boost
        enriched_scenarios = self._apply_cross_reference_boost(enriched_scenarios)

        # Filter by minimum confidence
        enriched_scenarios = [
            s for s in enriched_scenarios
            if s.confidence.overall_confidence >= min_confidence
        ]
        logger.info(
            f"After confidence filter (>={min_confidence}): {len(enriched_scenarios)} scenarios"
        )

        # Sort by actionability composite score (descending)
        enriched_scenarios.sort(
            key=lambda s: s.actionability.composite_score,
            reverse=True
        )
        logger.info("Scenarios sorted by actionability")

        return enriched_scenarios

    def _create_enriched_scenario(
        self,
        finding: dict,
        category: str
    ) -> EnrichedScenario:
        """Convert raw finding dictionary to EnrichedScenario.

        Args:
            finding: Raw finding from research agent
            category: Scenario category (annuity, life_event, revenue_opportunity)

        Returns:
            Validated EnrichedScenario instance
        """
        # Map research category to valid ScenarioCategory
        category_map = {
            "annuity": "annuity",
            "life_event": "planning",
            "revenue_opportunity": "investment"
        }
        valid_category = category_map.get(category, "other")

        # Generate scenario ID
        scenario_id = f"SCN-{uuid.uuid4().hex[:8].upper()}"

        # Extract name/title
        name = finding.get("title", finding.get("name", "Untitled Scenario"))
        description = finding.get("description", "No description provided")

        # Parse criteria from finding
        criteria = self._parse_criteria(finding.get("criteria", {}))

        # Create default revenue formula
        revenue_formula = RevenueFormula(
            formula_type="percentage",
            base_rate=0.01,
            multiplier_field="portfolio.total_value"
        )

        # Map urgency from finding to temporal context urgency
        raw_urgency = finding.get("temporal_context", {}).get("urgency", "medium")
        urgency_map = {
            "high": "short_term",
            "medium": "medium_term",
            "low": "long_term",
            "critical": "immediate",
            "immediate": "immediate",
            "short_term": "short_term",
            "medium_term": "medium_term",
            "long_term": "long_term"
        }
        urgency = urgency_map.get(raw_urgency.lower(), "medium_term")

        # Create temporal context
        temporal = TemporalContext(
            urgency=urgency,
            timing_rationale=f"Scenario urgency based on research findings: {raw_urgency}"
        )

        # Get confidence level from finding
        raw_confidence = finding.get("confidence", "MEDIUM")
        confidence_map = {"HIGH": 0.85, "MEDIUM": 0.7, "LOW": 0.5}
        confidence_value = confidence_map.get(raw_confidence.upper(), 0.7) if isinstance(raw_confidence, str) else float(raw_confidence)

        # Create confidence score (fields ordered for validator compatibility)
        confidence = ConfidenceScore(
            source_reliability=confidence_value,
            cross_reference_count=0,
            confidence_rationale=f"Confidence based on research agent assessment: {raw_confidence}",
            overall_confidence=confidence_value
        )

        # Get talking points from finding
        actionability_data = finding.get("actionability", {})
        talking_points = actionability_data.get("talking_points", [])
        if not talking_points:
            talking_points = ["Schedule a review meeting to discuss this opportunity"]

        # Map priority to urgency score
        priority = actionability_data.get("priority", "MEDIUM")
        priority_score_map = {"CRITICAL": 95, "HIGH": 80, "MEDIUM": 60, "LOW": 40}
        urgency_score = priority_score_map.get(priority.upper() if isinstance(priority, str) else "MEDIUM", 60)

        # Create actionability metrics
        actionability = ActionabilityMetrics(
            specificity_score=70,
            urgency_score=urgency_score,
            impact_score=75,
            feasibility_score=80,
            recommended_action=f"Review client portfolio for {name.lower()} opportunity",
            advisor_talking_points=talking_points
        )

        # Get metadata for source info
        metadata = finding.get("metadata", {})
        source_agent = metadata.get("source", "research_agent")

        # Create source provenance
        source = SourceProvenance(
            source_type="expert_analysis",
            source_name=source_agent,
            reliability_score=confidence_value,
            retrieved_at=datetime.now()
        )

        # Create enriched scenario
        enriched = EnrichedScenario(
            scenario_id=scenario_id,
            name=name,
            category=valid_category,
            description=description,
            criteria=criteria,
            revenue_formula=revenue_formula,
            temporal_context=temporal,
            confidence=confidence,
            actionability=actionability,
            discovered_at=datetime.now(),
            discovered_by=source_agent,
            sources=[source]
        )

        logger.debug(f"Created enriched scenario: {name}")
        return enriched

    def _parse_criteria(self, criteria_dict: dict[str, Any]) -> list[MatchCriterion]:
        """Parse criteria dictionary into list of MatchCriterion objects.

        Args:
            criteria_dict: Dictionary of field conditions

        Returns:
            List of MatchCriterion objects
        """
        criteria = []
        for field, condition in criteria_dict.items():
            if isinstance(condition, dict):
                operator = condition.get("operator", "eq")
                value = condition.get("value", "")
                # Map operators to valid ones (eq, gt, gte, lt, lte, contains, in_range)
                op_map = {
                    "equals": "eq",
                    "equal": "eq",
                    "greater_than": "gt",
                    "less_than": "lt",
                    "greater_than_or_equal": "gte",
                    "less_than_or_equal": "lte",
                    "within_days": "lte",
                    "contains": "contains",
                    "in": "in_range",
                    "between": "in_range"
                }
                operator = op_map.get(operator, "eq")  # Default to eq if unknown

                criteria.append(MatchCriterion(
                    field=field,
                    operator=operator,
                    value=value,
                    weight=1.0
                ))

        # Ensure at least one criterion
        if not criteria:
            criteria.append(MatchCriterion(
                field="age",
                operator="gte",
                value=18,
                weight=1.0
            ))

        return criteria

    def _calculate_actionability(self, finding: dict) -> ActionabilityMetrics:
        """Calculate actionability metrics for a scenario.

        Scores are calculated based on:
        - Specificity: How specific is the opportunity/event?
        - Urgency: How time-sensitive is it?
        - Impact: What's the potential revenue/client impact?
        - Feasibility: How easy is it to act on?

        Args:
            finding: Raw finding dictionary

        Returns:
            ActionabilityMetrics with calculated scores
        """
        # Specificity: Based on detail level and clarity
        specificity = min(1.0, (
            len(finding.get("description", "")) / 200 * 0.5 +
            len(finding.get("tags", [])) / 5 * 0.3 +
            (1.0 if finding.get("target_clients") else 0.0) * 0.2
        ))

        # Urgency: Based on temporal factors
        urgency_map = {"high": 0.9, "medium": 0.6, "low": 0.3}
        urgency = urgency_map.get(finding.get("urgency", "medium"), 0.6)

        # Impact: Based on potential value
        impact = finding.get("impact_score", 0.7)
        if finding.get("estimated_revenue"):
            impact = min(1.0, impact * 1.2)

        # Feasibility: Based on required effort and resources
        feasibility = finding.get("feasibility_score", 0.7)

        # Overall score: Weighted average
        overall = (
            specificity * 0.25 +
            urgency * 0.25 +
            impact * 0.30 +
            feasibility * 0.20
        )

        return ActionabilityMetrics(
            specificity_score=round(specificity, 2),
            urgency_score=round(urgency, 2),
            impact_score=round(impact, 2),
            feasibility_score=round(feasibility, 2),
            overall_score=round(overall, 2)
        )

    def _deduplicate_scenarios(
        self,
        scenarios: list[EnrichedScenario]
    ) -> list[EnrichedScenario]:
        """Remove duplicate or highly similar scenarios.

        Uses title similarity and category matching to identify duplicates.
        Keeps the scenario with the highest confidence score.

        Args:
            scenarios: List of enriched scenarios

        Returns:
            Deduplicated list of scenarios
        """
        if not scenarios:
            return []

        # Group by category and similar titles
        seen = {}
        deduplicated = []

        for scenario in scenarios:
            # Create a key based on category and normalized name
            key = (
                scenario.category,
                scenario.name.lower().strip()[:50]  # First 50 chars
            )

            if key not in seen:
                seen[key] = scenario
                deduplicated.append(scenario)
            else:
                # Keep the one with higher confidence
                existing = seen[key]
                if scenario.confidence.overall_confidence > existing.confidence.overall_confidence:
                    deduplicated.remove(existing)
                    deduplicated.append(scenario)
                    seen[key] = scenario
                    logger.debug(
                        f"Replaced duplicate scenario '{existing.name}' with higher "
                        f"confidence version"
                    )

        removed_count = len(scenarios) - len(deduplicated)
        if removed_count > 0:
            logger.info(f"Removed {removed_count} duplicate scenarios")

        return deduplicated

    def _apply_cross_reference_boost(
        self,
        scenarios: list[EnrichedScenario]
    ) -> list[EnrichedScenario]:
        """Boost confidence for scenarios found by multiple researchers.

        When similar scenarios are found by different research agents,
        increase their confidence score and cross-reference count.

        Args:
            scenarios: List of enriched scenarios

        Returns:
            Scenarios with updated confidence scores
        """
        # Group scenarios by similar characteristics
        groups = defaultdict(list)

        for scenario in scenarios:
            # Create grouping key based on name similarity and category
            key = (
                scenario.category,
                scenario.name.lower().strip()[:30]
            )
            groups[key].append(scenario)

        # Apply boost to multi-source scenarios
        boosted_scenarios = []
        for group_scenarios in groups.values():
            if len(group_scenarios) > 1:
                # Multiple sources found this scenario - get unique source names
                unique_sources = set()
                for s in group_scenarios:
                    for source in s.sources:
                        unique_sources.add(source.source_name)
                cross_ref_count = len(unique_sources)

                # Boost confidence (up to 0.2 increase for 3+ sources)
                boost = min(0.2, (cross_ref_count - 1) * 0.1)

                logger.debug(
                    f"Applying {boost:.2f} confidence boost to scenario with "
                    f"{cross_ref_count} cross-references"
                )

                # Update the highest-confidence scenario
                best_scenario = max(
                    group_scenarios,
                    key=lambda s: s.confidence.overall_confidence
                )

                # Create updated confidence (fields ordered for validator)
                new_confidence = ConfidenceScore(
                    source_reliability=best_scenario.confidence.source_reliability,
                    cross_reference_count=cross_ref_count,
                    confidence_rationale=f"Cross-referenced by {cross_ref_count} sources with confidence boost of {boost:.2f}",
                    overall_confidence=min(1.0, best_scenario.confidence.overall_confidence + boost)
                )

                # Create new scenario with updated confidence
                boosted_scenario = best_scenario.model_copy(
                    update={"confidence": new_confidence}
                )
                boosted_scenarios.append(boosted_scenario)
            else:
                # Single source, no boost
                boosted_scenarios.append(group_scenarios[0])

        logger.info("Applied cross-reference confidence boosts")
        return boosted_scenarios
