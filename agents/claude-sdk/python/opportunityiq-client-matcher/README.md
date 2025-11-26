# OpportunityIQ Client Matcher

**Status:** Phase 1 Complete - Core Tools Implemented
**Version:** 1.0.0
**Framework:** Claude SDK (Python)

A financial advisor tool that matches client profiles to opportunity scenarios and prioritizes revenue-generating actions using AI-powered analysis.

---

## Overview

OpportunityIQ analyzes client portfolios against predefined opportunity scenarios (annuity allocations, tax strategies, rebalancing opportunities, etc.) and ranks them by match quality and revenue potential.

### Key Features

- **Smart Matching:** Weighted criterion matching with 7 comparison operators
- **Revenue Estimation:** 4 formula types (percentage, flat fee, tiered, AUM-based)
- **Flexible Ranking:** Composite scoring with configurable weights
- **Multiple Outputs:** Markdown, text, JSON, and CSV reports
- **Production Ready:** Full type safety, validation, error handling, and logging

---

## Quick Start

### Prerequisites

- Python 3.10+
- `uv` (for virtual environment and package management)

### Installation

```bash
# 1. Clone or navigate to project directory
cd opportunityiq-client-matcher

# 2. Create virtual environment
uv venv

# 3. Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
source .venv/Scripts/activate  # Windows Git Bash

# 4. Install dependencies
uv pip install -r requirements.txt

# 5. Copy environment template
cp .env.example .env
```

### Verify Installation

```bash
python verify_implementation.py
```

You should see:
```
✓ VERIFICATION COMPLETE - All components working correctly!
```

---

## Architecture

### Three-Layer Design

```
┌─────────────────────────────────────────────┐
│              Tools Layer (API)               │
│  load_scenarios, match_clients, rank, etc.  │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│          Services Layer (Logic)              │
│  MatchingEngine, RevenueCalculator, etc.    │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│         Models Layer (Data)                  │
│  Scenario, ClientProfile, Opportunity       │
└─────────────────────────────────────────────┘
```

### Components

**Models (500 lines):**
- `Scenario` - Opportunity scenarios with matching criteria
- `ClientProfile` - Client demographics and portfolio
- `Opportunity` - Matched results with scores and revenue

**Services (786 lines):**
- `MatchingEngine` - Core matching algorithm
- `RevenueCalculator` - Revenue estimation logic
- `ReportGenerator` - Report formatting

**Tools (1,267 lines):**
- `load_scenarios` - Load scenario definitions
- `match_clients` - Match clients to scenarios
- `calculate_revenue` - Revenue calculations
- `rank_opportunities` - Ranking and filtering
- `generate_report` - Report generation

---

## Usage Examples

### Basic Workflow

```python
from src.tools import (
    load_scenarios,
    match_clients_to_scenarios,
    rank_opportunities,
    generate_report
)

# 1. Load scenarios
scenarios = load_scenarios("data/scenarios/annuity_scenarios.json")

# 2. Load clients (from your data source)
clients = load_clients()  # Your implementation

# 3. Match clients to scenarios
opportunities = match_clients_to_scenarios(
    clients,
    scenarios,
    min_match_threshold=60.0  # Only 60%+ matches
)

# 4. Rank by composite score (40% match, 60% revenue)
ranked = rank_opportunities(
    opportunities,
    ranking_strategy="composite",
    match_weight=0.4,
    revenue_weight=0.6
)

# 5. Generate report
report = generate_report(ranked, format="markdown")
print(report)
```

### Filtering Opportunities

```python
from src.tools import filter_opportunities

# Get high-priority opportunities with good matches
filtered = filter_opportunities(
    opportunities,
    min_match_score=70.0,
    priorities=["high"]
)

# Get quick wins (high match, low time)
quick_wins = filter_opportunities(
    opportunities,
    quick_wins_only=True
)

# Get high-value opportunities
high_value = filter_opportunities(
    opportunities,
    high_value_only=True,
    revenue_threshold=10000.0  # $10k+
)
```

### Report Formats

```python
# Markdown (human-readable)
md_report = generate_report(opportunities, format="markdown")

# Plain text (console/email)
text_report = generate_report(opportunities, format="text")

# JSON (API response)
json_report = generate_report(opportunities, format="json")

# Summary (quick overview)
summary = generate_report(opportunities, format="summary")

# CSV export (spreadsheet analysis)
export_opportunities_csv(opportunities, "reports/data.csv")
```

---

## Data Models

### Scenario Definition

```json
{
  "scenario_id": "annuity_allocation_001",
  "name": "Fixed Indexed Annuity Allocation",
  "description": "Client suitable for FIA allocation",
  "category": "annuity",
  "criteria": [
    {
      "field": "age",
      "operator": "gte",
      "value": 60,
      "weight": 1.0
    },
    {
      "field": "portfolio.total_value",
      "operator": "gte",
      "value": 250000,
      "weight": 1.5
    }
  ],
  "revenue_formula": {
    "formula_type": "percentage",
    "base_rate": 0.01,
    "multiplier_field": "portfolio.total_value",
    "min_revenue": 2500.0,
    "max_revenue": 50000.0
  },
  "priority": "high",
  "estimated_time_hours": 3.0
}
```

### Client Profile

```json
{
  "client_id": "CLT-2024-001",
  "name": "John Smith",
  "age": 65,
  "risk_tolerance": "moderate",
  "investment_objective": "balanced",
  "time_horizon_years": 15,
  "annual_income": 150000.0,
  "net_worth": 2000000.0,
  "liquidity_needs": "medium",
  "tax_bracket": 24.0,
  "portfolio": {
    "total_value": 1000000.0,
    "equity_allocation": 60.0,
    "fixed_income_allocation": 35.0,
    "alternative_allocation": 5.0
  }
}
```

---

## Configuration

### Environment Variables (.env)

```bash
# Anthropic API Key (for agent integration)
ANTHROPIC_API_KEY=your_key_here

# Logging
LOG_LEVEL=INFO

# Data paths
SCENARIOS_DIR=data/scenarios/
CLIENTS_DIR=data/clients/
REPORTS_DIR=reports/

# Matching configuration
MIN_MATCH_THRESHOLD=60.0
REVENUE_THRESHOLD=5000.0
```

---

## Matching Algorithm

### Criterion Evaluation

Each criterion specifies:
- **field:** Client profile field to check (supports dot notation)
- **operator:** Comparison operator (gt, lt, gte, lte, eq, contains, in)
- **value:** Expected value
- **weight:** Importance weight (0.0-1.0)

### Match Score Calculation

```
match_score = (points_earned / total_possible_points) × 100
```

Where:
- `points_earned` = sum of weights for matched criteria
- `total_possible_points` = sum of all criterion weights

### Composite Ranking Score

```
composite_score = (match_score × match_weight) + (revenue_normalized × revenue_weight)
```

Default weights:
- Match quality: 40%
- Revenue potential: 60%

---

## Revenue Formulas

### 1. Percentage
```python
revenue = base_rate × client[multiplier_field]
# Example: 1% of portfolio value
```

### 2. Flat Fee
```python
revenue = base_rate
# Example: $5,000 per engagement
```

### 3. Tiered
```python
# Example: 1% on first $100k, 0.5% above
tiers = {
    "0-100000": 0.01,
    "100000+": 0.005
}
```

### 4. AUM-Based
```python
# Convenience wrapper for percentage of AUM
revenue = base_rate × portfolio.total_value
```

---

## Testing

### Run Verification Script

```bash
python verify_implementation.py
```

### Run Unit Tests (Phase 3 - Not Yet Implemented)

```bash
pytest tests/ -v --cov=src
```

---

## Project Structure

```
opportunityiq-client-matcher/
├── src/
│   ├── models/              # Pydantic data models
│   ├── services/            # Business logic
│   └── tools/               # Agent-facing API
├── data/
│   ├── scenarios/           # Scenario JSON files
│   └── clients/             # Client profile JSON
├── tests/                   # Unit tests (Phase 3)
├── docs/                    # Documentation
├── reports/                 # Generated reports
├── requirements.txt         # Dependencies
├── .env.example             # Environment template
├── verify_implementation.py # Verification script
└── README.md               # This file
```

---

## Next Steps

### Phase 2: Sample Data
- Create example scenario files
- Create example client profiles
- Document data formats

### Phase 3: Testing
- Unit tests for all components
- Integration tests
- Test coverage > 80%

### Phase 4: Agent Integration
- Create agent with Claude SDK
- Register tools with agent
- Define agent workflow
- Add conversation handling

### Phase 5: Documentation
- API documentation
- Architecture deep-dive
- Usage tutorials
- Deployment guide

---

## Dependencies

**Core:**
- `pydantic>=2.0.0` - Data validation
- `anthropic>=0.40.0` - Claude SDK
- `python-dotenv>=1.0.0` - Environment management

**Development:**
- `pytest>=8.0.0` - Testing
- `black>=24.0.0` - Formatting
- `mypy>=1.8.0` - Type checking
- `ruff>=0.1.0` - Linting

---

## Biblical Principles Applied

### TRUTH
All decisions are traceable with detailed breakdowns (MatchDetail, RevenueCalculation)

### HONOR
Client data sovereignty - all processing happens locally

### EXCELLENCE
Production-grade code from inception with full error handling

### SERVE
Clear, helpful error messages and multiple output formats

---

## Support

For issues or questions, refer to:
- `IMPLEMENTATION_SUMMARY.md` - Complete implementation details
- `ARCHITECTURE_BLUEPRINT.md` - Design decisions and specifications
- `verify_implementation.py` - Working examples

---

## License

Internal use only. Not for redistribution.

---

*Last updated: 2025-11-21*
*Version: 1.0.0*
*Status: Phase 1 Complete*
