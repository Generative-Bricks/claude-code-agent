# Claude SDK TypeScript Agent Template

A production-ready template for building AI agents with the Claude Agent SDK and TypeScript.

## Quick Start

```bash
# 1. Copy this template
cp -r templates/claude-sdk-typescript agents/claude-sdk/typescript/my-agent

# 2. Navigate to your project
cd agents/claude-sdk/typescript/my-agent

# 3. Install dependencies
bun install

# 4. Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 5. Run the agent
bun run dev
```

## What's Included

```
├── src/
│   ├── index.ts           # Main agent configuration
│   ├── types/
│   │   └── index.ts       # Type definitions & Zod schemas
│   ├── tools/
│   │   └── exampleTools.ts # Example tool implementations
│   └── data/
│       └── mockData.ts    # Mock data for development
├── .claude/
│   └── CLAUDE.md          # Project documentation
├── package.json           # Dependencies & scripts
├── tsconfig.json          # TypeScript configuration
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Features

- **Type Safety**: Full TypeScript with strict mode enabled
- **Validation**: Zod schemas for runtime type checking
- **Error Handling**: Comprehensive error handling patterns
- **Mock Data**: Example data structure for development
- **Best Practices**: Follows Claude Code agent development guidelines
- **Production Ready**: Configured for deployment to Bedrock AgentCore

## Development Scripts

```bash
# Run in development mode
bun run dev

# Build for production
bun run build

# Type checking
bun run type-check
```

## Customization Guide

### 1. Define Your Agent Purpose

Edit `src/index.ts` and update:
- Agent name
- System prompt (persona and capabilities)
- Model selection

### 2. Create Your Tools

1. Define types in `src/types/index.ts`
2. Implement tools in `src/tools/`
3. Register tools in `src/index.ts`

See `docs/catalogs/common-tools-catalog.md` for reusable patterns.

### 3. Replace Mock Data

Update `src/data/mockData.ts` with your data sources:
- API integrations
- Database queries
- External services

### 4. Add Subagents (Optional)

For specialized tasks, add subagents in `src/index.ts`.

Example use cases:
- Deep analysis (Sonnet)
- Quick calculations (Haiku)
- Specialized domain expertise

### 5. Implement Interaction Logic

Choose your interface:
- CLI (stdin/stdout)
- HTTP API (Express/Fastify)
- WebSocket (real-time)
- Bedrock AgentCore deployment

### 6. Document Your Agent

Update `.claude/CLAUDE.md` with:
- Agent overview
- Tool descriptions
- Setup instructions
- Example usage

## Tool Design Best Practices

✅ **Keep tools focused** - One clear purpose per tool
✅ **Validate inputs** - Use Zod schemas for type safety
✅ **Return structured data** - Not just strings
✅ **Handle errors gracefully** - Provide actionable messages
✅ **Add clear documentation** - JSDoc comments for all tools

## Next Steps

1. Review `docs/workflows/agent-ideation-workflow.md` for development process
2. Check `docs/catalogs/common-tools-catalog.md` for tool patterns
3. See `docs/catalogs/mcp-integration-patterns.md` for MCP server usage
4. Update root `CLAUDE.md` "Existing Agents" section when done
5. Add entry to `docs/comparisons/agent-comparison-matrix.md`

## Resources

- [Claude Agent SDK Documentation](https://docs.anthropic.com/claude/agent-sdk)
- [Repository Root CLAUDE.md](../../CLAUDE.md)
- [Agent Ideation Workflow](../../docs/workflows/agent-ideation-workflow.md)
- [Common Tools Catalog](../../docs/catalogs/common-tools-catalog.md)

## Support

For issues or questions:
- Check `.claude/CLAUDE.md` for project-specific documentation
- Review root `CLAUDE.md` for repository guidelines
- See `docs/` for comprehensive documentation

---

**Remember:** Excellence is doing simple things extremely well. Start simple, test often, and iterate based on feedback.
