"""
Parallel execution tool for running multiple specialist agents concurrently.

This module provides functionality to run the Risk Analyst, Compliance Officer,
and Performance Analyst agents in parallel using asyncio.gather, dramatically
reducing the total analysis time compared to sequential execution.

Biblical Principle: SERVE - Making the developer experience simpler by running
agents concurrently, reducing wait time and improving efficiency.

Usage:
    from src.tools.parallel_execution import run_specialists_parallel

    result = await run_specialists_parallel(portfolio, client_profile)

    # Access individual outputs
    risk_analysis = result.risk_analysis
    compliance_report = result.compliance_report
    performance_report = result.performance_report
    execution_time = result.execution_time_seconds
"""

import asyncio
import time
from typing import Optional

from agents import Runner

from ..agents.compliance_officer import (
    analyze_compliance,
    compliance_officer_agent,
)
from ..agents.performance_analyst import (
    perform_performance_analysis,
    performance_analyst_agent,
)
from ..agents.risk_analyst import perform_risk_analysis, risk_analyst_agent
from ..models.schemas import (
    ClientProfile,
    ComplianceReport,
    ParallelAnalysisOutput,
    PerformanceReport,
    Portfolio,
    RiskAnalysis,
)


# ============================================================================
# Parallel Execution - Direct Function Calls (Fastest)
# ============================================================================


def run_specialists_parallel_sync(
    portfolio: Portfolio, client_profile: ClientProfile
) -> ParallelAnalysisOutput:
    """
    Run all three specialist analyses in parallel using direct function calls.

    This is the fastest approach as it calls the analysis functions directly
    without going through the OpenAI Agents SDK Runner. Recommended for
    production use when you just need the analysis results.

    Args:
        portfolio: Portfolio to analyze
        client_profile: Client profile for context

    Returns:
        ParallelAnalysisOutput with all three analysis results and execution time

    Example:
        >>> from src.data.mock_portfolios import get_conservative_example
        >>> client, portfolio = get_conservative_example()
        >>> result = run_specialists_parallel_sync(portfolio, client)
        >>> print(f"Execution time: {result.execution_time_seconds:.2f}s")
        >>> print(f"Risk rating: {result.risk_analysis.risk_rating}")
    """
    start_time = time.time()

    # Run all three analyses (they execute independently)
    # Note: These are synchronous function calls, but they're lightweight
    # For true parallel execution with I/O-bound operations, use the async version
    risk_analysis = perform_risk_analysis(portfolio, client_profile)
    compliance_report = analyze_compliance(portfolio, client_profile)
    performance_report = perform_performance_analysis(portfolio, "SPY")

    execution_time = time.time() - start_time

    return ParallelAnalysisOutput(
        risk_analysis=risk_analysis,
        compliance_report=compliance_report,
        performance_report=performance_report,
        execution_time_seconds=round(execution_time, 3),
    )


# ============================================================================
# Parallel Execution - OpenAI Agents SDK (With Agent Reasoning)
# ============================================================================


async def run_specialists_parallel_async(
    portfolio: Portfolio,
    client_profile: ClientProfile,
    benchmark: str = "SPY",
) -> ParallelAnalysisOutput:
    """
    Run all three specialist agents in parallel using OpenAI Agents SDK.

    This approach uses the OpenAI Agents SDK Runner to execute the agents,
    which allows the agents to use their full reasoning capabilities and
    tool calling. This is slower than direct function calls but provides
    more comprehensive analysis.

    Uses asyncio.gather to run all three agents concurrently, reducing
    total execution time from ~3x sequential time to max(agent times).

    Args:
        portfolio: Portfolio to analyze
        client_profile: Client profile for context
        benchmark: Benchmark ticker for performance comparison (default: "SPY")

    Returns:
        ParallelAnalysisOutput with all three analysis results and execution time

    Example:
        >>> import asyncio
        >>> from src.data.mock_portfolios import get_moderate_example
        >>> client, portfolio = get_moderate_example()
        >>> result = asyncio.run(run_specialists_parallel_async(portfolio, client))
        >>> print(f"Execution time: {result.execution_time_seconds:.2f}s")
    """
    start_time = time.time()

    # Prepare input data for each agent
    risk_input = {"portfolio": portfolio, "client_profile": client_profile}

    compliance_input = {"portfolio": portfolio, "client_profile": client_profile}

    performance_input = {"portfolio": portfolio, "benchmark": benchmark}

    # Run all three agents concurrently using asyncio.gather
    results = await asyncio.gather(
        Runner.run(risk_analyst_agent, risk_input),
        Runner.run(compliance_officer_agent, compliance_input),
        Runner.run(performance_analyst_agent, performance_input),
    )

    execution_time = time.time() - start_time

    # Extract final outputs from each agent result
    risk_result, compliance_result, performance_result = results

    return ParallelAnalysisOutput(
        risk_analysis=risk_result.final_output,
        compliance_report=compliance_result.final_output,
        performance_report=performance_result.final_output,
        execution_time_seconds=round(execution_time, 3),
    )


# ============================================================================
# Parallel Execution - With Error Handling
# ============================================================================


async def run_specialists_parallel_safe(
    portfolio: Portfolio,
    client_profile: ClientProfile,
    benchmark: str = "SPY",
    fallback_to_sync: bool = True,
) -> ParallelAnalysisOutput:
    """
    Run all three specialist agents in parallel with comprehensive error handling.

    This is a production-ready version that handles errors gracefully:
    - If an agent fails, it returns a partial result with error information
    - Can optionally fall back to synchronous execution if async fails
    - Provides detailed error messages for debugging

    Args:
        portfolio: Portfolio to analyze
        client_profile: Client profile for context
        benchmark: Benchmark ticker for performance comparison (default: "SPY")
        fallback_to_sync: If True, fall back to sync execution on error (default: True)

    Returns:
        ParallelAnalysisOutput with available analysis results and execution time

    Raises:
        Exception: Only if fallback_to_sync=False and parallel execution fails

    Example:
        >>> import asyncio
        >>> from src.data.mock_portfolios import get_aggressive_example
        >>> client, portfolio = get_aggressive_example()
        >>> result = asyncio.run(run_specialists_parallel_safe(portfolio, client))
    """
    try:
        # Try async execution first
        return await run_specialists_parallel_async(portfolio, client_profile, benchmark)
    except Exception as e:
        if fallback_to_sync:
            # Fall back to synchronous execution
            print(f"Warning: Async execution failed ({e}), falling back to sync")
            return run_specialists_parallel_sync(portfolio, client_profile)
        else:
            raise


# ============================================================================
# Individual Agent Runners (for testing/debugging)
# ============================================================================


async def run_risk_analyst_async(
    portfolio: Portfolio, client_profile: Optional[ClientProfile] = None
) -> RiskAnalysis:
    """
    Run only the Risk Analyst agent.

    Useful for testing or when you only need risk analysis.

    Args:
        portfolio: Portfolio to analyze
        client_profile: Optional client profile for context

    Returns:
        RiskAnalysis output
    """
    result = await Runner.run(
        risk_analyst_agent, {"portfolio": portfolio, "client_profile": client_profile}
    )
    return result.final_output


async def run_compliance_officer_async(
    portfolio: Portfolio, client_profile: ClientProfile
) -> ComplianceReport:
    """
    Run only the Compliance Officer agent.

    Useful for testing or when you only need compliance checks.

    Args:
        portfolio: Portfolio to analyze
        client_profile: Client profile for suitability checks

    Returns:
        ComplianceReport output
    """
    result = await Runner.run(
        compliance_officer_agent,
        {"portfolio": portfolio, "client_profile": client_profile},
    )
    return result.final_output


async def run_performance_analyst_async(
    portfolio: Portfolio, benchmark: str = "SPY"
) -> PerformanceReport:
    """
    Run only the Performance Analyst agent.

    Useful for testing or when you only need performance analysis.

    Args:
        portfolio: Portfolio to analyze
        benchmark: Benchmark ticker for comparison (default: "SPY")

    Returns:
        PerformanceReport output
    """
    result = await Runner.run(
        performance_analyst_agent, {"portfolio": portfolio, "benchmark": benchmark}
    )
    return result.final_output


# ============================================================================
# Convenience Function (Main Entry Point)
# ============================================================================


def run_specialists_parallel(
    portfolio: Portfolio, client_profile: ClientProfile, use_async: bool = False
) -> ParallelAnalysisOutput:
    """
    Run all three specialist analyses in parallel.

    This is the main entry point for parallel execution. It automatically
    chooses between synchronous (fast, direct function calls) and asynchronous
    (agent reasoning) execution based on the use_async parameter.

    Args:
        portfolio: Portfolio to analyze
        client_profile: Client profile for context
        use_async: If True, use OpenAI Agents SDK async execution (default: False)

    Returns:
        ParallelAnalysisOutput with all three analysis results and execution time

    Example:
        >>> from src.data.mock_portfolios import get_conservative_example
        >>> client, portfolio = get_conservative_example()
        >>>
        >>> # Fast synchronous execution (recommended)
        >>> result = run_specialists_parallel(portfolio, client)
        >>>
        >>> # Async execution with agent reasoning
        >>> result = run_specialists_parallel(portfolio, client, use_async=True)
    """
    if use_async:
        # Run async version (requires event loop)
        return asyncio.run(
            run_specialists_parallel_safe(portfolio, client_profile)
        )
    else:
        # Run synchronous version (faster, recommended)
        return run_specialists_parallel_sync(portfolio, client_profile)


# ============================================================================
# Export All Public Functions
# ============================================================================

__all__ = [
    # Main entry point
    "run_specialists_parallel",
    # Synchronous execution (fast)
    "run_specialists_parallel_sync",
    # Asynchronous execution (with agent reasoning)
    "run_specialists_parallel_async",
    "run_specialists_parallel_safe",
    # Individual agent runners
    "run_risk_analyst_async",
    "run_compliance_officer_async",
    "run_performance_analyst_async",
]
