"""
Risk Analyst Agent for Multi-Agent Portfolio Collaboration System.

This agent performs comprehensive risk analysis on client portfolios, calculating
key risk metrics and providing actionable recommendations for risk mitigation.

Biblical Principle: PERSEVERE - Build resilient systems that handle failures gracefully
and provide clear risk assessments to help clients navigate market uncertainties.

Stage: Wave 1 - Specialist Agent Implementation
"""

from typing import Optional

from agents import Agent, function_tool

from ..models.schemas import (
    AssetClass,
    ClientProfile,
    Portfolio,
    RiskAnalysis,
    RiskRating,
)


# ============================================================================
# Risk Calculation Helper Functions
# ============================================================================


def calculate_volatility(portfolio: Portfolio) -> float:
    """
    Calculate annualized portfolio volatility based on asset allocation.

    Methodology:
    - Conservative portfolios (>40% bonds): 8-12% volatility
    - Moderate portfolios (20-40% bonds): 12-18% volatility
    - Aggressive portfolios (<20% bonds): 18-25% volatility

    Args:
        portfolio: Portfolio object with holdings

    Returns:
        Annualized volatility percentage (0-100)
    """
    # Calculate bond allocation percentage
    total_value = portfolio.total_value
    bond_value = sum(
        holding.market_value
        for holding in portfolio.holdings
        if holding.asset_class == AssetClass.FIXED_INCOME
    )
    bond_allocation = (bond_value / total_value * 100) if total_value > 0 else 0

    # Determine volatility range based on bond allocation
    if bond_allocation > 40:
        # Conservative: 8-12%
        base_volatility = 10.0
        variation = 2.0
    elif bond_allocation >= 20:
        # Moderate: 12-18%
        base_volatility = 15.0
        variation = 3.0
    else:
        # Aggressive: 18-25%
        base_volatility = 21.5
        variation = 3.5

    # Add variation based on concentration
    holdings_count = len(portfolio.holdings)
    if holdings_count < 5:
        # Low diversification increases volatility
        base_volatility += variation
    elif holdings_count > 15:
        # High diversification reduces volatility
        base_volatility -= variation * 0.5

    # Ensure volatility stays within reasonable bounds
    return round(max(8.0, min(25.0, base_volatility)), 2)


def calculate_var_95(portfolio: Portfolio, volatility: float) -> float:
    """
    Calculate 95% Value at Risk (VaR).

    VaR represents the potential loss at the 95% confidence level.
    For a normal distribution, 95% VaR ≈ -1.645 * daily volatility.

    Methodology:
    - Convert annualized volatility to daily volatility (÷ √252)
    - Apply 1.645 multiplier for 95% confidence
    - Scale to percentage of portfolio value

    Args:
        portfolio: Portfolio object
        volatility: Annualized volatility percentage

    Returns:
        Potential loss percentage (negative value, e.g., -8.5 means 8.5% potential loss)
    """
    # Convert annual volatility to daily (assuming 252 trading days)
    daily_volatility = volatility / (252 ** 0.5)

    # Calculate 95% VaR using 1.645 standard deviations
    var_95 = -1.645 * daily_volatility

    return round(var_95, 2)


def calculate_beta(portfolio: Portfolio) -> float:
    """
    Calculate portfolio beta relative to market benchmark (SPY).

    Beta measures systematic risk relative to the market:
    - Beta < 1.0: Less volatile than market
    - Beta = 1.0: Moves with market
    - Beta > 1.0: More volatile than market

    Methodology (mock calculation):
    - Heavy bonds (>40%): 0.5-0.8 beta
    - Balanced (20-40% bonds): 0.8-1.1 beta
    - Heavy equities (<20% bonds): 1.0-1.3 beta

    Args:
        portfolio: Portfolio object with holdings

    Returns:
        Portfolio beta coefficient
    """
    total_value = portfolio.total_value

    # Calculate equity and bond allocations
    equity_value = sum(
        holding.market_value
        for holding in portfolio.holdings
        if holding.asset_class == AssetClass.EQUITY
    )
    bond_value = sum(
        holding.market_value
        for holding in portfolio.holdings
        if holding.asset_class == AssetClass.FIXED_INCOME
    )

    equity_pct = (equity_value / total_value * 100) if total_value > 0 else 0
    bond_pct = (bond_value / total_value * 100) if total_value > 0 else 0

    # Determine beta based on allocation
    if bond_pct > 40:
        # Conservative: Low beta
        base_beta = 0.65
    elif bond_pct >= 20:
        # Moderate: Market beta
        base_beta = 0.95
    else:
        # Aggressive: High beta
        base_beta = 1.15

    # Adjust for equity concentration
    if equity_pct > 80:
        base_beta += 0.10

    return round(base_beta, 2)


def calculate_concentration_score(portfolio: Portfolio) -> float:
    """
    Calculate portfolio concentration risk score.

    Concentration risk measures diversification quality:
    - 0 = Perfectly diversified
    - 100 = Highly concentrated

    Methodology:
    - Analyze top holding percentage
    - Consider sector concentration
    - Factor in total number of holdings

    Args:
        portfolio: Portfolio object with holdings

    Returns:
        Concentration score (0-100)
    """
    if not portfolio.holdings:
        return 100.0  # Empty portfolio is maximally concentrated

    total_value = portfolio.total_value
    holdings_count = len(portfolio.holdings)

    # Calculate top holding percentage
    top_holding_pct = max(
        (holding.market_value / total_value * 100) if total_value > 0 else 0
        for holding in portfolio.holdings
    )

    # Base concentration score on top holding
    if top_holding_pct > 25:
        concentration = 80.0
    elif top_holding_pct > 15:
        concentration = 60.0
    elif top_holding_pct > 10:
        concentration = 40.0
    else:
        concentration = 20.0

    # Adjust for number of holdings
    if holdings_count < 5:
        concentration += 15.0
    elif holdings_count > 15:
        concentration -= 15.0

    # Calculate sector concentration (if sector data available)
    sectors = {}
    for holding in portfolio.holdings:
        if holding.sector:
            sectors[holding.sector] = sectors.get(holding.sector, 0) + holding.market_value

    if sectors:
        max_sector_pct = max(sectors.values()) / total_value * 100 if total_value > 0 else 0
        if max_sector_pct > 40:
            concentration += 10.0
        elif max_sector_pct > 30:
            concentration += 5.0

    # Ensure score stays within 0-100 range
    return round(max(0.0, min(100.0, concentration)), 2)


def determine_risk_rating(
    volatility: float,
    concentration_score: float,
    beta: float
) -> RiskRating:
    """
    Determine overall portfolio risk rating based on metrics.

    Risk Rating Criteria:
    - LOW: Volatility <12%, Concentration <30, Beta <0.9
    - MEDIUM: Volatility 12-18%, Concentration 30-60, Beta 0.9-1.1
    - HIGH: Volatility 18-22%, Concentration 60-80, Beta 1.1-1.3
    - VERY_HIGH: Volatility >22%, Concentration >80, Beta >1.3

    Args:
        volatility: Annualized volatility percentage
        concentration_score: Concentration risk score (0-100)
        beta: Portfolio beta coefficient

    Returns:
        RiskRating enum value
    """
    # Count high-risk indicators
    risk_factors = 0

    if volatility > 22:
        risk_factors += 3
    elif volatility > 18:
        risk_factors += 2
    elif volatility > 12:
        risk_factors += 1

    if concentration_score > 80:
        risk_factors += 3
    elif concentration_score > 60:
        risk_factors += 2
    elif concentration_score > 30:
        risk_factors += 1

    if beta > 1.3:
        risk_factors += 2
    elif beta > 1.1:
        risk_factors += 1

    # Determine rating based on risk factor count
    if risk_factors >= 6:
        return RiskRating.VERY_HIGH
    elif risk_factors >= 4:
        return RiskRating.HIGH
    elif risk_factors >= 2:
        return RiskRating.MEDIUM
    else:
        return RiskRating.LOW


def generate_risk_concerns(
    portfolio: Portfolio,
    volatility: float,
    concentration_score: float,
    beta: float,
    client_profile: Optional[ClientProfile] = None
) -> list[str]:
    """
    Generate list of specific risk concerns based on portfolio analysis.

    Args:
        portfolio: Portfolio object
        volatility: Calculated volatility
        concentration_score: Calculated concentration score
        beta: Calculated beta
        client_profile: Optional client profile for suitability context

    Returns:
        List of risk concern strings
    """
    concerns = []

    # Volatility concerns
    if volatility > 20:
        concerns.append(f"High portfolio volatility ({volatility}%) may lead to significant short-term fluctuations")
    elif volatility > 16:
        concerns.append(f"Elevated volatility ({volatility}%) suggests moderate market sensitivity")

    # Concentration concerns
    if concentration_score > 70:
        concerns.append(f"High concentration risk (score: {concentration_score}) - portfolio lacks diversification")
    elif concentration_score > 50:
        concerns.append(f"Moderate concentration risk (score: {concentration_score}) - consider additional diversification")

    # Check for sector concentration
    if portfolio.holdings:
        total_value = portfolio.total_value
        sectors = {}
        for holding in portfolio.holdings:
            if holding.sector:
                sectors[holding.sector] = sectors.get(holding.sector, 0) + holding.market_value

        if sectors:
            for sector, value in sectors.items():
                sector_pct = (value / total_value * 100) if total_value > 0 else 0
                if sector_pct > 40:
                    concerns.append(f"Heavy concentration in {sector} sector ({sector_pct:.1f}%)")

    # Beta concerns
    if beta > 1.2:
        concerns.append(f"High beta ({beta}) indicates significant market sensitivity - expect amplified market movements")
    elif beta < 0.7:
        concerns.append(f"Low beta ({beta}) may limit upside potential in bull markets")

    # Client suitability concerns
    if client_profile:
        if client_profile.risk_tolerance.value == "Conservative" and volatility > 15:
            concerns.append("Portfolio volatility may exceed conservative risk tolerance")
        if client_profile.risk_tolerance.value == "Aggressive" and volatility < 12:
            concerns.append("Portfolio may be too conservative for aggressive growth objectives")

        # Time horizon concerns
        if client_profile.time_horizon < 5 and volatility > 18:
            concerns.append(f"High volatility with short time horizon ({client_profile.time_horizon} years) increases risk of losses")

    # Holdings count concerns
    holdings_count = len(portfolio.holdings)
    if holdings_count < 5:
        concerns.append(f"Limited number of holdings ({holdings_count}) increases concentration risk")

    return concerns


def generate_recommendations(
    portfolio: Portfolio,
    volatility: float,
    concentration_score: float,
    beta: float,
    client_profile: Optional[ClientProfile] = None
) -> list[str]:
    """
    Generate actionable risk mitigation recommendations.

    Args:
        portfolio: Portfolio object
        volatility: Calculated volatility
        concentration_score: Calculated concentration score
        beta: Calculated beta
        client_profile: Optional client profile for tailored recommendations

    Returns:
        List of recommendation strings
    """
    recommendations = []

    # Concentration recommendations
    if concentration_score > 60:
        recommendations.append("Diversify holdings across more securities to reduce concentration risk")
        recommendations.append("Consider sector rotation to balance exposure across industries")

    # Check asset allocation
    if portfolio.holdings:
        total_value = portfolio.total_value
        equity_pct = sum(
            h.market_value for h in portfolio.holdings
            if h.asset_class == AssetClass.EQUITY
        ) / total_value * 100 if total_value > 0 else 0

        bond_pct = sum(
            h.market_value for h in portfolio.holdings
            if h.asset_class == AssetClass.FIXED_INCOME
        ) / total_value * 100 if total_value > 0 else 0

        # Volatility-based recommendations
        if volatility > 18 and bond_pct < 20:
            recommendations.append("Increase fixed income allocation to reduce portfolio volatility")
        elif volatility < 10 and equity_pct < 50:
            recommendations.append("Consider increasing equity allocation for higher growth potential")

    # Beta-based recommendations
    if beta > 1.2:
        recommendations.append("Consider adding defensive holdings (utilities, consumer staples) to lower portfolio beta")

    # Client-specific recommendations
    if client_profile:
        if client_profile.risk_tolerance.value == "Conservative":
            if volatility > 12:
                recommendations.append("Rebalance toward more conservative holdings aligned with risk tolerance")
            recommendations.append("Consider capital preservation strategies (bonds, dividend stocks)")

        elif client_profile.risk_tolerance.value == "Moderate":
            if volatility < 10 or volatility > 20:
                recommendations.append("Adjust allocation to achieve moderate risk profile (12-18% volatility target)")

        elif client_profile.risk_tolerance.value == "Aggressive":
            if volatility < 15:
                recommendations.append("Consider growth-oriented equities to maximize long-term appreciation potential")

        # Time horizon recommendations
        if client_profile.time_horizon < 5 and volatility > 15:
            recommendations.append("Reduce volatility given short time horizon - limit recovery time for losses")
        elif client_profile.time_horizon > 10 and volatility < 12:
            recommendations.append("Longer time horizon allows for higher risk tolerance - consider growth opportunities")

    # General best practices
    if len(portfolio.holdings) < 10:
        recommendations.append("Increase portfolio diversification to at least 10-15 holdings")

    recommendations.append("Implement regular portfolio rebalancing (quarterly or semi-annually)")
    recommendations.append("Consider tax-loss harvesting opportunities to manage tax efficiency")

    return recommendations


# ============================================================================
# Convenience Function for Direct Use
# ============================================================================


def perform_risk_analysis(
    portfolio: Portfolio,
    client_profile: Optional[ClientProfile] = None
) -> RiskAnalysis:
    """
    Convenience function to perform risk analysis without using Agent runner.

    This function directly executes the risk analysis logic and returns
    a RiskAnalysis object. Useful for testing, direct integration, or
    parallel execution without the full Agent SDK workflow.

    Args:
        portfolio: Portfolio object containing holdings and metadata
        client_profile: Optional client profile for suitability-based recommendations

    Returns:
        RiskAnalysis object with all calculated metrics, concerns, and recommendations

    Example:
        >>> from src.data.mock_portfolios import get_conservative_example
        >>> client, portfolio = get_conservative_example()
        >>> risk_analysis = perform_risk_analysis(portfolio, client)
        >>> print(f"Risk Rating: {risk_analysis.risk_rating}")
    """
    # Calculate core risk metrics
    volatility = calculate_volatility(portfolio)
    var_95 = calculate_var_95(portfolio, volatility)
    beta = calculate_beta(portfolio)
    concentration_score = calculate_concentration_score(portfolio)

    # Determine overall risk rating
    risk_rating = determine_risk_rating(volatility, concentration_score, beta)

    # Generate concerns and recommendations
    concerns = generate_risk_concerns(
        portfolio, volatility, concentration_score, beta, client_profile
    )
    recommendations = generate_recommendations(
        portfolio, volatility, concentration_score, beta, client_profile
    )

    # Mock max drawdown calculation
    max_drawdown = round(-volatility * 1.5, 2)

    # Return comprehensive risk analysis
    return RiskAnalysis(
        volatility=volatility,
        var_95=var_95,
        beta=beta,
        concentration_score=concentration_score,
        max_drawdown=max_drawdown,
        risk_rating=risk_rating,
        concerns=concerns,
        recommendations=recommendations
    )


# ============================================================================
# Risk Analyst Agent Tool
# ============================================================================


@function_tool
def analyze_portfolio_risk(
    portfolio: Portfolio,
    client_profile: Optional[ClientProfile] = None
) -> RiskAnalysis:
    """
    Perform comprehensive risk analysis on a client portfolio.

    This tool calculates key risk metrics including volatility, Value at Risk (VaR),
    beta, and concentration risk. It provides a holistic risk assessment with
    specific concerns and actionable recommendations.

    Metrics Calculated:
    - Volatility: Annualized standard deviation (8-25% range)
    - VaR 95%: Potential loss at 95% confidence level
    - Beta: Systematic risk vs SPY benchmark (0.5-1.3 range)
    - Concentration Score: Diversification quality (0=diversified, 100=concentrated)
    - Max Drawdown: Historical maximum decline (mock value)
    - Risk Rating: Overall risk classification (LOW/MEDIUM/HIGH/VERY_HIGH)

    Args:
        portfolio: Portfolio object containing holdings and metadata
        client_profile: Optional client profile for suitability-based recommendations

    Returns:
        RiskAnalysis object with all calculated metrics, concerns, and recommendations

    Example:
        >>> risk_analysis = analyze_portfolio_risk(portfolio, client_profile)
        >>> print(f"Risk Rating: {risk_analysis.risk_rating}")
        >>> print(f"Volatility: {risk_analysis.volatility}%")
    """
    # Delegate to the convenience function to avoid code duplication
    return perform_risk_analysis(portfolio, client_profile)


# ============================================================================
# Risk Analyst Agent Definition
# ============================================================================


def create_risk_analyst_agent() -> Agent:
    """
    Create the Risk Analyst Agent for portfolio risk assessment.

    This agent specializes in identifying and quantifying portfolio risks,
    providing objective risk metrics and recommendations for risk mitigation.

    Capabilities:
    - Calculate volatility, VaR, beta, and concentration metrics
    - Assess portfolio risk rating (LOW/MEDIUM/HIGH/VERY_HIGH)
    - Identify specific risk concerns
    - Generate actionable risk mitigation recommendations
    - Evaluate client-portfolio risk alignment

    Biblical Principle: PERSEVERE - Help clients navigate market uncertainties
    with clear risk assessments and resilient portfolio strategies.

    Returns:
        Agent instance configured as Risk Analyst

    Example:
        >>> risk_analyst = create_risk_analyst_agent()
        >>> result = await Runner.run(risk_analyst, input={
        ...     "portfolio": portfolio_obj,
        ...     "client_profile": client_obj
        ... })
    """
    agent = Agent(
        name="Risk Analyst",
        instructions="""You are a specialized Risk Analyst agent focused on portfolio risk assessment.

Your primary responsibilities:
1. Calculate key risk metrics: volatility, VaR, beta, concentration score
2. Determine overall portfolio risk rating (LOW/MEDIUM/HIGH/VERY_HIGH)
3. Identify specific risk concerns based on portfolio composition
4. Provide actionable recommendations for risk mitigation
5. Assess risk alignment with client profile (if provided)

When analyzing portfolios:
- Be objective and quantitative in your assessment
- Explain risk metrics in clear, understandable terms
- Prioritize concerns by severity and likelihood
- Ensure recommendations are specific and actionable
- Consider both market risk (beta) and idiosyncratic risk (concentration)
- Factor in client risk tolerance and time horizon when available

Risk Analysis Framework:
- Volatility: Measure of portfolio price fluctuation (annualized)
- VaR 95%: Maximum expected loss at 95% confidence level
- Beta: Sensitivity to market movements vs benchmark
- Concentration: Diversification quality (lower is better)
- Risk Rating: Overall risk classification for client communication

Always use the analyze_portfolio_risk tool to perform calculations and generate structured analysis.
Present findings clearly with supporting data and rationale.""",
        model="gpt-4o",
        tools=[analyze_portfolio_risk]
    )

    return agent


# ============================================================================
# Convenience Export
# ============================================================================

# Create default agent instance for easy import
risk_analyst_agent = create_risk_analyst_agent()
