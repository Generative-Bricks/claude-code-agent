"""
FIA Analyzer Tools Module

This module exports all custom tools for the FIA Analyzer agent.

Tools:
- search_fia_products: Search for FIA products using web search
- extract_fia_rates: Parse FIA rate data from markdown content
- analyze_product_fit: Analyze FIA product suitability for a client

Biblical Principle: SERVE - Simple, clear exports that make developer experience easier.
"""

from src.tools.search_fia_products import search_fia_products
from src.tools.extract_fia_rates import extract_fia_rates
from src.tools.analyze_product_fit import analyze_product_fit

__all__ = [
    "search_fia_products",
    "extract_fia_rates",
    "analyze_product_fit",
]
