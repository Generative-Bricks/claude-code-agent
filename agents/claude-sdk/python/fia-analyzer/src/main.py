#!/usr/bin/env python3
"""
FIA Analyzer - Main Entry Point

Command-line interface for the FIA Analyzer agent.

Usage:
    # Analyze a product without client profile
    python src/main.py --product "Allianz Benefit Control"

    # Analyze with carrier filter
    python src/main.py --product "Nationwide Peak 10" --carrier "Nationwide"

    # Analyze with client suitability analysis
    python src/main.py --product "Allianz 222" --client-profile examples/sample_client.json

Biblical Principle: SERVE - Simple, clear interface that makes the agent easy to use
"""

import argparse
import json
import sys
import logging
from pathlib import Path
from typing import Optional

from src.agent import FIAAnalyzerAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_client_profile(file_path: str) -> dict:
    """
    Load client profile from JSON file.

    Args:
        file_path: Path to client profile JSON file

    Returns:
        Dictionary containing client profile data

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If JSON is invalid
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Client profile file not found: {file_path}")

    try:
        with open(path, 'r') as f:
            profile = json.load(f)
        logger.info(f"Loaded client profile from: {file_path}")
        return profile
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in client profile file: {e}")


def print_results(results: dict):
    """
    Print analysis results in a readable format.

    Args:
        results: Results dictionary from FIAAnalyzerAgent.analyze_product()
    """
    print("\n" + "=" * 80)
    print("FIA ANALYZER RESULTS")
    print("=" * 80)

    # Product information
    print(f"\nProduct: {results['product_name']}")
    if results.get('carrier'):
        print(f"Carrier: {results['carrier']}")

    # Search results
    if results.get('search_results'):
        print("\n--- SEARCH RESULTS ---")
        products = results['search_results'].get('products', [])
        if products:
            for idx, product in enumerate(products, 1):
                print(f"\n{idx}. {product['name']}")
                print(f"   Carrier: {product['carrier']}")
                print(f"   URL: {product['url']}")
                print(f"   Summary: {product['summary']}")
        else:
            print("No products found in search.")

    # Product data
    if results.get('product_data'):
        print("\n--- PRODUCT DETAILS ---")
        product = results['product_data']
        print(f"Product Type: {product.get('product_type', 'N/A')}")
        print(f"Contract Term: {product.get('contract_term', 'N/A')} years")
        print(f"Minimum Premium: ${product.get('minimum_premium', 0):,.0f}")

        # Surrender charges
        if product.get('surrender_charges'):
            print("\nSurrender Charges:")
            for charge in product['surrender_charges']:
                print(f"  Year {charge['year']}: {charge['percentage']}%")

        # Current rates
        if product.get('current_rates'):
            print("\nCurrent Rates:")
            for rate in product['current_rates']:
                print(f"  {rate['index_name']} - {rate['crediting_method']}")
                if rate.get('cap_rate'):
                    print(f"    Cap Rate: {rate['cap_rate']}%")
                if rate.get('participation_rate'):
                    print(f"    Participation Rate: {rate['participation_rate']}%")

        # Index options
        if product.get('index_options'):
            print("\nIndex Options:")
            for idx_option in product['index_options']:
                print(f"  - {idx_option['name']}: {idx_option['description']}")

        # Riders
        if product.get('riders'):
            print("\nAvailable Riders:")
            for rider in product['riders']:
                print(f"  - {rider['name']}")
                if rider.get('description'):
                    print(f"    {rider['description']}")

    # Suitability analysis
    if results.get('suitability_analysis'):
        print("\n--- SUITABILITY ANALYSIS ---")
        analysis = results['suitability_analysis']

        print(f"\nSuitability Score: {analysis['score']}%")
        print(f"Interpretation: {analysis['interpretation']}")
        print(f"Total Questions: {analysis['total_yes'] + analysis['total_no'] + analysis['total_na']}")
        print(f"  YES: {analysis['total_yes']}")
        print(f"  NO: {analysis['total_no']}")
        print(f"  N/A: {analysis['total_na']}")

        # Good fit factors
        if analysis.get('good_fit_factors'):
            print("\nGood Fit Factors:")
            for factor in analysis['good_fit_factors']:
                print(f"  ✓ {factor}")

        # Concerns
        if analysis.get('not_a_fit_factors'):
            print("\nConcerns:")
            for concern in analysis['not_a_fit_factors']:
                print(f"  ✗ {concern}")

        # Recommendations
        if analysis.get('recommendations'):
            print("\nRecommendations:")
            for rec in analysis['recommendations']:
                print(f"  → {rec}")

    # Summary
    print("\n--- SUMMARY ---")
    print(f"Total conversation turns: {results.get('total_turns', 'N/A')}")
    print(f"Product data extracted: {'Yes' if results.get('product_data') else 'No'}")
    print(f"Suitability analysis performed: {'Yes' if results.get('suitability_analysis') else 'No'}")

    print("\n" + "=" * 80)


def main():
    """
    Main entry point for FIA Analyzer CLI.

    Parses command-line arguments and runs the agent analysis.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="Analyze Fixed Indexed Annuity products using Claude AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a product
  python src/main.py --product "Allianz Benefit Control"

  # Analyze with carrier filter
  python src/main.py --product "Nationwide Peak 10" --carrier "Nationwide"

  # Analyze with client profile
  python src/main.py --product "Allianz 222" --client-profile examples/sample_client.json

  # Save results to JSON file
  python src/main.py --product "Allianz Benefit Control" --output results.json
        """
    )

    parser.add_argument(
        "--product",
        required=True,
        help="Product name to analyze (e.g., 'Allianz Benefit Control')"
    )

    parser.add_argument(
        "--carrier",
        help="Optional carrier name to filter search (e.g., 'Allianz Life')"
    )

    parser.add_argument(
        "--client-profile",
        help="Path to client profile JSON file for suitability analysis"
    )

    parser.add_argument(
        "--output",
        help="Optional path to save results as JSON"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging (DEBUG level)"
    )

    args = parser.parse_args()

    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")

    try:
        # Load client profile if provided
        client_profile = None
        if args.client_profile:
            try:
                client_profile = load_client_profile(args.client_profile)
            except Exception as e:
                logger.error(f"Failed to load client profile: {e}")
                print(f"\nError: {e}", file=sys.stderr)
                return 1

        # Initialize agent
        logger.info("Initializing FIA Analyzer Agent...")
        agent = FIAAnalyzerAgent()

        # Run analysis
        logger.info(f"Analyzing product: {args.product}")
        results = agent.analyze_product(
            product_name=args.product,
            carrier=args.carrier,
            client_profile_dict=client_profile
        )

        # Print results to console
        print_results(results)

        # Save to JSON if requested
        if args.output:
            output_path = Path(args.output)
            try:
                with open(output_path, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                logger.info(f"Results saved to: {args.output}")
                print(f"\nResults saved to: {args.output}")
            except Exception as e:
                logger.error(f"Failed to save results: {e}")
                print(f"\nWarning: Could not save results to file: {e}", file=sys.stderr)

        return 0

    except KeyboardInterrupt:
        logger.info("Analysis interrupted by user")
        print("\n\nAnalysis interrupted by user.", file=sys.stderr)
        return 1

    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        print(f"\nError: {e}", file=sys.stderr)
        print("\nRun with --verbose flag for detailed error information.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
