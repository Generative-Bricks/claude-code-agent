"""
Suitability Score Model

This module defines the Pydantic models for FIA suitability analysis results
based on the 40-question framework.

Biblical Principle: EXCELLENCE - Production-grade scoring with clear methodology
and transparent reasoning for every recommendation.
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field, computed_field


class QuestionResult(BaseModel):
    """Result for a single question in the suitability assessment."""

    question_id: int = Field(description="Question number (1-40)")
    question_text: str = Field(description="The full question text")
    answer: Literal["YES", "NO", "N/A"] = Field(
        description="Answer: YES = suitable factor, NO = concern, N/A = insufficient data"
    )
    rationale: str = Field(
        description="Explanation for why this answer was given"
    )
    category: str = Field(
        description="Question category (e.g., 'Financial Capacity', 'Risk Tolerance')"
    )


class SuitabilityScore(BaseModel):
    """
    Complete suitability analysis result for a client-product match.

    Uses the scoring methodology from the FIA Analysis Skill:
    - Score = (Total YES / Total Answerable) × 100
    - Only YES and NO answers count as "answerable"
    - N/A answers are excluded from scoring

    Interpretation Ranges:
    - 80-100%: Highly Suitable
    - 60-79%: Suitable (with discussion of concerns)
    - 40-59%: Marginal Fit (detailed discussion required)
    - Below 40%: Not Suitable

    Example:
        ```python
        score = SuitabilityScore(
            total_yes=28,
            total_no=5,
            total_na=7,
            question_breakdown=[...],
            good_fit_factors=[
                "Client seeks principal protection",
                "Conservative risk tolerance aligns with FIA structure"
            ],
            not_a_fit_factors=[
                "Client may need lump sum in 3 years"
            ],
            recommendations=[
                "Discuss liquidity needs in detail",
                "Ensure client understands surrender charges"
            ]
        )
        print(score.score)  # 84.85
        print(score.interpretation)  # "Highly Suitable"
        ```
    """

    # === Raw Counts ===
    total_yes: int = Field(
        description="Number of YES answers (favorable factors)"
    )
    total_no: int = Field(
        description="Number of NO answers (concerns or disqualifiers)"
    )
    total_na: int = Field(
        description="Number of N/A answers (insufficient data to answer)"
    )

    # === Question-by-Question Breakdown ===
    question_breakdown: List[QuestionResult] = Field(
        description="Detailed results for each of the 40 questions"
    )

    # === Analysis Summary ===
    good_fit_factors: List[str] = Field(
        description="List of factors that make this product a good fit for the client"
    )
    not_a_fit_factors: List[str] = Field(
        description="List of concerns or factors that suggest poor fit"
    )
    recommendations: List[str] = Field(
        description="Specific recommendations based on the analysis"
    )

    # === Additional Context ===
    product_name: str = Field(
        description="Name of the FIA product being evaluated"
    )
    client_name: Optional[str] = Field(
        default=None,
        description="Client name (if available)"
    )
    analyst_notes: Optional[str] = Field(
        default=None,
        description="Additional notes from the analyst or system"
    )

    @computed_field
    @property
    def total_answerable(self) -> int:
        """
        Total number of answerable questions (excludes N/A).

        Returns:
            Sum of YES and NO answers
        """
        return self.total_yes + self.total_no

    @computed_field
    @property
    def score(self) -> float:
        """
        Calculate the suitability score.

        Formula: (Total YES / Total Answerable) × 100

        Returns:
            Suitability score as a percentage (0-100)
        """
        if self.total_answerable == 0:
            return 0.0
        return round((self.total_yes / self.total_answerable) * 100, 2)

    @computed_field
    @property
    def interpretation(self) -> str:
        """
        Interpret the suitability score.

        Returns:
            One of: "Highly Suitable", "Suitable", "Marginal Fit", "Not Suitable"
        """
        score = self.score
        if score >= 80:
            return "Highly Suitable"
        elif score >= 60:
            return "Suitable"
        elif score >= 40:
            return "Marginal Fit"
        else:
            return "Not Suitable"

    @computed_field
    @property
    def recommendation_action(self) -> str:
        """
        Get the recommended action based on the score.

        Returns:
            Action recommendation string
        """
        score = self.score
        if score >= 90:
            return "Strong alignment - Proceed with application and discuss allocation selections"
        elif score >= 75:
            return "Good fit with minor concerns - Address NO answers before proceeding"
        elif score >= 60:
            return "Suitable but ensure client fully understands limitations"
        elif score >= 40:
            return "Mixed fit - Deep dive into concerns required. Consider alternatives"
        else:
            return "Not suitable - Recommend alternative products. Do NOT proceed"

    def get_questions_by_category(self, category: str) -> List[QuestionResult]:
        """
        Get all questions for a specific category.

        Args:
            category: Category name (e.g., "Risk Tolerance")

        Returns:
            List of QuestionResult objects for that category
        """
        return [q for q in self.question_breakdown if q.category == category]

    def get_questions_by_answer(self, answer: Literal["YES", "NO", "N/A"]) -> List[QuestionResult]:
        """
        Get all questions with a specific answer.

        Args:
            answer: Answer type to filter by

        Returns:
            List of QuestionResult objects with that answer
        """
        return [q for q in self.question_breakdown if q.answer == answer]

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "total_yes": 28,
                "total_no": 5,
                "total_na": 7,
                "product_name": "Allianz Benefit Control",
                "question_breakdown": [
                    {
                        "question_id": 1,
                        "question_text": "Does the client have at least $25,000 available to invest?",
                        "answer": "YES",
                        "rationale": "Client has $100,000 proposed premium",
                        "category": "Financial Capacity & Commitment"
                    },
                    {
                        "question_id": 2,
                        "question_text": "Can the client commit these funds for at least 10 years?",
                        "answer": "NO",
                        "rationale": "Client may need funds in 3 years for home purchase",
                        "category": "Financial Capacity & Commitment"
                    }
                ],
                "good_fit_factors": [
                    "Client seeks principal protection",
                    "Conservative risk tolerance",
                    "Has adequate emergency reserves"
                ],
                "not_a_fit_factors": [
                    "May need liquidity in 3 years",
                    "Unclear understanding of surrender charges"
                ],
                "recommendations": [
                    "Discuss surrender charge schedule in detail",
                    "Explore products with shorter surrender periods",
                    "Ensure free withdrawal provision is understood"
                ]
            }
        }


# Optional type alias for clarity
from typing import Optional

__all__ = ["SuitabilityScore", "QuestionResult"]
