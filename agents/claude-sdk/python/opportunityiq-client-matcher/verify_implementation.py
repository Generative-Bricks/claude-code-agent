"""
Quick verification script to test OpportunityIQ implementation.

This script verifies that all components are properly installed and importable.
"""

import sys


def verify_imports():
    """Verify all modules can be imported."""
    print("=" * 70)
    print("OpportunityIQ Client Matcher - Implementation Verification")
    print("=" * 70)
    print()

    # Test models
    print("1. Testing models...")
    try:
        from src.models import (
            Scenario,
            MatchCriterion,
            RevenueFormula,
            ClientProfile,
            Portfolio,
            Holdings,
            Opportunity,
            MatchDetail,
            RevenueCalculation,
        )
        print("   ✓ All 9 model classes imported successfully")
    except ImportError as e:
        print(f"   ✗ Model import failed: {e}")
        return False

    # Test services
    print("\n2. Testing services...")
    try:
        from src.services import (
            MatchingEngine,
            RevenueCalculator,
            ReportGenerator,
        )
        print("   ✓ All 3 service classes imported successfully")
    except ImportError as e:
        print(f"   ✗ Service import failed: {e}")
        return False

    # Test tools
    print("\n3. Testing tools...")
    try:
        from src.tools import (
            load_scenarios,
            load_all_scenario_files,
            match_client_to_scenarios,
            match_clients_to_scenarios,
            calculate_revenue,
            calculate_revenues_batch,
            estimate_total_revenue,
            rank_opportunities,
            filter_opportunities,
            get_top_opportunities,
            group_opportunities_by_client,
            generate_report,
            generate_client_report,
            generate_summary_statistics,
            export_opportunities_csv,
        )
        print("   ✓ All 15 tool functions imported successfully")
    except ImportError as e:
        print(f"   ✗ Tool import failed: {e}")
        return False

    # Test instantiation
    print("\n4. Testing service instantiation...")
    try:
        matching_engine = MatchingEngine()
        revenue_calculator = RevenueCalculator()
        report_generator = ReportGenerator()
        print("   ✓ All services instantiated successfully")
    except Exception as e:
        print(f"   ✗ Service instantiation failed: {e}")
        return False

    # Test model creation with basic data
    print("\n5. Testing model creation...")
    try:
        from datetime import date

        # Create minimal criterion
        criterion = MatchCriterion(
            field="age",
            operator="gte",
            value=65,
            weight=1.0
        )

        # Create minimal revenue formula
        revenue_formula = RevenueFormula(
            formula_type="flat_fee",
            base_rate=5000.0
        )

        # Create minimal scenario
        scenario = Scenario(
            scenario_id="test_001",
            name="Test Scenario",
            description="Test scenario for verification",
            category="annuity",
            criteria=[criterion],
            revenue_formula=revenue_formula
        )

        # Create minimal portfolio
        portfolio = Portfolio(
            total_value=500000.0,
            equity_allocation=60.0,
            fixed_income_allocation=40.0
        )

        # Create minimal client
        client = ClientProfile(
            client_id="CLT-TEST-001",
            name="Test Client",
            age=67,
            risk_tolerance="moderate",
            investment_objective="balanced",
            time_horizon_years=10,
            annual_income=100000.0,
            net_worth=1000000.0,
            liquidity_needs="medium",
            tax_bracket=24.0,
            portfolio=portfolio
        )

        print("   ✓ All models created successfully")
        print(f"     - Scenario: {scenario.scenario_id}")
        print(f"     - Client: {client.client_id} (age {client.age})")
        print(f"     - Portfolio value: ${client.portfolio.total_value:,.2f}")

    except Exception as e:
        print(f"   ✗ Model creation failed: {e}")
        return False

    # Test basic workflow
    print("\n6. Testing basic workflow (match → rank)...")
    try:
        # Match client to scenario
        opportunities = match_client_to_scenarios(client, scenario)

        if not opportunities:
            print("   ✗ Matching produced no opportunities")
            return False

        print(f"   ✓ Matching successful: {len(opportunities)} opportunity created")

        # Test ranking
        ranked = rank_opportunities(opportunities, ranking_strategy="composite")
        print(f"   ✓ Ranking successful: {len(ranked)} opportunity ranked")

        opp = ranked[0]
        print(f"     - Match score: {opp.match_score:.1f}%")
        print(f"     - Estimated revenue: ${opp.estimated_revenue:,.2f}")
        print(f"     - Rank: #{opp.rank}")

    except Exception as e:
        print(f"   ✗ Workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Test report generation
    print("\n7. Testing report generation...")
    try:
        report = generate_report(ranked, format="summary")
        print("   ✓ Report generation successful")
        print("\n" + "-" * 70)
        print(report)
        print("-" * 70)
    except Exception as e:
        print(f"   ✗ Report generation failed: {e}")
        return False

    return True


if __name__ == "__main__":
    print()
    success = verify_imports()
    print()
    print("=" * 70)

    if success:
        print("✓ VERIFICATION COMPLETE - All components working correctly!")
        print("=" * 70)
        sys.exit(0)
    else:
        print("✗ VERIFICATION FAILED - Check errors above")
        print("=" * 70)
        sys.exit(1)
