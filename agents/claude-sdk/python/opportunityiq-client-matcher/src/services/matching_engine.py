"""
Matching engine service for OpportunityIQ Client Matcher.

Core business logic for evaluating client profiles against scenario criteria.

TRUTH Principle: Every matching decision is traceable and explainable.
"""

import logging
from typing import Any
from datetime import date

from ..models import (
    ClientProfile,
    Scenario,
    MatchCriterion,
    MatchDetail
)

logger = logging.getLogger(__name__)


class MatchingEngine:
    """
    Evaluates client profiles against scenario matching criteria.

    Implements the core matching algorithm with support for various
    comparison operators.
    """

    def __init__(self):
        """Initialize the matching engine."""
        self.supported_operators = {
            "gt": self._operator_gt,
            "lt": self._operator_lt,
            "gte": self._operator_gte,
            "lte": self._operator_lte,
            "eq": self._operator_eq,
            "contains": self._operator_contains,
            "in": self._operator_in,
        }

    def match_client_to_scenario(
        self,
        client: ClientProfile,
        scenario: Scenario
    ) -> tuple[float, list[MatchDetail]]:
        """
        Evaluate a client against a scenario's criteria.

        Args:
            client: Client profile to evaluate
            scenario: Scenario to match against

        Returns:
            Tuple of (match_score_percentage, list of match details)

        Raises:
            ValueError: If scenario has no criteria or invalid operator
        """
        if not scenario.criteria:
            raise ValueError(f"Scenario {scenario.scenario_id} has no criteria")

        match_details = []
        total_weight = 0.0
        earned_points = 0.0

        for criterion in scenario.criteria:
            try:
                detail = self._evaluate_criterion(client, criterion)
                match_details.append(detail)
                total_weight += criterion.weight
                earned_points += detail.points_earned

            except Exception as e:
                logger.error(
                    f"Error evaluating criterion {criterion.field}: {e}",
                    exc_info=True
                )
                # Create failed match detail
                match_details.append(
                    MatchDetail(
                        criterion_field=criterion.field,
                        operator=criterion.operator,
                        expected_value=criterion.value,
                        actual_value=None,
                        matched=False,
                        weight=criterion.weight,
                        points_earned=0.0
                    )
                )
                total_weight += criterion.weight

        # Calculate match score as percentage
        if total_weight > 0:
            match_score = (earned_points / total_weight) * 100
        else:
            match_score = 0.0

        logger.info(
            f"Client {client.client_id} matched to scenario {scenario.scenario_id}: "
            f"{match_score:.1f}% ({earned_points:.2f}/{total_weight:.2f} points)"
        )

        return match_score, match_details

    def _evaluate_criterion(
        self,
        client: ClientProfile,
        criterion: MatchCriterion
    ) -> MatchDetail:
        """
        Evaluate a single criterion against client data.

        Args:
            client: Client profile
            criterion: Criterion to evaluate

        Returns:
            MatchDetail with evaluation results
        """
        # Extract actual value from client profile
        actual_value = self._get_field_value(client, criterion.field)

        # Get operator function
        operator_func = self.supported_operators.get(criterion.operator)
        if not operator_func:
            raise ValueError(f"Unsupported operator: {criterion.operator}")

        # Evaluate criterion
        matched = operator_func(actual_value, criterion.value)

        # Calculate points earned
        points_earned = criterion.weight if matched else 0.0

        return MatchDetail(
            criterion_field=criterion.field,
            operator=criterion.operator,
            expected_value=criterion.value,
            actual_value=actual_value,
            matched=matched,
            weight=criterion.weight,
            points_earned=points_earned
        )

    def _get_field_value(self, client: ClientProfile, field_path: str) -> Any:
        """
        Extract a field value from client profile using dot notation.

        Supports nested fields like 'portfolio.total_value' or 'age'.
        Also supports extra fields stored in Pydantic's __pydantic_extra__.

        Args:
            client: Client profile
            field_path: Field path in dot notation

        Returns:
            Field value

        Raises:
            AttributeError: If field doesn't exist
        """
        parts = field_path.split(".")
        value = client

        for part in parts:
            if hasattr(value, part):
                value = getattr(value, part)
            elif hasattr(value, '__pydantic_extra__') and part in value.__pydantic_extra__:
                # Access extra fields from Pydantic model
                value = value.__pydantic_extra__[part]
            else:
                raise AttributeError(
                    f"Field '{field_path}' not found in client profile"
                )

        return value

    # Operator implementations
    def _operator_gt(self, actual: Any, expected: Any) -> bool:
        """Greater than comparison."""
        if actual is None:
            return False
        return actual > expected

    def _operator_lt(self, actual: Any, expected: Any) -> bool:
        """Less than comparison."""
        if actual is None:
            return False
        return actual < expected

    def _operator_gte(self, actual: Any, expected: Any) -> bool:
        """Greater than or equal comparison."""
        if actual is None:
            return False
        return actual >= expected

    def _operator_lte(self, actual: Any, expected: Any) -> bool:
        """Less than or equal comparison."""
        if actual is None:
            return False
        return actual <= expected

    def _operator_eq(self, actual: Any, expected: Any) -> bool:
        """Equality comparison."""
        if actual is None:
            return False
        return actual == expected

    def _operator_contains(self, actual: Any, expected: Any) -> bool:
        """
        Contains comparison.

        Checks if expected value is in actual value (works for strings, lists).
        """
        if actual is None:
            return False
        try:
            return expected in actual
        except TypeError:
            return False

    def _operator_in(self, actual: Any, expected: Any) -> bool:
        """
        In comparison.

        Checks if actual value is in expected list.
        """
        if actual is None:
            return False
        if not isinstance(expected, (list, tuple)):
            return False
        return actual in expected
