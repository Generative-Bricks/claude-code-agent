# Scenario Advisor Agent

**Purpose:** Multi-agent system that performs deep research to discover financial advisor scenarios (annuity events, life events, revenue opportunities), synthesizes them into actionable scenarios with enriched metadata, then matches clients to opportunities.

**Framework:** Claude Agent SDK (Python)

**Language:** Python 3.11+

**Status:** Phase 1 Complete - Core Implementation (v1.0.0)

---

## Overview

The Scenario Advisor uses a two-phase architecture:

1. **Research Phase:** Three specialist agents discover scenarios in parallel
2. **Execution Phase:** Matches enriched scenarios against client data

```
┌─────────────────────────────────────────────────────────────────┐
│                   RESEARCH ORCHESTRATOR                          │
│              Coordinates parallel research                       │
└─────────────────────────────────────────────────────────────────┘
                            │
       ┌────────────────────┼────────────────────┐
       │                    │                    │
       ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   ANNUITY    │    │  LIFE EVENT  │    │   REVENUE    │
│  RESEARCHER  │    │  RESEARCHER  │    │  RESEARCHER  │
└──────────────┘    └──────────────┘    └──────────────┘
       │                    │                    │
       └────────────────────┼────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SCENARIO SYNTHESIZER                            │
│      Merge, validate, enrich with confidence/actionability       │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                 EXECUTION ORCHESTRATOR                           │
│       Match scenarios to clients, generate reports               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
scenario-advisor/
├── .env.example                    # Environment variables template
├── requirements.txt                # Python dependencies
├── CLAUDE.md                       # THIS FILE
│
├── src/
│   ├── __init__.py
│   ├── main.py                     # CLI entry point
│   │
│   ├── models/                     # Pydantic data models
│   │   ├── __init__.py
│   │   ├── scenario.py             # MatchCriterion, RevenueFormula, Scenario
│   │   ├── client_profile.py       # Holdings, Portfolio, ClientProfile
│   │   ├── opportunity.py          # MatchDetail, Opportunity
│   │   └── enriched.py             # EnrichedScenario, TemporalContext, etc.
│   │
│   ├── services/                   # Business logic
│   │   ├── __init__.py
│   │   ├── matching_engine.py      # Client-scenario matching
│   │   ├── revenue_calculator.py   # Revenue estimation
│   │   ├── report_generator.py     # Report formatting
│   │   ├── research_orchestrator.py    # Parallel research coordination
│   │   ├── scenario_synthesizer.py     # Scenario enrichment
│   │   └── execution_orchestrator.py   # End-to-end execution
│   │
│   └── agents/                     # Research agents
│       ├── __init__.py
│       ├── annuity_researcher.py   # Annuity event discovery
│       ├── life_event_researcher.py    # Life event discovery
│       └── revenue_researcher.py   # Revenue opportunity discovery
│
├── data/
│   ├── scenarios/                  # Output: enriched scenario JSON
│   ├── clients/                    # Input: client data
│   │   └── sample-clients.json     # 5 sample clients
│   └── output/                     # Generated reports
│
└── tests/
    ├── unit/
    └── integration/
```

---

## Quick Start

### Installation

```bash
# Navigate to project
cd agents/claude-sdk/python/scenario-advisor

# Create virtual environment
uv venv

# Activate (Windows Git Bash)
source .venv/Scripts/activate

# Install dependencies
uv pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY
```

### Usage

```bash
# Full pipeline (research + execute)
python -m src.main --mode full --clients data/clients/sample-clients.json

# Research only
python -m src.main --mode research --focus annuity life_event

# Execute only (with pre-generated scenarios)
python -m src.main --mode execute --clients data/clients/sample-clients.json

# Verbose output
python -m src.main --mode full --clients data/clients/sample-clients.json -v
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--mode` | Pipeline mode: research, execute, full | `full` |
| `--clients` | Path to client data JSON | required for execute |
| `--output` | Output directory | `data/output` |
| `--min-confidence` | Minimum scenario confidence | `0.6` |
| `--min-match` | Minimum match score threshold | `60.0` |
| `--focus` | Research focus areas | all |
| `-v, --verbose` | Enable debug logging | `False` |

---

## Core Concepts

### Enriched Scenarios

Unlike static scenarios, EnrichedScenarios include:

- **Temporal Context:** Urgency level, trigger dates, action windows
- **Confidence Score:** Source reliability, cross-reference count
- **Actionability Metrics:** Specificity, urgency, impact, feasibility scores
- **Advisor Talking Points:** Ready-to-use conversation starters

```python
class EnrichedScenario(BaseModel):
    # Base scenario fields
    scenario_id: str
    name: str
    criteria: list[MatchCriterion]
    revenue_formula: RevenueFormula

    # Enrichments
    temporal_context: TemporalContext
    confidence: ConfidenceScore
    actionability: ActionabilityMetrics
    advisor_talking_points: list[str]
```

### Research Agents

Three specialist agents run in parallel:

1. **Annuity Researcher:** Surrender periods, rate resets, RMD triggers, MYGA maturities
2. **Life Event Researcher:** Retirement, inheritance, divorce, health events
3. **Revenue Researcher:** Cross-sell, consolidation, rebalancing, tax optimization

Each agent uses Claude to:
- Analyze market conditions
- Generate scenario hypotheses
- Score confidence and actionability
- Produce advisor talking points

### Matching Engine

Uses weighted criterion evaluation:
- Operators: `gt`, `lt`, `gte`, `lte`, `eq`, `contains`, `in`
- Each criterion has a weight (0.0-1.0)
- Match score = (weighted points earned / total weight) × 100

---

## Data Models

### Scenario Categories

```python
Literal["annuity_event", "life_event", "revenue_opportunity"]
```

### Urgency Levels

```python
Literal["immediate", "short_term", "medium_term", "long_term"]
```

### Priority Levels

```python
Literal["immediate", "high", "medium", "low"]
```

### Revenue Formula Types

```python
Literal["percentage", "flat_fee", "tiered", "aum_based"]
```

---

## Sample Client Data

The project includes 5 sample clients in `data/clients/sample-clients.json`:

| Client | Age | Profile | Key Opportunity |
|--------|-----|---------|-----------------|
| Robert Thompson | 62 | Conservative, existing FIA | Surrender period ending |
| Jennifer Martinez | 48 | Moderate, inheritance pending | $300K deployment |
| David & Susan Chen | 71 | Very conservative, retired | Home sale proceeds |
| Amanda Foster | 55 | Moderate-aggressive, divorce | Settlement repositioning |
| Michael O'Brien | 67 | Conservative, pension decision | $380K lump sum |

---

## Key Patterns

### Parallel Research

```python
# Research orchestrator uses asyncio.gather
results = await asyncio.gather(
    self.annuity_researcher.research(time_range_days),
    self.life_event_researcher.research(time_range_days),
    self.revenue_researcher.research(time_range_days),
    return_exceptions=True
)
```

### Scenario Synthesis

1. **Deduplicate:** Remove similar scenarios, keep highest confidence
2. **Cross-reference:** Boost confidence for multi-source scenarios
3. **Validate:** Ensure all fields pass Pydantic validation
4. **Score:** Calculate composite actionability
5. **Sort:** Return by actionability (highest first)

### Matching Pipeline

```python
for client in clients:
    for scenario in scenarios:
        score, details = matching_engine.match_client_to_scenario(client, scenario)
        if score >= threshold:
            opportunities.append(create_opportunity(client, scenario, score))
```

---

## Error Handling

- Research failures don't block other researchers (graceful degradation)
- Invalid scenarios are logged and skipped
- Client loading failures show clear error messages
- All errors logged with context for debugging

---

## Extension Points

| Extension | File | Method |
|-----------|------|--------|
| New research agent | `src/agents/` | Create new `*_researcher.py` |
| New matching operator | `matching_engine.py` | Add to `_evaluate_criterion()` |
| New formula type | `revenue_calculator.py` | Add to `_calculate_*()` methods |
| New report format | `report_generator.py` | Add to `generate()` |
| CRM integration | `execution_orchestrator.py` | Extend `_load_clients()` |

---

## Dependencies

```
anthropic>=0.40.0      # Claude SDK
pydantic>=2.0.0        # Data validation
python-dotenv>=1.0.0   # Environment config
aiohttp>=3.9.0         # Async HTTP
pandas>=2.0.0          # Data handling
```

---

## Testing

```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Verify syntax
python -m py_compile src/**/*.py
```

---

## Principles Applied

- **TRUTH:** All decisions observable via match details and confidence scores
- **HONOR:** Client data stays local, clear data sovereignty
- **EXCELLENCE:** Production-grade validation, error handling, logging
- **SERVE:** Multiple output formats, clear next actions for advisors
- **PERSEVERE:** Graceful degradation when research fails
- **SHARPEN:** Feedback loop ready for scenario effectiveness tracking

---

*Last updated: November 2025*
*Version: 1.0.0*
