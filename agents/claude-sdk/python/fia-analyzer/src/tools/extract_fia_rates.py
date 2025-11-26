"""
Extract FIA Rates Tool

This tool parses FIA rate data from markdown content (typically from web pages or rate sheets)
and extracts structured product information into the FIAProduct model.

Biblical Principle: TRUTH - Explicit extraction with clear error handling when data is missing.
Biblical Principle: EXCELLENCE - Production-grade parsing with graceful handling of incomplete data.
"""

import logging
import re
from datetime import date
from typing import Optional

from src.models.fia_product import (
    FIAProduct,
    SurrenderCharge,
    IndexOption,
    CurrentRate,
    Rider,
    CommissionStructure,
    CompanyInfo
)

# Configure logging
logger = logging.getLogger(__name__)


def extract_fia_rates(markdown_content: str, product_name: str) -> FIAProduct:
    """
    Extract FIA product rates and features from markdown content.

    Parses markdown content (from web pages, rate sheets, or documentation) to extract
    structured FIA product data including rates, surrender charges, index options, and features.

    Args:
        markdown_content: Markdown text containing product information
        product_name: Name of the product being extracted (used for error messages and metadata)

    Returns:
        FIAProduct: Fully populated FIA product model with all extracted data

    Raises:
        ValueError: If required data is missing or product_name is invalid
        RuntimeError: If parsing fails critically

    Example:
        >>> content = '''
        ... # Allianz Benefit Control
        ... **Cap Rate**: 5.5%
        ... **Minimum Premium**: $25,000
        ... **Surrender Charges**: 9%, 8%, 7%, 6%, 5%, 4%, 3%, 2%, 1%, 0%
        ... '''
        >>> product = extract_fia_rates(content, "Allianz Benefit Control")
        >>> print(product.current_rates[0].cap_rate)
        5.5
    """
    # Biblical Principle: EXCELLENCE - Validate inputs from the start
    if not product_name or not product_name.strip():
        raise ValueError("Product name cannot be empty")
    if not markdown_content or not markdown_content.strip():
        raise ValueError("Markdown content cannot be empty")

    logger.info(f"Extracting rates for product: {product_name}")

    try:
        # Initialize extraction results
        extracted_data = {
            "name": product_name.strip(),
            "product_type": "Fixed Indexed Annuity",
            "data_collected_date": date.today(),
            "data_source": "Markdown extraction"
        }

        # Extract contract term (look for patterns like "10-year", "7 year", "term: 10")
        term_match = re.search(r'(?:term|period|years?)[:\s]+(\d+)', markdown_content, re.IGNORECASE)
        if term_match:
            extracted_data["contract_term"] = int(term_match.group(1))
            logger.debug(f"Extracted contract term: {extracted_data['contract_term']} years")
        else:
            # Default to 10 years if not found
            extracted_data["contract_term"] = 10
            logger.warning(f"Contract term not found, defaulting to 10 years")

        # Extract minimum premium (look for patterns like "$25,000", "minimum: $25000", "25k")
        premium_match = re.search(r'(?:minimum|min)[:\s]*\$?\s*([0-9,]+)(?:k|,000)?', markdown_content, re.IGNORECASE)
        if premium_match:
            premium_str = premium_match.group(1).replace(',', '')
            if 'k' in markdown_content[premium_match.start():premium_match.end()].lower():
                extracted_data["minimum_premium"] = float(premium_str) * 1000
            else:
                extracted_data["minimum_premium"] = float(premium_str)
            logger.debug(f"Extracted minimum premium: ${extracted_data['minimum_premium']:,.0f}")
        else:
            raise ValueError(f"Minimum premium not found in markdown content for {product_name}")

        # Extract surrender charges (look for percentage sequences like "9%, 8%, 7%...")
        surrender_pattern = r'surrender\s+charges?[:\s]*([0-9%,\s]+)'
        surrender_match = re.search(surrender_pattern, markdown_content, re.IGNORECASE)
        if surrender_match:
            charges_str = surrender_match.group(1)
            percentages = re.findall(r'(\d+(?:\.\d+)?)\s*%', charges_str)
            if percentages:
                extracted_data["surrender_charges"] = [
                    SurrenderCharge(year=idx + 1, percentage=float(pct))
                    for idx, pct in enumerate(percentages)
                ]
                logger.debug(f"Extracted {len(percentages)} surrender charge years")
            else:
                raise ValueError(f"Surrender charge percentages not found for {product_name}")
        else:
            raise ValueError(f"Surrender charges not found in markdown content for {product_name}")

        # Extract cap rates (look for "cap rate: 5.5%" or "5.5% cap")
        cap_rates = []
        cap_pattern = r'(?:cap\s+rate|cap)[:\s]*(\d+(?:\.\d+)?)\s*%'
        for match in re.finditer(cap_pattern, markdown_content, re.IGNORECASE):
            cap_rates.append(float(match.group(1)))
        if cap_rates:
            logger.debug(f"Extracted {len(cap_rates)} cap rate(s): {cap_rates}")

        # Extract participation rates (look for "participation rate: 100%" or "100% participation")
        participation_rates = []
        participation_pattern = r'(?:participation\s+rate|participation)[:\s]*(\d+(?:\.\d+)?)\s*%'
        for match in re.finditer(participation_pattern, markdown_content, re.IGNORECASE):
            participation_rates.append(float(match.group(1)))
        if participation_rates:
            logger.debug(f"Extracted {len(participation_rates)} participation rate(s): {participation_rates}")

        # Extract index options (look for common index names)
        index_names = []
        common_indices = [
            (r's&p\s*500', "S&P 500"),
            (r'nasdaq[- ]?100', "NASDAQ-100"),
            (r'russell\s*2000', "Russell 2000"),
            (r'euro\s*stoxx', "Euro STOXX 50"),
            (r'msci\s*eafe', "MSCI EAFE")
        ]
        for pattern, index_name in common_indices:
            if re.search(pattern, markdown_content, re.IGNORECASE):
                index_names.append(index_name)
                logger.debug(f"Found index option: {index_name}")

        # Build index options (use detected indices or default)
        if index_names:
            extracted_data["index_options"] = [
                IndexOption(
                    name=name,
                    description=f"{name} index allocation",
                    crediting_methods=["Annual Point-to-Point"]  # Default method
                )
                for name in index_names
            ]
        else:
            # Default to S&P 500 if no indices found
            extracted_data["index_options"] = [
                IndexOption(
                    name="S&P 500",
                    description="S&P 500 Price Return index allocation",
                    crediting_methods=["Annual Point-to-Point"]
                )
            ]
            logger.warning("No specific index options found, using default S&P 500")

        # Extract crediting methods
        crediting_methods = []
        method_patterns = [
            (r'annual\s+point[- ]to[- ]point', "Annual Point-to-Point"),
            (r'monthly\s+sum', "Monthly Sum"),
            (r'monthly\s+average', "Monthly Average"),
            (r'daily\s+average', "Daily Average")
        ]
        for pattern, method_name in method_patterns:
            if re.search(pattern, markdown_content, re.IGNORECASE):
                crediting_methods.append(method_name)

        extracted_data["available_crediting_methods"] = crediting_methods if crediting_methods else ["Annual Point-to-Point"]

        # Build current rates (combine cap and participation rates)
        current_rates = []
        if cap_rates or participation_rates:
            # Create rate entries for each detected index
            for idx, index_option in enumerate(extracted_data["index_options"]):
                rate_entry = CurrentRate(
                    index_name=index_option.name,
                    crediting_method=extracted_data["available_crediting_methods"][0],
                    cap_rate=cap_rates[0] if cap_rates else None,
                    participation_rate=participation_rates[0] if participation_rates else None
                )
                current_rates.append(rate_entry)
        extracted_data["current_rates"] = current_rates

        # Extract company/issuer information (look for carrier name)
        issuer_name = product_name.split()[0]  # Use first word of product name as fallback
        carrier_pattern = r'(?:issuer|carrier|company)[:\s]*([A-Za-z\s]+(?:Insurance|Life|Financial))'
        carrier_match = re.search(carrier_pattern, markdown_content, re.IGNORECASE)
        if carrier_match:
            issuer_name = carrier_match.group(1).strip()
            logger.debug(f"Extracted issuer: {issuer_name}")

        extracted_data["issuer"] = CompanyInfo(
            issuer=issuer_name,
            parent_company=None,  # Would need specific extraction logic
            financial_strength_ratings=None,  # Would need specific extraction logic
        )

        # Extract riders (look for income rider, death benefit, etc.)
        riders = []
        rider_patterns = [
            (r'(?:guaranteed\s+)?(?:lifetime\s+)?(?:withdrawal|income)\s+benefit', "Guaranteed Lifetime Withdrawal Benefit"),
            (r'death\s+benefit', "Death Benefit"),
            (r'(?:long[- ]term\s+)?care\s+benefit', "Long-Term Care Benefit"),
            (r'terminal\s+illness', "Terminal Illness Benefit")
        ]
        for pattern, rider_name in rider_patterns:
            if re.search(pattern, markdown_content, re.IGNORECASE):
                riders.append(Rider(
                    name=rider_name,
                    description=f"{rider_name} rider",
                    is_built_in=False  # Would need specific logic to determine
                ))
                logger.debug(f"Found rider: {rider_name}")
        extracted_data["riders"] = riders

        # Extract special features
        special_features = []
        feature_keywords = [
            "bonus", "multiplier", "enhanced", "guaranteed", "flexible", "indexed"
        ]
        for keyword in feature_keywords:
            if re.search(rf'\b{keyword}\b', markdown_content, re.IGNORECASE):
                special_features.append(f"Product includes {keyword} feature")
        extracted_data["special_features"] = special_features[:5]  # Limit to 5 features

        # Biblical Principle: TRUTH - Build and validate the complete model
        product = FIAProduct(**extracted_data)
        logger.info(f"Successfully extracted FIA product data for: {product_name}")
        return product

    except ValueError as e:
        logger.error(f"Validation error extracting {product_name}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error extracting {product_name}: {e}")
        raise RuntimeError(f"Failed to extract product data: {e}")
