# Scenario-Based Client Opportunity System
## Implementation Guide

### Overview
This system enables you to systematically identify revenue opportunities and improve client outcomes by:
1. Extracting scenarios from industry publications
2. Building a searchable scenario library
3. Matching scenarios to clients in your book of business
4. Generating actionable recommendations with context

---

## What You Received

### 1. Excel Template (scenario_template.xlsx)
**Three Worksheets:**

#### Sheet 1: Scenario Library (Main Working Sheet)
- 22 structured columns for comprehensive scenario documentation
- Color-coded headers for easy navigation
- Frozen header row for scrolling
- Ready for data entry

**Key Columns:**
- **Core ID**: Scenario ID, Name, Status
- **Classifications**: Product Type, Scenario Type, Urgency, Client Segment, Trigger Type, Complexity, Revenue Potential
- **Content**: Description, Business Case, Matching Criteria, Required Data, Next Steps
- **Compliance**: Exclusion Rules, State Restrictions, Accredited Investor flag, Minimum Assets
- **Metadata**: Source Publications, Dates

#### Sheet 2: Classification Reference (Dropdown Guide)
Pre-populated options for each classification category:
- 14 Product Types
- 12 Scenario Types
- 5 Urgency/Timing options
- 9 Client Segments
- 10 Trigger Types
- 4 Complexity Levels
- 5 Revenue Potential categories
- 4 Status options

Use this as your controlled vocabulary to maintain consistency.

#### Sheet 3: Example Scenarios (Learning Template)
Three fully-completed example scenarios:
1. **FIA-001**: FIA Approaching Surrender End
2. **DIV-001**: Concentrated Portfolio Diversification
3. **TAX-001**: Year-End Tax Loss Harvesting

These demonstrate proper completion and varying complexity levels.

### 2. Markdown Template (scenario_template.md)
- LLM-optimized format for AI processing
- Identical structure to Excel version
- Includes all classification categories
- Contains same three example scenarios
- Easy to version control and collaborate on

---

## How to Use This System

### Phase 1: Build Initial Scenario Library (30-40 Scenarios)

#### Step 1: Source Review (This Week)
- Review publications from your attached list
- Look for articles discussing:
  - Product innovations or changes
  - Market trends affecting client portfolios
  - Regulatory/tax changes
  - Industry best practices
  - Client advisory opportunities

#### Step 2: Scenario Extraction (Next 2-3 Weeks)
For each opportunity identified:
1. Open Excel template
2. Create new row in "Scenario Library" sheet
3. Assign Scenario ID using naming convention (e.g., FIA-004)
4. Complete all 22 columns
5. Reference "Classification Reference" sheet for dropdown options
6. Use "Example Scenarios" sheet as guide

**Critical Fields to Nail:**
- **Matching Criteria**: Must be precise, logical, actionable
  - Example: "Age >= 59.5 AND Account Type = 'IRA' AND Balance > $100,000"
- **Exclusion Rules**: Prevents false positives and compliance issues
  - Example: "Exclude if RMD already started; Exclude CA residents"
- **Required Data Fields**: Ensures you can actually run the match
  - Example: "Age, Account Type, Balance, State of Residence"

#### Step 3: Scenario Refinement
After building 10-15 scenarios, review for:
- **Consistency**: Are classifications used consistently?
- **Completeness**: Are all required fields populated?
- **Clarity**: Can someone else understand the matching criteria?
- **Feasibility**: Do you have the required client data?

### Phase 2: Connect to Client Data

#### Data Requirements
Your CRM/spreadsheet should include:
- **Demographics**: Age, state, employment status, net worth
- **Products**: Type, purchase date, value, surrender schedule, crediting rates
- **Accounts**: Type (IRA, Roth, taxable, etc.), balances, holdings
- **Portfolio**: Asset allocation, positions, cost basis, sector exposure
- **Planning**: Risk tolerance, time horizon, goals, liquidity needs

#### Data Preparation
1. Export CRM data to Google Sheets
2. Ensure clean, consistent column names
3. Validate data completeness
4. Add any calculated fields (e.g., "Days to Surrender End")

### Phase 3: Run Scenario Matching (AI-Powered)

#### The Matching Process
For each scenario:
1. AI reads the "Matching Criteria" logic
2. Applies criteria to each client record
3. Filters out excluded clients per "Exclusion Rules"
4. Generates prioritized list of matches

#### Expected Output Format
```
Client: John Smith (ID: 12345)
Scenario: FIA-001 - FIA Approaching Surrender End
Match Confidence: High

Reasoning:
- Has FIA purchased 6.5 years ago (Allianz 222, purchased 4/15/2019)
- Current value: $487,000
- Surrender period ends: 10/15/2025 (5 months away)
- Current cap rate: 4.5% vs market average 6.2%
- No withdrawals taken this year

Why This Matters:
- Client's product significantly underperforming current market offerings
- Optimal window for 1035 exchange without penalties
- Potential for 38% higher crediting rate with newer product

Recommended Actions:
1. Schedule review meeting in next 2 weeks
2. Run side-by-side illustration (current vs. replacement)
3. Review surrender schedule details
4. Discuss client's income needs timeline
5. Prepare 1035 paperwork if client approves

Next Steps Timeline: 30-60 days
Revenue Potential: $4,870 (est. commission on $487k)
```

### Phase 4: Continuous Improvement

#### Monthly Maintenance
- Add 3-5 new scenarios from recent publications
- Update existing scenarios if market conditions change
- Mark seasonal scenarios as Active/Inactive based on calendar
- Review and refine matching criteria based on results

#### Quarterly Review
- Analyze which scenarios generated most opportunities
- Identify gaps in scenario coverage
- Update classification categories if needed
- Archive obsolete scenarios

---

## Scenario Naming Convention

### Format: [CODE]-[NUMBER]

### Product/Category Codes:
- **FIA** = Fixed Indexed Annuities
- **VA** = Variable Annuities  
- **LIFE** = Life Insurance
- **EQ** = Equities
- **FI** = Fixed Income
- **ETF** = Exchange Traded Funds
- **MF** = Mutual Funds
- **REIT** = Real Estate Investment Trusts
- **ALT** = Alternatives/Private Equity
- **DIV** = Diversification Strategies
- **TAX** = Tax Planning
- **EST** = Estate Planning
- **RET** = Retirement Planning
- **RISK** = Risk Management
- **INCOME** = Income Planning
- **PLAN** = Comprehensive Planning
- **COST** = Cost Reduction
- **REG** = Regulatory/Compliance

### Examples:
- FIA-001, FIA-002, FIA-003 (FIA scenarios)
- TAX-001, TAX-002 (Tax planning scenarios)
- DIV-001, DIV-002 (Diversification scenarios)

---

## Best Practices

### Writing Matching Criteria
✅ **Good - Specific and Actionable:**
```
Age >= 59.5 AND Age < 73
AND Account Type = "Traditional IRA"  
AND Account Balance > $100,000
AND NOT taking RMDs yet
```

❌ **Bad - Vague and Unusable:**
```
Older clients with retirement accounts who might benefit from Roth conversions
```

### Writing Exclusion Rules
✅ **Good - Clear and Enforceable:**
```
- Exclude if RMDs already started (Age 73+ and taking distributions)
- Exclude if California resident (state tax considerations)
- Exclude if income < $100k (insufficient tax bracket benefit)
- Exclude if completed Roth conversion in last 12 months
```

❌ **Bad - Ambiguous:**
```
- Don't recommend if not appropriate
- Skip if client won't benefit
```

### Source Attribution
✅ **Good:**
```
Source: ThinkAdvisor, "New FIA Products Offer 6%+ Caps", Oct 15, 2025
Source: Financial Advisor Magazine, "Roth Conversion Strategies", Sep 2025
```

❌ **Bad:**
```
Source: Various articles
Source: Industry research
```

---

## Advanced Features to Consider

### Scenario Chaining
Some scenarios naturally lead to others:
- FIA replacement → Income planning review
- Concentrated position → Tax loss harvesting → Roth conversion

Consider adding a "Related Scenarios" field to create workflow chains.

### Priority Scoring
Add weighted scoring to prioritize opportunities:
- Revenue Potential (40%)
- Client Impact (30%)
- Urgency (20%)
- Ease of Implementation (10%)

### Client Tagging
Tag clients who match multiple scenarios:
- "High Priority - 3 Opportunities"
- "Tax Planning Focus"
- "Product Review Needed"

### Workflow Integration
Connect to CRM tasks:
- Auto-create task when match identified
- Set follow-up reminders
- Track conversion rates by scenario type

---

## Next Steps

### Immediate (This Week):
1. ✅ Review both template files
2. ✅ Understand the structure and classifications
3. ✅ Study the three example scenarios
4. ⬜ Identify 5-10 recent articles from your publication list
5. ⬜ Practice extracting 2-3 scenarios manually

### Short-Term (Next 2 Weeks):
1. ⬜ Build first 15-20 scenarios from publications
2. ⬜ Refine matching criteria with test data
3. ⬜ Validate you have required client data fields
4. ⬜ Start building comprehensive scenario library

### Medium-Term (Next Month):
1. ⬜ Complete 30-40 scenario library
2. ⬜ Connect to client database (Google Sheets)
3. ⬜ Run initial AI matching test on 10 sample clients
4. ⬜ Refine criteria based on false positives/negatives

### Long-Term (Ongoing):
1. ⬜ Build Skills for automated scenario extraction
2. ⬜ Build Skills for automated client matching
3. ⬜ Create recurring workflow for monthly opportunity reports
4. ⬜ Integrate with CRM for seamless execution

---

## Questions to Answer Before Building Skills

As you work through the initial 30-40 scenarios, document:

1. **Data Availability**: Which client data fields are missing? Do you need to add fields to your CRM?

2. **Matching Logic Patterns**: Are there common patterns in matching criteria that could be templated?

3. **Priority Rules**: How should opportunities be prioritized when a client matches multiple scenarios?

4. **Output Preferences**: What format works best for your review process? (Email digest, dashboard, task list?)

5. **Frequency**: How often should matching run? (Daily, weekly, monthly, on-demand?)

6. **False Positive Rate**: Which scenarios are producing too many low-quality matches?

7. **Integration Points**: Where should results flow? (CRM tasks, email, spreadsheet, dashboard?)

---

## Skill Development Roadmap

Once scenario library is mature (30-40 scenarios), we'll build:

### Skill 1: Scenario Extractor
- Monitors specified publications
- Extracts new opportunities automatically
- Adds to scenario library with suggested classifications
- Flags for human review and refinement

### Skill 2: Client Opportunity Matcher
- Reads scenario library
- Applies matching criteria to client database
- Generates prioritized opportunity list
- Provides reasoning and context for each match

### Skill 3: Opportunity Report Generator
- Creates formatted reports by client or scenario type
- Includes action plans and timeline
- Estimates revenue potential
- Tracks opportunities over time

### Skill 4: Publication Monitor (Ongoing)
- Daily/weekly scans of publication list
- Identifies relevant new articles
- Suggests scenario updates or new scenarios
- Keeps library current with market changes

---

## Success Metrics

Track to measure effectiveness:

### Scenario Quality
- % of scenarios generating matches (target: >60%)
- Average matches per scenario (target: 5-15)
- False positive rate (target: <20%)

### Business Impact  
- Opportunities identified per month
- Conversion rate (opportunities → meetings)
- Revenue generated from scenario-driven opportunities
- Client satisfaction with proactive service

### Efficiency Gains
- Time saved on manual book reviews
- Earlier identification of time-sensitive opportunities
- Reduction in missed opportunities

---

## Support Resources

### For Scenario Building:
- Use "Example Scenarios" sheet as template
- Reference "Classification Reference" for consistency
- Review publication list in your uploaded file

### For Questions:
- Share specific scenarios for feedback
- Ask about matching criteria logic
- Discuss data availability challenges
- Brainstorm new classification categories

### For Next Phases:
- We'll refine the approach based on your first 10-15 scenarios
- Skills will be built once templates are proven
- Continuous iteration based on real-world results

---

## Remember

This is a **systematic approach** to something you likely already do intuitively. The goal is to:
- Make it **scalable** (cover all clients, not just who comes to mind)
- Make it **consistent** (every opportunity captured)
- Make it **proactive** (ahead of client questions)
- Make it **efficient** (AI does the matching, you do the advising)

Start small, iterate, refine, and scale!
