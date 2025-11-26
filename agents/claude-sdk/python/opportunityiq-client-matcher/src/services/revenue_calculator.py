"""
Revenue calculation service for OpportunityIQ Client Matcher.

Business logic for estimating potential revenue from matched opportunities.

EXCELLENCE Principle: Accurate revenue calculations with transparent methodology.
"""

import logging
from typing import Optional

from ..models import (
    ClientProfile,
    Scenario,
    RevenueCalculation
)

logger = logging.getLogger(__name__)


class RevenueCalculator:
    """
    Calculates estimated revenue for matched opportunities.

    Supports multiple revenue formula types: percentage, flat_fee, tiered, aum_based.
    """

    def calculate_revenue(
        self,
        client: ClientProfile,
        scenario: Scenario
    ) -> RevenueCalculation:
        """
        Calculate estimated revenue for a client-scenario match.

        Args:
            client: Client profile
            scenario: Matched scenario

        Returns:
            RevenueCalculation with detailed breakdown

        Raises:
            ValueError: If formula type is unsupported or required data is missing
        """
        formula = scenario.revenue_formula
        formula_type = formula.formula_type

        # Route to appropriate calculation method
        if formula_type == "percentage":
            calculated = self._calculate_percentage(client, formula)
        elif formula_type == "flat_fee":
            calculated = self._calculate_flat_fee(client, formula)
        elif formula_type == "tiered":
            calculated = self._calculate_tiered(client, formula)
        elif formula_type == "aum_based":
            calculated = self._calculate_aum_based(client, formula)
        else:
            raise ValueError(f"Unsupported formula type: {formula_type}")

        # Apply min/max constraints
        final_amount = calculated
        min_applied = False
        max_applied = False

        if formula.min_revenue is not None and calculated < formula.min_revenue:
            final_amount = formula.min_revenue
            min_applied = True
            logger.debug(
                f"Applied minimum revenue: ${calculated:.2f} -> ${final_amount:.2f}"
            )

        if formula.max_revenue is not None and calculated > formula.max_revenue:
            final_amount = formula.max_revenue
            max_applied = True
            logger.debug(
                f"Applied maximum revenue cap: ${calculated:.2f} -> ${final_amount:.2f}"
            )

        # Get multiplier value if used
        multiplier_value = None
        if formula.multiplier_field:
            multiplier_value = self._get_multiplier_value(client, formula)

        logger.info(
            f"Revenue calculated for client {client.client_id}: "
            f"${final_amount:.2f} (formula: {formula_type})"
        )

        return RevenueCalculation(
            formula_type=formula_type,
            base_rate=formula.base_rate,
            multiplier_value=multiplier_value,
            calculated_amount=calculated,
            final_amount=final_amount,
            min_applied=min_applied,
            max_applied=max_applied
        )

    def _calculate_percentage(
        self,
        client: ClientProfile,
        formula: "RevenueFormula"
    ) -> float:
        """
        Calculate revenue as percentage of a client field.

        Example: 1% of portfolio value = 0.01 * portfolio_value

        Args:
            client: Client profile
            formula: Revenue formula

        Returns:
            Calculated revenue amount
        """
        if not formula.multiplier_field:
            raise ValueError("Percentage formula requires multiplier_field")

        multiplier = self._get_multiplier_value(client, formula)
        return formula.base_rate * multiplier

    def _calculate_flat_fee(
        self,
        client: ClientProfile,
        formula: "RevenueFormula"
    ) -> float:
        """
        Calculate revenue as flat fee.

        Args:
            client: Client profile (unused, but kept for interface consistency)
            formula: Revenue formula

        Returns:
            Flat fee amount (base_rate)
        """
        return formula.base_rate

    def _calculate_tiered(
        self,
        client: ClientProfile,
        formula: "RevenueFormula"
    ) -> float:
        """
        Calculate revenue using tiered rates.

        Example tiers: {'0-100000': 0.01, '100000-500000': 0.008, '500000+': 0.005}

        Args:
            client: Client profile
            formula: Revenue formula

        Returns:
            Calculated revenue based on tiers
        """
        if not formula.tiers:
            raise ValueError("Tiered formula requires tiers dictionary")

        if not formula.multiplier_field:
            raise ValueError("Tiered formula requires multiplier_field")

        value = self._get_multiplier_value(client, formula)
        total_revenue = 0.0

        # Sort tiers by lower bound
        sorted_tiers = self._parse_and_sort_tiers(formula.tiers)

        for (lower, upper), rate in sorted_tiers:
            if value <= lower:
                # Haven't reached this tier yet
                continue

            if upper is None:
                # Unlimited upper tier (e.g., "500000+")
                tier_amount = value - lower
                total_revenue += tier_amount * rate
                break
            else:
                # Calculate amount in this tier
                tier_upper = min(value, upper)
                tier_amount = tier_upper - lower
                total_revenue += tier_amount * rate

                if value <= upper:
                    # Value falls within this tier
                    break

        return total_revenue

    def _calculate_aum_based(
        self,
        client: ClientProfile,
        formula: "RevenueFormula"
    ) -> float:
        """
        Calculate revenue based on Assets Under Management (AUM).

        Convenience method that uses portfolio value by default.

        Args:
            client: Client profile
            formula: Revenue formula

        Returns:
            Calculated revenue
        """
        # Default to portfolio value if no multiplier field specified
        if not formula.multiplier_field:
            multiplier = client.portfolio.total_value
        else:
            multiplier = self._get_multiplier_value(client, formula)

        return formula.base_rate * multiplier

    def _get_multiplier_value(
        self,
        client: ClientProfile,
        formula: "RevenueFormula"
    ) -> float:
        """
        Extract multiplier value from client profile.

        Args:
            client: Client profile
            formula: Revenue formula with multiplier_field

        Returns:
            Numeric value to use as multiplier

        Raises:
            ValueError: If field doesn't exist or is not numeric
        """
        if not formula.multiplier_field:
            raise ValueError("No multiplier field specified")

        # Navigate nested fields using dot notation
        parts = formula.multiplier_field.split(".")
        value = client

        for part in parts:
            if hasattr(value, part):
                value = getattr(value, part)
            else:
                raise ValueError(
                    f"Field '{formula.multiplier_field}' not found in client profile"
                )

        # Ensure value is numeric
        if not isinstance(value, (int, float)):
            raise ValueError(
                f"Multiplier field '{formula.multiplier_field}' must be numeric, "
                f"got {type(value).__name__}"
            )

        return float(value)

    def _parse_and_sort_tiers(
        self,
        tiers: dict[str, float]
    ) -> list[tuple[tuple[float, Optional[float]], float]]:
        """
        Parse and sort tier ranges.

        Converts string ranges like "0-100000" or "500000+" into numeric tuples.

        Args:
            tiers: Dictionary of tier ranges to rates

        Returns:
            Sorted list of ((lower, upper), rate) tuples
        """
        parsed_tiers = []

        for range_str, rate in tiers.items():
            if "+" in range_str:
                # Unlimited upper bound (e.g., "500000+")
                lower = float(range_str.replace("+", ""))
                upper = None
            elif "-" in range_str:
                # Bounded range (e.g., "0-100000")
                lower_str, upper_str = range_str.split("-")
                lower = float(lower_str)
                upper = float(upper_str)
            else:
                raise ValueError(f"Invalid tier range format: {range_str}")

            parsed_tiers.append(((lower, upper), rate))

        # Sort by lower bound
        parsed_tiers.sort(key=lambda x: x[0][0])

        return parsed_tiers
