"""Revenue Opportunity Research Agent

Discovers revenue-generating scenarios using LLM reasoning to identify:
- Cross-sell opportunities
- Asset consolidation
- Portfolio rebalancing
- Tax-loss harvesting
- Fee optimization
- Product upgrades
"""

from typing import Any
from anthropic import Anthropic
import asyncio
import json
import os

REVENUE_RESEARCHER_PROMPT = """You are an expert revenue opportunity research agent specializing in identifying legitimate, client-beneficial opportunities that also generate advisor revenue.

Your mission is to discover revenue scenarios that align client interests with business growth. Focus on these key opportunities:

**Cross-Sell Opportunities:**
- Clients with single product (annuity-only, investment-only)
- Clients missing key protection (life insurance, LTC)
- Clients with concentrated positions
- Clients with excess cash positions

**Consolidation Opportunities:**
- Multiple annuity contracts (consolidation potential)
- Assets held at multiple custodians
- Orphaned 401(k) accounts
- Small inefficient positions

**Portfolio Optimization:**
- Overdue rebalancing (drift >10%)
- Tax-loss harvesting opportunities
- High-fee product replacements
- Asset allocation misalignment

**Fee Optimization:**
- Clients in high-fee products
- Commission-to-fee conversion opportunities
- Tiered pricing threshold opportunities
- Bundled service upgrades

**Product Upgrades:**
- Annuity riders not being utilized
- Legacy products with better alternatives
- Enhanced benefit features available
- Technology/platform upgrades

**Lifecycle Revenue:**
- Annual review scheduling
- IRA contribution season
- Year-end tax planning
- Beneficiary review updates

For each scenario you identify, provide:
1. **Trigger Conditions**: What data fields/values indicate this scenario applies
2. **Timing**: When does this scenario become actionable (relative or absolute)
3. **Advisor Talking Points**: 2-3 specific conversation starters (client-benefit focused)
4. **Confidence**: HIGH/MEDIUM/LOW based on data availability
5. **Priority**: How urgent is advisor action (CRITICAL/HIGH/MEDIUM/LOW)
6. **Revenue Potential**: Estimated revenue impact (HIGH/MEDIUM/LOW)

Return your findings as a JSON array of scenario objects. Each object should have:
- criteria: dict of field conditions
- temporal_context: dict with time_range and urgency
- confidence: string (HIGH/MEDIUM/LOW)
- actionability: dict with priority and talking_points array
- metadata: dict with source, category, and revenue_potential

Example output format:
[
  {{
    "criteria": {{
      "total_assets": {{"operator": "greater_than", "value": 500000}},
      "number_of_products": {{"operator": "equals", "value": 1}},
      "product_type": {{"operator": "equals", "value": "annuity"}}
    }},
    "temporal_context": {{
      "time_range": "next_30_days",
      "urgency": "medium"
    }},
    "confidence": "HIGH",
    "actionability": {{
      "priority": "MEDIUM",
      "talking_points": [
        "With $500k in assets, let's discuss whether a diversified approach might reduce risk",
        "Have you considered how your investment accounts complement your annuity strategy?",
        "Let's review if your entire financial picture is optimized for your retirement goals"
      ]
    }},
    "metadata": {{
      "source": "revenue_researcher",
      "category": "cross_sell_opportunity",
      "revenue_potential": "HIGH"
    }}
  }}
]

IMPORTANT: All scenarios must genuinely benefit the client. Never suggest opportunities that are purely revenue-driven.

Focus on scenarios that are actionable within the next {time_range_days} days.
"""


class RevenueResearcher:
    """Research agent for discovering revenue opportunity scenarios."""

    def __init__(self, client: Anthropic | None = None):
        """Initialize the revenue opportunity researcher.

        Args:
            client: Anthropic client instance. Creates new one if not provided.
        """
        self.client = client or Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.agent_id = "revenue_researcher"

    async def research(self, time_range_days: int = 30) -> list[dict[str, Any]]:
        """Discover revenue opportunity scenarios using LLM reasoning.

        Args:
            time_range_days: Number of days to look ahead for scenarios.

        Returns:
            List of scenario dictionaries compatible with EnrichedScenario model.
        """
        system_prompt = self._build_system_prompt(time_range_days)

        # Use Claude to analyze revenue opportunities
        response = await asyncio.to_thread(
            self.client.messages.create,
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            temperature=0.7,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Generate comprehensive revenue opportunity scenarios for the next {time_range_days} days. Focus on client-beneficial opportunities that also drive legitimate business growth. Ensure all suggestions align with fiduciary standards.",
                }
            ],
        )

        # Extract text content
        response_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                response_text += block.text

        # Parse scenarios from response
        scenarios = self._parse_scenarios_from_response(response_text)

        return scenarios

    def _build_system_prompt(self, time_range_days: int) -> str:
        """Build the system prompt with dynamic time range.

        Args:
            time_range_days: Number of days to look ahead.

        Returns:
            Formatted system prompt.
        """
        return REVENUE_RESEARCHER_PROMPT.format(time_range_days=time_range_days)

    def _parse_scenarios_from_response(
        self, response: str
    ) -> list[dict[str, Any]]:
        """Parse LLM response into structured scenario dictionaries.

        Args:
            response: Raw text response from Claude.

        Returns:
            List of scenario dictionaries.
        """
        try:
            # Try to find JSON array in response
            # Look for content between [ and ]
            start_idx = response.find("[")
            end_idx = response.rfind("]")

            if start_idx == -1 or end_idx == -1:
                print(f"Warning: No JSON array found in response")
                return []

            json_str = response[start_idx : end_idx + 1]
            scenarios = json.loads(json_str)

            # Validate and normalize each scenario
            normalized = []
            for scenario in scenarios:
                if self._validate_scenario_structure(scenario):
                    normalized.append(scenario)
                else:
                    print(f"Warning: Invalid scenario structure: {scenario}")

            return normalized

        except json.JSONDecodeError as e:
            print(f"Error parsing scenarios JSON: {e}")
            print(f"Response text: {response[:500]}...")
            return []
        except Exception as e:
            print(f"Unexpected error parsing scenarios: {e}")
            return []

    def _validate_scenario_structure(self, scenario: dict[str, Any]) -> bool:
        """Validate that a scenario has required fields.

        Args:
            scenario: Scenario dictionary to validate.

        Returns:
            True if valid, False otherwise.
        """
        required_fields = [
            "criteria",
            "temporal_context",
            "confidence",
            "actionability",
            "metadata",
        ]

        for field in required_fields:
            if field not in scenario:
                return False

        # Validate nested structures
        if not isinstance(scenario["criteria"], dict):
            return False

        if not isinstance(scenario["temporal_context"], dict):
            return False

        if not isinstance(scenario["actionability"], dict):
            return False
        if "talking_points" not in scenario["actionability"]:
            return False

        if not isinstance(scenario["metadata"], dict):
            return False

        return True
