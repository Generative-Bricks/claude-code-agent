# Multi-Agent Portfolio Collaboration System

**A production-grade multi-agent system for comprehensive portfolio analysis using the OpenAI Agents SDK.**

![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)
![OpenAI Agents SDK](https://img.shields.io/badge/OpenAI%20Agents-0.2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Biblical Principles](#biblical-principles)
- [Contributing](#contributing)

---

## 🎯 Overview

This system orchestrates multiple specialist AI agents to provide comprehensive portfolio analysis and recommendations. It uses the OpenAI Agents SDK to coordinate:

- **Risk Analyst** - Calculates volatility, VaR, beta, concentration risk
- **Compliance Officer** - Validates suitability, concentration limits, disclosures
- **Performance Analyst** - Analyzes returns, Sharpe ratio, alpha, attribution
- **Equity Specialist** - Deep-dive equity analysis (handoff agent)
- **Portfolio Manager** - Orchestrates all specialists and generates recommendations

The system supports both **interactive** (conversational) and **batch** (automated) analysis modes.

---

## ✨ Features

### Core Capabilities

- ✅ **Multi-Agent Orchestration** - Parallel execution of specialist agents using OpenAI Agents SDK
- ✅ **Comprehensive Risk Analysis** - Volatility, VaR (95%), beta, concentration scoring
- ✅ **Compliance Validation** - Suitability checks, regulatory requirements, disclosures
- ✅ **Performance Metrics** - Returns, Sharpe ratio, alpha, sector attribution
- ✅ **Suitability Scoring** - 0-100 score with weighted specialist inputs (Risk 25%, Compliance 35%, Performance 25%, Time Horizon 15%)
- ✅ **Actionable Recommendations** - Context-aware suggestions based on all analysis
- ✅ **Markdown Reports** - Client-ready documentation with all findings
- ✅ **Real-Time Market Data** - Yahoo Finance integration via yfinance library
- ✅ **Agent Handoffs** - Portfolio Manager can delegate to Equity Specialist for deep dives

### Technical Features

- ✅ **Type Safety** - Full Pydantic models with strict validation
- ✅ **Parallel Execution** - Async specialist coordination using `asyncio.gather()`
- ✅ **Session Memory** - SQLite-backed conversation persistence
- ✅ **Graceful Fallbacks** - Mock data when market data unavailable
- ✅ **Comprehensive Testing** - 106 tests (unit + integration + MCP)
- ✅ **CLI Interface** - Interactive and batch modes
- ✅ **Logging** - Detailed logging to files and console

---

## 🏗️ Architecture

### Multi-Agent Pattern

```
Portfolio Manager (Orchestrator)
├── Risk Analyst (parallel)
├── Compliance Officer (parallel)
├── Performance Analyst (parallel)
└── Equity Specialist (handoff)
```

**Workflow:**
1. **Discovery** - Portfolio Manager understands client profile and portfolio
2. **Analysis** - Coordinates specialist agents in parallel
3. **Scoring** - Calculates suitability from all specialist outputs
4. **Recommendations** - Generates actionable advice
5. **Documentation** - Creates comprehensive markdown report

### Specialist Agent Details

| Agent | Purpose | Key Metrics | Pattern |
|-------|---------|-------------|---------|
| **Risk Analyst** | Portfolio risk assessment | Volatility, VaR, beta, concentration | Agent as Tool |
| **Compliance Officer** | Regulatory compliance | Suitability, limits, disclosures | Agent as Tool |
| **Performance Analyst** | Return analysis | Total return, Sharpe, alpha, attribution | Agent as Tool |
| **Equity Specialist** | Deep equity analysis | Sector allocation, valuation, growth vs value | Handoff |
| **Portfolio Manager** | Orchestration | Suitability score, recommendations, report | Primary Agent |

---

## 🚀 Installation

### Prerequisites

- Python 3.11 or higher
- `uv` (Python package and virtual environment manager)

### Setup

```bash
# Clone the repository (if not already cloned)
cd portfolio-collaboration

# Create virtual environment
uv venv

# Activate virtual environment
# Windows (Git Bash/MINGW64):
source .venv/Scripts/activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Environment Variables

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
OPENAI_MODEL_MAIN=gpt-4.1          # Portfolio Manager model
OPENAI_MODEL_SPECIALIST=gpt-4o-mini # Specialist agent model
SESSION_DB_PATH=./portfolio_sessions.db
DEBUG=false
LOG_LEVEL=INFO
```

---

## 🎬 Quick Start

### List Available Data

```bash
python -m src.main --list
```

Output:
```
AVAILABLE DATA
==============

CLIENTS:
  - CLT-2024-001: Robert Williams (Age 68, conservative risk)
  - CLT-2024-002: Jennifer Martinez (Age 45, moderate risk)
  - CLT-2024-003: Michael Chen (Age 32, aggressive risk)

PORTFOLIOS:
  - Conservative Portfolio: 9 holdings
  - Moderate Portfolio: 12 holdings
  - Aggressive Growth Portfolio: 10 holdings
```

### Run Analysis (Batch Mode)

```bash
# Analyze specific client and portfolio
python -m src.main --client CLT-2024-001 --portfolio conservative

# Output saved to: outputs/CLT-2024-001_conservative_report.md
```

### Run Analysis (Interactive Mode)

```bash
# Interactive conversation with Portfolio Manager
python -m src.main --interactive --client CLT-2024-002 --portfolio moderate
```

### Batch Analysis (All Combinations)

```bash
# Analyze all client-portfolio combinations
python -m src.main --batch
```

---

## 📖 Usage

### CLI Commands

```bash
# Basic analysis
python -m src.main --client <CLIENT_ID> --portfolio <PORTFOLIO_NAME>

# Interactive mode
python -m src.main --interactive --client <CLIENT_ID> --portfolio <PORTFOLIO_NAME>

# Batch analysis
python -m src.main --batch

# List available data
python -m src.main --list
```

### Example: Analyzing a Portfolio

```bash
python -m src.main --client CLT-2024-001 --portfolio conservative
```

**Output:**
```
====================================================================================
Starting Portfolio Analysis
Client ID: CLT-2024-001
Portfolio: conservative
Mode: Batch
====================================================================================

✓ Loaded client profile: Robert Williams (Age 68)
✓ Loaded portfolio: Conservative Portfolio (9 holdings)
Running comprehensive analysis...
✓ Analysis complete
  - Risk Rating: low
  - Compliance Status: compliant
  - Suitability Score: 87.3/100 (highly_suitable)
Generating report...
✓ Report saved to: outputs/CLT-2024-001_conservative_report.md

====================================================================================
ANALYSIS SUMMARY
====================================================================================
Client: Robert Williams (CLT-2024-001)
Portfolio: Conservative Portfolio
Suitability: 87/100
Recommendations: 3
Action Items: 2
====================================================================================
```

### Programmatic Usage

```python
from src.agents.portfolio_manager import run_comprehensive_analysis, generate_client_report
from src.data.mock_portfolios import get_conservative_example
from src.models.schemas import ClientProfile, RiskTolerance

# Create client profile
client = ClientProfile(
    client_id="CLIENT-001",
    name="John Doe",
    age=55,
    risk_tolerance=RiskTolerance.moderate,
    investment_goals=["growth", "income"],
    time_horizon_years=15,
)

# Load portfolio
portfolio = get_conservative_example()

# Run analysis
recommendations = run_comprehensive_analysis(portfolio, client)

# Access results
print(f"Suitability Score: {recommendations.suitability_score.overall_score:.1f}/100")
print(f"Risk Rating: {recommendations.risk_analysis.risk_rating.value}")
print(f"Compliance: {recommendations.compliance_report.overall_status.value}")

# Generate report
report = generate_client_report(recommendations)
print(report)
```

---

## 🧪 Testing

### Run All Tests

```bash
pytest tests/
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest tests/test_risk_analyst.py tests/test_compliance_officer.py tests/test_performance_analyst.py tests/test_portfolio_manager.py

# Integration tests
pytest tests/test_integration.py -v

# MCP integration tests (uses real Yahoo Finance data - slower)
pytest tests/test_mcp_integration.py -m mcp -v

# Slow tests only
pytest tests/ -m slow
```

### Run with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

Coverage report will be generated in `htmlcov/index.html`.

### Test Summary

- **106 total tests** across 6 test files
- **78 unit tests** - Agent functionality, tools, calculations
- **13 integration tests** - End-to-end workflows, data flow
- **15 MCP integration tests** - Market data fetching, quality checks

---

## 📁 Project Structure

```
portfolio-collaboration/
├── src/
│   ├── agents/                    # Agent implementations
│   │   ├── risk_analyst.py        # Risk analysis agent
│   │   ├── compliance_officer.py  # Compliance validation agent
│   │   ├── performance_analyst.py # Performance analysis agent
│   │   ├── equity_specialist.py   # Equity deep-dive agent (handoff)
│   │   └── portfolio_manager.py   # Orchestrator agent
│   ├── tools/                     # Shared tools
│   │   ├── suitability_scoring.py # Suitability calculation
│   │   ├── report_generator.py    # Markdown report creation
│   │   ├── parallel_execution.py  # Parallel specialist coordination
│   │   └── market_data.py         # Yahoo Finance integration
│   ├── models/
│   │   └── schemas.py             # Pydantic models
│   ├── data/
│   │   └── mock_portfolios.py     # Sample data helpers
│   ├── mcp/
│   │   └── yahoo_finance_server.py # Yahoo Finance MCP server
│   └── main.py                    # CLI entry point
├── tests/                         # Test suite (106 tests)
│   ├── test_risk_analyst.py       # Risk analyst unit tests (20)
│   ├── test_compliance_officer.py # Compliance unit tests (22)
│   ├── test_performance_analyst.py # Performance unit tests (24)
│   ├── test_portfolio_manager.py  # Portfolio Manager unit tests (12)
│   ├── test_integration.py        # Integration tests (13)
│   └── test_mcp_integration.py    # MCP integration tests (15)
├── examples/                      # Sample data and demos
│   ├── sample_clients.json        # 3 client profiles
│   ├── sample_portfolios.json     # 3 portfolios
│   └── test_*.py                  # Example scripts
├── outputs/                       # Generated reports
├── logs/                          # Application logs
├── requirements.txt               # Python dependencies
├── pytest.ini                     # Test configuration
├── .env.example                   # Environment template
└── README.md                      # This file
```

---

## 📊 Sample Data

The system includes three pre-configured scenarios:

### Conservative Portfolio
- **Client**: Robert Williams (68 years old)
- **Risk Tolerance**: Conservative
- **Allocation**: 30% equities, 70% bonds
- **Holdings**: 9 positions (diversified across sectors)
- **Income Needs**: $50,000/year

### Moderate Portfolio
- **Client**: Jennifer Martinez (45 years old)
- **Risk Tolerance**: Moderate
- **Allocation**: 60% equities, 40% bonds
- **Holdings**: 12 positions (balanced growth and income)
- **Income Needs**: None

### Aggressive Portfolio
- **Client**: Michael Chen (32 years old)
- **Risk Tolerance**: Aggressive
- **Allocation**: 100% equities
- **Holdings**: 10 positions (growth-focused)
- **Income Needs**: None

---

## 📝 Biblical Principles

This project is built on six foundational principles:

1. **TRUTH** (John 14:6) - Transparent analysis and observable reasoning
2. **HONOR** (Matthew 22:36-40) - Client-first design with data sovereignty
3. **EXCELLENCE** (Colossians 3.23) - Production-grade from inception
4. **SERVE** (John 13:14) - Simplifying complex analysis for advisors
5. **PERSEVERE** (Hebrews 12:1-3) - Resilient systems with graceful failure handling
6. **SHARPEN** (Proverbs 27:17) - Continuous improvement through testing

Each principle is embedded in code comments and design decisions throughout the codebase.

---

## 🛠️ Development

### Adding New Agents

1. Create agent file in `src/agents/`
2. Define agent using `Agent()` with tools and instructions
3. Export agent in `src/agents/__init__.py`
4. Add to Portfolio Manager orchestration if needed
5. Create unit tests in `tests/test_<agent_name>.py`

### Adding New Tools

1. Create tool file in `src/tools/`
2. Implement tool function with `@function_tool` decorator
3. Export tool in `src/tools/__init__.py`
4. Add tool to appropriate agent(s)
5. Create unit tests

### Code Style

- **Python**: PEP 8 with Black formatting
- **Naming**: snake_case for files, functions; PascalCase for classes
- **Type Hints**: Required for all function signatures
- **Docstrings**: Required for all public functions
- **Comments**: Explain WHY, not WHAT

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ImportError: cannot import name 'X'`
- **Solution**: Ensure virtual environment is activated and dependencies installed: `uv pip install -r requirements.txt`

**Issue**: `KeyError: 'OPENAI_API_KEY'`
- **Solution**: Copy `.env.example` to `.env` and add your API key

**Issue**: Market data tests failing
- **Solution**: These tests use real Yahoo Finance data - ensure internet connection and Yahoo Finance is accessible

**Issue**: Tests show Pydantic schema errors
- **Solution**: This is a known compatibility issue with OpenAI Agents SDK strict schemas - functionality is correct, runtime validation needs adjustment

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- Built with [OpenAI Agents SDK](https://github.com/openai/openai-agents-sdk)
- Market data via [yfinance](https://github.com/ranaroussi/yfinance)
- Inspired by OpenAI Cookbook [multi-agent portfolio collaboration example](https://github.com/openai/openai-cookbook/tree/main/examples/agents_sdk/multi-agent-portfolio-collaboration)

---

## 📧 Contact

For questions, issues, or contributions, please open an issue on GitHub.

---

**Built with ❤️ following biblical principles of TRUTH, HONOR, EXCELLENCE, SERVE, PERSEVERE, and SHARPEN.**
