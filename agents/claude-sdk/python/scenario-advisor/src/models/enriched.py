"""
Enriched scenario models with provenance, temporal context, and actionability metrics.

This module extends the base Scenario model with additional context for:
- Source tracking and reliability
- Temporal urgency and timing
- Confidence scoring with rationale
- Actionability metrics for advisors
"""

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator, computed_field

from .scenario import Scenario


class SourceProvenance(BaseModel):
    """
    Tracks the origin and reliability of scenario information.

    Source types help determine how to weight information:
    - regulatory: High reliability, official guidance
    - news: Medium reliability, requires cross-reference
    - market_data: High reliability for trends
    - expert_analysis: Medium reliability, opinion-based
    - internal: Varies based on internal processes
    """
    source_type: Literal["regulatory", "news", "market_data", "expert_analysis", "internal"]
    source_name: str = Field(..., min_length=1, description="Name of the source (e.g., 'SEC', 'Bloomberg')")
    url: Optional[str] = Field(None, description="URL to source document if available")
    retrieved_at: datetime = Field(default_factory=datetime.now, description="When this information was retrieved")
    reliability_score: float = Field(..., ge=0.0, le=1.0, description="Source reliability (0.0-1.0)")

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: Optional[str]) -> Optional[str]:
        """Ensure URL starts with http/https if provided."""
        if v and not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        return v

    @field_validator("reliability_score")
    @classmethod
    def validate_reliability(cls, v: float, info) -> float:
        """Ensure reliability score is reasonable for source type."""
        source_type = info.data.get("source_type")

        # Regulatory sources should have high reliability
        if source_type == "regulatory" and v < 0.7:
            raise ValueError("Regulatory sources must have reliability >= 0.7")

        # News sources should not claim perfect reliability
        if source_type == "news" and v >= 0.95:
            raise ValueError("News sources should have reliability < 0.95")

        return v


class TemporalContext(BaseModel):
    """
    Captures timing urgency and action windows for scenarios.

    Urgency levels:
    - immediate: Action needed within days (e.g., compliance deadline)
    - short_term: Action within weeks (e.g., upcoming product launch)
    - medium_term: Action within months (e.g., rate changes)
    - long_term: Planning horizon (e.g., demographic trends)
    """
    urgency: Literal["immediate", "short_term", "medium_term", "long_term"]
    trigger_date: Optional[datetime] = Field(None, description="When the scenario becomes active")
    expiration_date: Optional[datetime] = Field(None, description="When the scenario is no longer relevant")
    optimal_action_window_days: Optional[int] = Field(
        None,
        ge=0,
        description="Days before trigger_date for optimal action"
    )
    days_before_event: Optional[int] = Field(
        None,
        description="Days remaining until trigger (negative if past)"
    )
    is_recurring: bool = Field(False, description="Whether this scenario repeats")
    timing_rationale: str = Field(
        ...,
        min_length=10,
        description="Why this urgency level was assigned"
    )

    @field_validator("expiration_date")
    @classmethod
    def validate_expiration(cls, v: Optional[datetime], info) -> Optional[datetime]:
        """Ensure expiration is after trigger date if both provided."""
        trigger = info.data.get("trigger_date")
        if v and trigger and v <= trigger:
            raise ValueError("expiration_date must be after trigger_date")
        return v

    @field_validator("optimal_action_window_days")
    @classmethod
    def validate_action_window(cls, v: Optional[int], info) -> Optional[int]:
        """Ensure action window is reasonable for urgency level."""
        urgency = info.data.get("urgency")

        if v is not None:
            if urgency == "immediate" and v > 30:
                raise ValueError("Immediate urgency should have action window <= 30 days")
            if urgency == "long_term" and v < 90:
                raise ValueError("Long-term urgency should have action window >= 90 days")

        return v


class ConfidenceScore(BaseModel):
    """
    Multi-factor confidence assessment for enriched scenarios.

    Overall confidence is computed from:
    - Source reliability
    - Number of cross-references
    - Internal validation

    Note: Fields are ordered so validators can access dependent fields.
    """
    # These fields must come first so they're available for overall_confidence validation
    source_reliability: float = Field(..., ge=0.0, le=1.0, description="Weighted average of source reliability")
    cross_reference_count: int = Field(..., ge=0, description="Number of independent sources confirming")
    confidence_rationale: str = Field(
        ...,
        min_length=10,
        description="Why this confidence level was assigned"
    )
    # overall_confidence comes last so validator can access other fields
    overall_confidence: float = Field(..., ge=0.0, le=1.0, description="Composite confidence score")

    @field_validator("overall_confidence")
    @classmethod
    def validate_overall_confidence(cls, v: float, info) -> float:
        """Ensure overall confidence aligns with source reliability and cross-references."""
        source_reliability = info.data.get("source_reliability", 0.0)
        cross_ref_count = info.data.get("cross_reference_count", 0)

        # With no cross-references, confidence cannot exceed source reliability
        if cross_ref_count == 0 and v > source_reliability:
            raise ValueError(
                f"Overall confidence ({v}) cannot exceed source reliability ({source_reliability}) "
                "when cross_reference_count is 0"
            )

        # With multiple cross-references, confidence should be reasonably high
        if cross_ref_count >= 3 and v < 0.6:
            raise ValueError(
                f"Overall confidence ({v}) should be >= 0.6 with {cross_ref_count} cross-references"
            )

        return v


class ActionabilityMetrics(BaseModel):
    """
    Quantifies how actionable a scenario is for financial advisors.

    Metrics:
    - specificity_score: How well-defined the action is (0-100)
    - urgency_score: How time-sensitive (0-100)
    - impact_score: Potential revenue/relationship impact (0-100)
    - feasibility_score: How practical to execute (0-100)
    """
    specificity_score: int = Field(..., ge=0, le=100, description="How specific the recommended action is")
    urgency_score: int = Field(..., ge=0, le=100, description="Time sensitivity of the action")
    impact_score: int = Field(..., ge=0, le=100, description="Potential impact on revenue/relationship")
    feasibility_score: int = Field(..., ge=0, le=100, description="How practical to execute")
    recommended_action: str = Field(
        ...,
        min_length=10,
        description="Clear, specific action for advisor to take"
    )
    advisor_talking_points: list[str] = Field(
        ...,
        min_length=1,
        description="Key points for advisor-client conversation"
    )

    @computed_field
    @property
    def composite_score(self) -> float:
        """
        Weighted composite of all actionability metrics.

        Weighting:
        - Specificity: 30% (clear actions are most valuable)
        - Urgency: 25% (timing matters)
        - Impact: 30% (revenue/relationship potential)
        - Feasibility: 15% (must be doable)

        Returns:
            float: Composite score from 0.0-100.0
        """
        return (
            self.specificity_score * 0.30 +
            self.urgency_score * 0.25 +
            self.impact_score * 0.30 +
            self.feasibility_score * 0.15
        )

    @field_validator("advisor_talking_points")
    @classmethod
    def validate_talking_points(cls, v: list[str]) -> list[str]:
        """Ensure all talking points are substantive."""
        if not v:
            raise ValueError("Must provide at least one talking point")

        for point in v:
            if len(point.strip()) < 10:
                raise ValueError(f"Talking point too short (min 10 chars): '{point}'")

        return v


class EnrichedScenario(Scenario):
    """
    Extended scenario model with full enrichment metadata.

    Builds on base Scenario with:
    - Temporal urgency and timing context
    - Multi-source confidence scoring
    - Actionability metrics for advisors
    - Discovery tracking

    This model represents a fully-enriched scenario ready for matching
    against client portfolios.
    """
    temporal_context: TemporalContext
    confidence: ConfidenceScore
    actionability: ActionabilityMetrics
    discovered_at: datetime = Field(default_factory=datetime.now, description="When this scenario was discovered")
    discovered_by: str = Field(
        ...,
        min_length=1,
        description="Process/agent that discovered this scenario"
    )
    sources: list[SourceProvenance] = Field(
        ...,
        min_length=1,
        description="All sources supporting this scenario"
    )

    @field_validator("sources")
    @classmethod
    def validate_sources(cls, v: list[SourceProvenance], info) -> list[SourceProvenance]:
        """Ensure sources align with confidence metrics."""
        if not v:
            raise ValueError("Must have at least one source")

        # Verify source_reliability matches confidence.source_reliability
        confidence = info.data.get("confidence")
        if confidence:
            avg_reliability = sum(s.reliability_score for s in v) / len(v)
            expected_reliability = confidence.source_reliability

            # Allow small floating point variance
            if abs(avg_reliability - expected_reliability) > 0.01:
                raise ValueError(
                    f"Average source reliability ({avg_reliability:.3f}) does not match "
                    f"confidence.source_reliability ({expected_reliability:.3f})"
                )

        return v

    @field_validator("temporal_context")
    @classmethod
    def validate_temporal_alignment(cls, v: TemporalContext, info) -> TemporalContext:
        """Ensure temporal urgency aligns with actionability urgency."""
        actionability = info.data.get("actionability")
        if actionability:
            temporal_urgency = v.urgency
            urgency_score = actionability.urgency_score

            # Immediate urgency should have high urgency score
            if temporal_urgency == "immediate" and urgency_score < 60:
                raise ValueError(
                    f"Immediate temporal urgency requires urgency_score >= 60, got {urgency_score}"
                )

            # Long-term should not have very high urgency score
            if temporal_urgency == "long_term" and urgency_score > 50:
                raise ValueError(
                    f"Long-term temporal urgency should have urgency_score <= 50, got {urgency_score}"
                )

        return v
