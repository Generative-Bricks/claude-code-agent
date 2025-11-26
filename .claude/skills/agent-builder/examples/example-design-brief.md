# Simple Calculator Agent - Design Document (Example)

**Document Version**: 1.0.0
**Date**: 2025-01-24
**Status**: Design Complete / Ready for Implementation
**Author**: Example User

---

## Executive Summary

**One-Sentence Description**: A conversational calculator agent that performs basic arithmetic operations with validation and clear explanations.

**Problem Solved**: Users need quick calculations without leaving their conversation context

**Primary Users**: Developers, analysts, anyone needing quick calculations

**Value Delivered**: Instant calculations with validation and explanation, no context switching

---

## 1. Brainstorm Results

### 1.1 Problem Statement

Users frequently need to perform simple calculations (add, subtract, multiply, divide) while working in a conversational interface. Switching to a calculator app breaks flow and wastes time. This agent provides instant calculations with input validation and clear explanations.

### 1.2 Success Criteria

1. **Accuracy**: Agent performs calculations with 100% accuracy
   - Measurement: Automated test suite
   - Target: 100% passing tests
   - Timeframe: Day 1

2. **Speed**: Agent responds in <1 second
   - Measurement: Response time monitoring
   - Target: <1 second per operation
   - Timeframe: Day 1

3. **Validation**: Agent catches invalid inputs
   - Measurement: Error handling tests
   - Target: All invalid inputs handled gracefully
   - Timeframe: Day 1

### 1.3 Acceptable Limitations

- **Simple operations only**: No advanced math (calculus, trigonometry, etc.)
- **Two-operand limit**: Operations work with exactly two numbers
- **No history**: Agent doesn't remember past calculations

### 1.4 Key Edge Cases

| Edge Case | How to Handle | Priority |
|-----------|--------------|----------|
| Division by zero | Return error with explanation | High |
| Non-numeric inputs | Validate and request valid numbers | High |
| Very large numbers | Handle with appropriate precision | Medium |

### 1.5 Technical Decisions

#### SDK Selection

**Selected**: Claude SDK (TypeScript)

**Rationale**:
- Simple conversational agent (no multi-agent orchestration)
- TypeScript for type safety
- Bun runtime for speed
- MCP not needed

#### Language Selection

**Selected**: TypeScript

**Rationale**:
- Compile-time type safety
- Fast development with Bun
- Simple project (no data science needs)

#### Complexity Assessment

**Level**: Low

**Estimated Metrics**:
- **Tools**: 4 tools (add, subtract, multiply, divide)
- **Subagents**: 0
- **Workflow Stages**: 1 (Direct calculation)
- **Development Time**: 4-6 hours

---

## 2. Design Specifications

### 2.1 Agent Persona

**Name**: Calculator Agent

**Role**: Performs basic arithmetic operations with validation and explanations

**Expertise**:
- **Mathematics**: Basic arithmetic (add, subtract, multiply, divide)

**Communication Style**:
- **Tone**: Friendly and helpful
- **Language**: Simple, clear
- **Personality**: Precise and reliable

**Capabilities**:
✅ **Can**:
- Perform addition, subtraction, multiplication, division
- Validate numeric inputs
- Explain results clearly
- Handle edge cases (division by zero, etc.)

❌ **Cannot**:
- Perform advanced math (trigonometry, calculus, etc.)
- Work with more than two operands
- Remember calculation history

**Limitations**:
- Two operands maximum per operation
- Basic operations only

**Safety Constraints**:
- Always validates inputs before calculation
- Provides clear error messages for invalid operations

### 2.2 Tool Specifications

#### Tool #1: add

**Purpose**: Add two numbers together

**When to use**: User requests addition or sum

**Input Schema** (TypeScript with Zod):
```typescript
const AddInputSchema = z.object({
  a: z.number().describe("First number"),
  b: z.number().describe("Second number")
});
```

**Output Schema**:
```typescript
interface AddOutput {
  success: boolean;
  data?: {
    result: number;
    explanation: string;
  };
  error?: string;
}
```

**Example**:
```
Input: { a: 5, b: 3 }
Output: {
  success: true,
  data: {
    result: 8,
    explanation: "5 + 3 = 8"
  }
}
```

---

#### Tool #2: subtract

**Purpose**: Subtract second number from first number

**When to use**: User requests subtraction or difference

**Input Schema**:
```typescript
const SubtractInputSchema = z.object({
  a: z.number().describe("Number to subtract from"),
  b: z.number().describe("Number to subtract")
});
```

**Output Schema**: Same as add

**Example**:
```
Input: { a: 10, b: 3 }
Output: {
  success: true,
  data: {
    result: 7,
    explanation: "10 - 3 = 7"
  }
}
```

---

#### Tool #3: multiply

**Purpose**: Multiply two numbers

**When to use**: User requests multiplication or product

**Input Schema**:
```typescript
const MultiplyInputSchema = z.object({
  a: z.number().describe("First number"),
  b: z.number().describe("Second number")
});
```

**Output Schema**: Same as add

**Example**:
```
Input: { a: 4, b: 5 }
Output: {
  success: true,
  data: {
    result: 20,
    explanation: "4 × 5 = 20"
  }
}
```

---

#### Tool #4: divide

**Purpose**: Divide first number by second number

**When to use**: User requests division or quotient

**Input Schema**:
```typescript
const DivideInputSchema = z.object({
  a: z.number().describe("Dividend (number to be divided)"),
  b: z.number().describe("Divisor (number to divide by)")
});
```

**Output Schema**: Same as add

**Error Conditions**:
| Error | Cause | Handling |
|-------|-------|----------|
| Division by zero | b === 0 | Return error: "Cannot divide by zero" |

**Example (Success)**:
```
Input: { a: 20, b: 4 }
Output: {
  success: true,
  data: {
    result: 5,
    explanation: "20 ÷ 4 = 5"
  }
}
```

**Example (Error)**:
```
Input: { a: 10, b: 0 }
Output: {
  success: false,
  error: "Cannot divide by zero"
}
```

---

### 2.3 Workflow Design

**Overview**: Single-stage direct calculation

**Stages**: 1 stage (Calculate)

**Progression**: Linear (stateless)

**State Management**: Stateless

#### Stage 1: Calculate

**Purpose**: Perform requested operation and return result

**Activities**:
1. Validate inputs (numeric, non-zero divisor if dividing)
2. Perform calculation
3. Return result with explanation

**Tools Used**:
- One of: `add`, `subtract`, `multiply`, `divide`

**Progression Condition**: N/A (single stage)

**Error Handling**: Return clear error message

---

### 2.4 Subagent Plan

No subagents planned (simple single-purpose agent).

---

### 2.5 Data Model

**Core Entities**: None (stateless calculations only)

---

### 2.6 MCP Integration Plan

No MCP integration planned.

---

### 2.7 Pattern Selections

| Pattern | Category | Rationale |
|---------|----------|-----------|
| Zod Validation | Validation | Type-safe input validation (required) |
| Graceful Degradation | Error Handling | Clear error messages for invalid operations |

---

## 3. Technical Architecture

### 3.1 Project Structure

```
calculator-agent/
├── src/
│   ├── index.ts              # Main agent configuration
│   ├── types/
│   │   └── index.ts          # Type definitions & Zod schemas
│   └── tools/
│       ├── add.ts
│       ├── subtract.ts
│       ├── multiply.ts
│       └── divide.ts
├── tests/
│   └── tools/
│       ├── add.test.ts
│       ├── subtract.test.ts
│       ├── multiply.test.ts
│       └── divide.test.ts
├── .claude/
│   └── CLAUDE.md
├── package.json
├── tsconfig.json
├── .env.example
├── .gitignore
└── README.md
```

### 3.2 Dependencies

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

### 3.3 Environment Configuration

```bash
# API Keys
ANTHROPIC_API_KEY=sk-ant-...

# Configuration
LOG_LEVEL=info
```

---

## 4. Implementation Guidance

### 4.1 Implementation Sequence

1. **Project Setup** (15 mins)
2. **Tool: add** (30 mins)
3. **Tool: subtract** (30 mins)
4. **Tool: multiply** (30 mins)
5. **Tool: divide** (45 mins - includes zero check)
6. **Agent Configuration** (30 mins)
7. **Testing** (1 hour)
8. **Documentation** (30 mins)

**Total Estimated Time**: 4-5 hours

### 4.2 Critical Implementation Notes

- Always validate inputs with Zod before calculations
- Division by zero must be caught and return clear error
- Results should include explanation string

---

## 5. Testing Strategy

### 5.1 Unit Tests

| Tool | Test Cases | Priority |
|------|------------|----------|
| add | - Positive numbers<br>- Negative numbers<br>- Zero | High |
| subtract | - Positive result<br>- Negative result<br>- Zero result | High |
| multiply | - Positive numbers<br>- Negative numbers<br>- By zero | High |
| divide | - Normal division<br>- **Division by zero**<br>- Fractional results | High |

### 5.2 Performance Targets

| Metric | Target |
|--------|--------|
| Tool response time | <100ms |
| Token usage | <500 tokens per operation |

---

## 6. Deployment Plan

### 6.1 Pre-Deployment Checklist

**Code Quality**:
- [x] Zod validation on all tools
- [x] Division by zero handled
- [x] TypeScript strict mode

**Testing**:
- [x] All unit tests passing
- [x] Edge cases tested

**Documentation**:
- [x] CLAUDE.md complete
- [x] README.md complete

---

## Scaffolding Instructions

**Phase 2 Ready**: This design is complete and ready for scaffolding.

**What will be generated**:
- Complete directory structure
- 4 tool templates with Zod validation
- Agent configuration
- Test structure
- Documentation templates

**What you need to implement**:
- Tool core logic (simple arithmetic)
- Test assertions

---

**This is a simplified example. Real agent designs would be more comprehensive.**
