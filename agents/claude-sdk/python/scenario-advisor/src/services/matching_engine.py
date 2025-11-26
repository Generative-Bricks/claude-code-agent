"""
Matching engine for evaluating client-scenario compatibility.

This module provides the core matching logic that evaluates whether a client
meets the criteria defined in a scenario and calculates a weighted match score.
"""

import logging
from typing import Any

from ..models import ClientProfile, Scenario, MatchDetail

logger = logging.getLogger(__name__)


class MatchingEngine:
    """
    Engine for matching clients to scenarios based on defined criteria.

    The matching engine evaluates each criterion in a scenario against client data,
    applying appropriate operators (gt, lt, eq, contains, etc.) and calculating
    a weighted match score based on criterion weights.
    """

    def match_client_to_scenario(
        self,
        client: ClientProfile,
        scenario: Scenario
    ) -> tuple[float, list[MatchDetail]]:
        """
        Evaluate if a client matches a scenario and calculate the match score.

        Args:
            client: The client to evaluate
            scenario: The scenario with criteria to match against

        Returns:
            Tuple of (match_score, match_details) where:
            - match_score: Weighted score from 0-100 indicating match quality
            - match_details: List of MatchDetail objects for each criterion

        Example:
            >>> engine = MatchingEngine()
            >>> score, details = engine.match_client_to_scenario(client, scenario)
            >>> if score >= 80:
            >>>     print(f"Strong match: {score}%")
        """
        logger.info(
            f"Matching client {client.client_id} to scenario {scenario.scenario_id}"
        )

        match_details: list[MatchDetail] = []
        total_weight = 0.0
        weighted_score = 0.0

        for criterion in scenario.criteria:
            met, actual_value = self._evaluate_criterion(criterion, client)

            points = criterion.weight if met else 0.0
            detail = MatchDetail(
                criterion_field=criterion.field,
                operator=criterion.operator,
                expected_value=criterion.value,
                actual_value=actual_value,
                matched=met,
                weight=criterion.weight,
                points_earned=points
            )
            match_details.append(detail)

            total_weight += criterion.weight
            if met:
                weighted_score += criterion.weight

        # Calculate final score as percentage (0-100)
        final_score = (weighted_score / total_weight * 100) if total_weight > 0 else 0.0

        logger.info(
            f"Match result: {final_score:.1f}% "
            f"({sum(1 for d in match_details if d.met)}/{len(match_details)} criteria met)"
        )

        return final_score, match_details

    def _evaluate_criterion(
        self,
        criterion: Any,
        client: ClientProfile
    ) -> tuple[bool, Any]:
        """
        Evaluate a single criterion against client data.

        Args:
            criterion: The criterion to evaluate (has field, operator, value)
            client: The client data to evaluate against

        Returns:
            Tuple of (criterion_met, actual_value) where:
            - criterion_met: Boolean indicating if criterion was satisfied
            - actual_value: The actual value found in client data

        Supported operators:
            - gt: Greater than
            - lt: Less than
            - gte: Greater than or equal
            - lte: Less than or equal
            - eq: Equal
            - contains: String/list contains
            - in: Value in list
        """
        field_path = criterion.field
        operator = criterion.operator
        expected_value = criterion.value

        # Get the actual value from client data
        actual_value = self._get_nested_value(client, field_path)

        logger.debug(
            f"Evaluating {field_path} {operator} {expected_value}: "
            f"actual={actual_value}"
        )

        # Evaluate based on operator
        met = False

        try:
            if operator == "gt":
                met = actual_value > expected_value
            elif operator == "lt":
                met = actual_value < expected_value
            elif operator == "gte":
                met = actual_value >= expected_value
            elif operator == "lte":
                met = actual_value <= expected_value
            elif operator == "eq":
                met = actual_value == expected_value
            elif operator == "contains":
                if isinstance(actual_value, str):
                    met = expected_value.lower() in actual_value.lower()
                elif isinstance(actual_value, list):
                    met = expected_value in actual_value
                else:
                    met = False
            elif operator == "in_range":
                # Check if value is in a list or range
                if isinstance(expected_value, list):
                    met = actual_value in expected_value
                elif isinstance(expected_value, tuple) and len(expected_value) == 2:
                    # Range tuple (min, max)
                    met = expected_value[0] <= actual_value <= expected_value[1]
                else:
                    met = False
            else:
                logger.warning(f"Unknown operator: {operator}")
                met = False
        except (TypeError, AttributeError) as e:
            logger.warning(
                f"Error evaluating criterion {field_path} {operator} {expected_value}: {e}"
            )
            met = False

        return met, actual_value

    def _get_nested_value(self, obj: Any, field_path: str) -> Any:
        """
        Get a nested value from an object using dot notation.

        Args:
            obj: The object to traverse (typically a Pydantic model)
            field_path: Dot-separated path to the field (e.g., "profile.age")

        Returns:
            The value at the specified path, or None if not found

        Example:
            >>> value = self._get_nested_value(client, "profile.age")
            >>> # Returns client.profile.age
        """
        parts = field_path.split(".")
        current = obj

        for part in parts:
            try:
                if hasattr(current, part):
                    current = getattr(current, part)
                elif isinstance(current, dict):
                    current = current.get(part)
                else:
                    logger.warning(f"Field not found: {field_path} (at {part})")
                    return None
            except (AttributeError, KeyError) as e:
                logger.warning(f"Error accessing field {field_path}: {e}")
                return None

        return current
