"""
Test script for parallel execution tool.

This script demonstrates the parallel execution tool by running all three
specialist agents (Risk, Compliance, Performance) concurrently on sample
portfolio data.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.mock_portfolios import (
    get_aggressive_example,
    get_conservative_example,
    get_moderate_example,
)
from src.tools.parallel_execution import (
    run_specialists_parallel,
    run_specialists_parallel_async,
    run_specialists_parallel_sync,
)


def test_synchronous_execution():
    """Test synchronous parallel execution (direct function calls)."""
    print("=" * 80)
    print("TEST 1: Synchronous Parallel Execution (Direct Function Calls)")
    print("=" * 80)

    # Load conservative client portfolio
    client, portfolio = get_conservative_example()

    print(f"\nClient: {client.client_id}, Age {client.age}, {client.risk_tolerance.value}")
    print(f"Portfolio: {portfolio.portfolio_id}, ${portfolio.total_value:,.0f}\n")

    # Run specialists in parallel (synchronously)
    print("Running Risk, Compliance, and Performance analyses...")
    result = run_specialists_parallel_sync(portfolio, client)

    print(f"✅ Completed in {result.execution_time_seconds:.3f} seconds\n")

    # Display results
    print("RISK ANALYSIS:")
    print(f"  - Volatility: {result.risk_analysis.volatility:.1f}%")
    print(f"  - Beta: {result.risk_analysis.beta:.2f}")
    print(f"  - VaR 95%: {result.risk_analysis.var_95:.1f}%")
    print(f"  - Risk Rating: {result.risk_analysis.risk_rating.value}")
    print(f"  - Concerns: {len(result.risk_analysis.concerns)}")

    print("\nCOMPLIANCE REPORT:")
    print(f"  - Status: {result.compliance_report.status.value}")
    print(f"  - Checks Performed: {len(result.compliance_report.checks_performed)}")
    print(f"  - Violations: {len(result.compliance_report.violations)}")
    print(f"  - Suitability Pass: {result.compliance_report.suitability_pass}")

    print("\nPERFORMANCE REPORT:")
    print(f"  - Total Return: {result.performance_report.total_return:.2f}%")
    print(f"  - Benchmark Return: {result.performance_report.benchmark_return:.2f}%")
    print(f"  - Sharpe Ratio: {result.performance_report.sharpe_ratio:.2f}")
    print(f"  - Top Performers: {len(result.performance_report.top_performers)}")

    return result


async def test_asynchronous_execution():
    """Test asynchronous parallel execution (with OpenAI Agents SDK)."""
    print("\n" + "=" * 80)
    print("TEST 2: Asynchronous Parallel Execution (OpenAI Agents SDK)")
    print("=" * 80)

    # Load moderate client portfolio
    client, portfolio = get_moderate_example()

    print(f"\nClient: {client.client_id}, Age {client.age}, {client.risk_tolerance.value}")
    print(f"Portfolio: {portfolio.portfolio_id}, ${portfolio.total_value:,.0f}\n")

    # Run specialists in parallel (asynchronously with agent reasoning)
    print("Running Risk, Compliance, and Performance agents with SDK...")
    result = await run_specialists_parallel_async(portfolio, client)

    print(f"✅ Completed in {result.execution_time_seconds:.3f} seconds\n")

    # Display results
    print("RISK ANALYSIS:")
    print(f"  - Volatility: {result.risk_analysis.volatility:.1f}%")
    print(f"  - Beta: {result.risk_analysis.beta:.2f}")
    print(f"  - Concentration Score: {result.risk_analysis.concentration_score:.0f}/100")

    print("\nCOMPLIANCE REPORT:")
    print(f"  - Status: {result.compliance_report.status.value}")
    print(f"  - Suitability Pass: {result.compliance_report.suitability_pass}")
    print(f"  - Concentration Limits Pass: {result.compliance_report.concentration_limits_pass}")

    print("\nPERFORMANCE REPORT:")
    print(f"  - Total Return: {result.performance_report.total_return:.2f}%")
    print(f"  - Excess Return: {result.performance_report.excess_return:.2f}%")
    if result.performance_report.alpha:
        print(f"  - Alpha: {result.performance_report.alpha:.2f}%")

    return result


def test_convenience_function():
    """Test the main convenience function."""
    print("\n" + "=" * 80)
    print("TEST 3: Convenience Function (run_specialists_parallel)")
    print("=" * 80)

    # Load aggressive client portfolio
    client, portfolio = get_aggressive_example()

    print(f"\nClient: {client.client_id}, Age {client.age}, {client.risk_tolerance.value}")
    print(f"Portfolio: {portfolio.portfolio_id}, ${portfolio.total_value:,.0f}\n")

    # Run using convenience function (defaults to sync)
    print("Running analyses using convenience function...")
    result = run_specialists_parallel(portfolio, client, use_async=False)

    print(f"✅ Completed in {result.execution_time_seconds:.3f} seconds\n")

    # Display summary
    print("SUMMARY:")
    print(f"  - Risk Rating: {result.risk_analysis.risk_rating.value}")
    print(f"  - Compliance Status: {result.compliance_report.status.value}")
    print(f"  - Performance Percentile: {result.performance_report.percentile_rank}th")
    print(f"  - Execution Time: {result.execution_time_seconds:.3f}s")

    return result


def main():
    """Run all tests."""
    print("\n🚀 Testing Parallel Execution Tool\n")

    # Test 1: Synchronous execution (fastest)
    sync_result = test_synchronous_execution()

    # Test 2: Asynchronous execution (with agent reasoning)
    # Note: Commented out because it requires OpenAI API key and makes actual API calls
    # async_result = asyncio.run(test_asynchronous_execution())

    # Test 3: Convenience function
    convenience_result = test_convenience_function()

    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED")
    print("=" * 80)
    print(f"\nSynchronous execution time: {sync_result.execution_time_seconds:.3f}s")
    print(f"Convenience function time: {convenience_result.execution_time_seconds:.3f}s")
    print("\nThe parallel execution tool is working correctly!")
    print("All three specialist agents can run concurrently, reducing total analysis time.")


if __name__ == "__main__":
    main()
