# Financial Advisory Scenario Library Template

## Purpose
This template is designed to capture business development scenarios from financial and insurance publications, enabling systematic identification of client opportunities through AI-powered analysis.

---

## Scenario Structure

Each scenario should include the following fields:

### Core Identification
- **Scenario ID**: Unique identifier (e.g., FIA-001, DIV-001, TAX-001)
- **Scenario Name**: Descriptive title for quick reference
- **Status**: Active | Under Review | Inactive | Seasonal

### Classification Categories

#### Product Type
- Fixed Indexed Annuities (FIA)
- Variable Annuities
- Life Insurance - Whole Life
- Life Insurance - Universal Life
- Life Insurance - Term
- Equities/Stocks
- Fixed Income/Bonds
- ETFs
- Mutual Funds
- REITs
- Alternatives/Private Equity
- Cash/Money Market
- Multi-Product Strategy
- Comprehensive Planning

#### Scenario Type
- Product Review/Replacement
- Tax Planning
- Estate Planning
- Retirement Income Planning
- Risk Management
- Portfolio Rebalancing
- Regulatory Compliance
- Market Opportunity
- Life Event Planning
- Beneficiary Review
- Cost Reduction
- Diversification

#### Urgency/Timing
- Immediate (0-30 days)
- Near-term (30-90 days)
- Strategic (90-365 days)
- Time-Sensitive Event
- Annual Review Item

#### Client Segment
- High Net Worth (HNW)
- Mass Affluent
- Emerging Wealth
- Pre-Retiree (5 years to retirement)
- New Retiree (0-5 years retired)
- Established Retiree (5+ years)
- Business Owner
- Young Professional
- Legacy Planning Focus

#### Trigger Type
- Market-Driven (Volatility)
- Market-Driven (Interest Rates)
- Market-Driven (Sector Performance)
- Regulatory/Tax Change
- Product-Specific (Surrender Period)
- Product-Specific (Crediting Rate)
- Product-Specific (Fee Changes)
- Life Event (Age Milestone)
- Life Event (Retirement)
- Economic Indicator

#### Complexity Level
- Simple (Quick Review/Conversation)
- Moderate (Analysis Required)
- Complex (Multi-Product Strategy)
- Advanced (Requires Specialist Coordination)

#### Revenue Potential
- High (Direct Product Sale)
- Medium (AUM Growth)
- Low (Planning Fee)
- Retention/Defensive
- Referral Opportunity

### Content Fields

#### Description
Brief overview of the scenario (2-3 sentences)

#### Business Case / Why This Matters
Clear articulation of the value proposition and importance to clients

#### Matching Criteria (Logic/Rules)
Specific, actionable criteria for identifying this scenario in client data. Include:
- Data field requirements
- Threshold values
- Logical operators (AND/OR)
- Conditional statements

Example format:
```
Purchase Date >= 6 years ago AND <= 7.5 years ago
AND Product Type = "FIA"
AND Surrender Schedule shows 0-12 months remaining
```

#### Required Client Data Fields
List of specific data points needed from CRM/database to match this scenario:
- Product Type
- Purchase Date
- Current Value
- Age
- Risk Tolerance
- etc.

#### Typical Actions / Next Steps
Sequential list of recommended actions when this scenario is identified:
1. First action
2. Second action
3. Third action

#### Exclusion Rules
Specific conditions that would disqualify a client from this scenario:
- Do not recommend if [condition]
- Exclude if [condition]
- Skip if [condition]

### Compliance & Requirements

#### State Restrictions
List any state-specific regulations, requirements, or restrictions

#### Accredited Investor Only
Yes | No

#### Minimum Asset Level
Specify minimum if applicable, or "N/A"

### Metadata

#### Source Publication(s)
List the publications where this scenario was identified

#### Date Added
YYYY-MM-DD format

#### Date Updated
YYYY-MM-DD format (same as Date Added for new scenarios)

---

## Example Scenarios

### Scenario 1: FIA Approaching Surrender End

**Scenario ID**: FIA-001  
**Scenario Name**: FIA Approaching Surrender End  
**Status**: Active

**Classification:**
- **Product Type**: Fixed Indexed Annuities (FIA)
- **Scenario Type**: Product Review/Replacement
- **Urgency/Timing**: Near-term (30-90 days)
- **Client Segment**: Established Retiree (5+ years)
- **Trigger Type**: Product-Specific (Surrender Period)
- **Complexity Level**: Moderate (Analysis Required)
- **Revenue Potential**: High (Direct Product Sale)

**Content:**

**Description**: Client has FIA within 6-12 months of surrender period expiration. Need to review current product performance, crediting rates, and explore potentially better alternatives.

**Business Case / Why This Matters**: FIA products purchased 5-7+ years ago may have lower caps, participation rates, and crediting methods compared to current offerings. Post-surrender period is optimal time for 1035 exchange without penalties.

**Matching Criteria (Logic/Rules)**:
```
Purchase Date >= 6 years ago AND <= 7.5 years ago
AND Product Type = "FIA"
AND Surrender Schedule shows 0-12 months remaining
```

**Required Client Data Fields**:
- Product Type
- Purchase Date
- Surrender Schedule
- Current Value
- Crediting Rate
- Cap Rate
- Participation Rate

**Typical Actions / Next Steps**:
1. Review current FIA performance vs market alternatives
2. Compare crediting rates and caps with current market offerings
3. Run illustration for potential replacement product
4. Schedule comprehensive review meeting with client
5. Coordinate 1035 exchange if appropriate

**Exclusion Rules**:
- Do not recommend replacement if <6 months to surrender end (too soon, wait for optimal timing)
- Do not recommend if client has initiated withdrawals in current contract year
- Exclude if new FIA purchased within last 12 months
- Skip if client has expressed intent to liquidate for income needs

**Compliance & Requirements:**

**State Restrictions**: Check state-specific suitability requirements; Some states require additional documentation for senior replacements (age 65+)

**Accredited Investor Only**: No

**Minimum Asset Level**: N/A

**Metadata:**
- **Source Publication(s)**: Financial Advisor Magazine, ThinkAdvisor
- **Date Added**: 2025-11-05
- **Date Updated**: 2025-11-05

---

### Scenario 2: Concentrated Portfolio Diversification

**Scenario ID**: DIV-001  
**Scenario Name**: Concentrated Portfolio Diversification  
**Status**: Active

**Classification:**
- **Product Type**: Alternatives/Private Equity
- **Scenario Type**: Diversification
- **Urgency/Timing**: Strategic (90-365 days)
- **Client Segment**: High Net Worth (HNW)
- **Trigger Type**: Market-Driven (Sector Performance)
- **Complexity Level**: Complex (Multi-Product Strategy)
- **Revenue Potential**: High (Direct Product Sale)

**Content:**

**Description**: Client portfolio shows concentration risk with >20% allocation in single stock or sector. Alternative investments can provide uncorrelated returns and broader diversification.

**Business Case / Why This Matters**: Concentrated positions create significant idiosyncratic risk. Recent market volatility highlights importance of diversification. Alternatives offer low correlation to traditional equities/bonds and can improve risk-adjusted returns.

**Matching Criteria (Logic/Rules)**:
```
(Single holding position >20% of portfolio 
OR Sector concentration >30% 
OR Portfolio beta >1.2 with high sector correlation)
AND Client Segment = "High Net Worth"
AND Liquidity needs < 40% of portfolio
```

**Required Client Data Fields**:
- Current Holdings
- Position Sizes
- Sectors
- Portfolio Value
- Risk Tolerance
- Liquidity Needs
- Investment Time Horizon
- Accredited Investor Status

**Typical Actions / Next Steps**:
1. Quantify concentration risk using portfolio analytics
2. Discuss risk tolerance and diversification goals with client
3. Present alternative investment options (private equity, private credit, real assets)
4. Create phased allocation strategy with timeline
5. Execute implementation with regular monitoring checkpoints

**Exclusion Rules**:
- Exclude if client explicitly wants concentrated position (e.g., business owner loyalty, conviction holding)
- Skip if client has <3 year time horizon for invested capital
- Exclude recent retirees who need significant liquidity (>40% of portfolio)
- Do not recommend if client is not accredited investor
- Skip if client has expressed preference for liquid-only investments

**Compliance & Requirements:**

**State Restrictions**: Some alternative products have state-specific registration requirements

**Accredited Investor Only**: Yes - Most alternatives require accredited investor status ($200k income or $1M net worth excluding primary residence)

**Minimum Asset Level**: $250,000 liquid net worth outside of primary residence

**Metadata:**
- **Source Publication(s)**: Barron's, WealthManagement.com
- **Date Added**: 2025-11-05
- **Date Updated**: 2025-11-05

---

### Scenario 3: Year-End Tax Loss Harvesting

**Scenario ID**: TAX-001  
**Scenario Name**: Year-End Tax Loss Harvesting  
**Status**: Seasonal

**Classification:**
- **Product Type**: Equities/Stocks
- **Scenario Type**: Tax Planning
- **Urgency/Timing**: Time-Sensitive Event
- **Client Segment**: Mass Affluent
- **Trigger Type**: Regulatory/Tax Change
- **Complexity Level**: Simple (Quick Review/Conversation)
- **Revenue Potential**: Low (Planning Fee)

**Content:**

**Description**: October-December opportunity to harvest losses in taxable accounts to offset capital gains and reduce tax liability. Must be completed by December 31st.

**Business Case / Why This Matters**: Tax loss harvesting can save clients thousands in taxes by offsetting gains. Proactive approach demonstrates value of active management. Time-sensitive opportunity that expires at year-end and cannot be recovered.

**Matching Criteria (Logic/Rules)**:
```
Account Type = "Taxable"
AND (Unrealized losses exist OR YTD realized gains > $0)
AND Current date between October 1 - December 15
AND Client tax bracket > 0% capital gains rate
```

**Required Client Data Fields**:
- Account Type (taxable vs. tax-deferred)
- Current Positions
- Cost Basis
- Unrealized Gains/Losses
- YTD Realized Gains
- Client Tax Bracket
- Recent Transaction History (for wash sale check)

**Typical Actions / Next Steps**:
1. Run cost basis report for all taxable accounts
2. Identify positions with unrealized losses
3. Review wash sale rule compliance (no repurchase within 30 days)
4. Execute loss harvesting trades before December 31st
5. Document for tax reporting and provide to CPA

**Exclusion Rules**:
- Do not harvest if would trigger wash sale violation (purchased same security within 30 days)
- Skip if client is in 0% capital gains bracket (no tax benefit)
- Exclude qualified retirement accounts (no tax benefit to harvesting)
- Do not recommend if client plans to sell/liquidate account in near term anyway

**Compliance & Requirements:**

**State Restrictions**: N/A - Federal tax strategy

**Accredited Investor Only**: No

**Minimum Asset Level**: N/A

**Metadata:**
- **Source Publication(s)**: Kiplinger's, Financial Advisor Magazine
- **Date Added**: 2025-11-05
- **Date Updated**: 2025-11-05

---

## Usage Instructions

### For Building Scenario Library:
1. Review target publications for opportunities
2. Extract relevant scenarios using this template
3. Assign unique Scenario ID following naming convention (PRODUCT-###)
4. Complete all classification categories
5. Write clear, actionable matching criteria
6. Document all exclusion rules
7. Note source publications for reference

### For AI-Powered Client Matching:
1. Load scenario library into analysis system
2. Connect to client database/CRM
3. For each scenario, apply matching criteria to client data
4. Filter out excluded clients based on exclusion rules
5. Generate prioritized opportunity list
6. Include context and reasoning for each match

### Maintenance:
- Review quarterly for relevance
- Update "Date Updated" when modified
- Mark as "Inactive" if no longer applicable
- Set "Seasonal" status for time-bound opportunities
- Archive outdated scenarios rather than deleting

---

## Scenario Naming Convention

**Format**: [PRODUCT_CODE]-[NUMBER]

**Product Codes**:
- FIA = Fixed Indexed Annuities
- VA = Variable Annuities
- LIFE = Life Insurance
- EQ = Equities
- FI = Fixed Income
- ALT = Alternatives
- DIV = Diversification
- TAX = Tax Planning
- EST = Estate Planning
- RET = Retirement Planning
- RISK = Risk Management
- PLAN = Comprehensive Planning

**Examples**:
- FIA-001, FIA-002, FIA-003
- DIV-001, DIV-002
- TAX-001, TAX-002

---

## Notes

- This template is designed for both human review and AI processing
- Matching criteria should be written in clear, logical expressions
- Exclusion rules are critical for compliance and suitability
- Source attribution helps with credibility and follow-up research
- Regular updates ensure scenarios remain current and relevant
