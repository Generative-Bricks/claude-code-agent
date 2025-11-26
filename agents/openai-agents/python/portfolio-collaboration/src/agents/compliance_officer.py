"""
Compliance Officer Agent for Multi-Agent Portfolio Collaboration System.

This agent performs regulatory compliance checks on client portfolios, ensuring
adherence to suitability requirements, concentration limits, age-based rules,
and identifying required regulatory disclosures.

Biblical Principle: TRUTH - All compliance decisions are transparent and explainable.
Biblical Principle: HONOR - Client protection through rigorous compliance standards.

Wave 1: Specialist Agents Implementation
"""

from typing import List, Tuple

from agents import Agent, function_tool

from ..models.schemas import (
    AssetClass,
    ClientProfile,
    ComplianceReport,
    ComplianceStatus,
    Portfolio,
    RiskTolerance,
)


# ============================================================================
# Compliance Business Rules
# ============================================================================


def calculate_bond_percentage(portfolio: Portfolio) -> float:
    """
    Calculate percentage of portfolio allocated to fixed income assets.

    Args:
        portfolio: Portfolio to analyze

    Returns:
        Percentage of portfolio in fixed income (0-100)
    """
    total_value = portfolio.total_value
    if total_value == 0:
        return 0.0

    bond_value = sum(
        holding.market_value
        for holding in portfolio.holdings
        if holding.asset_class == AssetClass.FIXED_INCOME
    )

    return (bond_value / total_value) * 100


def get_largest_holding_percentage(portfolio: Portfolio) -> float:
    """
    Calculate the percentage of the largest single holding in the portfolio.

    Args:
        portfolio: Portfolio to analyze

    Returns:
        Percentage of largest holding (0-100)
    """
    if not portfolio.holdings or portfolio.total_value == 0:
        return 0.0

    max_value = max(holding.market_value for holding in portfolio.holdings)
    return (max_value / portfolio.total_value) * 100


def check_suitability(
    portfolio: Portfolio, client: ClientProfile
) -> Tuple[ComplianceStatus, str, List[str]]:
    """
    Verify portfolio suitability against client risk tolerance and demographics.

    Business Rules:
    - Conservative clients: Should have 40%+ bonds, low volatility stocks
    - Moderate clients: Balanced allocation, diversified
    - Aggressive clients: Can have high growth stocks, minimal bonds
    - Age 65+: Should have 35%+ fixed income allocation

    Args:
        portfolio: Portfolio to analyze
        client: Client profile with risk tolerance and age

    Returns:
        Tuple of (status, message, warnings_list)
    """
    bond_pct = calculate_bond_percentage(portfolio)
    violations: List[str] = []
    warnings: List[str] = []

    # Conservative client suitability check
    if client.risk_tolerance == RiskTolerance.CONSERVATIVE:
        if bond_pct < 40:
            violations.append(
                f"Conservative client has insufficient fixed income allocation "
                f"({bond_pct:.1f}% vs 40% minimum requirement)"
            )

    # Moderate client suitability check
    elif client.risk_tolerance == RiskTolerance.MODERATE:
        if bond_pct < 20:
            warnings.append(
                f"Moderate client has low fixed income allocation ({bond_pct:.1f}%). "
                f"Consider minimum 20% for balanced portfolio"
            )
        elif bond_pct > 70:
            warnings.append(
                f"Moderate client has very high fixed income allocation ({bond_pct:.1f}%). "
                f"May be overly conservative for moderate risk profile"
            )

    # Aggressive client suitability check
    elif client.risk_tolerance == RiskTolerance.AGGRESSIVE:
        if bond_pct > 30:
            warnings.append(
                f"Aggressive client has high fixed income allocation ({bond_pct:.1f}%). "
                f"May be too conservative for aggressive risk tolerance"
            )

    # Age-based suitability check (65+ years old)
    if client.age >= 65:
        if bond_pct < 35:
            violations.append(
                f"Client age {client.age} requires minimum 35% fixed income allocation. "
                f"Current allocation: {bond_pct:.1f}%"
            )

    # Young client guidance (under 40)
    if client.age < 40 and bond_pct > 50:
        warnings.append(
            f"Client age {client.age} has high fixed income allocation ({bond_pct:.1f}%). "
            f"Consider higher equity allocation for long time horizon"
        )

    # Determine overall status
    if violations:
        status = ComplianceStatus.FAIL
        message = f"Suitability check FAILED: {len(violations)} violation(s) found"
    elif warnings:
        status = ComplianceStatus.REVIEW
        message = f"Suitability check requires REVIEW: {len(warnings)} warning(s) found"
    else:
        status = ComplianceStatus.PASS
        message = "Suitability check PASSED: Portfolio matches client risk profile"

    return status, message, violations + warnings


def check_concentration_limits(
    portfolio: Portfolio,
) -> Tuple[ComplianceStatus, str, List[str]]:
    """
    Verify no single holding exceeds 15% concentration limit.

    Regulatory Rule: No single position should exceed 15% of total portfolio value
    to ensure adequate diversification and limit single-security risk.

    Args:
        portfolio: Portfolio to analyze

    Returns:
        Tuple of (status, message, violations_list)
    """
    violations: List[str] = []
    max_limit = 15.0

    for holding in portfolio.holdings:
        holding_pct = (holding.market_value / portfolio.total_value) * 100

        if holding_pct > max_limit:
            violations.append(
                f"{holding.ticker} ({holding.company_name or 'N/A'}) exceeds "
                f"concentration limit: {holding_pct:.1f}% (max {max_limit}%)"
            )

    if violations:
        status = ComplianceStatus.FAIL
        message = f"Concentration check FAILED: {len(violations)} violation(s) found"
    else:
        status = ComplianceStatus.PASS
        message = "Concentration check PASSED: All holdings within 15% limit"

    return status, message, violations


def identify_required_disclosures(portfolio: Portfolio) -> List[str]:
    """
    Identify regulatory disclosures required based on portfolio holdings.

    Disclosure Rules:
    - High volatility stocks: Require risk disclosure
    - Leveraged ETFs: Require leveraged product disclosure
    - Alternative investments: Require alternative investment disclosure
    - Sector concentration: Require sector risk disclosure

    Args:
        portfolio: Portfolio to analyze

    Returns:
        List of required disclosure statements
    """
    disclosures: List[str] = []

    # Check for alternative investments
    alt_holdings = [
        h for h in portfolio.holdings if h.asset_class == AssetClass.ALTERNATIVES
    ]
    if alt_holdings:
        tickers = ", ".join(h.ticker for h in alt_holdings)
        disclosures.append(
            f"Alternative Investment Disclosure Required: Portfolio contains "
            f"alternative investments ({tickers}). Client must acknowledge "
            f"liquidity risks and valuation complexity."
        )

    # Check for leveraged products (ticker contains "3X", "2X", or "-X")
    leveraged_holdings = [
        h
        for h in portfolio.holdings
        if any(indicator in h.ticker.upper() for indicator in ["3X", "2X", "-X"])
    ]
    if leveraged_holdings:
        tickers = ", ".join(h.ticker for h in leveraged_holdings)
        disclosures.append(
            f"Leveraged Product Disclosure Required: Portfolio contains "
            f"leveraged ETFs ({tickers}). Client must acknowledge amplified "
            f"volatility and decay risks."
        )

    # Check for sector concentration (>30% in single sector)
    sector_allocation = {}
    for holding in portfolio.holdings:
        if holding.sector:
            sector = holding.sector
            sector_allocation[sector] = (
                sector_allocation.get(sector, 0) + holding.market_value
            )

    for sector, value in sector_allocation.items():
        sector_pct = (value / portfolio.total_value) * 100
        if sector_pct > 30:
            disclosures.append(
                f"Sector Concentration Disclosure Required: {sector} sector "
                f"represents {sector_pct:.1f}% of portfolio. Client must "
                f"acknowledge concentrated sector risk."
            )

    # General risk disclosure (always required)
    disclosures.append(
        "Standard Risk Disclosure: All investments carry risk of loss. "
        "Past performance does not guarantee future results."
    )

    return disclosures


# ============================================================================
# Compliance Officer Agent Tool
# ============================================================================


def _do_compliance_check(
    portfolio: Portfolio, client_profile: ClientProfile
) -> ComplianceReport:
    """
    Internal function that performs the actual compliance checking logic.

    This is called by both the @function_tool decorated version (for Agent SDK)
    and the convenience function (for direct use).
    """
    checks_performed: List[str] = []
    all_violations: List[str] = []
    all_warnings: List[str] = []

    # Check 1: Client Suitability
    checks_performed.append("Client Suitability Analysis")
    suitability_status, suitability_msg, suitability_issues = check_suitability(
        portfolio, client_profile
    )

    # Separate violations from warnings
    suitability_violations = [
        issue
        for issue in suitability_issues
        if "insufficient" in issue.lower() or "requires minimum" in issue.lower()
    ]
    suitability_warnings = [
        issue for issue in suitability_issues if issue not in suitability_violations
    ]

    all_violations.extend(suitability_violations)
    all_warnings.extend(suitability_warnings)

    suitability_pass = suitability_status == ComplianceStatus.PASS

    # Check 2: Concentration Limits
    checks_performed.append("Concentration Limit Verification (15% max per holding)")
    concentration_status, concentration_msg, concentration_violations = (
        check_concentration_limits(portfolio)
    )

    all_violations.extend(concentration_violations)
    concentration_pass = concentration_status == ComplianceStatus.PASS

    # Check 3: Required Disclosures
    checks_performed.append("Required Disclosure Identification")
    required_disclosures = identify_required_disclosures(portfolio)

    # Determine overall compliance status
    if all_violations:
        overall_status = ComplianceStatus.FAIL
    elif all_warnings:
        overall_status = ComplianceStatus.REVIEW
    else:
        overall_status = ComplianceStatus.PASS

    # Compile detailed notes
    notes = f"""
Compliance Analysis Summary:

Client: {client_profile.client_id}
Risk Tolerance: {client_profile.risk_tolerance.value}
Age: {client_profile.age}
Portfolio Value: ${portfolio.total_value:,.2f}

Suitability Check: {suitability_msg}
Concentration Check: {concentration_msg}

Overall Status: {overall_status.value}
""".strip()

    # Create and return ComplianceReport
    return ComplianceReport(
        overall_status=overall_status,
        checks_performed=checks_performed,
        violations=all_violations,
        warnings=all_warnings,
        required_disclosures=required_disclosures,
        suitability_pass=suitability_pass,
        concentration_limits_pass=concentration_pass,
        notes=notes,
    )


@function_tool
def perform_compliance_check(
    portfolio: Portfolio, client_profile: ClientProfile
) -> ComplianceReport:
    """
    Perform comprehensive regulatory compliance analysis on client portfolio.

    This tool executes all compliance checks including:
    1. Client suitability verification (risk tolerance + age)
    2. Concentration limit verification (15% max per holding)
    3. Required disclosure identification

    Args:
        portfolio: Portfolio object to analyze
        client_profile: Client profile for suitability checks

    Returns:
        ComplianceReport with detailed compliance status and findings

    Example:
        >>> report = perform_compliance_check(portfolio, client)
        >>> print(report.status)  # PASS, FAIL, or REVIEW
        >>> print(report.violations)  # List of violations found
    """
    # Delegate to internal function to avoid code duplication
    return _do_compliance_check(portfolio, client_profile)


# ============================================================================
# Compliance Officer Agent Definition
# ============================================================================

compliance_officer_agent = Agent(
    name="Compliance Officer",
    instructions="""You are a Compliance Officer Agent specializing in regulatory
compliance analysis for investment portfolios.

Your responsibilities:
1. Verify client suitability based on risk tolerance and demographics
2. Check concentration limits (no holding >15% of portfolio)
3. Apply age-based investment rules (65+ requires 35%+ fixed income)
4. Identify required regulatory disclosures

You MUST use the perform_compliance_check tool for all compliance analysis.
Return structured ComplianceReport with clear status, violations, and warnings.

Biblical Principle: TRUTH - Provide transparent, explainable compliance decisions.
Biblical Principle: HONOR - Protect clients through rigorous compliance standards.

Always be thorough, objective, and conservative in your compliance assessments.
When in doubt, flag for REVIEW rather than approving questionable portfolios.
""",
    tools=[perform_compliance_check],
    model="gpt-4o",
)


# ============================================================================
# Convenience Function for External Use
# ============================================================================


def analyze_compliance(
    portfolio: Portfolio, client_profile: ClientProfile
) -> ComplianceReport:
    """
    Convenience function to perform compliance analysis without using Agent runner.

    This function directly executes the compliance check logic and returns
    a ComplianceReport. Useful for testing or direct integration without
    the full Agent SDK workflow.

    Args:
        portfolio: Portfolio to analyze
        client_profile: Client profile for suitability checks

    Returns:
        ComplianceReport with compliance status and findings

    Example:
        >>> from src.agents.compliance_officer import analyze_compliance
        >>> report = analyze_compliance(my_portfolio, my_client)
        >>> if report.status == ComplianceStatus.FAIL:
        ...     print("Violations found:", report.violations)
    """
    return _do_compliance_check(portfolio, client_profile)
