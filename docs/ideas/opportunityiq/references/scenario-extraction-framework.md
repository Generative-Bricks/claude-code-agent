# Scenario Extraction Framework

## Purpose
This document provides the detailed methodology for extracting structured revenue scenarios from financial advisor publications and articles.

---

## The 6 Key Questions for Extraction

### Question 1: What's the Opportunity?
**Goal:** Identify the specific action an advisor can take

**What to look for:**
- Concrete action verbs: "review," "upgrade," "reposition," "harvest"
- Not just market commentary but actionable insights
- Clear value proposition for clients

**Examples:**
- ❌ Bad: "Interest rates are rising" (just information)
- ✅ Good: "Review clients with low-yielding cash and reposition to money market funds earning 5%"

**From article to opportunity:**
```
Article says: "Fixed indexed annuities are now offering 6-7% caps, up from 4-5% two years ago"

Opportunity: Review clients with older FIAs and upgrade them to higher-cap products
```

---

### Question 2: Who is This For?
**Goal:** Define the target client segment

**Segmentation dimensions:**
- Demographics (age, net worth, life stage)
- Product holdings (FIA, life insurance, taxable accounts)
- Situations (near retirement, concentrated position, high cash)
- Risk profile (conservative, moderate, aggressive)
- Life events (inheritance, business sale, divorce)

**Examples:**
- Retirees with FIAs purchased 5+ years ago
- HNW clients with concentrated positions (>30% in single stock)
- Pre-retirees (age 55-65) with cash > $100K earning < 3%
- Business owners approaching liquidity event

---

### Question 3: How Do You Identify Them?
**Goal:** Create specific, testable matching criteria

**Requirements:**
- Must be data-driven (can query from database)
- Must be specific enough to reduce false positives
- Must be broad enough to find opportunities
- Should use AND/OR logic clearly

**Format:**
```
Field_Name OPERATOR Value
AND/OR
Field_Name OPERATOR Value
```

**Example matching criteria:**
```
Product_Type = 'FIA'
AND Purchase_Date BETWEEN 5 and 8 years ago
AND Current_Cap_Rate < 5.5%
AND (Surrender_End_Date within 12 months OR Surrender_Charge < 3%)
```

**Common operators:**
- `=` (equals)
- `>`, `<`, `>=`, `<=` (comparisons)
- `BETWEEN X and Y` (ranges)
- `IN [list]` (multiple options)
- `contains` (text search)
- `within X days/months` (date proximity)

---

### Question 4: What's the Revenue?
**Goal:** Quantify the financial opportunity

**Revenue types:**
1. **Product Commission** (one-time)
   - Formula: `Product_Value × Commission_Rate`
   - Example: $500K FIA × 5% = $25,000

2. **AUM Fee** (recurring)
   - Formula: `New_AUM × Annual_Fee_Rate`
   - Example: $200K to managed account × 1% = $2,000/year

3. **Planning Fee** (project-based)
   - Formula: `Flat_Fee` or `Hours × Hourly_Rate`
   - Example: Estate plan = $5,000 flat

**Revenue ranges:**
- High: >$10,000
- Medium: $2,000-$10,000
- Low: $500-$2,000

Always provide:
- The formula
- A concrete example
- The revenue range
- Revenue type (one-time, recurring, project)

---

### Question 5: What are the Exclusions?
**Goal:** Prevent false positives and inappropriate recommendations

**Exclusion categories:**

**Recent actions:**
- Client already completed this action in last 6-12 months
- Already has optimal solution in place

**Circumstances:**
- Surrender charges too high (>7%)
- Major liquidity needs in next 12 months
- Health issues that affect insurability

**Preferences:**
- Client specifically declined this in past
- Conflicting goals or values
- Already reviewed and decided against

**Example exclusions:**
```
Do NOT recommend if:
- Client purchased new FIA within last 12 months
- Surrender charge > 7%
- Client has initiated income withdrawals this year
- Client plans to liquidate for known expense
```

**Why exclusions matter:**
- Reduces false positives
- Prevents advisor embarrassment
- Respects client preferences
- Improves match quality

---

### Question 6: What's the Next Action?
**Goal:** Define the implementation path

**Action components:**
1. **First step**: What does advisor do immediately?
2. **Meeting type**: Call, standard meeting, comprehensive review?
3. **Timeline**: How urgent? How long to implement?
4. **Professional coordination**: Self-sufficient or need CPA/attorney?

**Example action plan:**
```
Typical Actions:
1. Pull current FIA statement and surrender schedule
2. Run illustration: current product vs. new product
3. Calculate income improvement ($X at 4.5% vs. $Y at 6.5%)
4. Schedule 30-minute call to present options
5. If approved, prepare 1035 exchange paperwork
6. Submit to carrier

Timeline: 2-3 weeks from initial call to submission
Meeting: One 30-minute call
Coordination: Self-sufficient (no outside professionals)
```

---

## Scenario Extraction Template

When you extract a scenario, populate all these fields:

### Article Information
```
Source: [Publication name]
Title: [Article title]
Date: [Publication date]
URL: [Link if available]
Key Topic: [Market trend, product, regulation]
```

### Scenario Identity
```
Scenario ID: [CODE-###]
Scenario Name: [Clear, descriptive name]
Category: [FIA, Tax, Diversification, Insurance, Market, etc.]
```

### Business Case
```
Why This Matters:
[2-3 sentences explaining value proposition and urgency]

Example:
"FIA rates have increased 2-3% in the past 24 months. Clients who 
purchased during low-rate environment are earning significantly less 
than current market rates. Post-surrender period is optimal time to 
upgrade without penalties."
```

### Client Identification
```
Matching Criteria:
[Specific, testable criteria using data fields]

Required Data Fields:
- [Field 1]
- [Field 2]
- [Field 3]

Example:
Product_Type = 'FIA'
AND Purchase_Date >= 5 years ago
AND Current_Cap_Rate < 5.5%
AND Surrender_End_Date within 12 months

Required Fields:
- Product Type
- Purchase Date
- Cap Rate
- Surrender End Date
```

### Exclusions
```
Do Not Recommend If:
- [Exclusion 1]
- [Exclusion 2]
- [Exclusion 3]

Example:
- Client purchased new FIA within last 12 months
- Surrender charge > 7%
- Client specifically wants to liquidate
```

### Revenue
```
Revenue Formula:
[Formula with variables defined]

Revenue Calculation:
[Worked example]

Revenue Range: [$X - $Y]
Revenue Type: [High/Medium/Low, One-time/Recurring/Project]

Example:
Formula: Product_Value × 0.05
Calculation: $500,000 × 0.05 = $25,000
Range: $10,000 - $50,000
Type: High, One-time
```

### Classifications
```
Product Type: [FIA, Life, Equities, Bonds, etc.]
Scenario Type: [Product Review, Tax Planning, Diversification, etc.]
Urgency: [Immediate, Near-term, Strategic, Time-sensitive]
Client Segment: [HNW, Mass Affluent, Pre-Retiree, Retiree]
Trigger Type: [Market-driven, Product-specific, Life event, Regulatory]
Complexity: [Simple, Moderate, Complex, Advanced]
```

### Implementation
```
Typical Actions:
1. [Action 1]
2. [Action 2]
3. [Action 3]

Meeting Type: [Quick call / Standard meeting / Comprehensive review]
Timeline: [Immediate / 30-day / 90-day window]
Professional Coordination: [Self-sufficient / CPA needed / Attorney needed]
```

---

## Complete Extraction Examples

### Example 1: Article → Scenario (FIA Replacement)

**Article Excerpt:**
*"ThinkAdvisor - November 2025: With fixed indexed annuity cap rates now at 6.5-7%, advisors have an opportunity to review clients who purchased FIAs 5-7 years ago when caps were 4-5%. Post-surrender period is the ideal time to upgrade without penalties."*

**Extracted Scenario:**

```
---ARTICLE INFO---
Source: ThinkAdvisor
Title: "FIA Rates Surge: Review Older Contracts"
Date: November 2025
Key Topic: FIA rate increases

---SCENARIO IDENTITY---
Scenario ID: FIA-001
Scenario Name: FIA Surrender Period Ending Review
Category: Fixed Indexed Annuity

---BUSINESS CASE---
Why This Matters:
FIA cap rates have increased 2-3% over the past 24 months due to rising 
interest rates. Clients who purchased FIAs during the 2019-2021 low-rate 
environment are earning 4-5% caps while new products offer 6.5-7% caps. 
The post-surrender period is the optimal time to upgrade without penalties, 
potentially increasing client income by $5,000-$15,000 annually on a 
$500K contract.

---CLIENT IDENTIFICATION---
Matching Criteria:
Product_Type = 'FIA'
AND Purchase_Date BETWEEN 5 and 8 years ago
AND Current_Cap_Rate < 5.5%
AND (Surrender_End_Date within 12 months OR Surrender_Charge < 3%)

Required Data Fields:
- Product Type
- Product Value
- Purchase Date
- Current Cap Rate (or Participation Rate)
- Surrender Schedule / End Date
- Current Surrender Charge

---EXCLUSIONS---
Do Not Recommend If:
- Client purchased new FIA within last 12 months
- Surrender charge > 7% (too expensive to move)
- Client has initiated systematic income withdrawals this contract year
- Client plans to liquidate for known expense (house, car, etc.)
- Current FIA has valuable guaranteed living benefit rider that can't be replicated

---REVENUE---
Revenue Formula:
Revenue = Product_Value × Commission_Rate
Commission_Rate = 5% (typical for FIA replacement)

Revenue Calculation:
For $500K FIA: $500,000 × 0.05 = $25,000
For $250K FIA: $250,000 × 0.05 = $12,500
For $100K FIA: $100,000 × 0.05 = $5,000

Revenue Range: $5,000 - $50,000
Revenue Type: High, One-time (product commission)

---CLASSIFICATIONS---
Product Type: Fixed Indexed Annuity
Scenario Type: Product Review / Upgrade
Urgency: Near-term (within surrender period end window)
Client Segment: Retirees, Pre-retirees (typically age 60-75)
Trigger Type: Market-driven (interest rate environment)
Complexity: Moderate (requires illustration, contract review)

---IMPLEMENTATION---
Typical Actions:
1. Pull current FIA statement and surrender schedule
2. Verify current cap rate, participation rate, and fees
3. Run new product illustrations from 2-3 carriers
4. Calculate annual income difference (old cap vs. new cap)
5. Schedule 30-minute call or in-person meeting
6. Present comparison: current contract vs. new options
7. If client approves, prepare 1035 exchange paperwork
8. Submit to new carrier and coordinate with existing carrier

Meeting Type: Standard meeting (30-45 minutes)
Timeline: 30-60 day window (before surrender period ends)
Professional Coordination: Self-sufficient (no outside professionals needed)
```

---

### Example 2: Market Observation → Scenario (Cash Drag)

**Observation:**
*"Seeing lots of discussion on advisor forums about clients sitting on large cash balances earning 0.5% in savings accounts while money market funds are now yielding 5%."*

**Extracted Scenario:**

```
---ARTICLE INFO---
Source: Advisor Forums / Industry Discussion
Title: N/A (market observation)
Date: Q4 2025
Key Topic: Cash yields / money market rates

---SCENARIO IDENTITY---
Scenario ID: MKT-002
Scenario Name: Cash Drag Repositioning
Category: Cash Management / Asset Allocation

---BUSINESS CASE---
Why This Matters:
With money market funds now yielding 4.5-5.5%, conservative clients 
holding excess cash in low-yielding savings accounts (0.1-0.5%) are 
missing significant income. For a retiree with $200K cash, the difference 
is $9,000-$10,000 per year. This is a low-risk, easy conversation that 
improves client outcomes and can transition cash to AUM.

---CLIENT IDENTIFICATION---
Matching Criteria:
Cash_Balance > $50,000
AND Cash_Yield < 3.0%
AND Age >= 55 (retirees/pre-retirees)
AND NOT Major_Purchase_Planned_Next_12_Months

Optional enhancement:
AND Risk_Tolerance IN ['Conservative', 'Moderately Conservative']

Required Data Fields:
- Cash Balance (checking + savings)
- Current Cash Yield (if available)
- Age
- Upcoming major purchases (if tracked)

---EXCLUSIONS---
Do Not Recommend If:
- Cash is designated emergency fund and client wants to keep separate
- Major known expenses in next 12 months (house, car, medical procedure)
- Client already has money market fund or high-yield cash solution
- Client specifically wants FDIC bank account (vs securities)
- Cash is for business operating expenses

---REVENUE---
Revenue Formula:
Revenue = (Cash_Balance × Reposition_Percentage) × Annual_Fee_Rate
Reposition_Percentage = 0.40 to 0.60 (40-60% of cash can typically be moved)
Annual_Fee_Rate = 0.01 (1% AUM fee)

Revenue Calculation:
For $200K cash:
  Reposition = $200K × 0.50 = $100K
  Revenue = $100K × 0.01 = $1,000/year recurring

For $100K cash:
  Reposition = $100K × 0.50 = $50K
  Revenue = $50K × 0.01 = $500/year recurring

Revenue Range: $500 - $3,000/year (recurring)
Revenue Type: Medium, Recurring (AUM)

---CLASSIFICATIONS---
Product Type: Cash Management / Money Market
Scenario Type: Asset Allocation / Income Optimization
Urgency: Strategic (not urgent but timely given rate environment)
Client Segment: Retirees, Pre-retirees, Conservative investors
Trigger Type: Market-driven (interest rate environment)
Complexity: Simple (one phone call)

---IMPLEMENTATION---
Typical Actions:
1. Review total cash holdings across all accounts
2. Discuss liquidity needs: What's true emergency fund? Any upcoming expenses?
3. Calculate safe amount to reposition (typically 40-60% of total cash)
4. Show income comparison: $200K at 0.5% = $1,000 vs. $200K at 5% = $10,000
5. Recommend money market fund or Treasury money market
6. Execute repositioning (can happen same day)

Meeting Type: Quick call (15-20 minutes)
Timeline: Immediate (can execute same day or week)
Professional Coordination: Self-sufficient
```

---

### Example 3: Regulatory Change → Scenario (VA Fee Review)

**News:**
*"SEC proposes new disclosure rules for variable annuities effective Q1 2026, highlighting total annual costs more prominently."*

**Extracted Scenario:**

```
---ARTICLE INFO---
Source: Financial Advisor Magazine
Title: "New SEC Disclosure Rules for Variable Annuities"
Date: December 2025
Key Topic: Regulatory change - fee disclosure

---SCENARIO IDENTITY---
Scenario ID: REG-001
Scenario Name: Variable Annuity Fee Review
Category: Variable Annuity / Regulatory

---BUSINESS CASE---
Why This Matters:
New SEC disclosure rules (effective Q1 2026) will show VA fees more 
prominently in annual statements. Clients with high-fee VAs (>2.5% total 
annual cost) may experience sticker shock. Proactive review demonstrates 
transparency and client-first approach. Provides opportunity to explain 
fees OR reposition to lower-cost alternatives if fees aren't justified 
by benefits.

---CLIENT IDENTIFICATION---
Matching Criteria:
Product_Type = 'Variable Annuity'
AND Total_Annual_Fees > 2.5%
AND Purchase_Date > 5 years ago (outside surrender period)
AND Current_Value > $100,000
AND NOT Recent_VA_Review_In_Last_12_Months

Required Data Fields:
- Product Type
- Total Annual Fees (M&E + admin + subaccount + rider fees)
- Purchase Date
- Current Value
- Surrender Schedule

---EXCLUSIONS---
Do Not Recommend If:
- VA fees are justified by valuable guaranteed living benefit (GLWB) or 
  guaranteed minimum death benefit (GMDB) riders
- Recently purchased VA (< 3 years, still in heavy surrender period)
- Client fully understands and values the features/benefits
- Already a low-fee VA (< 2.0% total)
- Client is actively using guaranteed income rider

---REVENUE---
Revenue Formula:
Option A (Reposition to new VA):
  Revenue = Product_Value × Commission_Rate
  Commission_Rate = 0.04 to 0.05 (4-5%)

Option B (Reposition to managed account):
  Revenue = Product_Value × Annual_Fee_Rate  
  Annual_Fee_Rate = 0.01 (1% AUM)

Revenue Calculation:
For $250K VA:
  Option A (New VA): $250,000 × 0.05 = $12,500 one-time
  Option B (AUM): $250,000 × 0.01 = $2,500/year recurring

Revenue Range: $5,000 - $25,000 (or $1,000-$5,000/year if to AUM)
Revenue Type: High one-time (new product) OR Medium recurring (AUM)

---CLASSIFICATIONS---
Product Type: Variable Annuity
Scenario Type: Product Review / Fee Analysis / Regulatory
Urgency: Near-term (proactive before Q1 2026 disclosure rollout)
Client Segment: Mass Affluent to HNW (VA holders typically $100K+)
Trigger Type: Regulatory (SEC rule change)
Complexity: Moderate (requires fee breakdown, benefit analysis)

---IMPLEMENTATION---
Typical Actions:
1. Pull current VA statement and most recent performance report
2. Break down all-in costs: M&E + admin + subaccount fees + rider costs
3. Assess value of features: Are GLWB/GMDB worth the cost?
4. If high fees / low value: model alternatives (lower-cost VA, ETF portfolio)
5. Schedule proactive meeting: "Let's review this before new disclosures arrive"
6. Present options: (a) stay with explanation, (b) reposition to lower cost
7. If repositioning: check surrender charges, prepare 1035 or liquidation

Meeting Type: Standard meeting (45-60 minutes for thorough review)
Timeline: 30-90 days (proactive, before Q1 2026)
Professional Coordination: Self-sufficient, potentially coordinate with CPA 
                          if tax implications
```

---

## Trigger Phrases in Articles

When scanning publications, look for these trigger phrases:

**Opportunity Indicators:**
- "Advisors should review..."
- "Opportunity for advisors..."
- "Clients with [X] should consider..."
- "Now is the time to..."
- "Advisors can help clients by..."
- "Revenue opportunity from..."
- "Sales opportunity in..."

**Product/Market Triggers:**
- "New [product] launches with..."
- "[Rates/Fees/Features] have changed..."
- "[Product type] now offers..."
- "Clients are being pitched..."
- "Compared to [old version]..."

**Regulatory Triggers:**
- "New rule requires..."
- "Deadline approaching for..."
- "Advisors must now..."
- "Disclosure changes mean..."

**Market Condition Triggers:**
- "With [rates/volatility/market] now at..."
- "Given current [market condition]..."
- "As markets have..."

---

## Publication Sources (Priority Order)

### Tier 1: High-Value for Scenario Discovery

**Financial Advisor Magazine**
- Monthly feature articles
- Focus: Product innovations, advisor strategies
- Expected: 2-3 scenarios per month

**ThinkAdvisor**
- Daily news, weekly deep-dives
- Focus: Market trends, regulatory changes, product analysis
- Expected: 1-2 scenarios per week

**Barron's Advisor**
- Weekly advisor-focused content
- Focus: Investment strategies, market analysis
- Expected: 1 scenario per week

**Best's Review (AM Best)**
- Monthly insurance industry analysis
- Focus: Insurance products, carrier analysis
- Expected: 1-2 scenarios per month (insurance-focused)

### Tier 2: Supplemental Sources

**WealthManagement.com**
- Daily news and analysis
- Focus: RIA industry, technology, practice management

**RIABiz**
- Industry news and trends
- Focus: RIA business model, M&A, technology

**Investment News**
- Weekly publication
- Focus: Advisor industry news, regulatory changes

### Tier 3: Specialized

**Journal of Financial Planning (CFP Board)**
- Technical planning strategies
- Expected: 1-2 scenarios per month (planning-focused)

**NAIC Publications**
- Insurance regulations
- Expected: 0-1 scenario per month (regulatory)

---

## Testing Scenarios Before Activation

Before adding a scenario to your active library, test it:

### Step 1: Dry Run with Sample Data
- Take 5-10 sample clients
- Manually apply matching criteria
- Do the matches make sense?

### Step 2: False Positive Check
- Review each match individually
- Would you actually recommend this?
- Any obvious exclusions you missed?

### Step 3: Revenue Validation
- Are revenue estimates realistic?
- Do formulas work with real numbers?
- Any edge cases that break the calculation?

### Step 4: Actionability Check
- Is there a clear next action?
- Can you implement this within the timeline?
- Do you need any data you don't have?

### Step 5: Refinement
- Adjust criteria to reduce false positives
- Add exclusions discovered in testing
- Update revenue formulas if needed

**Only activate scenarios that pass 80%+ of test matches.**

---

## Scenario Quality Checklist

Before finalizing a scenario extraction, verify:

**Clarity (5 checks):**
- [ ] Can you explain the opportunity in 2 sentences?
- [ ] Is it clear what the advisor should do?
- [ ] Would another advisor understand this without your context?
- [ ] Are all technical terms defined?
- [ ] Is the business case compelling?

**Feasibility (5 checks):**
- [ ] Can you identify matching clients from standard advisor data?
- [ ] Are the criteria specific enough to reduce false positives?
- [ ] Do you have the required data fields?
- [ ] Can the matching criteria be automated?
- [ ] Is the exclusion list comprehensive?

**Actionability (5 checks):**
- [ ] Is there a clear next action for the advisor?
- [ ] Can this lead to revenue (not just goodwill)?
- [ ] Is the timeline reasonable?
- [ ] Can this be executed without rare expertise?
- [ ] Would you actually take this action with your clients?

**Value (5 checks):**
- [ ] Is the revenue potential material (>$500)?
- [ ] Would clients genuinely benefit from this?
- [ ] Does this differentiate the advisor's practice?
- [ ] Is the effort justified by the revenue?
- [ ] Will this likely convert to actual revenue?

**Scalability (5 checks):**
- [ ] Can this be systematized?
- [ ] Will this apply to multiple clients?
- [ ] Can AI identify this opportunity reliably?
- [ ] Does this scenario have longevity (not one-time event)?
- [ ] Can this be easily explained to the advisor?

**Score:** 
- 20-25 checks: ✅ Add to library
- 15-19 checks: ⚠️ Refine and retest
- <15 checks: ❌ Discard or completely rework

---

## Monthly Scenario Discovery Workflow

**Week 1: Article Scanning**
- Monday-Friday: Scan publication headlines (30 min total)
- Bookmark 2-3 most relevant articles
- Quick notes on potential opportunities

**Week 2: Extraction**
- Block 2 hours
- Extract 1-2 scenarios using this framework
- Add to "Potential Scenarios" queue

**Week 3: Testing**
- Test new scenarios with sample client data
- Validate matching criteria
- Check for false positives

**Week 4: Activation**
- Add validated scenarios to active library
- Archive or discard scenarios that didn't validate
- Update scenario performance tracker

**Monthly time investment: 4-6 hours**
**Expected output: 2-4 new validated scenarios per month**

---

This framework ensures every scenario extracted is actionable, testable, and revenue-generating.
