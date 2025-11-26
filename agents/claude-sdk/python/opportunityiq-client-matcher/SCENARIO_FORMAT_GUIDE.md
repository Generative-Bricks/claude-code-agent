# Scenario Format Guide

## Overview
This guide explains the correct JSON format for OpportunityIQ scenario files.

---

## Key Changes Made

### 1. Operator Abbreviations

**Old (Verbose):**
```json
"operator": "greater_than"
"operator": "less_than"
"operator": "greater_than_or_equal"
"operator": "less_than_or_equal"
```

**New (Abbreviated):**
```json
"operator": "gt"   // greater than
"operator": "lt"   // less than
"operator": "gte"  // greater than or equal
"operator": "lte"  // less than or equal
```

**Complete Operator List:**
- `gt` - Greater than
- `lt` - Less than
- `gte` - Greater than or equal
- `lte` - Less than or equal
- `eq` - Equals
- `contains` - String contains substring
- `in` - Value in list

---

### 2. Category Values

**Allowed Categories (Fixed List):**
```json
"category": "annuity"                 // FIA, annuity products
"category": "tax"                     // Tax planning, harvesting
"category": "rebalance"               // Portfolio rebalancing, cash management
"category": "alternative_investment"  // Alternatives, private equity
"category": "insurance"               // Life insurance, LTC
```

**What We Changed:**
- `"annuity_optimization"` → `"annuity"`
- `"cash_management"` → `"rebalance"`
- `"portfolio_diversification"` → `"rebalance"`

---

### 3. Revenue Formula Structure

**Required Fields:**
```json
"revenue_formula": {
  "formula_type": "percentage",     // REQUIRED: Type of calculation
  "base_rate": 0.01,                // REQUIRED: Base rate (1% = 0.01)
  "multiplier_field": "fia_value",  // OPTIONAL: Field to multiply rate by
  "min_revenue": 500,               // OPTIONAL: Minimum revenue threshold
  "max_revenue": 50000              // OPTIONAL: Maximum revenue cap
}
```

**Formula Types:**
1. **percentage** - Multiply base_rate by multiplier_field
   ```json
   {
     "formula_type": "percentage",
     "base_rate": 0.01,              // 1%
     "multiplier_field": "fia_value",
     "min_revenue": 500,
     "max_revenue": 50000
   }
   // Calculation: fia_value × 0.01 = revenue
   // Example: $250,000 × 0.01 = $2,500
   ```

2. **flat_fee** - Fixed dollar amount
   ```json
   {
     "formula_type": "flat_fee",
     "base_rate": 2500              // Fixed $2,500
   }
   // Calculation: Always $2,500 regardless of client data
   ```

3. **aum_based** - Percentage of assets under management
   ```json
   {
     "formula_type": "aum_based",
     "base_rate": 0.01,              // 1% annual fee
     "multiplier_field": "portfolio_value"
   }
   // Calculation: portfolio_value × 0.01 = annual fee
   // Example: $500,000 × 0.01 = $5,000/year
   ```

4. **tiered** - Different rates for different amounts
   ```json
   {
     "formula_type": "tiered",
     "base_rate": 0.01,              // Default rate if no tiers match
     "multiplier_field": "portfolio_value",
     "tiers": {
       "0-500000": 0.0075,           // 0.75% on first $500k
       "500000-1000000": 0.005,      // 0.50% on $500k-$1M
       "1000000+": 0.0025            // 0.25% on amounts over $1M
     }
   }
   // Calculation: Apply rates to ranges, sum total
   ```

---

## Complete Example: FIA Replacement Scenario

```json
{
  "scenario_id": "FIA-001",
  "name": "FIA Replacement Opportunity",
  "description": "Identify clients with Fixed Indexed Annuities where surrender period is ending and current rates are below market",

  "category": "annuity",

  "criteria": [
    {
      "field": "fia_surrender_end_months",
      "operator": "lte",
      "value": 12,
      "weight": 1.0
    },
    {
      "field": "fia_current_cap_rate",
      "operator": "lt",
      "value": 5.5,
      "weight": 0.8
    },
    {
      "field": "fia_value",
      "operator": "gt",
      "value": 50000,
      "weight": 0.6
    }
  ],

  "revenue_formula": {
    "formula_type": "percentage",
    "base_rate": 0.01,
    "multiplier_field": "fia_value",
    "min_revenue": 500,
    "max_revenue": 50000
  },

  "priority": "medium"
}
```

**What This Scenario Does:**

1. **Matches clients who:**
   - Have FIA surrender ending ≤ 12 months (`lte` = less than or equal)
   - Have current cap rate < 5.5% (`lt` = less than)
   - Have FIA value > $50,000 (`gt` = greater than)

2. **Calculates revenue:**
   - Take `fia_value` × `0.01` (1%)
   - Minimum revenue: $500
   - Maximum revenue: $50,000
   - Example: $250,000 FIA × 1% = $2,500

3. **Weights criteria:**
   - Surrender ending soon: 1.0 (most important)
   - Low cap rate: 0.8 (important)
   - FIA value: 0.6 (least important)

**Match Score Calculation:**
```
Match Score = (Σ weighted matches) / (Σ all weights) × 100

If all 3 criteria match:
  Score = (1.0 + 0.8 + 0.6) / (1.0 + 0.8 + 0.6) × 100 = 100%

If only first 2 match:
  Score = (1.0 + 0.8) / (1.0 + 0.8 + 0.6) × 100 = 75%
```

---

## Field Reference

### Criteria Fields

**field** - Client profile field to check:
- Demographics: `age`, `state`, `risk_tolerance`, `marital_status`
- Portfolio: `portfolio_value`, `cash_balance`, `cash_percentage`, `cash_yield`
- Holdings: `largest_position_pct`, `fia_value`, `fia_current_cap_rate`
- Timing: `fia_surrender_end_months`

**operator** - How to compare (see Operator List above)

**value** - What to compare against:
- Numbers: `50000`, `5.5`, `20.0`
- Strings: `"conservative"`, `"married"`
- Lists: `["conservative", "moderate"]`

**weight** - Importance (0.0 to 1.0):
- `1.0` = Critical criterion
- `0.8` = Important
- `0.5` = Moderate importance
- `0.3` = Nice to have

---

## Validation Checklist

Before using a scenario file, verify:

- [ ] `scenario_id` is unique (e.g., "FIA-001")
- [ ] `category` is one of: annuity, tax, rebalance, alternative_investment, insurance
- [ ] All `operator` values use abbreviations (gt, lt, gte, lte, eq, contains, in)
- [ ] `revenue_formula` has `formula_type` and `base_rate`
- [ ] `multiplier_field` exists in client profile data
- [ ] `weight` values are between 0.0 and 1.0
- [ ] At least one criterion is defined

---

## Creating New Scenarios

### Template:

```json
{
  "scenario_id": "XXX-001",
  "name": "Descriptive Name",
  "description": "What this opportunity is and why it matters",
  "category": "annuity|tax|rebalance|alternative_investment|insurance",

  "criteria": [
    {
      "field": "client_field_name",
      "operator": "gt|lt|gte|lte|eq|contains|in",
      "value": 0,
      "weight": 1.0
    }
  ],

  "revenue_formula": {
    "formula_type": "percentage|flat_fee|aum_based|tiered",
    "base_rate": 0.01,
    "multiplier_field": "field_name",
    "min_revenue": 100,
    "max_revenue": 10000
  },

  "priority": "high|medium|low",
  "estimated_time_hours": 1.0,
  "required_licenses": ["Series 7"],
  "compliance_notes": "Important compliance considerations"
}
```

### Steps:

1. **Define the opportunity** - What action can the advisor take?
2. **Identify target clients** - Who is this for?
3. **Write matching criteria** - How do you find them systematically?
4. **Calculate revenue** - What's the economic potential?
5. **Test with sample data** - Validate it works correctly

---

## Common Mistakes

### ❌ Wrong: Verbose operator names
```json
"operator": "greater_than"
```

### ✅ Correct: Abbreviated operators
```json
"operator": "gt"
```

---

### ❌ Wrong: Custom category
```json
"category": "cash_management"
```

### ✅ Correct: Use allowed category
```json
"category": "rebalance"
```

---

### ❌ Wrong: Missing base_rate
```json
"revenue_formula": {
  "formula_type": "percentage",
  "multiplier_field": "fia_value"
}
```

### ✅ Correct: Include base_rate
```json
"revenue_formula": {
  "formula_type": "percentage",
  "base_rate": 0.01,
  "multiplier_field": "fia_value"
}
```

---

## Testing Scenarios

```bash
# Load and validate scenarios
uv run python -c "from src.tools import load_all_scenario_files; \
scenarios = load_all_scenario_files('data/scenarios'); \
print(f'Loaded {len(scenarios)} valid scenarios')"

# Test full workflow
uv run python test_workflow.py
```

---

*Last updated: 2025-11-21*
*Version: 1.0.0*
