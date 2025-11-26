# Financial Advisor Agent - Annuity Allocation Specialist

## Project Overview

This is a production-ready financial advisor agent built with the Claude Agent SDK (TypeScript), specialized in annuity allocation analysis and retirement income planning. The agent follows the typical financial advisor workflow for client consultations.

## Directory Structure

```
financial-advisor-agent/
├── .claude/
│   ├── agents/
│   │   ├── annuity-analyzer.md       # Subagent for product analysis
│   │   └── risk-assessor.md          # Subagent for portfolio/tax analysis
│   └── CLAUDE.md                      # This file - project documentation
├── src/
│   ├── index.ts                       # Main agent entry point
│   ├── types/
│   │   └── index.ts                   # TypeScript types and Zod schemas
│   ├── tools/
│   │   └── annuity-tools.ts           # 6 core annuity analysis tools
│   └── data/
│       └── mock-portfolios.ts         # Sample client data and products
├── package.json                       # Dependencies and scripts
├── tsconfig.json                      # TypeScript configuration
└── .env.example                       # Environment variable template
```

## Key Components

### 1. Main Agent (src/index.ts)
The primary financial advisor agent that orchestrates consultations following the standard workflow:
1. **Discovery** - Gather client information
2. **Assessment** - Analyze current situation
3. **Analysis** - Evaluate annuity options
4. **Recommendation** - Present allocation strategy
5. **Documentation** - Generate summary report

### 2. Annuity Tools (src/tools/annuity-tools.ts)
Six specialized tools for annuity analysis:
- `analyze_annuity_suitability` - Assess fit for client profile (scoring algorithm)
- `calculate_annuity_payout` - Project income streams and payouts
- `compare_annuity_types` - Compare fixed, variable, and indexed options
- `assess_portfolio_allocation` - Recommend optimal annuity percentage
- `evaluate_tax_implications` - Analyze tax-deferred growth and RMD impacts
- `fetch_annuity_rates` - Get current market rates (mock with API hooks)

### 3. Subagents
- **annuity-analyzer** (Sonnet) - Deep product analysis, payout calculations
- **risk-assessor** (Haiku) - Portfolio allocation, tax optimization

### 4. Type System (src/types/index.ts)
Comprehensive TypeScript types with Zod validation:
- ClientProfile, AnnuityProduct, MarketRates
- SuitabilityResult, PayoutCalculation, TaxAnalysis
- PortfolioAllocation, AnnuityComparison

### 5. Mock Data (src/data/mock-portfolios.ts)
- 5 sample client profiles (varying ages, risk levels, goals)
- 5 annuity products (fixed, variable, indexed, immediate, deferred)
- Current market rates (2025 estimates)
- Sample portfolio allocations

## Running the Agent

### Setup
```bash
# Install dependencies
npm install

# Set API key (required)
export ANTHROPIC_API_KEY="your-key-here"
```

### Usage
```bash
# Run with default prompt
npm run advisor

# Run with custom prompt
npm run advisor "Analyze annuity suitability for Sarah Johnson"

# Show help
npm run advisor --help

# List sample clients
npm run advisor --clients
```

### Example Queries
1. "Analyze annuity suitability for a 65-year-old retiree with $750k savings"
2. "Compare fixed vs indexed annuities for moderate risk investor"
3. "Calculate payout for $200k immediate annuity for 70-year-old"
4. "Review portfolio allocation for Emily Rodriguez"
5. "Evaluate tax implications of $150k deferred annuity investment"

## Architecture Decisions

### Why TypeScript?
- Better type safety for financial calculations
- Excellent async support for agent workflows
- Rich ecosystem for web integration (future)

### Why Claude Agent SDK?
- Production-grade agent framework
- Built-in context management
- Subagent support for specialization
- MCP tool integration
- Session management

### Tool Design Philosophy
- **Single responsibility** - Each tool does one thing well
- **Comprehensive output** - Return structured JSON with all relevant data
- **Validation** - Zod schemas ensure data integrity
- **Mock with hooks** - Ready for real API integration

### Data Strategy
- **Phase 1** (Current): Mock data for development/testing
- **Phase 2** (Future): Real API integration via fetch_annuity_rates hooks
- **Hybrid approach**: Mock data with clear API integration points

## Financial Advisor Workflow Implementation

The agent implements the standard financial advisor consultation flow:

### 1. Discovery Phase
- Gathers client demographics (age, savings, income, expenses)
- Assesses risk tolerance and investment objectives
- Reviews existing portfolio and annuity holdings
- Identifies specific income needs and retirement timeline

### 2. Assessment Phase
- Runs suitability analysis with scoring algorithm
- Evaluates income gap (expenses vs income)
- Checks existing annuity exposure
- Assesses appropriateness for client life stage

### 3. Analysis Phase
- Calculates projected payouts for relevant options
- Compares annuity types (fixed, variable, indexed)
- Analyzes portfolio allocation recommendations
- Evaluates tax implications (qualified vs non-qualified)

### 4. Recommendation Phase
- Presents recommended annuity type with reasoning
- Suggests appropriate allocation percentage
- Highlights pros, cons, and potential warnings
- Discusses alternative approaches if applicable

### 5. Documentation Phase
- Summarizes key findings
- Documents rationale for compliance
- Provides specific action steps
- Sets expectations for implementation

## Compliance and Best Practices

### Suitability Standards
- Comprehensive scoring algorithm (0-100 scale)
- Age-appropriate recommendations
- Risk tolerance alignment
- Income need assessment
- Over-allocation warnings (>40% triggers alert)

### Fiduciary Principles
- Client best interest always prioritized
- Transparent fee disclosure
- Clear explanation of limitations
- Objective product comparisons
- Balanced pros/cons presentation

### Regulatory Considerations
- SEC/FINRA suitability compliance
- Clear documentation of reasoning
- Warning about liquidity constraints
- Disclosure of surrender charges
- Tax implication analysis

## Testing

### Sample Clients
1. **Sarah Johnson** (62, conservative, $750k)
   - Nearing retirement, needs income security
   - Test: Fixed or immediate annuity suitability

2. **Michael Chen** (58, moderate, $1.2M)
   - Mid-career, tax optimization focus
   - Test: Variable or indexed with tax analysis

3. **Linda Martinez** (70, conservative, $450k)
   - Already retired, has income gap
   - Test: Immediate annuity for income needs

4. **David Thompson** (55, aggressive, $900k)
   - Younger, growth-focused
   - Test: Variable annuity with growth potential

5. **Emily Rodriguez** (67, moderate, $580k)
   - Recently retired, balanced approach
   - Test: Indexed annuity for balance

### Test Scenarios
```bash
# Suitability assessment
npm run advisor "Analyze suitability for Sarah Johnson"

# Payout calculation
npm run advisor "Calculate $200k immediate annuity payout for 70-year-old"

# Portfolio analysis
npm run advisor "Assess portfolio for Michael Chen"

# Tax analysis
npm run advisor "Evaluate tax implications for $150k deferred annuity"

# Product comparison
npm run advisor "Compare annuity types for moderate risk investor"
```

## Future Enhancements

### Phase 2: Real API Integration
- Connect to live annuity rate APIs (Blueprint Income, CANNEX)
- Integrate market data APIs (Alpha Vantage, Yahoo Finance)
- Add tax calculation APIs (TaxJar)
- Implement CRM integration for client data

### Phase 3: Advanced Features
- Multi-year projection modeling
- Monte Carlo simulations for variable annuities
- Social Security optimization integration
- Estate planning considerations
- Long-term care rider analysis

### Phase 4: Web Interface
- React-based web UI
- Interactive visualizations
- PDF report generation
- Client portal access

## Key Dependencies

- `@anthropic-ai/claude-agent-sdk@^0.1.37` - Agent framework
- `zod@^3.22.4` - Runtime type validation
- `dotenv@^16.4.5` - Environment configuration
- `typescript@^5.3.3` - Type safety
- `tsx@^4.7.0` - TypeScript execution

## Development Workflow

### Adding New Tools
1. Define function in `src/tools/annuity-tools.ts`
2. Add Zod schema for validation
3. Implement calculation logic
4. Add to `annuityToolsServer` tools array
5. Update agent `allowedTools` in `src/index.ts`

### Adding New Subagents
1. Create definition file in `.claude/agents/`
2. Specify description, prompt, tools, model
3. Add to `agents` config in `src/index.ts`

### Modifying Mock Data
- Edit `src/data/mock-portfolios.ts`
- Add new client profiles or products
- Update market rates as needed

## Important Notes

### Financial Calculations
- All calculations use conservative assumptions
- Payout rates based on industry averages (2025)
- Life expectancy: Age 85 baseline
- Inflation rate: 2.8% (current estimate)

### Limitations (Current Version)
- Mock data only (no real API connections)
- Simplified payout calculations
- Basic tax analysis (not state-specific)
- No personalized health underwriting

### Production Deployment
Before production use:
1. Integrate real API data sources
2. Add comprehensive testing suite
3. Implement audit logging
4. Add compliance checks and approvals
5. Legal review of recommendations

## Support and Troubleshooting

### Common Issues

**"ANTHROPIC_API_KEY not set"**
- Set environment variable: `export ANTHROPIC_API_KEY="your-key"`

**"Module not found"**
- Run `npm install` to install dependencies

**"TypeScript errors"**
- Run `npm run build` to check compilation
- Ensure `tsconfig.json` is properly configured

### Getting Help
- Review example queries: `npm run advisor --help`
- Check sample clients: `npm run advisor --clients`
- Review agent subagents in `.claude/agents/`

## Last Updated
January 2025

## Version
1.0.0 - Initial production-ready implementation focused on annuity allocation workflow
