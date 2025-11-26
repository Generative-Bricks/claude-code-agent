# OpportunityIQ Client Matcher Agent

**Purpose:** Match financial advisor clients to revenue opportunity scenarios and generate prioritized action reports

**Framework:** Claude Agent SDK (Python)

**Language:** Python 3.11+

**Status:** ✅ Phase 1 Complete - Core Tools Implemented (v1.0.0)

---

## 📖 Project Overview

The OpportunityIQ Client Matcher Agent is a production-ready AI system that helps financial advisors systematically discover revenue opportunities by matching client profiles against predefined opportunity scenarios (FIA replacements, cash repositioning, portfolio concentration, tax strategies, etc.).

### Key Capabilities

1. **Smart Matching** - Weighted criterion evaluation with 7 comparison operators
2. **Revenue Calculation** - 4 formula types (percentage, flat fee, tiered, AUM-based)
3. **Intelligent Ranking** - Composite scoring balancing client fit and business value
4. **Flexible Reporting** - Multiple output formats (markdown, text, JSON, CSV)
5. **Production-Grade** - Full type safety, validation, error handling, and logging

### How It Works

```
Client Profiles → Match Against Scenarios → Calculate Revenue → Rank by Value → Generate Report
```

**Example Use Case:**
```
Input:  50 client profiles + 12 opportunity scenarios
Output: Top 25 opportunities ranked by revenue potential with actionable next steps
Result: Advisor knows exactly which clients to call this week and why
```

---

## 📂 Directory Structure

```
opportunityiq-client-matcher/
│
├── .env.example                          # Environment variables template
├── .gitignore                            # Git ignore rules
├── CLAUDE.md                             # THIS FILE - Project documentation
├── README.md                             # Quick start guide
├── IMPLEMENTATION_SUMMARY.md             # Detailed implementation report
├── requirements.txt                      # Python dependencies (31 packages)
├── verify_implementation.py              # Verification script
│
├── src/                                  # Source code (2,572 lines)
│   ├── __init__.py
│   │
│   ├── models/                           # Pydantic data models (500 lines)
│   │   ├── __init__.py
│   │   ├── scenario.py                   # Scenario, MatchCriterion, RevenueFormula
│   │   ├── client_profile.py             # ClientProfile, Portfolio, Holdings
│   │   └── opportunity.py                # Opportunity, MatchDetail, RevenueCalculation
│   │
│   ├── services/                         # Business logic services (786 lines)
│   │   ├── __init__.py
│   │   ├── matching_engine.py            # Core matching algorithm
│   │   ├── revenue_calculator.py         # Revenue calculation logic
│   │   └── report_generator.py           # Report formatting logic
│   │
│   └── tools/                            # Agent tools (1,267 lines)
│       ├── __init__.py
│       ├── load_scenarios.py             # Load scenarios from JSON
│       ├── match_clients.py              # Match clients to scenarios
│       ├── calculate_revenue.py          # Calculate revenue estimates
│       ├── rank_opportunities.py         # Rank and prioritize
│       └── generate_report.py            # Generate formatted reports
│
├── data/                                 # Data files
│   ├── scenarios/                        # Scenario definitions (JSON)
│   └── clients/                          # Example client data
│
├── tests/                                # Test suite (to be implemented)
│   ├── unit/                             # Unit tests
│   ├── integration/                      # Integration tests
│   └── fixtures/                         # Test data
│
├── docs/                                 # Additional documentation
│
├── credentials/                          # API credentials (gitignored)
│
└── .venv/                                # Virtual environment (31 packages)
```

---

## 🏗️ Architecture

### Three-Layer Design

```
┌──────────────────────────────────────────────────┐
│                   TOOLS LAYER                     │
│  (Claude-callable functions)                      │
│                                                   │
│  load_scenarios, match_clients, calculate_revenue│
│  rank_opportunities, generate_report              │
└───────────────────┬──────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────┐
│                SERVICES LAYER                     │
│  (Business logic)                                 │
│                                                   │
│  MatchingEngine, RevenueCalculator,               │
│  ReportGenerator                                  │
└───────────────────┬──────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────┐
│                 MODELS LAYER                      │
│  (Pydantic data models)                           │
│                                                   │
│  Scenario, ClientProfile, Opportunity             │
└──────────────────────────────────────────────────┘
```

### Key Design Decisions

**1. Pydantic for All Data Models**
- **Why:** Runtime validation, type safety, JSON serialization, self-documenting
- **Trade-off:** Slight performance overhead (negligible)
- **Result:** Catch errors early, clear contracts between components

**2. Separate Services from Tools**
- **Why:** Single responsibility, testability, reusability
- **Trade-off:** More files to manage
- **Result:** Easy to unit test, clear separation of concerns

**3. JSON Files for Scenarios (Not Database)**
- **Why:** Simplicity, transparency, version control, no infrastructure
- **Trade-off:** Manual JSON editing
- **Result:** Easy to understand, git-friendly, can migrate later

**4. Flexible Matching Criteria System**
- **Why:** Extensibility, observability, configurability
- **Trade-off:** More complex than hard-coded rules
- **Result:** Easy to add new scenarios without code changes

**5. Composite Ranking Score**
- **Why:** Multi-dimensional prioritization (revenue + match quality)
- **Trade-off:** Weights are somewhat arbitrary (can be tuned)
- **Result:** Better prioritization than revenue alone

---

## 🛠️ The 5 Core Tools

### 1. load_scenarios

**Purpose:** Load revenue opportunity scenarios from JSON files

**Input:**
```python
{
    "directory": "data/scenarios",
    "scenario_ids": ["FIA-001", "CASH-001"],  # Optional filter
    "min_match_threshold": 60.0  # Optional override
}
```

**Output:**
```python
[
    Scenario(
        scenario_id="FIA-001",
        name="FIA Replacement Opportunity",
        description="Client has FIA with favorable replacement conditions",
        criteria=[...],
        revenue_formula={...}
    ),
    ...
]
```

**Key Features:**
- Validates JSON against Pydantic schema
- Filters by scenario IDs if provided
- Handles missing files gracefully
- Returns detailed error messages

---

### 2. match_clients_to_scenarios

**Purpose:** Match client profiles against scenarios to identify opportunities

**Input:**
```python
{
    "clients": [ClientProfile(...)],
    "scenarios": [Scenario(...)],
    "min_match_threshold": 60.0  # 0-100 scale
}
```

**Output:**
```python
[
    Opportunity(
        client_name="John Smith",
        scenario_name="FIA Replacement",
        match_score=85.5,
        match_reasons=["Surrender period ending in 6 months", ...],
        estimated_revenue=5000.00,
        priority="high"
    ),
    ...
]
```

**Matching Algorithm:**
1. For each client-scenario pair:
   - Evaluate all match criteria (age > 60, portfolio > $100k, etc.)
   - Calculate weighted match score (0-100)
   - Check exclusion rules
   - If score >= threshold: Create Opportunity
2. Return all opportunities with detailed match reasons

**Supported Operators:**
- `greater_than`, `less_than`, `greater_than_or_equal`, `less_than_or_equal`
- `equals`, `contains`, `in` (list membership)

---

### 3. calculate_opportunity_revenue

**Purpose:** Calculate detailed revenue estimates for opportunities

**Input:**
```python
{
    "opportunity": Opportunity(...),
    "revenue_formula": RevenueFormula(...)
}
```

**Output:**
```python
{
    "estimated_revenue": 5000.00,
    "calculation": {
        "formula_type": "percentage",
        "base_amount": 500000.00,
        "rate": 0.01,
        "breakdown": ["$500,000 × 1% = $5,000"]
    },
    "confidence": "high"
}
```

**Supported Formula Types:**
1. **Percentage:** `base_rate × field_value`
2. **Flat Fee:** Fixed dollar amount
3. **Tiered:** Different rates for different ranges
4. **AUM-Based:** Percentage of portfolio value

**Example Calculations:**
```python
# Percentage: FIA replacement
$250,000 (FIA value) × 1% (commission) = $2,500

# Tiered: Portfolio management
$0-$500k at 1.00% = $5,000
$500k-$1M at 0.75% = $3,750
Total: $8,750

# AUM-Based: Cash repositioning
$150,000 (cash) × 1% (annual fee) = $1,500/year
```

---

### 4. rank_opportunities

**Purpose:** Rank and prioritize opportunities for advisor review

**Input:**
```python
{
    "opportunities": [Opportunity(...)],
    "ranking_strategy": "composite",  # or "revenue", "match_score", "priority"
    "match_weight": 0.4,
    "revenue_weight": 0.6,
    "filters": {
        "min_revenue": 1000.0,
        "priorities": ["high", "immediate"]
    }
}
```

**Output:**
```python
{
    "ranked_opportunities": [Opportunity(...)],  # Sorted highest to lowest
    "summary": {
        "total_revenue": 125000.00,
        "average_match_score": 78.5,
        "high_priority_count": 12
    }
}
```

**Ranking Strategies:**
1. **Composite** (default): Weighted combination of match score + revenue
2. **Revenue**: Sort by estimated revenue only
3. **Match Score**: Sort by match quality only
4. **Priority**: Sort by urgency/time sensitivity

**Filters:**
- Minimum revenue threshold
- Minimum match score
- Priority levels (immediate, high, medium, low)
- Time constraints (action needed within X days)
- Scenario categories

---

### 5. generate_report

**Purpose:** Generate formatted opportunity report for advisor

**Input:**
```python
{
    "opportunities": [Opportunity(...)],
    "format": "markdown",  # or "text", "json", "summary"
    "output_file": "report_2025-01-21.md"
}
```

**Output:**
```markdown
# OpportunityIQ Opportunity Report

Generated: 2025-01-21 14:30:00

## Summary
- **Total Opportunities:** 25
- **Total Revenue Potential:** $125,000
- **Average Match Score:** 78.5%
- **High Priority:** 8 opportunities

## Opportunities

### 1. John Smith - FIA Replacement ($5,000)
**Match Score:** 85.5% | **Priority:** High

**Why This Matches:**
- FIA surrender period ends in 6 months
- Current cap rate (4.2%) below market (6.5%)
- Client is 62 years old (optimal replacement age)

**Recommended Actions:**
1. Review current FIA performance
2. Compare to current market rates
3. Schedule meeting within 30 days
4. Prepare 1035 exchange paperwork

**Revenue Estimate:** $5,000 (1% of $500,000 FIA value)
**Confidence:** High

---

[Repeat for top 25 opportunities]
```

**Report Formats:**
- **Markdown:** Human-readable, email-friendly
- **Text:** Plain text, no formatting
- **JSON:** Machine-readable for integrations
- **Summary:** Quick overview with key stats

---

## 🚀 Quick Start

### Installation

```bash
# 1. Navigate to project
cd opportunityiq-client-matcher

# 2. Create virtual environment
uv venv

# 3. Activate
source .venv/Scripts/activate  # Windows Git Bash
source .venv/bin/activate       # Linux/Mac

# 4. Install dependencies
uv pip install -r requirements.txt

# 5. Verify installation
python verify_implementation.py
```

### Basic Usage

```python
from src.tools import (
    load_scenarios,
    match_clients_to_scenarios,
    rank_opportunities,
    generate_report
)

# 1. Load scenarios
scenarios = load_scenarios("data/scenarios")

# 2. Define clients (or load from Google Sheets)
clients = [
    {
        "client_id": "C001",
        "name": "John Smith",
        "age": 62,
        "portfolio_value": 500000,
        "fia_value": 250000,
        "fia_surrender_end_date": "2025-06-15"
    }
]

# 3. Match clients to scenarios
opportunities = match_clients_to_scenarios(
    clients,
    scenarios,
    min_match_threshold=60.0
)

# 4. Rank opportunities
ranked = rank_opportunities(
    opportunities,
    ranking_strategy="composite",
    match_weight=0.4,
    revenue_weight=0.6
)

# 5. Generate report
report = generate_report(
    ranked,
    format="markdown",
    output_file="report.md"
)

print(f"Found {len(ranked)} opportunities")
print(f"Total revenue potential: ${sum(opp.estimated_revenue for opp in ranked)}")
```

---

## 📊 Example Scenarios

### Scenario 1: FIA Replacement Opportunity

**Criteria:**
- FIA surrender period ends within 6-12 months
- Current cap rate < 5.5% (below market)
- FIA value > $50,000

**Revenue Formula:**
- 1% of FIA value (typical replacement commission)

**Example:**
- Client has $250,000 FIA with 4.2% cap ending in 8 months
- Market rates: 6.5-7%
- Revenue estimate: $2,500
- Action: Schedule review, run illustration, discuss 1035 exchange

---

### Scenario 2: Cash Drag Opportunity

**Criteria:**
- Cash balance > 20% of portfolio
- Portfolio value > $100,000
- Risk tolerance: moderate or aggressive

**Revenue Formula:**
- 1% annual fee on repositioned cash (assume 20% of cash deployed)

**Example:**
- Client has $150,000 cash (25% of $600k portfolio) earning 0.5%
- Money market rates: 5%
- Revenue estimate: $300/year (1% on $30,000 deployed)
- Action: Quick call, reposition to higher-yielding option

---

### Scenario 3: Concentrated Position Risk

**Criteria:**
- Single position > 25% of portfolio
- Portfolio value > $250,000
- Not aggressive risk tolerance

**Revenue Formula:**
- Tiered management fee on portfolio value

**Example:**
- Client has 40% portfolio in single stock ($200,000 of $500,000)
- Significant concentration risk
- Revenue estimate: $4,000 (diversification + management fees)
- Action: Risk review, diversification strategy, hedging options

---

## 🧪 Testing

### Current Status
- **Unit Tests:** To be implemented
- **Integration Tests:** To be implemented
- **Test Coverage Goal:** 80%+

### Verification

```bash
# Verify all components work
python verify_implementation.py

# Output:
# ✓ All 9 model classes imported successfully
# ✓ All 3 service classes imported successfully
# ✓ All 15 tool functions imported successfully
# ✓ Matching successful: 1 opportunity created
# ✓ Ranking successful: 1 opportunity ranked
# ✓ Report generation successful
# ✓ VERIFICATION COMPLETE
```

### Future Test Structure

```
tests/
├── unit/
│   ├── test_models.py              # Pydantic validation tests
│   ├── test_matching_engine.py     # Criterion evaluation tests
│   ├── test_revenue_calculator.py  # Formula calculation tests
│   └── test_tools.py               # Tool interface tests
├── integration/
│   └── test_workflows.py           # End-to-end workflow tests
└── fixtures/
    ├── scenarios.json              # Test scenarios
    └── clients.json                # Test clients
```

---

## 🔧 Development Workflow

### Adding a New Scenario

1. **Create JSON file** in `data/scenarios/`:
```json
{
  "scenario_id": "NEW-001",
  "name": "New Opportunity Type",
  "description": "Clear description of opportunity",
  "criteria": [
    {
      "field": "client.age",
      "operator": "greater_than",
      "value": 65,
      "weight": 1.0
    }
  ],
  "revenue_formula": {
    "formula_type": "percentage",
    "base_rate": 0.01,
    "multiplier_field": "portfolio.total_value"
  }
}
```

2. **Test with sample clients**:
```bash
python -c "from src.tools import load_scenarios; print(load_scenarios('data/scenarios'))"
```

3. **Run matching** with real clients to validate

### Adding a New Operator

1. Edit `src/services/matching_engine.py`
2. Add operator to `_evaluate_operator()` method
3. Add tests in `tests/unit/test_matching_engine.py`
4. Update documentation

### Adding a New Formula Type

1. Edit `src/services/revenue_calculator.py`
2. Add formula type to `_calculate_by_type()` method
3. Add tests in `tests/unit/test_revenue_calculator.py`
4. Update documentation and examples

---

## 🔑 Key Dependencies

```
Core:
- anthropic >= 0.40.0         # Claude SDK
- pydantic >= 2.0.0           # Data validation
- python-dotenv >= 1.0.0      # Environment variables

Development:
- pytest >= 7.4.0             # Testing
- black >= 23.0.0             # Code formatting
- ruff >= 0.1.0               # Linting
- mypy >= 1.7.0               # Type checking

Total: 31 packages
```

---

## 📝 Code Quality Standards

### Biblical Principles Applied

**TRUTH** - All operations are observable and traceable
- Every match decision documented with specific reasons
- Revenue calculations show step-by-step breakdown
- Clear logging at INFO and DEBUG levels

**HONOR** - Respect for client data and user needs
- Client data stays local (no external transmission)
- Clear data sovereignty
- Simple, helpful error messages

**EXCELLENCE** - Production-grade from inception
- Full type safety with Pydantic
- Comprehensive error handling
- No "fix it later" mentality
- Proper validation at every boundary

**SERVE** - Make advisor's job easier
- Multiple report formats
- Flexible configuration
- Clear next actions
- Fast performance

### Code Standards

- **Type Hints:** All functions fully typed
- **Docstrings:** Comprehensive (Args, Returns, Raises, Examples)
- **Error Handling:** Try-except with specific errors
- **Validation:** Pydantic at data boundaries
- **Logging:** Structured logging throughout
- **Naming:** Clear, descriptive names (no abbreviations)

---

## 🚧 Current Status & Roadmap

### ✅ Phase 1 Complete (Current)
- [x] Architecture design
- [x] Pydantic models (3 files, 500 lines)
- [x] Services layer (3 files, 786 lines)
- [x] Tools implementation (5 files, 1,267 lines)
- [x] Virtual environment setup
- [x] Dependencies installed
- [x] Basic documentation (README, IMPLEMENTATION_SUMMARY)
- [x] Verification script

### 🚧 Phase 2: Integration (Next)
- [ ] Create main agent file (`src/agent.py`)
- [ ] Create CLI entry point (`src/main.py`)
- [ ] Register tools with Claude SDK
- [ ] Define agent system prompt
- [ ] Test conversation workflow
- [ ] End-to-end testing

### 📋 Phase 3: Testing & Polish
- [ ] Unit tests (80%+ coverage)
- [ ] Integration tests
- [ ] Test fixtures and mock data
- [ ] Example scenario files (3 MVP scenarios)
- [ ] Example client data files
- [ ] Google Sheets integration (optional)

### 🎯 Phase 4: Production Ready
- [ ] Complete CLAUDE.md
- [ ] Comprehensive README
- [ ] Usage examples and tutorials
- [ ] Deployment guide
- [ ] Update root repository CLAUDE.md
- [ ] Add to agent comparison matrix
- [ ] Document learnings in memory system

---

## 💡 Key Learnings & Patterns

### What Worked Well

**Three-Layer Architecture**
- Clear separation: models → services → tools
- Easy to test each layer independently
- Services are reusable beyond Claude SDK

**Pydantic Everywhere**
- Catches errors at data boundaries
- Self-documenting with field descriptions
- JSON serialization just works

**Flexible Matching Criteria**
- Easy to add new scenarios without code changes
- Weighted scoring allows nuanced matching
- Full traceability with MatchDetail objects

**Multiple Revenue Formulas**
- Handles diverse advisor compensation models
- Tiered formulas match real-world fee structures
- Calculation breakdowns build trust

### Patterns to Reuse

**Tool → Service Separation**
```python
# Tool (thin wrapper)
def match_clients(...):
    engine = MatchingEngine()
    return engine.match(...)

# Service (thick logic)
class MatchingEngine:
    def match(self, clients, scenarios):
        # All business logic here
```

**Pydantic Factory Methods**
```python
class Opportunity(BaseModel):
    @classmethod
    def from_match(cls, client, scenario, ...):
        # Complex construction logic
        return cls(...)
```

**Detailed Breakdowns for Observability**
```python
class MatchDetail(BaseModel):
    criterion: MatchCriterion
    matched: bool
    actual_value: Any
    expected_value: Any
    explanation: str  # Plain English
```

---

## 🔗 Integration Points

### Future Enhancements

**Google Sheets Integration**
- Service in `src/services/google_sheets_service.py`
- OAuth 2.0 authentication
- Direct client data loading
- Real-time updates

**CRM Integration**
- Export opportunities to CRM
- Two-way sync of client data
- Opportunity tracking

**Reporting Dashboard**
- Web interface for report viewing
- Historical tracking
- Performance analytics

**Scenario Library**
- Shareable scenario marketplace
- Best-practice templates
- Community contributions

---

## 📚 Additional Resources

**Documentation:**
- [README.md](README.md) - Quick start guide
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Detailed implementation report
- [Architecture Blueprint](docs/architecture.md) - Complete architecture design (if created by ArchitectAgent)

**Related Agents:**
- [FIA Analyzer](../fia-analyzer/) - Similar architecture pattern
- [Google Drive Agent](../../../strands-agents/python/google-drive-agent/) - Service layer pattern

**External Links:**
- [Claude Agent SDK Docs](https://docs.anthropic.com/claude/agent-sdk)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [OpportunityIQ Skill Reference](../../../../docs/ideas/opportunityiq/SKILL.md)

---

## 🤝 Contributing

### Code Style

- Follow PEP 8
- Use Black for formatting
- Use Ruff for linting
- Use MyPy for type checking

### Commit Messages

```
feat: add new matching operator for date ranges
fix: correct revenue calculation for tiered formulas
docs: update CLAUDE.md with usage examples
test: add unit tests for matching engine
refactor: extract common validation logic
```

### Pull Requests

- Include tests for new features
- Update documentation
- Verify all tests pass
- Run verification script

---

## 📞 Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'src'`
- **Solution:** Ensure you're in the project root directory and virtual environment is activated

**Issue:** `pydantic.ValidationError` when loading scenarios
- **Solution:** Check JSON syntax and required fields against Scenario model

**Issue:** No opportunities matched
- **Solution:** Lower `min_match_threshold` or check client data has required fields

**Issue:** Revenue calculation returns $0
- **Solution:** Verify `multiplier_field` exists in client profile and has non-zero value

### Debugging Tips

**Enable DEBUG logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Inspect match details:**
```python
for opp in opportunities:
    print(f"Client: {opp.client_name}")
    print(f"Match score: {opp.match_score}%")
    for detail in opp.match_details:
        print(f"  - {detail.criterion_description}: {detail.reason}")
```

**Verify scenario criteria:**
```python
scenarios = load_scenarios("data/scenarios")
for scenario in scenarios:
    print(f"{scenario.scenario_id}: {len(scenario.criteria)} criteria")
    for crit in scenario.criteria:
        print(f"  - {crit.field} {crit.operator} {crit.value}")
```

---

## 🎯 Success Metrics

The Client Matcher Agent is successful when:

- [x] All 5 tools implemented and working
- [x] All 3 services functional
- [x] All models validated with Pydantic
- [ ] 80%+ test coverage
- [ ] Agent integrated with Claude SDK
- [ ] End-to-end workflow tested
- [ ] Documentation complete
- [ ] Example data files created

---

**Remember:** *"Whatever you do, work heartily, as for the Lord"* - Colossians 3:23

Excellence is not about complexity. It's about doing simple things consistently well, with transparency, respect for users, and continuous improvement.

---

*Last updated: 2025-11-21*
*Version: 1.0.0 - Phase 1 Complete*
*Next phase: Agent Integration*
