# Agent Builder Skill

An interactive AI agent development workflow orchestrator that guides you through building production-ready agents from concept to deployment.

## Overview

The Agent Builder skill implements a comprehensive 6-stage methodology for building AI agents:

**BRAINSTORM → DESIGN → IMPLEMENT → TEST → DOCUMENT → ITERATE**

It supports a **two-phase operation** for maximum flexibility:
- **Phase 1 (Design)**: Interactive planning and comprehensive design documentation
- **Phase 2 (Scaffolding)**: Project setup and boilerplate code generation

## Quick Start

### Phase 1: Design Your Agent

Simply say:
```
"Help me design an agent for [your use case]"
"I want to build an agent that [does something]"
"Guide me through planning an agent for [problem]"
```

The skill will:
1. Ask interactive questions through BRAINSTORM and DESIGN stages
2. Help you make informed decisions using proven frameworks
3. Generate comprehensive design documentation
4. Create a scaffolding manifest for Phase 2

**Output**:
- `agent-design-document.md` - Complete design specification
- `scaffolding-manifest.json` - Machine-readable spec for code generation

### Phase 2: Scaffold Your Agent

Provide the design document from Phase 1:
```
"Scaffold this agent design in [target directory]"
"Generate the project structure for this design"
"Create the boilerplate from this design document"
```

The skill will:
1. Parse your design document
2. Create directory structure
3. Generate boilerplate code files
4. Setup configuration files
5. Create pre-filled documentation

**Output**: Complete project structure ready for customization

## Features

### Interactive Guided Workflow
- Questions at each stage (BRAINSTORM → DESIGN)
- Decision frameworks for SDK selection, language choice, architecture
- Pattern-based guidance from proven production agents
- Real-time validation and quality checks

### Two-Phase Operation
- **Design anywhere**: Plan in one project, implement in another
- **Portable designs**: Version control, review, and share designs independently
- **Machine-readable**: Scaffolding manifest for programmatic code generation

### Comprehensive Documentation
- Auto-generated CLAUDE.md with all sections
- Pre-filled README.md from design decisions
- Comparison matrix entry templates
- Memory system integration

### Production-Grade Quality
- Checklist-driven development
- Pattern catalog with 15+ proven patterns
- Quality gates at each stage
- Production-ready standards

## Supported SDKs and Languages

### SDKs
- ✅ Claude SDK (TypeScript & Python)
- ✅ OpenAI Agents SDK (Python)
- ✅ Strands Agents (TypeScript & Python)
- ✅ LangGraph (Python)

### Languages
- ✅ TypeScript (with Bun runtime, Zod validation)
- ✅ Python (with uv virtual environments, Pydantic validation)

## Documentation

### Quick References
- [SKILL.md](./SKILL.md) - Complete skill documentation
- [Workflow Stages](./references/workflow-stages.md) - Detailed stage instructions
- [Decision Frameworks](./references/decision-frameworks.md) - SDK and architecture guidance
- [Pattern Catalog](./references/pattern-catalog.md) - 15+ proven patterns
- [Quality Checklists](./references/quality-checklists.md) - Production-ready criteria

### Templates
- [Design Document Template](./templates/design-document-template.md) - Phase 1 output template
- [Scaffolding Manifest](./templates/scaffolding-manifest.json) - Machine-readable spec

### Examples
- [examples/](./examples/) - Complete agent design examples

## Typical Workflow

### Step 1: Brainstorm (30-60 minutes)
```
User: "Help me design an agent for analyzing financial products"

Skill asks:
- What problem does this solve?
- Who are the primary users?
- What makes this valuable?
- Success criteria (3-5 measurable goals)?
- Which SDK? (Provides decision framework)
- Which language? (TypeScript or Python?)
- Complexity level? (Low/Medium/High)
```

### Step 2: Design (1-2 hours)
```
Skill asks:
- Agent persona and role?
- Tools needed (start with 3-5)?
- Workflow stages?
- Subagents needed?
- Data model design?
- MCP integration requirements?
- Which patterns to apply?
```

### Step 3: Generate Design Document
```
Skill generates:
- agent-design-document.md (comprehensive spec)
- scaffolding-manifest.json (machine-readable)

Ready for Phase 2!
```

### Step 4: Scaffold (15-30 minutes)
```
User: "Scaffold this design in /path/to/project"

Skill generates:
- Complete directory structure
- Tool templates with validation
- Agent configuration
- Mock data structures
- Test framework
- Documentation templates
```

### Step 5: Implement (4-60 hours, varies by complexity)
```
You implement:
- Tool core logic (marked with TODOs)
- Mock data content
- Test assertions
- Subagent prompts (if applicable)
```

### Step 6: Test, Document, Deploy
```
Following the quality checklists:
- Unit tests for tools
- Integration tests for workflows
- Complete CLAUDE.md
- Manual QA
- Production deployment
```

## Benefits

### Time Savings
- **2-4 hours** of setup eliminated per agent
- **Consistent structure** across all agents
- **Pre-filled documentation** from design decisions
- **Proven patterns** ready to apply

### Quality Improvements
- **Checklist-driven** development
- **Pattern-based** architecture
- **Production-grade** from inception
- **Comprehensive** testing strategy

### Team Collaboration
- **Portable designs** for review and approval
- **Consistent standards** across team
- **Knowledge capture** in memory system
- **Reusable patterns** for future agents

## Examples

### Example 1: Financial Analysis Agent
```
Problem: Financial advisors spend 30+ minutes analyzing FIA products
Solution: Agent reduces this to 5 minutes with higher accuracy

SDK: Claude SDK (TypeScript)
Complexity: Medium (6 tools, 2 subagents)
Patterns: Zod Validation, Mock Data First, Subagent Specialization
Time to Build: 15-20 hours
```

### Example 2: Document Q&A Agent
```
Problem: Users need to quickly find information in Google Drive docs
Solution: Natural language Q&A over documents

SDK: Strands Agents (Python)
Complexity: Low (4 tools, 0 subagents)
Patterns: Pydantic Validation, Direct Context Passing (no RAG)
Time to Build: 8-10 hours
```

### Example 3: Multi-Agent Portfolio Analysis
```
Problem: Portfolio analysis requires multiple specialized perspectives
Solution: 5 specialist agents working in parallel + handoffs

SDK: OpenAI Agents (Python)
Complexity: High (4 core tools, 5 agents)
Patterns: Parallel Execution, Weighted Scoring, Hybrid Multi-Agent
Time to Build: 40-50 hours
Performance: 65% faster with parallel execution
```

## When to Use This Skill

Use this skill when you:
- ✅ Want to build a new AI agent from scratch
- ✅ Need guidance on SDK and architecture decisions
- ✅ Want to apply proven patterns to your use case
- ✅ Need comprehensive design documentation
- ✅ Want to separate design and implementation phases
- ✅ Need production-grade quality standards

Don't use this skill when:
- ❌ You just need a quick prototype (use templates directly)
- ❌ You already have a complete design
- ❌ The project is extremely simple (1-2 tools, no workflow)

## FAQ

### Q: Can I use this for existing agents?
**A**: Yes! Use Phase 1 to document existing agent architecture, then use the design as reference for refactoring.

### Q: Do I need to use both phases?
**A**: No. You can use Phase 1 (Design) for documentation and planning, then implement manually. Or use existing templates and skip the skill entirely.

### Q: Can I customize the generated code?
**A**: Absolutely! The scaffolding generates boilerplate with TODO comments. You're expected to customize tool logic, mock data, and prompts.

### Q: What if I make mistakes in design?
**A**: Design documents are editable! Update your design document and regenerate scaffolding if needed. The skill helps catch issues early through checklists and validation.

### Q: Can I share designs with my team?
**A**: Yes! Design documents are portable, version-controllable markdown files. Share them for review before implementation.

### Q: How does this differ from templates?
**A**: Templates provide boilerplate code. This skill guides you through the entire design process, asks questions, provides decision frameworks, and generates customized documentation. Much more comprehensive than static templates.

## Getting Help

### Interactive Help
The skill itself provides guidance at each stage. Just ask:
- "What should I consider when choosing an SDK?"
- "What patterns should I use for this?"
- "How do I know if my design is complete?"

### Reference Documentation
- **SKILL.md**: Complete skill documentation
- **references/**: Detailed frameworks and patterns
- **examples/**: Real-world agent designs

### Common Questions
- SDK selection → See `decision-frameworks.md`
- Pattern application → See `pattern-catalog.md`
- Quality verification → See `quality-checklists.md`
- Workflow guidance → See `workflow-stages.md`

## Version History

**v1.0.0** (2025-01-24)
- Initial release
- Complete 6-stage workflow
- Two-phase operation (Design + Scaffolding)
- Interactive questioning framework
- 15+ proven patterns
- Comprehensive decision frameworks
- Quality checklists
- SDK support: Claude SDK, OpenAI Agents, Strands, LangGraph
- Language support: TypeScript, Python

## Contributing

Found a new pattern? Discovered a better approach? Update the pattern catalog and share your learnings!

## License

Part of the Claude Code Agent Testing Repository

---

**Remember**: Excellence is not about complexity. It's about doing simple things consistently well, with transparency, clear documentation, and continuous improvement.
