"""
Data Models Package

This package contains all Pydantic data models for the FIA Analyzer agent.

Models:
- FIAProduct: Complete FIA product representation with all features and rates
- ClientProfile: Client information for suitability analysis
- SuitabilityScore: Results from 40-question suitability assessment

Biblical Principle: TRUTH - All data structures are explicit, typed, and verifiable.
"""

from .fia_product import (
    FIAProduct,
    SurrenderCharge,
    IndexOption,
    CurrentRate,
    Rider,
    CommissionStructure,
    CompanyInfo,
)
from .client_profile import ClientProfile
from .suitability_score import SuitabilityScore, QuestionResult

__all__ = [
    # Main models
    "FIAProduct",
    "ClientProfile",
    "SuitabilityScore",
    # Supporting models
    "QuestionResult",
    "SurrenderCharge",
    "IndexOption",
    "CurrentRate",
    "Rider",
    "CommissionStructure",
    "CompanyInfo",
]
