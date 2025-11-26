# Financial Advisor Agent - Annuity Allocation Specialist

A production-ready AI agent built with Claude Agent SDK that specializes in annuity allocation analysis and retirement income planning.

## Overview

This agent assists financial advisors and individuals with annuity investment decisions by following the standard financial advisor consultation workflow:

1. **Discovery** - Gather client information
2. **Assessment** - Analyze current financial situation
3. **Analysis** - Evaluate annuity options
4. **Recommendation** - Present allocation strategy
5. **Documentation** - Generate summary reports

## Features

### Core Capabilities
- ✅ Annuity suitability assessment with scoring algorithm
- ✅ Payout calculations for different annuity types
- ✅ Product comparison (fixed, variable, indexed)
- ✅ Portfolio allocation optimization
- ✅ Tax implication analysis
- ✅ Specialized subagents for deep analysis

### Annuity Types Supported
- **Fixed Annuities** - Guaranteed returns
- **Variable Annuities** - Market-linked growth
- **Indexed Annuities** - Market participation with protection
- **Immediate Annuities** - Income starts immediately
- **Deferred Annuities** - Future income planning

### Analysis Tools
1. **Suitability Analysis** - Comprehensive client fit assessment
2. **Payout Calculator** - Projected income streams
3. **Type Comparison** - Objective product comparison
4. **Portfolio Optimizer** - Allocation recommendations
5. **Tax Analyzer** - Tax-deferred growth analysis
6. **Rate Fetcher** - Current market rates

## Quick Start

### Prerequisites
- Node.js 18+ or Bun
- Anthropic API key
- TypeScript knowledge (for development)

### Installation

```bash
# Clone or download the project
cd financial-advisor-agent

# Install dependencies
npm install

# Set your API key
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

### Basic Usage

```bash
# Run with default consultation prompt
npm run advisor

# Run with specific query
npm run advisor "Analyze annuity suitability for a 65-year-old retiree"

# Show available examples
npm run advisor --help

# List sample clients
npm run advisor --clients
```

## Example Queries

### Suitability Assessment
```bash
npm run advisor "Assess whether an annuity is suitable for Sarah Johnson"
```

### Payout Calculations
```bash
npm run advisor "Calculate monthly payout for $200,000 immediate annuity for 70-year-old"
```

### Product Comparison
```bash
npm run advisor "Compare fixed vs indexed annuities for moderate risk investor"
```

### Portfolio Analysis
```bash
npm run advisor "Review portfolio allocation for 65-year-old with $500k savings and conservative risk tolerance"
```

### Tax Analysis
```bash
npm run advisor "Evaluate tax implications of $150,000 deferred annuity investment"
```

## Sample Clients

The agent includes 5 sample client profiles for testing:

1. **Sarah Johnson** - Age 62, conservative, $750k savings
2. **Michael Chen** - Age 58, moderate, $1.2M savings
3. **Linda Martinez** - Age 70, conservative, $450k savings
4. **David Thompson** - Age 55, aggressive, $900k savings
5. **Emily Rodriguez** - Age 67, moderate, $580k savings

Access them by name or using "sample-1", "sample-2", etc.

## Architecture

### Project Structure
```
financial-advisor-agent/
├── src/
│   ├── index.ts              # Main agent entry point
│   ├── types/                # TypeScript type definitions
│   ├── tools/                # Annuity analysis tools
│   └── data/                 # Mock client and product data
├── .claude/
│   ├── agents/               # Subagent definitions
│   └── CLAUDE.md             # Detailed project documentation
├── package.json
└── tsconfig.json
```

### Technology Stack
- **Claude Agent SDK** - Agent orchestration
- **TypeScript** - Type safety and async workflows
- **Zod** - Runtime validation
- **Node.js/Bun** - Runtime environment

### Specialized Subagents
- **annuity-analyzer** (Sonnet) - Deep product analysis
- **risk-assessor** (Haiku) - Portfolio and tax optimization

## Development

### Build
```bash
npm run build
```

### Development Mode
```bash
npm run dev
```

### Type Checking
```bash
tsc --noEmit
```

## API Integration (Future)

The current implementation uses mock data but is designed for easy integration with real APIs:

- **Annuity Rates**: Blueprint Income, CANNEX
- **Market Data**: Alpha Vantage, Yahoo Finance
- **Tax Calculations**: TaxJar, tax APIs
- **CRM**: Salesforce, HubSpot integration points

All API hooks are pre-configured in `src/tools/annuity-tools.ts`.

## Compliance and Best Practices

### Suitability Standards
- Comprehensive scoring algorithm (0-100)
- Age-appropriate recommendations
- Risk tolerance alignment
- Over-allocation warnings

### Fiduciary Principles
- Client best interest prioritized
- Transparent fee disclosure
- Balanced pros/cons presentation
- Clear limitation explanations

### Regulatory Considerations
- SEC/FINRA compliance framework
- Documentation of reasoning
- Surrender charge disclosure
- Tax implication analysis

## Limitations

### Current Version (v1.0.0)
- Uses mock data for testing
- Simplified payout calculations
- Basic tax analysis (not state-specific)
- No real-time market data integration

### Before Production Use
1. Integrate real API data sources
2. Add comprehensive testing suite
3. Implement audit logging
4. Add compliance approval workflows
5. Obtain legal review

## Contributing

When adding new features:
1. Follow existing code structure
2. Add Zod schemas for validation
3. Include TypeScript types
4. Update documentation
5. Test with sample clients

## Troubleshooting

### API Key Issues
```bash
# Set the environment variable
export ANTHROPIC_API_KEY="sk-ant-..."

# Or create a .env file
echo 'ANTHROPIC_API_KEY=sk-ant-...' > .env
```

### Module Not Found
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### TypeScript Errors
```bash
# Check compilation
npm run build

# Verify tsconfig.json is present
```

## Documentation

For detailed documentation, see:
- `.claude/CLAUDE.md` - Complete project documentation
- `.claude/agents/` - Subagent specifications
- `src/types/index.ts` - Type definitions

## License

ISC

## Version

1.0.0 - Initial release (January 2025)

## Support

For issues or questions:
1. Review the documentation in `.claude/CLAUDE.md`
2. Check example queries with `npm run advisor --help`
3. Review sample clients with `npm run advisor --clients`

---

**Note**: This is a financial analysis tool for educational and advisory purposes. All recommendations should be reviewed by qualified financial professionals before implementation. Past performance does not guarantee future results.
