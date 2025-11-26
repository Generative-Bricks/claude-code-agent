# Common Tools Catalog

**Purpose:** Document reusable tool patterns discovered across agents to accelerate development and maintain consistency.

**Usage:** Before building a new tool, check this catalog to see if a similar pattern already exists. Reuse and adapt rather than reinvent.

---

## 📖 How to Use This Catalog

### When Building a New Agent
1. Review this catalog for similar tool patterns
2. Adapt proven patterns to your use case
3. Focus on the "Pattern" and "Implementation Tips" sections
4. Avoid common pitfalls listed for each pattern

### When Adding a New Pattern
1. Implement the tool in your agent first
2. Extract the reusable pattern
3. Document with clear examples
4. Include TypeScript and Python versions when possible
5. Share learnings and gotchas

---

## 🛠️ Tool Categories

- [Analysis Tools](#analysis-tools) - Evaluate, score, assess
- [Calculation Tools](#calculation-tools) - Compute, project, estimate
- [Comparison Tools](#comparison-tools) - Compare options, rank alternatives
- [Retrieval Tools](#retrieval-tools) - Fetch data from external sources
- [Validation Tools](#validation-tools) - Verify, check, validate inputs
- [Transformation Tools](#transformation-tools) - Convert, format, restructure data

---

## Analysis Tools

### Pattern: Suitability Scoring

**Purpose:** Evaluate how well something matches given criteria using a weighted scoring system.

**Used In:**
- Financial Advisor Agent (`analyze_annuity_suitability`)

**Pattern:**
```typescript
// Input: Entity to evaluate + criteria
interface SuitabilityInput {
  entity: EntityToEvaluate;
  criteria: EvaluationCriteria;
  weights?: Partial<Record<keyof EvaluationCriteria, number>>;
}

// Output: Score + detailed breakdown
interface SuitabilityOutput {
  overallScore: number; // 0-100
  breakdown: Record<string, {
    score: number;
    weight: number;
    rationale: string;
  }>;
  recommendation: 'highly_suitable' | 'suitable' | 'marginally_suitable' | 'not_suitable';
  reasoning: string;
}
```

**Implementation (TypeScript with Zod):**
```typescript
import { z } from 'zod';

// Define input schema
const SuitabilityInputSchema = z.object({
  entity: z.object({
    // Entity-specific fields
    age: z.number().int().min(0).max(120),
    riskTolerance: z.enum(['low', 'medium', 'high']),
    // ... more fields
  }),
  criteria: z.object({
    minAge: z.number().optional(),
    maxAge: z.number().optional(),
    requiredRiskTolerance: z.enum(['low', 'medium', 'high']).optional(),
    // ... more criteria
  }),
  weights: z.record(z.number().min(0).max(1)).optional(),
});

// Tool implementation
async function analyzeSuitability(
  input: z.infer<typeof SuitabilityInputSchema>
): Promise<SuitabilityOutput> {
  // Validate input
  const validated = SuitabilityInputSchema.parse(input);

  // Default weights if not provided
  const weights = validated.weights || {
    age: 0.3,
    riskTolerance: 0.4,
    // ... more default weights
  };

  // Calculate individual scores
  const scores: Record<string, { score: number; weight: number; rationale: string }> = {};

  // Age score
  if (validated.criteria.minAge && validated.criteria.maxAge) {
    const ageInRange =
      validated.entity.age >= validated.criteria.minAge &&
      validated.entity.age <= validated.criteria.maxAge;
    scores.age = {
      score: ageInRange ? 100 : 0,
      weight: weights.age,
      rationale: ageInRange
        ? `Age ${validated.entity.age} is within target range`
        : `Age ${validated.entity.age} is outside target range`,
    };
  }

  // Risk tolerance score
  // ... calculate other scores

  // Calculate weighted overall score
  const overallScore = Object.values(scores).reduce(
    (sum, item) => sum + (item.score * item.weight),
    0
  );

  // Determine recommendation
  let recommendation: SuitabilityOutput['recommendation'];
  if (overallScore >= 80) recommendation = 'highly_suitable';
  else if (overallScore >= 60) recommendation = 'suitable';
  else if (overallScore >= 40) recommendation = 'marginally_suitable';
  else recommendation = 'not_suitable';

  return {
    overallScore,
    breakdown: scores,
    recommendation,
    reasoning: generateReasoning(scores, overallScore),
  };
}
```

**Implementation Tips:**
- Use weighted scoring for flexibility
- Provide detailed breakdown, not just a final score
- Include rationale for each criterion
- Use clear recommendation categories
- Make weights configurable

**Common Pitfalls:**
- ❌ Returning only a number without explanation
- ❌ Hard-coding weights instead of making them configurable
- ❌ Not validating input ranges
- ❌ Missing edge cases (e.g., missing optional criteria)

---

## Calculation Tools

### Pattern: Projection Calculator

**Purpose:** Calculate future values based on current inputs and various parameters.

**Used In:**
- Financial Advisor Agent (`calculate_annuity_payout`)

**Pattern:**
```typescript
// Input: Current state + projection parameters
interface ProjectionInput {
  initialValue: number;
  parameters: ProjectionParameters;
  timeframe: {
    years: number;
    periodsPerYear?: number; // monthly, quarterly, etc.
  };
}

// Output: Projected values over time
interface ProjectionOutput {
  projections: Array<{
    period: number;
    periodLabel: string; // "Year 1", "Month 3", etc.
    value: number;
    breakdown?: Record<string, number>; // Optional component breakdown
  }>;
  summary: {
    totalValue: number;
    totalGrowth: number;
    averagePerPeriod: number;
  };
}
```

**Implementation (TypeScript with Zod):**
```typescript
import { z } from 'zod';

const ProjectionInputSchema = z.object({
  initialValue: z.number().positive(),
  parameters: z.object({
    rate: z.number().min(0).max(100), // Annual percentage rate
    inflationRate: z.number().min(0).max(100).optional(),
    // ... more parameters
  }),
  timeframe: z.object({
    years: z.number().int().positive(),
    periodsPerYear: z.number().int().positive().optional().default(1),
  }),
});

async function calculateProjection(
  input: z.infer<typeof ProjectionInputSchema>
): Promise<ProjectionOutput> {
  const validated = ProjectionInputSchema.parse(input);

  const projections: ProjectionOutput['projections'] = [];
  const totalPeriods = validated.timeframe.years * validated.timeframe.periodsPerYear;
  const ratePerPeriod = validated.parameters.rate / validated.timeframe.periodsPerYear / 100;

  let currentValue = validated.initialValue;

  for (let period = 1; period <= totalPeriods; period++) {
    // Calculate growth for this period
    const growth = currentValue * ratePerPeriod;
    currentValue += growth;

    // Apply inflation if provided
    if (validated.parameters.inflationRate) {
      const inflationPerPeriod = validated.parameters.inflationRate / validated.timeframe.periodsPerYear / 100;
      currentValue *= (1 - inflationPerPeriod);
    }

    projections.push({
      period,
      periodLabel: generatePeriodLabel(period, validated.timeframe.periodsPerYear),
      value: Math.round(currentValue * 100) / 100, // Round to 2 decimal places
      breakdown: {
        growth,
        inflation: validated.parameters.inflationRate
          ? currentValue * (validated.parameters.inflationRate / validated.timeframe.periodsPerYear / 100)
          : 0,
      },
    });
  }

  const totalGrowth = currentValue - validated.initialValue;

  return {
    projections,
    summary: {
      totalValue: currentValue,
      totalGrowth,
      averagePerPeriod: totalGrowth / totalPeriods,
    },
  };
}
```

**Implementation Tips:**
- Support different time periods (monthly, quarterly, annual)
- Provide both period-by-period and summary data
- Round financial values appropriately
- Consider compounding effects
- Include optional breakdown of components

**Common Pitfalls:**
- ❌ Not accounting for compounding
- ❌ Floating-point precision errors in financial calculations
- ❌ Missing period labels (users need context)
- ❌ Not handling edge cases (zero values, negative rates)

---

## Comparison Tools

### Pattern: Multi-Criteria Comparison

**Purpose:** Compare multiple options across various criteria with weighted rankings.

**Used In:**
- Financial Advisor Agent (`compare_annuity_types`)

**Pattern:**
```typescript
// Input: Options to compare + comparison criteria
interface ComparisonInput {
  options: Array<OptionToCompare>;
  criteria: Array<{
    name: string;
    weight: number; // 0-1
    preferHigher: boolean; // true = higher is better
  }>;
}

// Output: Ranked comparison with scores
interface ComparisonOutput {
  rankings: Array<{
    option: OptionToCompare;
    overallScore: number;
    rank: number;
    criteriaScores: Record<string, {
      rawValue: number | string;
      normalizedScore: number; // 0-100
      weightedScore: number;
    }>;
  }>;
  winner: OptionToCompare;
  summary: string;
}
```

**Implementation (TypeScript with Zod):**
```typescript
import { z } from 'zod';

const ComparisonInputSchema = z.object({
  options: z.array(z.object({
    id: z.string(),
    name: z.string(),
    attributes: z.record(z.union([z.number(), z.string()])),
  })).min(2),
  criteria: z.array(z.object({
    name: z.string(),
    weight: z.number().min(0).max(1),
    preferHigher: z.boolean(),
  })),
});

async function compareOptions(
  input: z.infer<typeof ComparisonInputSchema>
): Promise<ComparisonOutput> {
  const validated = ComparisonInputSchema.parse(input);

  // Normalize weights to sum to 1
  const totalWeight = validated.criteria.reduce((sum, c) => sum + c.weight, 0);
  const normalizedCriteria = validated.criteria.map(c => ({
    ...c,
    weight: c.weight / totalWeight,
  }));

  // Calculate scores for each option
  const rankings = validated.options.map(option => {
    const criteriaScores: Record<string, any> = {};
    let overallScore = 0;

    normalizedCriteria.forEach(criterion => {
      const rawValue = option.attributes[criterion.name];

      // Normalize the raw value to 0-100 scale
      const normalizedScore = normalizeValue(
        rawValue,
        validated.options.map(o => o.attributes[criterion.name]),
        criterion.preferHigher
      );

      const weightedScore = normalizedScore * criterion.weight;
      overallScore += weightedScore;

      criteriaScores[criterion.name] = {
        rawValue,
        normalizedScore,
        weightedScore,
      };
    });

    return {
      option,
      overallScore,
      rank: 0, // Will be set after sorting
      criteriaScores,
    };
  });

  // Sort by overall score and assign ranks
  rankings.sort((a, b) => b.overallScore - a.overallScore);
  rankings.forEach((ranking, index) => {
    ranking.rank = index + 1;
  });

  return {
    rankings,
    winner: rankings[0].option,
    summary: generateComparisonSummary(rankings),
  };
}

// Helper function to normalize values
function normalizeValue(
  value: number | string,
  allValues: Array<number | string>,
  preferHigher: boolean
): number {
  // Handle numeric values
  if (typeof value === 'number') {
    const numericValues = allValues.filter(v => typeof v === 'number') as number[];
    const min = Math.min(...numericValues);
    const max = Math.max(...numericValues);

    if (max === min) return 50; // All values are the same

    let normalized = ((value - min) / (max - min)) * 100;
    return preferHigher ? normalized : (100 - normalized);
  }

  // Handle categorical values (simple presence/absence)
  return 50; // Neutral score for non-numeric comparisons
}
```

**Implementation Tips:**
- Normalize criteria to comparable scales
- Support both numeric and categorical criteria
- Provide detailed breakdown, not just rankings
- Allow weighted criteria
- Generate human-readable summary

**Common Pitfalls:**
- ❌ Not normalizing values before comparing
- ❌ Forgetting to handle ties in rankings
- ❌ Ignoring user preferences (preferHigher/preferLower)
- ❌ Not validating that criteria exist in all options

---

## Retrieval Tools

### Pattern: Rate/Data Fetcher

**Purpose:** Fetch current data from external sources (APIs, databases, market data).

**Used In:**
- Financial Advisor Agent (`fetch_annuity_rates`)

**Pattern:**
```typescript
// Input: Query parameters
interface FetchInput {
  filters?: Record<string, any>;
  limit?: number;
  sortBy?: string;
}

// Output: Retrieved data with metadata
interface FetchOutput {
  data: Array<DataItem>;
  metadata: {
    source: string;
    timestamp: string;
    count: number;
    hasMore: boolean;
  };
  error?: string;
}
```

**Implementation (TypeScript with Zod):**
```typescript
import { z } from 'zod';

const FetchInputSchema = z.object({
  filters: z.record(z.any()).optional(),
  limit: z.number().int().positive().max(100).optional().default(10),
  sortBy: z.string().optional(),
});

async function fetchData(
  input: z.infer<typeof FetchInputSchema>
): Promise<FetchOutput> {
  const validated = FetchInputSchema.parse(input);

  try {
    // TODO: Replace with actual API call
    // const response = await fetch(`https://api.example.com/data?${params}`);
    // const data = await response.json();

    // Mock data for development
    const mockData = generateMockData(validated);

    return {
      data: mockData.slice(0, validated.limit),
      metadata: {
        source: 'Mock Data (replace with real API)',
        timestamp: new Date().toISOString(),
        count: mockData.length,
        hasMore: mockData.length > validated.limit,
      },
    };
  } catch (error) {
    return {
      data: [],
      metadata: {
        source: 'Error',
        timestamp: new Date().toISOString(),
        count: 0,
        hasMore: false,
      },
      error: error instanceof Error ? error.message : 'Unknown error occurred',
    };
  }
}
```

**Implementation Tips:**
- Include clear TODO comments for API integration
- Use mock data during development
- Return metadata (source, timestamp, count)
- Handle errors gracefully
- Consider rate limiting and caching
- Document where to replace mock data

**Common Pitfalls:**
- ❌ Not handling API failures
- ❌ Missing timeout handling
- ❌ No fallback data or error messages
- ❌ Forgetting to document mock data vs real data
- ❌ Not including data freshness timestamp

---

## Validation Tools

### Pattern: Input Validator

**Purpose:** Validate complex inputs before processing.

**Pattern:**
```typescript
// Input: Data to validate + validation rules
interface ValidationInput {
  data: unknown;
  rules: ValidationRules;
}

// Output: Validation result with detailed errors
interface ValidationOutput {
  isValid: boolean;
  errors: Array<{
    field: string;
    message: string;
    code: string;
  }>;
  warnings?: Array<{
    field: string;
    message: string;
  }>;
}
```

**Implementation (TypeScript with Zod):**
```typescript
import { z } from 'zod';

// Zod provides excellent validation out of the box
const UserInputSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  age: z.number().int().min(18, 'Must be at least 18').max(120),
  email: z.string().email('Invalid email format'),
  // ... more fields
});

function validateInput(data: unknown): ValidationOutput {
  try {
    UserInputSchema.parse(data);
    return {
      isValid: true,
      errors: [],
    };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return {
        isValid: false,
        errors: error.errors.map(err => ({
          field: err.path.join('.'),
          message: err.message,
          code: err.code,
        })),
      };
    }

    return {
      isValid: false,
      errors: [{
        field: 'unknown',
        message: 'Validation failed',
        code: 'UNKNOWN_ERROR',
      }],
    };
  }
}
```

**Implementation Tips:**
- Use Zod for TypeScript (provides both types and validation)
- Use Pydantic for Python (similar benefits)
- Provide specific error messages
- Include field paths for nested errors
- Consider warnings vs errors

**Common Pitfalls:**
- ❌ Generic error messages ("Invalid input")
- ❌ Not indicating which field failed
- ❌ Throwing errors instead of returning validation results
- ❌ Missing edge case validation

---

## Transformation Tools

### Pattern: Data Formatter

**Purpose:** Transform data from one format to another.

**Pattern:**
```typescript
// Input: Data + target format
interface TransformInput {
  data: SourceFormat;
  targetFormat: 'json' | 'csv' | 'xml' | 'markdown' | 'html';
  options?: FormatOptions;
}

// Output: Transformed data
interface TransformOutput {
  data: string;
  format: string;
  size: number; // bytes
}
```

**Implementation Tips:**
- Support multiple output formats
- Preserve data integrity
- Handle special characters
- Include size/metadata
- Allow format-specific options

---

## Best Practices Across All Tools

### Input Validation
✅ **Always validate inputs** with schemas (Zod, Pydantic)
✅ **Provide clear error messages** with field names
✅ **Set sensible defaults** for optional parameters

### Output Structure
✅ **Return structured data** (not just strings)
✅ **Include metadata** (timestamp, source, version)
✅ **Provide detailed breakdowns** not just summary values

### Error Handling
✅ **Handle all errors gracefully** (no uncaught exceptions)
✅ **Return actionable error messages**
✅ **Include error codes** for programmatic handling
✅ **Log errors** for debugging (but don't expose sensitive data)

### Documentation
✅ **Document input/output schemas** clearly
✅ **Provide usage examples** in docstrings
✅ **Explain edge cases** and limitations
✅ **Include TypeScript type definitions** or Python type hints

### Testing
✅ **Test happy path** (valid inputs)
✅ **Test error cases** (invalid inputs, missing data)
✅ **Test edge cases** (boundary values, empty inputs)
✅ **Test performance** for data-heavy operations

---

## Quick Reference: Choosing a Tool Pattern

| Need to... | Use Pattern | Example |
|------------|-------------|---------|
| Evaluate fit | Suitability Scoring | Client suitability, match scoring |
| Predict future | Projection Calculator | Revenue forecast, growth projection |
| Rank options | Multi-Criteria Comparison | Product comparison, vendor selection |
| Get external data | Rate/Data Fetcher | Market rates, API data |
| Check validity | Input Validator | Form validation, data verification |
| Convert format | Data Formatter | JSON to CSV, data export |

---

## Contributing New Patterns

When you discover a reusable pattern:

1. **Extract the pattern** from your working implementation
2. **Generalize it** (remove use-case-specific details)
3. **Document clearly**:
   - Purpose
   - Used in (which agents)
   - Pattern (interfaces/schemas)
   - Implementation (working code)
   - Tips
   - Pitfalls
4. **Add to appropriate category**
5. **Update memory system** (`docs/memory/memory.jsonl`)

---

*Part of the claude-code-agent repository*
*See root CLAUDE.md for repository structure*
*See docs/workflows/agent-ideation-workflow.md for building new agents*
