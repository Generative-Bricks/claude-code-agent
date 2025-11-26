# Starter Scenarios: Initial Focus Areas

## Overview
This document provides detailed, ready-to-use scenarios for your four initial focus areas:
1. Market/Interest Rate Sensitive Opportunities
2. FIA Reviews and Replacements
3. Portfolio Diversification
4. Tax Loss Harvesting

Each scenario is fully completed and can be added directly to your Scenario Library.

---

## CATEGORY 1: MARKET / INTEREST RATE SENSITIVE

### Scenario: MKT-001 - Rising Rate Bond Review

**Scenario ID**: MKT-001  
**Scenario Name**: Rising Rate Bond Review  
**Status**: Active

**Classifications:**
- **Product Type**: Fixed Income/Bonds
- **Scenario Type**: Portfolio Rebalancing
- **Urgency/Timing**: Near-term (30-90 days)
- **Client Segment**: Mass Affluent, HNW
- **Trigger Type**: Market-Driven (Interest Rates)
- **Complexity Level**: Moderate (Analysis Required)
- **Revenue Potential**: Medium (AUM Growth)
- **Meeting Requirements**: Standard Meeting (45-60 min)
- **Professional Coordination Required**: Self-Sufficient
- **Client Communication Strategy**: Proactive Outreach - Standard
- **Seasonality & Timing Window**: Year-Round
- **Life Stage Relevance**: Pre-Retiree (55-65), Early Retirement (65-75)
- **Risk Profile Match**: Conservative, Moderately Conservative

**Description**: 
As interest rates have risen significantly from historic lows, clients holding long-duration bonds or bond funds may face interest rate risk and opportunity cost. Review fixed income allocations for duration exposure and potential repositioning into higher-yielding instruments or shorter-duration securities.

**Business Case / Why This Matters**: 
When rates rise, existing bond values fall (inverse relationship). Clients who purchased bonds 3-5 years ago during low-rate environment may be earning 2-3% while new issues yield 5-6%. Additionally, long-duration bonds are more sensitive to rate changes. This creates both a risk management opportunity (reduce duration) and income enhancement opportunity (shift to higher yields).

**Matching Criteria (Logic/Rules)**:
```
(Bond_Holdings > 20% of portfolio OR Bond_Fund_Holdings > $100,000)
AND (Average_Bond_Duration > 7 years OR Purchased_Date > 3 years ago)
AND (Current_Yield_To_Maturity < Market_10Y_Treasury - 1.0%)
AND Client_Risk_Tolerance IN ['Conservative', 'Moderately Conservative']
```

**Required Client Data Fields**:
- Total Portfolio Value
- Bond Holdings ($ amount and %)
- Bond Fund Holdings
- Average Duration of Bond Holdings
- Purchase Dates of Bonds
- Current Yield to Maturity
- Maturity Dates
- Client Risk Tolerance
- Liquidity Needs

**Typical Actions / Next Steps**:
1. Pull bond holdings report with duration, yield, and maturity analysis
2. Calculate mark-to-market unrealized losses (if any)
3. Compare current yields to prevailing market rates
4. Model potential repositioning strategies (laddering, duration reduction)
5. Schedule review meeting to discuss rate environment and options
6. If agreed, execute trades to reposition

**Exclusion Rules**:
- Exclude if bonds held in tax-deferred accounts and would trigger tax loss harvesting benefit
- Do not recommend if client has specified "hold to maturity" preference
- Skip if bonds mature within 12 months (wait for maturity)
- Exclude if client purchased in last 6 months (too recent)
- Do not recommend if repositioning would trigger wash sale

**State Restrictions**: None (investment strategy)

**Accredited Investor Only**: No

**Minimum Asset Level**: $100,000 in fixed income

**Source Publication(s)**: Barron's, Financial Advisor Magazine, WealthManagement.com

**Date Added**: 2025-11-05  
**Date Updated**: 2025-11-05

---

### Scenario: MKT-002 - Cash Drag Opportunity

**Scenario ID**: MKT-002  
**Scenario Name**: Cash Drag Opportunity  
**Status**: Active

**Classifications:**
- **Product Type**: Cash/Money Market
- **Scenario Type**: Portfolio Rebalancing
- **Urgency/Timing**: Strategic (90-365 days)
- **Client Segment**: All segments
- **Trigger Type**: Market-Driven (Interest Rates)
- **Complexity Level**: Simple (Quick Review/Conversation)
- **Revenue Potential**: Medium (AUM Growth)
- **Meeting Requirements**: Quick Call (15-30 min)
- **Professional Coordination Required**: Self-Sufficient
- **Client Communication Strategy**: Proactive Outreach - Standard
- **Seasonality & Timing Window**: Year-Round
- **Life Stage Relevance**: All Life Stages
- **Risk Profile Match**: All Risk Profiles

**Description**: 
Clients holding excess cash in low or zero-yielding accounts (checking, savings) should be repositioned into higher-yielding money market funds, short-term treasuries, or sweep accounts now yielding 4-5%. This is "free money" opportunity with no additional risk.

**Business Case / Why This Matters**: 
With money market rates at 4.5-5.5%, cash in traditional bank accounts earning 0-0.5% represents significant opportunity cost. A client with $100k in cash earning 0.1% vs 5% is losing $4,900 annually. This is a simple, no-risk repositioning that improves client returns immediately and demonstrates proactive management.

**Matching Criteria (Logic/Rules)**:
```
(Cash_Holdings > $25,000 OR Cash_Percentage > 5% of portfolio)
AND Current_Cash_Yield < 3.0%
AND NOT (Earmarked_For_Major_Purchase_Next_90_Days)
```

**Required Client Data Fields**:
- Cash Holdings ($ and % of portfolio)
- Current Cash Yield
- Account Type (checking, savings, brokerage sweep, etc.)
- Upcoming Major Purchases (if known)
- Monthly Liquidity Needs

**Typical Actions / Next Steps**:
1. Identify cash balances and current yields
2. Calculate opportunity cost (current yield vs market rates)
3. Recommend repositioning to higher-yield vehicles
4. Execute money market or treasury purchase
5. Set up for automatic sweep if applicable

**Exclusion Rules**:
- Exclude if cash is earmarked for known major purchase within 90 days (house, car, etc.)
- Skip if client explicitly wants FDIC insurance vs securities (education opportunity here)
- Do not recommend if cash is emergency fund client wants in bank (respect preference)
- Exclude if amount < $10,000 (not material enough)

**State Restrictions**: None

**Accredited Investor Only**: No

**Minimum Asset Level**: $25,000 in cash holdings

**Source Publication(s)**: Kiplinger's, Money Magazine, Financial Advisor Magazine

**Date Added**: 2025-11-05  
**Date Updated**: 2025-11-05

---

### Scenario: MKT-003 - Equity Volatility Protection Review

**Scenario ID**: MKT-003  
**Scenario Name**: Equity Volatility Protection Review  
**Status**: Active

**Classifications:**
- **Product Type**: Fixed Indexed Annuities (FIA)
- **Scenario Type**: Risk Management
- **Urgency/Timing**: Strategic (90-365 days)
- **Client Segment**: Pre-Retiree (55-65), New Retiree (0-5 years retired)
- **Trigger Type**: Market-Driven (Volatility)
- **Complexity Level**: Moderate (Analysis Required)
- **Revenue Potential**: High (Direct Product Sale)
- **Meeting Requirements**: Standard Meeting (45-60 min)
- **Professional Coordination Required**: Self-Sufficient
- **Client Communication Strategy**: Educational First
- **Seasonality & Timing Window**: Market Event Driven
- **Life Stage Relevance**: Pre-Retiree (55-65), Early Retirement (65-75)
- **Risk Profile Match**: Conservative, Moderately Conservative, Moderate

**Description**: 
During periods of elevated market volatility (VIX > 20), clients approaching or in early retirement may benefit from repositioning a portion of equity exposure into FIAs, providing downside protection while maintaining upside participation. This is particularly relevant for the "fragile decade" (5 years before/after retirement).

**Business Case / Why This Matters**: 
Sequence of returns risk is highest in the years immediately before and after retirement. A 20-30% market decline in this window can permanently impair retirement outcomes. FIAs offer principal protection with market participation, making them effective volatility hedges for this critical life stage. With VIX elevated, this conversation becomes timely and relevant.

**Matching Criteria (Logic/Rules)**:
```
(Age BETWEEN 58 AND 72)
AND (VIX_Current > 20 OR S&P_YTD_Volatility > 15%)
AND (Equity_Allocation > 50% OR Equity_Value > $200,000)
AND (Has_FIA = False OR FIA_Allocation < 20%)
AND Risk_Tolerance IN ['Conservative', 'Moderately Conservative', 'Moderate']
AND Liquidity_Needs < 30% of portfolio
```

**Required Client Data Fields**:
- Age
- Retirement Date (actual or planned)
- Current Equity Allocation ($ and %)
- Current FIA Holdings (if any)
- Risk Tolerance
- Liquidity Needs
- Income Goals
- Total Portfolio Value

**Typical Actions / Next Steps**:
1. Calculate sequence of returns risk exposure
2. Model portfolio impact of market decline at current allocation
3. Present FIA as volatility hedge with illustrations
4. Discuss appropriate allocation (typically 15-30% for this scenario)
5. Review specific FIA products with current crediting rates
6. Execute purchase if client agrees

**Exclusion Rules**:
- Exclude if client has >30% in FIAs already (avoid over-concentration)
- Skip if client explicitly prefers all-equity approach
- Do not recommend if client needs high liquidity (>40% of portfolio in next 3 years)
- Exclude if VIX < 15 (wait for elevated volatility for relevance)
- Skip if client < 55 or > 75 (outside target window)

**State Restrictions**: Verify FIA suitability requirements by state, especially for senior investors

**Accredited Investor Only**: No

**Minimum Asset Level**: $200,000 in equities for repositioning

**Source Publication(s)**: ThinkAdvisor, Financial Advisor Magazine, Journal of Financial Service Professionals

**Date Added**: 2025-11-05  
**Date Updated**: 2025-11-05

---

## CATEGORY 2: FIA REVIEWS AND REPLACEMENTS

### Scenario: FIA-001 - FIA Approaching Surrender End

*[Previously created in template - included here for completeness]*

**Scenario ID**: FIA-001  
**Scenario Name**: FIA Approaching Surrender End  
**Status**: Active

**Classifications:**
- **Product Type**: Fixed Indexed Annuities (FIA)
- **Scenario Type**: Product Review/Replacement
- **Urgency/Timing**: Near-term (30-90 days)
- **Client Segment**: Established Retiree (5+ years)
- **Trigger Type**: Product-Specific (Surrender Period)
- **Complexity Level**: Moderate (Analysis Required)
- **Revenue Potential**: High (Direct Product Sale)
- **Meeting Requirements**: Standard Meeting (45-60 min)
- **Professional Coordination Required**: Self-Sufficient
- **Client Communication Strategy**: Proactive Outreach - Standard
- **Seasonality & Timing Window**: Year-Round
- **Life Stage Relevance**: Pre-Retiree, Retirees
- **Risk Profile Match**: Conservative, Moderately Conservative

**Description**: 
Client has FIA within 6-12 months of surrender period expiration. Need to review current product performance, crediting rates, and explore potentially better alternatives.

**Business Case / Why This Matters**: 
FIA products purchased 5-7+ years ago may have lower caps, participation rates, and crediting methods compared to current offerings. Post-surrender period is optimal time for 1035 exchange without penalties.

**Matching Criteria (Logic/Rules)**:
```
Product_Type = 'FIA'
AND Surrender_End_Date BETWEEN TODAY AND TODAY + 365 days
AND Purchase_Date >= 6 years ago
AND (Cap_Rate < Market_Average_Cap - 1.0% OR Participation_Rate < 100%)
```

**Required Client Data Fields**:
- Product Type
- Purchase Date
- Surrender Schedule/End Date
- Current Value
- Crediting Rate
- Cap Rate
- Participation Rate
- Income Rider Status

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
- Exclude if current product features (riders, etc.) cannot be matched

**State Restrictions**: Check state-specific suitability requirements; Some states require additional documentation for senior replacements (age 65+)

**Accredited Investor Only**: No

**Minimum Asset Level**: N/A

**Source Publication(s)**: Financial Advisor Magazine, ThinkAdvisor

**Date Added**: 2025-11-05  
**Date Updated**: 2025-11-05

---

### Scenario: FIA-002 - Low Crediting Rate FIA Review

**Scenario ID**: FIA-002  
**Scenario Name**: Low Crediting Rate FIA Review  
**Status**: Active

**Classifications:**
- **Product Type**: Fixed Indexed Annuities (FIA)
- **Scenario Type**: Product Review/Replacement
- **Urgency/Timing**: Strategic (90-365 days)
- **Client Segment**: All Retiree segments
- **Trigger Type**: Product-Specific (Crediting Rate)
- **Complexity Level**: Moderate (Analysis Required)
- **Revenue Potential**: High (Direct Product Sale)
- **Meeting Requirements**: Standard Meeting (45-60 min)
- **Professional Coordination Required**: Self-Sufficient
- **Client Communication Strategy**: Proactive Outreach - Standard
- **Seasonality & Timing Window**: Year-Round
- **Life Stage Relevance**: All Retiree segments
- **Risk Profile Match**: Conservative, Moderately Conservative

**Description**: 
Client's FIA has earned significantly below market average over the past 2-3 years, suggesting poor crediting strategy selection or product design. Even mid-surrender, may be worth discussing 1035 exchange if performance gap is substantial and fees are manageable.

**Business Case / Why This Matters**: 
Not all FIAs are created equal. Some crediting strategies, index choices, or product designs consistently underperform. If a client's FIA has earned 1-2% annually while market comparable products earned 4-5%, this represents material opportunity cost. In some cases, paying a modest surrender charge to move to a better product can be beneficial over a 10+ year horizon.

**Matching Criteria (Logic/Rules)**:
```
Product_Type = 'FIA'
AND Average_Annual_Crediting_Last_3_Years < 2.5%
AND Market_Average_FIA_Crediting_Last_3_Years > 4.0%
AND Current_Value > $100,000
AND (Surrender_Charge < 7% OR Years_Held > 3)
```

**Required Client Data Fields**:
- Product Type
- Current Value
- Historical Crediting Rates (last 2-3 years)
- Years Held
- Current Surrender Charge (% and $)
- Crediting Strategy
- Index Allocation
- Cap/Participation Rates

**Typical Actions / Next Steps**:
1. Calculate actual performance over past 2-3 years
2. Compare to market benchmarks and peer products
3. Run breakeven analysis (surrender cost vs improved earnings)
4. If breakeven < 3 years, schedule discussion
5. Present alternatives with side-by-side comparison
6. Execute 1035 if warranted

**Exclusion Rules**:
- Exclude if surrender charge > 10% (too expensive to move)
- Skip if client purchased < 2 years ago (too soon to evaluate performance)
- Do not recommend if breakeven > 5 years (too long to recover)
- Exclude if client's strategy selection caused underperformance and better option exists in same contract
- Skip if performance is in line with chosen conservative strategy (client preference)

**State Restrictions**: Enhanced suitability review required for replacements; Document performance comparison

**Accredited Investor Only**: No

**Minimum Asset Level**: $100,000 (surrender charges on smaller amounts may not be worth breakeven period)

**Source Publication(s)**: Best's Review, Insurance Journal, ThinkAdvisor

**Date Added**: 2025-11-05  
**Date Updated**: 2025-11-05

---

### Scenario: FIA-003 - Income Rider Optimization

**Scenario ID**: FIA-003  
**Scenario Name**: Income Rider Optimization  
**Status**: Active

**Classifications:**
- **Product Type**: Fixed Indexed Annuities (FIA)
- **Scenario Type**: Retirement Income Planning
- **Urgency/Timing**: Strategic (90-365 days)
- **Client Segment**: Pre-Retiree (5 years to retirement), New Retiree (0-5 years retired)
- **Trigger Type**: Life Event (Retirement)
- **Complexity Level**: Moderate (Analysis Required)
- **Revenue Potential**: Medium (AUM Growth)
- **Meeting Requirements**: Standard Meeting (45-60 min)
- **Professional Coordination Required**: Self-Sufficient
- **Client Communication Strategy**: Next Scheduled Touch
- **Seasonality & Timing Window**: Year-Round
- **Life Stage Relevance**: Pre-Retiree, Early Retirement
- **Risk Profile Match**: Conservative, Moderately Conservative, Moderate

**Description**: 
Client has FIA without income rider, or with suboptimal income rider, approaching retirement and will need guaranteed income stream. Review and potentially add/upgrade income rider, or reposition to FIA with stronger income guarantees.

**Business Case / Why This Matters**: 
Income riders provide guaranteed lifetime income with crediting bonuses and rollup rates. Clients approaching retirement (within 5 years) or recently retired may not have properly positioned FIA for income. Adding a rider or repositioning to income-focused FIA can significantly enhance retirement income security. Current income riders offer 5-7% rollup rates and 5-6% withdrawal rates—substantially better than products from 5-7 years ago.

**Matching Criteria (Logic/Rules)**:
```
Product_Type = 'FIA'
AND (Income_Rider = 'No' OR Income_Rider_Rollup_Rate < 5.0%)
AND (Age BETWEEN 60 AND 70 OR Retirement_Date <= 5 years)
AND Stated_Income_Need = 'Yes'
AND Surrender_End_Date <= 24 months OR Surrender_Charge < 5%
```

**Required Client Data Fields**:
- Product Type
- Income Rider Status (Yes/No)
- Income Rider Rollup Rate (if applicable)
- Income Rider Withdrawal Rate (if applicable)
- Age / Retirement Date
- Income Needs
- Current Value
- Surrender Schedule

**Typical Actions / Next Steps**:
1. Review current FIA and income rider (if any)
2. Calculate projected income from current setup
3. Illustrate income with upgraded/added rider
4. Compare to alternative FIA income products
5. Run cost-benefit analysis (rider fees vs. guaranteed income)
6. Execute rider addition or 1035 exchange if beneficial

**Exclusion Rules**:
- Exclude if client has sufficient pension/Social Security (no income gap)
- Skip if client prefers other income strategies (systematic withdrawals, etc.)
- Do not recommend if surrender charge > 7% and not near end
- Exclude if rider addition cost > benefit over 10-year period
- Skip if client wants maximum liquidity (income riders reduce liquidity)

**State Restrictions**: Verify income rider availability by state

**Accredited Investor Only**: No

**Minimum Asset Level**: $100,000 (rider fees on smaller amounts may not be cost-effective)

**Source Publication(s)**: ThinkAdvisor, Financial Advisor Magazine, Insurance Journal

**Date Added**: 2025-11-05  
**Date Updated**: 2025-11-05

---

## CATEGORY 3: PORTFOLIO DIVERSIFICATION

### Scenario: DIV-001 - Concentrated Portfolio Diversification

*[Previously created in template - included here for completeness]*

**Scenario ID**: DIV-001  
**Scenario Name**: Concentrated Portfolio Diversification  
**Status**: Active

[Full details as previously provided in template]

---

### Scenario: DIV-002 - Single Sector Overweight

**Scenario ID**: DIV-002  
**Scenario Name**: Single Sector Overweight  
**Status**: Active

**Classifications:**
- **Product Type**: Equities/Stocks
- **Scenario Type**: Diversification
- **Urgency/Timing**: Strategic (90-365 days)
- **Client Segment**: Mass Affluent, HNW
- **Trigger Type**: Market-Driven (Sector Performance)
- **Complexity Level**: Moderate (Analysis Required)
- **Revenue Potential**: Medium (AUM Growth)
- **Meeting Requirements**: Standard Meeting (45-60 min)
- **Professional Coordination Required**: Self-Sufficient
- **Client Communication Strategy**: Proactive Outreach - Standard
- **Seasonality & Timing Window**: Year-Round
- **Life Stage Relevance**: All Life Stages
- **Risk Profile Match**: Moderate, Moderately Aggressive, Aggressive

**Description**: 
Client portfolio shows concentration in a single sector (>30% allocation), creating sector-specific risk. Recent strong performance in certain sectors (technology, healthcare, energy) often leads to drift and overconcentration. Recommend rebalancing to reduce sector risk and improve diversification.

**Business Case / Why This Matters**: 
Sector concentration increases portfolio volatility and risk. The 2000 tech crash, 2008 financial crisis, and 2020 energy collapse all demonstrated sector-specific risk. Clients who benefited from strong sector performance often resist rebalancing, but concentration risk can wipe out years of gains quickly. Proactive rebalancing locks in gains and reduces future volatility.

**Matching Criteria (Logic/Rules)**:
```
(Any_Single_Sector > 30% of equity portfolio)
OR (Technology_Sector > 35% of equity portfolio)
OR (Single_Sector_YTD_Gain > 40% AND Sector_Allocation > 25%)
AND Portfolio_Beta > 1.1
AND Risk_Tolerance NOT IN ['Aggressive', 'Very Aggressive']
```

**Required Client Data Fields**:
- Equity Holdings by Sector
- Sector Allocations (%)
- YTD Performance by Sector
- Total Portfolio Value
- Portfolio Beta
- Risk Tolerance
- Target Allocation (if documented)

**Typical Actions / Next Steps**:
1. Generate sector allocation report
2. Calculate sector concentration vs benchmarks (S&P 500 sector weights)
3. Identify overweight sectors and quantify risk
4. Present rebalancing recommendations
5. Discuss tax implications if in taxable account
6. Execute rebalancing trades

**Exclusion Rules**:
- Exclude if client works in overweight sector and concentration is intentional (e.g., tech employee with tech stock)
- Skip if rebalancing would trigger significant capital gains (>25% of position) without offsetting losses
- Do not recommend if client explicitly stated sector preference
- Exclude if concentration developed in last 3 months (wait for 6+ month pattern)
- Skip if portfolio value < $50,000 (diversification less critical)

**State Restrictions**: None

**Accredited Investor Only**: No

**Minimum Asset Level**: $50,000 in equities

**Source Publication(s)**: Barron's, WealthManagement.com, Journal of Financial Service Professionals

**Date Added**: 2025-11-05  
**Date Updated**: 2025-11-05

---

### Scenario: DIV-003 - International Equity Underweight

**Scenario ID**: DIV-003  
**Scenario Name**: International Equity Underweight  
**Status**: Active

**Classifications:**
- **Product Type**: Equities/Stocks, ETFs
- **Scenario Type**: Diversification
- **Urgency/Timing**: Strategic (90-365 days)
- **Client Segment**: Mass Affluent, HNW
- **Trigger Type**: Market Opportunity
- **Complexity Level**: Moderate (Analysis Required)
- **Revenue Potential**: Medium (AUM Growth)
- **Meeting Requirements**: Standard Meeting (45-60 min)
- **Professional Coordination Required**: Self-Sufficient
- **Client Communication Strategy**: Proactive Outreach - Standard
- **Seasonality & Timing Window**: Year-Round
- **Life Stage Relevance**: Accumulation, Peak Earning, Pre-Retiree
- **Risk Profile Match**: Moderate, Moderately Aggressive, Aggressive

**Description**: 
Client has little to no international equity exposure (<10% of equity allocation) despite international markets representing ~50% of global market cap. This creates home country bias and concentrates portfolio in U.S. economy. Recommend adding international developed and/or emerging market exposure for global diversification.

**Business Case / Why This Matters**: 
U.S. investors often exhibit home country bias, missing opportunities in international markets and concentrating risk in U.S. economy. International equities provide: (1) Exposure to different economic cycles, (2) Currency diversification, (3) Access to companies dominating global industries, (4) Potentially lower valuations. While U.S. has outperformed recently, cycles change and diversified portfolios weather shifts better.

**Matching Criteria (Logic/Rules)**:
```
(International_Equity_Allocation < 10% of total equity)
OR (International_Equity_Value < $25,000)
AND Total_Equity_Allocation > 60%
AND Risk_Tolerance IN ['Moderate', 'Moderately Aggressive', 'Aggressive']
AND Age < 70
AND Investment_Time_Horizon > 5 years
```

**Required Client Data Fields**:
- Equity Holdings (domestic vs international)
- International Equity Allocation (%)
- Total Portfolio Value
- Risk Tolerance
- Age
- Investment Time Horizon
- Currency Risk Tolerance (if known)

**Typical Actions / Next Steps**:
1. Calculate current international allocation
2. Compare to recommended allocation (15-25% for moderate risk)
3. Discuss benefits of global diversification
4. Present international equity options (developed markets ETFs, emerging markets, global funds)
5. Address currency risk and volatility concerns
6. Implement phased approach (add 5-10% initially, monitor)

**Exclusion Rules**:
- Exclude if client has strong preference for U.S. only (respect preference after education)
- Skip if client < 5 year time horizon (volatility risk)
- Do not recommend if client has negative experience with international investing
- Exclude if age > 75 (typically too conservative for new international exposure)
- Skip if risk tolerance is Conservative (international equity may not suit)

**State Restrictions**: None

**Accredited Investor Only**: No

**Minimum Asset Level**: $100,000 in equities (for meaningful international allocation)

**Source Publication(s)**: Morningstar, WealthManagement.com, Financial Advisor Magazine

**Date Added**: 2025-11-05  
**Date Updated**: 2025-11-05

---

## CATEGORY 4: TAX LOSS HARVESTING

### Scenario: TAX-001 - Year-End Tax Loss Harvesting

*[Previously created in template - included here for completeness]*

**Scenario ID**: TAX-001  
**Scenario Name**: Year-End Tax Loss Harvesting  
**Status**: Seasonal

[Full details as previously provided in template]

---

### Scenario: TAX-002 - Q1 Tax Loss Harvesting with Roth Conversion

**Scenario ID**: TAX-002  
**Scenario Name**: Q1 Tax Loss Harvesting with Roth Conversion  
**Status**: Seasonal

**Classifications:**
- **Product Type**: Multi-Product Strategy
- **Scenario Type**: Tax Planning
- **Urgency/Timing**: Time-Sensitive Event
- **Client Segment**: Pre-Retiree, New Retiree
- **Trigger Type**: Regulatory/Tax Change
- **Complexity Level**: Complex (Multi-Product Strategy)
- **Revenue Potential**: Low (Planning Fee)
- **Meeting Requirements**: Comprehensive Review (90-120 min)
- **Professional Coordination Required**: CPA Coordination
- **Client Communication Strategy**: Proactive Outreach - High Priority
- **Seasonality & Timing Window**: Q1 Focus (Jan-Mar)
- **Life Stage Relevance**: Pre-Retiree, Early Retirement
- **Risk Profile Match**: All Risk Profiles

**Description**: 
After year-end, Q1 presents opportunity to harvest any tax losses in taxable accounts while simultaneously executing Roth conversions from Traditional IRA. Losses offset conversion income, reducing or eliminating tax on conversion. This is particularly powerful for clients who had market losses in prior year.

**Business Case / Why This Matters**: 
Roth conversions create taxable income, but tax losses can offset this income. If client has $50k in capital losses and converts $50k from IRA to Roth, conversion may be tax-free. This is especially valuable for early retirees in low tax brackets before RMDs and Social Security begin. Window is Q1 while tax losses are fresh and tax filing hasn't occurred.

**Matching Criteria (Logic/Rules)**:
```
(Has_Taxable_Account = True AND Unrealized_Losses > $10,000)
OR (Prior_Year_Realized_Losses > $3,000 AND Carryforward_Losses > $0)
AND Has_Traditional_IRA = True
AND Traditional_IRA_Balance > $50,000
AND Age BETWEEN 59.5 AND 72
AND NOT Currently_Taking_RMDs
AND Current_Date BETWEEN Jan-1 AND Mar-31
```

**Required Client Data Fields**:
- Taxable Account Holdings
- Unrealized Gains/Losses
- Prior Year Realized Losses
- Carryforward Loss Amount
- Traditional IRA Balance
- Age
- RMD Status
- Current Year Tax Bracket (estimated)
- State Tax Rate

**Typical Actions / Next Steps**:
1. Calculate available tax losses (current + carryforward)
2. Determine optimal Roth conversion amount (match to losses)
3. Coordinate with CPA to verify tax strategy
4. Execute tax loss harvesting in January
5. Execute Roth conversion by mid-February
6. Provide documentation to CPA for tax filing
7. Avoid wash sales (don't repurchase harvested positions within 30 days)

**Exclusion Rules**:
- Exclude if no taxable account with losses available
- Skip if already taking RMDs (different strategy needed)
- Do not recommend if age < 59.5 (10% penalty on conversion, usually not optimal)
- Exclude if client's tax bracket is 0% (no benefit from loss offset)
- Skip if after March 31 (less time to coordinate with CPA)
- Do not recommend if carryforward losses are minimal (<$5,000)

**State Restrictions**: Verify state tax treatment of Roth conversions (some states don't conform to federal treatment)

**Accredited Investor Only**: No

**Minimum Asset Level**: $50,000 in Traditional IRA, $10,000 in tax losses

**Source Publication(s)**: Kiplinger's, Journal of Financial Service Professionals, Financial Advisor Magazine

**Date Added**: 2025-11-05  
**Date Updated**: 2025-11-05

---

### Scenario: TAX-003 - Market Downturn Tax Loss Opportunity

**Scenario ID**: TAX-003  
**Scenario Name**: Market Downturn Tax Loss Opportunity  
**Status**: Active

**Classifications:**
- **Product Type**: Equities/Stocks, ETFs, Mutual Funds
- **Scenario Type**: Tax Planning
- **Urgency/Timing**: Immediate (0-30 days)
- **Client Segment**: Mass Affluent, HNW
- **Trigger Type**: Market-Driven (Volatility)
- **Complexity Level**: Simple (Quick Review/Conversation)
- **Revenue Potential**: Low (Planning Fee)
- **Meeting Requirements**: Quick Call (15-30 min)
- **Professional Coordination Required**: Self-Sufficient
- **Client Communication Strategy**: Proactive Outreach - High Priority
- **Seasonality & Timing Window**: Market Event Driven
- **Life Stage Relevance**: All Life Stages
- **Risk Profile Match**: All Risk Profiles

**Description**: 
When markets decline significantly (S&P down >10%), proactively reach out to clients with taxable accounts to harvest losses before recovery. This turns portfolio pain into tax benefit and demonstrates proactive management during volatile times.

**Business Case / Why This Matters**: 
Market downturns create tax loss opportunities, but many advisors wait until year-end. Proactive mid-year harvesting: (1) Locks in losses before potential recovery, (2) Creates tax asset (loss carryforward), (3) Demonstrates value during difficult markets, (4) Differentiates service. A 15% market decline on $500k = $75k in potential losses to harvest. At 20% capital gains rate, that's $15k in tax savings.

**Matching Criteria (Logic/Rules)**:
```
Has_Taxable_Account = True
AND S&P_500_Decline_from_High > 10%
AND (Unrealized_Losses_Current > $10,000 OR Equity_Positions_in_Loss > 3)
AND NOT (Tax_Loss_Harvested_in_Last_30_Days)
AND Equity_Allocation > 40%
```

**Required Client Data Fields**:
- Taxable Account Holdings
- Unrealized Gains/Losses by Position
- Cost Basis
- Purchase Dates (for wash sale check)
- Recent Transaction History
- Tax Bracket (estimated)

**Typical Actions / Next Steps**:
1. Generate unrealized loss report (triggered by market decline)
2. Identify positions in loss that are suitable for harvesting
3. Reach out proactively to client (phone or email)
4. Explain opportunity and tax benefit
5. Execute trades (sell at loss, buy similar but not identical security)
6. Document for tax reporting

**Exclusion Rules**:
- Exclude if no taxable account
- Skip if already harvested losses in last 30 days (avoid over-communication)
- Do not recommend if client is in 0% capital gains bracket (no benefit)
- Exclude if all positions are in qualified accounts (no tax benefit)
- Skip if market decline < 10% (not significant enough)
- Do not recommend if client has expressed desire not to trade during volatility

**State Restrictions**: None (federal tax strategy)

**Accredited Investor Only**: No

**Minimum Asset Level**: $50,000 in taxable account

**Source Publication(s)**: Barron's, WealthManagement.com, Financial Advisor Magazine

**Date Added**: 2025-11-05  
**Date Updated**: 2025-11-05

---

## Summary of Starter Scenarios

### By Category:
- **Market/Interest Rate Sensitive**: 3 scenarios (MKT-001 to MKT-003)
- **FIA Reviews**: 3 scenarios (FIA-001 to FIA-003)
- **Portfolio Diversification**: 3 scenarios (DIV-001 to DIV-003)
- **Tax Loss Harvesting**: 3 scenarios (TAX-001 to TAX-003)

**Total**: 12 detailed, ready-to-use scenarios

### Urgency Distribution:
- Immediate (0-30 days): 1 scenario
- Near-term (30-90 days): 2 scenarios
- Strategic (90-365 days): 6 scenarios
- Time-Sensitive Event: 2 scenarios
- Seasonal: 1 scenario

### Complexity Distribution:
- Simple: 2 scenarios
- Moderate: 9 scenarios
- Complex: 1 scenario

### Revenue Potential Distribution:
- High (Direct Product Sale): 4 scenarios
- Medium (AUM Growth): 5 scenarios
- Low (Planning Fee): 3 scenarios

---

## Next Steps

1. **Review These 12 Scenarios**: Ensure they align with your practice and client base

2. **Customize as Needed**: 
   - Adjust thresholds (e.g., minimum asset levels)
   - Modify exclusion rules based on your preferences
   - Update source publications to ones you actually monitor

3. **Add to Your Template**: Copy these into your Scenario Library Excel sheet

4. **Test with Sample Clients**: 
   - Pick 3-5 clients
   - Manually apply matching criteria
   - Refine criteria based on results

5. **Build Additional Scenarios**: Use these as templates to create 18-28 more scenarios across other areas

6. **Plan Next Build Session**: 
   - Estate planning scenarios?
   - Life insurance reviews?
   - Beneficiary updates?
   - RMD planning?
   - College planning?

Ready to test these with your client data?
