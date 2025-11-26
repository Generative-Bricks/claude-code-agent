"""
Unit tests for search_fia_products tool.

Tests the search functionality including:
- Basic product search
- Carrier filtering
- Mock data returns
- Error handling
"""

import pytest
from src.tools.search_fia_products import search_fia_products


class TestSearchFIAProducts:
    """Test suite for search_fia_products tool."""

    def test_search_allianz_benefit_control(self):
        """Test searching for Allianz Benefit Control."""
        result = search_fia_products("Allianz Benefit Control")

        assert "products" in result
        assert len(result["products"]) > 0

        product = result["products"][0]
        assert "name" in product
        assert "carrier" in product
        assert "url" in product
        assert "summary" in product

        assert "Allianz" in product["name"]
        assert "Benefit Control" in product["name"]

    def test_search_with_carrier_filter(self):
        """Test searching with carrier name specified."""
        result = search_fia_products("Benefit Control", carrier="Allianz")

        assert "products" in result
        assert len(result["products"]) > 0

        product = result["products"][0]
        assert "Allianz" in product["carrier"]

    def test_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        result_lower = search_fia_products("allianz benefit control")
        result_upper = search_fia_products("ALLIANZ BENEFIT CONTROL")
        result_mixed = search_fia_products("Allianz Benefit Control")

        # All should return same product
        assert result_lower["products"][0]["name"] == result_upper["products"][0]["name"]
        assert result_lower["products"][0]["name"] == result_mixed["products"][0]["name"]

    def test_search_nationwide_peak_10(self):
        """Test searching for Nationwide Peak 10."""
        result = search_fia_products("Peak 10", carrier="Nationwide")

        assert "products" in result
        assert len(result["products"]) > 0

        product = result["products"][0]
        assert "Nationwide" in product["carrier"] or "Nationwide" in product["name"]

    def test_search_returns_required_fields(self):
        """Test that search results contain all required fields."""
        result = search_fia_products("Allianz Benefit Control")

        product = result["products"][0]
        required_fields = ["name", "carrier", "url", "summary"]

        for field in required_fields:
            assert field in product, f"Missing required field: {field}"
            assert product[field], f"Field {field} should not be empty"

    def test_search_url_format(self):
        """Test that returned URLs are valid."""
        result = search_fia_products("Allianz Benefit Control")

        product = result["products"][0]
        url = product["url"]

        assert url.startswith("http://") or url.startswith("https://")
        assert len(url) > 10

    def test_search_summary_not_empty(self):
        """Test that summary provides meaningful description."""
        result = search_fia_products("Allianz Benefit Control")

        product = result["products"][0]
        summary = product["summary"]

        assert len(summary) > 20  # Should be more than just a few words
        assert isinstance(summary, str)

    def test_search_unknown_product(self):
        """Test searching for unknown product returns empty or helpful message."""
        result = search_fia_products("NonExistent Product XYZ123")

        assert "products" in result
        # Should either return empty list or products with note about no matches
        assert isinstance(result["products"], list)

    def test_search_partial_match(self):
        """Test searching with partial product name."""
        # Search with just "Benefit" should still find "Benefit Control"
        result = search_fia_products("Benefit")

        assert "products" in result
        if len(result["products"]) > 0:
            # If any results found, at least one should contain "Benefit"
            product_names = [p["name"] for p in result["products"]]
            assert any("Benefit" in name for name in product_names)

    def test_search_carrier_only(self):
        """Test searching with just carrier name."""
        result = search_fia_products("Allianz")

        assert "products" in result
        # Should return Allianz products if any exist
        if len(result["products"]) > 0:
            product = result["products"][0]
            assert "Allianz" in product["name"] or "Allianz" in product["carrier"]

    def test_search_returns_dict(self):
        """Test that search always returns a dictionary."""
        result = search_fia_products("Test")

        assert isinstance(result, dict)
        assert "products" in result
        assert isinstance(result["products"], list)

    def test_search_multiple_results(self):
        """Test that search can return multiple products."""
        result = search_fia_products("Allianz")

        assert "products" in result
        products = result["products"]

        # Each product should be unique
        if len(products) > 1:
            names = [p["name"] for p in products]
            assert len(names) == len(set(names))  # All names unique

    def test_search_empty_string(self):
        """Test search behavior with empty string."""
        result = search_fia_products("")

        assert isinstance(result, dict)
        assert "products" in result
        # Should handle gracefully (empty results or all products)

    def test_search_special_characters(self):
        """Test search handles special characters."""
        result = search_fia_products("Product & Name (Special)")

        assert isinstance(result, dict)
        assert "products" in result
        # Should not crash with special characters

    def test_search_whitespace_handling(self):
        """Test that extra whitespace is handled."""
        result1 = search_fia_products("  Allianz  Benefit  Control  ")
        result2 = search_fia_products("Allianz Benefit Control")

        # Should return same results regardless of whitespace
        assert isinstance(result1, dict)
        assert isinstance(result2, dict)
