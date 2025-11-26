"""
Search FIA Products Tool

This tool searches for Fixed Indexed Annuity products using web search capabilities.
Currently uses mock data for known products with clear integration points for real APIs.

Biblical Principle: TRUTH - Transparent about data sources and clear about mock vs real data.
Biblical Principle: HONOR - Provides honest, verifiable product information.
"""

import logging
from typing import Optional
from pydantic import BaseModel, Field, field_validator

# Configure logging
logger = logging.getLogger(__name__)


class ProductSearchInput(BaseModel):
    """Input schema for FIA product search."""

    product_name: str = Field(
        description="Product name to search for (e.g., 'Allianz Benefit Control')"
    )
    carrier: Optional[str] = Field(
        default=None,
        description="Insurance carrier name to filter results (e.g., 'Allianz Life')"
    )

    @field_validator("product_name")
    @classmethod
    def validate_product_name(cls, v: str) -> str:
        """Validate product name is not empty."""
        if not v or not v.strip():
            raise ValueError("Product name cannot be empty")
        return v.strip()


class ProductSearchResult(BaseModel):
    """Individual product search result."""

    name: str = Field(description="Full product name")
    carrier: str = Field(description="Insurance carrier name")
    url: str = Field(description="URL to product information page")
    summary: str = Field(description="Brief product summary")


class ProductSearchOutput(BaseModel):
    """Output schema for FIA product search."""

    products: list[ProductSearchResult] = Field(
        description="List of matching FIA products"
    )


def search_fia_products(product_name: str, carrier: Optional[str] = None) -> dict:
    """
    Search for Fixed Indexed Annuity products by name and optionally filter by carrier.

    This function currently uses mock data for known products. In a production environment,
    this would integrate with:
    - FIA product databases (e.g., Wink Intel, Cannex)
    - Carrier websites via web scraping
    - Insurance product APIs
    - Google Custom Search API for product pages

    Args:
        product_name: Product name to search for (e.g., "Allianz Benefit Control")
        carrier: Optional carrier name to filter results (e.g., "Allianz Life")

    Returns:
        Dictionary with structure: {"products": [{"name": str, "carrier": str, "url": str, "summary": str}]}

    Raises:
        ValueError: If product_name is empty or invalid

    Example:
        >>> result = search_fia_products("Benefit Control", "Allianz Life")
        >>> print(result["products"][0]["name"])
        "Allianz Benefit Control"
    """
    # Biblical Principle: EXCELLENCE - Validate inputs from the start
    try:
        validated_input = ProductSearchInput(product_name=product_name, carrier=carrier)
    except Exception as e:
        logger.error(f"Invalid input for search_fia_products: {e}")
        raise ValueError(f"Invalid search parameters: {e}")

    logger.info(f"Searching for FIA product: '{validated_input.product_name}' "
                f"(carrier filter: {validated_input.carrier or 'None'})")

    # Normalize search terms for comparison
    search_name_lower = validated_input.product_name.lower()
    carrier_filter_lower = validated_input.carrier.lower() if validated_input.carrier else None

    # === MOCK DATA SECTION ===
    # TODO: Replace with real API integration
    # Integration points:
    # 1. Wink Intel API: https://www.winkintel.com/api
    # 2. Carrier website scraping with BeautifulSoup
    # 3. Google Custom Search API: https://developers.google.com/custom-search
    # 4. Database of FIA products with metadata

    mock_products = []

    # Allianz products
    if "allianz" in search_name_lower and "benefit control" in search_name_lower:
        if not carrier_filter_lower or "allianz" in carrier_filter_lower:
            mock_products.append({
                "name": "Allianz Benefit Control",
                "carrier": "Allianz Life Insurance Company of North America",
                "url": "https://www.allianzlife.com/products/annuities/benefit-control",
                "summary": "Fixed indexed annuity with 10-year term, income benefit protection, "
                          "and multiple index options including S&P 500 and proprietary indices."
            })

    if "allianz" in search_name_lower and "222" in search_name_lower:
        if not carrier_filter_lower or "allianz" in carrier_filter_lower:
            mock_products.append({
                "name": "Allianz 222",
                "carrier": "Allianz Life Insurance Company of North America",
                "url": "https://www.allianzlife.com/products/annuities/allianz-222",
                "summary": "Fixed indexed annuity with 7-year term, bonus features, "
                          "and flexible allocation options across multiple crediting strategies."
            })

    # === END MOCK DATA SECTION ===

    # Biblical Principle: TRUTH - Be explicit when no results found
    if not mock_products:
        logger.warning(f"No products found for search: '{validated_input.product_name}' "
                      f"(carrier: {validated_input.carrier or 'None'})")
        return {"products": []}

    # Validate output structure
    try:
        output = ProductSearchOutput(
            products=[ProductSearchResult(**p) for p in mock_products]
        )
        logger.info(f"Found {len(output.products)} product(s) matching search criteria")
        return output.model_dump()
    except Exception as e:
        logger.error(f"Error formatting search results: {e}")
        raise RuntimeError(f"Failed to format search results: {e}")
