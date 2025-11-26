"""
Suitability Scoring Tool for Multi-Agent Portfolio Collaboration System.

This module calculates client-portfolio suitability scores by combining inputs
from Risk Analyst, Compliance Officer, and Performance Analyst agents.

Biblical Principle: TRUTH - Transparent scoring methodology with clear explanations.
Biblical Principle: EXCELLENCE - Comprehensive suitability analysis from inception.

Scoring Components:
- Risk Fit (25%): Portfolio risk vs client risk tolerance
- Compliance Fit (35%): Regulatory compliance status
- Performance Fit (25%): Returns vs benchmark expectations
- Time Horizon Fit (15%): Volatility alignment with investment timeline

Overall Score = (risk_fit * 0.25) + (compliance_fit * 0.35) +
                (performance_fit * 0.25) + (time_horizon_fit * 0.15)

Interpretation:
- 80-100: Highly Suitable
- 60-79: Suitable
- 40-59: Marginal Fit
- 0-39: Not Suitable
"""

from typing import List

from src.models.schemas import (
    ClientProfile,
    ComplianceReport,
    ComplianceStatus,
    PerformanceReport,
    RiskAnalysis,
    RiskRating,
    RiskTolerance,
    SuitabilityRating,
    SuitabilityScore,
)


# ============================================================================
# Helper Functions for Component Scoring
# ============================================================================


def calculate_risk_fit_score(
    client_profile: ClientProfile, risk_analysis: RiskAnalysis
) -> float:
    """
    Calculate risk fit score (0-100) based on client risk tolerance vs portfolio risk.

    Conservative client + LOW risk portfolio = 100 points (perfect match)
    Conservative client + HIGH risk portfolio = 30 points (poor match)
    Aggressive client + HIGH risk portfolio = 100 points (perfect match)
    Aggressive client + LOW risk portfolio = 60 points (acceptable but underutilized)

    Args:
        client_profile: Client profile with risk tolerance
        risk_analysis: Risk analysis with portfolio risk rating

    Returns:
        Risk fit score (0-100)
    """
    client_risk = client_profile.risk_tolerance
    portfolio_risk = risk_analysis.risk_rating

    # Define scoring matrix
    # [Client Risk][Portfolio Risk] = Score
    scoring_matrix = {
        RiskTolerance.CONSERVATIVE: {
            RiskRating.LOW: 100,
            RiskRating.MEDIUM: 70,
            RiskRating.HIGH: 40,
            RiskRating.VERY_HIGH: 30,
        },
        RiskTolerance.MODERATE: {
            RiskRating.LOW: 75,
            RiskRating.MEDIUM: 100,
            RiskRating.HIGH: 75,
            RiskRating.VERY_HIGH: 50,
        },
        RiskTolerance.AGGRESSIVE: {
            RiskRating.LOW: 60,
            RiskRating.MEDIUM: 80,
            RiskRating.HIGH: 100,
            RiskRating.VERY_HIGH: 100,
        },
    }

    # Get score from matrix
    base_score = scoring_matrix[client_risk][portfolio_risk]

    # Adjust score based on beta (market sensitivity)
    # Beta > 1.3 = more volatile than market (reduce score for conservative clients)
    # Beta < 0.7 = less volatile than market (reduce score for aggressive clients)
    beta = risk_analysis.beta

    if client_risk == RiskTolerance.CONSERVATIVE and beta > 1.3:
        base_score = max(30, base_score - 10)  # Penalize high market sensitivity
    elif client_risk == RiskTolerance.AGGRESSIVE and beta < 0.7:
        base_score = max(60, base_score - 10)  # Penalize low market sensitivity

    return float(base_score)


def calculate_compliance_fit_score(compliance_report: ComplianceReport) -> float:
    """
    Calculate compliance fit score (0-100) based on compliance status.

    PASS status = 100 points
    REVIEW status = 70 points
    FAIL status = 30 points

    Args:
        compliance_report: Compliance analysis results

    Returns:
        Compliance fit score (0-100)
    """
    status = compliance_report.overall_status

    # Base score from compliance status
    status_scores = {
        ComplianceStatus.PASS: 100,
        ComplianceStatus.REVIEW: 70,
        ComplianceStatus.FAIL: 30,
    }

    base_score = status_scores[status]

    # Adjust for specific check failures
    # If suitability check failed, reduce score significantly
    if not compliance_report.suitability_pass:
        base_score = min(base_score, 40)

    # If concentration limits failed, reduce score
    if not compliance_report.concentration_limits_pass:
        base_score = max(30, base_score - 15)

    return float(base_score)


def calculate_performance_fit_score(performance_report: PerformanceReport) -> float:
    """
    Calculate performance fit score (0-100) based on excess returns vs benchmark.

    Excess return >5% = 100 points
    Excess return 2-5% = 85 points
    Excess return 0-2% = 70 points
    Excess return -2-0% = 50 points
    Excess return <-2% = 30 points

    Args:
        performance_report: Performance analysis results

    Returns:
        Performance fit score (0-100)
    """
    excess_return = performance_report.excess_return

    # Score based on excess return thresholds
    if excess_return > 5.0:
        score = 100
    elif excess_return >= 2.0:
        score = 85
    elif excess_return >= 0.0:
        score = 70
    elif excess_return >= -2.0:
        score = 50
    else:
        score = 30

    # Adjust for Sharpe ratio (risk-adjusted returns)
    # Sharpe > 1.0 = excellent risk-adjusted returns (bonus)
    # Sharpe < 0.5 = poor risk-adjusted returns (penalty)
    sharpe = performance_report.sharpe_ratio

    if sharpe > 1.0:
        score = min(100, score + 5)  # Bonus for high Sharpe
    elif sharpe < 0.5:
        score = max(30, score - 10)  # Penalty for low Sharpe

    return float(score)


def calculate_time_horizon_fit_score(
    client_profile: ClientProfile, risk_analysis: RiskAnalysis
) -> float:
    """
    Calculate time horizon fit score (0-100) based on volatility vs time horizon.

    Long horizon (>15yr) + high volatility = OK (100 points)
    Medium horizon (5-15yr) + medium volatility = OK (100 points)
    Short horizon (<5yr) + high volatility = BAD (40 points)

    Principle: Longer time horizons can tolerate higher volatility.

    Args:
        client_profile: Client profile with time horizon
        risk_analysis: Risk analysis with volatility

    Returns:
        Time horizon fit score (0-100)
    """
    time_horizon = client_profile.time_horizon
    volatility = risk_analysis.volatility

    # Define volatility thresholds
    # Low volatility: <10%
    # Medium volatility: 10-20%
    # High volatility: >20%

    if time_horizon > 15:
        # Long time horizon - can handle high volatility
        if volatility > 20:
            score = 100  # Perfect - time to recover from volatility
        elif volatility > 10:
            score = 95
        else:
            score = 85  # Slightly conservative for long horizon
    elif time_horizon >= 5:
        # Medium time horizon - moderate volatility preferred
        if volatility > 20:
            score = 70  # Acceptable but risky
        elif volatility > 10:
            score = 100  # Perfect match
        else:
            score = 90  # Good match
    else:
        # Short time horizon - low volatility required
        if volatility > 20:
            score = 40  # Poor match - too risky
        elif volatility > 10:
            score = 60  # Marginal - some risk
        else:
            score = 100  # Perfect - capital preservation

    return float(score)


def generate_suitability_explanation(
    overall_score: float,
    risk_fit: float,
    compliance_fit: float,
    performance_fit: float,
    time_horizon_fit: float,
    client_profile: ClientProfile,
    risk_analysis: RiskAnalysis,
    compliance_report: ComplianceReport,
    performance_report: PerformanceReport,
) -> str:
    """
    Generate detailed explanation of suitability scoring.

    Explains why the score was calculated and highlights key factors
    (both positive and negative).

    Args:
        overall_score: Overall suitability score
        risk_fit: Risk fit component score
        compliance_fit: Compliance fit component score
        performance_fit: Performance fit component score
        time_horizon_fit: Time horizon fit component score
        client_profile: Client profile
        risk_analysis: Risk analysis results
        compliance_report: Compliance report
        performance_report: Performance report

    Returns:
        Detailed explanation string
    """
    explanation_parts: List[str] = []

    # Overall interpretation
    if overall_score >= 80:
        explanation_parts.append(
            f"This portfolio is HIGHLY SUITABLE (score: {overall_score:.1f}/100) for the client."
        )
    elif overall_score >= 60:
        explanation_parts.append(
            f"This portfolio is SUITABLE (score: {overall_score:.1f}/100) for the client."
        )
    elif overall_score >= 40:
        explanation_parts.append(
            f"This portfolio is a MARGINAL FIT (score: {overall_score:.1f}/100) for the client."
        )
    else:
        explanation_parts.append(
            f"This portfolio is NOT SUITABLE (score: {overall_score:.1f}/100) for the client."
        )

    # Risk fit explanation
    client_risk = client_profile.risk_tolerance.value
    portfolio_risk = risk_analysis.risk_rating.value

    if risk_fit >= 85:
        explanation_parts.append(
            f"RISK ALIGNMENT ({risk_fit:.0f}/100): Excellent match - {client_risk} client with {portfolio_risk} risk portfolio."
        )
    elif risk_fit >= 70:
        explanation_parts.append(
            f"RISK ALIGNMENT ({risk_fit:.0f}/100): Good match - {client_risk} client with {portfolio_risk} risk portfolio."
        )
    else:
        explanation_parts.append(
            f"RISK ALIGNMENT ({risk_fit:.0f}/100): Concern - {client_risk} client may be uncomfortable with {portfolio_risk} risk portfolio (beta: {risk_analysis.beta:.2f})."
        )

    # Compliance fit explanation
    compliance_status = compliance_report.overall_status.value

    if compliance_fit >= 95:
        explanation_parts.append(
            f"COMPLIANCE ({compliance_fit:.0f}/100): All checks passed ({compliance_status})."
        )
    elif compliance_fit >= 70:
        explanation_parts.append(
            f"COMPLIANCE ({compliance_fit:.0f}/100): Status is {compliance_status} - review recommended."
        )
    else:
        violations = (
            ", ".join(compliance_report.violations)
            if compliance_report.violations
            else "multiple issues"
        )
        explanation_parts.append(
            f"COMPLIANCE ({compliance_fit:.0f}/100): CONCERN - {compliance_status} status due to {violations}."
        )

    # Performance fit explanation
    excess_return = performance_report.excess_return

    if performance_fit >= 85:
        explanation_parts.append(
            f"PERFORMANCE ({performance_fit:.0f}/100): Strong results - outperforming benchmark by {excess_return:+.2f}% (Sharpe: {performance_report.sharpe_ratio:.2f})."
        )
    elif performance_fit >= 70:
        explanation_parts.append(
            f"PERFORMANCE ({performance_fit:.0f}/100): Meeting expectations - tracking benchmark with {excess_return:+.2f}% excess return."
        )
    else:
        explanation_parts.append(
            f"PERFORMANCE ({performance_fit:.0f}/100): Underperforming benchmark by {abs(excess_return):.2f}% with Sharpe ratio of {performance_report.sharpe_ratio:.2f}."
        )

    # Time horizon fit explanation
    time_horizon = client_profile.time_horizon
    volatility = risk_analysis.volatility

    if time_horizon_fit >= 90:
        explanation_parts.append(
            f"TIME HORIZON ({time_horizon_fit:.0f}/100): Excellent match - {time_horizon}-year timeline aligns well with {volatility:.1f}% volatility."
        )
    elif time_horizon_fit >= 70:
        explanation_parts.append(
            f"TIME HORIZON ({time_horizon_fit:.0f}/100): Acceptable - {time_horizon}-year timeline can handle {volatility:.1f}% volatility."
        )
    else:
        explanation_parts.append(
            f"TIME HORIZON ({time_horizon_fit:.0f}/100): CONCERN - {time_horizon}-year timeline may be too short for {volatility:.1f}% volatility."
        )

    return " ".join(explanation_parts)


def map_score_to_interpretation(overall_score: float) -> SuitabilityRating:
    """
    Map overall suitability score to interpretation category.

    80-100: Highly Suitable
    60-79: Suitable
    40-59: Marginal Fit
    0-39: Not Suitable

    Args:
        overall_score: Overall suitability score (0-100)

    Returns:
        Suitability rating enum
    """
    if overall_score >= 80:
        return SuitabilityRating.HIGHLY_SUITABLE
    elif overall_score >= 60:
        return SuitabilityRating.SUITABLE
    elif overall_score >= 40:
        return SuitabilityRating.MARGINAL_FIT
    else:
        return SuitabilityRating.NOT_SUITABLE


# ============================================================================
# Main Suitability Scoring Function
# ============================================================================


def calculate_suitability_score(
    client_profile: ClientProfile,
    risk_analysis: RiskAnalysis,
    compliance_report: ComplianceReport,
    performance_report: PerformanceReport,
) -> SuitabilityScore:
    """
    Calculate client-portfolio suitability score.

    Combines inputs from Risk Analyst, Compliance Officer, and Performance Analyst
    to produce a weighted suitability score (0-100) with detailed explanation.

    Weighting:
    - Risk Fit: 25%
    - Compliance Fit: 35%
    - Performance Fit: 25%
    - Time Horizon Fit: 15%

    Args:
        client_profile: Client profile with demographics and risk tolerance
        risk_analysis: Risk analysis results from Risk Analyst agent
        compliance_report: Compliance check results from Compliance Officer agent
        performance_report: Performance analysis results from Performance Analyst agent

    Returns:
        SuitabilityScore with overall score, component scores, interpretation, and explanation

    Example:
        >>> client = ClientProfile(
        ...     client_id="C001",
        ...     age=45,
        ...     risk_tolerance=RiskTolerance.MODERATE,
        ...     investment_goals=["Retirement"],
        ...     time_horizon=20
        ... )
        >>> risk = RiskAnalysis(
        ...     volatility=15.0,
        ...     var_95=-12.5,
        ...     beta=1.1,
        ...     concentration_score=30.0,
        ...     risk_rating=RiskRating.MEDIUM
        ... )
        >>> compliance = ComplianceReport(
        ...     status=ComplianceStatus.PASS,
        ...     checks_performed=["Suitability", "Concentration"],
        ...     suitability_pass=True,
        ...     concentration_limits_pass=True
        ... )
        >>> performance = PerformanceReport(
        ...     total_return=12.5,
        ...     benchmark_return=10.0,
        ...     excess_return=2.5,
        ...     sharpe_ratio=1.2
        ... )
        >>> score = calculate_suitability_score(client, risk, compliance, performance)
        >>> print(score.overall_score)  # ~85-90 (Highly Suitable)
        >>> print(score.interpretation)  # SuitabilityRating.HIGHLY_SUITABLE
    """
    # Calculate component scores
    risk_fit = calculate_risk_fit_score(client_profile, risk_analysis)
    compliance_fit = calculate_compliance_fit_score(compliance_report)
    performance_fit = calculate_performance_fit_score(performance_report)
    time_horizon_fit = calculate_time_horizon_fit_score(client_profile, risk_analysis)

    # Calculate weighted overall score
    # Risk: 25%, Compliance: 35%, Performance: 25%, Time Horizon: 15%
    overall_score = (
        (risk_fit * 0.25)
        + (compliance_fit * 0.35)
        + (performance_fit * 0.25)
        + (time_horizon_fit * 0.15)
    )

    # Map score to interpretation
    interpretation = map_score_to_interpretation(overall_score)

    # Generate detailed explanation
    explanation = generate_suitability_explanation(
        overall_score=overall_score,
        risk_fit=risk_fit,
        compliance_fit=compliance_fit,
        performance_fit=performance_fit,
        time_horizon_fit=time_horizon_fit,
        client_profile=client_profile,
        risk_analysis=risk_analysis,
        compliance_report=compliance_report,
        performance_report=performance_report,
    )

    # Return SuitabilityScore model
    return SuitabilityScore(
        overall_score=overall_score,
        risk_fit=risk_fit,
        compliance_fit=compliance_fit,
        performance_fit=performance_fit,
        time_horizon_fit=time_horizon_fit,
        interpretation=interpretation,
        explanation=explanation,
    )
