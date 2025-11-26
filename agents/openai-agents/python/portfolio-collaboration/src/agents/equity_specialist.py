"""
Equity Specialist Agent for deep-dive equity analysis.

This agent provides specialized equity analysis when handed off from the Portfolio Manager.
It performs sector analysis, valuation metrics, growth vs value classification, and generates
equity-specific recommendations.

Biblical Principle: EXCELLENCE - Provides thorough, detailed equity analysis with clear insights.
"""

from typing import Dict, List

from agents import Agent

from ..models.schemas import (
    AssetClass,
    EquityDeepDiveReport,
    Portfolio,
    PortfolioHolding,
    RiskTolerance,
)


# ============================================================================
# Sector and Classification Constants
# ============================================================================

# Growth sectors - typically higher valuation, focused on capital appreciation
GROWTH_SECTORS = ["Technology", "Communication Services", "Consumer Discretionary"]

# Value sectors - typically dividend-paying, focus on income and stability
VALUE_SECTORS = ["Utilities", "Consumer Staples", "Financials", "Energy"]

# Neutral sectors can be either growth or value depending on specific holdings
# We split these 50/50 for classification purposes
NEUTRAL_SECTORS = ["Healthcare", "Industrials", "Materials", "Real Estate"]


# ============================================================================
# Helper Functions for Equity Analysis
# ============================================================================


def calculate_sector_allocations(portfolio: Portfolio) -> Dict[str, Dict]:
    """
    Calculate sector allocation percentages and holdings breakdown.

    Args:
        portfolio: Portfolio object containing all holdings

    Returns:
        Dict mapping sector names to allocation data (percentage, holdings, market value)

    Biblical Principle: TRUTH - Transparent calculation of portfolio composition
    """
    sector_allocations = {}

    # Filter to equity holdings only
    equity_holdings = [
        h for h in portfolio.holdings if h.asset_class == AssetClass.EQUITY
    ]

    # If no equity holdings, return empty dict
    if not equity_holdings:
        return {}

    # Calculate total equity value for percentage calculations
    total_equity_value = sum(h.market_value for h in equity_holdings)

    # Aggregate holdings by sector
    for holding in equity_holdings:
        sector = holding.sector or "Other"

        if sector not in sector_allocations:
            sector_allocations[sector] = {
                "allocation_pct": 0.0,
                "holdings": [],
                "market_value": 0.0,
            }

        sector_allocations[sector]["allocation_pct"] += (
            holding.market_value / total_equity_value
        ) * 100
        sector_allocations[sector]["holdings"].append(holding.ticker)
        sector_allocations[sector]["market_value"] += holding.market_value

    return sector_allocations


def generate_sector_analysis(
    sector_allocations: Dict[str, Dict], risk_tolerance: RiskTolerance
) -> Dict[str, str]:
    """
    Generate detailed analysis commentary for each sector.

    Analyzes concentration, diversification needs, and alignment with risk tolerance.

    Args:
        sector_allocations: Dict of sector allocation data
        risk_tolerance: Client's risk tolerance level

    Returns:
        Dict mapping sector names to analysis commentary

    Biblical Principle: SERVE - Provides clear, actionable insights for decision-making
    """
    sector_analysis = {}

    for sector, data in sector_allocations.items():
        allocation_pct = data["allocation_pct"]
        top_holdings = ", ".join(data["holdings"][:3])  # Show top 3 holdings

        # Build analysis text
        analysis_parts = [
            f"{sector}: {allocation_pct:.1f}% allocation.",
            f"Top holdings: {top_holdings}.",
        ]

        # Concentration analysis
        if allocation_pct > 30:
            analysis_parts.append(
                "High concentration - consider diversification to reduce sector-specific risk."
            )
        elif allocation_pct < 5:
            analysis_parts.append(
                "Minimal exposure - may want to increase for better diversification."
            )
        else:
            analysis_parts.append("Appropriate allocation for a diversified portfolio.")

        # Risk tolerance alignment
        if sector in GROWTH_SECTORS:
            if risk_tolerance == RiskTolerance.CONSERVATIVE and allocation_pct > 25:
                analysis_parts.append(
                    "Growth sector allocation may be high for conservative risk tolerance."
                )
            elif risk_tolerance == RiskTolerance.AGGRESSIVE and allocation_pct < 15:
                analysis_parts.append(
                    "Consider increasing allocation for aggressive growth strategy."
                )

        if sector in VALUE_SECTORS:
            if risk_tolerance == RiskTolerance.AGGRESSIVE and allocation_pct > 25:
                analysis_parts.append(
                    "High value sector allocation may limit growth potential for aggressive strategy."
                )
            elif risk_tolerance == RiskTolerance.CONSERVATIVE and allocation_pct < 15:
                analysis_parts.append(
                    "Consider increasing allocation for income stability."
                )

        sector_analysis[sector] = " ".join(analysis_parts)

    return sector_analysis


def calculate_valuation_metrics(equity_holdings: List[PortfolioHolding]) -> Dict[str, float]:
    """
    Calculate portfolio-level valuation metrics (mock implementation).

    In production, this would fetch real-time valuation data from market data APIs.
    For now, we generate realistic mock metrics based on sector composition.

    Args:
        equity_holdings: List of equity holdings in the portfolio

    Returns:
        Dict with valuation metrics (P/E, P/B, dividend_yield)

    Biblical Principle: TRUTH - Clear disclosure that these are mock metrics
    """
    import random

    # Set seed based on portfolio composition for consistent results
    seed_value = sum(hash(h.ticker) for h in equity_holdings) % 10000
    random.seed(seed_value)

    # Mock valuation metrics - in production, fetch from market data
    # Technology/growth sectors typically have higher P/E ratios
    # Value/dividend sectors have lower P/E but higher dividend yields

    growth_weight = sum(
        h.market_value
        for h in equity_holdings
        if h.sector in GROWTH_SECTORS
    )
    total_value = sum(h.market_value for h in equity_holdings)
    growth_pct = (growth_weight / total_value * 100) if total_value > 0 else 50

    # P/E ratio: Growth-heavy portfolios have higher P/E
    pe_ratio = 15 + (growth_pct / 100) * 15  # Range: 15-30
    pe_ratio += random.uniform(-2, 2)  # Add some variance

    # P/B ratio: Typically 2-5 for diversified portfolios
    pb_ratio = 2.5 + random.uniform(-0.5, 2.5)

    # Dividend yield: Value-heavy portfolios have higher yields
    dividend_yield = 4 - (growth_pct / 100) * 3  # Range: 1-4%
    dividend_yield += random.uniform(-0.3, 0.3)

    return {
        "P/E": round(pe_ratio, 2),
        "P/B": round(pb_ratio, 2),
        "dividend_yield": round(dividend_yield, 2),
    }


def classify_growth_vs_value(equity_holdings: List[PortfolioHolding]) -> Dict[str, float]:
    """
    Classify equity holdings as Growth or Value and calculate allocation percentages.

    Classification logic:
    - Growth sectors: Technology, Communication Services, Consumer Discretionary
    - Value sectors: Utilities, Consumer Staples, Financials, Energy
    - Neutral sectors: Split 50/50 between growth and value

    Args:
        equity_holdings: List of equity holdings

    Returns:
        Dict with Growth and Value allocation percentages

    Biblical Principle: TRUTH - Clear, rule-based classification methodology
    """
    growth_value = 0.0
    value_value = 0.0

    for holding in equity_holdings:
        sector = holding.sector or "Other"

        if sector in GROWTH_SECTORS:
            growth_value += holding.market_value
        elif sector in VALUE_SECTORS:
            value_value += holding.market_value
        else:
            # Neutral sectors - split 50/50
            growth_value += holding.market_value * 0.5
            value_value += holding.market_value * 0.5

    total = growth_value + value_value

    if total == 0:
        return {"Growth": 0.0, "Value": 0.0}

    return {
        "Growth": round((growth_value / total) * 100, 2),
        "Value": round((value_value / total) * 100, 2),
    }


def generate_equity_recommendations(
    sector_allocations: Dict[str, Dict],
    valuation_metrics: Dict[str, float],
    growth_vs_value: Dict[str, float],
    risk_tolerance: RiskTolerance,
) -> List[str]:
    """
    Generate actionable equity-specific recommendations.

    Based on sector concentration, valuation levels, growth/value balance,
    and client risk tolerance.

    Args:
        sector_allocations: Sector allocation data
        valuation_metrics: Portfolio valuation metrics
        growth_vs_value: Growth vs Value classification
        risk_tolerance: Client risk tolerance

    Returns:
        List of equity-specific recommendations

    Biblical Principle: SERVE - Actionable guidance tailored to client needs
    """
    recommendations = []

    # Check sector concentration
    if sector_allocations:
        max_sector = max(sector_allocations.items(), key=lambda x: x[1]["allocation_pct"])
        if max_sector[1]["allocation_pct"] > 30:
            recommendations.append(
                f"Reduce concentration in {max_sector[0]} sector (currently {max_sector[1]['allocation_pct']:.1f}%) "
                "to improve diversification and reduce sector-specific risk."
            )

    # Check valuation levels
    pe_ratio = valuation_metrics.get("P/E", 20)
    if pe_ratio > 25:
        recommendations.append(
            f"Portfolio P/E ratio of {pe_ratio:.1f} suggests elevated valuations. "
            "Consider rebalancing toward value stocks or defensive sectors if markets become volatile."
        )
    elif pe_ratio < 17:
        recommendations.append(
            f"Portfolio P/E ratio of {pe_ratio:.1f} suggests attractive valuations. "
            "Current positioning may offer good value for long-term growth."
        )

    # Check growth vs value balance
    growth_pct = growth_vs_value.get("Growth", 50)
    value_pct = growth_vs_value.get("Value", 50)

    if risk_tolerance == RiskTolerance.CONSERVATIVE:
        if growth_pct > 60:
            recommendations.append(
                f"Growth allocation of {growth_pct:.1f}% may be aggressive for conservative risk tolerance. "
                "Consider shifting toward value/dividend stocks for stability."
            )
    elif risk_tolerance == RiskTolerance.AGGRESSIVE:
        if value_pct > 60:
            recommendations.append(
                f"Value allocation of {value_pct:.1f}% may limit upside potential for aggressive strategy. "
                "Consider increasing growth stock exposure to align with return objectives."
            )
    else:  # Moderate
        if abs(growth_pct - value_pct) > 30:
            recommendations.append(
                "Consider rebalancing growth/value split for a more balanced moderate risk approach."
            )

    # Dividend yield recommendations
    dividend_yield = valuation_metrics.get("dividend_yield", 2)
    if dividend_yield < 1.5 and risk_tolerance == RiskTolerance.CONSERVATIVE:
        recommendations.append(
            f"Low dividend yield of {dividend_yield:.2f}% may not align with income needs. "
            "Consider adding dividend-paying stocks or dividend-focused ETFs."
        )

    # Sector diversification
    if len(sector_allocations) < 5:
        recommendations.append(
            f"Portfolio is concentrated in {len(sector_allocations)} sectors. "
            "Consider expanding to 6-8 sectors for better diversification."
        )

    return recommendations


def generate_detailed_analysis(
    sector_analysis: Dict[str, str],
    valuation_metrics: Dict[str, float],
    growth_vs_value: Dict[str, float],
    recommendations: List[str],
    risk_tolerance: RiskTolerance,
) -> str:
    """
    Generate comprehensive narrative equity analysis.

    Synthesizes all analysis components into a detailed report for the Portfolio Manager.

    Args:
        sector_analysis: Sector-by-sector analysis
        valuation_metrics: Portfolio valuation metrics
        growth_vs_value: Growth vs Value classification
        recommendations: List of recommendations
        risk_tolerance: Client risk tolerance

    Returns:
        Comprehensive narrative analysis text

    Biblical Principle: EXCELLENCE - Thorough, professional analysis
    """
    analysis_parts = [
        "=== EQUITY DEEP DIVE ANALYSIS ===\n",
        "\n## PORTFOLIO COMPOSITION\n",
    ]

    # Sector analysis summary
    analysis_parts.append(
        f"The equity portfolio is diversified across {len(sector_analysis)} sectors:\n"
    )
    for _sector, analysis in sector_analysis.items():
        analysis_parts.append(f"- {analysis}\n")

    # Valuation metrics
    analysis_parts.append("\n## VALUATION METRICS\n")
    analysis_parts.append(
        f"Portfolio-level valuation metrics indicate the following characteristics:\n"
    )
    analysis_parts.append(
        f"- Price-to-Earnings (P/E) Ratio: {valuation_metrics.get('P/E', 0):.2f}\n"
    )
    analysis_parts.append(
        f"- Price-to-Book (P/B) Ratio: {valuation_metrics.get('P/B', 0):.2f}\n"
    )
    analysis_parts.append(
        f"- Dividend Yield: {valuation_metrics.get('dividend_yield', 0):.2f}%\n"
    )

    # Interpret valuations
    pe_ratio = valuation_metrics.get("P/E", 20)
    if pe_ratio > 25:
        analysis_parts.append(
            "\nThe elevated P/E ratio suggests the portfolio leans toward growth stocks "
            "with higher valuations, which may carry increased volatility risk.\n"
        )
    elif pe_ratio < 17:
        analysis_parts.append(
            "\nThe below-market P/E ratio suggests the portfolio includes value stocks "
            "trading at attractive valuations relative to earnings.\n"
        )
    else:
        analysis_parts.append(
            "\nThe P/E ratio is in line with broad market averages, suggesting "
            "a balanced valuation profile.\n"
        )

    # Growth vs Value analysis
    analysis_parts.append("\n## GROWTH VS VALUE ALLOCATION\n")
    growth_pct = growth_vs_value.get("Growth", 0)
    value_pct = growth_vs_value.get("Value", 0)
    analysis_parts.append(
        f"The portfolio is split {growth_pct:.1f}% Growth and {value_pct:.1f}% Value.\n"
    )

    if growth_pct > 60:
        analysis_parts.append(
            "This growth-oriented positioning offers higher upside potential but "
            "carries increased volatility during market downturns.\n"
        )
    elif value_pct > 60:
        analysis_parts.append(
            "This value-oriented positioning provides stability and income potential "
            "but may lag during strong growth rallies.\n"
        )
    else:
        analysis_parts.append(
            "This balanced growth/value split provides exposure to both capital "
            "appreciation and stability.\n"
        )

    # Risk tolerance alignment
    analysis_parts.append("\n## RISK TOLERANCE ALIGNMENT\n")
    if risk_tolerance == RiskTolerance.CONSERVATIVE:
        analysis_parts.append(
            "For a conservative investor, the portfolio should emphasize capital "
            "preservation, dividend income, and lower volatility sectors.\n"
        )
    elif risk_tolerance == RiskTolerance.AGGRESSIVE:
        analysis_parts.append(
            "For an aggressive investor, the portfolio should emphasize growth potential, "
            "with willingness to accept higher volatility for greater returns.\n"
        )
    else:
        analysis_parts.append(
            "For a moderate investor, the portfolio should balance growth and stability "
            "with diversified sector exposure.\n"
        )

    # Recommendations summary
    if recommendations:
        analysis_parts.append("\n## KEY RECOMMENDATIONS\n")
        for i, rec in enumerate(recommendations, 1):
            analysis_parts.append(f"{i}. {rec}\n")

    analysis_parts.append(
        "\n=== END OF EQUITY DEEP DIVE ANALYSIS ===\n"
    )

    return "".join(analysis_parts)


# ============================================================================
# Equity Specialist Agent Definition
# ============================================================================

equity_specialist_agent = Agent(
    name="Equity Specialist",
    handoff_description=(
        "Expert in deep-dive equity analysis including sector allocation, "
        "valuation metrics, growth vs value classification, and equity-specific recommendations"
    ),
    instructions="""You are an expert equity analyst specializing in deep-dive equity portfolio analysis.

When you receive a portfolio and client profile, you provide comprehensive equity analysis covering:

1. **Sector Analysis**: Break down equity holdings by sector, identify concentration risks,
   and provide sector-specific commentary

2. **Valuation Metrics**: Calculate and interpret portfolio-level metrics like P/E ratio,
   P/B ratio, and dividend yield

3. **Growth vs Value Classification**: Classify holdings as growth or value stocks and
   analyze the balance

4. **Risk Alignment**: Assess whether the equity allocation aligns with the client's
   risk tolerance

5. **Recommendations**: Provide specific, actionable recommendations for improving
   sector diversification, valuation balance, and risk alignment

Your analysis should be thorough, professional, and tailored to the client's risk profile.
Use clear language and provide specific numbers and percentages to support your insights.

When you complete your analysis, return control to the Portfolio Manager with your
detailed equity deep dive report.""",
    model="gpt-4o",  # Use GPT-4 for detailed analytical reasoning
)


# ============================================================================
# Agent Analysis Function (called by Portfolio Manager)
# ============================================================================


def perform_equity_deep_dive(
    portfolio: Portfolio,
    client_profile,  # ClientProfile type
    focus_areas: List[str],
    _questions: List[str] = None,
) -> EquityDeepDiveReport:
    """
    Perform comprehensive equity deep dive analysis.

    This function is called by the Portfolio Manager when deep equity analysis is needed.
    It analyzes sectors, valuations, growth/value split, and generates recommendations.

    Args:
        portfolio: Portfolio to analyze
        client_profile: Client profile with risk tolerance and goals
        focus_areas: Specific areas to focus on (e.g., "Valuation", "Sector allocation")
        questions: Optional specific questions from client or manager

    Returns:
        EquityDeepDiveReport with comprehensive analysis

    Biblical Principle: EXCELLENCE - Thorough analysis delivering maximum value
    """
    # Filter equity holdings
    equity_holdings = [
        h for h in portfolio.holdings if h.asset_class == AssetClass.EQUITY
    ]

    if not equity_holdings:
        # No equity holdings - return minimal report
        return EquityDeepDiveReport(
            focus_areas_analyzed=focus_areas,
            sector_analysis={},
            valuation_metrics={},
            growth_vs_value_split={"Growth": 0.0, "Value": 0.0},
            recommendations=[
                "Portfolio contains no equity holdings. Consider adding equity exposure "
                "based on client risk tolerance and investment objectives."
            ],
            detailed_analysis="No equity holdings found in portfolio. Unable to perform equity analysis.",
        )

    # Calculate sector allocations
    sector_allocations = calculate_sector_allocations(portfolio)

    # Generate sector analysis with risk tolerance context
    sector_analysis = generate_sector_analysis(
        sector_allocations, client_profile.risk_tolerance
    )

    # Calculate valuation metrics
    valuation_metrics = calculate_valuation_metrics(equity_holdings)

    # Classify growth vs value
    growth_vs_value_split = classify_growth_vs_value(equity_holdings)

    # Generate recommendations
    recommendations = generate_equity_recommendations(
        sector_allocations,
        valuation_metrics,
        growth_vs_value_split,
        client_profile.risk_tolerance,
    )

    # Generate detailed narrative analysis
    detailed_analysis = generate_detailed_analysis(
        sector_analysis,
        valuation_metrics,
        growth_vs_value_split,
        recommendations,
        client_profile.risk_tolerance,
    )

    return EquityDeepDiveReport(
        focus_areas_analyzed=focus_areas,
        sector_analysis=sector_analysis,
        valuation_metrics=valuation_metrics,
        growth_vs_value_split=growth_vs_value_split,
        recommendations=recommendations,
        detailed_analysis=detailed_analysis,
    )
