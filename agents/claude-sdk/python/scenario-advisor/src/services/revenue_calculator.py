"""
Revenue calculation engine for client opportunities.

This module handles revenue calculations based on different formula types
(percentage, flat fee, tiered, AUM-based) with support for min/max caps.
"""

import logging
from typing import Any

from ..models import Opportunity, RevenueFormula, RevenueCalculation

logger = logging.getLogger(__name__)


class RevenueCalculator:
    """
    Calculator for estimating revenue from client opportunities.

    Supports multiple calculation methods:
    - Percentage-based (e.g., % of premium, % of assets)
    - Flat fee
    - Tiered (different rates for different amount ranges)
    - AUM-based (percentage of assets under management)

    Applies min/max caps to ensure revenue stays within acceptable bounds.
    """

    def calculate(
        self,
        opportunity: Opportunity,
        revenue_formula: RevenueFormula
    ) -> RevenueCalculation:
        """
        Calculate estimated revenue for an opportunity.

        Args:
            opportunity: The client opportunity to calculate revenue for
            revenue_formula: The formula defining how to calculate revenue

        Returns:
            RevenueCalculation with estimated revenue and calculation details

        Example:
            >>> calculator = RevenueCalculator()
            >>> calc = calculator.calculate(opportunity, formula)
            >>> print(f"Estimated revenue: ${calc.estimated_revenue:,.2f}")
        """
        logger.info(
            f"Calculating revenue for {opportunity.scenario_name} "
            f"using {revenue_formula.formula_type} formula"
        )

        # Get base value for calculation
        base_value = self._get_base_value(opportunity, revenue_formula)

        # Calculate based on formula type
        calculated_revenue = 0.0

        if revenue_formula.formula_type == "percentage":
            calculated_revenue = self._calculate_percentage(revenue_formula, base_value)
        elif revenue_formula.formula_type == "flat_fee":
            calculated_revenue = self._calculate_flat_fee(revenue_formula)
        elif revenue_formula.formula_type == "tiered":
            calculated_revenue = self._calculate_tiered(revenue_formula, base_value)
        elif revenue_formula.formula_type == "aum_based":
            calculated_revenue = self._calculate_aum_based(revenue_formula, base_value)
        else:
            logger.warning(f"Unknown formula type: {revenue_formula.formula_type}")
            calculated_revenue = 0.0

        # Apply min/max caps
        final_revenue = calculated_revenue

        if revenue_formula.min_revenue and calculated_revenue < revenue_formula.min_revenue:
            logger.debug(
                f"Applying minimum cap: ${calculated_revenue:,.2f} -> "
                f"${revenue_formula.min_revenue:,.2f}"
            )
            final_revenue = revenue_formula.min_revenue

        if revenue_formula.max_revenue and calculated_revenue > revenue_formula.max_revenue:
            logger.debug(
                f"Applying maximum cap: ${calculated_revenue:,.2f} -> "
                f"${revenue_formula.max_revenue:,.2f}"
            )
            final_revenue = revenue_formula.max_revenue

        calculation = RevenueCalculation(
            estimated_revenue=final_revenue,
            formula_type=revenue_formula.formula_type,
            base_value=base_value,
            calculation_details={
                "raw_calculation": calculated_revenue,
                "capped": final_revenue != calculated_revenue,
                "formula": revenue_formula.model_dump()
            }
        )

        logger.info(f"Final revenue estimate: ${final_revenue:,.2f}")

        return calculation

    def _get_base_value(
        self,
        opportunity: Opportunity,
        revenue_formula: RevenueFormula
    ) -> float:
        """
        Extract the base value for revenue calculation from client data.

        Args:
            opportunity: The client opportunity
            revenue_formula: The revenue formula (may specify base_field)

        Returns:
            The base value to use in calculations
        """
        # For now, return a default value
        # In production, this would extract from client data based on base_field
        # Example: if base_field is "assets.total", get client.assets.total

        base_field = getattr(revenue_formula, "base_field", None)

        if base_field:
            logger.debug(f"Base field specified: {base_field}")
            # In production: return self._get_nested_value(opportunity.client, base_field)
            return 100000.0  # Mock value for now

        return 100000.0  # Default mock value

    def _calculate_percentage(self, formula: RevenueFormula, base_value: float) -> float:
        """
        Calculate revenue as a percentage of base value.

        Args:
            formula: The revenue formula with percentage rate
            base_value: The base value to apply percentage to

        Returns:
            Calculated revenue amount
        """
        rate = formula.parameters.get("rate", 0.0)
        revenue = base_value * (rate / 100)

        logger.debug(
            f"Percentage calculation: ${base_value:,.2f} * {rate}% = ${revenue:,.2f}"
        )

        return revenue

    def _calculate_flat_fee(self, formula: RevenueFormula) -> float:
        """
        Return a flat fee amount.

        Args:
            formula: The revenue formula with fee amount

        Returns:
            The flat fee amount
        """
        fee = formula.parameters.get("amount", 0.0)

        logger.debug(f"Flat fee: ${fee:,.2f}")

        return fee

    def _calculate_tiered(self, formula: RevenueFormula, base_value: float) -> float:
        """
        Calculate revenue using tiered rates based on value ranges.

        Args:
            formula: The revenue formula with tier definitions
            base_value: The value to calculate against

        Returns:
            Calculated revenue amount

        Example tiers:
            [
                {"min": 0, "max": 100000, "rate": 1.0},
                {"min": 100000, "max": 500000, "rate": 0.75},
                {"min": 500000, "max": null, "rate": 0.5}
            ]
        """
        tiers = formula.parameters.get("tiers", [])

        total_revenue = 0.0
        remaining_value = base_value

        for tier in tiers:
            tier_min = tier.get("min", 0)
            tier_max = tier.get("max")
            tier_rate = tier.get("rate", 0.0)

            if remaining_value <= 0:
                break

            # Calculate the amount in this tier
            if tier_max is None:
                tier_amount = remaining_value
            else:
                tier_amount = min(remaining_value, tier_max - tier_min)

            tier_revenue = tier_amount * (tier_rate / 100)
            total_revenue += tier_revenue
            remaining_value -= tier_amount

            logger.debug(
                f"Tier ${tier_min:,.0f}-${tier_max or 'infinity'}: "
                f"${tier_amount:,.2f} * {tier_rate}% = ${tier_revenue:,.2f}"
            )

        logger.debug(f"Total tiered revenue: ${total_revenue:,.2f}")

        return total_revenue

    def _calculate_aum_based(self, formula: RevenueFormula, aum_value: float) -> float:
        """
        Calculate revenue as a percentage of AUM (Assets Under Management).

        Args:
            formula: The revenue formula with AUM percentage
            aum_value: The total assets under management

        Returns:
            Calculated annual revenue
        """
        aum_rate = formula.parameters.get("aum_rate", 0.0)
        revenue = aum_value * (aum_rate / 100)

        logger.debug(
            f"AUM-based calculation: ${aum_value:,.2f} * {aum_rate}% = ${revenue:,.2f}"
        )

        return revenue
