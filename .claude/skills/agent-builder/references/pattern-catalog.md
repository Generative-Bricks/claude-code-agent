# Agent Builder Pattern Catalog

This document catalogs proven, reusable patterns discovered through building production-ready AI agents. Each pattern includes purpose, implementation, examples, and guidance on when to use it.

## Table of Contents

1. [Validation Patterns](#validation-patterns)
2. [Subagent Patterns](#subagent-patterns)
3. [Data Management Patterns](#data-management-patterns)
4. [Scoring & Ranking Patterns](#scoring--ranking-patterns)
5. [Architecture Patterns](#architecture-patterns)
6. [Error Handling Patterns](#error-handling-patterns)
7. [Performance Patterns](#performance-patterns)
8. [Integration Patterns](#integration-patterns)

---

## Validation Patterns

### Pattern 1: Zod Validation (TypeScript)

**Purpose**: Type-safe input validation with runtime checking

**Problem Solved**: Catching invalid inputs before they cause errors in business logic

**When to use**:
- ✅ All TypeScript agent tools (always recommended)
- ✅ When you need compile-time + runtime validation
- ✅ Complex nested object validation

**Implementation**:

```typescript
import { z } from 'zod';

// Define schema
const ToolInputSchema = z.object({
  // Required string with min length
  name: z.string().min(1, "Name is required"),

  // Positive number
  amount: z.number().positive("Amount must be positive"),

  // Optional with default
  limit: z.number().positive().default(10),

  // Enum
  type: z.enum(['option1', 'option2', 'option3']),

  // Nested object
  metadata: z.object({
    source: z.string(),
    timestamp: z.date()
  }).optional(),

  // Array of strings
  tags: z.array(z.string()).min(1)
});

// Infer TypeScript type from schema
type ToolInput = z.infer<typeof ToolInputSchema>;

// Tool implementation
export function myTool(input: unknown): ToolOutput {
  try {
    // Validate and parse - throws on invalid input
    const validated = ToolInputSchema.parse(input);

    // Use validated data (fully typed)
    // ...

    return { success: true, data: {...} };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return {
        success: false,
        error: `Validation failed: ${error.errors.map(e => e.message).join(', ')}`
      };
    }
    return { success: false, error: 'Unknown error' };
  }
}
```

**Benefits**:
- ✅ Compile-time type safety
- ✅ Runtime validation
- ✅ Clear error messages
- ✅ Self-documenting schemas

**Pitfalls**:
- ⚠️ Can be verbose for complex schemas
- ⚠️ Adds slight runtime overhead

**Examples**:
- Financial Advisor Agent (all 6 tools use Zod)

---

### Pattern 2: Pydantic Validation (Python)

**Purpose**: Runtime validation with type hints and data classes

**Problem Solved**: Ensuring data integrity in Python with runtime type checking

**When to use**:
- ✅ All Python agent tools (always recommended)
- ✅ Complex data models
- ✅ API request/response validation

**Implementation**:

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Literal
from datetime import datetime

# Define model
class ToolInput(BaseModel):
    # Required string with constraints
    name: str = Field(min_length=1, description="Name is required")

    # Positive number
    amount: float = Field(gt=0, description="Amount must be positive")

    # Optional with default
    limit: int = Field(default=10, gt=0)

    # Literal (enum-like)
    type: Literal['option1', 'option2', 'option3']

    # Nested model
    metadata: Optional['Metadata'] = None

    # List of strings with min length
    tags: List[str] = Field(min_items=1)

    # Custom validator
    @validator('amount')
    def amount_must_be_reasonable(cls, v):
        if v > 1_000_000:
            raise ValueError('Amount too large')
        return v

    class Config:
        # Enable validation on assignment
        validate_assignment = True

class Metadata(BaseModel):
    source: str
    timestamp: datetime

# Tool implementation
def my_tool(input_data: dict) -> dict:
    try:
        # Validate and parse - raises ValidationError on invalid input
        validated = ToolInput(**input_data)

        # Use validated data (type-safe attributes)
        # ...

        return {"success": True, "data": {...}}
    except ValidationError as e:
        return {
            "success": False,
            "error": f"Validation failed: {e.errors()}"
        }
```

**Benefits**:
- ✅ Runtime type checking
- ✅ Automatic JSON serialization
- ✅ Clear validation errors
- ✅ Works with type checkers (mypy, pyright)

**Pitfalls**:
- ⚠️ Runtime-only (no compile-time checking like TypeScript)
- ⚠️ Pydantic v1 vs v2 compatibility issues

**Examples**:
- FIA Analyzer (all tools use Pydantic)
- Portfolio Collaboration (all 20+ models use Pydantic)
- OpportunityIQ Client Matcher (3-layer architecture with Pydantic throughout)

---

## Subagent Patterns

### Pattern 3: Specialization Pattern

**Purpose**: Delegate tasks based on domain expertise

**Problem Solved**: Main agent can't be expert in all domains

**When to use**:
- ✅ Different tasks require different expertise (finance, legal, technical)
- ✅ Domain-specific knowledge needed
- ✅ Clear separation of concerns

**Implementation**:

```typescript
// Main agent configuration
const mainAgent = new Agent({
  name: 'Orchestrator',
  model: 'claude-sonnet-4',
  instructions: `
    You are an orchestrator that delegates to specialists.

    Use the Finance Specialist for financial analysis.
    Use the Legal Specialist for compliance questions.
    Use the Technical Specialist for technical evaluation.
  `,
  tools: [/* main tools */]
});

// Specialized subagents
const financeSpecialist = new Agent({
  name: 'Finance Specialist',
  model: 'claude-sonnet-4',
  instructions: `
    You are a financial analysis expert.
    Analyze portfolios, calculate metrics, assess risk.
  `,
  tools: [/* finance tools */]
});

const legalSpecialist = new Agent({
  name: 'Legal Specialist',
  model: 'claude-sonnet-4',
  instructions: `
    You are a compliance expert.
    Check regulatory requirements, assess legal risks.
  `,
  tools: [/* legal tools */]
});

// Delegation
async function delegateTask(task, domain) {
  if (domain === 'finance') {
    return financeSpecialist.run(task);
  } else if (domain === 'legal') {
    return legalSpecialist.run(task);
  }
  // ...
}
```

**Benefits**:
- ✅ Clear separation of expertise
- ✅ Each subagent focused on one domain
- ✅ Easy to add new specialists

**Pitfalls**:
- ⚠️ Coordination overhead
- ⚠️ Context passing complexity

**Examples**:
- Portfolio Collaboration (Risk, Compliance, Performance specialists)

---

### Pattern 4: Complexity-Based Delegation

**Purpose**: Use different models based on reasoning complexity

**Problem Solved**: Optimize for cost and speed while maintaining quality

**When to use**:
- ✅ Some tasks need deep reasoning (use Sonnet)
- ✅ Some tasks are simple calculations (use Haiku)
- ✅ Performance optimization matters

**Implementation**:

```typescript
const mainAgent = new Agent({
  name: 'Main Agent',
  model: 'claude-sonnet-4',
  instructions: `
    For complex analysis requiring deep reasoning, delegate to Deep Analysis Subagent.
    For quick calculations and simple transformations, delegate to Quick Calc Subagent.
  `
});

// Complex reasoning subagent (Sonnet)
const deepAnalysisAgent = new Agent({
  name: 'Deep Analysis',
  model: 'claude-sonnet-4', // or claude-opus-4 for even deeper reasoning
  instructions: 'Perform in-depth analysis with nuanced reasoning.'
});

// Quick calculations subagent (Haiku)
const quickCalcAgent = new Agent({
  name: 'Quick Calc',
  model: 'claude-haiku-4',
  instructions: 'Perform fast calculations and simple transformations.'
});
```

**Benefits**:
- ✅ Cost optimization (Haiku cheaper than Sonnet)
- ✅ Speed optimization (Haiku faster)
- ✅ Quality where needed (Sonnet for complex tasks)

**Pitfalls**:
- ⚠️ Need clear decision criteria for delegation
- ⚠️ Context passing overhead

**Examples**:
- Financial Advisor Agent (Sonnet for analysis, Haiku for optimization)

---

### Pattern 5: Parallel Execution Pattern

**Purpose**: Run independent subagents concurrently for performance

**Problem Solved**: Sequential execution too slow when tasks are independent

**When to use**:
- ✅ Multiple independent tasks
- ✅ No shared state between tasks
- ✅ Performance matters

**Implementation**:

```python
import asyncio

# Define multiple independent agents
risk_agent = Agent(name="Risk Analyst", ...)
compliance_agent = Agent(name="Compliance Officer", ...)
performance_agent = Agent(name="Performance Analyst", ...)

# Run in parallel
async def analyze_portfolio(portfolio_data):
    # Run all agents concurrently
    results = await asyncio.gather(
        risk_agent.run(portfolio_data),
        compliance_agent.run(portfolio_data),
        performance_agent.run(portfolio_data)
    )

    risk_result, compliance_result, performance_result = results

    # Combine results
    return {
        "risk": risk_result,
        "compliance": compliance_result,
        "performance": performance_result
    }
```

**Benefits**:
- ✅ 65%+ performance improvement (3 agents: 5s vs 15s)
- ✅ Simple to implement with asyncio.gather()
- ✅ Scales well with more agents

**Pitfalls**:
- ⚠️ Only for independent tasks (no shared state)
- ⚠️ Error handling more complex
- ⚠️ Token limits if too many parallel requests

**Examples**:
- Portfolio Collaboration (Risk/Compliance/Performance run in parallel)

**Metrics**:
- 3 agents in parallel: ~65% faster
- 5 agents in parallel: ~70% faster

---

## Data Management Patterns

### Pattern 6: Mock Data First

**Purpose**: Develop and test independently of external APIs

**Problem Solved**: Dependency on unreliable or slow external APIs during development

**When to use**:
- ✅ Always (recommended for all agents)
- ✅ External API not ready yet
- ✅ Want fast, predictable tests
- ✅ Need offline development

**Implementation**:

```typescript
// Mock data structured identically to production API
const MOCK_PRODUCTS = [
  {
    id: 'PROD-001',
    name: 'Fixed Indexed Annuity A',
    carrier: 'Example Insurance Co',
    capRate: 0.055,
    participationRate: 0.80,
    minimumInvestment: 25000,
    // ... all fields matching production API
  },
  // ... more examples including edge cases
];

// Data fetching with mock/real toggle
export async function fetchProducts(query: string): Promise<Product[]> {
  const USE_MOCK = process.env.USE_MOCK_DATA === 'true';

  if (USE_MOCK) {
    // Return mock data (fast, reliable)
    return MOCK_PRODUCTS.filter(p =>
      p.name.toLowerCase().includes(query.toLowerCase())
    );
  } else {
    // TODO: Replace with real API call when ready
    const response = await fetch(`/api/products?q=${query}`, {
      headers: { 'Authorization': `Bearer ${process.env.API_KEY}` }
    });
    return response.json();
  }
}
```

**Benefits**:
- ✅ Fast development (no API delays)
- ✅ Predictable tests (no flaky external dependencies)
- ✅ Offline development possible
- ✅ Easy to create edge case data

**Pitfalls**:
- ⚠️ Mock data must match production structure exactly
- ⚠️ Remember to test with real API before deployment
- ⚠️ Keep mock data updated if API changes

**Examples**:
- Financial Advisor Agent (all tools use mock data)
- FIA Analyzer (mock product data)
- Portfolio Collaboration (supports both mock and real via Yahoo Finance)

---

### Pattern 7: Service-Based Architecture

**Purpose**: Separate business logic from tool wrappers

**Problem Solved**: Tool code becomes complex and hard to test

**When to use**:
- ✅ Medium to high complexity agents
- ✅ Want to reuse logic outside of tools
- ✅ Need to test business logic separately
- ✅ Multiple tools share logic

**Implementation**:

```
project/
├── src/
│   ├── models/         # Pydantic models (validation)
│   │   ├── client.py
│   │   └── product.py
│   ├── services/       # Business logic
│   │   ├── analysis_service.py
│   │   └── matching_service.py
│   └── tools/          # Claude-callable wrappers
│       ├── analyze_tool.py
│       └── match_tool.py
```

```python
# Layer 1: Models (Pydantic validation)
# models/client.py
class Client(BaseModel):
    id: str
    age: int
    income: float

# Layer 2: Services (Business logic)
# services/analysis_service.py
class AnalysisService:
    def calculate_suitability(self, client: Client, product: Product) -> float:
        # Complex business logic here
        score = ...
        return score

# Layer 3: Tools (Claude-callable wrappers)
# tools/analyze_tool.py
def analyze_suitability(input_data: dict) -> dict:
    try:
        # Parse input
        client = Client(**input_data['client'])
        product = Product(**input_data['product'])

        # Call service
        service = AnalysisService()
        score = service.calculate_suitability(client, product)

        # Return result
        return {"success": True, "data": {"score": score}}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

**Benefits**:
- ✅ Clear separation of concerns
- ✅ Easy to test services independently
- ✅ Reusable business logic
- ✅ Tools stay simple (thin wrappers)

**Pitfalls**:
- ⚠️ More files to manage
- ⚠️ Overkill for simple agents

**Examples**:
- OpportunityIQ Client Matcher (3-layer: models → services → tools)
- Google Drive Agent (AuthService, DriveService, ContentExtractor, CacheService)

---

### Pattern 8: Direct Context Passing (No RAG)

**Purpose**: Avoid RAG complexity for small document collections

**Problem Solved**: RAG adds 4+ extra steps for documents that fit in context

**When to use**:
- ✅ Working with 1 document at a time
- ✅ Documents are 5-20 pages each
- ✅ Entire document fits in LLM context (200K+ tokens)
- ✅ User doesn't need semantic search across 100s of docs

**Implementation**:

```python
# Simple 3-step workflow
def answer_question(document_id: str, question: str) -> str:
    # Step 1: Fetch document
    document_content = drive_service.get_file_content(document_id)

    # Step 2: Pass entire document to LLM
    response = client.messages.create(
        model="claude-sonnet-4",
        messages=[{
            "role": "user",
            "content": f"""
                Document:
                {document_content}

                Question: {question}

                Answer the question based on the document above.
            """
        }]
    )

    # Step 3: Return answer
    return response.content[0].text
```

**vs RAG (7+ steps)**:
```python
# Complex RAG workflow
def answer_question_with_rag(document_id: str, question: str) -> str:
    # Step 1: Fetch document
    # Step 2: Chunk document
    # Step 3: Generate embeddings
    # Step 4: Store in vector DB
    # Step 5: Embed question
    # Step 6: Similarity search
    # Step 7: Retrieve relevant chunks
    # Step 8: Pass chunks to LLM
    # ...
```

**Benefits**:
- ✅ 3 steps vs 7+ with RAG
- ✅ No vector database needed
- ✅ No embedding generation
- ✅ Simpler architecture
- ✅ Faster development

**Pitfalls**:
- ⚠️ Doesn't scale to 100s of documents
- ⚠️ Can't do semantic search across corpus
- ⚠️ Limited by context window

**When to avoid**:
- ❌ Need to search across 50+ documents
- ❌ Documents are 100+ pages each
- ❌ Need semantic similarity search

**Examples**:
- Google Drive Agent (passes full document to Claude)

---

## Scoring & Ranking Patterns

### Pattern 9: Weighted Scoring

**Purpose**: Multi-dimensional assessment with transparent calculation

**Problem Solved**: Need to combine multiple factors into single score

**When to use**:
- ✅ Suitability analysis
- ✅ Ranking/prioritization
- ✅ Multi-criteria decision making
- ✅ Need transparent, explainable scores

**Implementation**:

```python
class WeightedScoring:
    def __init__(self, weights: dict[str, float]):
        # Ensure weights sum to 1.0
        total = sum(weights.values())
        self.weights = {k: v/total for k, v in weights.items()}

    def calculate_score(self, scores: dict[str, float]) -> float:
        """
        Calculate weighted score.

        Args:
            scores: Dict of criterion name → score (0-100)

        Returns:
            Weighted score (0-100)
        """
        weighted_score = sum(
            scores[criterion] * weight
            for criterion, weight in self.weights.items()
        )
        return weighted_score

# Example usage
weights = {
    "compliance": 0.35,  # Most important (regulatory)
    "risk": 0.25,
    "performance": 0.25,
    "time_horizon": 0.15
}

scoring = WeightedScoring(weights)

client_scores = {
    "compliance": 90,
    "risk": 75,
    "performance": 80,
    "time_horizon": 85
}

final_score = scoring.calculate_score(client_scores)
# Result: 82.75 (weighted average)
```

**Score Interpretation**:
```python
def interpret_score(score: float) -> str:
    if score >= 80:
        return "Highly Suitable"
    elif score >= 60:
        return "Suitable"
    elif score >= 40:
        return "Marginal Fit"
    else:
        return "Not Suitable"
```

**Benefits**:
- ✅ Transparent calculation
- ✅ Easy to explain to users
- ✅ Customizable weights per use case
- ✅ Clear interpretation

**Pitfalls**:
- ⚠️ Choosing appropriate weights is subjective
- ⚠️ Weights may need tuning based on feedback

**Examples**:
- Portfolio Collaboration (Compliance 35%, Risk 25%, Performance 25%, Time Horizon 15%)
- FIA Analyzer (10-question suitability framework)
- OpportunityIQ Client Matcher (match quality + revenue)

---

### Pattern 10: Multi-Criteria Comparison

**Purpose**: Compare options across multiple dimensions

**Problem Solved**: Need to rank options considering multiple factors

**When to use**:
- ✅ Product comparison
- ✅ Option evaluation
- ✅ Best-fit analysis

**Implementation**:

```typescript
interface ComparisonCriterion {
  name: string;
  weight: number;
  preferHigher: boolean; // true = higher is better, false = lower is better
}

interface Option {
  id: string;
  name: string;
  values: Record<string, number>;
}

function compareOptions(
  options: Option[],
  criteria: ComparisonCriterion[]
): RankedOption[] {
  // Normalize weights
  const totalWeight = criteria.reduce((sum, c) => sum + c.weight, 0);
  const normalizedCriteria = criteria.map(c => ({
    ...c,
    weight: c.weight / totalWeight
  }));

  // Calculate scores for each option
  const scoredOptions = options.map(option => {
    const criteriaScores = normalizedCriteria.map(criterion => {
      const value = option.values[criterion.name];

      // Normalize value to 0-100 scale
      const allValues = options.map(o => o.values[criterion.name]);
      const min = Math.min(...allValues);
      const max = Math.max(...allValues);
      const range = max - min;

      let normalizedValue = range > 0
        ? ((value - min) / range) * 100
        : 50;

      // Invert if lower is better
      if (!criterion.preferHigher) {
        normalizedValue = 100 - normalizedValue;
      }

      return {
        criterion: criterion.name,
        score: normalizedValue,
        weight: criterion.weight
      };
    });

    const overallScore = criteriaScores.reduce(
      (sum, cs) => sum + (cs.score * cs.weight),
      0
    );

    return {
      ...option,
      criteriaScores,
      overallScore
    };
  });

  // Sort by overall score (descending)
  return scoredOptions.sort((a, b) => b.overallScore - a.overallScore);
}

// Example usage
const options = [
  { id: 'A', name: 'Option A', values: { cost: 100, quality: 80, speed: 90 } },
  { id: 'B', name: 'Option B', values: { cost: 120, quality: 95, speed: 70 } },
  { id: 'C', name: 'Option C', values: { cost: 80, quality: 70, speed: 85 } }
];

const criteria = [
  { name: 'cost', weight: 0.3, preferHigher: false }, // Lower cost is better
  { name: 'quality', weight: 0.5, preferHigher: true },
  { name: 'speed', weight: 0.2, preferHigher: true }
];

const ranked = compareOptions(options, criteria);
// Result: Options ranked by weighted multi-criteria score
```

**Benefits**:
- ✅ Fair comparison across dimensions
- ✅ Transparent scoring
- ✅ Customizable criteria and weights
- ✅ Clear winner identification

**Pitfalls**:
- ⚠️ Normalization can skew results if range is small
- ⚠️ Weights are subjective

**Examples**:
- Financial Advisor Agent (compare_annuity_types tool)

---

## Architecture Patterns

### Pattern 11: Hybrid Multi-Agent (Parallel + Handoff)

**Purpose**: Combine breadth (parallel) with depth (handoff)

**Problem Solved**: Need both wide coverage and deep analysis

**When to use**:
- ✅ Multiple independent analyses needed (parallel)
- ✅ Some tasks need deeper specialized attention (handoff)
- ✅ Performance matters

**Implementation**:

```python
# OpenAI Agents SDK example

# Parallel agents (breadth)
risk_agent = Agent(name="Risk Analyst", instructions="...", model="gpt-4")
compliance_agent = Agent(name="Compliance Officer", instructions="...", model="gpt-4")
performance_agent = Agent(name="Performance Analyst", instructions="...", model="gpt-4")

# Handoff agent (depth)
equity_specialist = Agent(
    name="Equity Specialist",
    instructions="Deep equity analysis with detailed research",
    model="gpt-4"
)

# Orchestrator
portfolio_manager = Agent(
    name="Portfolio Manager",
    instructions="""
        For general analysis:
        - Use Risk Analyst, Compliance Officer, Performance Analyst in parallel

        For deep equity analysis:
        - Hand off to Equity Specialist
    """,
    model="gpt-4"
)

# Execution
async def analyze_portfolio(portfolio_data):
    # Phase 1: Parallel execution (breadth)
    parallel_results = await asyncio.gather(
        risk_agent.run(portfolio_data),
        compliance_agent.run(portfolio_data),
        performance_agent.run(portfolio_data)
    )

    # Phase 2: Deep analysis if needed (depth)
    if needs_equity_analysis:
        equity_result = await equity_specialist.run(equity_data)
    else:
        equity_result = None

    # Combine results
    return combine_results(parallel_results, equity_result)
```

**Benefits**:
- ✅ Fast broad analysis (parallel)
- ✅ Deep specialized analysis when needed (handoff)
- ✅ Best of both worlds

**Pitfalls**:
- ⚠️ More complex orchestration
- ⚠️ Need clear criteria for when to hand off

**Examples**:
- Portfolio Collaboration (Risk/Compliance/Performance parallel, Equity handoff)

**Metrics**:
- 65% faster than sequential for 3+ parallel agents
- Deep analysis available without sacrificing speed

---

### Pattern 12: External Service Integration

**Purpose**: Leverage existing services instead of building custom

**Problem Solved**: Don't rebuild what already exists

**When to use**:
- ✅ External service does 80%+ of what you need
- ✅ Maintained by someone else
- ✅ Reduces complexity significantly

**Implementation**:

```python
# BEFORE: Custom implementation
def extract_pdf_content(pdf_path: str) -> str:
    # Complex custom PDF parsing code (200+ lines)
    # Using reportlab, PyPDF2, etc.
    # ...

# AFTER: Use Anthropic PDF skill
from anthropic import Anthropic

client = Anthropic()

def extract_pdf_content(pdf_path: str) -> str:
    # Let Anthropic handle it (simple)
    with open(pdf_path, 'rb') as f:
        result = client.skills.pdf.extract(file=f)
    return result.text
```

**Before vs After**:
- Code reduction: 70%+ (200 lines → 50 lines)
- Maintenance: External (not your responsibility)
- Quality: Professional (maintained by provider)

**Services to Consider**:
- **PDF Processing**: Anthropic PDF skill
- **Web Scraping**: Fetch MCP server
- **Documentation**: Context7 MCP server
- **Market Data**: Yahoo Finance MCP server

**Benefits**:
- ✅ Massive code reduction (50-70%)
- ✅ Maintained externally
- ✅ Higher quality
- ✅ Faster development

**Pitfalls**:
- ⚠️ Dependency on external service
- ⚠️ Limited customization
- ⚠️ Potential costs

**Examples**:
- FIA Analyzer (Anthropic PDF skill + Fetch MCP server = 70% code reduction)

---

## Error Handling Patterns

### Pattern 13: Graceful Degradation

**Purpose**: Partial success better than total failure

**Problem Solved**: Agent crashes when one component fails

**When to use**:
- ✅ Always (production-grade systems)
- ✅ Multiple independent operations
- ✅ User needs partial results

**Implementation**:

```typescript
async function analyzePortfolio(portfolio: Portfolio): Promise<AnalysisResult> {
  const results: Partial<AnalysisResult> = {};
  const errors: string[] = [];

  // Try risk analysis
  try {
    results.risk = await analyzeRisk(portfolio);
  } catch (error) {
    errors.push(`Risk analysis failed: ${error.message}`);
    // Continue anyway
  }

  // Try compliance check
  try {
    results.compliance = await checkCompliance(portfolio);
  } catch (error) {
    errors.push(`Compliance check failed: ${error.message}`);
    // Continue anyway
  }

  // Try performance analysis
  try {
    results.performance = await analyzePerformance(portfolio);
  } catch (error) {
    errors.push(`Performance analysis failed: ${error.message}`);
    // Continue anyway
  }

  // Return partial results with warnings
  return {
    ...results,
    partial: errors.length > 0,
    errors: errors.length > 0 ? errors : undefined,
    message: errors.length > 0
      ? `Analysis completed with ${errors.length} warning(s)`
      : 'Analysis completed successfully'
  };
}
```

**Benefits**:
- ✅ User gets partial results instead of nothing
- ✅ Clear error messaging
- ✅ System remains functional

**Pitfalls**:
- ⚠️ Users must understand results are partial
- ⚠️ Need clear error messages

**Examples**:
- Portfolio Collaboration (continues with partial data on failures)

---

## Performance Patterns

### Pattern 14: Caching

**Purpose**: Avoid re-fetching unchanged data

**Problem Solved**: Repeated API calls for same data

**When to use**:
- ✅ Same data fetched multiple times
- ✅ Data changes infrequently
- ✅ API calls are slow or expensive

**Implementation**:

```python
import hashlib
import json
from pathlib import Path
from datetime import datetime, timedelta

class CacheService:
    def __init__(self, cache_dir: str = '.cache', ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)

    def _get_cache_key(self, key: str) -> str:
        """Generate cache filename from key"""
        return hashlib.md5(key.encode()).hexdigest() + '.json'

    def get(self, key: str) -> Optional[dict]:
        """Get cached data if exists and not expired"""
        cache_file = self.cache_dir / self._get_cache_key(key)

        if not cache_file.exists():
            return None

        # Check if expired
        mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
        if datetime.now() - mtime > self.ttl:
            cache_file.unlink()  # Delete expired cache
            return None

        # Return cached data
        with open(cache_file) as f:
            return json.load(f)

    def set(self, key: str, data: dict) -> None:
        """Cache data"""
        cache_file = self.cache_dir / self._get_cache_key(key)
        with open(cache_file, 'w') as f:
            json.dump(data, f)

# Usage
cache = CacheService(ttl_hours=24)

def fetch_product_data(product_id: str) -> dict:
    # Check cache first
    cached = cache.get(product_id)
    if cached:
        return cached

    # Fetch from API
    data = api.fetch_product(product_id)

    # Cache for future
    cache.set(product_id, data)

    return data
```

**Benefits**:
- ✅ Faster response times
- ✅ Reduced API costs
- ✅ Works offline with cached data

**Pitfalls**:
- ⚠️ Stale data if TTL too long
- ⚠️ Cache invalidation complexity
- ⚠️ Disk space usage

**Examples**:
- Google Drive Agent (caches file contents to avoid re-downloads)

---

## Integration Patterns

### Pattern 15: MCP Server Integration

**Purpose**: Access external services via Model Context Protocol

**Problem Solved**: Need external data/capabilities without custom implementation

**When to use**:
- ✅ Need documentation (Context7)
- ✅ Need web content (Fetch)
- ✅ Need specific integrations (Google Drive, Slack, etc.)

**Implementation**:

```typescript
// 1. Configure MCP server in .mcp.json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  }
}

// 2. Grant permissions in .claude/settings.local.json
{
  "permissions": {
    "allow": [
      "mcp__context7__get-library-docs",
      "mcp__fetch__fetch"
    ]
  }
}

// 3. Use in agent code
import { mcp } from '@anthropics/sdk';

// Fetch library documentation
const docs = await mcp.context7.getLibraryDocs({
  context7CompatibleLibraryID: '/anthropics/anthropic-sdk-typescript',
  topic: 'agents'
});

// Fetch web content
const content = await mcp.fetch.fetch({
  url: 'https://example.com/product-info',
  prompt: 'Extract product specifications'
});
```

**Benefits**:
- ✅ No custom integration code
- ✅ Maintained by providers
- ✅ Standardized protocol

**Pitfalls**:
- ⚠️ Dependency on external services
- ⚠️ Need to configure permissions
- ⚠️ MCP server must be available

**Examples**:
- FIA Analyzer (Fetch MCP server for web scraping)
- Many agents (Context7 for documentation)

---

## Pattern Selection Guide

**For Validation** → Always use Pattern 1 (Zod) or Pattern 2 (Pydantic)

**For Subagents**:
- Different domains → Pattern 3 (Specialization)
- Different complexity → Pattern 4 (Complexity-Based)
- Independent tasks → Pattern 5 (Parallel)

**For Data**:
- All agents → Pattern 6 (Mock Data First)
- Medium+ complexity → Pattern 7 (Service-Based Architecture)
- Small docs → Pattern 8 (Direct Context Passing)

**For Scoring**:
- Multi-factor assessment → Pattern 9 (Weighted Scoring)
- Product comparison → Pattern 10 (Multi-Criteria Comparison)

**For Architecture**:
- Need breadth + depth → Pattern 11 (Hybrid Multi-Agent)
- Service exists → Pattern 12 (External Service Integration)

**For Errors** → Always use Pattern 13 (Graceful Degradation)

**For Performance**:
- Repeated data → Pattern 14 (Caching)

**For Integration**:
- External services → Pattern 15 (MCP Server Integration)

---

## Summary

These 15 proven patterns provide:
- ✅ Production-tested solutions
- ✅ Clear implementation examples
- ✅ Guidance on when to use each
- ✅ Benefits and pitfalls documented
- ✅ Real-world examples from production agents

Apply these patterns during the **DESIGN** stage to build robust, maintainable agents.
