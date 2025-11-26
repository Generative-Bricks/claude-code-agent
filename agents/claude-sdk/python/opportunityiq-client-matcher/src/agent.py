"""
OpportunityIQ Client Matcher Agent

Main agent implementation using Claude SDK for matching clients to revenue opportunities.

Workflow:
1. Load scenarios from JSON files
2. Load client data (JSON or eventually Google Sheets)
3. Match clients against scenarios
4. Calculate revenue potential
5. Rank and prioritize opportunities
6. Generate actionable reports

Biblical Principle: TRUTH - Every match decision is observable and traceable
Biblical Principle: HONOR - Client data sovereignty and privacy
Biblical Principle: EXCELLENCE - Production-grade from inception
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from anthropic import Anthropic
from dotenv import load_dotenv

from src.tools import (
    load_all_scenario_files,
    match_clients_to_scenarios,
    calculate_revenue,
    rank_opportunities,
    generate_report
)
from src.models import Scenario, ClientProfile, Opportunity

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OpportunityIQAgent:
    """
    OpportunityIQ Client Matcher Agent with Claude SDK integration.

    This agent specializes in matching financial advisor clients to revenue
    opportunity scenarios and generating prioritized action reports.

    Core Capabilities:
    - Load opportunity scenarios from JSON
    - Match client profiles against scenarios
    - Calculate revenue potential
    - Rank by composite score (match quality + revenue)
    - Generate formatted reports (markdown, text, JSON, CSV)

    Attributes:
        client: Anthropic API client
        model: Claude model to use
        scenarios_directory: Path to scenarios directory
        default_scenarios: List of loaded default scenarios
    """

    def __init__(self, scenarios_directory: str = "data/scenarios"):
        """
        Initialize the OpportunityIQ Agent.

        Loads configuration from environment variables:
        - ANTHROPIC_API_KEY (required)
        - CLAUDE_MODEL (optional - defaults to claude-sonnet-4-5-20250929)
        - SCENARIOS_DIRECTORY (optional - defaults to data/scenarios)

        Args:
            scenarios_directory: Path to directory containing scenario JSON files

        Raises:
            ValueError: If ANTHROPIC_API_KEY is not found in environment
        """
        # Load environment variables
        load_dotenv()

        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")
        self.scenarios_directory = os.getenv(
            "SCENARIOS_DIRECTORY",
            scenarios_directory
        )

        # Biblical Principle: EXCELLENCE - Validate configuration from start
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found in environment. "
                "Please set it in .env file or environment variables."
            )

        # Initialize Claude client
        self.client = Anthropic(api_key=self.api_key)

        # Load default scenarios
        self.default_scenarios = []
        self._load_default_scenarios()

        logger.info(f"OpportunityIQ Agent initialized with model: {self.model}")
        logger.info(f"Loaded {len(self.default_scenarios)} default scenarios")

    def _load_default_scenarios(self):
        """
        Load default scenarios from scenarios directory.

        Loads all JSON files from the scenarios directory and validates them
        against the Scenario model. Logs warnings for invalid files.
        """
        scenarios_path = Path(self.scenarios_directory)

        if not scenarios_path.exists():
            logger.warning(f"Scenarios directory not found: {self.scenarios_directory}")
            return

        try:
            self.default_scenarios = load_all_scenario_files(self.scenarios_directory)
            logger.info(f"Loaded {len(self.default_scenarios)} scenarios from {self.scenarios_directory}")
        except Exception as e:
            logger.error(f"Failed to load default scenarios: {e}")
            self.default_scenarios = []

    def analyze_clients(
        self,
        clients: List[Dict[str, Any]],
        scenarios: Optional[List[Dict[str, Any]]] = None,
        min_match_threshold: float = 60.0,
        ranking_strategy: str = "composite",
        match_weight: float = 0.4,
        revenue_weight: float = 0.6,
        limit: Optional[int] = None,
        report_format: str = "markdown"
    ) -> Dict[str, Any]:
        """
        Analyze clients for revenue opportunities and generate report.

        This is the primary entry point for the agent's workflow:
        1. Load scenarios (use provided or defaults)
        2. Match clients to scenarios
        3. Calculate revenue for each match
        4. Rank opportunities
        5. Generate report

        Args:
            clients: List of client profile dictionaries
            scenarios: Optional list of scenario dictionaries (uses defaults if None)
            min_match_threshold: Minimum match score required (0-100)
            ranking_strategy: How to rank ("composite", "revenue", "match_score", "priority")
            match_weight: Weight for match score in composite ranking (0.0-1.0)
            revenue_weight: Weight for revenue in composite ranking (0.0-1.0)
            limit: Optional limit on number of opportunities to return
            report_format: Report format ("markdown", "text", "json", "summary")

        Returns:
            Dictionary containing:
            - opportunities: List of Opportunity objects
            - report: Formatted report string
            - summary: Summary statistics

        Raises:
            ValueError: If inputs are invalid
        """
        logger.info(f"Starting client analysis for {len(clients)} clients")

        # 1. Load scenarios
        if scenarios is None:
            if not self.default_scenarios:
                raise ValueError("No scenarios available. Provide scenarios or check scenarios directory.")
            scenarios_to_use = self.default_scenarios
            logger.info(f"Using {len(scenarios_to_use)} default scenarios")
        else:
            scenarios_to_use = scenarios
            logger.info(f"Using {len(scenarios_to_use)} provided scenarios")

        # 2. Match clients to scenarios
        logger.info("Matching clients to scenarios...")
        opportunities = match_clients_to_scenarios(
            clients=clients,
            scenarios=scenarios_to_use,
            min_match_threshold=min_match_threshold
        )

        logger.info(f"Found {len(opportunities)} opportunities")

        # 3. Calculate revenue for each opportunity (if not already calculated)
        # Note: Revenue is calculated during matching, so this is a no-op currently
        # Keeping for future enhancement where revenue calculation might be separate

        # 4. Rank opportunities
        logger.info(f"Ranking opportunities using {ranking_strategy} strategy...")
        ranked_opportunities = rank_opportunities(
            opportunities=opportunities,
            ranking_strategy=ranking_strategy,
            match_weight=match_weight,
            revenue_weight=revenue_weight,
            limit=limit
        )

        # Calculate summary statistics
        total_revenue = sum(opp.estimated_revenue for opp in ranked_opportunities)
        avg_match_score = sum(opp.match_score for opp in ranked_opportunities) / len(ranked_opportunities) if ranked_opportunities else 0

        logger.info(f"Ranked {len(ranked_opportunities)} opportunities")
        logger.info(f"Total revenue potential: ${total_revenue:.2f}")

        # 5. Generate report
        logger.info(f"Generating {report_format} report...")
        report = generate_report(
            opportunities=ranked_opportunities,
            format=report_format
        )

        # Return comprehensive results
        summary = {
            "total_opportunities": len(ranked_opportunities),
            "total_revenue": total_revenue,
            "average_match_score": avg_match_score,
            "clients_analyzed": len(clients),
            "scenarios_used": len(scenarios_to_use)
        }

        return {
            "opportunities": ranked_opportunities,
            "report": report,
            "summary": summary,
            "config": {
                "min_match_threshold": min_match_threshold,
                "ranking_strategy": ranking_strategy,
                "match_weight": match_weight,
                "revenue_weight": revenue_weight,
                "scenarios_count": len(scenarios_to_use),
                "clients_count": len(clients)
            }
        }

    def load_clients_from_file(self, file_path: str) -> List[ClientProfile]:
        """
        Load client data from JSON file.

        Args:
            file_path: Path to JSON file containing client data

        Returns:
            List of ClientProfile objects

        Raises:
            FileNotFoundError: If file does not exist
            ValueError: If JSON is invalid or validation fails
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Client data file not found: {file_path}")

        try:
            with open(path, 'r') as f:
                clients_data = json.load(f)

            if not isinstance(clients_data, list):
                raise ValueError("Client data must be a JSON array")

            # Convert dictionaries to ClientProfile objects
            clients = []
            for i, client_dict in enumerate(clients_data):
                try:
                    client = ClientProfile(**client_dict)
                    clients.append(client)
                except Exception as e:
                    logger.warning(f"Skipping client at index {i} due to validation error: {e}")
                    continue

            logger.info(f"Loaded {len(clients)} clients from: {file_path}")
            return clients

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in client data file: {e}")

    def load_scenarios_from_directory(self, directory: str) -> List[Dict[str, Any]]:
        """
        Load scenarios from a directory of JSON files.

        Args:
            directory: Path to directory containing scenario JSON files

        Returns:
            List of scenario dictionaries

        Raises:
            ValueError: If directory doesn't exist or contains no valid scenarios
        """
        scenarios = load_all_scenario_files(directory)

        if not scenarios:
            raise ValueError(f"No valid scenarios found in directory: {directory}")

        logger.info(f"Loaded {len(scenarios)} scenarios from: {directory}")
        return scenarios

    def quick_analysis(
        self,
        clients_file: str,
        scenarios_directory: Optional[str] = None,
        output_file: Optional[str] = None,
        top_n: int = 25
    ) -> Dict[str, Any]:
        """
        Quick analysis workflow: load clients, match, rank, and report.

        Convenience method for the most common use case:
        1. Load clients from file
        2. Load scenarios from directory (or use defaults)
        3. Run analysis
        4. Generate Top N report
        5. Optionally save to file

        Args:
            clients_file: Path to client data JSON file
            scenarios_directory: Optional scenarios directory (uses default if None)
            output_file: Optional path to save report
            top_n: Number of top opportunities to include in report

        Returns:
            Analysis results dictionary

        Example:
            agent = OpportunityIQAgent()
            results = agent.quick_analysis(
                clients_file="data/clients/sample-clients.json",
                output_file="report.md",
                top_n=25
            )
            print(results["report"])
        """
        logger.info("=== OpportunityIQ Quick Analysis ===")

        # Load clients
        clients = self.load_clients_from_file(clients_file)

        # Load scenarios if directory provided
        scenarios = None
        if scenarios_directory:
            scenarios = self.load_scenarios_from_directory(scenarios_directory)

        # Run analysis
        results = self.analyze_clients(
            clients=clients,
            scenarios=scenarios,
            limit=top_n,
            report_format="markdown"
        )

        # Save report if output file specified
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w') as f:
                f.write(results["report"])

            logger.info(f"Report saved to: {output_file}")
            results["output_file"] = str(output_path)

        logger.info("=== Analysis Complete ===")
        logger.info(f"Found {len(results['opportunities'])} opportunities")
        logger.info(f"Total revenue potential: ${results['summary']['total_revenue']:.2f}")

        return results

    def get_scenario_info(self) -> Dict[str, Any]:
        """
        Get information about loaded scenarios.

        Returns:
            Dictionary with scenario statistics and details
        """
        return {
            "count": len(self.default_scenarios),
            "directory": self.scenarios_directory,
            "scenarios": [
                {
                    "scenario_id": s.scenario_id,
                    "name": s.name,
                    "category": s.category,
                    "criteria_count": len(s.criteria)
                }
                for s in self.default_scenarios
            ]
        }

    def generate_insights_with_llm(
        self,
        opportunities: List[Opportunity],
        top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate AI-powered insights for top opportunities using Claude.

        Takes the top N opportunities and generates personalized insights including:
        - Why this opportunity makes sense for this specific client
        - Advisor talking points and conversation starters
        - Risk considerations and potential objections
        - Recommended next steps

        Args:
            opportunities: List of matched opportunities
            top_n: Number of top opportunities to analyze (default: 5)

        Returns:
            List of dictionaries with opportunity data + AI insights

        Example:
            insights = agent.generate_insights_with_llm(opportunities, top_n=3)
            for insight in insights:
                print(f"Client: {insight['client_name']}")
                print(f"Reasoning: {insight['ai_reasoning']}")
        """
        logger.info(f"Generating AI insights for top {top_n} opportunities...")

        # Select top N opportunities
        top_opportunities = opportunities[:top_n]
        insights = []

        for idx, opp in enumerate(top_opportunities, 1):
            logger.info(f"Generating insights for opportunity {idx}/{len(top_opportunities)}: {opp.client_name} - {opp.scenario_name}")

            # Build context prompt
            prompt = f"""You are a financial advisor assistant analyzing a revenue opportunity.

**Opportunity Overview:**
- Client: {opp.client_name}
- Opportunity: {opp.scenario_name}
- Match Score: {opp.match_score:.1f}%
- Estimated Revenue: ${opp.estimated_revenue:,.2f}
- Priority: {getattr(opp, 'priority', 'medium')}

**Match Details:**
{self._format_match_details(opp)}

**Your Task:**
Generate a concise analysis (200-300 words) with these sections:

1. **Why This Fits** (2-3 sentences): Explain why this opportunity makes sense for this specific client based on the match criteria.

2. **Talking Points** (3-4 bullet points): Key points the advisor should emphasize when discussing this with the client.

3. **Considerations** (2-3 bullet points): Potential risks, objections, or important factors to address.

4. **Next Steps** (2-3 action items): Specific, actionable steps the advisor should take.

Keep the tone professional but conversational. Focus on practical, actionable insights."""

            try:
                # Call Claude API
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    temperature=0.7,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )

                # Extract insight text
                insight_text = response.content[0].text

                # Track token usage
                input_tokens = response.usage.input_tokens
                output_tokens = response.usage.output_tokens
                total_tokens = input_tokens + output_tokens

                logger.info(f"  Generated insights ({total_tokens} tokens: {input_tokens} in, {output_tokens} out)")

                # Build enhanced opportunity dict
                insights.append({
                    "rank": getattr(opp, 'rank', idx),
                    "client_name": opp.client_name,
                    "scenario_name": opp.scenario_name,
                    "match_score": opp.match_score,
                    "estimated_revenue": opp.estimated_revenue,
                    "priority": getattr(opp, 'priority', 'medium'),
                    "ai_insights": insight_text,
                    "tokens_used": total_tokens,
                    "opportunity": opp  # Include original object
                })

            except Exception as e:
                logger.error(f"  Failed to generate insights: {e}")
                # Return opportunity without insights on error
                insights.append({
                    "rank": getattr(opp, 'rank', idx),
                    "client_name": opp.client_name,
                    "scenario_name": opp.scenario_name,
                    "match_score": opp.match_score,
                    "estimated_revenue": opp.estimated_revenue,
                    "priority": getattr(opp, 'priority', 'medium'),
                    "ai_insights": None,
                    "error": str(e),
                    "opportunity": opp
                })

        # Calculate total tokens
        total_tokens = sum(i.get('tokens_used', 0) for i in insights)
        logger.info(f"AI insights generation complete. Total tokens: {total_tokens}")

        return insights

    def _format_match_details(self, opportunity: Opportunity) -> str:
        """Format match details for LLM prompt."""
        if not opportunity.match_details:
            return "No detailed match criteria available."

        details = []
        for detail in opportunity.match_details:
            status = "✓" if detail.matched else "✗"
            details.append(
                f"{status} {detail.criterion_field}: "
                f"Expected {detail.operator} {detail.expected_value}, "
                f"Actual: {detail.actual_value}"
            )

        return "\n".join(details)


def main():
    """
    Example usage of OpportunityIQ Agent.

    Demonstrates basic workflow with sample data.
    """
    # Initialize agent
    agent = OpportunityIQAgent()

    # Print scenario info
    info = agent.get_scenario_info()
    print(f"\nLoaded {info['count']} scenarios:")
    for scenario in info['scenarios']:
        print(f"  - {scenario['scenario_id']}: {scenario['name']}")

    # Example: Quick analysis with sample data
    try:
        results = agent.quick_analysis(
            clients_file="data/clients/sample-clients.json",
            output_file="outputs/analysis_report.md",
            top_n=10
        )

        print(f"\nAnalysis Complete!")
        print(f"Found {len(results['opportunities'])} opportunities")
        print(f"Report saved to: {results.get('output_file', 'N/A')}")

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Please ensure sample data files exist.")

    except Exception as e:
        print(f"\nError during analysis: {e}")
        logger.error(f"Analysis failed: {e}", exc_info=True)


if __name__ == "__main__":
    main()
