# Product & Carrier Reference System

## Purpose
Maintain standardized, reusable reference tables for insurance products, carriers, and investment vehicles to ensure consistency across scenario matching and reporting.

---

## Why This Matters

### Problem Without Reference Tables
```
// Data variations across sources:
Client 1: Product = "Allianz 222"
Client 2: Product = "allianz 222"
Client 3: Product = "Allianz Index Advantage 222"
Client 4: Product = "222"

// Scenario matching fails due to inconsistency
```

### Solution With Reference Tables
```
// All variants mapped to standard reference
Product_Code: "ALL-222"
Product_Name_Standard: "Allianz Index Advantage 222"
Carrier_Standard: "Allianz Life Insurance Company"
Product_Type: "Fixed Indexed Annuity"
```

---

## Reference Table Structures

### Table 1: Insurance Carriers

**Purpose**: Standardize carrier names and track key details

```
| Carrier_ID | Carrier_Name_Standard              | Carrier_Short_Name | Carrier_Type     | AM_Best_Rating | States_Licensed | Active | Notes                           |
|------------|------------------------------------|--------------------|------------------|----------------|-----------------|--------|---------------------------------|
| ALL        | Allianz Life Insurance Company     | Allianz            | Life & Annuity   | A+             | All 50          | Yes    | Major FIA provider              |
| NW         | Nationwide Life Insurance Company  | Nationwide         | Life & Annuity   | A+             | All 50          | Yes    | Strong FIA and life portfolios  |
| AXA        | AXA Equitable Life Insurance Co    | AXA Equitable      | Life & Annuity   | A               | All 50          | Yes    | Variable annuity focus          |
| PACI       | Pacific Life Insurance Company     | Pacific Life       | Life & Annuity   | A+             | All 50          | Yes    | Diverse product line            |
| LSW        | LSW Life Insurance Company         | LSW                | Life             | A              | 47 states       | Yes    | Formerly Great Western          |
```

**Fields:**
- **Carrier_ID**: Short code (2-6 characters) for internal use
- **Carrier_Name_Standard**: Full legal name
- **Carrier_Short_Name**: Common name for client communications
- **Carrier_Type**: Life Only, Annuity Only, Life & Annuity, P&C
- **AM_Best_Rating**: Current financial strength rating
- **States_Licensed**: "All 50" or list of states
- **Active**: Yes/No - Currently writing business
- **Notes**: Key information about carrier

**Usage in Scenarios:**
```
Matching Criteria:
  Carrier IN (carrier_reference[carrier_reference.Active == 'Yes'].Carrier_ID)
  
Exclusion Rules:
  Exclude if Carrier = carrier_reference[carrier_reference.AM_Best_Rating < 'A'].Carrier_ID
```

---

### Table 2: Fixed Indexed Annuity Products

**Purpose**: Track FIA product details for comparison and replacement analysis

```
| Product_ID | Carrier_ID | Product_Name                | Launch_Date | Surrender_Years | Current_Cap_Range | Participation_Range | Income_Rider_Available | Product_Status | Notes                          |
|------------|------------|-----------------------------| ------------|-----------------|-------------------|---------------------|------------------------|----------------|--------------------------------|
| ALL-222    | ALL        | Allianz Index Advantage 222 | 2018-01-01  | 7               | 4.5% - 5.5%      | 100%                | Yes                    | Active         | Popular product, wide adoption |
| NW-PEAK10  | NW         | Nationwide Peak 10          | 2019-06-01  | 10              | 5.0% - 6.5%      | 110%                | Yes                    | Active         | Higher participation rates     |
| AXA-EQU    | AXA        | AXA Equitable Accumulator   | 2017-03-15  | 7               | 4.0% - 5.0%      | 95%                 | No                     | Discontinued   | Replaced by new version        |
| PACI-SEL   | PACI       | Pacific Life Index Selector | 2020-09-01  | 6               | 5.5% - 7.0%      | 105%                | Yes                    | Active         | Shorter surrender, higher caps |
```

**Fields:**
- **Product_ID**: Carrier prefix + product code
- **Carrier_ID**: Links to carrier table
- **Product_Name**: Official product name
- **Launch_Date**: When product became available
- **Surrender_Years**: Length of surrender period
- **Current_Cap_Range**: Current market cap rates (updated periodically)
- **Participation_Range**: Current participation rates
- **Income_Rider_Available**: Yes/No/Optional
- **Product_Status**: Active, Discontinued, Legacy (grandfathered)
- **Notes**: Key selling points or considerations

**Usage in Scenarios:**
```
Scenario: FIA Replacement Analysis
Logic:
  1. Find client's current FIA product
  2. Join to product_reference on Product_ID
  3. Compare client's cap rate to Current_Cap_Range
  4. Flag if client's rate < min(Current_Cap_Range) for similar products
  
  If Current_Product.Cap_Rate < Product_Reference[
      Product_Reference.Product_Status == 'Active' AND
      Product_Reference.Surrender_Years == Current_Product.Surrender_Years
  ].Current_Cap_Range.min() → Flag for review
```

---

### Table 3: Life Insurance Products

**Purpose**: Track life insurance product details

```
| Product_ID | Carrier_ID | Product_Name               | Product_Type       | Launch_Date | Underwriting_Type | Cash_Value | Product_Status | Target_Market    | Notes                        |
|------------|------------|----------------------------|--------------------| ------------|-------------------|------------|----------------|------------------|------------------------------|
| ALL-LIFP   | ALL        | Allianz Life Pro+          | Indexed UL         | 2019-01-01  | Full Medical      | Yes        | Active         | HNW, Business    | Strong cash accumulation     |
| NW-YRT     | NW         | Nationwide YRT Term        | Term Life          | 2018-06-01  | Simplified Issue  | No         | Active         | Mass Market      | Quick issue process          |
| PACI-VUL   | PACI       | Pacific Life VUL Protector | Variable UL        | 2020-03-15  | Full Medical      | Yes        | Active         | Sophisticated    | Investment options           |
| LSW-WL     | LSW        | LSW Whole Life Guaranteed  | Whole Life         | 2017-09-01  | Full Medical      | Yes        | Active         | Estate Planning  | Guaranteed death benefit     |
```

**Fields:**
- **Product_ID**: Carrier prefix + product code
- **Carrier_ID**: Links to carrier table
- **Product_Name**: Official product name
- **Product_Type**: Term, Whole Life, Universal Life, Indexed UL, Variable UL
- **Launch_Date**: When product became available
- **Underwriting_Type**: Full Medical, Simplified Issue, Guaranteed Issue
- **Cash_Value**: Yes/No
- **Product_Status**: Active, Discontinued, Legacy
- **Target_Market**: Who the product is designed for
- **Notes**: Key features or benefits

---

### Table 4: Variable Annuity Products

**Purpose**: Track VA product details and features

```
| Product_ID | Carrier_ID | Product_Name          | Launch_Date | Investment_Options | GLWB_Available | GMDB_Available | Annual_Fee_Range | Product_Status | Notes                   |
|------------|------------|-----------------------|-------------|--------------------| ---------------|----------------|------------------|----------------|-------------------------|
| AXA-STRU   | AXA        | AXA Structured Capital| 2019-01-01  | 50+                | Yes            | Yes            | 1.25% - 1.75%    | Active         | Buffered downside       |
| NW-ADVI    | NW         | Nationwide Advisory VUL| 2018-06-01 | 40+                | Yes            | No             | 0.95% - 1.45%    | Active         | Fee-based platform      |
| PACI-SEL   | PACI       | Pacific Select        | 2017-09-01  | 60+                | Yes            | Yes            | 1.50% - 2.00%    | Active         | Wide fund selection     |
```

---

### Table 5: Crediting Strategies

**Purpose**: Standardize how crediting methods are named and compared

```
| Strategy_ID | Strategy_Name_Standard       | Strategy_Type     | Common_Aliases                          | Typical_Cap_Range | Typical_Part_Range | Risk_Level | Notes                              |
|-------------|------------------------------|-------------------|----------------------------------------|-------------------|--------------------| -----------|------------------------------------|
| PTP-1Y      | Point-to-Point Annual        | Annual            | Annual PTP, 1-Year PTP                 | 4.0% - 6.5%      | N/A                | Low        | Most common, simplest to explain   |
| MSUM-12     | Monthly Sum                  | Monthly           | Monthly Cap, 12-Month Sum              | 1.5% - 2.5%      | N/A                | Medium     | Caps monthly gains, sums over year |
| PART-1Y     | Annual Participation         | Participation     | Annual Participation, 1-Year Part Rate | N/A               | 40% - 120%         | Medium     | No cap, limited by participation   |
| PTP-2Y      | Point-to-Point Biennial      | Multi-year        | 2-Year PTP, Biennial                   | 8.0% - 14.0%     | N/A                | Medium-High| Higher caps, longer lock-in        |
```

**Usage:**
- Standardize strategy names across carriers
- Enable apples-to-apples comparisons
- Support illustrations and projections

---

## Name Mapping Tables

### Purpose: Handle Data Variations

**Carrier Name Variants**
```
| Name_Variant                      | Maps_To_Carrier_ID |
|-----------------------------------|--------------------|
| Allianz                           | ALL                |
| allianz                           | ALL                |
| Allianz Life                      | ALL                |
| Allianz Life Insurance Company    | ALL                |
| ALL                               | ALL                |
| Nationwide                        | NW                 |
| Nationwide Life                   | NW                 |
| NWLI                              | NW                 |
| NW                                | NW                 |
```

**Product Name Variants**
```
| Name_Variant           | Maps_To_Product_ID |
|------------------------|--------------------|
| Allianz 222            | ALL-222            |
| allianz 222            | ALL-222            |
| 222                    | ALL-222            |
| Index Advantage 222    | ALL-222            |
| Allianz Idx Adv 222    | ALL-222            |
| Peak 10                | NW-PEAK10          |
| Nationwide Peak        | NW-PEAK10          |
| NW Peak 10             | NW-PEAK10          |
```

**Usage:**
```python
# When loading client data
client_products['Carrier_Standard'] = client_products['Carrier_Raw'].map(
    carrier_variants.set_index('Name_Variant')['Maps_To_Carrier_ID']
)

client_products['Product_Standard'] = client_products['Product_Raw'].map(
    product_variants.set_index('Name_Variant')['Maps_To_Product_ID']
)

# Now you can match consistently
match = client_products.merge(
    product_reference,
    left_on='Product_Standard',
    right_on='Product_ID'
)
```

---

## Skill Concept: Reference Table Manager

### Skill Purpose
Automated maintenance and lookup of product/carrier reference data

### Skill Functions

**Function 1: Standardize Product Name**
```
Input: "allianz 222", "All-222", "Index Advantage 222"
Output: {
  "Product_ID": "ALL-222",
  "Product_Name_Standard": "Allianz Index Advantage 222",
  "Carrier_ID": "ALL",
  "Carrier_Name": "Allianz Life Insurance Company"
}
```

**Function 2: Compare Product Features**
```
Input: Client's current product ID, List of alternative product IDs
Output: Side-by-side comparison table with:
  - Cap rates
  - Participation rates
  - Surrender periods
  - Fees
  - Riders
  - Crediting strategies
```

**Function 3: Find Similar Products**
```
Input: Product_ID, Criteria (same surrender length, similar cap, etc.)
Output: List of comparable products ranked by features
```

**Function 4: Market Comparison**
```
Input: Product_ID
Output: {
  "Current_Product_Cap": 4.5%,
  "Market_Average_Cap": 5.8%,
  "Market_Best_Cap": 7.0%,
  "Ranking": "Below Average",
  "Better_Alternatives": [product_list]
}
```

**Function 5: Update Market Rates**
```
Input: Product_ID, New_Cap_Range, New_Participation_Range, Date
Output: Updates reference table and logs change history
Purpose: Keep reference tables current with market changes
```

**Function 6: Validate Product Data**
```
Input: Client product data (raw from CRM)
Output: {
  "Matched": True/False,
  "Standardized_Product_ID": "ALL-222",
  "Confidence": "High/Medium/Low",
  "Suggested_Corrections": []
}
```

---

## Implementation Approach

### Phase 1: Build Static Reference Tables (Week 1-2)
1. Create carrier reference table
   - List all carriers you write with
   - Add key details (ratings, status, etc.)
   
2. Create product reference tables
   - FIA products (start with most common)
   - Life insurance products
   - Variable annuities if applicable
   
3. Create name mapping tables
   - Identify common variations from your CRM
   - Map to standard IDs

### Phase 2: Test with Client Data (Week 3)
1. Load sample client data
2. Apply standardization mappings
3. Identify gaps or unmapped values
4. Update mapping tables

### Phase 3: Build Skill (Week 4+)
1. Create skill with lookup functions
2. Add comparison logic
3. Integrate with scenario matching
4. Build update workflows

---

## Reference Table Templates

### Excel Structure

**Workbook: Product_Reference_Tables.xlsx**

**Sheet 1: Carriers**
- All carrier information
- Color coded by rating (green=A+, yellow=A, etc.)

**Sheet 2: FIA_Products**
- FIA product details
- Links to carrier sheet
- Current as of [date]

**Sheet 3: Life_Products**
- Life insurance products
- Links to carrier sheet

**Sheet 4: VA_Products**
- Variable annuity products
- Links to carrier sheet

**Sheet 5: Crediting_Strategies**
- Standardized crediting methods
- Aliases and comparisons

**Sheet 6: Carrier_Name_Mapping**
- All known variants → Standard ID

**Sheet 7: Product_Name_Mapping**
- All known variants → Standard Product ID

**Sheet 8: Update_Log**
- Date, What_Changed, Who_Updated, Notes
- Tracks changes over time

---

## Maintenance Schedule

### Monthly
- Review market cap/participation rates
- Update Current_Cap_Range and Participation_Range
- Add any new products launched
- Mark discontinued products

### Quarterly
- Review AM Best ratings
- Verify carrier status (still writing business?)
- Clean up mapping tables (add new variants found)
- Archive old products

### Annually
- Comprehensive review of all tables
- Remove obsolete products (not in any client portfolios)
- Update notes and target markets
- Validate all carrier information

---

## Integration with Scenario Matching

### Before Reference Tables
```
Scenario Matching Criteria:
"Product Type = 'FIA' AND Product Name contains 'Allianz'"

Problems:
- Misses "allianz", "ALL", "Allianz 222"
- Matches unintended products
- Can't compare features
```

### With Reference Tables
```
Scenario Matching Criteria:
"Product_ID IN (SELECT Product_ID FROM products WHERE Carrier_ID = 'ALL' AND Product_Type = 'FIA')"

OR with enriched data:
"Product_ID IN product_reference[product_reference.Current_Cap_Range.max() > 6.0].Product_ID"

Benefits:
- Consistent matching
- Feature-based filtering
- Market comparisons
- Automatic updates
```

---

## Sample Workflow

### Client Has FIA → Replacement Scenario

**Step 1: Standardize client data**
```
Client Raw Data: "Allianz 222 annuity"
After Mapping: Product_ID = "ALL-222"
```

**Step 2: Enrich with reference data**
```
Lookup Product_ID in reference table:
- Product_Name: "Allianz Index Advantage 222"
- Current_Cap_Range: "4.5% - 5.5%"
- Surrender_Years: 7
- Purchase_Date: 2019-04-15 (from client data)
```

**Step 3: Apply scenario logic**
```
IF (
  TODAY - Purchase_Date > 6 years AND
  Client_Cap_Rate < Product_Reference.Current_Cap_Range.min() AND
  Product_Status = 'Active'
) THEN Flag for replacement review
```

**Step 4: Find alternatives**
```
Query: FIA products with:
- Same Surrender_Years OR Surrender_Years - 2
- Current_Cap_Range.max() > Client_Cap_Rate
- Product_Status = 'Active'
- Carrier AM_Best_Rating >= 'A'

Returns: List of better alternatives with comparison
```

**Step 5: Generate recommendation**
```
Client: John Smith
Current Product: Allianz Index Advantage 222 (ALL-222)
Current Cap: 4.5%
Purchased: 2019-04-15 (6.5 years ago)

Better Alternatives:
1. Pacific Life Index Selector (PACI-SEL)
   - Cap: 5.5% - 7.0% (up to 2.5% higher)
   - Surrender: 6 years (1 year shorter)
   - Income Rider: Available
   
2. Nationwide Peak 10 (NW-PEAK10)
   - Cap: 5.0% - 6.5% (up to 2.0% higher)
   - Participation: 110% (better than current 100%)
   - Surrender: 10 years (note: longer commitment)
```

---

## Next Steps

1. **Review Concept**: Does this reference table approach make sense for your practice?

2. **Identify Starting Scope**: 
   - How many carriers do you work with regularly? (5? 10? 20?)
   - How many FIA products are in your book? (10? 25? 50?)
   - Do you need life insurance products in v1?

3. **Gather Product Data**:
   - Product names and codes
   - Current caps and participation rates
   - Surrender periods
   - Any other key features

4. **Build Initial Tables**:
   - I can create template spreadsheets
   - We'll populate with your top 10-20 products to start
   - Build mapping table from your CRM data variations

5. **Plan Skill Development**:
   - After manual tables proven
   - Build automated lookup and comparison skill
   - Integrate with scenario matching

Ready to start building these reference tables?
