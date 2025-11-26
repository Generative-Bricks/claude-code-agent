

# Agent Builder Workflow Stages - Detailed Reference

This document provides comprehensive instructions, questioning templates, and guidance for each stage of the agent building workflow.

## Table of Contents

1. [Stage 1: BRAINSTORM](#stage-1-brainstorm)
2. [Stage 2: DESIGN](#stage-2-design)
3. [Stage 3: IMPLEMENT](#stage-3-implement)
4. [Stage 4: TEST](#stage-4-test)
5. [Stage 5: DOCUMENT](#stage-5-document)
6. [Stage 6: DEPLOY](#stage-6-deploy)
7. [Stage 7: OBSERVE](#stage-7-observe)
8. [Stage 8: EVALUATE](#stage-8-evaluate)
9. [Stage 9: ITERATE](#stage-9-iterate)

---

## Stage 1: BRAINSTORM

**Objective**: Define the problem space and make foundational architectural decisions

**Duration**: 30-60 minutes

**Output**: Clear problem statement, success criteria, SDK/language selection, complexity assessment

### Questioning Framework

#### 1.1 Use Case Definition

**Questions to Ask**:

```
Q1: What problem does this agent solve?
   - Be specific about the pain point
   - Who experiences this problem?
   - How is it currently being solved (if at all)?

Q2: Who are the primary users of this agent?
   - End users (consumers, clients)
   - Business users (employees, professionals)
   - Developers (internal tooling)
   - Other agents (agent-to-agent)

Q3: What makes this agent valuable?
   - Time savings (how much?)
   - Cost reduction (how much?)
   - Quality improvement (what metric?)
   - Capability enablement (what new capability?)

Q4: What would success look like?
   - Specific, measurable outcome
   - Timeline expectation
   - Adoption metric
```

**Example Interaction**:

```
User: "I want to build an agent to help financial advisors."

Agent: "Let me understand the specific problem you're solving.

Q1: What specific problem does this agent solve for financial advisors?

Q2: Are the primary users:
   a) The financial advisors themselves
   b) Their clients
   c) Both

Q3: What makes this valuable? Does it:
   a) Save time in a specific workflow
   b) Improve accuracy of analysis
   c) Enable new capabilities they don't have today
   d) Reduce compliance risk

Q4: What would success look like? For example:
   - 'Advisors can analyze products in 5 minutes instead of 30'
   - 'Reduces research time by 50%'
   - 'Enables advisors to handle 2x more client reviews'"
```

#### 1.2 Success Criteria Definition

**Questions to Ask**:

```
Q1: What are 3-5 measurable goals for this agent?
   - Each should be specific and measurable
   - Each should have a clear success threshold
   - Prioritize by importance

Q2: What are the key edge cases this agent must handle?
   - Missing data scenarios
   - Invalid input scenarios
   - API failures or timeouts
   - Conflicting requirements

Q3: What are acceptable limitations?
   - What is explicitly out of scope?
   - What assumptions are we making?
   - What requires human judgment?
   - What level of accuracy is acceptable?
```

**Guidance for Good Success Criteria**:

✅ **Good Examples**:
- "Agent can evaluate client suitability with 85%+ accuracy"
- "Agent responds to queries in <10 seconds 95% of the time"
- "Agent handles 20+ edge cases gracefully without errors"
- "Agent generates reports in 3 industry-standard formats"

❌ **Poor Examples**:
- "Agent works well" (not measurable)
- "Agent is fast" (no specific threshold)
- "Agent helps advisors" (too vague)
- "Agent is smart" (not quantifiable)

#### 1.3 SDK Selection

**Questions to Ask**:

```
Q1: Do you need multi-agent orchestration?
   - Multiple specialized agents working together
   - Agents handing off tasks to each other
   - Parallel execution of multiple agents
   → If YES: Consider OpenAI Agents, Strands, LangGraph
   → If NO: Claude SDK is sufficient

Q2: Do you need model flexibility (multiple providers)?
   - Ability to use different models for different tasks
   - Not locked to one provider (Anthropic/OpenAI)
   - Multi-cloud deployment
   → If YES: Consider Strands, LangGraph
   → If NO: Claude SDK or OpenAI Agents acceptable

Q3: Do you need complex state management?
   - Branching workflows with multiple paths
   - State persistence across sessions
   - Complex state transitions
   → If YES: Consider LangGraph, OpenAI Agents
   → If NO: Claude SDK sufficient

Q4: What are your performance requirements?
   - Need parallel execution for speed
   - Sub-second response times critical
   - Handle 1000s of requests/day
   → High volume: Consider async-capable frameworks

Q5: What's your team's language preference?
   - TypeScript ecosystem and tooling
   - Python data science libraries
   - Both equally comfortable
```

**Decision Tree**:

```
START → Need multi-agent orchestration?
         ├─ YES → Need model flexibility?
         │        ├─ YES → STRANDS or LANGGRAPH
         │        └─ NO → OPENAI AGENTS
         └─ NO → Complex state management?
                  ├─ YES → LANGGRAPH
                  └─ NO → Prefer Python or TypeScript?
                           ├─ PYTHON → CLAUDE SDK (Python)
                           └─ TYPESCRIPT → CLAUDE SDK (TypeScript)
```

**See**: `decision-frameworks.md` for complete SDK comparison matrix

#### 1.4 Language Selection

**Questions to Ask**:

```
Q1: What integrations are needed?
   - Web APIs (REST, GraphQL)
   - Databases (SQL, NoSQL)
   - Cloud services (AWS, GCP, Azure)
   - Data science libraries (NumPy, Pandas)
   - ML frameworks (TensorFlow, PyTorch)

Q2: What's your deployment target?
   - Web application (favor TypeScript)
   - Data pipeline (favor Python)
   - Serverless functions (either works)
   - Desktop application (either works)
   - Jupyter notebooks (favor Python)

Q3: What's your team's expertise?
   - Strong TypeScript experience
   - Strong Python experience
   - Equal comfort with both
   - Learning opportunity desired

Q4: What's your type safety preference?
   - Compile-time checking (TypeScript)
   - Runtime validation (Python with Pydantic)
   - Both (either language with proper tooling)
```

**Recommendation Matrix**:

| Factor | TypeScript | Python |
|--------|-----------|---------|
| Web/API integrations | ✅ Excellent | ✅ Good |
| Data science/ML | ⚠️ Limited | ✅ Excellent |
| Type safety | ✅ Compile-time | ✅ Runtime (Pydantic) |
| Async patterns | ✅ Native | ✅ asyncio |
| Package ecosystem | ✅ npm/Bun | ✅ PyPI/uv |
| Runtime speed | ✅ Bun (fast) | ⚠️ Python (slower) |
| Validation | Zod | Pydantic |

#### 1.5 Complexity Estimation

**Questions to Ask**:

```
Q1: How many distinct capabilities does the agent need?
   - 1-3 capabilities → Low complexity (1-3 tools)
   - 4-7 capabilities → Medium complexity (4-7 tools)
   - 8+ capabilities → High complexity (8+ tools)

Q2: Are there specialized sub-tasks requiring different approaches?
   - NO → No subagents needed
   - YES, 1-2 specialized tasks → Medium complexity (0-2 subagents)
   - YES, 3+ specialized tasks → High complexity (3+ subagents)

Q3: How complex is the conversation workflow?
   - Linear (A → B → C) → Low complexity
   - Branching (A → B or C → D) → Medium complexity
   - Complex state machine → High complexity

Q4: What data management is required?
   - Stateless (no persistence) → Low complexity
   - Simple state (in-memory) → Medium complexity
   - Complex state (database, sessions) → High complexity
```

**Complexity Level Definitions**:

**Low Complexity**:
- 1-3 tools
- 0 subagents
- Simple linear workflow (1-3 stages)
- Stateless or minimal state
- Examples: Document Q&A, simple search, basic calculator

**Medium Complexity**:
- 4-7 tools
- 0-2 subagents
- Multi-stage workflow with moderate branching
- State management (in-memory or simple persistence)
- Examples: Financial analysis, product comparison, content generation

**High Complexity**:
- 8+ tools
- 3+ subagents
- Complex orchestration with parallel execution
- Advanced state management (database, sessions)
- Examples: Multi-agent portfolio analysis, complex workflow automation

### Output Template for BRAINSTORM Stage

```markdown
## BRAINSTORM RESULTS

### Problem Statement
[One-sentence clear description of the problem being solved]

### Use Case
**Primary Users**: [Who uses this agent]
**Problem Solved**: [Specific pain point addressed]
**Value Delivered**: [Quantified value - time savings, cost reduction, etc.]

### Success Criteria
1. [Measurable goal #1]
2. [Measurable goal #2]
3. [Measurable goal #3]
4. [Measurable goal #4]
5. [Measurable goal #5]

### Acceptable Limitations
- [Limitation #1]
- [Limitation #2]

### Key Edge Cases
- [Edge case #1]
- [Edge case #2]

### Technical Decisions

**SDK Selected**: [Claude SDK / OpenAI Agents / Strands / LangGraph]
**Rationale**: [Why this SDK was chosen]

**Language Selected**: [TypeScript / Python]
**Rationale**: [Why this language was chosen]

**Complexity Level**: [Low / Medium / High]
**Estimated Tools**: [Number]
**Estimated Subagents**: [Number]

### Next Steps
- Proceed to DESIGN stage
- Define agent persona
- Design tool specifications
```

### Progressive Hints (Optional)

At the end of the BRAINSTORM stage, offer these optional standards checkpoints:

> **Hint 1**: "Apply 6 Principles decision framework?"
> → If yes: Reference `references/principles-framework.md` and check decisions against TRUTH, HONOR, EXCELLENCE, SERVE, PERSEVERE, SHARPEN

> **Hint 2**: "Classify with Agent Taxonomy (Level 0-4)?"
> → If yes: Reference `references/agent-taxonomy.md` to determine agent level (Reasoning → Connected → Strategic → Collaborative → Self-Evolving)

**How to apply**: If the user accepts a hint, briefly explain the relevant standard and help them apply it to their decisions. If declined, proceed to the next stage without enforcement.

---

## Stage 2: DESIGN

**Objective**: Create complete architectural blueprint with all specifications

**Duration**: 1-2 hours

**Output**: Agent persona, tool specifications, workflow design, data model, pattern selections

### Questioning Framework

#### 2.1 Agent Persona & Role

**Questions to Ask**:

```
Q1: What expertise does this agent have?
   - Domain knowledge (finance, healthcare, engineering)
   - Technical capabilities (analysis, calculation, research)
   - Communication style (formal, casual, technical)

Q2: How should the agent communicate?
   - Professional and formal
   - Friendly and conversational
   - Technical and precise
   - Adaptive based on user

Q3: What are the agent's limitations?
   - Cannot make final decisions (human-in-the-loop)
   - Cannot access certain data sources
   - Cannot guarantee 100% accuracy
   - Requires human verification for critical actions

Q4: What should the agent never do?
   - Never provide medical/legal advice (if applicable)
   - Never make financial decisions without human approval
   - Never access data without permission
   - Never override safety constraints
```

**Persona Template**:

```markdown
### Agent Persona

**Name**: [Agent name]

**Role**: [Primary role description]

**Expertise**:
- [Domain #1]: [Level of expertise]
- [Domain #2]: [Level of expertise]

**Communication Style**:
- Tone: [Formal / Conversational / Technical]
- Language: [Simple / Professional / Domain-specific]
- Personality: [Helpful / Analytical / Creative]

**Capabilities**:
- ✅ Can: [List what agent can do]
- ❌ Cannot: [List what agent cannot do]

**Limitations**:
- [Explicit limitation #1]
- [Explicit limitation #2]

**Safety Constraints**:
- [What agent will never do]
- [What requires human approval]
```

#### 2.2 Tool Design (Start with 3-5 tools)

**Questions to Ask for Each Tool**:

```
Q1: What is this tool's single purpose?
   - One clear, focused responsibility
   - If description has "and", consider splitting

Q2: What inputs does this tool need?
   - Required parameters
   - Optional parameters
   - Type for each parameter
   - Validation rules for each

Q3: What does this tool output?
   - Return type/structure
   - Success response format
   - Error response format

Q4: What errors can this tool encounter?
   - Invalid inputs
   - Missing data
   - External API failures
   - Timeouts

Q5: What validation is needed?
   - Type checking
   - Range validation
   - Format validation
   - Business rule validation
```

**Tool Specification Template**:

```markdown
### Tool: [tool_name]

**Purpose**: [One-sentence description of what this tool does]

**When to use**: [Specific scenarios where this tool should be used]

**Input Schema**:
```typescript
// TypeScript with Zod
{
  requiredParam: z.string().min(1),
  optionalParam: z.number().positive().optional(),
  enumParam: z.enum(['option1', 'option2', 'option3'])
}
```

```python
# Python with Pydantic
class ToolInput(BaseModel):
    required_param: str = Field(min_length=1)
    optional_param: Optional[int] = Field(None, gt=0)
    enum_param: Literal['option1', 'option2', 'option3']
```

**Output Schema**:
```typescript
{
  success: boolean,
  data: {
    // Success response structure
  },
  error?: string
}
```

**Error Conditions**:
- Invalid input: [What happens]
- Missing data: [What happens]
- API failure: [What happens]
- Timeout: [What happens]

**Example Usage**:
```
Input: { param: "value" }
Output: { success: true, data: { ... } }
```
```

**Tool Naming Conventions**:

✅ **Good Names** (verb + noun):
- `analyze_annuity_suitability`
- `calculate_income_projection`
- `search_products`
- `fetch_market_data`
- `generate_report`

❌ **Poor Names**:
- `processData` (too vague)
- `helper` (not descriptive)
- `tool1` (meaningless)
- `doStuff` (unprofessional)

#### 2.3 Workflow Design

**Questions to Ask**:

```
Q1: What are the distinct stages of the conversation?
   - Linear progression (A → B → C)
   - Branching paths (A → B or C)
   - Loops (A → B → back to A)

Q2: What information is collected at each stage?
   - User inputs
   - Tool outputs
   - Intermediate calculations
   - State updates

Q3: How does the workflow progress?
   - User-driven (waits for user input)
   - Agent-driven (autonomous progression)
   - Hybrid (some autonomous, some waiting)

Q4: What happens on failures?
   - Retry logic
   - Fallback strategies
   - Error messaging
   - Graceful degradation

Q5: When is the workflow complete?
   - Specific end condition
   - User satisfaction check
   - Deliverable produced
```

**Workflow Template**:

```markdown
### Workflow Stages

#### Stage 1: [Stage Name]
**Purpose**: [What this stage accomplishes]

**Activities**:
- [Activity #1]
- [Activity #2]

**Information Collected**:
- [Data point #1]
- [Data point #2]

**Tools Used**:
- `tool_name`: [Purpose in this stage]

**Progression Condition**:
- [When/how to move to next stage]

**Error Handling**:
- [What happens on failure]

---

#### Stage 2: [Stage Name]
[Same template as Stage 1]

---

[Repeat for all stages]
```

**Common Workflow Patterns**:

**Pattern 1: Discovery → Analysis → Recommendation**
```
1. Discovery: Gather user requirements and constraints
2. Analysis: Process data, perform calculations, evaluate options
3. Recommendation: Present findings, provide actionable next steps
```

**Pattern 2: Search → Extract → Transform → Present**
```
1. Search: Find relevant information/documents
2. Extract: Pull out key data points
3. Transform: Process and analyze extracted data
4. Present: Format and deliver results
```

**Pattern 3: Validate → Execute → Verify → Report**
```
1. Validate: Check inputs and preconditions
2. Execute: Perform primary operations
3. Verify: Confirm results meet criteria
4. Report: Generate output documentation
```

#### 2.4 Subagent Planning

**Questions to Ask**:

```
Q1: Are there specialized tasks requiring different expertise?
   - Deep domain analysis vs. quick calculations
   - Different reasoning depths
   - Different speed requirements

Q2: Which model for which task?
   - Sonnet: Complex reasoning, deep analysis, nuanced decisions
   - Haiku: Optimization, quick calculations, simple transformations

Q3: How do subagents communicate?
   - Parent agent delegates specific tasks
   - Subagents return structured results
   - Clear context passed to subagents

Q4: What context do subagents need?
   - Relevant data from parent conversation
   - Specific success criteria
   - Constraints and limitations
```

**Subagent Specification Template**:

```markdown
### Subagent: [Name]

**Model**: [Sonnet / Haiku]
**Rationale**: [Why this model for this task]

**Responsibility**: [What this subagent does]

**Triggered When**: [Conditions for delegation]

**Input Context**:
- [Data point #1]
- [Data point #2]

**Expected Output**:
- [Output structure]

**Success Criteria**:
- [How parent agent evaluates subagent result]

**Example Delegation**:
```
Parent → Subagent:
  "Analyze this portfolio for risk metrics: [data]
   Return: volatility, beta, VaR, concentration score"

Subagent → Parent:
  { volatility: 0.15, beta: 1.2, var_95: 0.08, concentration: 0.65 }
```
```

**Subagent Patterns**:

**Pattern: Specialization (Different domains)**
```
Main Agent (Orchestrator)
├── Risk Analysis Subagent (Sonnet)
├── Performance Analysis Subagent (Sonnet)
└── Optimization Subagent (Haiku)
```

**Pattern: Complexity (Different reasoning depth)**
```
Main Agent (Conversational)
├── Deep Analysis Subagent (Sonnet - complex reasoning)
└── Quick Calc Subagent (Haiku - fast calculations)
```

**Pattern: Parallel (Independent tasks)**
```
Main Agent
├── Task 1 Subagent → Run in parallel
├── Task 2 Subagent → Run in parallel
└── Task 3 Subagent → Run in parallel
Then: Combine results
```

#### 2.5 Data Model Design

**Questions to Ask**:

```
Q1: What are the core data entities?
   - User profiles
   - Products
   - Transactions
   - Analysis results

Q2: What data needs persistence?
   - Session state
   - User preferences
   - Historical data
   - Analysis results

Q3: What data relationships exist?
   - One-to-many
   - Many-to-many
   - Hierarchical

Q4: What validation is required?
   - Type constraints
   - Value ranges
   - Required vs. optional
   - Cross-field validation
```

**Data Model Template**:

```typescript
// TypeScript with Zod
const UserProfileSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  age: z.number().positive(),
  preferences: z.array(z.string()).optional()
});

type UserProfile = z.infer<typeof UserProfileSchema>;
```

```python
# Python with Pydantic
class UserProfile(BaseModel):
    id: UUID
    name: str = Field(min_length=1)
    age: int = Field(gt=0)
    preferences: Optional[List[str]] = None
```

#### 2.6 MCP Integration Planning

**Questions to Ask**:

```
Q1: What external data sources are needed?
   - Documentation (use Context7)
   - Web content (use Fetch)
   - Specific APIs (custom MCP server)

Q2: What MCP servers are available?
   - Check existing .mcp.json configuration
   - Identify which servers solve your needs

Q3: Do you need custom MCP tools?
   - Custom data sources
   - Proprietary APIs
   - Specialized integrations

Q4: How will MCP tools be used?
   - Direct agent access
   - Wrapper tools for simplified access
   - Cached/proxied for performance
```

#### 2.7 Pattern Selection

**Questions to Ask**:

```
Q1: Which validation pattern?
   → Always use Zod (TypeScript) or Pydantic (Python)

Q2: Do you need subagents?
   → If yes, use Specialization or Parallel pattern

Q3: Do you need external data?
   → Mock Data First pattern (always recommended)

Q4: Is this medium/high complexity?
   → Consider Service-Based Architecture

Q5: Do you have independent parallel tasks?
   → Use Parallel Execution pattern

Q6: Do you need ranking/scoring?
   → Use Weighted Scoring pattern

Q7: Are you working with small document collections?
   → Consider Direct Context Passing (no RAG)
```

**See**: `pattern-catalog.md` for complete pattern descriptions

### Output Template for DESIGN Stage

```markdown
## DESIGN RESULTS

[Include all templates filled out from sections 2.1-2.7]

### Agent Persona
[From template 2.1]

### Tool Specifications
[From template 2.2 - one per tool]

### Workflow Design
[From template 2.3]

### Subagent Plan
[From template 2.4 - if applicable]

### Data Model
[From template 2.5]

### MCP Integration
[From template 2.6 - if applicable]

### Pattern Selections
- Validation: Zod/Pydantic
- [Other patterns with rationale]

### Architecture Diagram
```
[Visual representation of agent architecture]
```

### Next Steps
- Proceed to IMPLEMENT stage (Phase 2)
- Generate scaffolding manifest
- Create project structure
```

### Progressive Hints (Optional)

At the end of the DESIGN stage, offer these optional standards checkpoints:

> **Hint 1**: "Apply A2A protocol standards for multi-agent communication?"
> → If yes: Reference `references/agent-taxonomy.md` for Agent-to-Agent protocol, message format, capability negotiation

> **Hint 2**: "Need memory strategy guidance (STM/LTM/Hybrid)?"
> → If yes: Reference `references/memory-strategies.md` for memory pattern selection based on use case

**How to apply**: If the user accepts a hint, guide them through applying the relevant standard to their architectural design.

---

## Stage 3: IMPLEMENT

**Objective**: Generate project structure and guide implementation

**Duration**: 4-12 hours (varies by complexity)

**Output**: Working agent with scaffolded code, configuration, and structure

### Implementation Sequence

#### 3.1 Project Setup

**Activities**:
1. Create directory structure
2. Initialize package manager (npm/Bun for TS, uv for Python)
3. Install dependencies
4. Configure environment (.env)
5. Setup git repository

**TypeScript Project Structure**:
```
project-name/
├── src/
│   ├── index.ts              # Main agent configuration
│   ├── types/
│   │   └── index.ts          # Type definitions & Zod schemas
│   ├── tools/
│   │   ├── tool1.ts
│   │   ├── tool2.ts
│   │   └── tool3.ts
│   └── data/
│       └── mockData.ts       # Mock data management
├── tests/
│   └── tools/
│       ├── tool1.test.ts
│       └── tool2.test.ts
├── .claude/
│   └── CLAUDE.md
├── package.json
├── tsconfig.json
├── .env.example
├── .gitignore
├── README.md
└── bun.lockb
```

**Python Project Structure**:
```
project-name/
├── src/
│   ├── __init__.py
│   ├── main.py               # Main agent configuration
│   ├── models/
│   │   └── __init__.py       # Pydantic models
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── tool1.py
│   │   ├── tool2.py
│   │   └── tool3.py
│   └── data/
│       └── mock_data.py
├── tests/
│   ├── __init__.py
│   └── test_tools.py
├── .claude/
│   └── CLAUDE.md
├── requirements.txt
├── pyproject.toml
├── .env.example
├── .gitignore
├── README.md
└── .venv/
```

#### 3.2 Tool Implementation

**Implementation Order**:
1. Implement tools one at a time
2. Add validation schema first
3. Implement core logic
4. Add error handling
5. Test individually
6. Move to next tool

**Tool Implementation Template (TypeScript)**:
```typescript
import { z } from 'zod';

// 1. Define input schema
const ToolNameInputSchema = z.object({
  param1: z.string().min(1),
  param2: z.number().positive().optional()
});

type ToolNameInput = z.infer<typeof ToolNameInputSchema>;

// 2. Define output type
interface ToolNameOutput {
  success: boolean;
  data?: {
    // Output structure
  };
  error?: string;
}

// 3. Implement tool function
export async function toolName(
  input: ToolNameInput
): Promise<ToolNameOutput> {
  try {
    // Validate input
    const validated = ToolNameInputSchema.parse(input);

    // Core logic
    // ...

    // Return success
    return {
      success: true,
      data: {
        // Output data
      }
    };
  } catch (error) {
    // Error handling
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error'
    };
  }
}

// 4. Export tool configuration
export const toolNameConfig = {
  name: 'tool_name',
  description: 'Clear description of what this tool does',
  input_schema: ToolNameInputSchema,
  function: toolName
};
```

**Tool Implementation Template (Python)**:
```python
from pydantic import BaseModel, Field
from typing import Optional, Literal

# 1. Define input model
class ToolNameInput(BaseModel):
    param1: str = Field(min_length=1)
    param2: Optional[int] = Field(None, gt=0)

# 2. Define output model
class ToolNameOutput(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None

# 3. Implement tool function
def tool_name(input_data: ToolNameInput) -> ToolNameOutput:
    try:
        # Core logic
        # ...

        # Return success
        return ToolNameOutput(
            success=True,
            data={
                # Output data
            }
        )
    except Exception as e:
        # Error handling
        return ToolNameOutput(
            success=False,
            error=str(e)
        )

# 4. Tool configuration
TOOL_CONFIG = {
    "name": "tool_name",
    "description": "Clear description of what this tool does",
    "input_schema": ToolNameInput,
    "function": tool_name
}
```

#### 3.3 Agent Configuration

**Agent Config Template (TypeScript - Claude SDK)**:
```typescript
import { Agent } from '@anthropics/sdk';
import { toolNameConfig } from './tools/toolName';

const agent = new Agent({
  name: 'Agent Name',
  model: 'claude-sonnet-4',
  instructions: `
    You are [agent persona].

    Your responsibilities:
    - [Responsibility #1]
    - [Responsibility #2]

    Your capabilities:
    - [Capability #1]
    - [Capability #2]

    Your limitations:
    - [Limitation #1]
    - [Limitation #2]

    Workflow:
    1. [Stage 1]: [Description]
    2. [Stage 2]: [Description]

    Always:
    - Validate user inputs
    - Handle errors gracefully
    - Provide clear explanations
    - Ask for clarification when needed
  `,
  tools: [
    toolNameConfig,
    // ... other tools
  ]
});

export default agent;
```

**Agent Config Template (Python - Claude SDK)**:
```python
from anthropic import Anthropic
from .tools import tool_name

client = Anthropic()

AGENT_CONFIG = {
    "name": "Agent Name",
    "model": "claude-sonnet-4",
    "instructions": """
        You are [agent persona].

        Your responsibilities:
        - [Responsibility #1]
        - [Responsibility #2]

        Your capabilities:
        - [Capability #1]
        - [Capability #2]

        Your limitations:
        - [Limitation #1]
        - [Limitation #2]

        Workflow:
        1. [Stage 1]: [Description]
        2. [Stage 2]: [Description]

        Always:
        - Validate user inputs
        - Handle errors gracefully
        - Provide clear explanations
        - Ask for clarification when needed
    """,
    "tools": [
        tool_name.TOOL_CONFIG,
        # ... other tools
    ]
}
```

#### 3.4 Mock Data Implementation

**Mock Data Best Practices**:
1. Structure identically to production data
2. Include variety (success cases, edge cases)
3. Use realistic values
4. Mark TODO for production replacement
5. Support both mock and real via env config

**Mock Data Template**:
```typescript
// mockData.ts
export const MOCK_PRODUCTS = [
  {
    id: 'PROD-001',
    name: 'Example Product 1',
    value: 100000,
    rate: 0.055,
    // ... other fields matching production API
  },
  // ... more examples
];

// TODO: Replace with real API call
export async function fetchProducts(): Promise<Product[]> {
  const USE_MOCK = process.env.USE_MOCK_DATA === 'true';

  if (USE_MOCK) {
    return MOCK_PRODUCTS;
  } else {
    // Production API call
    const response = await fetch('/api/products');
    return response.json();
  }
}
```

### Implementation Best Practices

**1. One Tool at a Time**
- Implement completely before moving to next
- Test individually
- Verify validation works
- Check error handling

**2. Error Handling from Day One**
- Try-catch blocks
- Specific error messages
- Graceful degradation
- User-friendly feedback

**3. Type Safety Throughout**
- Zod schemas for all inputs (TypeScript)
- Pydantic models for all data (Python)
- No `any` types in TypeScript
- Full type hints in Python

**4. Clear Naming**
- Descriptive function names
- Consistent naming conventions
- Self-documenting code
- Comments for "why" not "what"

**5. Test as You Build**
- Write tests alongside implementation
- Test happy paths
- Test error cases
- Test edge cases

### Progressive Hints (Optional)

At the end of the IMPLEMENT stage, offer these optional standards checkpoints:

> **Hint 1**: "Apply coding standards (lint/validation rules)?"
> → If yes: Reference `references/coding-standards.md` for language-specific linting, Zod/Pydantic validation patterns, error handling standards

**How to apply**: If the user accepts the hint, review the implementation against coding standards and suggest improvements where applicable.

---

## Stage 4: TEST

**Objective**: Verify agent behavior comprehensively

**Duration**: 2-4 hours

**Output**: Test suite covering tools, workflows, and edge cases

### Testing Framework

#### 4.1 Unit Tests (Individual Tools)

**Test Structure**:
```typescript
// tool1.test.ts
import { describe, test, expect } from 'bun:test';
import { toolName } from './tool1';

describe('toolName', () => {
  test('handles valid input successfully', async () => {
    const result = await toolName({
      param1: 'value',
      param2: 123
    });

    expect(result.success).toBe(true);
    expect(result.data).toBeDefined();
  });

  test('rejects invalid input', async () => {
    const result = await toolName({
      param1: '', // Invalid (too short)
      param2: -1  // Invalid (negative)
    });

    expect(result.success).toBe(false);
    expect(result.error).toBeDefined();
  });

  test('handles missing optional parameters', async () => {
    const result = await toolName({
      param1: 'value'
      // param2 omitted
    });

    expect(result.success).toBe(true);
  });
});
```

**What to Test**:
- ✅ Valid inputs → Success response
- ✅ Invalid inputs → Error handling
- ✅ Missing optional params → Defaults work
- ✅ Edge cases → Boundary conditions
- ✅ Error scenarios → Graceful failures

#### 4.2 Integration Tests (Complete Workflows)

**Test Structure**:
```typescript
describe('Complete Workflow', () => {
  test('Discovery → Analysis → Recommendation workflow', async () => {
    // Stage 1: Discovery
    const userInput = { /* user requirements */ };

    // Stage 2: Analysis
    const analysisResult = await agent.process(userInput);
    expect(analysisResult.stage).toBe('analysis_complete');

    // Stage 3: Recommendation
    const recommendation = await agent.generateRecommendation();
    expect(recommendation).toBeDefined();
    expect(recommendation.options).toHaveLength(3);
  });
});
```

#### 4.3 Edge Case Tests

**Critical Edge Cases**:
- Missing data scenarios
- Invalid type inputs
- API timeout simulations
- Conflicting requirements
- Extreme values (very large, very small, zero, negative)
- Special characters in strings
- Empty arrays/objects
- Null/undefined handling

#### 4.4 Performance Tests

**Metrics to Measure**:
- Response time per tool (target: <1s for simple, <5s for complex)
- End-to-end workflow time (target: <2min)
- Token usage per interaction
- Memory usage
- Subagent efficiency (if applicable)

#### 4.5 Manual QA Scenarios

**QA Checklist**:
- [ ] Happy path workflow completes successfully
- [ ] Agent provides clear explanations
- [ ] Error messages are helpful and actionable
- [ ] Agent asks for clarification when needed
- [ ] Output format is correct
- [ ] Agent stays within defined scope
- [ ] Agent respects limitations
- [ ] Conversation flow feels natural

### Progressive Hints (Optional)

At the end of the TEST stage, offer these optional standards checkpoints:

> **Hint 1**: "Apply testing pyramid (80/15/5 unit/integration/e2e)?"
> → If yes: Reference `references/coding-standards.md` for testing standards and ensure coverage ratios are appropriate

**How to apply**: If the user accepts the hint, review the test suite against the testing pyramid and suggest adjustments to test distribution.

---

## Stage 5: DOCUMENT

**Objective**: Create production-grade documentation

**Duration**: 1-2 hours

**Output**: Comprehensive CLAUDE.md, README.md, and supporting docs

### Documentation Components

#### 5.1 Agent CLAUDE.md

**Sections Required**:

```markdown
# [Agent Name]

**Purpose**: [One-sentence description]
**Framework**: [SDK name and version]
**Language**: [TypeScript/Python]
**Status**: [Development/Production-Ready/v1.0.0]

## Overview
[2-3 paragraphs describing what this agent does, why it exists, and who uses it]

## Directory Structure
```
[Complete directory tree]
```

## Features
- Feature #1 with description
- Feature #2 with description

## Tools
### 1. tool_name
**Purpose**: [Description]
**Inputs**: [Schema]
**Outputs**: [Schema]
**Example**: [Usage example]

[Repeat for all tools]

## Workflow
[Detailed workflow description with stages]

## Setup
[Step-by-step installation and configuration]

## Usage
[How to run the agent with examples]

## Testing
[How to run tests]

## Known Limitations
[Explicit limitations documented]

## Key Architectural Decisions
[Why certain choices were made]

## Future Enhancements
[Planned improvements]
```

#### 5.2 README.md

**Sections Required**:

```markdown
# [Agent Name]

[Brief description]

## Quick Start

```bash
# Installation
[commands]

# Configuration
[steps]

# Run
[commands]
```

## Features
- [Feature list]

## Requirements
- [Dependencies]

## Documentation
See [CLAUDE.md](.claude/CLAUDE.md) for complete documentation.

## License
[License information]
```

#### 5.3 Supporting Documentation

**Comparison Matrix Entry Template**:
```markdown
## [Agent Name] Comparison

**Framework**: [SDK]
**Language**: [Language]
**Complexity**: [Low/Medium/High]
**Tools**: [Count]
**Subagents**: [Count]
**LOC**: [Lines of code]

### Patterns Used
- [Pattern #1]
- [Pattern #2]

### What Worked Well
- [Success #1]
- [Success #2]

### Challenges
- [Challenge #1]
- [Challenge #2]

### Learnings
- [Learning #1]
- [Learning #2]
```

**Memory System Entry Template**:
```json
{
  "entity": "[Agent Name]",
  "entityType": "Agent",
  "observations": [
    "Built using [SDK] [version]",
    "Implements [Pattern #1], [Pattern #2]",
    "[Key architectural decision]",
    "[Performance characteristic]"
  ]
}
```

---

## Stage 9: ITERATE

**Objective**: Continuous improvement based on feedback

**Duration**: Ongoing

**Output**: Enhanced agent with bug fixes, new features, and updated docs

### Iteration Framework

#### 9.1 Feedback Collection

**Sources**:
- User feedback (direct comments, feature requests)
- Usage metrics (frequency, success rate, failure modes)
- Error logs (common errors, edge cases encountered)
- Performance data (slow operations, bottlenecks)

#### 9.2 Improvement Identification

**Categories**:
- Bugs (incorrect behavior, crashes)
- Performance (slow operations)
- UX (confusing prompts, unclear errors)
- Features (missing capabilities users request)
- Documentation (unclear instructions)

#### 9.3 Prioritization

**Priority Matrix**:
- P0: Critical bugs, security issues (fix immediately)
- P1: Major usability issues, common pain points (fix within 1 week)
- P2: Minor bugs, small improvements (fix within 1 month)
- P3: Nice-to-haves, future features (backlog)

#### 9.4 Incremental Updates

**Best Practices**:
- Make small, focused changes
- Test thoroughly after each change
- Update documentation immediately
- Commit often with clear messages
- Version appropriately (semver)

#### 9.5 Learning Capture

**Document**:
- What worked well
- What didn't work
- Unexpected challenges
- Creative solutions
- Patterns discovered
- Reusable components

**Update**:
- Pattern catalog (new patterns discovered)
- Comparison matrix (new metrics, learnings)
- Memory system (architectural decisions, insights)

### Progressive Hints (Optional)

At the end of the ITERATE stage, offer these optional standards checkpoints:

> **Hint 1**: "Setup feedback loops (user input → eval cases)?"
> → If yes: Reference `references/operations-guide.md` for feedback collection patterns and the feedback-to-eval-case pipeline

**How to apply**: If the user accepts the hint, help them establish a systematic process for converting user feedback into durable evaluation test cases.

---

## Stage 6: DEPLOY

**Objective**: Guide deployment with proper gates, rollout strategy, and rollback planning

**Duration**: 1-4 hours (configuration) + ongoing monitoring

**Output**: Deployment checklist, rollout plan, rollback procedures

> **Standards Reference**: See [operations-guide.md](./operations-guide.md) for full deployment standards

### Questioning Framework

#### 7.1 Deployment Readiness

**Questions to Ask**:

```
Q1: Have all offline evaluations passed?
   - Benchmarks (HELM, MTEB if applicable)
   - Safety testing (jailbreak resistance)
   - Red team review completed
   - Regression suite passing

Q2: What is your deployment target?
   - Staging (integration testing)
   - Canary (1% traffic)
   - Limited rollout (10% traffic)
   - Gradual (50% traffic)
   - Full production (100%)

Q3: What are your rollback triggers?
   - Error rate threshold (e.g., >1%)
   - Latency spike (e.g., p99 > 5s)
   - Guardrail breach (safety violation)
   - Quality score drop (e.g., <80%)

Q4: Is the agent identity registered?
   - SPIFFE ID assigned (if applicable)
   - Agent documented in inventory
   - Access controls configured
   - Dependencies documented
```

#### 7.2 Deployment Gates

**Gate Progression**:

```
1. Offline Evals → Benchmarks, safety testing
         ↓
2. Red Team → Adversarial testing
         ↓
3. Staging → Integration testing
         ↓
4. Production → Gradual rollout
```

**Gate Checklist**:
- [ ] **Offline Evals**: All benchmarks passing, safety tests passing
- [ ] **Red Team**: Adversarial testing completed, findings addressed
- [ ] **Staging**: Integration tests passing, no regressions
- [ ] **Production**: Rollout plan approved, monitoring configured

#### 7.3 Rollout Strategy

**Questions to Ask**:

```
Q1: What rollout phases?
   - Canary: 1% traffic for 1-4 hours
   - Limited: 10% traffic for 1-2 days
   - Gradual: 50% traffic for 1-2 days
   - Full: 100% traffic

Q2: What monitoring during rollout?
   - Error rates
   - Latency percentiles
   - Quality scores
   - User feedback

Q3: What triggers automatic rollback?
   - Define specific thresholds
   - Configure alerts
```

#### 7.4 Rollback Planning

**Rollback Checklist**:
- [ ] Previous version available for quick redirect
- [ ] Automatic triggers configured
- [ ] Manual rollback procedure documented
- [ ] Incident response plan in place
- [ ] Log preservation strategy defined

### Output Template

```markdown
## Deployment Plan

### Pre-Deployment Checklist
- [ ] Offline evaluations: [Status]
- [ ] Red team testing: [Status]
- [ ] Staging integration: [Status]

### Rollout Strategy
- **Phase 1 (Canary)**: 1% traffic for [duration]
- **Phase 2 (Limited)**: 10% traffic for [duration]
- **Phase 3 (Gradual)**: 50% traffic for [duration]
- **Phase 4 (Full)**: 100% traffic

### Rollback Triggers
- Error rate > [threshold]
- p99 latency > [threshold]
- Quality score < [threshold]
- Guardrail breach (automatic)

### Identity & Inventory
- Agent ID: [ID]
- Owner: [Team/Person]
- Dependencies: [List]
```

### Progressive Hint

> "Apply deployment gates checklist?"

---

## Stage 7: OBSERVE

**Objective**: Setup and configure observability infrastructure

**Duration**: 2-4 hours (initial setup) + ongoing tuning

**Output**: Observability configuration, dashboard setup, alert rules

> **Standards Reference**: See [operations-guide.md](./operations-guide.md) for OpenTelemetry standards

### Questioning Framework

#### 8.1 Observability Backend

**Questions to Ask**:

```
Q1: What observability backend?
   - Jaeger (open source)
   - Datadog (commercial)
   - AWS X-Ray (AWS native)
   - Grafana + Tempo (open source)
   - Custom solution

Q2: What trace exporter?
   - OTLP (OpenTelemetry Protocol)
   - Zipkin
   - Jaeger
   - Provider-specific
```

#### 8.2 Tracing Configuration

**Required Trace Taxonomy**:

```
ai.request → ai.plan → ai.retrieve → ai.generate
```

**Required Attributes**:
| Attribute | Description | Required |
|-----------|-------------|----------|
| `gen_ai.system` | LLM provider | Yes |
| `gen_ai.request.model` | Model ID | Yes |
| `ai.agent.id` | Agent identifier | Yes |
| `user.session.id` | User session | Yes |
| `trace.id` | Trace identifier | Yes |

**Questions to Ask**:

```
Q1: What span depth?
   - Request-level only (minimal)
   - Full trace (request → plan → retrieve → generate)
   - Custom spans for specific tools

Q2: What attributes to capture?
   - Required attributes (see above)
   - Tool-specific attributes
   - Business context
```

#### 8.3 Metrics Configuration

**Required Metrics**:

| Metric | Type | Percentiles |
|--------|------|-------------|
| Latency | Histogram | p50/p90/p95/p99 |
| Token usage | Counter | input/output |
| Cost | Counter | USD estimate |
| Quality | Gauge | eval_score |

**Questions to Ask**:

```
Q1: What latency thresholds?
   - p50: [target]
   - p90: [target]
   - p95: [target]
   - p99: [target]

Q2: What token budget?
   - Max tokens per request: [limit]
   - Max tokens per session: [limit]

Q3: What quality thresholds?
   - Minimum eval_score: [threshold]
   - Minimum win_rate: [threshold]
```

#### 8.4 Alerting Configuration

**Questions to Ask**:

```
Q1: What alerting thresholds?
   - Error rate: [threshold]
   - Latency spike: [threshold]
   - Token budget: [threshold]
   - Quality drop: [threshold]

Q2: Who receives alerts?
   - On-call team
   - Slack channel
   - PagerDuty
```

#### 8.5 Logging Standards

**Requirements**:
- Format: Structured JSON
- Content: Summaries, IDs, error codes
- **NEVER LOG**: PII, secrets, full user prompts

### Output Template

```markdown
## Observability Configuration

### Backend
- Provider: [Jaeger/Datadog/X-Ray/etc.]
- Exporter: [OTLP/Zipkin/etc.]

### Traces
- Taxonomy: ai.request → ai.plan → ai.retrieve → ai.generate
- Attributes: gen_ai.system, gen_ai.request.model, ai.agent.id, user.session.id

### Metrics
| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| p50 latency | [X]ms | [Y]ms |
| p99 latency | [X]ms | [Y]ms |
| Error rate | <[X]% | >[Y]% |
| Token usage | <[X] | >[Y] |

### Alerts
- Recipient: [Team/Channel]
- Escalation: [Policy]
```

### Progressive Hint

> "Setup OpenTelemetry observability?"

---

## Stage 8: EVALUATE

**Objective**: Design evaluation framework with offline, online, and human feedback loops

**Duration**: 2-4 hours (design) + ongoing operation

**Output**: Evaluation plan with metrics, thresholds, and feedback loops

> **Standards Reference**: See [operations-guide.md](./operations-guide.md) for evaluation framework

### Questioning Framework

#### 9.1 Success Metrics (Outside-In)

**Questions to Ask**:

```
Q1: How will you measure success? (Black box - outcome focused)
   - Acceptance Rate: % suggestions accepted
   - Win Rate: A/B test performance vs baseline
   - Success Rate: Task completion %
   - User satisfaction: Thumbs up ratio

Q2: What are your success targets?
   - Acceptance Rate: [target]%
   - Win Rate: >[target]%
   - Success Rate: >[target]%
```

#### 9.2 Process Metrics (Inside-Out)

**Questions to Ask**:

```
Q1: How will you measure process quality? (Glass box - process focused)
   - Faithfulness: Answer matches context
   - Context Precision: Relevant context retrieved
   - Tool Efficiency: Appropriate tool usage

Q2: What analysis methods?
   - Tracing analysis
   - RAGAS metrics (for RAG agents)
   - Latency/cost analysis
```

#### 9.3 Offline Evaluation (Pre-Deploy)

**Questions to Ask**:

```
Q1: What benchmarks?
   - HELM (general)
   - MTEB (embeddings)
   - Domain-specific benchmarks
   - Custom eval dataset

Q2: What RAG metrics? (if applicable)
   - Faithfulness
   - Context Precision
   - Context Recall

Q3: What safety testing?
   - Jailbreak resistance
   - Harmful output detection
   - PII leakage testing
```

#### 9.4 Online Evaluation (Post-Deploy)

**Questions to Ask**:

```
Q1: What online evaluation strategy?
   - A/B testing: Randomized assignment
   - Shadow traffic: Run candidate silently
   - Canary: Gradual rollout with monitoring
   - None (offline only)

Q2: What statistical significance?
   - Sample size requirements
   - Confidence level (95%/99%)
   - Duration for A/B tests
```

#### 9.5 Human Feedback

**Questions to Ask**:

```
Q1: How will you collect human feedback?
   - In-product: Thumbs up/down
   - Review queues: Expert review
   - Surveys: Periodic user surveys

Q2: How will you use feedback?
   - Convert to eval cases (regression tests)
   - Few-shot tuning (improve prompts)
   - Identify improvement areas
```

### Feedback Loop Pipeline

```
Collect (API/UI) → Convert (Eval Cases) → Optimize (Prompts) → Update (Deploy)
```

### Output Template

```markdown
## Evaluation Plan

### Success Metrics (Outside-In)
| Metric | Target | Measurement |
|--------|--------|-------------|
| Acceptance Rate | >[X]% | [Method] |
| Win Rate | >[X]% | A/B test |
| Success Rate | >[X]% | [Method] |

### Process Metrics (Inside-Out)
| Metric | Target | Tool |
|--------|--------|------|
| Faithfulness | >[X] | RAGAS |
| Context Precision | >[X] | RAGAS |
| Tool Efficiency | >[X]% | Tracing |

### Offline Evaluation
- Benchmarks: [List]
- Safety tests: [List]
- Eval dataset: [Location]

### Online Evaluation
- Strategy: [A/B / Shadow / Canary]
- Sample size: [N]
- Duration: [Days]

### Human Feedback
- Collection: [In-product / Review queue]
- Processing: [Eval case conversion]
- Frequency: [Daily / Weekly]
```

### Progressive Hint

> "Define evaluation framework (Offline/Online/Human)?"

---

## Summary

This comprehensive 9-stage workflow ensures:
- ✅ Thorough planning before coding (BRAINSTORM)
- ✅ Informed architectural decisions (DESIGN)
- ✅ Production-grade implementation (IMPLEMENT)
- ✅ Comprehensive testing (TEST)
- ✅ Complete documentation (DOCUMENT)
- ✅ Safe deployment practices (DEPLOY)
- ✅ Full observability (OBSERVE)
- ✅ Data-driven evaluation (EVALUATE)
- ✅ Continuous improvement (ITERATE)

Each stage builds on the previous, creating a robust, well-documented, production-ready agent with full lifecycle management.
