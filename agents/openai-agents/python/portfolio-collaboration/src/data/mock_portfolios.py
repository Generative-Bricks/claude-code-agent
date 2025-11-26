"""
Mock portfolio and client data for testing multi-agent workflows.

This module provides helper functions to load sample data from JSON files
and convert them to Pydantic models for use in agent testing and development.

Biblical Principle: SERVE - Providing easy access to test data simplifies development.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from src.models import ClientProfile, Portfolio, PortfolioHolding


# ============================================================================
# Path Configuration
# ============================================================================

# Get the root directory of the project
PROJECT_ROOT = Path(__file__).parent.parent.parent
EXAMPLES_DIR = PROJECT_ROOT / "examples"

CLIENTS_FILE = EXAMPLES_DIR / "sample_clients.json"
PORTFOLIOS_FILE = EXAMPLES_DIR / "sample_portfolios.json"


# ============================================================================
# Data Loading Functions
# ============================================================================


def load_client_profiles() -> Dict[str, ClientProfile]:
    """
    Load all sample client profiles from JSON.

    Returns:
        Dictionary mapping client_id to ClientProfile model

    Raises:
        FileNotFoundError: If sample_clients.json doesn't exist
        ValueError: If JSON is invalid or doesn't match schema
    """
    if not CLIENTS_FILE.exists():
        raise FileNotFoundError(f"Sample clients file not found: {CLIENTS_FILE}")

    with open(CLIENTS_FILE, "r") as f:
        data = json.load(f)

    clients = {}
    for client_data in data["clients"]:
        client = ClientProfile(**client_data)
        clients[client.client_id] = client

    return clients


def load_client_profile(client_id: str) -> Optional[ClientProfile]:
    """
    Load a specific client profile by ID.

    Args:
        client_id: Client identifier (e.g., "CLIENT001")

    Returns:
        ClientProfile model or None if not found
    """
    clients = load_client_profiles()
    return clients.get(client_id)


def load_portfolios() -> Dict[str, Portfolio]:
    """
    Load all sample portfolios from JSON.

    Returns:
        Dictionary mapping portfolio_id to Portfolio model

    Raises:
        FileNotFoundError: If sample_portfolios.json doesn't exist
        ValueError: If JSON is invalid or doesn't match schema
    """
    if not PORTFOLIOS_FILE.exists():
        raise FileNotFoundError(f"Sample portfolios file not found: {PORTFOLIOS_FILE}")

    with open(PORTFOLIOS_FILE, "r") as f:
        data = json.load(f)

    portfolios = {}
    for portfolio_data in data["portfolios"]:
        # Convert holdings to PortfolioHolding models
        holdings = [
            PortfolioHolding(**holding) for holding in portfolio_data["holdings"]
        ]

        # Convert as_of_date string to datetime
        as_of_date = datetime.fromisoformat(
            portfolio_data["as_of_date"].replace("Z", "+00:00")
        )

        # Create Portfolio model
        portfolio = Portfolio(
            portfolio_id=portfolio_data["portfolio_id"],
            client_id=portfolio_data["client_id"],
            holdings=holdings,
            total_value=portfolio_data["total_value"],
            benchmark=portfolio_data["benchmark"],
            as_of_date=as_of_date,
        )

        portfolios[portfolio.portfolio_id] = portfolio

    return portfolios


def load_portfolio(portfolio_id: str) -> Optional[Portfolio]:
    """
    Load a specific portfolio by ID.

    Args:
        portfolio_id: Portfolio identifier (e.g., "PORT001")

    Returns:
        Portfolio model or None if not found
    """
    portfolios = load_portfolios()
    return portfolios.get(portfolio_id)


def load_client_portfolio_pair(
    client_id: str,
) -> Optional[tuple[ClientProfile, Portfolio]]:
    """
    Load a matching client profile and portfolio pair.

    Args:
        client_id: Client identifier (e.g., "CLIENT001")

    Returns:
        Tuple of (ClientProfile, Portfolio) or None if not found
    """
    client = load_client_profile(client_id)
    if not client:
        return None

    # Find the portfolio associated with this client
    portfolios = load_portfolios()
    portfolio = None
    for p in portfolios.values():
        if p.client_id == client_id:
            portfolio = p
            break

    if not portfolio:
        return None

    return (client, portfolio)


# ============================================================================
# Convenience Functions
# ============================================================================


def get_all_tickers() -> List[str]:
    """
    Get a list of all unique tickers across all portfolios.

    Returns:
        List of ticker symbols
    """
    portfolios = load_portfolios()
    tickers = set()

    for portfolio in portfolios.values():
        for holding in portfolio.holdings:
            tickers.add(holding.ticker)

    return sorted(list(tickers))


def get_portfolio_summary(portfolio_id: str) -> Dict:
    """
    Get a summary of a portfolio's composition.

    Args:
        portfolio_id: Portfolio identifier

    Returns:
        Dictionary with asset class breakdown and sector allocation
    """
    portfolio = load_portfolio(portfolio_id)
    if not portfolio:
        return {}

    # Calculate asset class breakdown
    asset_class_breakdown = {}
    sector_breakdown = {}

    for holding in portfolio.holdings:
        # Asset class
        asset_class = holding.asset_class.value
        if asset_class not in asset_class_breakdown:
            asset_class_breakdown[asset_class] = 0
        asset_class_breakdown[asset_class] += holding.market_value

        # Sector
        if holding.sector:
            sector = holding.sector
            if sector not in sector_breakdown:
                sector_breakdown[sector] = 0
            sector_breakdown[sector] += holding.market_value

    # Convert to percentages
    total_value = portfolio.total_value
    asset_class_pct = {
        k: round((v / total_value) * 100, 2) for k, v in asset_class_breakdown.items()
    }
    sector_pct = {
        k: round((v / total_value) * 100, 2) for k, v in sector_breakdown.items()
    }

    return {
        "portfolio_id": portfolio_id,
        "total_value": total_value,
        "num_holdings": len(portfolio.holdings),
        "asset_class_breakdown": asset_class_pct,
        "sector_breakdown": sector_pct,
    }


def get_conservative_example() -> tuple[ClientProfile, Portfolio]:
    """Get the conservative risk profile example (CLT-2024-001, conservative)."""
    pair = load_client_portfolio_pair("CLT-2024-001")
    if not pair:
        raise ValueError("Conservative example not found")
    return pair


def get_moderate_example() -> tuple[ClientProfile, Portfolio]:
    """Get the moderate risk profile example (CLT-2024-002, moderate)."""
    pair = load_client_portfolio_pair("CLT-2024-002")
    if not pair:
        raise ValueError("Moderate example not found")
    return pair


def get_aggressive_example() -> tuple[ClientProfile, Portfolio]:
    """Get the aggressive risk profile example (CLT-2024-003, aggressive)."""
    pair = load_client_portfolio_pair("CLT-2024-003")
    if not pair:
        raise ValueError("Aggressive example not found")
    return pair


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    # Example: Load all clients and portfolios
    print("=== Loading Sample Data ===\n")

    clients = load_client_profiles()
    print(f"Loaded {len(clients)} client profiles:")
    for client_id, client in clients.items():
        print(
            f"  - {client_id}: Age {client.age}, {client.risk_tolerance.value}, {client.time_horizon}yr horizon"
        )

    print()

    portfolios = load_portfolios()
    print(f"Loaded {len(portfolios)} portfolios:")
    for portfolio_id, portfolio in portfolios.items():
        print(
            f"  - {portfolio_id}: ${portfolio.total_value:,.0f}, {len(portfolio.holdings)} holdings"
        )

    print()

    # Example: Load a client-portfolio pair
    print("=== Conservative Example ===\n")
    client, portfolio = get_conservative_example()
    print(f"Client: {client.client_id}, Age {client.age}")
    print(f"Risk Tolerance: {client.risk_tolerance.value}")
    print(f"Portfolio: {portfolio.portfolio_id}, ${portfolio.total_value:,.0f}")

    summary = get_portfolio_summary(portfolio.portfolio_id)
    print(f"\nAsset Allocation:")
    for asset_class, pct in summary["asset_class_breakdown"].items():
        print(f"  - {asset_class}: {pct}%")

    print(f"\nAll unique tickers: {', '.join(get_all_tickers())}")
