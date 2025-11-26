# Expense Tracker Agent - Design Document

**Document Version**: 1.0.0
**Date**: 2025-01-24
**Status**: Design Complete / Ready for Implementation
**Author**: Claude (Agent Builder Skill)

---

## Executive Summary

**One-Sentence Description**: An AI-powered expense tracking agent that helps individuals manage business expenses through natural language, receipt scanning, and intelligent categorization.

**Problem Solved**: Tracking business expenses is tedious - manual entry, categorization, and report generation take valuable time away from actual work.

**Primary Users**: Freelancers, contractors, and small business owners tracking their own business expenses

**Value Delivered**:
- Natural language expense entry (no forms to fill)
- Automatic receipt data extraction
- Intelligent auto-categorization
- Quick access to spending insights and reports

---

## 1. Brainstorm Results

### 1.1 Problem Statement

Freelancers and small business owners need to track business expenses for tax purposes, budgeting, and financial management. Current solutions require manual data entry, tedious categorization, and often don't integrate well with conversational workflows. This agent enables natural, conversational expense tracking with intelligent automation.

### 1.2 Success Criteria

1. **Auto-categorization Accuracy**: 85%+ correct category suggestions
   - Measurement: Manual review of categorized expenses
   - Target: 85%+ accuracy
   - Timeframe: After initial training period (100 expenses)

2. **Entry Speed**: <5 seconds for natural language expense entry
   - Measurement: Time from input to confirmation
   - Target: <5 seconds
   - Timeframe: Day 1

3. **Receipt Processing**: <10 seconds for receipt OCR and data extraction
   - Measurement: Time from image submission to parsed data
   - Target: <10 seconds
   - Timeframe: Day 1

4. **Data Reliability**: Zero data loss, 100% persistence
   - Measurement: All expenses retrievable after entry
   - Target: 100%
   - Timeframe: Day 1

5. **Query Response**: <2 seconds for searches and summaries
   - Measurement: Time from query to response
   - Target: <2 seconds
   - Timeframe: Day 1

### 1.3 Acceptable Limitations

- **Single user**: No multi-user or sharing features (personal use)
- **English only**: Natural language processing in English only
- **Local storage**: SQLite database (no cloud sync in v1)
- **Basic OCR**: Receipt processing may struggle with handwritten or damaged receipts
- **No attachments**: Receipts stored as references, not embedded in database

### 1.4 Key Edge Cases

| Edge Case | How to Handle | Priority |
|-----------|--------------|----------|
| Ambiguous category | Ask user to confirm or choose from suggestions | High |
| Receipt image unreadable | Return partial data with confidence scores, ask for manual entry | High |
| Duplicate expense detection | Warn user of potential duplicate, allow override | Medium |
| Missing required fields | Prompt for specific missing information | High |
| Large CSV import | Process in batches, show progress | Medium |
| Date in past/future | Allow with confirmation, validate reasonable range | Low |

### 1.5 Technical Decisions

#### SDK Selection

**Selected**: Claude SDK (Python)

**Rationale**:
- Excellent reasoning for intelligent categorization
- Anthropic vision capabilities for receipt processing
- Python has superior data processing libraries (pandas, sqlite3)
- Pydantic for type-safe data validation
- Good image handling with PIL/Pillow

#### Language Selection

**Selected**: Python

**Rationale**:
- Built-in `sqlite3` module
- Excellent CSV handling with `csv` and `pandas`
- PIL/Pillow for image preprocessing
- Pydantic for data models
- Rich ecosystem for data analysis and reporting

#### Complexity Assessment

**Level**: Medium

**Metrics**:
- **Tools**: 7 tools
- **Subagents**: 0 (not needed)
- **Workflow Stages**: 4 stages
- **Development Time**: 15-20 hours

---

## 2. Design Specifications

### 2.1 Agent Persona

**Name**: Expense Tracker Agent

**Role**: Personal business expense management assistant

**Expertise**:
- **Expense Management**: Understanding of business expense categories and tax-deductible expenses
- **Data Extraction**: Parsing expense information from natural language and receipts
- **Financial Reporting**: Generating summaries and reports

**Communication Style**:
- **Tone**: Friendly, efficient, and helpful
- **Language**: Simple, conversational (not accounting jargon)
- **Personality**: Organized, reliable, proactive about clarifications

**Capabilities**:
✅ **Can**:
- Add expenses via natural language ("$45 lunch with client at Olive Garden")
- Extract data from receipt images
- Import expenses from CSV files
- Intelligently categorize expenses
- Search and filter expense history
- Generate spending summaries by category, time period
- Export data to CSV reports

❌ **Cannot**:
- Provide tax advice (only categorization)
- Access external bank accounts or APIs
- Process currencies other than USD (v1)
- Handle multi-user scenarios
- Sync to cloud services

**Limitations**:
- Categories are suggestions - user has final say
- Receipt OCR may require manual corrections
- Reports are data exports, not formatted financial statements

**Safety Constraints**:
- Never deletes expenses without explicit confirmation
- Always confirms before bulk operations (import, category changes)
- Warns about potential duplicates

### 2.2 Tool Specifications

---

#### Tool #1: add_expense

**Purpose**: Add a new expense via natural language or structured input

**When to use**: User wants to record an expense

**Input Schema** (Pydantic):
```python
class AddExpenseInput(BaseModel):
    """Input for adding a new expense"""

    # Natural language input (optional - will be parsed)
    description: Optional[str] = Field(
        None,
        description="Natural language expense description, e.g., '$50 lunch at Chipotle'"
    )

    # Structured input (optional - used if provided)
    amount: Optional[float] = Field(
        None,
        gt=0,
        description="Expense amount in USD"
    )
    vendor: Optional[str] = Field(
        None,
        min_length=1,
        description="Vendor/merchant name"
    )
    category: Optional[str] = Field(
        None,
        description="Expense category (will auto-suggest if not provided)"
    )
    date: Optional[str] = Field(
        None,
        description="Expense date (YYYY-MM-DD format, defaults to today)"
    )
    notes: Optional[str] = Field(
        None,
        description="Additional notes about the expense"
    )
    receipt_path: Optional[str] = Field(
        None,
        description="Path to receipt image (if available)"
    )

    @validator('date')
    def validate_date_format(cls, v):
        if v:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Date must be in YYYY-MM-DD format')
        return v
```

**Output Schema**:
```python
class AddExpenseOutput(BaseModel):
    success: bool
    data: Optional[ExpenseRecord] = None
    suggested_category: Optional[str] = None
    category_confidence: Optional[float] = None
    needs_confirmation: bool = False
    confirmation_prompt: Optional[str] = None
    error: Optional[str] = None

class ExpenseRecord(BaseModel):
    id: str
    amount: float
    vendor: str
    category: str
    date: str
    notes: Optional[str] = None
    receipt_path: Optional[str] = None
    created_at: str
```

**Error Conditions**:
| Error | Cause | Handling |
|-------|-------|----------|
| Missing amount | Can't parse amount from description | Ask user to specify amount |
| Invalid date | Date format wrong or unreasonable | Request valid date |
| Unknown category | Category not in standard list | Create as custom category |

**Example Usage**:

**Natural Language Input**:
```json
{
  "description": "$85.50 dinner with client John at Morton's Steakhouse"
}
```

**Output**:
```json
{
  "success": true,
  "data": {
    "id": "exp_20250124_001",
    "amount": 85.50,
    "vendor": "Morton's Steakhouse",
    "category": "Meals & Entertainment",
    "date": "2025-01-24",
    "notes": "Client: John",
    "created_at": "2025-01-24T14:30:00Z"
  },
  "suggested_category": "Meals & Entertainment",
  "category_confidence": 0.95,
  "needs_confirmation": false
}
```

**Structured Input**:
```json
{
  "amount": 299.99,
  "vendor": "Amazon",
  "category": "Office Supplies",
  "date": "2025-01-20",
  "notes": "Standing desk converter"
}
```

---

#### Tool #2: process_receipt

**Purpose**: Extract expense data from a receipt image using OCR

**When to use**: User uploads or references a receipt image

**Input Schema**:
```python
class ProcessReceiptInput(BaseModel):
    """Input for processing a receipt image"""

    image_path: str = Field(
        ...,
        description="Path to the receipt image file"
    )
    auto_add: bool = Field(
        default=False,
        description="Automatically add expense if extraction is confident"
    )
```

**Output Schema**:
```python
class ProcessReceiptOutput(BaseModel):
    success: bool
    extracted_data: Optional[ExtractedReceiptData] = None
    confidence: float = Field(
        description="Overall confidence score (0-1)"
    )
    needs_review: bool = Field(
        description="Whether extracted data needs human review"
    )
    expense_added: Optional[ExpenseRecord] = None
    error: Optional[str] = None

class ExtractedReceiptData(BaseModel):
    vendor: Optional[str] = None
    vendor_confidence: float = 0.0
    amount: Optional[float] = None
    amount_confidence: float = 0.0
    date: Optional[str] = None
    date_confidence: float = 0.0
    items: Optional[List[str]] = None
    suggested_category: Optional[str] = None
```

**Error Conditions**:
| Error | Cause | Handling |
|-------|-------|----------|
| File not found | Image path invalid | Return error, request valid path |
| Unreadable image | Low quality, damaged, or non-receipt | Return partial data with low confidence |
| Unsupported format | Not JPG, PNG, or PDF | Return error, list supported formats |

**Example Usage**:

**Input**:
```json
{
  "image_path": "/home/user/receipts/lunch_receipt.jpg",
  "auto_add": false
}
```

**Output**:
```json
{
  "success": true,
  "extracted_data": {
    "vendor": "Panera Bread",
    "vendor_confidence": 0.95,
    "amount": 18.45,
    "amount_confidence": 0.98,
    "date": "2025-01-24",
    "date_confidence": 0.90,
    "items": ["Turkey Sandwich", "Iced Tea", "Chips"],
    "suggested_category": "Meals & Entertainment"
  },
  "confidence": 0.94,
  "needs_review": false,
  "expense_added": null
}
```

---

#### Tool #3: import_expenses

**Purpose**: Bulk import expenses from a CSV file

**When to use**: User wants to import multiple expenses from a file

**Input Schema**:
```python
class ImportExpensesInput(BaseModel):
    """Input for importing expenses from CSV"""

    file_path: str = Field(
        ...,
        description="Path to CSV file"
    )
    date_column: str = Field(
        default="date",
        description="Name of date column in CSV"
    )
    amount_column: str = Field(
        default="amount",
        description="Name of amount column in CSV"
    )
    vendor_column: str = Field(
        default="vendor",
        description="Name of vendor column in CSV"
    )
    category_column: Optional[str] = Field(
        default=None,
        description="Name of category column (will auto-categorize if not provided)"
    )
    notes_column: Optional[str] = Field(
        default=None,
        description="Name of notes column"
    )
    skip_duplicates: bool = Field(
        default=True,
        description="Skip potential duplicate entries"
    )
    dry_run: bool = Field(
        default=True,
        description="Preview import without saving (recommended first)"
    )
```

**Output Schema**:
```python
class ImportExpensesOutput(BaseModel):
    success: bool
    total_rows: int
    imported: int
    skipped: int
    errors: int
    error_details: List[str] = []
    preview: Optional[List[ExpenseRecord]] = None  # For dry_run
    duplicates_found: int = 0
    dry_run: bool
```

**Example Usage**:

**Input** (Dry Run):
```json
{
  "file_path": "/home/user/expenses_2024.csv",
  "date_column": "Date",
  "amount_column": "Amount",
  "vendor_column": "Description",
  "dry_run": true
}
```

**Output**:
```json
{
  "success": true,
  "total_rows": 150,
  "imported": 0,
  "skipped": 3,
  "errors": 2,
  "error_details": [
    "Row 45: Invalid date format",
    "Row 89: Missing amount"
  ],
  "preview": [
    {"id": "preview_1", "amount": 45.00, "vendor": "Office Depot", ...},
    {"id": "preview_2", "amount": 120.00, "vendor": "Adobe", ...}
  ],
  "duplicates_found": 3,
  "dry_run": true
}
```

---

#### Tool #4: search_expenses

**Purpose**: Search and filter expense history

**When to use**: User wants to find specific expenses or browse history

**Input Schema**:
```python
class SearchExpensesInput(BaseModel):
    """Input for searching expenses"""

    query: Optional[str] = Field(
        None,
        description="Search query (searches vendor, notes, category)"
    )
    category: Optional[str] = Field(
        None,
        description="Filter by category"
    )
    vendor: Optional[str] = Field(
        None,
        description="Filter by vendor name (partial match)"
    )
    date_from: Optional[str] = Field(
        None,
        description="Start date (YYYY-MM-DD)"
    )
    date_to: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD)"
    )
    min_amount: Optional[float] = Field(
        None,
        ge=0,
        description="Minimum amount"
    )
    max_amount: Optional[float] = Field(
        None,
        ge=0,
        description="Maximum amount"
    )
    limit: int = Field(
        default=50,
        ge=1,
        le=500,
        description="Maximum results to return"
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Offset for pagination"
    )
    sort_by: Literal["date", "amount", "vendor", "category"] = Field(
        default="date",
        description="Sort field"
    )
    sort_order: Literal["asc", "desc"] = Field(
        default="desc",
        description="Sort order"
    )
```

**Output Schema**:
```python
class SearchExpensesOutput(BaseModel):
    success: bool
    expenses: List[ExpenseRecord]
    total_count: int
    total_amount: float
    has_more: bool
    query_summary: str
```

**Example Usage**:

**Input**:
```json
{
  "category": "Travel",
  "date_from": "2025-01-01",
  "date_to": "2025-01-31",
  "sort_by": "amount",
  "sort_order": "desc"
}
```

**Output**:
```json
{
  "success": true,
  "expenses": [
    {"id": "exp_001", "amount": 450.00, "vendor": "Delta Airlines", ...},
    {"id": "exp_002", "amount": 189.00, "vendor": "Marriott", ...}
  ],
  "total_count": 8,
  "total_amount": 1245.50,
  "has_more": false,
  "query_summary": "8 Travel expenses from Jan 2025 totaling $1,245.50"
}
```

---

#### Tool #5: get_summary

**Purpose**: Generate spending summaries by category, time period, or vendor

**When to use**: User wants to see spending analytics or totals

**Input Schema**:
```python
class GetSummaryInput(BaseModel):
    """Input for generating expense summaries"""

    period: Literal["day", "week", "month", "quarter", "year", "custom"] = Field(
        default="month",
        description="Time period for summary"
    )
    date_from: Optional[str] = Field(
        None,
        description="Start date for custom period (YYYY-MM-DD)"
    )
    date_to: Optional[str] = Field(
        None,
        description="End date for custom period (YYYY-MM-DD)"
    )
    group_by: Literal["category", "vendor", "day", "week", "month"] = Field(
        default="category",
        description="How to group the summary"
    )
    include_details: bool = Field(
        default=False,
        description="Include individual expense details"
    )
    top_n: Optional[int] = Field(
        None,
        ge=1,
        le=50,
        description="Limit to top N groups by amount"
    )
```

**Output Schema**:
```python
class GetSummaryOutput(BaseModel):
    success: bool
    summary: ExpenseSummary
    period_label: str
    generated_at: str

class ExpenseSummary(BaseModel):
    total_amount: float
    total_count: int
    groups: List[SummaryGroup]
    comparison: Optional[PeriodComparison] = None

class SummaryGroup(BaseModel):
    name: str
    amount: float
    count: int
    percentage: float
    expenses: Optional[List[ExpenseRecord]] = None  # If include_details

class PeriodComparison(BaseModel):
    previous_period_amount: float
    change_amount: float
    change_percentage: float
```

**Example Usage**:

**Input**:
```json
{
  "period": "month",
  "group_by": "category",
  "top_n": 5
}
```

**Output**:
```json
{
  "success": true,
  "summary": {
    "total_amount": 3250.75,
    "total_count": 45,
    "groups": [
      {"name": "Software & Subscriptions", "amount": 850.00, "count": 8, "percentage": 26.1},
      {"name": "Meals & Entertainment", "amount": 625.50, "count": 15, "percentage": 19.2},
      {"name": "Travel", "amount": 580.00, "count": 3, "percentage": 17.8},
      {"name": "Office Supplies", "amount": 445.25, "count": 12, "percentage": 13.7},
      {"name": "Professional Services", "amount": 350.00, "count": 2, "percentage": 10.8}
    ],
    "comparison": {
      "previous_period_amount": 2890.50,
      "change_amount": 360.25,
      "change_percentage": 12.5
    }
  },
  "period_label": "January 2025",
  "generated_at": "2025-01-24T15:00:00Z"
}
```

---

#### Tool #6: export_report

**Purpose**: Export expenses to CSV or formatted report

**When to use**: User wants to export data for records, taxes, or accounting

**Input Schema**:
```python
class ExportReportInput(BaseModel):
    """Input for exporting expense reports"""

    format: Literal["csv", "summary_csv", "detailed_csv"] = Field(
        default="csv",
        description="Export format"
    )
    date_from: Optional[str] = Field(
        None,
        description="Start date (YYYY-MM-DD)"
    )
    date_to: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD)"
    )
    categories: Optional[List[str]] = Field(
        None,
        description="Filter by specific categories"
    )
    output_path: Optional[str] = Field(
        None,
        description="Output file path (auto-generated if not provided)"
    )
    include_summary: bool = Field(
        default=True,
        description="Include summary section at top of report"
    )
```

**Output Schema**:
```python
class ExportReportOutput(BaseModel):
    success: bool
    file_path: str
    total_expenses: int
    total_amount: float
    date_range: str
    preview: Optional[str] = None  # First few lines of the export
    error: Optional[str] = None
```

**Example Usage**:

**Input**:
```json
{
  "format": "detailed_csv",
  "date_from": "2025-01-01",
  "date_to": "2025-01-31",
  "include_summary": true
}
```

**Output**:
```json
{
  "success": true,
  "file_path": "/home/user/expense_reports/expenses_2025-01.csv",
  "total_expenses": 45,
  "total_amount": 3250.75,
  "date_range": "2025-01-01 to 2025-01-31",
  "preview": "# Expense Report: January 2025\n# Total: $3,250.75 (45 expenses)\n\nDate,Vendor,Amount,Category,Notes\n2025-01-24,Morton's,85.50,Meals,Client dinner..."
}
```

---

#### Tool #7: manage_categories

**Purpose**: View, add, or modify expense categories

**When to use**: User wants to see available categories or add custom ones

**Input Schema**:
```python
class ManageCategoriesInput(BaseModel):
    """Input for managing expense categories"""

    action: Literal["list", "add", "rename", "merge"] = Field(
        default="list",
        description="Action to perform"
    )
    category_name: Optional[str] = Field(
        None,
        description="Category name (for add/rename/merge)"
    )
    new_name: Optional[str] = Field(
        None,
        description="New name (for rename)"
    )
    merge_into: Optional[str] = Field(
        None,
        description="Target category for merge"
    )
```

**Output Schema**:
```python
class ManageCategoriesOutput(BaseModel):
    success: bool
    categories: List[CategoryInfo]
    action_result: Optional[str] = None
    expenses_affected: int = 0

class CategoryInfo(BaseModel):
    name: str
    expense_count: int
    total_amount: float
    is_custom: bool
```

**Example Usage**:

**Input** (List):
```json
{
  "action": "list"
}
```

**Output**:
```json
{
  "success": true,
  "categories": [
    {"name": "Meals & Entertainment", "expense_count": 25, "total_amount": 1250.00, "is_custom": false},
    {"name": "Travel", "expense_count": 12, "total_amount": 2400.00, "is_custom": false},
    {"name": "Software & Subscriptions", "expense_count": 15, "total_amount": 890.00, "is_custom": false},
    {"name": "Office Supplies", "expense_count": 18, "total_amount": 450.00, "is_custom": false},
    {"name": "Professional Services", "expense_count": 5, "total_amount": 1500.00, "is_custom": false},
    {"name": "Contractor Equipment", "expense_count": 3, "total_amount": 750.00, "is_custom": true}
  ],
  "action_result": null
}
```

---

### 2.3 Workflow Design

**Overview**: Multi-stage conversational workflow that handles expense management requests

**Stages**: 4 main stages

**Progression**: Request-driven (user initiates each stage)

**State Management**: SQLite persistence

---

#### Stage 1: Request Understanding

**Purpose**: Parse and understand user's intent

**Trigger**: Any user message

**Activities**:
1. Analyze user input for intent (add, search, summarize, export, etc.)
2. Extract relevant parameters (amounts, dates, categories, etc.)
3. Determine which tool to invoke

**Information Collected**:
- User intent
- Extracted parameters
- Context from conversation

**Progression Condition**: Intent identified

**Error Handling**: Ask for clarification if intent unclear

---

#### Stage 2: Data Processing

**Purpose**: Execute requested operation

**Trigger**: Intent identified

**Activities**:
1. Validate input parameters
2. Invoke appropriate tool
3. Process results

**Tools Used**:
- All 7 tools depending on intent

**Progression Condition**: Tool execution complete

**Error Handling**: Return clear error message, suggest alternatives

---

#### Stage 3: Confirmation (when needed)

**Purpose**: Get user confirmation for sensitive operations

**Trigger**: Bulk operations, deletions, ambiguous categorization

**Activities**:
1. Present proposed action
2. Wait for user confirmation
3. Process confirmation

**Information Collected**:
- User confirmation
- Any corrections or adjustments

**Progression Condition**: User confirms or cancels

---

#### Stage 4: Response

**Purpose**: Present results to user

**Trigger**: Operation complete

**Activities**:
1. Format results for display
2. Provide relevant insights or suggestions
3. Ask if user needs anything else

---

### 2.4 Data Model

#### SQLite Schema

```sql
-- Expense categories (both default and custom)
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    is_custom BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Main expenses table
CREATE TABLE expenses (
    id TEXT PRIMARY KEY,
    amount REAL NOT NULL,
    vendor TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    date DATE NOT NULL,
    notes TEXT,
    receipt_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Receipt metadata (optional)
CREATE TABLE receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_id TEXT,
    file_path TEXT NOT NULL,
    original_filename TEXT,
    extracted_data TEXT,  -- JSON blob of OCR results
    confidence REAL,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (expense_id) REFERENCES expenses(id)
);

-- Indexes for common queries
CREATE INDEX idx_expenses_date ON expenses(date);
CREATE INDEX idx_expenses_category ON expenses(category_id);
CREATE INDEX idx_expenses_vendor ON expenses(vendor);
CREATE INDEX idx_expenses_amount ON expenses(amount);
```

#### Default Categories

```python
DEFAULT_CATEGORIES = [
    "Advertising & Marketing",
    "Bank Fees & Charges",
    "Conferences & Events",
    "Contractor Payments",
    "Education & Training",
    "Equipment & Hardware",
    "Insurance",
    "Internet & Phone",
    "Legal & Professional",
    "Meals & Entertainment",
    "Office Supplies",
    "Professional Services",
    "Rent & Utilities",
    "Software & Subscriptions",
    "Travel",
    "Vehicle & Transportation",
    "Other / Miscellaneous"
]
```

#### Entity Models

```python
class Expense(BaseModel):
    """Core expense entity"""
    id: str
    amount: float = Field(gt=0)
    vendor: str = Field(min_length=1)
    category: str
    date: date
    notes: Optional[str] = None
    receipt_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class Category(BaseModel):
    """Expense category"""
    id: int
    name: str = Field(min_length=1)
    is_custom: bool = False
    created_at: datetime

class Receipt(BaseModel):
    """Receipt metadata"""
    id: int
    expense_id: Optional[str] = None
    file_path: str
    original_filename: Optional[str] = None
    extracted_data: Optional[dict] = None
    confidence: Optional[float] = None
    processed_at: datetime
```

---

### 2.5 Pattern Selections

| Pattern | Category | Rationale |
|---------|----------|-----------|
| **Pydantic Validation** | Validation | Type-safe input/output validation for all tools |
| **Service-Based Architecture** | Architecture | Separate models, services, tools layers for testability |
| **Mock Data First** | Data Management | Enable development without real expenses |
| **Graceful Degradation** | Error Handling | Partial results better than complete failure |
| **Caching** | Performance | Cache category lookups and recent queries |

---

## 3. Technical Architecture

### 3.1 Project Structure

```
expense-tracker/
├── src/
│   ├── __init__.py
│   ├── main.py                    # Main agent configuration
│   ├── models/                    # Pydantic models
│   │   ├── __init__.py
│   │   ├── expense.py
│   │   ├── category.py
│   │   └── receipt.py
│   ├── services/                  # Business logic
│   │   ├── __init__.py
│   │   ├── expense_service.py
│   │   ├── category_service.py
│   │   ├── receipt_service.py
│   │   ├── import_service.py
│   │   └── report_service.py
│   ├── tools/                     # Agent tools
│   │   ├── __init__.py
│   │   ├── add_expense.py
│   │   ├── process_receipt.py
│   │   ├── import_expenses.py
│   │   ├── search_expenses.py
│   │   ├── get_summary.py
│   │   ├── export_report.py
│   │   └── manage_categories.py
│   ├── database/                  # Database layer
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── schema.py
│   │   └── migrations.py
│   └── utils/                     # Utilities
│       ├── __init__.py
│       ├── date_utils.py
│       └── categorization.py
├── tests/
│   ├── __init__.py
│   ├── test_tools/
│   │   ├── test_add_expense.py
│   │   ├── test_search_expenses.py
│   │   └── test_get_summary.py
│   ├── test_services/
│   │   └── test_expense_service.py
│   └── test_integration/
│       └── test_workflows.py
├── data/
│   ├── expenses.db               # SQLite database
│   └── mock/
│       └── sample_expenses.json  # Mock data
├── .claude/
│   └── CLAUDE.md
├── requirements.txt
├── pyproject.toml
├── .env.example
├── .gitignore
├── README.md
└── DESIGN.md                     # This file
```

### 3.2 Dependencies

```txt
# Core
anthropic>=0.18.0
pydantic>=2.6.0
python-dotenv>=1.0.0

# Database
# (sqlite3 is built-in)

# Data processing
pandas>=2.2.0

# Image processing (for receipts)
pillow>=10.2.0

# Development
pytest>=8.0.0
pytest-asyncio>=0.23.0
mypy>=1.8.0
```

### 3.3 Environment Configuration

```bash
# API Keys
ANTHROPIC_API_KEY=sk-ant-...

# Database
DATABASE_PATH=./data/expenses.db

# Configuration
USE_MOCK_DATA=false
LOG_LEVEL=info

# Receipts
RECEIPTS_DIR=./data/receipts
MAX_RECEIPT_SIZE_MB=10
```

---

## 4. Implementation Guidance

### 4.1 Implementation Sequence

1. **Project Setup** (30 mins)
   - Create directory structure
   - Setup virtual environment with uv
   - Install dependencies
   - Configure environment

2. **Database Layer** (1 hour)
   - Create schema.py with table definitions
   - Implement connection management
   - Create migration scripts
   - Seed default categories

3. **Models** (1 hour)
   - Implement Pydantic models
   - Add validators
   - Create model tests

4. **Services** (4 hours)
   - ExpenseService (CRUD operations)
   - CategoryService (category management)
   - ImportService (CSV processing)
   - ReportService (summaries, exports)

5. **Tools** (4 hours)
   - add_expense
   - search_expenses
   - get_summary
   - export_report
   - manage_categories
   - import_expenses

6. **Receipt Processing** (2 hours)
   - ReceiptService (OCR with Claude vision)
   - process_receipt tool
   - Image preprocessing

7. **Agent Configuration** (1 hour)
   - System prompt
   - Tool registration
   - Conversation flow

8. **Testing** (3 hours)
   - Unit tests for services
   - Unit tests for tools
   - Integration tests

9. **Documentation** (1 hour)
   - CLAUDE.md
   - README.md
   - Usage examples

**Total Estimated Time**: 17-20 hours

### 4.2 Critical Implementation Notes

1. **Receipt OCR**: Use Claude's vision capabilities with base64 encoded images
2. **Date Handling**: Always store dates as ISO format (YYYY-MM-DD)
3. **Amount Precision**: Use REAL type in SQLite, round to 2 decimal places in display
4. **Category Matching**: Use fuzzy matching for auto-categorization
5. **Duplicate Detection**: Check vendor + amount + date within 3 days
6. **CSV Import**: Validate structure before processing, support various column names

---

## 5. Testing Strategy

### 5.1 Unit Tests

| Component | Test Cases | Priority |
|-----------|------------|----------|
| add_expense | Valid input, missing fields, auto-categorization | High |
| search_expenses | Various filters, pagination, empty results | High |
| get_summary | Different periods, groupings, empty data | High |
| export_report | All formats, date ranges, file creation | Medium |
| import_expenses | Valid CSV, invalid format, duplicates | Medium |
| process_receipt | Valid image, unreadable, auto-add | Medium |
| manage_categories | List, add, rename, merge | Low |

### 5.2 Integration Tests

1. **Full Workflow**: Add expense → Search → Summarize → Export
2. **Import Workflow**: Import CSV → Verify data → Generate report
3. **Receipt Workflow**: Process receipt → Review → Add expense

### 5.3 Performance Targets

| Operation | Target |
|-----------|--------|
| Add expense | <2 seconds |
| Search (simple) | <1 second |
| Search (complex) | <2 seconds |
| Summary (month) | <2 seconds |
| Export (100 expenses) | <5 seconds |
| Receipt OCR | <10 seconds |
| CSV import (100 rows) | <10 seconds |

---

## 6. Future Enhancements (v2+)

### Version 1.1
- Budget tracking and alerts
- Recurring expense templates
- Receipt image storage in database
- Multi-currency support

### Version 2.0
- Cloud sync (optional)
- Mobile-friendly reports
- Bank statement import (OFX format)
- Tax category mapping
- Expense approval workflow

---

## Scaffolding Instructions

**Phase 2 Ready**: This design is complete and ready for scaffolding.

**Target Directory**: `agents/claude-sdk/python/expense-tracker/`

**To scaffold**:
1. Create directory structure per section 3.1
2. Generate database schema from section 2.4
3. Create tool files with input/output schemas from section 2.2
4. Setup testing structure

**What will be generated**:
- Complete directory structure
- Pydantic models
- Tool templates with validation
- Service stubs
- Database schema
- Test structure
- Documentation templates

**What you need to implement**:
- Service business logic
- Agent system prompt
- Receipt OCR integration
- Auto-categorization logic
- Test assertions

---

**End of Design Document**
