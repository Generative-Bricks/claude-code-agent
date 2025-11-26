#!/usr/bin/env python3
"""
Test OpportunityIQ workflow without requiring Anthropic API key.

This script tests the core matching workflow:
1. Load scenarios
2. Load clients
3. Match clients to scenarios
4. Rank opportunities
5. Generate report
"""

import json
from pathlib import Path

# Import tools directly (no API key needed)
from src.tools import (
    load_all_scenario_files,
    match_clients_to_scenarios,
    rank_opportunities,
    generate_report
)
from src.models import ClientProfile

def main():
    print("=" * 80)
    print("OpportunityIQ Client Matcher - Workflow Test")
    print("=" * 80)

    # 1. Load scenarios
    print("\n1. Loading scenarios...")
    scenarios = load_all_scenario_files("data/scenarios")
    print(f"   ✓ Loaded {len(scenarios)} scenarios")
    for scenario in scenarios:
        print(f"     - {scenario.scenario_id}: {scenario.name}")

    # 2. Load clients
    print("\n2. Loading clients...")
    with open("data/clients/sample-clients.json", 'r') as f:
        clients_data = json.load(f)

    # Convert to Pydantic objects
    clients = [ClientProfile(**client_data) for client_data in clients_data]
    print(f"   ✓ Loaded {len(clients)} clients")

    # 3. Match clients
    print("\n3. Matching clients to scenarios...")
    opportunities = match_clients_to_scenarios(
        clients=clients,
        scenarios=scenarios,
        min_match_threshold=60.0
    )
    print(f"   ✓ Found {len(opportunities)} opportunities")

    # 4. Rank opportunities
    print("\n4. Ranking opportunities...")
    ranked_result = rank_opportunities(
        opportunities=opportunities,
        ranking_strategy="composite",
        match_weight=0.4,
        revenue_weight=0.6,
        limit=10
    )

    ranked_opps = ranked_result["ranked_opportunities"]
    summary = ranked_result["summary"]

    print(f"   ✓ Ranked {len(ranked_opps)} opportunities")
    print(f"   Total Revenue Potential: ${summary['total_revenue']:,.2f}")
    print(f"   Average Match Score: {summary['average_match_score']:.1f}%")

    # 5. Generate report
    print("\n5. Generating report...")
    report = generate_report(opportunities=ranked_opps, format="text")
    print("   ✓ Report generated")

    # Print top 3
    print("\n" + "=" * 80)
    print("TOP 3 OPPORTUNITIES:")
    print("=" * 80)
    for idx, opp in enumerate(ranked_opps[:3], 1):
        print(f"\n{idx}. {opp.get('client_name', 'Unknown')} - {opp.get('scenario_name', 'Unknown')}")
        print(f"   Match Score: {opp.get('match_score', 0):.1f}%")
        print(f"   Revenue Estimate: ${opp.get('estimated_revenue', 0):,.2f}")
        match_reasons = opp.get('match_reasons', [])
        if match_reasons:
            print(f"   Match Reasons:")
            for reason in match_reasons[:2]:
                print(f"     • {reason}")

    # Save full report
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "test_report.md"

    markdown_report = generate_report(opportunities=ranked_opps, format="markdown")
    with open(output_file, 'w') as f:
        f.write(markdown_report)

    print(f"\n📄 Full markdown report saved to: {output_file}")
    print("\n" + "=" * 80)
    print("✅ WORKFLOW TEST COMPLETE - All components working!")
    print("=" * 80)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
