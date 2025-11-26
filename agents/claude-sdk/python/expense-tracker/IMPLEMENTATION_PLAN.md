# Expense Tracker Agent - Implementation Plan

**Version**: 1.0.0
**Date**: 2025-01-24
**Reference**: See DESIGN.md for complete specifications

---

## Execution Overview

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: Foundation Agent (Sequential - Must Run First)    │
│  Database + Models + Config                                 │
│  Estimated: 3 hours                                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┴─────────────────────┐
        ↓                                           ↓
┌───────────────────────┐              ┌───────────────────────┐
│  PHASE 2A: Core Ops   │              │  PHASE 2B: Advanced   │
│  Agent (Parallel)     │      ||      │  Features Agent       │
│  CRUD + Search        │              │  Import + Export      │
│  Estimated: 5 hours   │              │  Estimated: 6 hours   │
└───────────────────────┘              └───────────────────────┘
        └─────────────────────┬─────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 3: Orchestrator (Sequential - After Phase 2)         │
│  Main Agent + Integration Tests + Documentation             │
│  Estimated: 3 hours                                         │
└─────────────────────────────────────────────────────────────┘
```

**Total Time with Parallelization**: ~11 hours
**Total Time Sequential**: ~17 hours
**Time Savings**: ~35%

---

## Phase 1: Foundation Agent

**Agent Role**: Build the database layer, Pydantic models, and project configuration

**Must Complete Before**: Phase 2A and 2B can begin

**Estimated Time**: 3 hours

### Tasks

#### Task 1.1: Project Setup (30 minutes)

**Objective**: Create project structure and install dependencies

**Steps**:
1. Create directory structure:
   ```
   expense-tracker/
   ├── src/
   │   ├── __init__.py
   │   ├── models/
   │   │   └── __init__.py
   │   ├── services/
   │   │   └── __init__.py
   │   ├── tools/
   │   │   └── __init__.py
   │   ├── database/
   │   │   └── __init__.py
   │   └── utils/
   │       └── __init__.py
   ├── tests/
   │   ├── __init__.py
   │   ├── test_tools/
   │   │   └── __init__.py
   │   ├── test_services/
   │   │   └── __init__.py
   │   └── test_integration/
   │       └── __init__.py
   ├── data/
   │   └── mock/
   └── .claude/
   ```

2. Create virtual environment:
   ```bash
   cd agents/claude-sdk/python/expense-tracker
   uv venv
   source .venv/bin/activate  # or .venv/Scripts/activate on Windows
   ```

3. Create `requirements.txt`:
   ```txt
   anthropic>=0.18.0
   pydantic>=2.6.0
   python-dotenv>=1.0.0
   pandas>=2.2.0
   pillow>=10.2.0
   pytest>=8.0.0
   pytest-asyncio>=0.23.0
   ```

4. Create `.env.example`:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-...
   DATABASE_PATH=./data/expenses.db
   USE_MOCK_DATA=false
   LOG_LEVEL=info
   RECEIPTS_DIR=./data/receipts
   ```

5. Create `pyproject.toml` with project metadata

6. Create `.gitignore`:
   ```
   .venv/
   __pycache__/
   *.pyc
   .env
   data/expenses.db
   data/receipts/
   *.egg-info/
   ```

7. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

**Deliverables**:
- [ ] Complete directory structure created
- [ ] Virtual environment initialized
- [ ] Dependencies installed
- [ ] Configuration files in place

---

#### Task 1.2: Database Schema (45 minutes)

**Objective**: Create SQLite database schema and connection management

**File**: `src/database/schema.py`

**Implementation**:
```python
"""
Database schema definitions for expense tracker.

Tables:
- categories: Expense categories (default and custom)
- expenses: Main expense records
- receipts: Receipt metadata and OCR results
"""

SCHEMA = """
-- Expense categories (both default and custom)
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    is_custom BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Main expenses table
CREATE TABLE IF NOT EXISTS expenses (
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

-- Receipt metadata
CREATE TABLE IF NOT EXISTS receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_id TEXT,
    file_path TEXT NOT NULL,
    original_filename TEXT,
    extracted_data TEXT,
    confidence REAL,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (expense_id) REFERENCES expenses(id)
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date);
CREATE INDEX IF NOT EXISTS idx_expenses_category ON expenses(category_id);
CREATE INDEX IF NOT EXISTS idx_expenses_vendor ON expenses(vendor);
CREATE INDEX IF NOT EXISTS idx_expenses_amount ON expenses(amount);
"""

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

**File**: `src/database/connection.py`

**Implementation**:
```python
"""
Database connection management.

Provides:
- Connection pooling
- Transaction management
- Query execution helpers
"""
import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Generator
import os

from .schema import SCHEMA, DEFAULT_CATEGORIES


class DatabaseConnection:
    """SQLite database connection manager."""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or os.getenv("DATABASE_PATH", "./data/expenses.db")
        self._ensure_directory()
        self._initialized = False

    def _ensure_directory(self):
        """Create database directory if it doesn't exist."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    def initialize(self):
        """Initialize database schema and seed data."""
        if self._initialized:
            return

        with self.get_connection() as conn:
            conn.executescript(SCHEMA)

            # Seed default categories
            for category in DEFAULT_CATEGORIES:
                conn.execute(
                    "INSERT OR IGNORE INTO categories (name, is_custom) VALUES (?, ?)",
                    (category, False)
                )
            conn.commit()

        self._initialized = True

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Get database connection with context management."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def execute(self, query: str, params: tuple = ()) -> list:
        """Execute a query and return results."""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()

    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """Execute an insert and return last row id."""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.lastrowid


# Global database instance
db = DatabaseConnection()
```

**Deliverables**:
- [ ] `src/database/schema.py` - Schema definitions
- [ ] `src/database/connection.py` - Connection management
- [ ] `src/database/__init__.py` - Exports db instance
- [ ] Database initializes correctly with tables and indexes

---

#### Task 1.3: Pydantic Models (45 minutes)

**Objective**: Create all Pydantic models for data validation

**File**: `src/models/expense.py`

```python
"""Expense-related Pydantic models."""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


class ExpenseRecord(BaseModel):
    """Complete expense record from database."""
    id: str
    amount: float = Field(gt=0)
    vendor: str = Field(min_length=1)
    category: str
    date: date
    notes: Optional[str] = None
    receipt_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class AddExpenseInput(BaseModel):
    """Input for adding a new expense."""
    description: Optional[str] = Field(
        None,
        description="Natural language expense description"
    )
    amount: Optional[float] = Field(None, gt=0)
    vendor: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = None
    date: Optional[str] = None
    notes: Optional[str] = None
    receipt_path: Optional[str] = None

    @validator('date')
    def validate_date_format(cls, v):
        if v:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Date must be in YYYY-MM-DD format')
        return v


class AddExpenseOutput(BaseModel):
    """Output from adding an expense."""
    success: bool
    data: Optional[ExpenseRecord] = None
    suggested_category: Optional[str] = None
    category_confidence: Optional[float] = None
    needs_confirmation: bool = False
    confirmation_prompt: Optional[str] = None
    error: Optional[str] = None
```

**File**: `src/models/category.py`

```python
"""Category-related Pydantic models."""
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime


class CategoryInfo(BaseModel):
    """Category information with stats."""
    id: int
    name: str = Field(min_length=1)
    expense_count: int = 0
    total_amount: float = 0.0
    is_custom: bool = False


class ManageCategoriesInput(BaseModel):
    """Input for managing categories."""
    action: Literal["list", "add", "rename", "merge"] = "list"
    category_name: Optional[str] = None
    new_name: Optional[str] = None
    merge_into: Optional[str] = None


class ManageCategoriesOutput(BaseModel):
    """Output from category management."""
    success: bool
    categories: List[CategoryInfo] = []
    action_result: Optional[str] = None
    expenses_affected: int = 0
    error: Optional[str] = None
```

**File**: `src/models/search.py`

```python
"""Search and summary Pydantic models."""
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime

from .expense import ExpenseRecord


class SearchExpensesInput(BaseModel):
    """Input for searching expenses."""
    query: Optional[str] = None
    category: Optional[str] = None
    vendor: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    min_amount: Optional[float] = Field(None, ge=0)
    max_amount: Optional[float] = Field(None, ge=0)
    limit: int = Field(default=50, ge=1, le=500)
    offset: int = Field(default=0, ge=0)
    sort_by: Literal["date", "amount", "vendor", "category"] = "date"
    sort_order: Literal["asc", "desc"] = "desc"


class SearchExpensesOutput(BaseModel):
    """Output from expense search."""
    success: bool
    expenses: List[ExpenseRecord] = []
    total_count: int = 0
    total_amount: float = 0.0
    has_more: bool = False
    query_summary: str = ""
    error: Optional[str] = None


class SummaryGroup(BaseModel):
    """Summary group data."""
    name: str
    amount: float
    count: int
    percentage: float
    expenses: Optional[List[ExpenseRecord]] = None


class PeriodComparison(BaseModel):
    """Period comparison data."""
    previous_period_amount: float
    change_amount: float
    change_percentage: float


class ExpenseSummary(BaseModel):
    """Expense summary data."""
    total_amount: float
    total_count: int
    groups: List[SummaryGroup] = []
    comparison: Optional[PeriodComparison] = None


class GetSummaryInput(BaseModel):
    """Input for generating summaries."""
    period: Literal["day", "week", "month", "quarter", "year", "custom"] = "month"
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    group_by: Literal["category", "vendor", "day", "week", "month"] = "category"
    include_details: bool = False
    top_n: Optional[int] = Field(None, ge=1, le=50)


class GetSummaryOutput(BaseModel):
    """Output from summary generation."""
    success: bool
    summary: Optional[ExpenseSummary] = None
    period_label: str = ""
    generated_at: str = ""
    error: Optional[str] = None
```

**File**: `src/models/receipt.py`

```python
"""Receipt-related Pydantic models."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from .expense import ExpenseRecord


class ExtractedReceiptData(BaseModel):
    """Data extracted from receipt image."""
    vendor: Optional[str] = None
    vendor_confidence: float = 0.0
    amount: Optional[float] = None
    amount_confidence: float = 0.0
    date: Optional[str] = None
    date_confidence: float = 0.0
    items: Optional[List[str]] = None
    suggested_category: Optional[str] = None


class ProcessReceiptInput(BaseModel):
    """Input for processing a receipt."""
    image_path: str
    auto_add: bool = False


class ProcessReceiptOutput(BaseModel):
    """Output from receipt processing."""
    success: bool
    extracted_data: Optional[ExtractedReceiptData] = None
    confidence: float = 0.0
    needs_review: bool = True
    expense_added: Optional[ExpenseRecord] = None
    error: Optional[str] = None
```

**File**: `src/models/import_export.py`

```python
"""Import and export Pydantic models."""
from pydantic import BaseModel, Field
from typing import Optional, List

from .expense import ExpenseRecord


class ImportExpensesInput(BaseModel):
    """Input for importing expenses from CSV."""
    file_path: str
    date_column: str = "date"
    amount_column: str = "amount"
    vendor_column: str = "vendor"
    category_column: Optional[str] = None
    notes_column: Optional[str] = None
    skip_duplicates: bool = True
    dry_run: bool = True


class ImportExpensesOutput(BaseModel):
    """Output from expense import."""
    success: bool
    total_rows: int = 0
    imported: int = 0
    skipped: int = 0
    errors: int = 0
    error_details: List[str] = []
    preview: Optional[List[ExpenseRecord]] = None
    duplicates_found: int = 0
    dry_run: bool = True


class ExportReportInput(BaseModel):
    """Input for exporting expense reports."""
    format: str = Field(default="csv", pattern="^(csv|summary_csv|detailed_csv)$")
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    categories: Optional[List[str]] = None
    output_path: Optional[str] = None
    include_summary: bool = True


class ExportReportOutput(BaseModel):
    """Output from report export."""
    success: bool
    file_path: str = ""
    total_expenses: int = 0
    total_amount: float = 0.0
    date_range: str = ""
    preview: Optional[str] = None
    error: Optional[str] = None
```

**File**: `src/models/__init__.py`

```python
"""Export all models."""
from .expense import ExpenseRecord, AddExpenseInput, AddExpenseOutput
from .category import CategoryInfo, ManageCategoriesInput, ManageCategoriesOutput
from .search import (
    SearchExpensesInput, SearchExpensesOutput,
    GetSummaryInput, GetSummaryOutput,
    ExpenseSummary, SummaryGroup, PeriodComparison
)
from .receipt import (
    ExtractedReceiptData, ProcessReceiptInput, ProcessReceiptOutput
)
from .import_export import (
    ImportExpensesInput, ImportExpensesOutput,
    ExportReportInput, ExportReportOutput
)

__all__ = [
    # Expense
    "ExpenseRecord", "AddExpenseInput", "AddExpenseOutput",
    # Category
    "CategoryInfo", "ManageCategoriesInput", "ManageCategoriesOutput",
    # Search & Summary
    "SearchExpensesInput", "SearchExpensesOutput",
    "GetSummaryInput", "GetSummaryOutput",
    "ExpenseSummary", "SummaryGroup", "PeriodComparison",
    # Receipt
    "ExtractedReceiptData", "ProcessReceiptInput", "ProcessReceiptOutput",
    # Import/Export
    "ImportExpensesInput", "ImportExpensesOutput",
    "ExportReportInput", "ExportReportOutput",
]
```

**Deliverables**:
- [ ] `src/models/expense.py` - Expense models
- [ ] `src/models/category.py` - Category models
- [ ] `src/models/search.py` - Search and summary models
- [ ] `src/models/receipt.py` - Receipt models
- [ ] `src/models/import_export.py` - Import/export models
- [ ] `src/models/__init__.py` - Exports all models
- [ ] All models validate correctly (test with sample data)

---

#### Task 1.4: Utility Functions (30 minutes)

**Objective**: Create shared utility functions

**File**: `src/utils/date_utils.py`

```python
"""Date utility functions."""
from datetime import date, datetime, timedelta
from typing import Tuple, Optional


def parse_date(date_str: str) -> date:
    """Parse date string in YYYY-MM-DD format."""
    return datetime.strptime(date_str, '%Y-%m-%d').date()


def format_date(d: date) -> str:
    """Format date as YYYY-MM-DD."""
    return d.strftime('%Y-%m-%d')


def get_period_range(
    period: str,
    reference_date: date = None
) -> Tuple[date, date]:
    """Get start and end dates for a period."""
    ref = reference_date or date.today()

    if period == "day":
        return ref, ref
    elif period == "week":
        start = ref - timedelta(days=ref.weekday())
        end = start + timedelta(days=6)
        return start, end
    elif period == "month":
        start = ref.replace(day=1)
        if ref.month == 12:
            end = ref.replace(year=ref.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end = ref.replace(month=ref.month + 1, day=1) - timedelta(days=1)
        return start, end
    elif period == "quarter":
        quarter = (ref.month - 1) // 3
        start_month = quarter * 3 + 1
        start = ref.replace(month=start_month, day=1)
        end_month = start_month + 2
        if end_month == 12:
            end = ref.replace(month=12, day=31)
        else:
            end = ref.replace(month=end_month + 1, day=1) - timedelta(days=1)
        return start, end
    elif period == "year":
        start = ref.replace(month=1, day=1)
        end = ref.replace(month=12, day=31)
        return start, end
    else:
        raise ValueError(f"Unknown period: {period}")


def format_period_label(start: date, end: date) -> str:
    """Generate human-readable period label."""
    if start == end:
        return start.strftime('%B %d, %Y')
    elif start.year == end.year:
        if start.month == end.month:
            return f"{start.strftime('%B %d')} - {end.strftime('%d, %Y')}"
        else:
            return f"{start.strftime('%B')} - {end.strftime('%B %Y')}"
    else:
        return f"{start.strftime('%B %Y')} - {end.strftime('%B %Y')}"
```

**File**: `src/utils/id_generator.py`

```python
"""ID generation utilities."""
from datetime import datetime
import uuid


def generate_expense_id() -> str:
    """Generate unique expense ID."""
    timestamp = datetime.now().strftime('%Y%m%d')
    unique = uuid.uuid4().hex[:8]
    return f"exp_{timestamp}_{unique}"
```

**Deliverables**:
- [ ] `src/utils/date_utils.py` - Date utilities
- [ ] `src/utils/id_generator.py` - ID generation
- [ ] `src/utils/__init__.py` - Exports utilities

---

#### Task 1.5: Mock Data & Tests (30 minutes)

**Objective**: Create mock data and basic tests

**File**: `data/mock/sample_expenses.json`

```json
[
  {
    "id": "exp_20250124_mock001",
    "amount": 85.50,
    "vendor": "Morton's Steakhouse",
    "category": "Meals & Entertainment",
    "date": "2025-01-24",
    "notes": "Client dinner with John Smith",
    "created_at": "2025-01-24T19:30:00Z"
  },
  {
    "id": "exp_20250123_mock002",
    "amount": 299.99,
    "vendor": "Amazon",
    "category": "Office Supplies",
    "date": "2025-01-23",
    "notes": "Standing desk converter",
    "created_at": "2025-01-23T10:15:00Z"
  }
]
```

**File**: `tests/test_models/test_expense.py`

```python
"""Tests for expense models."""
import pytest
from src.models import AddExpenseInput, ExpenseRecord


def test_add_expense_input_valid():
    """Test valid expense input."""
    input_data = AddExpenseInput(
        amount=50.00,
        vendor="Test Vendor",
        date="2025-01-24"
    )
    assert input_data.amount == 50.00
    assert input_data.vendor == "Test Vendor"


def test_add_expense_input_invalid_date():
    """Test invalid date format."""
    with pytest.raises(ValueError):
        AddExpenseInput(
            amount=50.00,
            vendor="Test",
            date="01-24-2025"  # Wrong format
        )


def test_add_expense_input_negative_amount():
    """Test negative amount rejected."""
    with pytest.raises(ValueError):
        AddExpenseInput(amount=-50.00, vendor="Test")
```

**Deliverables**:
- [ ] `data/mock/sample_expenses.json` - Sample expense data
- [ ] `tests/test_models/test_expense.py` - Model tests
- [ ] Tests pass: `pytest tests/test_models/`

---

### Phase 1 Completion Checklist

- [ ] Project structure created
- [ ] Virtual environment working
- [ ] Dependencies installed
- [ ] Database schema created and initializes
- [ ] All Pydantic models defined
- [ ] Utility functions created
- [ ] Mock data in place
- [ ] Basic model tests passing
- [ ] Can import all modules without errors

**Verification Command**:
```bash
cd agents/claude-sdk/python/expense-tracker
source .venv/bin/activate
python -c "from src.models import *; from src.database import db; db.initialize(); print('Foundation ready!')"
pytest tests/test_models/ -v
```

---

## Phase 2A: Core Operations Agent

**Agent Role**: Implement core expense CRUD operations and category management

**Dependencies**: Phase 1 (Foundation) must be complete

**Can Run In Parallel With**: Phase 2B (Advanced Features)

**Estimated Time**: 5 hours

### Tasks

#### Task 2A.1: ExpenseService (1.5 hours)

**Objective**: Implement core expense CRUD operations

**File**: `src/services/expense_service.py`

**Methods to implement**:
- `create_expense(input: AddExpenseInput) -> ExpenseRecord`
- `get_expense(expense_id: str) -> Optional[ExpenseRecord]`
- `search_expenses(input: SearchExpensesInput) -> List[ExpenseRecord]`
- `update_expense(expense_id: str, updates: dict) -> ExpenseRecord`
- `delete_expense(expense_id: str) -> bool`
- `check_duplicate(amount: float, vendor: str, date: date) -> bool`

**Deliverables**:
- [ ] `src/services/expense_service.py` complete
- [ ] All methods tested
- [ ] Duplicate detection working

---

#### Task 2A.2: CategoryService (1 hour)

**Objective**: Implement category management

**File**: `src/services/category_service.py`

**Methods to implement**:
- `list_categories() -> List[CategoryInfo]`
- `get_category_by_name(name: str) -> Optional[CategoryInfo]`
- `add_category(name: str) -> CategoryInfo`
- `rename_category(old_name: str, new_name: str) -> CategoryInfo`
- `merge_categories(source: str, target: str) -> int`
- `suggest_category(vendor: str, notes: str) -> Tuple[str, float]`

**Deliverables**:
- [ ] `src/services/category_service.py` complete
- [ ] Category CRUD working
- [ ] Auto-suggestion logic implemented

---

#### Task 2A.3: Tools - add_expense (1 hour)

**Objective**: Implement add_expense tool

**File**: `src/tools/add_expense.py`

**Features**:
- Natural language parsing
- Structured input handling
- Auto-categorization
- Duplicate detection

**Deliverables**:
- [ ] `src/tools/add_expense.py` complete
- [ ] Natural language parsing working
- [ ] Returns proper output schema

---

#### Task 2A.4: Tools - search_expenses (45 minutes)

**Objective**: Implement search_expenses tool

**File**: `src/tools/search_expenses.py`

**Features**:
- Multiple filter criteria
- Pagination
- Sorting
- Total calculations

**Deliverables**:
- [ ] `src/tools/search_expenses.py` complete
- [ ] All filters working
- [ ] Pagination working

---

#### Task 2A.5: Tools - manage_categories (45 minutes)

**Objective**: Implement manage_categories tool

**File**: `src/tools/manage_categories.py`

**Features**:
- List with stats
- Add custom
- Rename
- Merge

**Deliverables**:
- [ ] `src/tools/manage_categories.py` complete
- [ ] All actions working
- [ ] Expense counts accurate

---

### Phase 2A Completion Checklist

- [ ] ExpenseService complete with tests
- [ ] CategoryService complete with tests
- [ ] add_expense tool working
- [ ] search_expenses tool working
- [ ] manage_categories tool working
- [ ] All unit tests passing

**Verification**:
```bash
pytest tests/test_services/test_expense_service.py -v
pytest tests/test_tools/test_add_expense.py -v
pytest tests/test_tools/test_search_expenses.py -v
```

---

## Phase 2B: Advanced Features Agent

**Agent Role**: Implement import, export, summary, and receipt processing

**Dependencies**: Phase 1 (Foundation) must be complete

**Can Run In Parallel With**: Phase 2A (Core Operations)

**Estimated Time**: 6 hours

### Tasks

#### Task 2B.1: ImportService (1.5 hours)

**Objective**: Implement CSV import functionality

**File**: `src/services/import_service.py`

**Methods to implement**:
- `validate_csv(file_path: str, column_mapping: dict) -> ValidationResult`
- `import_csv(input: ImportExpensesInput) -> ImportExpensesOutput`
- `detect_duplicates(expenses: List) -> List[int]`
- `auto_categorize_batch(expenses: List) -> List`

**Deliverables**:
- [ ] `src/services/import_service.py` complete
- [ ] CSV parsing working
- [ ] Dry run mode working
- [ ] Duplicate detection working

---

#### Task 2B.2: ReportService (1.5 hours)

**Objective**: Implement summary and export functionality

**File**: `src/services/report_service.py`

**Methods to implement**:
- `generate_summary(input: GetSummaryInput) -> ExpenseSummary`
- `export_csv(input: ExportReportInput) -> str`
- `calculate_period_comparison(current: date, previous: date) -> PeriodComparison`
- `group_expenses(expenses: List, group_by: str) -> List[SummaryGroup]`

**Deliverables**:
- [ ] `src/services/report_service.py` complete
- [ ] Summaries calculating correctly
- [ ] CSV export working
- [ ] Period comparisons working

---

#### Task 2B.3: ReceiptService (1.5 hours)

**Objective**: Implement receipt OCR using Claude vision

**File**: `src/services/receipt_service.py`

**Methods to implement**:
- `process_image(image_path: str) -> ExtractedReceiptData`
- `extract_with_claude_vision(image_bytes: bytes) -> dict`
- `parse_receipt_response(response: str) -> ExtractedReceiptData`
- `calculate_confidence(extracted: ExtractedReceiptData) -> float`

**Deliverables**:
- [ ] `src/services/receipt_service.py` complete
- [ ] Claude vision integration working
- [ ] Confidence scores calculated
- [ ] Error handling for unreadable receipts

---

#### Task 2B.4: Tools - import_expenses (30 minutes)

**File**: `src/tools/import_expenses.py`

**Deliverables**:
- [ ] Tool wrapper complete
- [ ] Dry run mode exposed
- [ ] Error details returned

---

#### Task 2B.5: Tools - get_summary (30 minutes)

**File**: `src/tools/get_summary.py`

**Deliverables**:
- [ ] Tool wrapper complete
- [ ] All grouping options working
- [ ] Period label formatted

---

#### Task 2B.6: Tools - export_report (30 minutes)

**File**: `src/tools/export_report.py`

**Deliverables**:
- [ ] Tool wrapper complete
- [ ] File creation working
- [ ] Preview generation working

---

#### Task 2B.7: Tools - process_receipt (30 minutes)

**File**: `src/tools/process_receipt.py`

**Deliverables**:
- [ ] Tool wrapper complete
- [ ] Auto-add option working
- [ ] Confidence thresholds implemented

---

### Phase 2B Completion Checklist

- [ ] ImportService complete with tests
- [ ] ReportService complete with tests
- [ ] ReceiptService complete with tests
- [ ] All 4 tools working
- [ ] Unit tests passing

**Verification**:
```bash
pytest tests/test_services/test_import_service.py -v
pytest tests/test_services/test_report_service.py -v
pytest tests/test_tools/test_import_expenses.py -v
pytest tests/test_tools/test_get_summary.py -v
```

---

## Phase 3: Orchestrator

**Agent Role**: Create main agent, integration tests, and documentation

**Dependencies**: Phase 2A and 2B must be complete

**Estimated Time**: 3 hours

### Tasks

#### Task 3.1: Main Agent Configuration (1 hour)

**File**: `src/main.py`

**Implementation**:
- Import all tools
- Configure Anthropic client
- Write system prompt
- Register tools
- Create conversation handler

**System Prompt**:
```
You are an intelligent expense tracking assistant. You help users manage their business expenses through natural conversation.

Your capabilities:
- Add expenses via natural language ("$50 lunch at Chipotle")
- Process receipt images to extract expense data
- Import expenses from CSV files
- Search and filter expense history
- Generate spending summaries by category or time period
- Export expense reports
- Manage expense categories

When adding expenses:
1. Extract amount, vendor, and date from the input
2. Suggest an appropriate category
3. Confirm the expense details before saving

When searching:
- Help users find specific expenses
- Provide totals and summaries when relevant

Always be helpful, accurate, and confirm important actions before proceeding.
```

**Deliverables**:
- [ ] `src/main.py` complete
- [ ] All 7 tools registered
- [ ] System prompt defined
- [ ] Agent responds to basic queries

---

#### Task 3.2: Integration Tests (1 hour)

**File**: `tests/test_integration/test_workflows.py`

**Test Scenarios**:
1. Add expense workflow (natural language → stored in DB → searchable)
2. Import workflow (CSV → preview → import → verify)
3. Summary workflow (add expenses → generate summary → verify totals)
4. Export workflow (add expenses → export → verify file)

**Deliverables**:
- [ ] Integration tests complete
- [ ] All workflows tested end-to-end
- [ ] Tests passing

---

#### Task 3.3: Documentation (1 hour)

**File**: `.claude/CLAUDE.md`

Complete agent documentation including:
- Overview
- Directory structure
- Setup instructions
- Tool descriptions
- Usage examples
- Known limitations

**File**: `README.md`

Quick start guide:
- Installation
- Configuration
- Basic usage
- Examples

**Deliverables**:
- [ ] CLAUDE.md complete
- [ ] README.md complete
- [ ] All examples work

---

### Phase 3 Completion Checklist

- [ ] Main agent functional
- [ ] All 7 tools working together
- [ ] Integration tests passing
- [ ] Documentation complete
- [ ] Agent handles natural conversation

**Final Verification**:
```bash
# Run all tests
pytest tests/ -v

# Test agent manually
python -m src.main
```

---

## Implementation Notes

### Key Patterns to Follow

1. **Pydantic Validation**: All tool inputs/outputs use Pydantic models
2. **Service Layer**: Business logic in services, tools are thin wrappers
3. **Error Handling**: Try-catch with specific error messages
4. **Graceful Degradation**: Return partial results when possible

### Common Gotchas

1. **SQLite Date Format**: Store as TEXT in ISO format (YYYY-MM-DD)
2. **Pydantic v2**: Use `model_validate()` not `parse_obj()`
3. **Module Imports**: Use `python -m src.main` not `python src/main.py`
4. **Receipt OCR**: Base64 encode images for Claude vision

### Testing Commands

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_tools/test_add_expense.py -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

---

## Summary

| Phase | Agent | Hours | Dependencies |
|-------|-------|-------|--------------|
| 1 | Foundation | 3 | None |
| 2A | Core Ops | 5 | Phase 1 |
| 2B | Advanced | 6 | Phase 1 |
| 3 | Orchestrator | 3 | Phase 2A + 2B |
| **Total** | **4 agents** | **~11 hrs** | (17 sequential) |

**Time Savings**: 35% through parallel execution of Phase 2A and 2B
