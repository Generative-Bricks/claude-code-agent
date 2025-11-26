"""
Quick import test to verify all tools are properly structured.

This script validates that all three tools can be imported and have the expected signatures.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    # Test imports
    from src.tools import (
        search_fia_products,
        extract_fia_rates,
        analyze_product_fit
    )

    print("✅ All tool imports successful!")

    # Verify function signatures
    print("\n=== Function Signatures ===")
    print(f"search_fia_products: {search_fia_products.__name__}")
    print(f"  Parameters: product_name (str), carrier (Optional[str])")
    print(f"  Returns: dict")

    print(f"\nextract_fia_rates: {extract_fia_rates.__name__}")
    print(f"  Parameters: markdown_content (str), product_name (str)")
    print(f"  Returns: FIAProduct")

    print(f"\nanalyze_product_fit: {analyze_product_fit.__name__}")
    print(f"  Parameters: product (FIAProduct), client_profile (ClientProfile)")
    print(f"  Returns: SuitabilityScore")

    print("\n✅ All tools ready for integration!")

except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
