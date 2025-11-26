# [Agent Name] - Design Document

**Document Version**: 1.0.0
**Date**: [YYYY-MM-DD]
**Status**: Design Complete / Ready for Implementation
**Author**: [Your Name]

---

## Document Purpose

This design document captures all architectural decisions, specifications, and implementation guidance for the **[Agent Name]** project. It serves as the complete blueprint for Phase 2 (scaffolding and implementation).

---

## Executive Summary

**One-Sentence Description**: [Describe what this agent does in one sentence]

**Problem Solved**: [Specific pain point this agent addresses]

**Primary Users**: [Who will use this agent]

**Value Delivered**: [Quantified benefit - time savings, cost reduction, capability enablement, etc.]

---

## Table of Contents

1. [Brainstorm Results](#brainstorm-results)
2. [Design Specifications](#design-specifications)
3. [Technical Architecture](#technical-architecture)
4. [Implementation Guidance](#implementation-guidance)
5. [Testing Strategy](#testing-strategy)
6. [Deployment Plan](#deployment-plan)
7. [Appendices](#appendices)
   - A: Glossary
   - B: References
   - C: Open Questions
   - D: Future Enhancements
   - E: 6 Principles Check (Optional)
   - F: Agent Taxonomy Classification (Optional)
   - G: Operations Plan (Optional)

---

## 1. Brainstorm Results

### 1.1 Problem Statement

[Clear, concise description of the problem being solved. Include:
- What pain point exists today
- Who experiences this pain
- Why current solutions are inadequate
- What success looks like]

**Example**:
```
Financial advisors spend 30+ minutes manually researching and comparing Fixed Indexed Annuity (FIA) products for each client. This manual process is error-prone, inconsistent, and doesn't scale. Success means reducing this to 5 minutes with higher accuracy and consistency.
```

### 1.2 Success Criteria

[3-5 measurable goals with clear success thresholds]

1. **[Criterion #1]**: [Specific, measurable goal with success threshold]
   - Measurement: [How to measure]
   - Target: [Numeric target]
   - Timeframe: [When to achieve]

2. **[Criterion #2]**: [Second criterion]
   - Measurement: [How to measure]
   - Target: [Numeric target]
   - Timeframe: [When to achieve]

3. **[Criterion #3]**: [Third criterion]
   - Measurement: [How to measure]
   - Target: [Numeric target]
   - Timeframe: [When to achieve]

**Example**:
```
1. Accuracy: Agent provides correct suitability assessment in 85%+ of cases
   - Measurement: Comparison against advisor manual assessment
   - Target: 85% agreement
   - Timeframe: Within 3 months of deployment

2. Speed: Agent completes analysis in <5 minutes, 95% of the time
   - Measurement: End-to-end workflow timing
   - Target: <5 minutes
   - Timeframe: Immediate (day 1)
```

### 1.3 Acceptable Limitations

[What is explicitly out of scope or acceptable as a limitation]

- **Limitation #1**: [What the agent won't do and why that's acceptable]
- **Limitation #2**: [Second limitation]
- **Limitation #3**: [Third limitation]

**Example**:
```
- Requires human review: Agent provides recommendations but final decision requires human approval
- No historical data: Agent doesn't track past recommendations (focus is current analysis)
- English only: Initial version supports English language only
```

### 1.4 Key Edge Cases

[Critical edge cases the agent must handle gracefully]

| Edge Case | How to Handle | Priority |
|-----------|--------------|----------|
| [Case #1] | [Handling approach] | High/Medium/Low |
| [Case #2] | [Handling approach] | High/Medium/Low |
| [Case #3] | [Handling approach] | High/Medium/Low |

**Example**:
```
| Missing client data | Request specific missing fields, continue with partial analysis | High |
| Product no longer available | Suggest similar alternatives, flag as unavailable | Medium |
| Conflicting requirements | Present trade-offs, ask user for prioritization | High |
```

### 1.5 Technical Decisions

#### SDK Selection

**Selected**: [Claude SDK / OpenAI Agents / Strands / LangGraph]

**Rationale**:
[Explain why this SDK was chosen. Reference decision frameworks.]

**Example**:
```
Selected: Claude SDK (TypeScript)

Rationale:
- Excellent reasoning capabilities needed for complex financial analysis
- No multi-agent orchestration required (simple subagent support sufficient)
- Anthropic models acceptable (no multi-provider requirement)
- Team has strong TypeScript experience
- Bun runtime benefits (speed, simplicity)
```

#### Language Selection

**Selected**: [TypeScript / Python]

**Rationale**:
[Explain why this language was chosen]

**Example**:
```
Selected: TypeScript

Rationale:
- Primary deployment target is web application
- Compile-time type safety reduces errors
- Bun runtime provides excellent performance
- Team expertise in TypeScript
- Rich web ecosystem for integrations
```

#### Complexity Assessment

**Level**: [Low / Medium / High]

**Estimated Metrics**:
- **Tools**: [Number] tools
- **Subagents**: [Number] subagents
- **Workflow Stages**: [Number] stages
- **Development Time**: [Hours] hours

**Example**:
```
Level: Medium

Estimated Metrics:
- Tools: 6 tools
- Subagents: 2 subagents (Deep Analysis, Quick Calc)
- Workflow Stages: 5 stages (Discovery → Assessment → Analysis → Recommendation → Documentation)
- Development Time: 15-20 hours
```

---

## 2. Design Specifications

### 2.1 Agent Persona

**Name**: [Agent name]

**Role**: [Primary role description]

**Expertise**:
- **[Domain #1]**: [Level of expertise and specific knowledge]
- **[Domain #2]**: [Level of expertise and specific knowledge]
- **[Domain #3]**: [Level of expertise and specific knowledge]

**Communication Style**:
- **Tone**: [Formal / Conversational / Technical / Adaptive]
- **Language**: [Simple / Professional / Domain-specific]
- **Personality**: [Helpful / Analytical / Creative / etc.]

**Capabilities**:
✅ **Can**:
- [Capability #1]
- [Capability #2]
- [Capability #3]

❌ **Cannot**:
- [What agent cannot do #1]
- [What agent cannot do #2]
- [What agent cannot do #3]

**Limitations**:
- [Explicit limitation #1]
- [Explicit limitation #2]

**Safety Constraints**:
- [What agent will never do #1]
- [What requires human approval #1]

**Example**:
```
Name: Financial Advisor Agent

Role: Specializes in Fixed Indexed Annuity (FIA) analysis and retirement income planning

Expertise:
- Financial Planning: Expert-level knowledge of retirement planning strategies
- FIA Products: Deep understanding of FIA structures, caps, participation rates, riders
- Suitability Analysis: Proficient in assessing client-product fit

Communication Style:
- Tone: Professional yet approachable
- Language: Financial advisor terminology (not consumer-facing)
- Personality: Analytical, thorough, detail-oriented

Capabilities:
✅ Can:
- Analyze FIA product features and suitability
- Calculate income projections
- Compare multiple FIA products
- Assess client risk tolerance fit

❌ Cannot:
- Make final investment decisions (human advisor required)
- Access real-time market data (uses cached/provided data)
- Provide tax or legal advice

Limitations:
- Recommendations require human advisor review and approval
- Analysis based on provided data only (no independent research)

Safety Constraints:
- Never bypasses compliance requirements
- Always requires human approval for final recommendations
- Never accesses client data without proper authorization
```

### 2.2 Tool Specifications

[For each tool, provide complete specification]

#### Tool #1: [tool_name]

**Purpose**: [One-sentence description of what this tool does]

**When to use**: [Specific scenarios where this tool should be invoked]

**Input Schema**:

**TypeScript (Zod)**:
```typescript
const ToolNameInputSchema = z.object({
  param1: z.string().min(1).describe("Description of param1"),
  param2: z.number().positive().describe("Description of param2"),
  param3: z.enum(['option1', 'option2', 'option3']).optional(),
  // ... all parameters
});

type ToolNameInput = z.infer<typeof ToolNameInputSchema>;
```

**Python (Pydantic)**:
```python
class ToolNameInput(BaseModel):
    param1: str = Field(min_length=1, description="Description of param1")
    param2: int = Field(gt=0, description="Description of param2")
    param3: Optional[Literal['option1', 'option2', 'option3']] = None
    # ... all parameters
```

**Output Schema**:

**TypeScript**:
```typescript
interface ToolNameOutput {
  success: boolean;
  data?: {
    field1: string;
    field2: number;
    // ... output fields
  };
  error?: string;
}
```

**Python**:
```python
class ToolNameOutput(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
```

**Validation Rules**:
- [Rule #1]: [Description and justification]
- [Rule #2]: [Description and justification]

**Error Conditions**:
| Error | Cause | Handling |
|-------|-------|----------|
| Invalid input | [What makes input invalid] | [How to handle] |
| Missing data | [What data is missing] | [How to handle] |
| External failure | [External dependency failed] | [How to handle] |
| Timeout | [Operation took too long] | [How to handle] |

**Example Usage**:

**Input**:
```json
{
  "param1": "example value",
  "param2": 123
}
```

**Output (Success)**:
```json
{
  "success": true,
  "data": {
    "field1": "result",
    "field2": 456
  }
}
```

**Output (Error)**:
```json
{
  "success": false,
  "error": "Validation failed: param2 must be positive"
}
```

**Implementation Notes**:
- [Note #1]: [Important implementation detail]
- [Note #2]: [Another implementation detail]

---

[Repeat "Tool Specifications" section for each tool]

**Tool Summary**:

| Tool Name | Purpose | Inputs | Outputs |
|-----------|---------|--------|---------|
| tool_1 | [Brief purpose] | [Key inputs] | [Key outputs] |
| tool_2 | [Brief purpose] | [Key inputs] | [Key outputs] |
| tool_3 | [Brief purpose] | [Key inputs] | [Key outputs] |

---

### 2.3 Workflow Design

**Overview**: [High-level description of the workflow]

**Stages**: [Number] stages

**Progression**: [Linear / Branching / Hybrid]

**State Management**: [Stateless / In-Memory / Persisted]

---

#### Stage 1: [Stage Name]

**Purpose**: [What this stage accomplishes]

**Trigger**: [What initiates this stage]

**Activities**:
1. [Activity #1]
2. [Activity #2]
3. [Activity #3]

**Information Collected**:
- [Data point #1]
- [Data point #2]
- [Data point #3]

**Tools Used**:
- `tool_name_1`: [Purpose in this stage]
- `tool_name_2`: [Purpose in this stage]

**State Updates**:
- [What state is updated]

**Progression Condition**:
- [When/how to move to next stage]

**Error Handling**:
- [What happens if this stage fails]
- [Graceful degradation approach]

**Expected Duration**: [Time estimate]

---

[Repeat "Stage" section for each workflow stage]

---

**Workflow Diagram**:

```
[Visual representation of workflow - can be ASCII art or description]

Stage 1 (Discovery)
    ↓
    Collect user requirements
    ↓
Stage 2 (Assessment)
    ↓
    Evaluate criteria
    ↓
Stage 3 (Analysis)
    ↓
    Perform calculations
    ↓
Stage 4 (Recommendation)
    ↓
    Generate recommendations
    ↓
Stage 5 (Documentation)
    ↓
    Create reports
```

---

### 2.4 Subagent Plan

[If using subagents, provide specifications. If not, state "No subagents planned."]

#### Subagent #1: [Name]

**Model**: [Sonnet / Haiku / Opus]

**Rationale**: [Why this model for this subagent]

**Responsibility**: [What this subagent does]

**Triggered When**: [Conditions for delegation]

**Input Context**:
- [Data point #1 from main agent]
- [Data point #2 from main agent]
- [Data point #3 from main agent]

**Expected Output**:
```
{
  field1: value,
  field2: value
}
```

**Success Criteria**:
- [How main agent evaluates subagent result]

**Communication Pattern**:
```
Main Agent → Subagent:
  Prompt: "[Example delegation prompt]"
  Context: { ... }

Subagent → Main Agent:
  Result: { ... }
```

**Error Handling**:
- [What happens if subagent fails]

---

[Repeat "Subagent" section for each subagent]

**Subagent Summary**:

| Subagent | Model | Responsibility | When Used |
|----------|-------|----------------|-----------|
| subagent_1 | Sonnet | [Responsibility] | [Trigger condition] |
| subagent_2 | Haiku | [Responsibility] | [Trigger condition] |

---

### 2.5 Data Model

**Core Entities**:

[For each major data entity, provide Pydantic/Zod schema]

#### Entity: [EntityName]

**TypeScript (Zod)**:
```typescript
const EntityNameSchema = z.object({
  id: z.string().uuid(),
  field1: z.string(),
  field2: z.number(),
  nested: z.object({
    subfield1: z.string()
  }).optional()
});

type EntityName = z.infer<typeof EntityNameSchema>;
```

**Python (Pydantic)**:
```python
class EntityName(BaseModel):
    id: UUID
    field1: str
    field2: int
    nested: Optional['NestedModel'] = None
```

**Description**: [What this entity represents]

**Relationships**: [How this entity relates to others]

**Validation**: [Key validation rules]

---

[Repeat "Entity" section for each core entity]

**Data Model Diagram**:

```
[Visual representation of entity relationships]

User
  ├── has many → Preferences
  └── creates → Requests

Request
  ├── contains → Criteria
  └── produces → Result

Result
  ├── includes → Recommendation[]
  └── generates → Report
```

---

### 2.6 MCP Integration Plan

[If using MCP servers, document here. If not, state "No MCP integration planned."]

**MCP Servers Used**:

| Server | Purpose | Tools Used |
|--------|---------|------------|
| Context7 | Documentation retrieval | `get-library-docs` |
| Fetch | Web content | `fetch` |
| [Custom] | [Purpose] | [Tools] |

**Configuration** (`.mcp.json`):
```json
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
```

**Permissions** (`.claude/settings.local.json`):
```json
{
  "permissions": {
    "allow": [
      "mcp__context7__get-library-docs",
      "mcp__fetch__fetch"
    ]
  }
}
```

**Usage Patterns**:
- [How MCP tools are used in workflow]
- [Caching strategy, if applicable]
- [Error handling for MCP failures]

---

### 2.7 Pattern Selections

**Patterns Applied**:

| Pattern | Category | Rationale |
|---------|----------|-----------|
| Zod/Pydantic Validation | Validation | Type-safe input validation (required) |
| Mock Data First | Data Management | Fast development, predictable tests |
| [Pattern #3] | [Category] | [Why this pattern was selected] |
| [Pattern #4] | [Category] | [Why this pattern was selected] |

**Detailed Pattern Descriptions**:

#### Pattern: [Pattern Name]

**Purpose**: [What this pattern solves]

**Implementation**: [How it will be implemented in this agent]

**Benefits**: [Why it's valuable for this agent]

---

[Repeat for each pattern]

---

## 3. Technical Architecture

### 3.1 Project Structure

```
[agent-name]/
├── src/
│   ├── index.ts (or main.py)      # Main agent configuration
│   ├── types/                      # Type definitions & schemas
│   │   └── index.ts
│   ├── tools/                      # Tool implementations
│   │   ├── tool1.ts
│   │   ├── tool2.ts
│   │   └── tool3.ts
│   ├── subagents/ (if applicable)  # Subagent configurations
│   │   ├── deepAnalysis.ts
│   │   └── quickCalc.ts
│   └── data/                       # Mock data & data management
│       └── mockData.ts
├── tests/                          # Test suite
│   ├── tools/
│   │   ├── tool1.test.ts
│   │   └── tool2.test.ts
│   └── integration/
│       └── workflow.test.ts
├── .claude/                        # Claude Code configuration
│   └── CLAUDE.md
├── package.json (or requirements.txt)
├── tsconfig.json (or pyproject.toml)
├── .env.example
├── .gitignore
└── README.md
```

### 3.2 Dependencies

**Required Packages**:

**TypeScript**:
```json
{
  "dependencies": {
    "@anthropics/sdk": "^0.1.37",
    "zod": "^3.22.0"
  },
  "devDependencies": {
    "@types/bun": "latest",
    "typescript": "^5.0.0"
  }
}
```

**Python**:
```txt
anthropic>=0.18.0
pydantic>=2.6.0
python-dotenv>=1.0.0
```

**Justification**:
- [Dependency #1]: [Why it's needed]
- [Dependency #2]: [Why it's needed]

### 3.3 Environment Configuration

**Required Environment Variables**:

```bash
# API Keys
ANTHROPIC_API_KEY=sk-ant-...

# Configuration
USE_MOCK_DATA=true  # Set to false for production
LOG_LEVEL=info      # debug, info, warn, error

# External APIs (if applicable)
EXTERNAL_API_KEY=...
EXTERNAL_API_URL=https://...
```

---

## 4. Implementation Guidance

### 4.1 Implementation Sequence

**Recommended Order**:

1. **Project Setup** (30 mins)
   - Create directory structure
   - Install dependencies
   - Configure environment

2. **Tool #1: [Simplest Tool]** (1-2 hours)
   - Implement validation schema
   - Implement core logic
   - Add error handling
   - Test individually

3. **Tool #2: [Next Tool]** (1-2 hours)
   - Same process as Tool #1

4. **[Continue for all tools]**

5. **Agent Configuration** (1 hour)
   - Write system prompt
   - Configure tools
   - Test basic workflow

6. **Subagents** (if applicable) (2-3 hours)
   - Implement subagent configurations
   - Test delegation
   - Verify communication

7. **Integration** (2-3 hours)
   - Test complete workflows
   - Add mock data
   - Verify edge cases

8. **Testing** (2-4 hours)
   - Unit tests
   - Integration tests
   - Performance tests
   - Manual QA

9. **Documentation** (1-2 hours)
   - Complete CLAUDE.md
   - Write README.md
   - Add inline comments

**Total Estimated Time**: [X-Y hours]

### 4.2 Critical Implementation Notes

**Note #1**: [Important detail that affects implementation]

**Note #2**: [Another critical note]

**Note #3**: [Third critical note]

**Example**:
```
Note #1: Always validate annuity data before calculations to prevent incorrect income projections

Note #2: Cap rates can change frequently - use cached data with TTL of 24 hours max

Note #3: Suitability scoring algorithm must be transparent for regulatory compliance
```

### 4.3 Mock Data Requirements

**Mock Data Needed**:

1. **[Data Type #1]**: [Description and quantity needed]
2. **[Data Type #2]**: [Description and quantity needed]
3. **[Data Type #3]**: [Description and quantity needed]

**Mock Data Structure**:
[Must match production API exactly]

```typescript
const MOCK_DATA = [
  {
    // Example mock data structure
  }
];
```

**Integration Points** (mark with TODO for production):
```typescript
// TODO: Replace with real API call
export async function fetchData(): Promise<Data[]> {
  const USE_MOCK = process.env.USE_MOCK_DATA === 'true';

  if (USE_MOCK) {
    return MOCK_DATA;
  } else {
    const response = await fetch('/api/data');
    return response.json();
  }
}
```

---

## 5. Testing Strategy

### 5.1 Unit Tests

**Tools to Test**:

| Tool | Test Cases | Priority |
|------|------------|----------|
| tool_1 | - Happy path<br>- Invalid input<br>- Edge cases | High |
| tool_2 | - Happy path<br>- Missing data<br>- Error conditions | High |
| tool_3 | - Happy path<br>- Boundary values<br>- Optional params | Medium |

**Test Framework**: [Bun test / pytest / jest]

**Coverage Target**: [60% minimum for production, 80%+ for critical tools]

### 5.2 Integration Tests

**Workflows to Test**:

1. **Happy Path Workflow**:
   - Description: [Complete workflow with valid inputs]
   - Expected: [Successful completion]

2. **Error Recovery Workflow**:
   - Description: [Workflow with intentional errors]
   - Expected: [Graceful degradation, clear error messages]

3. **Edge Case Workflow**:
   - Description: [Workflow with edge case inputs]
   - Expected: [Handled appropriately]

### 5.3 Manual QA Scenarios

**Scenario #1**: [Description]
- **Setup**: [How to set up this scenario]
- **Steps**: [Step-by-step actions]
- **Expected Result**: [What should happen]

[Repeat for 3-5 critical scenarios]

### 5.4 Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Tool response time (simple) | <1 second | Per-tool timing |
| Tool response time (complex) | <5 seconds | Per-tool timing |
| End-to-end workflow | <2 minutes | Full workflow timing |
| Token usage per interaction | <10,000 tokens | API response data |

---

## 6. Deployment Plan

### 6.1 Pre-Deployment Checklist

**Code Quality**:
- [ ] All type safety verified
- [ ] Input validation complete (Zod/Pydantic)
- [ ] Error handling comprehensive
- [ ] No hardcoded secrets

**Testing**:
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Manual QA complete
- [ ] Performance targets met

**Documentation**:
- [ ] CLAUDE.md complete
- [ ] README.md complete
- [ ] Inline comments added
- [ ] API documentation generated (if applicable)

**Security**:
- [ ] Secrets in environment variables
- [ ] Input validation prevents injection
- [ ] Error messages don't leak sensitive info
- [ ] API keys properly secured

### 6.2 Deployment Steps

1. **Environment Setup**:
   ```bash
   # Commands to set up production environment
   ```

2. **Deployment**:
   ```bash
   # Commands to deploy
   ```

3. **Verification**:
   ```bash
   # Commands to verify deployment
   ```

4. **Monitoring**:
   - [What to monitor]
   - [Alerting thresholds]

### 6.3 Rollback Plan

**If issues arise**:
1. [Step to roll back]
2. [Step to diagnose]
3. [Step to fix and redeploy]

---

## 7. Appendices

### Appendix A: Glossary

[Define domain-specific terms used in this document]

| Term | Definition |
|------|------------|
| [Term #1] | [Definition] |
| [Term #2] | [Definition] |

### Appendix B: References

**Documentation**:
- [SDK documentation URL]
- [Domain knowledge source]
- [Pattern catalog reference]

**Related Agents**:
- [Similar agent #1]: [What to learn from it]
- [Similar agent #2]: [What to learn from it]

### Appendix C: Open Questions

[Questions that need answering during implementation]

1. **Question #1**: [Unanswered question]
   - **Impact**: [How this affects implementation]
   - **Resolution**: [How/when to resolve]

2. **Question #2**: [Another question]
   - **Impact**: [Impact]
   - **Resolution**: [Resolution approach]

### Appendix D: Future Enhancements

[Features to add in future versions]

**Version 1.1**:
- Enhancement #1
- Enhancement #2

**Version 2.0**:
- Major enhancement #1
- Major enhancement #2

**Long-term Vision**:
- [Future direction #1]
- [Future direction #2]

---

### Appendix E: 6 Principles Check (Optional)

[If you opted to apply the 6 Principles decision framework during BRAINSTORM, document the check here]

> **Reference**: See `references/principles-framework.md` for detailed guidance

| Principle | Question | Answer | Notes |
|-----------|----------|--------|-------|
| TRUTH | Is every decision observable and explainable? | [ ] Yes / [ ] No | [Notes] |
| HONOR | Does design respect user data sovereignty? | [ ] Yes / [ ] No | [Notes] |
| EXCELLENCE | Is it production-grade from inception? | [ ] Yes / [ ] No | [Notes] |
| SERVE | Does it simplify the user experience? | [ ] Yes / [ ] No | [Notes] |
| PERSEVERE | Will it handle failures gracefully? | [ ] Yes / [ ] No | [Notes] |
| SHARPEN | Can it improve through feedback? | [ ] Yes / [ ] No | [Notes] |

**Cascade Check**:
- [ ] Personal Foundation (purpose, alignment)
- [ ] Operational Alignment (quality, transparency)
- [ ] External Impact (user value, community benefit)
- [ ] System Integration (ecosystem fit, sustainability)

---

### Appendix F: Agent Taxonomy Classification (Optional)

[If you opted to classify with Agent Taxonomy during BRAINSTORM, document the classification here]

> **Reference**: See `references/agent-taxonomy.md` for detailed guidance

**Agent Level**: [ ] Level 0 / [ ] Level 1 / [ ] Level 2 / [ ] Level 3 / [ ] Level 4

| Level | Name | Has Feature | Your Agent |
|-------|------|-------------|------------|
| 0 | Reasoning Agent | None | [Yes/No] |
| 1 | Connected Agent | Tools | [Yes/No] |
| 2 | Strategic Agent | Subagents | [Yes/No] |
| 3 | Collaborative Agent | A2A Protocol | [Yes/No] |
| 4 | Self-Evolving Agent | Memory Evolution | [Yes/No] |

**A2A Protocol** (if Level 3+):
- SPIFFE ID Planned: [ ] Yes / [ ] No
- Capability Advertisement: [ ] Yes / [ ] No
- Message Format Standard: [ ] Yes / [ ] No

---

### Appendix G: Operations Plan (Optional)

[If you plan to deploy to production, document operations requirements here]

> **Reference**: See `references/operations-guide.md` for detailed guidance

#### Deployment Gates

- [ ] Offline evaluations passing
- [ ] Red team review complete (if applicable)
- [ ] Staging environment tested
- [ ] Production readiness confirmed

#### Rollout Strategy

| Phase | Traffic % | Duration | Success Criteria |
|-------|----------|----------|------------------|
| Canary | 1% | [Time] | [Criteria] |
| Limited | 10% | [Time] | [Criteria] |
| Gradual | 50% | [Time] | [Criteria] |
| Full | 100% | [Time] | [Criteria] |

#### Observability Plan

**Tracing**: [ ] OpenTelemetry planned
**Metrics**: [ ] Latency, tokens, cost tracked
**Logging**: [ ] Structured JSON, no PII
**Alerting**: [ ] Thresholds defined

#### Evaluation Framework

**Offline**: [ ] Benchmark suite planned
**Online**: [ ] A/B testing planned
**Human**: [ ] Feedback mechanism planned

---

## Scaffolding Instructions

**Phase 2 Ready**: This design is complete and ready for scaffolding.

**To scaffold this agent**:

1. Use the scaffolding manifest file: `scaffolding-manifest.json`
2. Target directory: `[Specify where to scaffold]`
3. Command: `scaffold-agent --design agent-design-document.md --manifest scaffolding-manifest.json --target /path/to/project`

**What will be generated**:
- Complete directory structure
- Tool templates with validation schemas
- Agent configuration with system prompt
- Mock data structures
- Test structure
- Configuration files
- Documentation templates

**What you need to implement**:
- Tool core logic (marked with TODO comments)
- Mock data content
- Test assertions
- Subagent prompts (if applicable)

---

**End of Design Document**

---

**Document Metadata**:
- **Total Pages**: [Number]
- **Design Completion**: [Date]
- **Approved By**: [Name]
- **Implementation Start**: [Date]
- **Target Completion**: [Date]
