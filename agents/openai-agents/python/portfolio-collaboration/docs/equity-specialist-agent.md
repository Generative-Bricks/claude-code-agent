# Equity Specialist Agent

**Status:** ✅ Production-Ready (Wave 1)
**Agent Type:** Handoff Agent
**Framework:** OpenAI Agents SDK v0.5.1
**Model:** GPT-4o

---

## Overview

The Equity Specialist Agent provides deep-dive equity analysis when handed off from the Portfolio Manager. It specializes in sector allocation analysis, valuation metrics, growth vs value classification, and equity-specific recommendations tailored to client risk profiles.

## Purpose

When the Portfolio Manager needs detailed equity insights beyond basic portfolio analysis, it hands off control to the Equity Specialist. This agent performs comprehensive equity analysis and returns detailed findings to inform investment decisions.

## Core Capabilities

### 1. Sector Analysis
- **Breakdown by Sector:** Analyzes allocation across all equity sectors (Technology, Healthcare, Financials, etc.)
- **Concentration Detection:** Identifies over-concentrated sectors (>30% allocation)
- **Diversification Assessment:** Flags under-represented sectors (<5% allocation)
- **Risk Alignment:** Evaluates sector mix against client risk tolerance

### 2. Valuation Metrics
- **Price-to-Earnings (P/E) Ratio:** Portfolio-level P/E calculation
- **Price-to-Book (P/B) Ratio:** Value vs book value assessment
- **Dividend Yield:** Income generation potential
- **Valuation Commentary:** Interpretation (elevated, attractive, or market-level valuations)

### 3. Growth vs Value Classification
- **Growth Sectors:** Technology, Communication Services, Consumer Discretionary
- **Value Sectors:** Utilities, Consumer Staples, Financials, Energy
- **Neutral Sectors:** Healthcare, Industrials, Materials, Real Estate (split 50/50)
- **Allocation Analysis:** Calculates % split and assesses alignment with strategy

### 4. Risk Tolerance Alignment
- **Conservative:** Emphasis on capital preservation, dividend income, lower volatility
- **Moderate:** Balanced growth and stability with diversified sectors
- **Aggressive:** Growth-oriented with higher volatility tolerance

### 5. Equity-Specific Recommendations
- Sector diversification suggestions
- Valuation-based rebalancing advice
- Growth/value balance adjustments
- Income generation enhancements

---

## Input Schema

**EquityDeepDiveRequest** (from `src/models/schemas.py`):

```python
{
    "portfolio": Portfolio,           # Portfolio object with holdings
    "client_profile": ClientProfile,  # Client risk tolerance and goals
    "focus_areas": List[str],         # Areas to analyze (e.g., "Valuation", "Sector allocation")
    "questions": Optional[List[str]]  # Specific client questions
}
```

---

## Output Schema

**EquityDeepDiveReport** (from `src/models/schemas.py`):

```python
{
    "focus_areas_analyzed": List[str],              # Areas covered in analysis
    "sector_analysis": Dict[str, str],              # Sector-by-sector commentary
    "valuation_metrics": Dict[str, float],          # P/E, P/B, dividend_yield
    "growth_vs_value_split": Dict[str, float],      # Growth % and Value %
    "recommendations": List[str],                   # Actionable equity recommendations
    "detailed_analysis": str                        # Comprehensive narrative analysis
}
```

---

## Usage Examples

### Programmatic Usage (Function Call)

```python
from src.agents.equity_specialist import perform_equity_deep_dive
from src.data.mock_portfolios import load_portfolio, load_client_profile

# Load data
portfolio = load_portfolio("PORT001")
client = load_client_profile("CLIENT001")

# Perform analysis
report = perform_equity_deep_dive(
    portfolio=portfolio,
    client_profile=client,
    focus_areas=["Sector allocation", "Valuation", "Growth vs Value"],
    questions=["Is the portfolio too concentrated?"]
)

# Access results
print(report.sector_analysis)
print(report.valuation_metrics)
print(report.recommendations)
```

### Agent Handoff Usage (OpenAI Agents SDK)

```python
from agents import Agent, Runner
from src.agents.equity_specialist import equity_specialist_agent

# Portfolio Manager agent with equity specialist handoff
portfolio_manager = Agent(
    name="Portfolio Manager",
    instructions="You coordinate portfolio analysis. Hand off to the Equity Specialist for deep equity analysis.",
    handoffs=[equity_specialist_agent],
    model="gpt-4o"
)

# Run with handoff
result = await Runner.run(
    portfolio_manager,
    input="I need a detailed equity analysis of this portfolio."
)
```

---

## Analysis Logic

### Sector Allocation Thresholds

```python
# High concentration (action needed)
if allocation > 30%:
    "Consider diversification to reduce sector-specific risk"

# Low allocation (opportunity)
if allocation < 5%:
    "May want to increase for better diversification"

# Appropriate allocation
if 5% <= allocation <= 30%:
    "Appropriate allocation for a diversified portfolio"
```

### Valuation Interpretations

```python
# P/E Ratio
if pe_ratio > 25:
    "Elevated valuations - potential volatility risk"
elif pe_ratio < 17:
    "Attractive valuations - good value for long-term growth"
else:
    "In line with broad market averages"
```

### Growth vs Value Balance

```python
# Conservative client
if growth_pct > 60:
    "Growth allocation may be aggressive for conservative risk tolerance"

# Aggressive client
if value_pct > 60:
    "Value allocation may limit upside potential for aggressive strategy"

# Moderate client
if abs(growth_pct - value_pct) > 30:
    "Consider rebalancing for more balanced approach"
```

---

## Implementation Details

### File Structure

```
src/agents/equity_specialist.py
├── Agent Definition (equity_specialist_agent)
├── Analysis Functions
│   ├── calculate_sector_allocations()
│   ├── generate_sector_analysis()
│   ├── calculate_valuation_metrics()
│   ├── classify_growth_vs_value()
│   ├── generate_equity_recommendations()
│   └── generate_detailed_analysis()
└── Main Entry Point (perform_equity_deep_dive())
```

### Key Functions

**`calculate_sector_allocations(portfolio)`**
- Filters equity holdings
- Calculates % allocation per sector
- Tracks top holdings by sector

**`generate_sector_analysis(sector_allocations, risk_tolerance)`**
- Analyzes concentration levels
- Provides sector-specific commentary
- Aligns with client risk tolerance

**`calculate_valuation_metrics(equity_holdings)`**
- Mock implementation (Wave 1)
- Realistic metrics based on sector composition
- Production: Replace with real market data API

**`classify_growth_vs_value(equity_holdings)`**
- Rule-based classification by sector
- Calculates allocation percentages
- Handles neutral sectors (50/50 split)

**`generate_equity_recommendations(...)`**
- Actionable recommendations
- Based on concentration, valuation, balance, and risk tolerance
- Prioritizes highest-impact changes

**`generate_detailed_analysis(...)`**
- Comprehensive narrative report
- Synthesizes all analysis components
- Professional formatting for Portfolio Manager consumption

---

## Testing

### Run Example Script

```bash
cd /home/seed537/projects/claude-code-agent/agents/openai-agents/python/portfolio-collaboration
source .venv/bin/activate
python examples/equity_specialist_example.py
```

### Expected Output

- Portfolio composition summary
- Sector-by-sector analysis with percentages
- Valuation metrics (P/E, P/B, dividend yield)
- Growth vs Value split (%)
- 2-5 actionable recommendations
- Detailed narrative analysis (15-20 lines)

### Sample Analysis (CLIENT001 - Conservative)

```
Portfolio: $1,000,000 (5 sectors, 8 holdings)
Risk Tolerance: Conservative

Sector Allocation:
- Consumer Staples: 31.3% (HIGH CONCENTRATION)
- Telecommunications: 26.7%
- Energy: 16.1%
- Healthcare: 14.4%
- Industrials: 11.5%

Valuation Metrics:
- P/E: 14.6 (Attractive)
- P/B: 4.0
- Dividend Yield: 3.9%

Growth vs Value: 26.3% Growth / 73.7% Value

Recommendations:
1. Reduce Consumer Staples concentration from 31.3%
2. Value-oriented positioning aligns well with conservative profile
3. Consider adding more sectors (currently 5, target 6-8)
```

---

## Future Enhancements (Wave 2+)

### Wave 2: Market Data Integration
- Real-time P/E, P/B, dividend yield from Yahoo Finance API
- Historical valuation ranges for context
- Sector performance trends

### Wave 3: Advanced Analytics
- Sector momentum analysis
- Factor exposure (momentum, quality, low volatility)
- Style drift detection over time

### Wave 4: AI-Powered Insights
- Natural language Q&A about equity holdings
- Comparative analysis vs peer portfolios
- Scenario modeling (e.g., "What if tech stocks drop 20%?")

---

## Design Decisions

### Why Handoff Agent (Not Tool)?

**Handoff agents take control of the conversation:**
- Can perform multi-step reasoning
- Generate narrative analysis (not just data)
- Ask follow-up questions if needed
- Return control when complete

**Tools are for discrete data retrieval:**
- Single input → single output
- No conversation state
- Limited to structured data

**Equity analysis requires narrative reasoning** → Handoff agent is the right choice.

### Why Mock Valuation Metrics (Wave 1)?

**Reasons:**
1. Focus on agent architecture first
2. Avoid API dependencies in early testing
3. Demonstrate analysis logic without external services
4. Clear integration points for Wave 2

**Mock metrics are:**
- Realistic (based on sector composition)
- Consistent (seeded by portfolio composition)
- Documented (comments explain they're mock)

---

## Biblical Principles Applied

### TRUTH
- All calculations are transparent and explainable
- Mock data clearly labeled as mock
- Analysis logic documented with thresholds

### HONOR
- User-first: Analysis tailored to client risk tolerance
- Respects client goals and constraints
- Provides clear, actionable recommendations

### EXCELLENCE
- Production-grade from inception
- Comprehensive error handling
- Type hints and docstrings throughout

### SERVE
- Simplifies complex equity analysis
- Clear, accessible insights (not jargon-heavy)
- Actionable recommendations prioritized

### PERSEVERE
- Handles edge cases (no equity holdings, missing sectors)
- Graceful degradation with partial data
- Consistent results under varying inputs

### SHARPEN
- Modular design (easy to enhance each function)
- Clear separation of concerns
- Ready for real market data integration (Wave 2)

---

## Success Criteria

- [x] File created at correct location (`src/agents/equity_specialist.py`)
- [x] Uses OpenAI Agents SDK handoff pattern
- [x] Returns proper `EquityDeepDiveReport` Pydantic model
- [x] Provides detailed sector analysis with commentary
- [x] Calculates valuation metrics and growth/value split
- [x] Generates actionable equity-specific recommendations
- [x] Has comprehensive docstrings and type hints
- [x] Can be imported and used by Portfolio Manager
- [x] Example script demonstrates functionality
- [x] All imports resolve correctly

---

**Last Updated:** 2025-01-14
**Wave Status:** Wave 1 Complete
**Next Wave:** Wave 2 (Risk Analyst & Compliance Officer Agents)
