"""
Main Workflow & CLI for Multi-Agent Portfolio Collaboration System.

This module provides the command-line interface and main workflow orchestration
for running portfolio analysis using the Portfolio Manager and specialist agents.

Usage:
    # Interactive mode with Portfolio Manager agent
    python -m src.main --interactive

    # Analyze specific client and portfolio
    python -m src.main --client CLT-2024-002 --portfolio conservative

    # Batch analysis of all client-portfolio pairs
    python -m src.main --batch

    # Generate report only (requires previous analysis)
    python -m src.main --client CLT-2024-001 --report-only

Biblical Principle: SERVE - Making powerful multi-agent analysis accessible through simple interface.
Biblical Principle: EXCELLENCE - Production-ready CLI with comprehensive error handling.
Biblical Principle: TRUTH - Full transparency in analysis workflow and agent interactions.
"""

import argparse
import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Optional, Tuple

from dotenv import load_dotenv

from agents import Runner
from agents.memory import SQLiteSession

# Load environment variables from .env file
# Explicitly specify the .env path relative to project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Import Portfolio Manager and data models
from src.agents.portfolio_manager import portfolio_manager_agent
from src.data.mock_portfolios import (
    get_aggressive_example,
    get_conservative_example,
    get_moderate_example,
)
from src.models.schemas import ClientProfile, Portfolio
from src.tools.report_generator import save_report_to_file

# ============================================================================
# Logging Configuration
# ============================================================================

# Create logs directory
LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging
LOG_FILE = LOGS_DIR / "portfolio_analysis.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# ============================================================================
# Paths Configuration
# ============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = PROJECT_ROOT / "examples"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
SESSION_DB_PATH = PROJECT_ROOT / "portfolio_sessions.db"

# Ensure directories exist
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# Data Loading Functions
# ============================================================================


def load_client_profiles() -> dict:
    """
    Load client profiles from examples/sample_clients.json.

    Returns:
        dict: Dictionary mapping client_id to ClientProfile objects
    """
    client_file = EXAMPLES_DIR / "sample_clients.json"

    try:
        with open(client_file, "r") as f:
            data = json.load(f)

        clients = {}
        for client_data in data.get("clients", []):
            client = ClientProfile(**client_data)
            clients[client.client_id] = client

        logger.info(f"Loaded {len(clients)} client profiles from {client_file}")
        return clients

    except FileNotFoundError:
        logger.error(f"Client profiles file not found: {client_file}")
        return {}
    except Exception as e:
        logger.error(f"Error loading client profiles: {e}")
        return {}


def load_portfolios() -> dict:
    """
    Load portfolios from examples/sample_portfolios.json.

    Returns:
        dict: Dictionary mapping portfolio names to Portfolio objects
    """
    portfolio_file = EXAMPLES_DIR / "sample_portfolios.json"

    try:
        with open(portfolio_file, "r") as f:
            data = json.load(f)

        portfolios = {}
        for portfolio_data in data.get("portfolios", []):
            portfolio = Portfolio(**portfolio_data)
            portfolios[portfolio.portfolio_id] = portfolio

        logger.info(f"Loaded {len(portfolios)} portfolios from {portfolio_file}")
        return portfolios

    except FileNotFoundError:
        logger.error(f"Portfolios file not found: {portfolio_file}")
        return {}
    except Exception as e:
        logger.error(f"Error loading portfolios: {e}")
        return {}


def get_portfolio_by_name(name: str) -> Optional[Portfolio]:
    """
    Get a portfolio by name using helper functions or loaded data.

    Args:
        name: Portfolio name (conservative, moderate, aggressive)

    Returns:
        Portfolio object or None if not found
    """
    name_lower = name.lower()

    # Try helper functions first (unpack tuple to get just Portfolio)
    if name_lower == "conservative":
        _, portfolio = get_conservative_example()
        return portfolio
    elif name_lower == "moderate":
        _, portfolio = get_moderate_example()
        return portfolio
    elif name_lower == "aggressive":
        _, portfolio = get_aggressive_example()
        return portfolio

    # Fall back to loaded portfolios
    portfolios = load_portfolios()
    return portfolios.get(name)


# ============================================================================
# Analysis Functions
# ============================================================================


def run_portfolio_analysis(
    client_id: str,
    portfolio_name: str,
    interactive: bool = False,
) -> Tuple[bool, Optional[str]]:
    """
    Run comprehensive portfolio analysis for a client.

    Args:
        client_id: Client identifier (e.g., "CLT-2024-001")
        portfolio_name: Portfolio name (e.g., "conservative", "moderate", "aggressive")
        interactive: If True, run in interactive mode with Agent Runner

    Returns:
        Tuple of (success: bool, report_path: Optional[str])
    """
    logger.info(f"\n{'=' * 80}")
    logger.info(f"Starting Portfolio Analysis")
    logger.info(f"Client ID: {client_id}")
    logger.info(f"Portfolio: {portfolio_name}")
    logger.info(f"Mode: {'Interactive' if interactive else 'Batch'}")
    logger.info(f"{'=' * 80}\n")

    # Load client profile
    clients = load_client_profiles()
    client_profile = clients.get(client_id)

    if not client_profile:
        logger.error(f"Client {client_id} not found")
        return False, None

    # Load portfolio
    portfolio = get_portfolio_by_name(portfolio_name)

    if not portfolio:
        logger.error(f"Portfolio '{portfolio_name}' not found")
        return False, None

    logger.info(f"✓ Loaded client profile: {client_profile.client_id} (Age {client_profile.age})")
    logger.info(
        f"✓ Loaded portfolio: {portfolio.portfolio_id} ({len(portfolio.holdings)} holdings)"
    )

    try:
        if interactive:
            # Interactive mode - use Agent Runner with conversation (async)
            return asyncio.run(run_interactive_analysis(client_profile, portfolio))
        else:
            # Batch mode - direct API calls
            return run_batch_analysis(client_profile, portfolio)

    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        return False, None


async def run_interactive_analysis(
    client_profile: ClientProfile, portfolio: Portfolio
) -> Tuple[bool, Optional[str]]:
    """
    Run analysis in interactive mode using Agent Runner.

    This mode allows conversational interaction with the Portfolio Manager
    agent using the OpenAI Agents SDK Runner.

    Args:
        client_profile: Client profile object
        portfolio: Portfolio object

    Returns:
        Tuple of (success: bool, report_path: Optional[str])
    """
    logger.info("Starting interactive mode...")

    # Initialize session with SQLite for conversation memory
    # Create unique session ID based on client and portfolio
    from datetime import datetime
    session_id = f"{client_profile.client_id}_{portfolio.portfolio_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    session = SQLiteSession(db_path=str(SESSION_DB_PATH), session_id=session_id)
    logger.info(f"Created session: {session_id}")

    # Create initial user message requesting analysis
    # Include portfolio holdings details
    holdings_details = "\n".join([
        f"  {i+1}. {h.ticker} ({h.company_name or 'N/A'}): {h.shares} shares @ ${h.current_price:.2f} = ${h.market_value:,.2f}"
        for i, h in enumerate(portfolio.holdings)
    ])

    initial_message = f"""Please analyze this portfolio for my client.

**Client Profile:**
- Client ID: {client_profile.client_id}
- Age: {client_profile.age}
- Risk Tolerance: {client_profile.risk_tolerance.value}
- Time Horizon: {client_profile.time_horizon} years
- Investment Goals: {', '.join(client_profile.investment_goals)}
{f'- Annual Income: ${client_profile.annual_income:,.0f}' if client_profile.annual_income else ''}

**Portfolio ({portfolio.portfolio_id}):**
- Total Value: ${portfolio.total_value:,.2f}
- Holdings ({len(portfolio.holdings)}):
{holdings_details}

Please run a comprehensive analysis and provide recommendations.
"""

    logger.info("\n" + "=" * 80)
    logger.info("USER REQUEST:")
    logger.info("=" * 80)
    logger.info(initial_message)
    logger.info("=" * 80 + "\n")

    # Run the Portfolio Manager agent
    try:
        result = await Runner.run(
            portfolio_manager_agent,
            input=initial_message,
            session=session,
            context={
                "client_profile": client_profile.model_dump(),
                "portfolio": portfolio.model_dump(),
            },
        )

        logger.info("\n" + "=" * 80)
        logger.info("PORTFOLIO MANAGER RESPONSE:")
        logger.info("=" * 80)
        logger.info(result.final_output)
        logger.info("=" * 80 + "\n")

        # Log execution metrics
        logger.info("\n" + "=" * 80)
        logger.info("EXECUTION METRICS:")
        logger.info("=" * 80)

        # Token usage (if available)
        if hasattr(result, 'usage') and result.usage:
            logger.info(f"Token Usage:")
            logger.info(f"  - Prompt tokens: {result.usage.get('prompt_tokens', 'N/A')}")
            logger.info(f"  - Completion tokens: {result.usage.get('completion_tokens', 'N/A')}")
            logger.info(f"  - Total tokens: {result.usage.get('total_tokens', 'N/A')}")

        # Tool calls (if available in messages)
        if hasattr(result, 'messages') and result.messages:
            tool_calls = []
            for msg in result.messages:
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        tool_name = tool_call.function.name if hasattr(tool_call, 'function') else str(tool_call)
                        tool_calls.append(tool_name)

            if tool_calls:
                logger.info(f"\nTools Called ({len(tool_calls)}):")
                for i, tool in enumerate(tool_calls, 1):
                    logger.info(f"  {i}. {tool}")

        logger.info("=" * 80 + "\n")

        # Save report if generated
        report_path = None
        if "# Portfolio Analysis Report" in result.final_output:
            report_filename = f"{client_profile.client_id}_{portfolio.portfolio_id}_report.md"
            report_path = save_report_to_file(result.final_output, report_filename)
            logger.info(f"✓ Report saved to: {report_path}")

        return True, report_path

    except Exception as e:
        logger.error(f"Interactive analysis failed: {e}", exc_info=True)
        return False, None


def run_batch_analysis(
    client_profile: ClientProfile, portfolio: Portfolio
) -> Tuple[bool, Optional[str]]:
    """
    Run analysis in batch mode (non-interactive).

    This mode directly calls the analysis tools without Agent Runner,
    suitable for automated processing of multiple portfolios.

    Args:
        client_profile: Client profile object
        portfolio: Portfolio object

    Returns:
        Tuple of (success: bool, report_path: Optional[str])
    """
    logger.info("Starting batch mode analysis...")

    try:
        # Import callable tools (not @function_tool decorated versions)
        from src.agents.portfolio_manager import (
            do_comprehensive_analysis,
            do_generate_client_report,
        )

        # Run comprehensive analysis
        logger.info("Running comprehensive analysis...")
        recommendations = do_comprehensive_analysis(portfolio, client_profile)

        logger.info(f"✓ Analysis complete")
        logger.info(f"  - Risk Rating: {recommendations.risk_analysis.risk_rating.value}")
        logger.info(
            f"  - Compliance Status: {recommendations.compliance_report.overall_status.value}"
        )
        logger.info(
            f"  - Suitability Score: {recommendations.suitability_score.overall_score:.1f}/100 "
            f"({recommendations.suitability_score.interpretation.value})"
        )

        # Generate report
        logger.info("Generating report...")
        report = do_generate_client_report(recommendations)

        # Save report
        report_filename = f"{client_profile.client_id}_{portfolio.portfolio_id}_report.md"
        report_path = save_report_to_file(report, report_filename)

        logger.info(f"✓ Report saved to: {report_path}")
        logger.info(f"\n{'=' * 80}")
        logger.info("ANALYSIS SUMMARY")
        logger.info(f"{'=' * 80}")
        logger.info(f"Client: {client_profile.client_id}")
        logger.info(f"Portfolio: {portfolio.portfolio_id}")
        logger.info(f"Suitability: {recommendations.suitability_score.overall_score:.0f}/100")
        logger.info(f"Recommendations: {len(recommendations.recommendations)}")
        logger.info(f"Action Items: {len(recommendations.action_items)}")
        logger.info(f"{'=' * 80}\n")

        return True, report_path

    except Exception as e:
        logger.error(f"Batch analysis failed: {e}", exc_info=True)
        return False, None


def run_batch_all() -> None:
    """
    Run batch analysis for all client-portfolio combinations.

    This processes all available clients against all available portfolios,
    useful for testing and bulk analysis.
    """
    logger.info("\n" + "=" * 80)
    logger.info("BATCH ANALYSIS - ALL COMBINATIONS")
    logger.info("=" * 80 + "\n")

    clients = load_client_profiles()
    portfolio_names = ["conservative", "moderate", "aggressive"]

    if not clients:
        logger.error("No clients loaded. Exiting.")
        return

    total = len(clients) * len(portfolio_names)
    completed = 0
    failed = 0

    for client_id in clients.keys():
        for portfolio_name in portfolio_names:
            success, report_path = run_portfolio_analysis(
                client_id=client_id,
                portfolio_name=portfolio_name,
                interactive=False,
            )

            if success:
                completed += 1
            else:
                failed += 1

    logger.info("\n" + "=" * 80)
    logger.info("BATCH ANALYSIS COMPLETE")
    logger.info("=" * 80)
    logger.info(f"Total: {total}")
    logger.info(f"Completed: {completed}")
    logger.info(f"Failed: {failed}")
    logger.info(f"Success Rate: {completed/total*100:.0f}%")
    logger.info("=" * 80 + "\n")


# ============================================================================
# CLI Argument Parser
# ============================================================================


def create_argument_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser with all options."""
    parser = argparse.ArgumentParser(
        description="Multi-Agent Portfolio Collaboration System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Interactive mode with Portfolio Manager
    python -m src.main --interactive

    # Analyze specific client and portfolio
    python -m src.main --client CLT-2024-002 --portfolio moderate

    # Batch analysis of all combinations
    python -m src.main --batch

    # List available clients and portfolios
    python -m src.main --list
        """,
    )

    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode with conversational agent",
    )

    parser.add_argument(
        "--client",
        type=str,
        help="Client ID (e.g., CLT-2024-001)",
    )

    parser.add_argument(
        "--portfolio",
        type=str,
        help="Portfolio name (conservative, moderate, aggressive)",
    )

    parser.add_argument(
        "--batch",
        action="store_true",
        help="Run batch analysis for all client-portfolio combinations",
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List available clients and portfolios",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging (DEBUG level)",
    )

    return parser


def list_available_data() -> None:
    """List all available clients and portfolios."""
    logger.info("\n" + "=" * 80)
    logger.info("AVAILABLE DATA")
    logger.info("=" * 80 + "\n")

    # List clients
    clients = load_client_profiles()
    logger.info("CLIENTS:")
    for client_id, client in clients.items():
        logger.info(
            f"  - {client_id}: Age {client.age}, {client.risk_tolerance.value} risk tolerance"
        )

    # List portfolios
    logger.info("\nPORTFOLIOS:")
    portfolios = load_portfolios()
    for name, portfolio in portfolios.items():
        logger.info(f"  - {name}: {len(portfolio.holdings)} holdings")

    logger.info("\n" + "=" * 80 + "\n")


# ============================================================================
# Main Entry Point
# ============================================================================


def main() -> int:
    """
    Main entry point for the Portfolio Analysis CLI.

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    parser = create_argument_parser()
    args = parser.parse_args()

    # Handle --verbose flag
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info("Verbose logging enabled")

    # Handle --list command
    if args.list:
        list_available_data()
        return 0

    # Handle --batch command
    if args.batch:
        run_batch_all()
        return 0

    # Handle single analysis (requires --client and --portfolio)
    if args.client and args.portfolio:
        success, report_path = run_portfolio_analysis(
            client_id=args.client,
            portfolio_name=args.portfolio,
            interactive=args.interactive,
        )
        return 0 if success else 1

    # Handle interactive mode without specific client/portfolio
    if args.interactive:
        logger.info("Interactive mode requires --client and --portfolio arguments")
        logger.info("Use --list to see available options")
        return 1

    # No valid command provided
    parser.print_help()
    return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
