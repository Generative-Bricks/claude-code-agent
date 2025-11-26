#!/usr/bin/env python3
"""
OpportunityIQ Client Matcher - Main Entry Point

Command-line interface for the OpportunityIQ Client Matcher agent.

Usage Examples:
    # Quick analysis with sample data
    python -m src.main

    # Analyze specific client file
    python -m src.main --clients data/clients/my-clients.json

    # Use custom scenarios directory
    python -m src.main --clients data/clients/my-clients.json --scenarios data/my-scenarios

    # Save report to file
    python -m src.main --clients data/clients/my-clients.json --output report.md

    # Top 10 opportunities only
    python -m src.main --clients data/clients/my-clients.json --limit 10

    # Adjust ranking weights (favor revenue over match quality)
    python -m src.main --clients data/clients/my-clients.json --revenue-weight 0.8 --match-weight 0.2

Biblical Principle: SERVE - Simple, clear interface that makes the agent easy to use
"""

import argparse
import sys
import logging
from pathlib import Path
from typing import Optional

from src.agent import OpportunityIQAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_summary(results: dict):
    """
    Print analysis summary in a readable format.

    Args:
        results: Results dictionary from OpportunityIQAgent.analyze_clients()
    """
    summary = results['summary']
    config = results['config']
    opportunities = results['opportunities']

    print("\n" + "=" * 80)
    print("OPPORTUNITYIQ CLIENT MATCHER - ANALYSIS SUMMARY")
    print("=" * 80)

    # Configuration
    print("\n📋 CONFIGURATION")
    print(f"Clients Analyzed: {config['clients_count']}")
    print(f"Scenarios Used: {config['scenarios_count']}")
    print(f"Min Match Threshold: {config['min_match_threshold']}%")
    print(f"Ranking Strategy: {config['ranking_strategy']}")
    print(f"Weights: Match {config['match_weight']:.0%} | Revenue {config['revenue_weight']:.0%}")

    # Summary Statistics
    print("\n📊 RESULTS")
    print(f"Opportunities Found: {summary['total_opportunities']}")
    print(f"Total Revenue Potential: ${summary['total_revenue']:,.2f}")
    print(f"Average Match Score: {summary['average_match_score']:.1f}%")

    # Breakdown by category
    if summary.get('by_category'):
        print("\n📈 BY CATEGORY")
        for category, count in summary['by_category'].items():
            print(f"  • {category}: {count} opportunities")

    # Breakdown by priority
    if summary.get('by_priority'):
        print("\n⚡ BY PRIORITY")
        for priority, count in summary['by_priority'].items():
            priority_display = priority.replace('_', ' ').title()
            print(f"  • {priority_display}: {count} opportunities")

    # Top 5 opportunities preview
    if opportunities:
        print("\n🎯 TOP 5 OPPORTUNITIES")
        for idx, opp in enumerate(opportunities[:5], 1):
            print(f"\n{idx}. {opp.client_name} - {opp.scenario_name}")
            print(f"   Match Score: {opp.match_score:.1f}% | Revenue: ${opp.estimated_revenue:,.2f}")
            priority = getattr(opp, 'priority', 'N/A')
            if priority and priority != 'N/A':
                priority = priority.replace('_', ' ').title()
            print(f"   Priority: {priority}")

    print("\n" + "=" * 80)


def main():
    """
    Main entry point for OpportunityIQ CLI.

    Parses command-line arguments and runs the agent analysis.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="Match financial advisor clients to revenue opportunity scenarios",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick analysis with sample data
  python src/main.py

  # Analyze specific client file
  python src/main.py --clients data/clients/my-clients.json

  # Use custom scenarios
  python src/main.py --clients data/clients/my-clients.json --scenarios data/custom-scenarios

  # Save report and show top 10
  python src/main.py --clients data/clients/my-clients.json --output report.md --limit 10

  # Adjust ranking (favor revenue)
  python src/main.py --clients data/clients/my-clients.json --revenue-weight 0.8 --match-weight 0.2

  # JSON output for integrations
  python src/main.py --clients data/clients/my-clients.json --format json --output results.json
        """
    )

    # Input arguments
    parser.add_argument(
        "--clients",
        help="Path to client data JSON file (defaults to sample-clients.json)"
    )

    parser.add_argument(
        "--scenarios",
        help="Path to scenarios directory (defaults to data/scenarios)"
    )

    # Analysis parameters
    parser.add_argument(
        "--min-match-threshold",
        type=float,
        default=60.0,
        help="Minimum match score required (0-100, default: 60.0)"
    )

    parser.add_argument(
        "--ranking-strategy",
        choices=["composite", "revenue", "match_score", "priority"],
        default="composite",
        help="How to rank opportunities (default: composite)"
    )

    parser.add_argument(
        "--match-weight",
        type=float,
        default=0.4,
        help="Weight for match score in composite ranking (0.0-1.0, default: 0.4)"
    )

    parser.add_argument(
        "--revenue-weight",
        type=float,
        default=0.6,
        help="Weight for revenue in composite ranking (0.0-1.0, default: 0.6)"
    )

    parser.add_argument(
        "--limit",
        type=int,
        help="Limit number of opportunities to return (e.g., top 25)"
    )

    # Output arguments
    parser.add_argument(
        "--format",
        choices=["markdown", "text", "json", "summary"],
        default="markdown",
        help="Report format (default: markdown)"
    )

    parser.add_argument(
        "--output",
        help="Path to save report (prints to console if not specified)"
    )

    # Utility arguments
    parser.add_argument(
        "--list-scenarios",
        action="store_true",
        help="List available scenarios and exit"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging (DEBUG level)"
    )

    parser.add_argument(
        "--generate-insights",
        action="store_true",
        help="Generate AI-powered insights using Claude (uses API tokens)"
    )

    parser.add_argument(
        "--insights-count",
        type=int,
        default=3,
        help="Number of opportunities to generate insights for (default: 3)"
    )

    args = parser.parse_args()

    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")

    try:
        # Initialize agent
        logger.info("Initializing OpportunityIQ Agent...")
        agent = OpportunityIQAgent()

        # List scenarios and exit if requested
        if args.list_scenarios:
            info = agent.get_scenario_info()
            print(f"\n📁 Scenarios Directory: {info['directory']}")
            print(f"📊 Total Scenarios: {info['count']}\n")

            if info['scenarios']:
                print("Available Scenarios:")
                for scenario in info['scenarios']:
                    print(f"\n  ID: {scenario['scenario_id']}")
                    print(f"  Name: {scenario['name']}")
                    print(f"  Category: {scenario['category']}")
                    print(f"  Criteria: {scenario['criteria_count']} matching rules")
            else:
                print("No scenarios found. Please check scenarios directory.")

            return 0

        # Validate weights
        if args.match_weight + args.revenue_weight != 1.0:
            logger.warning(
                f"Match weight ({args.match_weight}) + Revenue weight ({args.revenue_weight}) "
                f"should equal 1.0. Normalizing..."
            )
            total = args.match_weight + args.revenue_weight
            args.match_weight = args.match_weight / total
            args.revenue_weight = args.revenue_weight / total
            logger.info(f"Normalized weights: Match={args.match_weight:.2f}, Revenue={args.revenue_weight:.2f}")

        # Determine clients file
        clients_file = args.clients or "data/clients/sample-clients.json"

        # Verify clients file exists
        if not Path(clients_file).exists():
            logger.error(f"Client data file not found: {clients_file}")
            print(f"\nError: Client data file not found: {clients_file}", file=sys.stderr)
            print("\nPlease provide a valid client data file with --clients argument.", file=sys.stderr)
            print("Example: python src/main.py --clients data/clients/my-clients.json", file=sys.stderr)
            return 1

        # Load clients
        logger.info(f"Loading clients from: {clients_file}")
        clients = agent.load_clients_from_file(clients_file)

        # Load scenarios if directory provided
        scenarios = None
        if args.scenarios:
            logger.info(f"Loading scenarios from: {args.scenarios}")
            scenarios = agent.load_scenarios_from_directory(args.scenarios)

        # Run analysis
        logger.info("Running analysis...")
        results = agent.analyze_clients(
            clients=clients,
            scenarios=scenarios,
            min_match_threshold=args.min_match_threshold,
            ranking_strategy=args.ranking_strategy,
            match_weight=args.match_weight,
            revenue_weight=args.revenue_weight,
            limit=args.limit,
            report_format=args.format
        )

        # Generate AI insights if requested
        if args.generate_insights:
            logger.info("Generating AI-powered insights...")
            print(f"\n🤖 Generating AI insights for top {args.insights_count} opportunities...")
            print("(This will use Claude API tokens)\n")

            insights = agent.generate_insights_with_llm(
                opportunities=results["opportunities"],
                top_n=args.insights_count
            )

            results["ai_insights"] = insights

            # Print insights
            print("\n" + "=" * 80)
            print("🤖 AI-POWERED INSIGHTS")
            print("=" * 80)

            for insight in insights:
                print(f"\n{'='*80}")
                print(f"#{insight['rank']} - {insight['client_name']} - {insight['scenario_name']}")
                print(f"Match: {insight['match_score']:.1f}% | Revenue: ${insight['estimated_revenue']:,.2f}")
                print(f"{'='*80}")

                if insight.get('ai_insights'):
                    print(f"\n{insight['ai_insights']}")
                    if 'tokens_used' in insight:
                        print(f"\n[Tokens: {insight['tokens_used']}]")
                elif insight.get('error'):
                    print(f"\n❌ Error generating insights: {insight['error']}")

                print()

        # Print summary to console
        print_summary(results)

        # Print or save report
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w') as f:
                f.write(results["report"])

            logger.info(f"Report saved to: {args.output}")
            print(f"\n📄 Full report saved to: {args.output}")
        else:
            print("\n" + "=" * 80)
            print("FULL REPORT")
            print("=" * 80)
            print(results["report"])

        return 0

    except KeyboardInterrupt:
        logger.info("Analysis interrupted by user")
        print("\n\nAnalysis interrupted by user.", file=sys.stderr)
        return 1

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"\nError: {e}", file=sys.stderr)
        return 1

    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        print(f"\nError: {e}", file=sys.stderr)
        return 1

    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        print(f"\nError: {e}", file=sys.stderr)
        print("\nRun with --verbose flag for detailed error information.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
