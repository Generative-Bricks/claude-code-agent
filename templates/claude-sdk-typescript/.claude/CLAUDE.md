# [Your Agent Name]

**Template:** Claude SDK TypeScript Agent Template
**Status:** 🚧 Template - Customize Before Use
**Version:** 1.0.0

---

## ⚠️ Template Instructions

This is a **template file**. When creating a new agent:

1. Copy this template to your agent directory
2. Replace all `[placeholders]` with your actual information
3. Delete this instructions section
4. Fill out all sections with your agent's details

---

## 📖 Project Overview

**Purpose:** [Describe what your agent does in 1-2 sentences]

**Use Case:** [Who will use this agent and for what purpose?]

**Key Features:**
- [Feature 1]
- [Feature 2]
- [Feature 3]

---

## 🗂️ Directory Structure

```
[your-agent-name]/
├── src/
│   ├── index.ts              # Main agent configuration
│   ├── types/
│   │   └── index.ts          # Type definitions & Zod schemas
│   ├── tools/
│   │   └── [yourTools].ts    # Tool implementations
│   └── data/
│       └── [yourData].ts     # Data management
├── .claude/
│   └── CLAUDE.md             # This file
├── package.json              # Dependencies & scripts
├── tsconfig.json             # TypeScript configuration
├── .env                      # Environment variables (git-ignored)
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
└── README.md                 # Quick start guide
```

---

## 🚀 Setup Instructions

### Prerequisites

- Bun (for TypeScript runtime and package management)
- Anthropic API key
- [Any other prerequisites]

### Installation

```bash
# Navigate to project directory
cd [path/to/your-agent]

# Install dependencies
bun install

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Running the Agent

```bash
# Development mode
bun run dev

# Production mode
bun start

# Type checking
bun run type-check
```

---

## 🛠️ Agent Configuration

### Model

**Primary Model:** `claude-sonnet-4-5-20250929`

**Rationale:** [Why this model? e.g., "Sonnet provides excellent reasoning for complex analysis"]

### System Prompt

**Persona:** [Describe your agent's role and expertise]

**Key Behaviors:**
- [Behavior 1]
- [Behavior 2]
- [Behavior 3]

**Limitations:**
- [Limitation 1]
- [Limitation 2]

---

## 🔧 Tools

### Tool 1: [Tool Name]

**Purpose:** [What does this tool do?]

**Input:**
```typescript
{
  param1: string;  // Description
  param2: number;  // Description
}
```

**Output:**
```typescript
{
  result: any;     // Description
  metadata: {};    // Description
}
```

**Usage Example:**
```typescript
// Example of how to use this tool
const result = await tool1({ param1: "value", param2: 42 });
```

### Tool 2: [Tool Name]

[Repeat for each tool]

---

## 🌊 Workflow

**Stage 1: [Stage Name]**
- [What happens in this stage]
- [Key actions]

**Stage 2: [Stage Name]**
- [What happens in this stage]
- [Key actions]

[Add more stages as needed]

---

## 🤖 Subagents (if applicable)

### Subagent 1: [Name]

**Model:** [Model used]

**Purpose:** [What specialized task does this subagent handle?]

**When Used:** [Under what conditions is this subagent invoked?]

---

## 📊 Data Model

### Primary Data Structures

**[Entity Name]:**
```typescript
interface Entity {
  id: string;
  // Add fields
}
```

[Describe your data structures]

---

## 🔗 External Integrations

### API Integrations

- **[API Name]:** [Purpose and usage]
- **[API Name]:** [Purpose and usage]

### MCP Servers Used

- **[MCP Server]:** [How it's used]
- **[MCP Server]:** [How it's used]

---

## 🧪 Testing

### Manual Testing Scenarios

1. **[Scenario Name]:**
   - Input: [Example input]
   - Expected: [Expected behavior]
   - Result: [✅/❌]

2. **[Scenario Name]:**
   - Input: [Example input]
   - Expected: [Expected behavior]
   - Result: [✅/❌]

### Edge Cases

- [Edge case 1 and how it's handled]
- [Edge case 2 and how it's handled]

---

## 📈 Performance

**Metrics:**
- Average response time: [Time]
- Tool calls per conversation: [Number]
- Token usage (avg): [Number]

**Optimization Opportunities:**
- [Potential optimization 1]
- [Potential optimization 2]

---

## 🚧 Known Limitations

1. [Limitation 1]
2. [Limitation 2]
3. [Limitation 3]

---

## 🎯 Future Enhancements

- [ ] [Enhancement 1]
- [ ] [Enhancement 2]
- [ ] [Enhancement 3]

---

## 📝 Development Notes

### Key Decisions

**[Decision Topic]:**
- **Decision:** [What was decided]
- **Rationale:** [Why this decision was made]
- **Date:** [When decided]

### Learnings

- [Learning 1]
- [Learning 2]

### Gotchas

- [Gotcha 1 and solution]
- [Gotcha 2 and solution]

---

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | [Date] | Initial release |

---

## 📚 References

- [Claude Agent SDK Documentation](https://docs.anthropic.com/claude/agent-sdk)
- [Repository Root CLAUDE.md](../../../CLAUDE.md)
- [Agent Ideation Workflow](../../../docs/workflows/agent-ideation-workflow.md)
- [Common Tools Catalog](../../../docs/catalogs/common-tools-catalog.md)

---

**Last Updated:** [Date]
**Maintained By:** [Your Name]
