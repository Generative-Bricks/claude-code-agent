# FIA Analyzer Agent

**Status:** In Development (Week 1 Complete)

**Purpose:** Analyze Fixed Indexed Annuity products for financial advisors using Claude SDK with Skills integration.

## Architecture

- **Framework:** Claude SDK (Python)
- **Skills:** Anthropic PDF skill + Custom FIA Analysis skill
- **MCP:** Fetch server for web content retrieval
- **Tools:** 3 custom tools (search, extract, analyze)

## Quick Start

### 1. Setup (First Time Only)

```bash
cd /home/seed537/projects/claude-code-agent/agents/claude-sdk/python/fia-analyzer

# Create virtual environment
uv venv

# Install dependencies
uv pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 2. Running the Agent

**Basic Product Analysis:**
```bash
uv run python -m src.main --product "Allianz Benefit Control"
```

**With Carrier Filter:**
```bash
uv run python -m src.main --product "Peak 10" --carrier "Nationwide"
```

**With Client Profile (Suitability Analysis):**
```bash
uv run python -m src.main --product "Allianz 222" --client-profile examples/sample_client.json
```

**Save Results to JSON:**
```bash
uv run python -m src.main --product "Allianz Benefit Control" --output results.json
```

**Verbose Logging (Debug Mode):**
```bash
uv run python -m src.main --product "Allianz 222" --client-profile examples/sample_client.json --verbose
```

## Testing Tools Individually

```bash
# Test Search Tool
uv run python -c "from src.tools.search_fia_products import search_fia_products; import json; print(json.dumps(search_fia_products('Allianz Benefit Control'), indent=2))"

# Test Extract Tool (requires markdown content)
uv run python -c "from src.tools.extract_fia_rates import extract_fia_rates; print('Extract tool ready - requires markdown content')"

# Test Analyze Tool (requires product and client profile)
uv run python -c "from src.tools.analyze_product_fit import analyze_product_fit; print('Analyze tool ready - requires FIAProduct and ClientProfile models')"

# Test data models import
uv run python -c "from src.models import FIAProduct, ClientProfile, SuitabilityScore; print('All data models imported successfully')"
```

## Project Structure

```
fia-analyzer/
├── .env                    # Environment variables (not in git)
├── .env.example            # Template for environment setup
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── scripts/               # Utility scripts
│   └── upload_fia_skill.py # Upload FIA Analysis Skill to workspace
├── skill/                 # FIA Analysis Skill (for upload to workspace)
│   ├── SKILL.md           # Skill instructions with YAML frontmatter
│   ├── FIA_SKILL_INSTRUCTIONS.md
│   ├── QUICK_START_PROMPT.md
│   ├── README.md
│   └── allianz_benefit_control_analysis.* # Example outputs
├── src/
│   ├── __init__.py        # Package initialization
│   ├── agent.py           # Main agent implementation
│   ├── main.py            # CLI entry point
│   ├── models/            # Pydantic data models
│   │   ├── __init__.py
│   │   ├── fia_product.py         # FIA product model
│   │   ├── client_profile.py      # Client profile model
│   │   └── suitability_score.py   # Suitability scoring model
│   ├── tools/             # Custom tools
│   │   ├── __init__.py
│   │   ├── search_fia_products.py  # Search tool
│   │   ├── extract_fia_rates.py    # Extract tool
│   │   └── analyze_product_fit.py  # Analyze tool
│   └── services/          # Future services (e.g., API integrations)
├── examples/
│   └── sample_client.json # Example client profile
├── outputs/               # Analysis results output directory
└── tests/                 # Unit and integration tests (TBD)
```

## Environment Variables

Required in `.env`:
- `ANTHROPIC_API_KEY` - Your Anthropic API key (required)
- `CLAUDE_MODEL` - Claude model ID (optional, defaults to claude-sonnet-4-5-20250929)
- `FIA_SKILL_ID` - Custom skill ID (optional, upload via Claude Code UI first)
- `SEARCH_API_KEY` - Optional for production search API

## Skills Setup

### Manual Upload (Required)

**Note:** The Anthropic Python SDK does not currently expose a Skills upload API. The `client.beta.skills.*` endpoints shown in some cookbooks are not available in the public SDK yet.

```bash
cd agents/claude-sdk/python/fia-analyzer

# Step 1: Get upload instructions
python scripts/upload_fia_skill.py
```

This will display:
- Files in your skill/ directory
- Manual upload instructions
- Where to upload (Claude Code UI or Anthropic console)

**Manual Upload Steps:**

1. **Open Claude Code UI or https://console.anthropic.com/**
   - Navigate to Skills panel

2. **Upload the skill directory:**
   - Location: `agents/claude-sdk/python/fia-analyzer/skill/`
   - Display title: "FIA Analysis Skill"
   - Upload all files in the skill/ directory

3. **Copy the returned skill_id**
   - Format: `skill_01AbCdEfGhIjKlMnOpQrStUv`

4. **Save to .env automatically:**
   ```bash
   python scripts/upload_fia_skill.py --save-id <your_skill_id>
   ```

**Note:** The agent will work without the custom skill - it just won't have the specialized FIA Analysis skill for advanced report generation. The Anthropic PDF skill will still be available.

## 5-Stage Workflow

The agent implements a structured workflow:

1. **Discovery** - Understand what the user wants to analyze
2. **Search** - Find relevant FIA products using search_fia_products tool
3. **Fetch & Extract** - Retrieve product details from URLs and extract structured data
4. **Analyze** - Perform suitability analysis (if client profile provided)
5. **Generate Report** - Use Claude skills (PDF + custom FIA skill) to create final report

## Tools Overview

### 1. search_fia_products
- **Purpose:** Search for FIA products by name and carrier
- **Input:** product_name (required), carrier (optional)
- **Output:** List of matching products with URLs and summaries
- **Current Implementation:** Mock data for known products

### 2. extract_fia_rates
- **Purpose:** Parse FIA product information from markdown content
- **Input:** markdown_content, product_name
- **Output:** Structured FIAProduct model with all features, rates, and terms
- **Extraction:** Cap rates, participation rates, surrender charges, index options, riders

### 3. analyze_product_fit
- **Purpose:** Analyze FIA product suitability for a client
- **Input:** FIAProduct model, ClientProfile model
- **Output:** SuitabilityScore with scoring, recommendations, and detailed breakdown
- **Framework:** 10 key questions (subset of 40-question framework)

### 4. mcp__fetch__fetch (MCP Tool)
- **Purpose:** Fetch web content from URLs
- **Input:** url, max_length (optional)
- **Output:** Markdown-formatted web content
- **Provider:** MCP Fetch server

## Data Models

### FIAProduct
Complete FIA product model with:
- Basic info (name, term, minimum premium)
- Surrender charges and fees
- Index options and crediting methods
- Current rates (caps, participation rates)
- Riders and benefits
- Company information

### ClientProfile
Client information for suitability analysis:
- Demographics (age, state)
- Financial situation (assets, income, emergency fund)
- Investment objectives (income, protection, tax deferral)
- Risk tolerance
- Liquidity needs
- Time horizon
- Product understanding

### SuitabilityScore
Suitability analysis results with:
- Score calculation (YES / (YES + NO) × 100)
- Question-by-question breakdown
- Good fit factors
- Concerns (not-a-fit factors)
- Recommendations
- Interpretation (Highly Suitable, Suitable, Marginal Fit, Not Suitable)

## Example Usage

### Example 1: Basic Product Analysis

```bash
uv run python -m src.main --product "Allianz Benefit Control"
```

**Output:**
- Product search results
- Product details (if found)
- Basic analysis (no suitability scoring)

### Example 2: Product Analysis with Client Profile

```bash
uv run python -m src.main --product "Allianz Benefit Control" --client-profile examples/sample_client.json
```

**Output:**
- Product search results
- Product details
- Suitability score (e.g., 85.71% - Highly Suitable)
- Good fit factors
- Concerns (if any)
- Specific recommendations

### Example 3: Save Results for Documentation

```bash
uv run python -m src.main --product "Allianz 222" --client-profile examples/sample_client.json --output outputs/analysis_2025_11_13.json
```

**Output:**
- Console output with formatted results
- JSON file saved to outputs/ directory
- Full conversation history included in JSON

## Troubleshooting

### ModuleNotFoundError

**Problem:** Cannot import src modules

**Solution:** Ensure you're in the project root directory and use `-m` flag:
```bash
cd /home/seed537/projects/claude-code-agent/agents/claude-sdk/python/fia-analyzer
uv run python -m src.main --product "Allianz Benefit Control"
```

### API Key Issues

**Problem:** "ANTHROPIC_API_KEY not found in environment"

**Solution:**
1. Verify `.env` file exists in project root
2. Ensure `ANTHROPIC_API_KEY` is set in `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
   ```
3. Do NOT use quotes around the API key value

### Import Errors

**Problem:** "No module named 'anthropic'" or similar

**Solution:** Reinstall dependencies:
```bash
# Make sure virtual environment is active
source .venv/Scripts/activate  # Windows Git Bash

# Reinstall dependencies
uv pip install -r requirements.txt

# Or use uv run (automatic venv activation)
uv run python -m src.main --product "Allianz Benefit Control"
```

### Tool Execution Errors

**Problem:** Tool fails during execution

**Solution:**
1. Run with verbose logging to see detailed error:
   ```bash
   uv run python -m src.main --product "Allianz Benefit Control" --verbose
   ```
2. Test the tool individually (see "Testing Tools Individually" section)
3. Check that input data matches expected format (Pydantic validation)

### Skills Not Working

**Problem:** Custom FIA Analysis skill not found

**Solution:**
1. The agent will work without the custom skill (uses PDF skill only)
2. To add custom skill:
   - Upload skill via Claude Code UI
   - Get skill_id from UI
   - Add to `.env`: `FIA_SKILL_ID=skill_xxxxx`

## Development Status

**Week 1 Complete:**
- ✅ Project structure and virtual environment
- ✅ Data models (FIAProduct, ClientProfile, SuitabilityScore)
- ✅ 3 custom tools (search, extract, analyze)
- ✅ Main agent implementation with skills container
- ✅ CLI entry point with argument parsing
- ✅ Example client profile

**Week 2 In Progress:**
- ✅ Integration testing with Claude API
- ⏳ End-to-end testing with real product searches
- ⏳ Unit tests for all tools
- ⏳ Documentation refinements

**Week 2 Remaining:**
- ⏳ Custom FIA Analysis skill implementation
- ⏳ Production-ready error handling
- ⏳ Performance optimization
- ⏳ Comprehensive testing suite

## Next Steps

1. **Test with real API:** Run analysis with your Anthropic API key
2. **Create custom skill:** Upload FIA Analysis skill to Claude Code
3. **Add unit tests:** Write tests for tools and models
4. **Integrate real data:** Replace mock search with real FIA product database
5. **Build CLI enhancements:** Add more command-line options and output formats

## Biblical Principles Applied

This project follows the 6 Foundational Principles:

1. **TRUTH** - All decisions are observable and explainable
   - Clear logging at every stage
   - Transparent scoring methodology
   - Explicit error messages

2. **HONOR** - User-first design with data sovereignty
   - Client data remains in client control
   - No hidden processing
   - Clear consent for data usage

3. **EXCELLENCE** - Production-grade from inception
   - Proper error handling from start
   - Type safety with Pydantic models
   - Comprehensive input validation

4. **SERVE** - Simple, helpful developer experience
   - Clear CLI interface
   - Helpful error messages
   - Easy setup process

5. **PERSEVERE** - Resilient systems with graceful failure
   - Retry logic for API calls
   - Fallback strategies for missing data
   - N/A handling in suitability scoring

6. **SHARPEN** - Continuous improvement
   - Structured logging for debugging
   - Conversation history tracking
   - Clear metrics and results

## Support

For questions, issues, or contributions, see `PROJECT_STATUS.md` for detailed implementation plan and task assignments.

---

**Last Updated:** November 13, 2025
**Version:** 1.0.0 (Week 1 Complete)
**Maintainer:** seed537
