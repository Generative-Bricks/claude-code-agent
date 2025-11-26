# Claude Code Agent Testing Repository

**Purpose:** A comprehensive testing ground for building, experimenting with, and documenting AI agents using various SDKs and frameworks (Claude SDK, Strands Agents, LangGraph, etc.) across multiple languages (TypeScript, Python, Go, etc.).

**Status:** Active Development | Version 1.0.0

---

## 📑 Table of Contents

- [Repository Philosophy](#-repository-philosophy)
- [Directory Structure](#️-directory-structure)
- [Quick Start](#-quick-start)
- [Documentation System](#-documentation-system)
- [Standards & Principles](#-standards--principles)
- [Existing Agents](#-existing-agents)
- [Available MCP Servers](#️-available-mcp-servers)
- [Development Workflow](#-development-workflow)
- [Technology Stack](#-technology-stack)
- [Quality Standards](#-quality-standards)
- [Citation Standards](#-citation-standards)
- [Adding New SDKs/Frameworks](#-adding-new-sdksframeworks)
- [Key Learnings & Patterns](#-key-learnings--patterns)
- [Additional Resources](#-additional-resources)
- [Anti-Patterns to Avoid](#-anti-patterns-to-avoid)
- [Success Indicators](#-success-indicators)
- [Session Management](#-session-management)
- [Contributing](#-contributing-to-this-repository)
- [Support & Troubleshooting](#-support--troubleshooting)

---

## 🔗 Quick Links

### Global Standards & Principles
- **[Core Framework](/home/seed537/.claude/principles/CORE_FRAMEWORK.md)** - 6 foundational principles with biblical sources and cascade framework
- **[Development Standards](/home/seed537/.claude/standards/DEVELOPMENT.md)** - Coding standards, testing, validation (Zod/Pydantic)
- **[Agent Standards](/home/seed537/.claude/standards/AGENTIC.md)** - Agent architecture, lifecycle, memory, coordination
- **[Operations Standards](/home/seed537/.claude/standards/OPERATIONS.md)** - Observability, traceability, evaluation, security

---

## 📖 Repository Philosophy

This repository follows the **6 Foundational Principles** derived from biblical foundations. These principles cascade through standards to implementation: Principles → Standards → Implementation.

1. **TRUTH** - Every agent decision is observable and explainable
2. **HONOR** - User-first design with data sovereignty
3. **EXCELLENCE** - Production-grade from inception
4. **SERVE** - Simple, helpful developer experience
5. **PERSEVERE** - Resilient systems with graceful failure handling
6. **SHARPEN** - Continuous improvement through testing and feedback

**See [Core Framework](/home/seed537/.claude/principles/CORE_FRAMEWORK.md) for the complete framework with biblical sources, cascade explanation, and decision framework.**

---

## 🗂️ Directory Structure

```
claude-code-agent/
├── .claude/
│   └── settings.local.json          # Claude Code permissions & MCP config
├── .mcp.json                        # MCP server configuration (AWS, Context7, etc.)
├── CLAUDE.md                        # THIS FILE - Repository overview
│
Note: Global standards and principles are in /home/seed537/.claude/
│   ├── principles/                  # Core framework (copied from docs/principles/)
│   └── standards/                   # Development, Agent, Operations standards
│
├── agents/                          # Agent implementations by SDK/framework
│   ├── claude-sdk/
│   │   ├── typescript/
│   │   │   └── financial-advisor/  # Financial advisor agent (production-ready)
│   │   └── python/
│   │       ├── fia-analyzer/       # FIA analyzer agent (production-ready)
│   │       └── opportunityiq-client-matcher/  # Client revenue opportunity matcher (production-ready)
│   ├── strands-agents/
│   │   ├── typescript/             # Future Strands TS agents
│   │   └── python/
│   │       ├── google-drive-agent/ # Google Drive agent (production-ready)
│   │       └── llm-brainstorm-arena/ # Multi-LLM brainstorm comparison (production-ready)
│   ├── openai-agents/
│   │   └── python/
│   │       └── portfolio-collaboration/  # Multi-agent portfolio system (production-ready)
│   └── langgraph-agents/
│       └── python/                 # Future LangGraph agents
│
├── docs/
│   ├── references/
│   │   └── context7-library-ids-reference.md  # Verified Context7 library IDs
│   ├── workflows/
│   │   └── agent-ideation-workflow.md         # Brainstorm → Design → Implement → Test
│   ├── comparisons/
│   │   └── agent-comparison-matrix.md         # Side-by-side agent comparisons
│   ├── catalogs/
│   │   ├── common-tools-catalog.md            # Reusable tool patterns
│   │   └── mcp-integration-patterns.md        # MCP server usage patterns
│   └── memory/
│       └── memory.jsonl                        # Knowledge graph (entities & relations)
│
└── templates/                       # Quick-start templates for new agents
    ├── claude-sdk-typescript/       # Claude SDK TypeScript boilerplate
    ├── claude-sdk-python/           # Claude SDK Python boilerplate
    ├── openai-agents-python/        # OpenAI Agents SDK Python boilerplate
    └── strands-agents-typescript/   # Strands Agents TypeScript boilerplate
```

---

## 🚀 Quick Start

### Starting a New Agent Project

1. **Choose your SDK/framework and language:**
   - Claude SDK (TypeScript or Python)
   - Strands Agents (TypeScript or Python)
   - LangGraph (Python)
   - Others as needed

2. **Copy the appropriate template:**
   ```bash
   # Example: Starting a new Claude SDK TypeScript agent
   cp -r templates/claude-sdk-typescript agents/claude-sdk/typescript/my-new-agent
   cd agents/claude-sdk/typescript/my-new-agent
   ```

3. **Install dependencies:**
   ```bash
   # For TypeScript projects
   bun install

   # For Python projects
   uv venv
   source .venv/Scripts/activate  # Windows Git Bash
   uv pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Start building:**
   - Review the template's CLAUDE.md for specific instructions
   - Follow the [Agent Ideation Workflow](docs/workflows/agent-ideation-workflow.md)
   - Document your decisions in the memory system

---

## 📚 Documentation System

### Memory System (docs/memory/memory.jsonl)

The memory system tracks:
- **Agent architecture decisions** - Why certain architectural choices were made
- **Design patterns** - Tool patterns, subagent patterns, workflow patterns
- **Testing insights** - What worked, what didn't, gotchas discovered
- **SDK/framework learnings** - Which frameworks work best for specific use cases

**Usage:**
```typescript
// Memory entries follow MCP Memory Server format
{"entity": "financial-advisor-agent", "entityType": "Agent", "observations": [...]}
{"from": "financial-advisor-agent", "to": "Claude SDK", "relationType": "uses"}
```

### Documentation Files

- **agent-ideation-workflow.md** - Step-by-step process from idea to production
- **agent-comparison-matrix.md** - Compare agents side-by-side
- **common-tools-catalog.md** - Reusable tool patterns across agents
- **mcp-integration-patterns.md** - Best practices for MCP server integration
- **context7-library-ids-reference.md** - Verified library IDs for documentation retrieval

---

## 📋 Standards & Principles

This repository follows a cascade of principles → standards → implementation. All agents should comply with the standards documented in `/home/seed537/.claude/standards/`.

### Principles Framework

The [Core Framework](principles/CORE_FRAMEWORK.md) establishes 6 foundational principles derived from biblical sources, which cascade into software development principles and technical standards.

### Development Standards

**[Development Standards](standards/DEVELOPMENT.md)** - Coding standards, language baselines (TypeScript/Python), validation requirements (Zod/Pydantic), testing pyramid, and Git workflow.

### Agent Standards

**[Agent Standards](standards/AGENTIC.md)** - Agent architecture, taxonomy (Levels 0-4), lifecycle, memory strategies, multi-agent coordination, and MCP integration patterns.

### Operations Standards

**[Operations Standards](standards/OPERATIONS.md)** - Observability (OpenTelemetry), traceability, evaluation framework (offline/online/human), and security requirements.

**See [Standards README](standards/README.md) for the complete standards overview.**

---

## 🧪 Existing Agents

All agents are production-ready. See each agent's CLAUDE.md for full documentation.

| Agent | Framework | Language | Purpose | Quick Start |
|-------|-----------|----------|---------|-------------|
| **[Financial Advisor](agents/claude-sdk/typescript/financial-advisor/CLAUDE.md)** | Claude SDK v0.1.37 | TypeScript | Annuity allocation analysis and retirement income planning | `cd agents/claude-sdk/typescript/financial-advisor && bun install && bun run dev` |
| **[Google Drive Assistant](agents/strands-agents/python/google-drive-agent/CLAUDE.md)** | Strands Agents v1.0.0+ | Python | Q&A and document summarization over Google Drive (no RAG needed) | `cd agents/strands-agents/python/google-drive-agent && uv venv && uv pip install -r requirements.txt && uv run python src/main.py` |
| **[LLM Brainstorm Arena](agents/strands-agents/python/llm-brainstorm-arena/CLAUDE.md)** | Strands Agents v1.0.0+ | Python | Multi-LLM brainstorming comparison (Claude, GPT-5.1, Gemini) with hybrid scoring | `cd agents/strands-agents/python/llm-brainstorm-arena && uv venv && uv pip install -r requirements.txt && python -m src.main "Your prompt"` |
| **[FIA Analyzer](agents/claude-sdk/python/fia-analyzer/CLAUDE.md)** | Claude SDK | Python | Fixed Indexed Annuity product analysis with suitability scoring | `cd agents/claude-sdk/python/fia-analyzer && uv venv && uv pip install -r requirements.txt && uv run python -m src.main --product "Product Name"` |
| **[Portfolio Collaboration](agents/openai-agents/python/portfolio-collaboration/CLAUDE.md)** | OpenAI Agents SDK v0.2.0+ | Python | Multi-agent portfolio analysis (5 specialists, parallel execution) | `cd agents/openai-agents/python/portfolio-collaboration && uv venv && uv pip install -r requirements.txt && python -m src.main --list` |
| **[OpportunityIQ Matcher](agents/claude-sdk/python/opportunityiq-client-matcher/CLAUDE.md)** | Claude SDK | Python | Match clients to revenue opportunities with prioritized reports | `cd agents/claude-sdk/python/opportunityiq-client-matcher && uv venv && uv pip install -r requirements.txt && python -m src.main --clients data/clients/sample-clients.json --scenarios data/scenarios` |

---

## 🛠️ Available MCP Servers

The repository has access to the following MCP servers (configured in `.mcp.json`):

### AWS Services
- **bedrock-agentcore-mcp-server** - Bedrock AgentCore documentation
- **awslabs.core-mcp-server** - AWS prompt understanding
- **awslabs.aws-documentation-mcp-server** - AWS docs search & retrieval
- **awslabs.code-doc-gen-mcp-server** - Code documentation generation
- **awslabs.frontend-mcp-server** - React & web app guidance
- **aws-knowledge-mcp-server** - AWS regional availability & knowledge

### Development Tools
- **context7** - Library documentation retrieval (see [Context7 Library IDs Reference](docs/references/context7-library-ids-reference.md))
- **fetch** - Web content fetching
- **strands-agents** - Strands Agents framework docs
- **powertools** - Powertools for AWS Lambda docs

### Data & Memory
- **memory** - MCP Memory Server for knowledge graphs
- **time** - Timezone and time conversions
- **ide** - VS Code diagnostics and code execution

**Usage Example:**
```typescript
// Fetch library documentation
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/anthropics/anthropic-sdk-typescript"
})

// Search AWS documentation
mcp__awslabs_aws-documentation-mcp-server__search_documentation({
  search_phrase: "Lambda function URLs"
})
```

---

## 🎯 Development Workflow

### Agent Ideation Process

1. **Brainstorm** - Define use case, user needs, and success criteria
2. **Design** - Architecture, tools, subagents, workflows
3. **Implement** - Build incrementally with tests
4. **Test** - Verify behavior, performance, edge cases
5. **Document** - Update memory system and comparison matrix

See [Agent Ideation Workflow](docs/workflows/agent-ideation-workflow.md) for detailed steps.

**See [Agent Standards](standards/AGENTIC.md) for agent lifecycle and architecture patterns. See [Operations Standards](standards/OPERATIONS.md) for deployment gates and evaluation requirements.**

### Git Workflow

**Commit Message Format:**
```
type: brief description

Types: feat, fix, docs, refactor, test, chore
```

**Example:**
```bash
git add agents/claude-sdk/typescript/my-agent
git commit -m "feat: add customer service agent with sentiment analysis"
```

---

## 📦 Technology Stack

### Preferred Tools
- **Runtime:** Bun (TypeScript/JavaScript projects)
- **Language:** TypeScript with strict settings
- **Python:** uv for virtual environments and package management
- **Formatter:** Prettier (.prettierrc and .prettierignore)
- **Version Control:** Git via command line

**See [Development Standards](standards/DEVELOPMENT.md) for full coding standards, validation requirements (Zod/Pydantic), testing pyramid, and language-specific guidelines.**

### Python Development

**ALWAYS use `uv` for Python projects:**
```bash
# Create virtual environment
uv venv

# Activate (Windows Git Bash)
source .venv/Scripts/activate

# Install dependencies
uv pip install -r requirements.txt

# Run scripts
uv run python src/main.py
```

### TypeScript Development

**Use Bun for all TypeScript projects:**
```bash
# Install dependencies
bun install

# Run development mode
bun run dev

# Build for production
bun run build
```

---

## ✅ Quality Standards

### Before Starting Any Agent

- [ ] Can I explain the agent's purpose in 1-2 sentences?
- [ ] Have I checked existing patterns in [Common Tools Catalog](docs/catalogs/common-tools-catalog.md)?
- [ ] Have I reviewed similar agents in [Agent Comparison Matrix](docs/comparisons/agent-comparison-matrix.md)?
- [ ] Is this the simplest solution that could work?

### Before Marking Agent "Done"

- [ ] All tools have proper error handling
- [ ] Agent handles failures gracefully
- [ ] Documentation is complete (README.md + CLAUDE.md)
- [ ] Memory system is updated with learnings
- [ ] Comparison matrix includes the new agent
- [ ] Code follows naming conventions (kebab-case for docs, camelCase/snake_case for code)
- [ ] Validation: Zod (TypeScript) or Pydantic (Python) for all external inputs
- [ ] Testing: Unit tests (80%), integration tests (15%), E2E tests (5%)

### Code Quality

- **Readable over clever** - Write code your future self will understand
- **Explicit over implicit** - Clear intent in every line
- **Documented over self-explanatory** - Explain the WHY, not just WHAT
- **Tested over assumed** - Verify behavior with real examples
- **One purpose per file** - If you can't explain it in one sentence, split it

**See [Development Standards](standards/DEVELOPMENT.md) for detailed coding standards, validation requirements, and testing guidelines. See [Operations Standards](standards/OPERATIONS.md) for evaluation requirements.**

---

## 📝 Citation Standards

### Internal Documents (Global Standards)

Use absolute paths to the global `.claude/` directory:
- `[Core Framework](/home/seed537/.claude/principles/CORE_FRAMEWORK.md)` - Complete principles framework
- `[Development Standards](/home/seed537/.claude/standards/DEVELOPMENT.md)` - Coding standards and requirements
- `[Agent Standards](/home/seed537/.claude/standards/AGENTIC.md)` - Agent architecture and lifecycle
- `[Operations Standards](/home/seed537/.claude/standards/OPERATIONS.md)` - Observability and evaluation

**Format:** Include context: "See [Standard Name](/home/seed537/.claude/path/to/file.md) for [brief description]"

### Internal Documents (Project-Specific)

Use relative paths from repository root:
- `[Agent Ideation Workflow](docs/workflows/agent-ideation-workflow.md)` - Project workflow
- `[Financial Advisor Agent](agents/claude-sdk/typescript/financial-advisor/CLAUDE.md)` - Agent documentation
- `[Common Tools Catalog](docs/catalogs/common-tools-catalog.md)` - Project patterns

### External Resources

Include URL and brief description:
- `[Claude Code Documentation](https://docs.claude.com/claude-code)` - Official Claude Code docs
- `[Claude Agent SDK](https://docs.anthropic.com/claude/agent-sdk)` - Anthropic SDK documentation
- `[Model Context Protocol](https://modelcontextprotocol.io)` - MCP specification

### Code References

- **Existing code:** Use file paths: `src/tools/example.ts`
- **New/proposed code:** Use markdown code blocks with language tags

---

## 🔄 Adding New SDKs/Frameworks

To add support for a new SDK or framework:

1. **Create framework directory:**
   ```bash
   mkdir -p agents/new-framework-name/typescript
   mkdir -p agents/new-framework-name/python
   ```

2. **Create template:**
   ```bash
   mkdir -p templates/new-framework-typescript
   # Add boilerplate files
   ```

3. **Add to context7 reference:**
   - Find library ID using Context7 resolve-library-id
   - Add to [Context7 Library IDs Reference](docs/references/context7-library-ids-reference.md)

4. **Update documentation:**
   - Add framework to this CLAUDE.md
   - Document patterns in [Common Tools Catalog](docs/catalogs/common-tools-catalog.md)
   - Update [Agent Comparison Matrix](docs/comparisons/agent-comparison-matrix.md) structure if needed

---

## 🧠 Key Learnings & Patterns

**Core Patterns:**
- **Validation First:** Zod (TypeScript) or Pydantic (Python) for all external inputs
- **Focused Tools:** One clear purpose per tool, descriptive names, structured returns
- **Mock Data:** Start with mock data, clear integration points for real APIs
- **Error Handling:** Comprehensive error handling from day one

**See [Common Tools Catalog](docs/catalogs/common-tools-catalog.md) for reusable patterns and [Agent Comparison Matrix](docs/comparisons/agent-comparison-matrix.md) for agent-specific learnings.**

---

## 📖 Additional Resources

### Context7 Library IDs (Most Used)

**Agent Development:**
- `/anthropics/anthropic-sdk-typescript` - Claude SDK for TypeScript
- `/anthropics/anthropic-sdk-python` - Claude SDK for Python
- `/strands-agents/docs` - Strands Agents framework
- `/websites/ai-sdk_dev` - Vercel AI SDK

**MCP Integration:**
- `/websites/modelcontextprotocol_io` - MCP specification
- `/modelcontextprotocol/typescript-sdk` - MCP TypeScript SDK
- `/modelcontextprotocol/python-sdk` - MCP Python SDK

**Full list:** See [Context7 Library IDs Reference](docs/references/context7-library-ids-reference.md)

### External Documentation

- [Claude Code Documentation](https://docs.claude.com/claude-code) - Official Claude Code IDE documentation
- [Claude Agent SDK](https://docs.anthropic.com/claude/agent-sdk) - Anthropic's official agent SDK documentation
- [Strands Agents Framework](https://strands.ai/docs) - Strands Agents framework documentation
- [Model Context Protocol](https://modelcontextprotocol.io) - MCP specification and documentation

---

## 🚫 Anti-Patterns to Avoid

### Agent Design
- 🚩 Over-engineering tools (keep them simple and focused)
- 🚩 Too many subagents (only create when clearly needed)
- 🚩 Unclear workflows (document the flow explicitly)
- 🚩 Mixed concerns (one agent = one clear purpose)

### Code
- 🚩 "This is a bit complex but..." (simplify instead)
- 🚩 "While we're here, let's also..." (atomic commits only)
- 🚩 "We might need this later..." (YAGNI - You Aren't Gonna Need It)
- 🚩 Skipping error handling (handle errors from the start)

### Documentation
- 🚩 Outdated documentation (update as you code)
- 🚩 Missing CLAUDE.md in agent projects (always required)
- 🚩 Forgetting to update memory system (document learnings immediately)
- 🚩 No comparison matrix entry (helps others learn from your work)

---

## 🎯 Success Indicators

You're on the right track when:
- New agents are easy to start (copy template → customize → run)
- Patterns are reusable across different agents
- Documentation stays current without effort
- Learnings are captured in the memory system
- Each agent has a clear, singular purpose
- Tools are simple and well-tested
- Error handling is comprehensive
- The codebase is simpler than when you started

---

## 📝 Session Management

**Workflow:** Focus on atomic tasks → Test incrementally → Document as you go → Update memory system → Commit with clear messages.

**See [Agent Ideation Workflow](docs/workflows/agent-ideation-workflow.md) for detailed development process.**

---

## 🤝 Contributing to This Repository

### Adding a New Agent

1. Copy the appropriate template
2. Implement following the [Agent Ideation Workflow](docs/workflows/agent-ideation-workflow.md)
3. Create comprehensive CLAUDE.md in the agent directory
4. Update the root CLAUDE.md "Existing Agents" section
5. Add entry to [Agent Comparison Matrix](docs/comparisons/agent-comparison-matrix.md)
6. Document patterns in [Common Tools Catalog](docs/catalogs/common-tools-catalog.md)
7. Update memory.jsonl with architectural decisions

### Improving Templates

1. Make changes to the template in templates/
2. Document the improvement rationale
3. Consider if existing agents should be updated
4. Update this CLAUDE.md if template structure changes

---

## 📞 Support & Troubleshooting

### Common Issues

**Issue:** Dependencies not installing
- **TypeScript:** Ensure Bun is installed (`bun --version`)
- **Python:** Use `uv venv` (NOT `python -m venv`)

**Issue:** MCP servers not connecting
- Check `.mcp.json` configuration
- Verify API keys in `.env`
- Review `.claude/settings.local.json` permissions

**Issue:** Agent not responding correctly
- Check agent prompts for clarity
- Verify tool input schemas (Zod validation)
- Review subagent context passing
- Test tools individually before integration

---

**Remember:** *"Whatever you do, work heartily, as for the Lord"* - Colossians 3:23

Excellence is not about complexity. It's about doing simple things consistently well, with transparency, respect for users, and continuous improvement.

---

*Last updated: January 2025*
*Repository Version: 1.0.0*
*Maintained by: seed537*
