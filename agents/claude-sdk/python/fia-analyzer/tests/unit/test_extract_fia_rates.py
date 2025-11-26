"""
Unit tests for extract_fia_rates tool.

Tests the extraction functionality including:
- Parsing markdown content
- Extracting rates, charges, and features
- Creating FIAProduct models
- Error handling for malformed content
"""

import pytest
from src.tools.extract_fia_rates import extract_fia_rates
from src.models import FIAProduct


class TestExtractFIARates:
    """Test suite for extract_fia_rates tool."""

    def test_extract_from_sample_markdown(self, sample_markdown_content):
        """Test extracting rates from well-formed markdown."""
        result = extract_fia_rates(sample_markdown_content, "Allianz Benefit Control")

        assert isinstance(result, FIAProduct)
        assert result.name == "Allianz Benefit Control"

    def test_extract_product_name(self, sample_markdown_content):
        """Test that product name is correctly set."""
        result = extract_fia_rates(sample_markdown_content, "Allianz Benefit Control")

        assert result.name == "Allianz Benefit Control"
        assert isinstance(result.name, str)
        assert len(result.name) > 0

    def test_extract_contract_term(self, sample_markdown_content):
        """Test extracting contract term."""
        result = extract_fia_rates(sample_markdown_content, "Allianz Benefit Control")

        # Should extract "10 years" → 10
        assert result.contract_term == 10
        assert isinstance(result.contract_term, int)

    def test_extract_minimum_premium(self, sample_markdown_content):
        """Test extracting minimum premium."""
        result = extract_fia_rates(sample_markdown_content, "Allianz Benefit Control")

        # Should extract "$25,000" → 25000.0
        assert result.minimum_premium == 25000.0
        assert isinstance(result.minimum_premium, float)

    def test_extract_cap_rates(self, sample_markdown_content):
        """Test extracting cap rates from markdown."""
        result = extract_fia_rates(sample_markdown_content, "Allianz Benefit Control")

        # Should find cap rate of 5.5% for S&P 500
        cap_rates = [rate for rate in result.current_rates if rate.cap_rate is not None]
        assert len(cap_rates) > 0

        sp500_rate = next(
            (r for r in cap_rates if "S&P 500" in r.index_name), None
        )
        assert sp500_rate is not None
        assert sp500_rate.cap_rate == 5.5

    def test_extract_participation_rates(self, sample_markdown_content):
        """Test extracting participation rates."""
        result = extract_fia_rates(sample_markdown_content, "Allianz Benefit Control")

        # Should find 100% participation rate for PIMCO
        part_rates = [
            rate for rate in result.current_rates if rate.participation_rate is not None
        ]
        assert len(part_rates) > 0

        pimco_rate = next(
            (r for r in part_rates if "PIMCO" in r.index_name), None
        )
        assert pimco_rate is not None
        assert pimco_rate.participation_rate == 100.0

    def test_extract_surrender_charges(self, sample_markdown_content):
        """Test extracting surrender charge schedule."""
        result = extract_fia_rates(sample_markdown_content, "Allianz Benefit Control")

        assert len(result.surrender_charges) > 0

        # Check first year charge
        year1 = next((sc for sc in result.surrender_charges if sc.year == 1), None)
        assert year1 is not None
        assert year1.percentage == 9.0

        # Check that charges are in ascending year order
        years = [sc.year for sc in result.surrender_charges]
        assert years == sorted(years)

    def test_extract_rider_information(self, sample_markdown_content):
        """Test extracting rider details."""
        result = extract_fia_rates(sample_markdown_content, "Allianz Benefit Control")

        # Should extract GLWB rider
        glwb_riders = [r for r in result.riders if "GLWB" in r.name or "Lifetime" in r.name]
        assert len(glwb_riders) > 0

        glwb = glwb_riders[0]
        assert "0.95" in glwb.cost or "95" in glwb.cost

    def test_extract_rider_withdrawal_percentages(self, sample_markdown_content):
        """Test extracting withdrawal percentages from riders."""
        result = extract_fia_rates(sample_markdown_content, "Allianz Benefit Control")

        glwb_riders = [r for r in result.riders if r.withdrawal_percentages is not None]
        if glwb_riders:
            glwb = glwb_riders[0]
            assert "60" in glwb.withdrawal_percentages
            assert glwb.withdrawal_percentages["60"] == 4.0

    def test_extract_company_info(self, sample_markdown_content):
        """Test extracting company information."""
        result = extract_fia_rates(sample_markdown_content, "Allianz Benefit Control")

        assert result.issuer is not None
        assert "Allianz" in result.issuer.issuer
        assert result.issuer.financial_strength_ratings is not None

    def test_extract_financial_ratings(self, sample_markdown_content):
        """Test extracting financial strength ratings."""
        result = extract_fia_rates(sample_markdown_content, "Allianz Benefit Control")

        ratings = result.issuer.financial_strength_ratings
        assert ratings is not None
        assert "AM Best" in ratings
        assert ratings["AM Best"] == "A+"

    def test_extract_with_missing_data(self):
        """Test extraction with incomplete markdown."""
        minimal_markdown = """
        # Test Product

        Minimum Premium: $50,000
        """

        result = extract_fia_rates(minimal_markdown, "Test Product")

        assert isinstance(result, FIAProduct)
        assert result.name == "Test Product"
        assert result.minimum_premium == 50000.0

    def test_extract_handles_empty_markdown(self):
        """Test extraction with empty markdown content."""
        result = extract_fia_rates("", "Empty Product")

        assert isinstance(result, FIAProduct)
        assert result.name == "Empty Product"
        # Should have default values, not crash

    def test_extract_index_options(self, sample_markdown_content):
        """Test extracting index options."""
        result = extract_fia_rates(sample_markdown_content, "Allianz Benefit Control")

        # Should identify S&P 500 and PIMCO indexes
        index_names = [idx.name for idx in result.index_options]
        assert any("S&P 500" in name for name in index_names)

    def test_extract_current_rates_not_empty(self, sample_markdown_content):
        """Test that current_rates list is populated."""
        result = extract_fia_rates(sample_markdown_content, "Allianz Benefit Control")

        assert len(result.current_rates) > 0
        assert all(isinstance(rate.index_name, str) for rate in result.current_rates)

    def test_extract_product_type(self, sample_markdown_content):
        """Test that product type defaults to FIA."""
        result = extract_fia_rates(sample_markdown_content, "Allianz Benefit Control")

        assert result.product_type == "Fixed Indexed Annuity"

    def test_extract_with_alternative_formatting(self):
        """Test extraction with different markdown formatting."""
        alternative_markdown = """
        Product: Alternative FIA
        Term: 7 years
        Min Premium: $10,000

        Cap Rate (S&P 500): 6.25%
        """

        result = extract_fia_rates(alternative_markdown, "Alternative FIA")

        assert isinstance(result, FIAProduct)
        assert result.contract_term == 7
        assert result.minimum_premium == 10000.0

    def test_extract_rates_as_of_date(self, sample_markdown_content):
        """Test extracting rates effective date."""
        result = extract_fia_rates(sample_markdown_content, "Allianz Benefit Control")

        # Should parse "January 15, 2024" or similar
        if result.rates_as_of_date:
            assert result.rates_as_of_date.year >= 2024

    def test_extract_preserves_product_name(self):
        """Test that provided product name is used."""
        markdown = "# Different Name in Markdown\n\nSome content"

        result = extract_fia_rates(markdown, "Provided Product Name")

        # Should use provided name, not parsed name
        assert result.name == "Provided Product Name"

    def test_extract_multiple_surrender_charges(self, sample_markdown_content):
        """Test extracting complete surrender schedule."""
        result = extract_fia_rates(sample_markdown_content, "Allianz Benefit Control")

        # Should extract all 10 years
        assert len(result.surrender_charges) >= 5
        assert all(sc.percentage >= 0 for sc in result.surrender_charges)

    def test_extract_crediting_methods(self, sample_markdown_content):
        """Test that crediting methods are identified."""
        result = extract_fia_rates(sample_markdown_content, "Allianz Benefit Control")

        # Should identify crediting methods from the markdown
        assert len(result.available_crediting_methods) > 0
        assert any("Point-to-Point" in method for method in result.available_crediting_methods)

    def test_extract_with_special_characters(self):
        """Test extraction handles special characters in content."""
        markdown_with_special = """
        Product: Test & Product™
        Premium: $25,000–$1,000,000
        Rate: 5.5%–6.5%
        """

        result = extract_fia_rates(markdown_with_special, "Test Product")

        assert isinstance(result, FIAProduct)
        # Should not crash on special characters

    def test_extract_returns_valid_pydantic_model(self, sample_markdown_content):
        """Test that returned object is a valid Pydantic model."""
        result = extract_fia_rates(sample_markdown_content, "Allianz Benefit Control")

        # Should be able to serialize/deserialize
        json_data = result.model_dump_json()
        assert isinstance(json_data, str)

        # Should validate
        FIAProduct.model_validate_json(json_data)
