# Client Matching Methodology

## Purpose
This document details the methodology for matching clients to revenue scenarios and generating ranked opportunity lists.

---

## Overview of Matching Process

```
Client Data + Scenario Library
         ↓
Apply Matching Criteria (for each scenario)
         ↓
Generate All Matches (may be 50-100+ matches)
         ↓
Calculate Revenue for Each Match
         ↓
Apply Business Rules
         ↓
Rank by Weighted Score
         ↓
Filter to Top 25
         ↓
Format as Report
```

---

## Step 1: Apply Matching Criteria

### How Matching Works

For each scenario in the library, apply its matching criteria to all clients:

**Example Scenario: FIA-001 (Surrender Ending)**
```
Matching Criteria:
Product_Type = 'FIA'
AND Purchase_Date >= 5 years ago
AND Current_Cap_Rate < 5.5%
AND Surrender_End_Date within 12 months
```

**Matching Logic:**
1. Loop through all clients
2. For each client, check if they meet ALL criteria (AND logic)
3. If yes → Create a match record
4. If no → Skip to next client

**Match Record:**
```
{
  "client_id": "12345",
  "client_name": "Martinez, Sofia",
  "scenario_id": "FIA-001",
  "scenario_name": "FIA Surrender Ending Review",
  "matching_data": {
    "Product_Type": "FIA",
    "Product_Value": "$487,000",
    "Purchase_Date": "2019-03-15",
    "Current_Cap_Rate": "4.2%",
    "Surrender_End_Date": "2026-02-28"
  }
}
```

### Handling Multiple Product Holdings

**Problem:** A client may have multiple FIAs, multiple life insurance policies, etc.

**Solution:** Create separate matches for each qualifying product

**Example:**
```
Client: Johnson, Robert
- FIA #1: $250K, purchased 2018, cap 4.5%, surrender ends in 3 months → MATCH
- FIA #2: $180K, purchased 2022, cap 6.5%, surrender ends in 4 years → NO MATCH
- FIA #3: $100K, purchased 2019, cap 4.0%, surrender ends in 1 month → MATCH

Result: 2 separate matches for same client + same scenario
```

**In final ranking:** Select the highest-value match per client (unless bundling applies)

---

## Step 2: Check Exclusions

After generating initial matches, apply exclusions:

### Exclusion Logic

**For each match, check if any exclusion criteria apply:**

Example exclusions for FIA-001:
```
Exclude if:
- Client purchased new FIA within last 12 months → Check: Recent_FIA_Purchase
- Surrender charge > 7% → Check: Current_Surrender_Charge
- Client initiated withdrawals → Check: Withdrawal_Activity_This_Year
- Client has liquidation plans → Check: Notes/Upcoming_Expenses
```

**If ANY exclusion is true → Remove match**

### Data Availability Issues

**Problem:** You may not have data for all exclusions

**Solutions:**
1. **Best practice:** Flag for manual review instead of auto-excluding
2. **Conservative:** If you can't verify, include the match with a "Verify: [exclusion]" note
3. **Aggressive:** Only exclude if you have positive confirmation

**Recommended approach:** Flag uncertain exclusions for advisor verification

---

## Step 3: Calculate Revenue

For each remaining match, calculate estimated revenue:

### Revenue Calculation Methods

**Method 1: Product Commission (One-Time)**
```
Revenue = Product_Value × Commission_Rate

Example (FIA Replacement):
Product_Value = $487,000
Commission_Rate = 0.05 (5%)
Revenue = $487,000 × 0.05 = $24,350
```

**Method 2: AUM Fee (Recurring Annual)**
```
Revenue = New_AUM × Annual_Fee_Rate

Example (Cash to Managed Account):
Cash_Balance = $180,000
Reposition_Percentage = 0.50 (assume 50% can be moved)
New_AUM = $180,000 × 0.50 = $90,000
Annual_Fee_Rate = 0.01 (1%)
Revenue = $90,000 × 0.01 = $900/year
```

**Method 3: Planning Fee (Project)**
```
Revenue = Flat_Fee OR (Hours × Hourly_Rate)

Example (Estate Planning):
Flat_Fee = $5,000

OR

Estimated_Hours = 8
Hourly_Rate = $400
Revenue = 8 × $400 = $3,200
```

**Method 4: Life Insurance (Face Value)**
```
Revenue = Face_Value × Commission_Percentage

Example (Term Life):
Needed_Coverage = $1,000,000
Commission_Percentage = 0.01 (1% of face value, varies by product)
Revenue = $1,000,000 × 0.01 = $10,000
```

### Handling Missing Data

**If required data for revenue calculation is missing:**

**Option A:** Use scenario average
```
If Product_Value is missing:
  Use Avg_Product_Value for this scenario
  Example: Avg FIA value = $350,000
```

**Option B:** Use client net worth proxy
```
If Product_Value is missing but Net_Worth is known:
  Estimate = Net_Worth × Product_Percentage
  Example: $2M net worth, FIAs typically 25% = $500K estimated
```

**Option C:** Flag for manual entry
```
Revenue = "Data needed: Product_Value"
Rank lower in list until data obtained
```

---

## Step 4: Apply Business Rules

### Rule 1: One Opportunity Per Client (Primary Rule)

**Problem:** One client may match multiple scenarios

**Solution:** Select ONE opportunity per client for the Top 25 list

**Selection logic:**
1. Calculate weighted score for each opportunity (see Step 5)
2. Select the highest-scoring opportunity
3. Archive other matches for that client

**Exception:** Bundling Rule (see below)

**Example:**
```
Client: Martinez, Sofia
- FIA-001 (FIA Surrender): $24,350 revenue, score 26,180
- TAX-001 (Tax Loss Harvesting): $1,500 revenue, score 1,650
- DIV-001 (Concentration Review): $3,200 revenue, score 3,520

Selected: FIA-001 (highest score)
Archived: TAX-001, DIV-001 (revisit after FIA-001 completed)
```

### Rule 2: Bundling Exception

**When to bundle multiple opportunities for one client:**

**Criteria:**
- Total combined revenue > $5,000
- Opportunities are complementary (not competing)
- Can be addressed in single meeting
- Timeline aligns

**Common bundles:**
- Tax loss harvesting + Roth conversion
- FIA review + life insurance gap analysis
- Diversification + alternative investment placement

**Example:**
```
Client: Chen, David
- TAX-001 (Tax Loss): $2,000 (alone might not make Top 25)
- TAX-002 (Roth Conversion): $3,500 (alone might not make Top 25)
- Combined: $5,500 + efficiency bonus

Bundle these as: "Tax Planning Package" with combined revenue $5,500
```

### Rule 3: Recency Rule

**Avoid recommending same scenario type recently completed:**

```
If (Scenario completed for this client within last X months):
  Exclude match

Recency windows:
- Product replacement: 12 months
- Tax planning: 6 months (unless special circumstance)
- Diversification review: 6 months
- Comprehensive plan: 12 months
```

**Implementation:** Check `Last_Action_Date` and `Action_Type` fields

### Rule 4: Concentration Limits

**Prevent over-concentration on single scenario type:**

**In Top 25, limit to:**
- Max 8 opportunities of same scenario type
- Max 5 opportunities of same category
- Ensures diversity of opportunities

**Example:**
```
Top 25 contains:
- 8x FIA reviews (at limit)
- 5x Tax loss harvesting
- 4x Cash drag opportunities
- 3x Life insurance gaps
- 5x Other scenarios

If 9th FIA review would qualify, skip to next scenario type
```

**Rationale:** Advisor needs variety, not 25 FIA reviews

---

## Step 5: Calculate Weighted Score

Each opportunity gets a weighted score based on multiple factors:

### Base Score = Estimated Revenue

```
Base_Score = Estimated_Revenue
```

### Urgency Multiplier

```
If Urgency = "Immediate" (deadline < 30 days): × 1.3
If Urgency = "Near-term" (deadline 30-90 days): × 1.2
If Urgency = "Time-sensitive" (deadline 90-180 days): × 1.1
If Urgency = "Strategic" (no deadline): × 1.0
```

**Example:**
```
Opportunity: FIA surrender ends in 45 days
Base revenue: $24,350
Urgency: Near-term
Weighted score: $24,350 × 1.2 = $29,220
```

### Complexity Adjustment

```
If Complexity = "Simple" (one call): ÷ 1.0 (no adjustment)
If Complexity = "Moderate" (standard meeting): ÷ 1.0 (no adjustment)
If Complexity = "Complex" (multiple meetings): ÷ 1.1
If Complexity = "Advanced" (professional coordination): ÷ 1.2
```

**Rationale:** Penalize opportunities that require disproportionate effort

**Example:**
```
Opportunity: Estate plan requiring attorney coordination
Base revenue: $8,000
Complexity: Advanced
Weighted score: $8,000 ÷ 1.2 = $6,667
```

### Likelihood Multiplier (Optional)

**If you have confidence scoring:**

```
If Likelihood = "High" (80%+ probability): × 1.1
If Likelihood = "Medium" (50-80% probability): × 1.0
If Likelihood = "Low" (<50% probability): × 0.9
```

**Example:**
```
Opportunity: Client previously expressed interest in this area
Base revenue: $15,000
Likelihood: High
Weighted score: $15,000 × 1.1 = $16,500
```

### Final Weighted Score Formula

```
Weighted_Score = (Base_Revenue × Urgency_Multiplier × Likelihood_Multiplier) ÷ Complexity_Adjustment
```

**Complete Example:**
```
Opportunity: Martinez - FIA Surrender Review
Base_Revenue: $24,350
Urgency: Near-term (× 1.2)
Likelihood: High (× 1.1)
Complexity: Moderate (÷ 1.0)

Weighted_Score = ($24,350 × 1.2 × 1.1) ÷ 1.0 = $32,142
```

---

## Step 6: Rank Opportunities

### Primary Sort: Weighted Score (Descending)

```
Sort all opportunities by Weighted_Score, highest first
```

### Tiebreaker Rules

**If two opportunities have same weighted score:**

1. **Higher base revenue wins**
2. **If still tied, earlier urgency deadline wins**
3. **If still tied, lower complexity wins**
4. **If still tied, alphabetical by client name**

---

## Step 7: Filter to Top 25

### Selection Process

1. Sort all opportunities by weighted score (descending)
2. Apply business rules:
   - One per client (select highest for each)
   - Concentration limits (max 8 of same type)
   - Minimum revenue threshold (typically $500)
3. Select top 25 after applying rules

### Minimum Revenue Threshold

**Purpose:** Exclude opportunities below advisor's engagement threshold

**Typical thresholds:**
- Solo advisor: $500 minimum
- Small team: $1,000 minimum
- Large practice: $2,000 minimum

**Adjustable based on:**
- Practice size
- Service model
- Relationship value

**Example:**
```
Set minimum_revenue = $500

Filter out any opportunities where Base_Revenue < $500
Then apply ranking and select Top 25
```

---

## Step 8: Format Report

### Standard Report Format

```
TOP 25 OPPORTUNITIES
Week of [Date]
Total Estimated Revenue: $[X]

RANK | CLIENT | OPPORTUNITY | REVENUE | URGENCY | ACTION
-----|---------|-------------|---------|---------|--------
1    | Martinez, Sofia | FIA Surrender Review | $24,350 | 2 months | Schedule review call
2    | Johnson, Robert | Life Insurance Gap | $18,500 | 30 days | Needs analysis meeting
3    | Chen, David | Tax Planning Package | $12,800 | 45 days | Tax projection meeting
...
25   | Wilson, Sarah | Cash Repositioning | $850 | Strategic | Brief call to discuss
```

### Detailed Report (Per Opportunity)

```
OPPORTUNITY #1 - Martinez, Sofia
Scenario: FIA-001 - Surrender Period Ending Review
Revenue Estimate: $24,350
Urgency: Near-term (Surrender ends in 2 months)

WHY IT'S AN OPPORTUNITY:
- Current FIA: $487,000 @ 4.2% cap
- Purchased: March 2019 (almost 7 years ago)
- Surrender period ends: February 28, 2026
- New products offering: 6.5-7.0% caps
- Income improvement: ~$11,000/year

MATCHING DATA:
- Product Type: Fixed Indexed Annuity
- Current Value: $487,000
- Purchase Date: 03/15/2019
- Current Cap Rate: 4.2%
- Surrender End: 02/28/2026 (60 days)
- Surrender Charge: 0% (past surrender period)

NEXT ACTIONS:
1. Pull current FIA statement
2. Run new product illustrations (3 carriers)
3. Calculate income improvement
4. Schedule 30-minute call with Sofia
5. Present comparison and options

TIMELINE: 30-60 days (before surrender period ends)
MEETING: One 30-minute call
PROFESSIONAL COORDINATION: None needed
```

---

## Edge Cases and Solutions

### Edge Case 1: Client Matches Too Many Scenarios

**Problem:** One client matches 10+ scenarios

**Solution:**
- Select top 3 by revenue
- Group into "Comprehensive Review" opportunity
- Revenue = Sum of top 3
- Action = Schedule comprehensive planning meeting

### Edge Case 2: Scenario Matches Too Many Clients

**Problem:** One scenario (e.g., Cash Drag) matches 40 clients

**Solution:**
- Apply stricter thresholds for this scenario
- Example: Increase minimum cash balance from $50K to $100K
- Or: Only include top 10 by revenue for this scenario
- Prevents one scenario from dominating Top 25

### Edge Case 3: Missing Critical Data

**Problem:** Can't calculate revenue without missing data

**Solutions:**
- **Option A:** Flag as "Data Needed" and rank lower
- **Option B:** Use scenario average as estimate
- **Option C:** Exclude from Top 25 until data obtained

**Recommended:** Option A with note: "Revenue estimate pending [data needed]"

### Edge Case 4: Seasonal Scenarios

**Problem:** Some scenarios only apply at certain times

**Example:** Tax loss harvesting only in Q4/Q1

**Solution:**
- Tag scenarios with seasonality
- Auto-activate/deactivate based on date
- Q4: Activate tax loss harvesting scenarios
- Q1: Deactivate tax scenarios, activate RMD planning

### Edge Case 5: Relationship-Based Exclusions

**Problem:** Scenario matches but relationship dynamics make it inappropriate

**Example:** Client is upset about recent poor performance

**Solution:**
- Add "Client_Status" or "Relationship_Health" field
- Exclude matches where Client_Status = "Needs attention" or "Service issue"
- Address relationship first, then revisit opportunities

---

## Quality Control Checks

### Before Finalizing Top 25

**Run these validation checks:**

1. **Sanity Check Revenue Estimates**
   - Are any estimates obviously wrong? ($1M commission on $10K product?)
   - Review outliers (top 3 and bottom 3)

2. **Verify Urgency Claims**
   - Do urgent opportunities actually have deadlines?
   - Check dates are future, not past

3. **Check for Duplicates**
   - Same client appearing multiple times? (should only be once)
   - Similar opportunities for different clients? (may be valid)

4. **Validate Matching Logic**
   - Spot-check 5 random matches
   - Pull actual client data and verify criteria are met
   - Any false positives?

5. **Review Exclusions**
   - Did any exclusions fail to apply when they should have?
   - Any matches that advisor would immediately reject?

6. **Concentration Review**
   - Is Top 25 too concentrated in one scenario type?
   - Good distribution across product types?

7. **Actionability Check**
   - Can advisor actually act on these THIS WEEK?
   - Any scenarios requiring data/prep advisor doesn't have?

---

## Continuous Improvement

### Track Performance Metrics

**For each opportunity presented:**

1. **Was it acted upon?** (Yes/No)
2. **Revenue generated?** (Actual vs. estimated)
3. **False positive?** (Matched but not actually appropriate)
4. **Data accuracy?** (Estimates accurate or way off?)

**Aggregate metrics:**
- Conversion rate (% of Top 25 that become actions)
- Revenue accuracy (avg % difference between estimated and actual)
- False positive rate (% of matches that advisor rejects)
- Time to action (how long until advisor acts?)

### Refinement Loop

**Monthly review:**
- Which scenarios generated most revenue? (Do more of these)
- Which had highest false positive rate? (Tighten criteria)
- Which had best conversion? (Lower thresholds to find more)
- Which never convert? (Consider retiring)

**Quarterly review:**
- Update revenue formulas based on actual results
- Adjust urgency and complexity weights
- Add new scenarios, retire underperformers
- Refine matching criteria

---

## Advanced Matching Techniques

### Fuzzy Matching

**For scenarios with soft criteria:**

Instead of hard cutoffs, use ranges with scoring:

**Example: Cash Balance Threshold**

Hard cutoff:
```
Cash_Balance > $50,000 → Include
Cash_Balance ≤ $50,000 → Exclude
```

Fuzzy matching:
```
Cash_Balance > $100,000 → Score 1.0
Cash_Balance $75,000-$100,000 → Score 0.8
Cash_Balance $50,000-$75,000 → Score 0.6
Cash_Balance < $50,000 → Score 0.0 (exclude)

Apply score as multiplier to revenue
```

**Benefit:** Captures gradations, not just binary yes/no

### Predictive Scoring (Advanced)

**If you have historical data:**

Train a model to predict:
- Likelihood of client accepting recommendation
- Probability of generating revenue
- Expected revenue (not just formula-based)

**Factors to consider:**
- Client communication frequency
- Past acceptance rate
- Relationship tenure
- Household complexity
- Prior similar opportunities

**Use predictions to adjust weighted scores**

### Multi-Scenario Patterns

**Look for clients who match multiple complementary scenarios:**

**Example pattern:**
```
Client matches:
- FIA-001 (Surrender ending)
- TAX-001 (Tax loss harvesting)
- DIV-002 (Sector overweight)

Pattern: "Comprehensive portfolio review" opportunity
Combined revenue > sum of parts
```

**Implementation:**
- Define common patterns
- Detect when client matches pattern
- Group as single "comprehensive" opportunity
- Adjust revenue upward (efficiency bonus)

---

## Matching Workflow Summary

```
START
  ↓
Load Client Data
  ↓
Load Scenario Library
  ↓
FOR EACH Scenario:
  ↓
  FOR EACH Client:
    ↓
    Apply Matching Criteria
      ↓
      If Match → Create Match Record
      ↓
      Check Exclusions
      ↓
      If Not Excluded → Calculate Revenue
      ↓
      Calculate Weighted Score
    ↓
  NEXT Client
  ↓
NEXT Scenario
  ↓
Sort All Matches by Weighted Score
  ↓
Apply Business Rules:
  - One per client
  - Concentration limits
  - Minimum thresholds
  ↓
Select Top 25
  ↓
Format Report
  ↓
Quality Control Review
  ↓
DELIVER TO ADVISOR
  ↓
END
```

---

This methodology ensures systematic, repeatable opportunity identification with minimal false positives and maximum advisor efficiency.
