"""
Tools package for Multi-Agent Portfolio Collaboration System.

This package contains utility tools for parallel execution, report generation,
suitability scoring, market data retrieval, and other shared functionality.
"""

from src.tools.market_data import (
    StockPrice,
    HistoricalData,
    CompanyInfo,
    DividendData,
    fetch_current_price,
    fetch_historical_data,
    fetch_stock_info,
    fetch_dividend_data,
    fetch_financial_statement,
    fetch_multiple_prices,
    fetch_multiple_stock_info,
    calculate_returns,
    calculate_volatility,
)
from src.tools.parallel_execution import (
    run_compliance_officer_async,
    run_performance_analyst_async,
    run_risk_analyst_async,
    run_specialists_parallel,
    run_specialists_parallel_async,
    run_specialists_parallel_safe,
    run_specialists_parallel_sync,
)
from src.tools.report_generator import (
    format_compliance_section,
    format_performance_section,
    format_risk_section,
    format_suitability_section,
    generate_markdown_report,
    save_report_to_file,
)
from src.tools.suitability_scoring import (
    calculate_compliance_fit_score,
    calculate_performance_fit_score,
    calculate_risk_fit_score,
    calculate_suitability_score,
    calculate_time_horizon_fit_score,
)

__all__ = [
    # Market Data (Models)
    "StockPrice",
    "HistoricalData",
    "CompanyInfo",
    "DividendData",
    # Market Data (Functions)
    "fetch_current_price",
    "fetch_historical_data",
    "fetch_stock_info",
    "fetch_dividend_data",
    "fetch_financial_statement",
    "fetch_multiple_prices",
    "fetch_multiple_stock_info",
    "calculate_returns",
    "calculate_volatility",
    # Parallel Execution
    "run_specialists_parallel",
    "run_specialists_parallel_sync",
    "run_specialists_parallel_async",
    "run_specialists_parallel_safe",
    "run_risk_analyst_async",
    "run_compliance_officer_async",
    "run_performance_analyst_async",
    # Report Generation
    "generate_markdown_report",
    "format_risk_section",
    "format_compliance_section",
    "format_performance_section",
    "format_suitability_section",
    "save_report_to_file",
    # Suitability Scoring
    "calculate_suitability_score",
    "calculate_risk_fit_score",
    "calculate_compliance_fit_score",
    "calculate_performance_fit_score",
    "calculate_time_horizon_fit_score",
]
