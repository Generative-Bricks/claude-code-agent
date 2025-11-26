"""Life Event Research Agent

Discovers life event scenarios using LLM reasoning to identify:
- Retirement transitions
- Inheritance events
- Divorce proceedings
- Death of spouse
- Job changes
- Health events
- Home sales
"""

from typing import Any
from anthropic import Anthropic
import asyncio
import json
import os

LIFE_EVENT_RESEARCHER_PROMPT = """You are an expert life event research agent specializing in identifying significant life transitions that create financial planning opportunities.

Your mission is to discover life event scenarios that require advisor intervention. Focus on these key events:

**Retirement Transitions:**
- Approaching retirement age (within 12 months)
- Recent retirement (within 6 months)
- Social Security claiming decisions
- Pension election windows

**Family Events:**
- Death of spouse (recent or upcoming estate settlement)
- Divorce proceedings or settlements
- Inheritance receipts
- Birth/adoption of children or grandchildren
- Adult children leaving home

**Career Changes:**
- Job changes or unemployment
- Business sale or exit
- Executive compensation events
- 401(k) rollover opportunities

**Health Events:**
- Long-term care needs
- Major medical expenses
- Medicare enrollment (age 65)
- Disability events

**Major Purchases:**
- Home sales or purchases
- Large asset liquidations
- Real estate investments

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
      "age": {{"operator": "equals", "value": 65}},
      "retirement_date": {{"operator": "within_days", "value": 180}}
    }},
    "temporal_context": {{
      "time_range": "next_6_months",
      "urgency": "high"
    }},
    "confidence": "HIGH",
    "actionability": {{
      "priority": "CRITICAL",
      "talking_points": [
        "You're approaching retirement in 6 months - let's review your income strategy",
        "Medicare enrollment is mandatory at 65 - have you completed your application?",
        "Consider converting traditional IRA funds to Roth before RMDs begin at 73"
      ]
    }},
    "metadata": {{
      "source": "life_event_researcher",
      "category": "retirement_transition"
    }}
  }}
]

Focus on scenarios that are actionable within the next {time_range_days} days.
"""


class LifeEventResearcher:
    """Research agent for discovering life event scenarios."""

    def __init__(self, client: Anthropic | None = None):
        """Initialize the life event researcher.

        Args:
            client: Anthropic client instance. Creates new one if not provided.
        """
        self.client = client or Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.agent_id = "life_event_researcher"

    async def research(self, time_range_days: int = 30) -> list[dict[str, Any]]:
        """Discover life event scenarios using LLM reasoning.

        Args:
            time_range_days: Number of days to look ahead for scenarios.

        Returns:
            List of scenario dictionaries compatible with EnrichedScenario model.
        """
        system_prompt = self._build_system_prompt(time_range_days)

        # Use Claude to analyze life event patterns
        response = await asyncio.to_thread(
            self.client.messages.create,
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            temperature=0.7,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Generate comprehensive life event scenarios for the next {time_range_days} days. Consider all major life transitions and focus on time-sensitive opportunities that require proactive advisor outreach.",
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
        return LIFE_EVENT_RESEARCHER_PROMPT.format(time_range_days=time_range_days)

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
