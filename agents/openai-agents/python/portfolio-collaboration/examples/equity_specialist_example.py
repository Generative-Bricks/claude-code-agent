"""
Example demonstrating the Equity Specialist Agent functionality.

This script shows how to use the Equity Specialist Agent to perform deep-dive
equity analysis on a portfolio, including sector analysis, valuation metrics,
and growth vs value classification.

Run with:
    python examples/equity_specialist_example.py
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.equity_specialist import perform_equity_deep_dive
from src.data.mock_portfolios import load_client_profile, load_portfolio


def main():
    """
    Demonstrate equity specialist analysis functionality.

    Biblical Principle: EXCELLENCE - Showcasing thorough equity analysis capabilities
    """
    print("=" * 80)
    print("EQUITY SPECIALIST AGENT DEMONSTRATION")
    print("=" * 80)
    print()

    # Load sample data
    print("Loading sample portfolio and client profile...")
    portfolio = load_portfolio("PORT001")
    client = load_client_profile("CLIENT001")

    if not portfolio or not client:
        print("Error: Could not load sample data. Please check examples/ directory.")
        return

    print(f"Portfolio ID: {portfolio.portfolio_id}")
    print(f"Client ID: {client.client_id}")
    print(f"Client Risk Tolerance: {client.risk_tolerance.value}")
    print(f"Total Portfolio Value: ${portfolio.total_value:,.2f}")
    print()

    # Perform equity deep dive analysis
    print("-" * 80)
    print("PERFORMING EQUITY DEEP DIVE ANALYSIS")
    print("-" * 80)
    print()

    focus_areas = [
        "Sector allocation",
        "Valuation metrics",
        "Growth vs Value balance",
        "Risk alignment",
    ]

    questions = [
        "Is the portfolio too concentrated in any sector?",
        "Are valuations reasonable?",
        "Does the growth/value split align with client risk tolerance?",
    ]

    report = perform_equity_deep_dive(
        portfolio=portfolio,
        client_profile=client,
        focus_areas=focus_areas,
        questions=questions,
    )

    # Display results
    print("ANALYSIS RESULTS")
    print("=" * 80)
    print()

    print("Focus Areas Analyzed:")
    for area in report.focus_areas_analyzed:
        print(f"  - {area}")
    print()

    print("SECTOR ANALYSIS:")
    print("-" * 40)
    for sector, analysis in report.sector_analysis.items():
        print(f"\n{sector}:")
        print(f"  {analysis}")
    print()

    print("VALUATION METRICS:")
    print("-" * 40)
    for metric, value in report.valuation_metrics.items():
        if metric == "dividend_yield":
            print(f"  {metric}: {value:.2f}%")
        else:
            print(f"  {metric}: {value:.2f}")
    print()

    print("GROWTH VS VALUE SPLIT:")
    print("-" * 40)
    for category, percentage in report.growth_vs_value_split.items():
        print(f"  {category}: {percentage:.1f}%")
    print()

    print("RECOMMENDATIONS:")
    print("-" * 40)
    for i, rec in enumerate(report.recommendations, 1):
        print(f"{i}. {rec}")
    print()

    print("DETAILED ANALYSIS:")
    print("=" * 80)
    print(report.detailed_analysis)
    print()

    print("=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
