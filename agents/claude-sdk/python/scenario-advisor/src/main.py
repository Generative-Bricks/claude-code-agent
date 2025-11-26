"""
Financial Scenario Advisor - CLI Entry Point

Orchestrates the full pipeline:
1. Research phase: Parallel research across domains
2. Synthesis phase: Generate scenario library
3. Execution phase: Match clients to scenarios
"""

import asyncio
import argparse
import logging
import json
import os
from pathlib import Path
from typing import Optional, List
from datetime import datetime

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from src.services.research_orchestrator import ResearchOrchestrator
from src.services.scenario_synthesizer import ScenarioSynthesizer
from src.services.execution_orchestrator import ExecutionOrchestrator

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def save_json(data: dict, output_dir: Path, filename: str) -> None:
    """Save data to JSON file with timestamp."""
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"{timestamp}_{filename}"

    with open(output_file, "w") as f:
        json.dump(data, f, indent=2, default=str)

    logger.info(f"Saved {filename} to {output_file}")


async def run_research_phase(
    focus_areas: Optional[List[str]],
    output_dir: Path,
    min_confidence: float
) -> dict:
    """Run research and synthesis phases."""
    logger.info("Starting research phase...")

    orchestrator = ResearchOrchestrator()
    research_results = await orchestrator.run_parallel_research(focus_areas)

    # Save research results
    save_json(research_results, output_dir, "research_results.json")

    logger.info("Starting synthesis phase...")
    synthesizer = ScenarioSynthesizer()
    scenarios = synthesizer.synthesize(research_results, min_confidence)

    # Save scenarios
    save_json({"scenarios": scenarios}, output_dir, "scenario_library.json")

    logger.info(f"Generated {len(scenarios)} scenarios with confidence >= {min_confidence}")

    return scenarios


async def run_execution_phase(
    scenarios: dict,
    clients_path: str,
    output_dir: Path,
    min_match_score: float
) -> dict:
    """Run execution phase to match clients with scenarios."""
    logger.info("Starting execution phase...")

    # Load client data
    clients_file = Path(clients_path)
    if not clients_file.exists():
        raise FileNotFoundError(f"Client data not found: {clients_path}")

    with open(clients_file, "r") as f:
        client_data = json.load(f)

    # Execute matching
    executor = ExecutionOrchestrator()
    opportunities = await executor.execute(scenarios, client_data, min_match_score)

    # Save opportunities
    save_json({"opportunities": opportunities}, output_dir, "client_opportunities.json")

    logger.info(f"Generated {len(opportunities)} client opportunities")

    return opportunities


async def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Financial Scenario Advisor - Multi-agent scenario research and client matching system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full pipeline with all focus areas
  python -m src.main --mode full --clients data/clients/sample-clients.json

  # Research only, focusing on annuity products
  python -m src.main --mode research --focus annuity

  # Execute with existing scenarios
  python -m src.main --mode execute --clients data/clients/my-clients.json --min-match 70.0

  # Full pipeline with higher quality thresholds
  python -m src.main --mode full --clients data/clients/sample-clients.json --min-confidence 0.75 --min-match 75.0
        """
    )

    parser.add_argument(
        "--mode",
        choices=["research", "execute", "full"],
        default="full",
        help="Pipeline mode: research only, execute only, or full pipeline (default: full)"
    )

    parser.add_argument(
        "--clients",
        type=str,
        help="Path to client data JSON file (required for execute/full modes)"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="data/output",
        help="Output directory for results (default: data/output)"
    )

    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.6,
        help="Minimum confidence score for scenarios (0.0-1.0, default: 0.6)"
    )

    parser.add_argument(
        "--min-match",
        type=float,
        default=60.0,
        help="Minimum match score for client opportunities (0-100, default: 60.0)"
    )

    parser.add_argument(
        "--focus",
        nargs="+",
        choices=["annuity", "life_event", "revenue"],
        help="Focus areas for research (default: all areas)"
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)

    # Validate arguments
    if args.mode in ["execute", "full"] and not args.clients:
        parser.error("--clients is required for execute and full modes")

    output_dir = Path(args.output)
    scenarios = None

    try:
        # Research phase
        if args.mode in ["research", "full"]:
            scenarios = await run_research_phase(
                args.focus,
                output_dir,
                args.min_confidence
            )

        # Execution phase
        if args.mode in ["execute", "full"]:
            # Load scenarios if executing only
            if args.mode == "execute":
                # Look for most recent scenario library
                scenario_files = sorted(
                    output_dir.glob("*_scenario_library.json"),
                    reverse=True
                )
                if not scenario_files:
                    raise FileNotFoundError(
                        "No scenario library found. Run research mode first."
                    )

                with open(scenario_files[0], "r") as f:
                    data = json.load(f)
                    scenarios = data.get("scenarios", [])

                logger.info(f"Loaded {len(scenarios)} scenarios from {scenario_files[0]}")

            # Execute matching
            opportunities = await run_execution_phase(
                scenarios,
                args.clients,
                output_dir,
                args.min_match
            )

            # Summary
            logger.info("\n" + "="*60)
            logger.info("EXECUTION SUMMARY")
            logger.info("="*60)
            logger.info(f"Total opportunities identified: {len(opportunities)}")
            logger.info(f"Output directory: {output_dir}")
            logger.info("="*60)

        logger.info("Pipeline completed successfully!")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=args.verbose)
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
