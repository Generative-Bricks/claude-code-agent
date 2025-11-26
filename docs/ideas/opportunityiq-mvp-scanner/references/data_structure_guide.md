# Data Structure & Integration Guide

## Overview
Your data will come from multiple sources with varying structures, but all will share a common client identifier. This guide explains how to structure data for optimal scenario matching.

---

## Core Principle: Client-Centric Data Model

### The Hub-and-Spoke Model

**CLIENT (Hub)**
- Client ID (primary key)
- Name
- Age
- State
- Risk Tolerance
- Net Worth
- etc.

**PRODUCTS (Spoke 1)**
- Client ID (foreign key)
- Product ID
- Product Type
- Carrier
- Value
- Purchase Date
- etc.

**HOLDINGS (Spoke 2)**
- Client ID (foreign key)
- Position ID  
- Ticker
- Shares
- Cost Basis
- etc.

**ACCOUNTS (Spoke 3)**
- Client ID (foreign key)
- Account ID
- Account Type
- Balance
- Custodian
- etc.

### Key Concept
All data sources join on **Client ID**, allowing scenarios to pull information across multiple datasets.

---

## Expected Data Structures

### Structure 1: Annuity Products Sheet
```
| Client_ID | Client_Name | Product_Type | Carrier        | Product_Name | Purchase_Date | Current_Value | Surrender_End | Cap_Rate | Participation_Rate |
|-----------|-------------|--------------|----------------|--------------|---------------|---------------|---------------|----------|-------------------|
| 12345     | John Smith  | FIA          | Allianz        | Allianz 222  | 2019-04-15    | 487000        | 2025-10-15    | 4.5%     | 85%               |
| 12345     | John Smith  | FIA          | Nationwide     | Peak 10      | 2021-06-01    | 125000        | 2028-06-01    | 5.2%     | 100%              |
| 23456     | Jane Doe    | Variable Ann | AXA            | AXA Equitable| 2018-03-10    | 312000        | 2025-03-10    | N/A      | N/A               |
```

**Key Features:**
- One row per product
- Client ID on every row
- Client name included for human readability
- Product-specific fields populated

**Matching Example:**
```
Scenario: FIA Approaching Surrender End
Logic: 
  Find all rows where:
    - Product_Type = "FIA"
    - Surrender_End between TODAY and TODAY + 12 months
    - Cap_Rate < 5.5% (market threshold)
  
  Returns: Client 12345, Allianz 222 product
```

---

### Structure 2: Portfolio Holdings Sheet
```
| Client_ID | Account_ID | Account_Type | Ticker | Position_Name           | Shares | Cost_Basis | Current_Value | Unrealized_GL | Sector      |
|-----------|------------|--------------|--------|------------------------|--------|------------|---------------|---------------|-------------|
| 12345     | 555-001    | Taxable      | AAPL   | Apple Inc             | 500    | 75000      | 95000         | 20000         | Technology  |
| 12345     | 555-001    | Taxable      | MSFT   | Microsoft Corp        | 300    | 85000      | 125000        | 40000         | Technology  |
| 12345     | 555-002    | IRA          | VTI    | Vanguard Total Market | 1000   | 180000     | 195000        | 15000         | Diversified |
| 23456     | 666-001    | Taxable      | TSLA   | Tesla Inc             | 200    | 150000     | 48000         | -102000       | Auto        |
```

**Key Features:**
- Multiple rows per client (one per position)
- Account ID links positions to accounts
- Position-level detail enables sophisticated analysis

**Matching Example:**
```
Scenario: Concentrated Portfolio
Logic:
  1. Group by Client_ID
  2. Calculate: Position_Value / Sum(All_Positions_Value)
  3. Find: Any single position > 20% of total portfolio
  
  Returns: Client 23456 if TSLA represents >20% of total holdings
```

---

### Structure 3: Client Master Sheet
```
| Client_ID | First_Name | Last_Name | Age | State | Net_Worth | Liquid_Net_Worth | Risk_Tolerance | Life_Stage    | Accredited_Investor |
|-----------|------------|-----------|-----|-------|-----------|------------------|----------------|---------------|---------------------|
| 12345     | John       | Smith     | 68  | TX    | 2500000   | 1800000          | Moderate       | Early Retiree | Yes                 |
| 23456     | Jane       | Doe       | 45  | CA    | 850000    | 600000           | Aggressive     | Peak Earning  | No                  |
| 34567     | Bob        | Johnson   | 72  | FL    | 1200000   | 950000           | Conservative   | Established   | Yes                 |
```

**Key Features:**
- One row per client
- Demographic and planning data
- Used for filtering and segmentation

**Matching Example:**
```
Scenario: Alternative Investment Diversification
Logic:
  Join Holdings to Client Master on Client_ID
  Filter:
    - Concentration > 20% (from Holdings)
    - Accredited_Investor = "Yes" (from Client Master)
    - Liquid_Net_Worth > 250000 (from Client Master)
  
  Returns: Client 12345 (meets all criteria)
```

---

### Structure 4: Account Summary Sheet
```
| Client_ID | Account_ID | Account_Type     | Custodian | Balance  | Owner      | Beneficiary    | RMD_Required | Last_Distribution_Date |
|-----------|------------|------------------|-----------|----------|------------|----------------|--------------|------------------------|
| 12345     | 555-001    | Joint Taxable    | Schwab    | 450000   | Joint      | Trust          | No           | N/A                    |
| 12345     | 555-002    | Traditional IRA  | Schwab    | 875000   | John Smith | Spouse         | No           | N/A                    |
| 34567     | 777-001    | Traditional IRA  | Schwab    | 620000   | Bob Johnson| Children       | Yes          | 2024-12-15             |
```

**Key Features:**
- Account-level metadata
- Links to holdings detail
- Tax treatment information

**Matching Example:**
```
Scenario: Roth Conversion Opportunity
Logic:
  Find accounts where:
    - Account_Type = "Traditional IRA"
    - RMD_Required = "No" (not yet 73)
    - Balance > 100000
  Join to Client Master:
    - Age between 59.5 and 72
  
  Returns: Client 12345, Account 555-002
```

---

## Data Relationship Diagram

```
CLIENT_MASTER (1)
    ├── Client_ID (PK)
    ├── Demographics
    └── Risk Profile
         |
         ├─── ACCOUNTS (Many)
         |       ├── Client_ID (FK)
         |       ├── Account_ID (PK)
         |       └── Account Details
         |            |
         |            └─── HOLDINGS (Many)
         |                    ├── Account_ID (FK)
         |                    ├── Position_ID (PK)
         |                    └── Position Details
         |
         ├─── PRODUCTS (Many)
         |       ├── Client_ID (FK)
         |       ├── Product_ID (PK)
         |       └── Product Details
         |
         └─── TRANSACTIONS (Many)
                 ├── Client_ID (FK)
                 ├── Transaction_ID (PK)
                 └── Transaction Details
```

---

## Scenario Matching Logic Patterns

### Pattern 1: Single-Source Match
**Scenario**: FIA Surrender Review
**Data Needed**: Products table only
```python
# Pseudo-code
products[
    (products.Product_Type == 'FIA') & 
    (products.Surrender_End < today + 12_months) &
    (products.Cap_Rate < market_threshold)
].Client_ID.unique()
```

### Pattern 2: Cross-Source Match
**Scenario**: Concentrated Position for HNW
**Data Needed**: Holdings + Client Master
```python
# Calculate concentration from holdings
concentrated = holdings.groupby('Client_ID').apply(
    lambda x: (x.Current_Value.max() / x.Current_Value.sum()) > 0.20
)

# Join with client criteria
eligible = concentrated[concentrated].merge(
    client_master[
        (client_master.Accredited_Investor == 'Yes') &
        (client_master.Liquid_Net_Worth > 250000)
    ],
    on='Client_ID'
)
```

### Pattern 3: Multi-Source Complex Match
**Scenario**: Year-End Tax Loss Harvesting + Roth Conversion
**Data Needed**: Holdings + Accounts + Client Master
```python
# Find unrealized losses in taxable accounts
losses = holdings[
    (holdings.Unrealized_GL < 0) &
    (holdings.Account_Type == 'Taxable')
]

# Check if they also have Traditional IRA
ira_accounts = accounts[
    (accounts.Account_Type == 'Traditional IRA') &
    (accounts.Balance > 100000)
]

# Join with client age requirements
eligible = losses.merge(ira_accounts, on='Client_ID').merge(
    client_master[
        (client_master.Age >= 59.5) & 
        (client_master.Age < 73)
    ],
    on='Client_ID'
)
```

### Pattern 4: Time-Series Match
**Scenario**: Portfolio Rebalancing Based on Drift
**Data Needed**: Holdings (current) + Target Allocation (stored)
```python
# Calculate current allocation
current_alloc = holdings.groupby(['Client_ID', 'Sector']).agg({
    'Current_Value': 'sum'
}).groupby(level=0).apply(lambda x: x / x.sum())

# Compare to target (from client_master or separate table)
drift = current_alloc.merge(target_allocation, on=['Client_ID', 'Sector'])
drift['Difference'] = abs(drift['Current_Pct'] - drift['Target_Pct'])

# Find clients with >5% drift in any sector
needs_rebalance = drift[drift.Difference > 0.05].Client_ID.unique()
```

---

## Handling Data Variations

### Challenge 1: Missing Fields
**Problem**: Not all clients have all data fields

**Solution**: Use null-safe logic
```python
# Instead of:
clients[clients.Risk_Tolerance == 'Aggressive']

# Use:
clients[clients.Risk_Tolerance.fillna('Unknown') == 'Aggressive']

# Or exclude nulls:
clients[clients.Risk_Tolerance.notna() & 
        (clients.Risk_Tolerance == 'Aggressive')]
```

### Challenge 2: Inconsistent Naming
**Problem**: "FIA" vs "Fixed Indexed Annuity" vs "Fixed Index Annuity"

**Solution**: Standardization mapping (this is where Product Reference Table helps)
```python
# Standardization mapping
product_type_map = {
    'FIA': 'Fixed Indexed Annuity',
    'Fixed Indexed Annuity': 'Fixed Indexed Annuity',
    'Fixed Index Annuity': 'Fixed Indexed Annuity',
    'SPIA': 'Single Premium Immediate Annuity',
    # etc.
}

products['Product_Type_Std'] = products['Product_Type'].map(product_type_map)
```

### Challenge 3: Multi-Row per Client
**Problem**: Some scenarios need client-level view, data is position-level

**Solution**: Aggregation with group-by
```python
# Roll up to client level
client_summary = holdings.groupby('Client_ID').agg({
    'Current_Value': 'sum',           # Total portfolio value
    'Unrealized_GL': 'sum',            # Total unrealized gains/losses
    'Position_Name': 'count',          # Number of positions
    'Sector': lambda x: x.value_counts().index[0]  # Most common sector
})
```

---

## MCP Server Integration (Future State)

### Current State
- Upload Google Sheets with client identifier in each row
- Multiple sheets for different data types
- Manual export/upload process

### Future State with MCP
- MCP server exposes unified client data API
- Real-time access to all client information
- Standardized query interface

### MCP Server Functions (to build)
```python
# Function 1: Get client profile
get_client_profile(client_id) -> {demographics, risk, planning_data}

# Function 2: Get client products
get_client_products(client_id, product_type=None) -> [{product1}, {product2}]

# Function 3: Get client holdings
get_client_holdings(client_id, account_id=None) -> [{position1}, {position2}]

# Function 4: Get client accounts
get_client_accounts(client_id, account_type=None) -> [{account1}, {account2}]

# Function 5: Search clients by criteria
search_clients(criteria_dict) -> [client_ids]

# Function 6: Scenario matching
match_scenario(scenario_id, client_ids=None) -> {client_id: match_details}
```

### Benefits of MCP Integration
1. **Real-time data** - No manual exports
2. **Consistent structure** - Standardized regardless of source
3. **Access control** - Secure, authenticated access
4. **Audit trail** - Track what data was accessed when
5. **Performance** - Optimized queries vs. full data dumps

---

## Recommended Data Structure for Initial Testing

### Option 1: Simple Flat File (Good for First 10 Scenarios)
Create one "Client Portfolio Summary" sheet:
```
| Client_ID | Name | Age | State | Total_AUM | Has_FIA | FIA_Surrender_Date | Has_Concentrated_Position | Taxable_Account_Balance | IRA_Balance | Risk_Tolerance |
```

**Pros:**
- Easy to create
- Quick to test scenarios
- All data in one place

**Cons:**
- Doesn't scale well
- Loses detail
- Hard to maintain

### Option 2: Normalized Structure (Recommended)
Separate sheets for different entity types:
1. **Clients** - One row per client (demographics)
2. **Products** - One row per product (annuities, life insurance)
3. **Accounts** - One row per account (IRAs, taxable, etc.)
4. **Holdings** - One row per position (stocks, bonds, funds)

**Pros:**
- Scales infinitely
- Maintains detail
- Mirrors actual database structure
- Prepares for MCP integration

**Cons:**
- More complex to set up initially
- Requires joins in matching logic

### Recommended Starting Point
Start with **Option 2** using Google Sheets with separate tabs:
- Tab 1: "Clients"
- Tab 2: "Annuity_Products"  
- Tab 3: "Life_Insurance_Products"
- Tab 4: "Investment_Accounts"
- Tab 5: "Investment_Holdings"

This structure will work for both your immediate testing AND scale to MCP server integration later.

---

## Data Quality Requirements

### Critical Fields (Must Have)
- Client_ID (unique identifier across ALL sheets)
- Client_Name (for human readability)
- Age or Date_of_Birth (many scenarios age-dependent)
- State (for state restrictions)

### High-Value Fields (Should Have)
- Product_Type (for product-specific scenarios)
- Purchase_Date (for time-based scenarios)
- Current_Value (for threshold-based scenarios)
- Account_Type (for tax-planning scenarios)
- Risk_Tolerance (for suitability)

### Nice-to-Have Fields
- Specific product names and carriers
- Detailed crediting rates and caps
- Cost basis information
- Transaction history
- Beneficiary information

---

## Next Steps

1. **Audit Your Data Sources**
   - List all systems that have client data
   - Identify what data is available in each
   - Note any gaps or missing fields

2. **Standardize Client ID**
   - Ensure consistent client identifier across all sources
   - Document ID format and rules
   - Create crosswalk if multiple ID systems exist

3. **Create Initial Test Dataset**
   - Export 10-20 clients with complete data
   - Structure using recommended normalized format
   - Include variety of scenarios (FIA holders, concentrated positions, etc.)

4. **Define Extraction Process**
   - How will you export from CRM?
   - What format (CSV, Excel, Google Sheets)?
   - How often will data be refreshed?

5. **Plan MCP Server**
   - After proving concept with manual uploads
   - Design API endpoints for each data type
   - Build authentication and access controls

---

## Questions to Answer

1. What is your primary client identifier? (Client ID, Account Number, SSN, custom ID?)

2. Which system is "source of truth" for different data types?
   - Demographics: CRM?
   - Products: Policy Admin System?
   - Holdings: Schwab?
   - Transactions: Schwab + Product carriers?

3. How frequently does data change?
   - Daily (holdings values)?
   - Weekly (transactions)?
   - Monthly (new products)?
   - Quarterly (client demographics)?

4. What's your initial test scope?
   - 10 clients, all data?
   - 100 clients, limited data?
   - All clients, specific data only?

Ready to start structuring your initial test dataset?
