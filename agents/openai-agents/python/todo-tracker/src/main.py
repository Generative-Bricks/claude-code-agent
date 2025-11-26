"""
Main CLI entry point for the Todo Tracker Agent.

This module provides the command-line interface for interacting with
the Todo Tracker agent through natural language conversation.

Usage:
    # Interactive mode (default)
    python -m src.main

    # Single command mode
    python -m src.main --command "add a todo to buy groceries"

    # Show statistics
    python -m src.main --stats

Biblical Principle: SERVE - Simple interface for powerful task management.
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH)

from agents import Runner

from src.agent import todo_tracker_agent
from src.services.storage import get_storage

# ============================================================================
# Logging Configuration
# ============================================================================

LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOGS_DIR / "todo_tracker.log"

# Configure logging - only show our app logs on console, send all to file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
    ],
)

# Suppress noisy third-party logs (httpx telemetry, openai internals)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# ============================================================================
# CLI Functions
# ============================================================================


def show_statistics() -> None:
    """Display todo statistics."""
    storage = get_storage()
    stats = storage.get_stats()

    print("\n" + "=" * 50)
    print("📊 Todo Statistics")
    print("=" * 50)
    print(f"Total todos:    {stats['total']}")
    print(f"Pending:        {stats['pending']}")
    print(f"In progress:    {stats['in_progress']}")
    print(f"Completed:      {stats['completed']}")
    print(f"Overdue:        {stats['overdue']}")
    print("=" * 50 + "\n")


def show_welcome() -> None:
    """Display welcome message."""
    print("\n" + "=" * 50)
    print("📋 Todo Tracker Agent")
    print("=" * 50)
    print("Your AI-powered task management assistant")
    print("")
    print("Commands:")
    print("  - Type naturally to manage your todos")
    print("  - 'quit' or 'exit' to leave")
    print("  - 'stats' to see statistics")
    print("  - 'help' for usage tips")
    print("=" * 50 + "\n")


def show_help() -> None:
    """Display help message."""
    print("\n" + "-" * 50)
    print("💡 Usage Tips")
    print("-" * 50)
    print("\nAdding todos:")
    print('  "Add a todo to buy groceries"')
    print('  "Create a high priority task to finish report by Friday"')
    print('  "Add todo: call mom, tag it as family"')
    print("\nViewing todos:")
    print('  "Show all my todos"')
    print('  "List pending tasks"')
    print('  "Show urgent todos"')
    print('  "What\'s overdue?"')
    print("\nCompleting todos:")
    print('  "Mark abc123 as done"')
    print('  "Complete the groceries todo"')
    print("\nUpdating todos:")
    print('  "Change priority of abc123 to high"')
    print('  "Update the report deadline to next Monday"')
    print("\nDeleting todos:")
    print('  "Delete todo abc123"')
    print('  "Remove the groceries task"')
    print("\nSearching:")
    print('  "Find todos about groceries"')
    print('  "Search for work tasks"')
    print("-" * 50 + "\n")


async def run_interactive() -> None:
    """Run the agent in interactive mode."""
    show_welcome()

    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()

            # Handle special commands
            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n👋 Goodbye! Stay productive!")
                break

            if user_input.lower() == "stats":
                show_statistics()
                continue

            if user_input.lower() == "help":
                show_help()
                continue

            # Run the agent
            logger.info(f"User input: {user_input}")

            result = await Runner.run(
                todo_tracker_agent,
                input=user_input,
            )

            # Display response
            print(f"\nAssistant: {result.final_output}\n")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            print(f"\n❌ Error: {str(e)}\n")


async def run_single_command(command: str) -> None:
    """Run a single command and exit."""
    logger.info(f"Single command: {command}")

    try:
        result = await Runner.run(
            todo_tracker_agent,
            input=command,
        )
        print(result.final_output)
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        print(f"Error: {str(e)}")
        sys.exit(1)


# ============================================================================
# CLI Argument Parser
# ============================================================================


def create_argument_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Todo Tracker Agent - AI-powered task management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Interactive mode
    python -m src.main

    # Single command
    python -m src.main -c "add todo to buy milk"

    # Show statistics
    python -m src.main --stats
        """,
    )

    parser.add_argument(
        "-c", "--command",
        type=str,
        help="Run a single command and exit",
    )

    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show todo statistics and exit",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    return parser


# ============================================================================
# Main Entry Point
# ============================================================================


def main() -> int:
    """Main entry point."""
    parser = create_argument_parser()
    args = parser.parse_args()

    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Handle --stats flag
    if args.stats:
        show_statistics()
        return 0

    # Handle single command
    if args.command:
        asyncio.run(run_single_command(args.command))
        return 0

    # Default: interactive mode
    asyncio.run(run_interactive())
    return 0


if __name__ == "__main__":
    sys.exit(main())
