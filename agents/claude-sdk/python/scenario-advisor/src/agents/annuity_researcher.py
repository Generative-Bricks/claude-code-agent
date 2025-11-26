"""Annuity Research Agent

Discovers annuity-related scenarios using LLM reasoning to identify:
- Surrender period endings
- Rate resets
- MYGA maturities
- RMD triggers
- Bonus recapture periods
"""

from typing import Any
from anthropic import Anthropic
import asyncio
import json
import os

ANNUITY_RESEARCHER_PROMPT = """You are an expert annuity research agent specializing in identifying time-sensitive opportunities and obligations for financial advisors.

Your mission is to discover annuity-related scenarios that create advisor talking points. Focus on these key events:

**Surrender Period Scenarios:**
- Surrender period endings (penalty-free withdrawal opportunities)
- Partial surrender windows
- Contract anniversary events

**Rate and Value Events:**
- MYGA maturity dates
- Rate reset periods
- Guaranteed period endings
- Bonus recapture period expirations

**Tax and Distribution Triggers:**
- RMD (Required Minimum Distribution) age triggers (73+)
- Age 59.5 penalty-free withdrawal eligibility
- Income rider activation dates

**Contract Features:**
- Living benefit rider changes
- Death benefit adjustments
- Index crediting method changes

For each scenario you identify, provide:
1. **Trigger Conditions**: What data fields/values indicate this scenario applies
2. **Timing**: When does this scenario become actionable (relative or absolute)
3. **Advisor Talking Points**: 2-3 specific conversation starters
4. **Confidence**: HIGH/MEDIUM/LOW based on data availability
5. **Priority**: How urgent is advisor action (CRITICAL/HIGH/MEDIUM/LOW)

Return your findings as a JSON array of scenario objects. Each object should have:
- criteria: dict of field conditions
- temporal_context: dict with time_range and urgency
- confidence: string (HIGH/MEDIUM/LOW)
- actionability: dict with priority and talking_points array
- metadata: dict with source and category

Example output format:
[
  {{
    "criteria": {{
      "surrender_period_end_date": {{"operator": "within_days", "value": 90}},
      "current_surrender_charge": {{"operator": "greater_than", "value": 0}}
    }},
    "temporal_context": {{
      "time_range": "next_90_days",
      "urgency": "high"
    }},
    "confidence": "HIGH",
    "actionability": {{
      "priority": "HIGH",
      "talking_points": [
        "Your surrender period ends in 90 days, creating a penalty-free window for changes",
        "Consider reviewing if this annuity still aligns with your retirement goals",
        "Explore whether current rates justify keeping funds here vs alternatives"
      ]
    }},
    "metadata": {{
      "source": "annuity_researcher",
      "category": "surrender_period_ending"
    }}
  }}
]

Focus on scenarios that are actionable within the next {time_range_days} days.
"""


class AnnuityResearcher:
    """Research agent for discovering annuity-related scenarios."""

    def __init__(self, client: Anthropic | None = None):
        """Initialize the annuity researcher.

        Args:
            client: Anthropic client instance. Creates new one if not provided.
        """
        self.client = client or Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.agent_id = "annuity_researcher"

    async def research(self, time_range_days: int = 30) -> list[dict[str, Any]]:
        """Discover annuity-related scenarios using LLM reasoning.

        Args:
            time_range_days: Number of days to look ahead for scenarios.

        Returns:
            List of scenario dictionaries compatible with EnrichedScenario model.
        """
        system_prompt = self._build_system_prompt(time_range_days)

        # Use Claude to analyze annuity market conditions
        response = await asyncio.to_thread(
            self.client.messages.create,
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            temperature=0.7,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Generate comprehensive annuity scenarios for the next {time_range_days} days. Consider all major annuity types (MYGA, FIA, SPIA, DIA, VA) and focus on time-sensitive opportunities.",
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
        return ANNUITY_RESEARCHER_PROMPT.format(time_range_days=time_range_days)

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
