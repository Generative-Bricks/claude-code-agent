"""
Example script demonstrating Compliance Officer Agent usage.

This script shows how to use the Compliance Officer Agent to perform
regulatory compliance checks on a sample portfolio.

Run: uv run python examples/test_compliance_officer.py
"""

from datetime import datetime

from src.agents.compliance_officer import analyze_compliance
from src.models.schemas import (
    AssetClass,
    ClientProfile,
    ComplianceStatus,
    Portfolio,
    PortfolioHolding,
    RiskTolerance,
)


def create_sample_client() -> ClientProfile:
    """Create a sample client profile for testing."""
    return ClientProfile(
        client_id="CLIENT-001",
        age=70,  # Retirement age - should trigger age-based rules
        risk_tolerance=RiskTolerance.CONSERVATIVE,
        investment_goals=["Retirement income", "Capital preservation"],
        time_horizon=15,
        annual_income=80000.0,
        net_worth=1200000.0,
        liquidity_needs="Moderate - quarterly distributions",
    )


def create_non_compliant_portfolio() -> Portfolio:
    """
    Create a portfolio that FAILS compliance checks.

    Issues:
    - Conservative 70-year-old client with insufficient bonds (only 20%)
    - Single holding (AAPL) exceeds 25% concentration limit
    """
    holdings = [
        # 25% in AAPL - VIOLATES concentration limit (15% max)
        PortfolioHolding(
            ticker="AAPL",
            company_name="Apple Inc.",
            shares=500,
            current_price=175.00,
            market_value=87500.00,
            asset_class=AssetClass.EQUITY,
            sector="Technology",
        ),
        # 60% in tech stocks
        PortfolioHolding(
            ticker="MSFT",
            company_name="Microsoft Corp.",
            shares=400,
            current_price=370.00,
            market_value=148000.00,
            asset_class=AssetClass.EQUITY,
            sector="Technology",
        ),
        PortfolioHolding(
            ticker="GOOGL",
            company_name="Alphabet Inc.",
            shares=300,
            current_price=140.00,
            market_value=42000.00,
            asset_class=AssetClass.EQUITY,
            sector="Technology",
        ),
        # Only 20% bonds - VIOLATES age and risk tolerance rules
        PortfolioHolding(
            ticker="AGG",
            company_name="iShares Core US Aggregate Bond ETF",
            shares=600,
            current_price=95.00,
            market_value=57000.00,
            asset_class=AssetClass.FIXED_INCOME,
            sector="Fixed Income",
        ),
        # 2% cash
        PortfolioHolding(
            ticker="CASH",
            company_name="Cash & Equivalents",
            shares=1,
            current_price=5500.00,
            market_value=5500.00,
            asset_class=AssetClass.CASH,
        ),
    ]

    total = sum(h.market_value for h in holdings)

    return Portfolio(
        portfolio_id="PORT-001",
        client_id="CLIENT-001",
        holdings=holdings,
        total_value=total,
        as_of_date=datetime.now(),
        benchmark="SPY",
    )


def create_compliant_portfolio() -> Portfolio:
    """
    Create a portfolio that PASSES compliance checks.

    Characteristics:
    - Conservative allocation (50% bonds)
    - Age-appropriate (client is 70)
    - No concentration violations
    """
    holdings = [
        # 50% bonds - COMPLIANT for conservative 70-year-old
        PortfolioHolding(
            ticker="AGG",
            company_name="iShares Core US Aggregate Bond ETF",
            shares=2000,
            current_price=95.00,
            market_value=190000.00,
            asset_class=AssetClass.FIXED_INCOME,
            sector="Fixed Income",
        ),
        PortfolioHolding(
            ticker="TLT",
            company_name="iShares 20+ Year Treasury Bond ETF",
            shares=500,
            current_price=90.00,
            market_value=45000.00,
            asset_class=AssetClass.FIXED_INCOME,
            sector="Fixed Income",
        ),
        # 40% diversified equities (no single holding >15%)
        PortfolioHolding(
            ticker="VTI",
            company_name="Vanguard Total Stock Market ETF",
            shares=400,
            current_price=240.00,
            market_value=96000.00,  # 12.3%
            asset_class=AssetClass.EQUITY,
            sector="Diversified",
        ),
        PortfolioHolding(
            ticker="VXUS",
            company_name="Vanguard Total International Stock ETF",
            shares=800,
            current_price=60.00,
            market_value=48000.00,  # 6.2%
            asset_class=AssetClass.EQUITY,
            sector="International",
        ),
        PortfolioHolding(
            ticker="VNQ",
            company_name="Vanguard Real Estate ETF",
            shares=300,
            current_price=85.00,
            market_value=25500.00,  # 3.3%
            asset_class=AssetClass.EQUITY,
            sector="Real Estate",
        ),
        # 10% cash
        PortfolioHolding(
            ticker="VMFXX",
            company_name="Vanguard Federal Money Market Fund",
            shares=1,
            current_price=76000.00,
            market_value=76000.00,
            asset_class=AssetClass.CASH,
        ),
    ]

    total = sum(h.market_value for h in holdings)

    return Portfolio(
        portfolio_id="PORT-002",
        client_id="CLIENT-001",
        holdings=holdings,
        total_value=total,
        as_of_date=datetime.now(),
        benchmark="SPY",
    )


def main():
    """Run compliance analysis examples."""
    print("=" * 80)
    print("COMPLIANCE OFFICER AGENT - EXAMPLE USAGE")
    print("=" * 80)
    print()

    client = create_sample_client()

    print(f"Client Profile: {client.client_id}")
    print(f"  Age: {client.age}")
    print(f"  Risk Tolerance: {client.risk_tolerance.value}")
    print()

    # Test 1: Non-compliant portfolio
    print("-" * 80)
    print("TEST 1: NON-COMPLIANT PORTFOLIO (Should FAIL)")
    print("-" * 80)
    print()

    bad_portfolio = create_non_compliant_portfolio()
    print(f"Portfolio Value: ${bad_portfolio.total_value:,.2f}")
    print(f"Number of Holdings: {len(bad_portfolio.holdings)}")
    print()

    report = analyze_compliance(bad_portfolio, client)

    print(f"Status: {report.status.value}")
    print(f"Suitability Pass: {report.suitability_pass}")
    print(f"Concentration Pass: {report.concentration_limits_pass}")
    print()

    if report.violations:
        print("VIOLATIONS:")
        for i, violation in enumerate(report.violations, 1):
            print(f"  {i}. {violation}")
        print()

    if report.warnings:
        print("WARNINGS:")
        for i, warning in enumerate(report.warnings, 1):
            print(f"  {i}. {warning}")
        print()

    print("Checks Performed:")
    for check in report.checks_performed:
        print(f"  ✓ {check}")
    print()

    # Test 2: Compliant portfolio
    print("-" * 80)
    print("TEST 2: COMPLIANT PORTFOLIO (Should PASS)")
    print("-" * 80)
    print()

    good_portfolio = create_compliant_portfolio()
    print(f"Portfolio Value: ${good_portfolio.total_value:,.2f}")
    print(f"Number of Holdings: {len(good_portfolio.holdings)}")
    print()

    report2 = analyze_compliance(good_portfolio, client)

    print(f"Status: {report2.status.value}")
    print(f"Suitability Pass: {report2.suitability_pass}")
    print(f"Concentration Pass: {report2.concentration_limits_pass}")
    print()

    if report2.violations:
        print("VIOLATIONS:")
        for i, violation in enumerate(report2.violations, 1):
            print(f"  {i}. {violation}")
        print()
    else:
        print("✓ No violations found")
        print()

    if report2.warnings:
        print("WARNINGS:")
        for i, warning in enumerate(report2.warnings, 1):
            print(f"  {i}. {warning}")
        print()

    print("Checks Performed:")
    for check in report2.checks_performed:
        print(f"  ✓ {check}")
    print()

    print("Required Disclosures:")
    for i, disclosure in enumerate(report2.required_disclosures, 1):
        print(f"  {i}. {disclosure}")
    print()

    print("=" * 80)
    print("COMPLIANCE ANALYSIS COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
