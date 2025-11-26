# Agent Builder Decision Frameworks

This document provides comprehensive frameworks for making critical architectural decisions when building AI agents.

## Table of Contents

1. [SDK Selection Framework](#sdk-selection-framework)
2. [Language Selection Framework](#language-selection-framework)
3. [Complexity Assessment Framework](#complexity-assessment-framework)
4. [Tool Design Framework](#tool-design-framework)
5. [Subagent Decision Framework](#subagent-decision-framework)
6. [State Management Framework](#state-management-framework)
7. [Testing Strategy Framework](#testing-strategy-framework)

---

## SDK Selection Framework

### Complete Comparison Matrix

| Feature | Claude SDK | OpenAI Agents | Strands Agents | LangGraph |
|---------|-----------|---------------|----------------|-----------|
| **Primary Provider** | Anthropic only | OpenAI only | Multi-provider | Multi-provider |
| **Best Models** | Claude 3.5 Sonnet, Opus | GPT-4, GPT-4 Turbo | Any (Claude, GPT, Gemini) | Any (via LangChain) |
| **Multi-Agent Support** | ⚠️ Basic (subagents) | ✅ Excellent (parallel + handoffs) | ✅ Good | ✅ Good |
| **Parallel Execution** | ⚠️ Manual | ✅ Built-in | ⚠️ Manual | ⚠️ Manual |
| **State Management** | ⚠️ Basic | ✅ SQLite session memory | ⚠️ Basic | ✅ Excellent (state graphs) |
| **Workflow Complexity** | ⚠️ Simple workflows | ✅ Complex orchestration | ✅ Moderate | ✅ Complex with branching |
| **Language Support** | TypeScript, Python | Python | TypeScript, Python | Python only |
| **MCP Integration** | ✅ Native | ❌ None | ✅ Extensive | ⚠️ Possible |
| **Session Persistence** | ⚠️ Manual | ✅ Built-in (SQLite) | ⚠️ Manual | ✅ Built-in |
| **Learning Curve** | ✅ Easy | ✅ Easy | ✅ Moderate | ⚠️ Steep |
| **Documentation** | ✅ Excellent | ✅ Excellent | ✅ Good | ✅ Excellent |
| **Community** | Growing | Large | Growing | Large (LangChain) |
| **Production Ready** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Deployment** | Simple | Simple | Lightweight | Moderate |
| **Cost Model** | Pay per token | Pay per token | Pay per token (any provider) | Pay per token |

### Decision Tree

```
START
│
├─ Need multi-agent orchestration?
│  ├─ YES → Need model flexibility?
│  │        ├─ YES → STRANDS or LANGGRAPH
│  │        │        └─ Complex state machine?
│  │        │           ├─ YES → LANGGRAPH
│  │        │           └─ NO → STRANDS
│  │        └─ NO → Need parallel + handoffs?
│  │                ├─ YES → OPENAI AGENTS
│  │                └─ NO → CLAUDE SDK with subagents
│  │
│  └─ NO → Complex state management needed?
│           ├─ YES → LANGGRAPH
│           └─ NO → Provider preference?
│                    ├─ Anthropic → CLAUDE SDK
│                    ├─ OpenAI → OPENAI AGENTS
│                    └─ Multi → STRANDS
```

### Detailed SDK Profiles

#### Claude SDK

**Best For**:
- Conversational agents requiring excellent reasoning
- Single-agent applications with optional subagents
- Projects where Anthropic's Claude models are preferred
- Rapid prototyping and simple workflows
- Extensive MCP server integration

**Strengths**:
- ✅ Excellent reasoning capabilities (Claude Sonnet 4+)
- ✅ Simple, clean API
- ✅ Native MCP support
- ✅ Both TypeScript and Python support
- ✅ Fast development cycle
- ✅ Good documentation

**Limitations**:
- ⚠️ Anthropic models only
- ⚠️ Basic multi-agent orchestration
- ⚠️ Manual state persistence
- ⚠️ Manual parallel execution

**Use Cases**:
- Financial advisor agents (analysis and recommendations)
- Document Q&A agents
- Content generation agents
- Research assistants
- FIA product analyzers

**Example Projects**:
- Financial Advisor Agent (TypeScript)
- FIA Analyzer (Python)
- OpportunityIQ Client Matcher (Python)

**Code Complexity**: Low to Medium
**Learning Time**: 1-2 days
**Production Readiness**: ✅ Excellent

---

#### OpenAI Agents SDK

**Best For**:
- Multi-agent collaboration systems
- Agents requiring parallel + handoff patterns
- Projects benefiting from built-in session memory
- Complex agent orchestration
- OpenAI model ecosystem

**Strengths**:
- ✅ Excellent multi-agent coordination
- ✅ Built-in parallel execution (`asyncio.gather()`)
- ✅ SQLite session memory out of the box
- ✅ Handoff patterns for deep delegation
- ✅ Hybrid pattern (parallel + depth)
- ✅ Clean separation of concerns

**Limitations**:
- ⚠️ OpenAI models only (GPT-4, GPT-4 Turbo)
- ⚠️ Python only (no TypeScript)
- ⚠️ No native MCP support
- ⚠️ Newer SDK (evolving rapidly)

**Use Cases**:
- Portfolio analysis with specialist agents
- Multi-perspective content review
- Complex research with specialized roles
- Collaborative problem solving
- Systems requiring conversation history

**Example Projects**:
- Portfolio Collaboration (5 specialist agents)

**Code Complexity**: Medium
**Learning Time**: 2-3 days
**Production Readiness**: ✅ Excellent
**Performance**: 65% faster with parallel execution

---

#### Strands Agents

**Best For**:
- Model-agnostic architectures
- Lightweight deployments
- Extensive integration needs (Google Drive, Slack, etc.)
- Multi-provider requirements
- Flexible MCP usage

**Strengths**:
- ✅ Multi-provider support (Claude, GPT, Gemini, etc.)
- ✅ Extensive MCP integration
- ✅ Lightweight architecture
- ✅ TypeScript and Python support
- ✅ Model-driven approach
- ✅ Good for integrations (Google, Slack, etc.)

**Limitations**:
- ⚠️ Manual state management
- ⚠️ Manual parallel execution
- ⚠️ Smaller community (compared to LangChain)
- ⚠️ Less multi-agent orchestration compared to OpenAI Agents

**Use Cases**:
- Google Drive document assistants
- Slack bots with AI capabilities
- Multi-model experimentation
- Integration-heavy applications
- Lightweight agent deployments

**Example Projects**:
- Google Drive Document Assistant

**Code Complexity**: Medium
**Learning Time**: 2-3 days
**Production Readiness**: ✅ Excellent

---

#### LangGraph

**Best For**:
- Complex state machines
- Multi-step workflows with branching
- Applications requiring state visualization
- Integration with LangChain ecosystem
- Advanced graph-based workflows

**Strengths**:
- ✅ Excellent state management (state graphs)
- ✅ Complex workflow support with branching
- ✅ Workflow visualization
- ✅ LangChain ecosystem integration
- ✅ Multi-provider support
- ✅ Built-in persistence

**Limitations**:
- ⚠️ Python only
- ⚠️ Steeper learning curve
- ⚠️ More complex architecture
- ⚠️ Requires understanding of graph concepts

**Use Cases**:
- Complex decision trees
- Multi-stage approval workflows
- Conditional branching logic
- State-driven applications
- Advanced automation workflows

**Example Projects**:
- (Planned for future in this repository)

**Code Complexity**: High
**Learning Time**: 5-7 days
**Production Readiness**: ✅ Excellent

---

### SDK Selection Questionnaire

Answer these questions to determine the best SDK:

**1. Provider Flexibility**
```
Q: Must you support multiple model providers?
   ├─ YES → STRANDS or LANGGRAPH
   └─ NO → Continue to Q2
```

**2. Multi-Agent Coordination**
```
Q: Do you need multiple agents working together?
   ├─ NO → CLAUDE SDK
   └─ YES → Continue to Q3
```

**3. Orchestration Pattern**
```
Q: What orchestration pattern do you need?
   ├─ Simple delegation (1-2 subagents) → CLAUDE SDK
   ├─ Parallel + Handoffs → OPENAI AGENTS
   └─ Complex state machines → LANGGRAPH
```

**4. State Complexity**
```
Q: How complex is your state management?
   ├─ Simple (in-memory) → CLAUDE SDK or OPENAI AGENTS
   ├─ Session persistence → OPENAI AGENTS
   └─ Complex state graphs → LANGGRAPH
```

**5. Language Preference**
```
Q: What's your language requirement?
   ├─ TypeScript only → CLAUDE SDK or STRANDS
   ├─ Python only → Any SDK works
   └─ Either → CLAUDE SDK or STRANDS
```

**6. Integration Needs**
```
Q: What integrations do you need?
   ├─ MCP servers (Context7, Fetch, etc.) → CLAUDE SDK or STRANDS
   ├─ LangChain ecosystem → LANGGRAPH
   ├─ Google Workspace, Slack → STRANDS
   └─ Minimal → Any SDK works
```

---

## Language Selection Framework

### Comparison Matrix

| Factor | TypeScript | Python |
|--------|-----------|---------|
| **Type Safety** | ✅ Compile-time (strict) | ✅ Runtime (Pydantic) |
| **Runtime** | Bun (very fast) | CPython (slower) |
| **Package Manager** | npm, pnpm, Bun | pip, uv |
| **Virtual Environments** | Not needed (Bun) | Required (uv venv) |
| **Validation** | Zod | Pydantic |
| **Async Support** | ✅ Native (async/await) | ✅ asyncio |
| **Web/API Focus** | ✅ Excellent | ✅ Good (FastAPI, Flask) |
| **Data Science** | ⚠️ Limited | ✅ Excellent (NumPy, Pandas) |
| **ML Libraries** | ⚠️ Limited | ✅ Extensive (TensorFlow, PyTorch) |
| **Ecosystem** | Web, Node.js, Deno, Bun | Data science, ML, scripting |
| **Learning Curve** | Moderate (types) | Easy (beginners) → Moderate (advanced) |
| **IDE Support** | ✅ Excellent (VS Code) | ✅ Excellent (VS Code, PyCharm) |
| **Production** | ✅ Excellent | ✅ Excellent |

### Decision Tree

```
START
│
├─ Data science / ML integrations needed?
│  ├─ YES → PYTHON
│  └─ NO → Continue
│
├─ Primary deployment target?
│  ├─ Web application → TYPESCRIPT
│  ├─ Data pipeline → PYTHON
│  ├─ Jupyter notebooks → PYTHON
│  ├─ Serverless functions → EITHER
│  └─ Desktop app → EITHER
│
├─ Team expertise?
│  ├─ Strong TypeScript → TYPESCRIPT
│  ├─ Strong Python → PYTHON
│  └─ Equal → Continue
│
├─ Type safety preference?
│  ├─ Compile-time errors → TYPESCRIPT
│  ├─ Runtime validation → PYTHON (Pydantic)
│  └─ Either → Continue
│
└─ Integration ecosystem?
   ├─ Need NumPy, Pandas, SciPy → PYTHON
   ├─ Need React, Next.js, Express → TYPESCRIPT
   └─ Neither specific → Choose based on team preference
```

### Detailed Language Profiles

#### TypeScript

**Best For**:
- Web application agents
- API-focused agents
- Projects requiring strict compile-time type safety
- Bun runtime benefits (speed, simplicity)
- Teams with strong TypeScript experience

**Strengths**:
- ✅ Strict type checking at compile time
- ✅ Excellent IDE support (autocomplete, refactoring)
- ✅ Bun runtime (fast, all-in-one tool)
- ✅ Rich web ecosystem (Next.js, Express, etc.)
- ✅ Clean async/await syntax
- ✅ Zod for runtime validation
- ✅ No virtual environment complexity

**Limitations**:
- ⚠️ Limited data science libraries
- ⚠️ Smaller ML ecosystem
- ⚠️ Learning curve for type system

**Example Use Cases**:
- Financial Advisor Agent (web-focused)
- API-driven agents
- Real-time web agents
- Chatbot integrations

**Setup Complexity**: Low (Bun handles everything)
**Performance**: Excellent (Bun is very fast)

---

#### Python

**Best For**:
- Data science and ML-focused agents
- Agents requiring NumPy, Pandas, SciPy
- Jupyter notebook workflows
- Data pipeline agents
- Teams with strong Python experience

**Strengths**:
- ✅ Extensive data science ecosystem
- ✅ Excellent ML libraries (TensorFlow, PyTorch)
- ✅ Pydantic for type safety and validation
- ✅ Clean, readable syntax
- ✅ Rich async support (asyncio)
- ✅ Jupyter integration
- ✅ Large community

**Limitations**:
- ⚠️ Requires virtual environment management
- ⚠️ Slower runtime (compared to Bun/Node)
- ⚠️ Runtime type errors (not compile-time)
- ⚠️ Dependency management can be complex

**Example Use Cases**:
- FIA Analyzer (data processing)
- Portfolio Collaboration (financial analysis)
- OpportunityIQ Client Matcher (data matching)
- Research agents with data analysis
- Agents requiring statistical models

**Setup Complexity**: Moderate (virtual env + dependencies)
**Performance**: Good (acceptable for most use cases)

---

### Language Selection Questionnaire

**1. Integration Requirements**
```
Q: What libraries/frameworks do you need?

If you need:
- NumPy, Pandas, SciPy, Matplotlib → PYTHON
- TensorFlow, PyTorch, scikit-learn → PYTHON
- React, Next.js, Express, Hono → TYPESCRIPT
- FastAPI, Flask, Django → PYTHON
- Either/Neither → Continue to Q2
```

**2. Deployment Target**
```
Q: Where will this agent be deployed?

- Jupyter notebooks → PYTHON
- Web application → TYPESCRIPT
- Data pipeline → PYTHON
- Serverless (AWS Lambda, etc.) → Either
- Desktop app → Either
- Continue to Q3
```

**3. Team Expertise**
```
Q: What's your team's primary language?

- Primarily TypeScript → TYPESCRIPT
- Primarily Python → PYTHON
- Equal or learning → Continue to Q4
```

**4. Type Safety Approach**
```
Q: What type safety do you prefer?

- Compile-time errors → TYPESCRIPT
- Runtime validation → PYTHON
- Either → Choose based on ecosystem
```

---

## Complexity Assessment Framework

### Complexity Levels

#### Low Complexity

**Characteristics**:
- 1-3 tools
- 0 subagents
- Simple linear workflow (1-3 stages)
- Stateless or minimal state
- No complex data transformations
- Direct context passing

**Time to Build**: 4-8 hours

**Examples**:
- Document Q&A agent
- Simple search agent
- Basic calculator agent
- Straightforward information retrieval

**Tool Example**:
```
1. search_documents - Find relevant documents
2. extract_content - Pull text from documents
3. summarize - Generate summary
```

**When to Choose**:
- Single, well-defined purpose
- No specialized delegation needed
- Simple user interactions
- Minimal data processing

---

#### Medium Complexity

**Characteristics**:
- 4-7 tools
- 0-2 subagents
- Multi-stage workflow with moderate branching
- State management (in-memory or simple persistence)
- Moderate data transformations
- Some specialized analysis

**Time to Build**: 10-20 hours

**Examples**:
- Financial analysis agent
- Product comparison agent
- Content generation with validation
- FIA product analyzer

**Tool Example**:
```
1. search_products - Find products by criteria
2. extract_features - Parse product specifications
3. calculate_scores - Evaluate against criteria
4. compare_options - Side-by-side comparison
5. generate_recommendation - Create recommendation
6. create_report - Format output
```

**Subagent Example**:
- Main agent (conversational)
- Deep analysis subagent (Sonnet)
- Optimization subagent (Haiku)

**When to Choose**:
- Multiple related capabilities needed
- Some tasks require deeper analysis
- Moderate workflow complexity
- Some state tracking needed

---

#### High Complexity

**Characteristics**:
- 8+ tools
- 3+ subagents or multi-agent orchestration
- Complex orchestration with parallel execution
- Advanced state management (database, sessions)
- Complex data transformations and analysis
- Multiple specialized domains

**Time to Build**: 30-60+ hours

**Examples**:
- Multi-agent portfolio analysis
- Complex workflow automation
- Multi-perspective research system
- Collaborative problem solving

**Tool Example**:
```
1-4: Risk analysis tools
5-8: Performance analysis tools
9-12: Compliance checking tools
13-15: Report generation tools
```

**Multi-Agent Example**:
```
Portfolio Manager (Orchestrator)
├── Risk Analyst (parallel)
├── Compliance Officer (parallel)
├── Performance Analyst (parallel)
└── Equity Specialist (handoff for depth)
```

**When to Choose**:
- Multiple specialized domains
- Parallel execution beneficial
- Complex state management required
- Sophisticated orchestration needed

---

### Complexity Decision Tree

```
START
│
├─ How many distinct capabilities?
│  ├─ 1-3 → LOW COMPLEXITY
│  ├─ 4-7 → Continue to Q2
│  └─ 8+ → HIGH COMPLEXITY
│
├─ Q2: Need specialized sub-tasks?
│  ├─ NO → MEDIUM COMPLEXITY (no subagents)
│  ├─ 1-2 specialized tasks → MEDIUM COMPLEXITY (0-2 subagents)
│  └─ 3+ specialized tasks → HIGH COMPLEXITY (multi-agent)
│
├─ Q3: Workflow complexity?
│  ├─ Linear (A → B → C) → LOW COMPLEXITY
│  ├─ Branching (A → B or C) → MEDIUM COMPLEXITY
│  └─ State machine / parallel → HIGH COMPLEXITY
│
└─ Q4: Data/state management?
   ├─ Stateless → LOW COMPLEXITY
   ├─ In-memory state → MEDIUM COMPLEXITY
   └─ Database / sessions → HIGH COMPLEXITY
```

---

## Tool Design Framework

### Principles

**1. Single Responsibility**
- Each tool does one thing well
- If description has "and", consider splitting
- Clear, focused purpose

**2. Descriptive Naming**
- Use verb + noun pattern
- Be specific (not generic)
- Self-documenting

**3. Input Validation**
- Always use Zod (TypeScript) or Pydantic (Python)
- Validate at tool boundaries
- Clear validation error messages

**4. Structured Output**
- Consistent return format
- Include success flag
- Separate data and errors

**5. Error Handling**
- Handle errors gracefully
- Provide actionable error messages
- Never crash without context

### Tool Count Guidelines

| Agent Complexity | Recommended Tool Count | Rationale |
|-----------------|----------------------|-----------|
| Low | 1-3 tools | Simple, focused functionality |
| Medium | 4-7 tools | Multiple related capabilities |
| High | 8-12 tools | Complex multi-domain operations |
| Very High | 13+ tools | Consider splitting into multiple agents |

**⚠️ Warning**: More than 15 tools often indicates:
- Agent trying to do too much
- Should be split into multiple agents
- Or some tools should be combined

### Tool Design Template

```markdown
### Tool: [verb_noun_description]

**Purpose**: [One-sentence description]

**When to use**: [Specific scenarios]

**Inputs**:
- param1 (type, validation): description
- param2 (type, validation): description

**Outputs**:
- success (boolean): operation status
- data (object): result data
- error (string, optional): error message

**Error Conditions**:
- Invalid input: [behavior]
- Missing data: [behavior]
- External failure: [behavior]

**Example**:
```
Input: { param1: "value" }
Output: { success: true, data: {...} }
```
```

---

## Subagent Decision Framework

### When to Use Subagents

**Use subagents when**:
- ✅ Clear specialization needed (different domains)
- ✅ Different reasoning depths required (complex vs simple)
- ✅ Different model requirements (Sonnet vs Haiku)
- ✅ Clear delegation workflow

**Don't use subagents when**:
- ❌ A single tool would suffice
- ❌ External service can handle it (MCP server, API)
- ❌ Adds unnecessary complexity

### Subagent Patterns

#### Pattern 1: Specialization (Domain Expertise)

**Structure**:
```
Main Agent (General Purpose)
├── Finance Subagent (Sonnet) - Financial analysis
├── Legal Subagent (Sonnet) - Legal compliance
└── Technical Subagent (Sonnet) - Technical evaluation
```

**When to use**: Different domain expertise required

---

#### Pattern 2: Complexity Levels (Reasoning Depth)

**Structure**:
```
Main Agent (Conversational)
├── Deep Analysis Subagent (Sonnet) - Complex reasoning
└── Quick Calc Subagent (Haiku) - Fast calculations
```

**When to use**: Tasks have different complexity levels

---

#### Pattern 3: Parallel Execution (Independent Tasks)

**Structure**:
```
Orchestrator Agent
├── Task 1 Subagent → Run in parallel
├── Task 2 Subagent → Run in parallel
└── Task 3 Subagent → Run in parallel
Then: Combine results
```

**When to use**: Independent tasks that can run concurrently

---

### Subagent vs. External Service

| Factor | Subagent | External Service (MCP, API) |
|--------|----------|---------------------------|
| Control | Full control | Limited to API |
| Latency | Single hop | Additional network hop |
| Cost | Token cost | Token + API cost |
| Customization | Highly customizable | Limited to API capabilities |
| Maintenance | Your responsibility | Provider maintains |
| Reliability | Depends on model | Depends on provider |

**Rule of thumb**: If an external service does 80%+ of what you need, use it instead of building a subagent.

---

## State Management Framework

### State Complexity Levels

#### Level 1: Stateless

**Characteristics**:
- No persistence between interactions
- Each request is independent
- No conversation history

**Best for**:
- Simple calculators
- One-shot queries
- Stateless APIs

**Implementation**: None needed

---

#### Level 2: In-Memory State

**Characteristics**:
- State exists during conversation
- Lost when agent restarts
- Simple data structures

**Best for**:
- Short conversations
- Temporary workflow state
- Non-critical data

**Implementation**: JavaScript objects or Python dicts

---

#### Level 3: Session Persistence

**Characteristics**:
- State persists across restarts
- Tied to user session
- Retrievable later

**Best for**:
- Multi-turn conversations
- User preferences
- Conversation history

**Implementation**: SQLite (OpenAI Agents), files, or simple DB

---

#### Level 4: Complex State Graphs

**Characteristics**:
- Multiple states with transitions
- Branching workflows
- State visualization

**Best for**:
- Complex workflows
- Approval processes
- State machines

**Implementation**: LangGraph

---

## Testing Strategy Framework

### Test Coverage Levels

#### Minimal (Quick Validation)
- Manual QA scenarios
- Basic happy path tests
- Time: 30-60 minutes

**For**: Prototypes, demos, internal tools

---

#### Standard (Production Ready)
- Unit tests for critical tools
- Integration tests for workflows
- Manual QA scenarios
- Edge case testing
- Time: 2-4 hours

**For**: Production agents, customer-facing tools

---

#### Comprehensive (High Reliability)
- Full unit test coverage (80%+)
- Integration tests
- Performance tests
- MCP integration tests
- Automated regression tests
- Time: 4-8 hours

**For**: Mission-critical systems, financial applications

---

### Test Prioritization

**P0 (Must Have)**:
- Happy path workflows work
- Critical tools function correctly
- Error handling prevents crashes

**P1 (Should Have)**:
- Edge cases handled gracefully
- Performance acceptable
- All tools have basic tests

**P2 (Nice to Have)**:
- Comprehensive edge case coverage
- Performance benchmarks
- Load testing

---

## Summary

These frameworks provide:
- ✅ Clear decision criteria for SDK selection
- ✅ Language choice guidance based on requirements
- ✅ Complexity assessment to scope projects appropriately
- ✅ Tool design principles for focused, maintainable tools
- ✅ Subagent usage patterns
- ✅ State management strategies
- ✅ Testing approach based on requirements

Use these frameworks during the **BRAINSTORM** and **DESIGN** stages to make informed architectural decisions that align with your project's needs.
