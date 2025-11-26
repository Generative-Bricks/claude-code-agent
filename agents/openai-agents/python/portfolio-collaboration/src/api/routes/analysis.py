"""
Analysis API Routes for Portfolio Collaboration System.

Provides REST endpoints for portfolio analysis, data listing, and comparison.

Biblical Principle: SERVE - Simple, accessible API for powerful analysis.
Biblical Principle: EXCELLENCE - Production-grade error handling and logging.
"""

import asyncio
import logging
import time
import uuid
from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from src.api.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    ClientListResponse,
    ClientSummary,
    ComparisonRequest,
    ComparisonResponse,
    ComparisonResult,
    ErrorResponse,
    PortfolioListResponse,
    PortfolioSummary,
)
from src.agents.portfolio_manager import do_comprehensive_analysis
from src.main import load_client_profiles, load_portfolios, get_portfolio_by_name
from src.models.schemas import Portfolio

logger = logging.getLogger(__name__)
router = APIRouter()


# ============================================================================
# Analysis Endpoint
# ============================================================================


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_portfolio(request: AnalysisRequest):
    """
    Run comprehensive portfolio analysis for a client.

    Uses the existing do_comprehensive_analysis function from
    portfolio_manager.py to run all specialists in parallel.

    Biblical Principle: TRUTH - Transparent, comprehensive analysis.
    Biblical Principle: EXCELLENCE - Production-ready error handling.

    Args:
        request: AnalysisRequest with client_profile and portfolio

    Returns:
        AnalysisResponse with complete recommendations and metrics

    Raises:
        HTTPException: If analysis fails
    """
    # Generate unique analysis ID
    analysis_id = f"ANLYS-{datetime.now().strftime('%Y-%m-%d')}-{str(uuid.uuid4())[:8].upper()}"

    logger.info(f"Starting analysis {analysis_id}")
    logger.info(f"  Client: {request.client_profile.client_id}")
    logger.info(f"  Portfolio: {request.portfolio.portfolio_id}")

    start_time = time.time()

    try:
        # Run comprehensive analysis using callable tool
        # Biblical Principle: SERVE - Leveraging existing analysis infrastructure
        recommendations = do_comprehensive_analysis(
            request.portfolio, request.client_profile
        )

        execution_time = time.time() - start_time

        logger.info(f"✓ Analysis {analysis_id} complete in {execution_time:.2f}s")
        logger.info(
            f"  Suitability Score: {recommendations.suitability_score.overall_score:.1f}/100"
        )

        return AnalysisResponse(
            success=True,
            recommendations=recommendations,
            analysis_id=analysis_id,
            timestamp=datetime.now(),
            execution_time_seconds=execution_time,
        )

    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Analysis {analysis_id} failed after {execution_time:.2f}s: {e}")
        logger.error(f"Error details:", exc_info=True)

        # Biblical Principle: TRUTH - Honest error reporting
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "AnalysisError",
                "message": f"Portfolio analysis failed: {str(e)}",
                "type": "ANALYSIS_FAILED",
                "analysis_id": analysis_id,
                "timestamp": datetime.now().isoformat(),
            },
        )


# ============================================================================
# Client Listing Endpoint
# ============================================================================


@router.get("/clients", response_model=ClientListResponse)
async def list_clients():
    """
    List all available client profiles from examples/sample_clients.json.

    Returns lightweight ClientSummary objects.

    Biblical Principle: SERVE - Easy discovery of available data.

    Returns:
        ClientListResponse with list of client summaries

    Raises:
        HTTPException: If clients cannot be loaded
    """
    logger.info("Fetching client list")

    try:
        # Load all client profiles
        clients_dict = load_client_profiles()

        if not clients_dict:
            logger.warning("No clients found in sample data")
            return ClientListResponse(clients=[], total=0)

        # Convert to ClientSummary objects
        # Biblical Principle: EXCELLENCE - Lightweight summaries for listing
        client_summaries = [
            ClientSummary.from_client_profile(profile)
            for profile in clients_dict.values()
        ]

        logger.info(f"✓ Loaded {len(client_summaries)} clients")

        return ClientListResponse(clients=client_summaries, total=len(client_summaries))

    except Exception as e:
        logger.error(f"Failed to load clients: {e}", exc_info=True)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "DataLoadError",
                "message": f"Failed to load client profiles: {str(e)}",
                "type": "DATA_LOAD_FAILED",
                "timestamp": datetime.now().isoformat(),
            },
        )


# ============================================================================
# Portfolio Listing Endpoint
# ============================================================================


@router.get("/portfolios", response_model=PortfolioListResponse)
async def list_portfolios():
    """
    List all available portfolios from examples/sample_portfolios.json.

    Returns lightweight PortfolioSummary objects.

    Biblical Principle: SERVE - Easy discovery of available portfolios.

    Returns:
        PortfolioListResponse with list of portfolio summaries

    Raises:
        HTTPException: If portfolios cannot be loaded
    """
    logger.info("Fetching portfolio list")

    try:
        # Load all portfolios
        portfolios_dict = load_portfolios()

        if not portfolios_dict:
            logger.warning("No portfolios found in sample data")
            return PortfolioListResponse(portfolios=[], total=0)

        # Convert to PortfolioSummary objects
        # Biblical Principle: EXCELLENCE - Lightweight summaries for listing
        portfolio_summaries = [
            PortfolioSummary.from_portfolio(portfolio)
            for portfolio in portfolios_dict.values()
        ]

        logger.info(f"✓ Loaded {len(portfolio_summaries)} portfolios")

        return PortfolioListResponse(
            portfolios=portfolio_summaries, total=len(portfolio_summaries)
        )

    except Exception as e:
        logger.error(f"Failed to load portfolios: {e}", exc_info=True)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "DataLoadError",
                "message": f"Failed to load portfolios: {str(e)}",
                "type": "DATA_LOAD_FAILED",
                "timestamp": datetime.now().isoformat(),
            },
        )


# ============================================================================
# Portfolio Comparison Endpoint
# ============================================================================


@router.post("/compare", response_model=ComparisonResponse)
async def compare_portfolios(request: ComparisonRequest):
    """
    Compare multiple portfolios for a client.

    Runs analysis on each portfolio in parallel and ranks by suitability.

    Biblical Principle: EXCELLENCE - Comprehensive comparison for informed decisions.
    Biblical Principle: PERSEVERE - Parallel execution for efficient processing.

    Args:
        request: ComparisonRequest with client_profile and portfolio_ids

    Returns:
        ComparisonResponse with sorted results and best fit recommendation

    Raises:
        HTTPException: If portfolios not found or comparison fails
    """
    # Generate unique comparison ID
    comparison_id = f"CMP-{datetime.now().strftime('%Y-%m-%d')}-{str(uuid.uuid4())[:8].upper()}"

    logger.info(f"Starting comparison {comparison_id}")
    logger.info(f"  Client: {request.client_profile.client_id}")
    logger.info(f"  Portfolios: {len(request.portfolio_ids)}")

    start_time = time.time()

    try:
        # Load all requested portfolios
        # Biblical Principle: TRUTH - Validate all inputs before processing
        portfolios_dict = load_portfolios()
        portfolios_to_compare: List[Portfolio] = []

        for portfolio_id in request.portfolio_ids:
            portfolio = portfolios_dict.get(portfolio_id)
            if not portfolio:
                logger.error(f"Portfolio {portfolio_id} not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "error": "PortfolioNotFound",
                        "message": f"Portfolio '{portfolio_id}' not found",
                        "type": "PORTFOLIO_NOT_FOUND",
                        "portfolio_id": portfolio_id,
                        "timestamp": datetime.now().isoformat(),
                    },
                )
            portfolios_to_compare.append(portfolio)

        logger.info(f"✓ Loaded {len(portfolios_to_compare)} portfolios")

        # Run analysis for each portfolio in parallel
        # Biblical Principle: PERSEVERE - Efficient parallel processing
        logger.info("Running parallel analysis on all portfolios...")

        async def analyze_single_portfolio(portfolio: Portfolio):
            """Helper to analyze a single portfolio asynchronously."""
            try:
                # Run analysis in thread pool to avoid blocking
                loop = asyncio.get_event_loop()
                recommendations = await loop.run_in_executor(
                    None,
                    do_comprehensive_analysis,
                    portfolio,
                    request.client_profile,
                )
                return portfolio.portfolio_id, recommendations, None
            except Exception as e:
                logger.error(
                    f"Analysis failed for portfolio {portfolio.portfolio_id}: {e}"
                )
                return portfolio.portfolio_id, None, str(e)

        # Execute all analyses in parallel
        analysis_results = await asyncio.gather(
            *[analyze_single_portfolio(p) for p in portfolios_to_compare]
        )

        # Process results and check for errors
        comparison_results: List[ComparisonResult] = []
        errors = []

        for portfolio_id, recommendations, error in analysis_results:
            if error:
                errors.append(f"Portfolio {portfolio_id}: {error}")
                continue

            if recommendations:
                comparison_results.append(
                    ComparisonResult(
                        portfolio_id=portfolio_id,
                        recommendations=recommendations,
                        suitability_score=recommendations.suitability_score.overall_score,
                        suitability_rating=recommendations.suitability_score.interpretation.value,
                    )
                )

        # Check if any analyses succeeded
        if not comparison_results:
            error_msg = "; ".join(errors)
            logger.error(f"All portfolio analyses failed: {error_msg}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "ComparisonError",
                    "message": f"All portfolio analyses failed: {error_msg}",
                    "type": "ALL_ANALYSES_FAILED",
                    "comparison_id": comparison_id,
                    "timestamp": datetime.now().isoformat(),
                },
            )

        # Sort results by suitability score (descending)
        # Biblical Principle: SERVE - Clear ranking for easy decision-making
        comparison_results.sort(key=lambda x: x.suitability_score, reverse=True)

        # Identify best fit portfolio
        best_fit_portfolio_id = comparison_results[0].portfolio_id

        execution_time = time.time() - start_time

        logger.info(f"✓ Comparison {comparison_id} complete in {execution_time:.2f}s")
        logger.info(f"  Best fit: {best_fit_portfolio_id}")
        logger.info(
            f"  Score: {comparison_results[0].suitability_score:.1f}/100 ({comparison_results[0].suitability_rating})"
        )

        if errors:
            logger.warning(f"  Partial results: {len(errors)} portfolio(s) failed")

        return ComparisonResponse(
            success=True,
            results=comparison_results,
            best_fit_portfolio_id=best_fit_portfolio_id,
            comparison_id=comparison_id,
            timestamp=datetime.now(),
            execution_time_seconds=execution_time,
        )

    except HTTPException:
        # Re-raise HTTP exceptions (already properly formatted)
        raise

    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Comparison {comparison_id} failed after {execution_time:.2f}s: {e}")
        logger.error("Error details:", exc_info=True)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "ComparisonError",
                "message": f"Portfolio comparison failed: {str(e)}",
                "type": "COMPARISON_FAILED",
                "comparison_id": comparison_id,
                "timestamp": datetime.now().isoformat(),
            },
        )


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    "router",
    "analyze_portfolio",
    "list_clients",
    "list_portfolios",
    "compare_portfolios",
]
