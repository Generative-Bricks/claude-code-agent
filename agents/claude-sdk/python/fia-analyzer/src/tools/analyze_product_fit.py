"""
Analyze Product Fit Tool

This tool analyzes FIA product suitability for a client using the 40-question framework.
For MVP, implements 10 key questions covering the most critical suitability factors.

Biblical Principle: HONOR - Client-first analysis with transparent reasoning for every decision.
Biblical Principle: EXCELLENCE - Production-grade suitability scoring with clear methodology.
"""

import logging
from typing import List

from src.models.fia_product import FIAProduct
from src.models.client_profile import ClientProfile
from src.models.suitability_score import SuitabilityScore, QuestionResult

# Configure logging
logger = logging.getLogger(__name__)


def analyze_product_fit(product: FIAProduct, client_profile: ClientProfile) -> SuitabilityScore:
    """
    Analyze FIA product suitability for a client using a structured question framework.

    Implements a subset of the 40-question suitability framework, focusing on the
    most critical factors for FIA suitability determination. Uses the scoring methodology:
    - Score = (Total YES / Total Answerable) × 100
    - N/A answers are excluded from scoring (insufficient data)

    The analysis covers:
    1. Financial Capacity (minimum premium, asset sufficiency)
    2. Time Horizon (term commitment, liquidity needs)
    3. Risk Tolerance (principal protection, volatility concerns)
    4. Investment Objectives (income needs, growth expectations)
    5. Understanding (product complexity, surrender charges)

    Args:
        product: FIAProduct model with complete product information
        client_profile: ClientProfile model with client financial and personal data

    Returns:
        SuitabilityScore: Complete suitability analysis with scoring, breakdown, and recommendations

    Raises:
        ValueError: If product or client_profile is None

    Example:
        >>> product = FIAProduct(name="Allianz Benefit Control", minimum_premium=25000, ...)
        >>> client = ClientProfile(age=62, total_investable_assets=500000, ...)
        >>> score = analyze_product_fit(product, client)
        >>> print(f"{score.score}% - {score.interpretation}")
        "85.71% - Highly Suitable"
    """
    # Biblical Principle: EXCELLENCE - Validate inputs from the start
    if product is None:
        raise ValueError("Product cannot be None")
    if client_profile is None:
        raise ValueError("Client profile cannot be None")

    logger.info(f"Analyzing product fit: {product.name} for client "
                f"(age: {client_profile.age or 'unknown'})")

    # Initialize question results list
    questions: List[QuestionResult] = []

    # === CATEGORY 1: Financial Capacity & Commitment ===

    # Q1: Does client meet minimum premium requirement?
    if client_profile.total_investable_assets is not None and product.minimum_premium is not None:
        if client_profile.total_investable_assets >= product.minimum_premium:
            questions.append(QuestionResult(
                question_id=1,
                question_text=f"Does the client have sufficient assets to meet the minimum premium of ${product.minimum_premium:,.0f}?",
                answer="YES",
                rationale=f"Client has ${client_profile.total_investable_assets:,.0f} in investable assets, "
                         f"which exceeds the ${product.minimum_premium:,.0f} minimum premium requirement.",
                category="Financial Capacity & Commitment"
            ))
        else:
            questions.append(QuestionResult(
                question_id=1,
                question_text=f"Does the client have sufficient assets to meet the minimum premium of ${product.minimum_premium:,.0f}?",
                answer="NO",
                rationale=f"Client has only ${client_profile.total_investable_assets:,.0f} in investable assets, "
                         f"which is below the ${product.minimum_premium:,.0f} minimum premium requirement.",
                category="Financial Capacity & Commitment"
            ))
    else:
        questions.append(QuestionResult(
            question_id=1,
            question_text="Does the client have sufficient assets to meet the minimum premium?",
            answer="N/A",
            rationale="Client asset information or product minimum premium not available.",
            category="Financial Capacity & Commitment"
        ))

    # Q2: Is the proposed premium a reasonable percentage of client's portfolio?
    if (client_profile.proposed_premium_amount is not None and
        client_profile.total_investable_assets is not None and
        client_profile.total_investable_assets > 0):
        percentage = (client_profile.proposed_premium_amount / client_profile.total_investable_assets) * 100
        if percentage <= 50:  # Biblical Principle: HONOR - Don't over-concentrate
            questions.append(QuestionResult(
                question_id=2,
                question_text="Is the proposed premium a reasonable percentage of the client's total assets (≤50%)?",
                answer="YES",
                rationale=f"Proposed premium of ${client_profile.proposed_premium_amount:,.0f} represents "
                         f"{percentage:.1f}% of total investable assets, which is within reasonable limits.",
                category="Financial Capacity & Commitment"
            ))
        else:
            questions.append(QuestionResult(
                question_id=2,
                question_text="Is the proposed premium a reasonable percentage of the client's total assets (≤50%)?",
                answer="NO",
                rationale=f"Proposed premium of ${client_profile.proposed_premium_amount:,.0f} represents "
                         f"{percentage:.1f}% of total investable assets, which is too high (over 50%).",
                category="Financial Capacity & Commitment"
            ))
    else:
        questions.append(QuestionResult(
            question_id=2,
            question_text="Is the proposed premium a reasonable percentage of the client's total assets?",
            answer="N/A",
            rationale="Proposed premium amount or total assets not available.",
            category="Financial Capacity & Commitment"
        ))

    # Q3: Does client have emergency reserves outside this investment?
    if client_profile.has_emergency_fund is not None:
        if client_profile.has_emergency_fund:
            questions.append(QuestionResult(
                question_id=3,
                question_text="Does the client have 3-6 months of emergency reserves outside this investment?",
                answer="YES",
                rationale="Client confirmed having adequate emergency reserves.",
                category="Financial Capacity & Commitment"
            ))
        else:
            questions.append(QuestionResult(
                question_id=3,
                question_text="Does the client have 3-6 months of emergency reserves outside this investment?",
                answer="NO",
                rationale="Client does not have adequate emergency reserves. This is a significant concern.",
                category="Financial Capacity & Commitment"
            ))
    else:
        questions.append(QuestionResult(
            question_id=3,
            question_text="Does the client have 3-6 months of emergency reserves outside this investment?",
            answer="N/A",
            rationale="Emergency fund status not documented.",
            category="Financial Capacity & Commitment"
        ))

    # === CATEGORY 2: Time Horizon & Liquidity ===

    # Q4: Can client commit funds for the full contract term?
    if client_profile.can_commit_funds_for_term is not None:
        if client_profile.can_commit_funds_for_term:
            questions.append(QuestionResult(
                question_id=4,
                question_text=f"Can the client commit funds for the full {product.contract_term}-year surrender period?",
                answer="YES",
                rationale=f"Client confirmed ability to commit funds for {product.contract_term} years.",
                category="Time Horizon & Liquidity"
            ))
        else:
            questions.append(QuestionResult(
                question_id=4,
                question_text=f"Can the client commit funds for the full {product.contract_term}-year surrender period?",
                answer="NO",
                rationale=f"Client cannot commit to {product.contract_term}-year term. This is a major concern.",
                category="Time Horizon & Liquidity"
            ))
    else:
        questions.append(QuestionResult(
            question_id=4,
            question_text=f"Can the client commit funds for the full {product.contract_term}-year surrender period?",
            answer="N/A",
            rationale="Client's commitment ability not documented.",
            category="Time Horizon & Liquidity"
        ))

    # Q5: Does client need liquidity in the near term (2-3 years)?
    if client_profile.needs_liquidity_near_term is not None:
        if not client_profile.needs_liquidity_near_term:  # NOT needing liquidity is positive
            questions.append(QuestionResult(
                question_id=5,
                question_text="Is the client free from near-term liquidity needs (next 2-3 years)?",
                answer="YES",
                rationale="Client does not anticipate significant liquidity needs in the near term.",
                category="Time Horizon & Liquidity"
            ))
        else:
            questions.append(QuestionResult(
                question_id=5,
                question_text="Is the client free from near-term liquidity needs (next 2-3 years)?",
                answer="NO",
                rationale="Client needs liquidity in next 2-3 years, which conflicts with surrender charges.",
                category="Time Horizon & Liquidity"
            ))
    else:
        questions.append(QuestionResult(
            question_id=5,
            question_text="Is the client free from near-term liquidity needs?",
            answer="N/A",
            rationale="Near-term liquidity needs not documented.",
            category="Time Horizon & Liquidity"
        ))

    # === CATEGORY 3: Risk Tolerance & Investment Style ===

    # Q6: Does client prioritize principal protection?
    if client_profile.seeks_principal_protection is not None:
        if client_profile.seeks_principal_protection:
            questions.append(QuestionResult(
                question_id=6,
                question_text="Does the client prioritize principal protection from market downturns?",
                answer="YES",
                rationale="Client seeks principal protection, which aligns well with FIA structure.",
                category="Risk Tolerance & Investment Style"
            ))
        else:
            questions.append(QuestionResult(
                question_id=6,
                question_text="Does the client prioritize principal protection from market downturns?",
                answer="NO",
                rationale="Client does not prioritize principal protection. May prefer higher-risk investments.",
                category="Risk Tolerance & Investment Style"
            ))
    else:
        questions.append(QuestionResult(
            question_id=6,
            question_text="Does the client prioritize principal protection from market downturns?",
            answer="N/A",
            rationale="Principal protection preference not documented.",
            category="Risk Tolerance & Investment Style"
        ))

    # Q7: Is client's risk tolerance conservative or moderate?
    if client_profile.risk_tolerance is not None:
        risk_lower = client_profile.risk_tolerance.lower()
        if risk_lower in ["conservative", "moderate"]:
            questions.append(QuestionResult(
                question_id=7,
                question_text="Is the client's risk tolerance conservative or moderate (not aggressive)?",
                answer="YES",
                rationale=f"Client's {client_profile.risk_tolerance} risk tolerance aligns well with FIA products.",
                category="Risk Tolerance & Investment Style"
            ))
        else:
            questions.append(QuestionResult(
                question_id=7,
                question_text="Is the client's risk tolerance conservative or moderate (not aggressive)?",
                answer="NO",
                rationale=f"Client's {client_profile.risk_tolerance} risk tolerance may be too aggressive for FIAs.",
                category="Risk Tolerance & Investment Style"
            ))
    else:
        questions.append(QuestionResult(
            question_id=7,
            question_text="Is the client's risk tolerance conservative or moderate?",
            answer="N/A",
            rationale="Risk tolerance not documented.",
            category="Risk Tolerance & Investment Style"
        ))

    # === CATEGORY 4: Investment Objectives ===

    # Q8: Does client want guaranteed lifetime income?
    if client_profile.wants_guaranteed_lifetime_income is not None:
        if client_profile.wants_guaranteed_lifetime_income:
            questions.append(QuestionResult(
                question_id=8,
                question_text="Does the client want guaranteed lifetime income?",
                answer="YES",
                rationale="Client desires guaranteed lifetime income, which FIAs with income riders can provide.",
                category="Investment Objectives"
            ))
        else:
            questions.append(QuestionResult(
                question_id=8,
                question_text="Does the client want guaranteed lifetime income?",
                answer="NO",
                rationale="Client does not prioritize guaranteed lifetime income. May prefer accumulation-focused products.",
                category="Investment Objectives"
            ))
    else:
        questions.append(QuestionResult(
            question_id=8,
            question_text="Does the client want guaranteed lifetime income?",
            answer="N/A",
            rationale="Lifetime income preference not documented.",
            category="Investment Objectives"
        ))

    # Q9: Is client comfortable with realistic FIA returns (3-6% annually)?
    if client_profile.comfortable_with_expected_returns is not None:
        if client_profile.comfortable_with_expected_returns:
            questions.append(QuestionResult(
                question_id=9,
                question_text="Is the client comfortable with realistic FIA return expectations (3-6% annually)?",
                answer="YES",
                rationale="Client has appropriate return expectations for FIA products.",
                category="Investment Objectives"
            ))
        else:
            questions.append(QuestionResult(
                question_id=9,
                question_text="Is the client comfortable with realistic FIA return expectations (3-6% annually)?",
                answer="NO",
                rationale="Client expects returns higher than typical FIA performance. Major concern.",
                category="Investment Objectives"
            ))
    else:
        questions.append(QuestionResult(
            question_id=9,
            question_text="Is the client comfortable with realistic FIA return expectations?",
            answer="N/A",
            rationale="Return expectations not documented.",
            category="Investment Objectives"
        ))

    # === CATEGORY 5: Product Understanding ===

    # Q10: Does client understand this is not a direct market investment?
    if client_profile.understands_not_direct_market_investment is not None:
        if client_profile.understands_not_direct_market_investment:
            questions.append(QuestionResult(
                question_id=10,
                question_text="Does the client understand this is not a direct market investment?",
                answer="YES",
                rationale="Client understands FIA structure and how it differs from direct market investments.",
                category="Product Understanding"
            ))
        else:
            questions.append(QuestionResult(
                question_id=10,
                question_text="Does the client understand this is not a direct market investment?",
                answer="NO",
                rationale="Client does not fully understand FIA structure. Education required before proceeding.",
                category="Product Understanding"
            ))
    else:
        questions.append(QuestionResult(
            question_id=10,
            question_text="Does the client understand this is not a direct market investment?",
            answer="N/A",
            rationale="Client's product understanding not documented.",
            category="Product Understanding"
        ))

    # Biblical Principle: TRUTH - Calculate totals transparently
    total_yes = sum(1 for q in questions if q.answer == "YES")
    total_no = sum(1 for q in questions if q.answer == "NO")
    total_na = sum(1 for q in questions if q.answer == "N/A")

    logger.info(f"Analysis complete: {total_yes} YES, {total_no} NO, {total_na} N/A")

    # Build good fit factors (from YES answers)
    good_fit_factors = [
        q.rationale for q in questions if q.answer == "YES"
    ]

    # Build concerns (from NO answers)
    not_a_fit_factors = [
        q.rationale for q in questions if q.answer == "NO"
    ]

    # Generate recommendations based on concerns
    recommendations = []
    if total_no > 0:
        recommendations.append(f"Address all {total_no} concerns identified in the NO answers before proceeding")
    if total_na > 5:
        recommendations.append(f"Gather missing client information ({total_na} N/A answers) for complete assessment")

    # Specific recommendations based on question results
    if any("emergency" in q.rationale.lower() and q.answer == "NO" for q in questions):
        recommendations.append("Client should establish emergency fund before investing in illiquid annuity")
    if any("liquidity" in q.rationale.lower() and q.answer == "NO" for q in questions):
        recommendations.append("Discuss surrender charge schedule in detail and explore products with shorter terms")
    if any("return" in q.rationale.lower() and q.answer == "NO" for q in questions):
        recommendations.append("Reset client expectations about realistic FIA returns (3-6% annually)")
    if any("understanding" in q.rationale.lower() and q.answer == "NO" for q in questions):
        recommendations.append("Provide comprehensive product education before proceeding with application")

    # If highly suitable, add positive recommendations
    score_value = (total_yes / (total_yes + total_no) * 100) if (total_yes + total_no) > 0 else 0
    if score_value >= 80:
        recommendations.append("Proceed with product application and discuss index allocation strategies")
        recommendations.append("Review rider options to optimize income and protection benefits")

    # Biblical Principle: EXCELLENCE - Return complete, production-ready analysis
    try:
        suitability_score = SuitabilityScore(
            total_yes=total_yes,
            total_no=total_no,
            total_na=total_na,
            question_breakdown=questions,
            good_fit_factors=good_fit_factors,
            not_a_fit_factors=not_a_fit_factors,
            recommendations=recommendations if recommendations else ["Complete missing data and re-analyze"],
            product_name=product.name,
            client_name=None,  # Not provided in ClientProfile
            analyst_notes=f"Analysis based on {len(questions)} key suitability questions"
        )
        logger.info(f"Suitability analysis complete: {suitability_score.score}% - {suitability_score.interpretation}")
        return suitability_score
    except Exception as e:
        logger.error(f"Error building suitability score: {e}")
        raise RuntimeError(f"Failed to build suitability score: {e}")
