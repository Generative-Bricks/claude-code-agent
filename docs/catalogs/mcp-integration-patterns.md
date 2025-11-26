# MCP Integration Patterns

**Purpose:** Document best practices and patterns for integrating Model Context Protocol (MCP) servers with AI agents.

**Scope:** This repository has access to multiple MCP servers (AWS, Context7, Strands, Memory, etc.). This document shows how to use them effectively in agent development.

---

## 📖 Available MCP Servers

Configured in `.mcp.json`:

| MCP Server | Purpose | Primary Use Cases |
|-----------|---------|-------------------|
| **bedrock-agentcore-mcp-server** | Bedrock AgentCore docs | Deploying agents to AWS Bedrock |
| **awslabs.core-mcp-server** | AWS prompt understanding | Expert AWS advice |
| **awslabs.aws-documentation-mcp-server** | AWS docs search | Fetching AWS documentation |
| **awslabs.code-doc-gen-mcp-server** | Code documentation | Generating project docs |
| **awslabs.frontend-mcp-server** | Web app guidance | React & frontend development |
| **aws-knowledge-mcp-server** | AWS regional availability | Checking service availability |
| **context7** | Library documentation | SDK/framework docs |
| **fetch** | Web content retrieval | Fetching web pages |
| **strands-agents-mcp** | Strands framework docs | Building Strands agents |
| **powertools** | Powertools for AWS Lambda | Serverless best practices |
| **memory** | Knowledge graph | Storing agent memories |
| **time** | Time zone conversions | Time-related queries |
| **ide** | VS Code integration | Code diagnostics & execution |

---

## 🎯 Integration Patterns

### Pattern 1: Documentation Retrieval Pattern

**Use Case:** Fetching up-to-date SDK or framework documentation during agent development.

**MCP Servers:** `context7`, `strands-agents-mcp`, `awslabs.aws-documentation-mcp-server`

**When to Use:**
- Building tools that interact with specific SDKs
- Need latest API documentation
- Verifying best practices
- Learning new framework features

**Example: Fetching Claude SDK Documentation**

```typescript
// Step 1: Get the correct library ID from docs/references/context7-library-ids-reference.md
const libraryId = '/anthropics/anthropic-sdk-typescript';

// Step 2: Fetch documentation
const docs = await mcp__context7__get_library_docs({
  context7CompatibleLibraryID: libraryId,
  topic: 'tool calling', // Optional: focus on specific topic
  tokens: 5000, // Optional: limit response size
});

// Step 3: Use documentation to inform tool development
// The docs contain code examples and best practices
```

**Best Practices:**
✅ **Store library IDs** in `docs/references/context7-library-ids-reference.md`
✅ **Use topic parameter** to get focused documentation
✅ **Cache results** if fetching repeatedly
✅ **Verify library ID** with `resolve-library-id` tool first

**Common Pitfalls:**
❌ Hard-coding library IDs (they may change)
❌ Not specifying topic (returns too much irrelevant info)
❌ Forgetting to check `docs/references/` first

---

### Pattern 2: Memory Persistence Pattern

**Use Case:** Storing agent learnings, architectural decisions, and patterns across sessions.

**MCP Server:** `memory`

**When to Use:**
- Capturing architectural decisions
- Storing user preferences
- Building knowledge graphs
- Learning from agent interactions

**Example: Storing Agent Learnings**

```typescript
// Create entity for new agent
await mcp__memory__create_entities({
  entities: [
    {
      name: 'my-new-agent',
      entityType: 'Agent',
      observations: [
        'Customer service agent for e-commerce support',
        'Handles order tracking, returns, and product questions',
        'Uses 5 tools with Zod validation',
        'Implemented workflow: Greeting → Identify Issue → Resolve → Follow-up',
      ],
    },
  ],
});

// Create relations to other entities
await mcp__memory__create_relations({
  relations: [
    {
      from: 'my-new-agent',
      to: 'Claude SDK',
      relationType: 'uses',
    },
    {
      from: 'my-new-agent',
      to: 'TypeScript',
      relationType: 'implemented_in',
    },
  ],
});

// Add observations about patterns used
await mcp__memory__add_observations({
  observations: [
    {
      entityName: 'Zod Validation Pattern',
      contents: [
        'Successfully used in my-new-agent for order validation',
        'Caught 15 edge cases during testing',
      ],
    },
  ],
});
```

**Best Practices:**
✅ **Create entities** for agents, patterns, and learnings
✅ **Use relations** to connect related concepts
✅ **Add observations** as you discover insights
✅ **Search memory** before building new patterns
✅ **Update regularly** throughout development

**Memory Entity Types:**
- `Agent` - Individual agent implementations
- `SDK` - Frameworks and SDKs
- `Language` - Programming languages
- `Pattern` - Reusable patterns
- `Tool` - Individual tools
- `MCPServer` - MCP server integrations
- `Documentation` - Documentation references
- `Architectural Decision` - Key design decisions
- `Learning` - Insights and gotchas

---

### Pattern 3: AWS Documentation Search Pattern

**Use Case:** Finding AWS service documentation and best practices.

**MCP Server:** `awslabs.aws-documentation-mcp-server`

**When to Use:**
- Deploying agents to AWS
- Integrating with AWS services
- Learning AWS best practices
- Troubleshooting AWS issues

**Example: Finding Lambda Documentation**

```typescript
// Step 1: Search for relevant documentation
const searchResults = await mcp__awslabs_aws_documentation_mcp_server__search_documentation({
  search_phrase: 'Lambda function URLs',
  limit: 10,
});

// Step 2: Read the most relevant page
const topResult = searchResults[0];
const docContent = await mcp__awslabs_aws_documentation_mcp_server__read_documentation({
  url: topResult.url,
  max_length: 5000,
  start_index: 0,
});

// Step 3: Get related content recommendations
const recommendations = await mcp__awslabs_aws_documentation_mcp_server__recommend({
  url: topResult.url,
});

// Check "New" recommendations for recently released features
const newFeatures = recommendations.filter(r => r.type === 'New');
```

**Best Practices:**
✅ **Use specific search terms** ("Lambda function URLs" vs "Lambda")
✅ **Read documentation** don't just rely on search results
✅ **Check recommendations** for related content
✅ **Look at "New" recommendations** for recent updates
✅ **Paginate long documents** with `start_index`

**Search Tips:**
- Include service names for better results
- Use technical terms rather than general phrases
- Try abbreviations and alternative terms
- Use quotes for exact phrase matching

---

### Pattern 4: Regional Availability Check Pattern

**Use Case:** Verifying AWS service availability before deployment.

**MCP Server:** `aws-knowledge-mcp-server`

**When to Use:**
- Planning multi-region deployments
- Checking feature availability
- Validating CloudFormation resources
- Architecture design decisions

**Example: Checking Bedrock Availability**

```typescript
// Check if Bedrock is available in target region
const availability = await mcp__aws_knowledge_mcp_server__aws___get_regional_availability({
  region: 'us-east-1',
  resource_type: 'product',
  filters: ['Amazon Bedrock', 'AWS Lambda'],
});

// Check specific API availability
const apiAvailability = await mcp__aws_knowledge_mcp_server__aws___get_regional_availability({
  region: 'eu-west-1',
  resource_type: 'api',
  filters: ['Bedrock Runtime+InvokeModel', 'Lambda+CreateFunction'],
});

// List all AWS regions
const regions = await mcp__aws_knowledge_mcp_server__aws___list_regions();
```

**Best Practices:**
✅ **Check before deploying** to avoid region-specific failures
✅ **Use specific resource names** for accurate results
✅ **Check both products and APIs** for complete picture
✅ **Document region constraints** in agent CLAUDE.md

---

### Pattern 5: Code Documentation Generation Pattern

**Use Case:** Automatically generating comprehensive documentation for agent code.

**MCP Server:** `awslabs.code-doc-gen-mcp-server`

**When to Use:**
- Documenting completed agents
- Creating project README files
- Generating API documentation
- Onboarding new developers

**Example: Generating Agent Documentation**

```typescript
// Step 1: Prepare repository for analysis
const preparedRepo = await mcp__awslabs_code_doc_gen_mcp_server__prepare_repository({
  project_root: '/path/to/agent',
});

// Step 2: Analyze directory structure and create ProjectAnalysis
// (You manually fill out the ProjectAnalysis based on your code review)
const analysis: ProjectAnalysis = {
  project_type: 'AI Agent',
  features: ['Tool calling', 'Subagent support', 'Zod validation'],
  file_structure: preparedRepo.file_structure,
  dependencies: { '@anthropic-ai/agent-sdk': '0.1.37' },
  primary_languages: ['TypeScript'],
  has_infrastructure_as_code: false,
};

// Step 3: Create documentation context
const docContext = await mcp__awslabs_code_doc_gen_mcp_server__create_context({
  project_root: '/path/to/agent',
  analysis,
});

// Step 4: Plan documentation structure
const docPlan = await mcp__awslabs_code_doc_gen_mcp_server__plan_documentation({
  doc_context: docContext,
});

// Step 5: Generate documentation (with empty sections for you to fill)
const generatedDocs = await mcp__awslabs_code_doc_gen_mcp_server__generate_documentation({
  plan: docPlan,
  doc_context: docContext,
});

// YOU must then fill in all empty sections with detailed content
```

**Best Practices:**
✅ **Analyze code first** before creating ProjectAnalysis
✅ **Fill out all sections** of ProjectAnalysis accurately
✅ **Write detailed content** for generated sections (don't leave empty)
✅ **Include code examples** in documentation
✅ **Update regularly** as agent evolves

---

### Pattern 6: Library Documentation Lookup Pattern

**Use Case:** Quick reference lookup for SDK methods, patterns, or best practices.

**MCP Server:** `context7`

**When to Use:**
- Implementing specific SDK features
- Verifying method signatures
- Finding code examples
- Learning framework patterns

**Example: Looking Up Strands Agents Patterns**

```typescript
// First, resolve the library ID (or check docs/references/)
const libraryMatch = await mcp__context7__resolve_library_id({
  libraryName: 'strands agents',
});

// Fetch focused documentation
const strandsToolDocs = await mcp__context7__get_library_docs({
  context7CompatibleLibraryID: '/strands-agents/docs',
  topic: 'tools',
  tokens: 3000,
});

const strandsMCPDocs = await mcp__context7__get_library_docs({
  context7CompatibleLibraryID: '/strands-agents/docs',
  topic: 'MCP integration',
  tokens: 3000,
});
```

**Workflow:**
1. Check `docs/references/context7-library-ids-reference.md` for known IDs
2. If not found, use `resolve-library-id` to find the correct ID
3. Fetch documentation with specific `topic` parameter
4. Limit tokens to get focused, relevant information

---

## 🔄 Multi-Server Integration Patterns

### Pattern: Comprehensive Agent Development

**Scenario:** Building a new agent with AWS deployment and documentation.

**MCP Servers Used:** Multiple

**Workflow:**

```typescript
// 1. Research framework documentation (Context7)
const claudeSDKDocs = await mcp__context7__get_library_docs({
  context7CompatibleLibraryID: '/anthropics/anthropic-sdk-typescript',
  topic: 'getting started',
});

// 2. Check AWS service availability (AWS Knowledge)
const bedrockAvailable = await mcp__aws_knowledge_mcp_server__aws___get_regional_availability({
  region: 'us-east-1',
  resource_type: 'product',
  filters: ['Amazon Bedrock'],
});

// 3. Build agent implementation
// ... (your agent code)

// 4. Document architectural decisions (Memory)
await mcp__memory__create_entities({
  entities: [{
    name: 'my-deployment-decision',
    entityType: 'Architectural Decision',
    observations: [
      'Deployed to us-east-1 due to Bedrock availability',
      'Used Lambda function URLs for simple HTTP endpoint',
      'Chose Claude SDK over Strands for Anthropic-specific features',
    ],
  }],
});

// 5. Generate comprehensive documentation (Code Doc Gen)
const docs = await mcp__awslabs_code_doc_gen_mcp_server__generate_documentation({
  plan: docPlan,
  doc_context: docContext,
});

// 6. Research AWS deployment best practices (AWS Docs)
const lambdaDocs = await mcp__awslabs_aws_documentation_mcp_server__search_documentation({
  search_phrase: 'Lambda deployment best practices',
});
```

**This pattern demonstrates:**
- Starting with research (Context7)
- Validating deployment options (AWS Knowledge)
- Building the agent
- Documenting decisions (Memory)
- Generating documentation (Code Doc Gen)
- Learning deployment practices (AWS Docs)

---

## 📋 MCP Server Decision Matrix

**Which MCP server should I use?**

| Need | MCP Server | Tool Example |
|------|------------|--------------|
| **SDK documentation** | context7 | `get-library-docs` |
| **AWS service docs** | awslabs.aws-documentation-mcp-server | `search_documentation` |
| **AWS availability** | aws-knowledge-mcp-server | `get_regional_availability` |
| **Store learnings** | memory | `create_entities` |
| **Generate docs** | awslabs.code-doc-gen-mcp-server | `generate_documentation` |
| **Strands framework** | strands-agents-mcp | `search_docs` |
| **React patterns** | awslabs.frontend-mcp-server | `GetReactDocsByTopic` |
| **Serverless patterns** | powertools | `search_docs` |
| **Web content** | fetch | `fetch` |
| **Bedrock AgentCore** | bedrock-agentcore-mcp-server | `search_agentcore_docs` |

---

## ✅ Best Practices Summary

### General MCP Integration
1. **Check configured servers** in `.mcp.json` before integration
2. **Read server documentation** before first use
3. **Handle errors gracefully** (servers may be unavailable)
4. **Cache responses** when appropriate
5. **Limit response sizes** to avoid token waste

### Context7 Specific
1. **Maintain library ID reference** in `docs/references/`
2. **Use topic parameter** for focused results
3. **Verify library IDs** before fetching
4. **Update reference** when adding new SDKs

### Memory Server Specific
1. **Create entities consistently** (standardize entity types)
2. **Use clear relation types** (uses, implements, exemplifies)
3. **Add observations continuously** (not just at project end)
4. **Search before creating** (avoid duplicates)

### AWS Documentation Specific
1. **Use specific search terms** for better results
2. **Read full pages** not just snippets
3. **Check recommendations** for related content
4. **Look for new features** in recommendations

---

## 🚫 Anti-Patterns to Avoid

### Over-Fetching
❌ Fetching entire documentation when you only need one section
✅ Use topic parameter or specific searches

### Ignoring Errors
❌ Not handling MCP server unavailability
✅ Implement fallbacks and error messages

### Duplicate Storage
❌ Creating multiple memory entities for the same concept
✅ Search first, then create or update

### Hard-Coded Values
❌ Hard-coding library IDs or region names
✅ Reference from configuration files

### Forgetting to Document
❌ Not updating memory system with learnings
✅ Document decisions as you make them

---

## 📝 Configuration Example

Example `.mcp.json` configuration:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-memory"],
      "env": {
        "MEMORY_PATH": "./docs/memory"
      }
    },
    "awslabs.aws-documentation-mcp-server": {
      "command": "npx",
      "args": ["-y", "@awslabs/aws-documentation-mcp-server"]
    }
  }
}
```

---

## 🔗 Related Resources

- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [Context7 Library Reference](../references/context7-library-ids-reference.md)
- [Memory System](../memory/memory.jsonl)
- [Root CLAUDE.md](../../CLAUDE.md) - Available MCP servers section

---

**Next Steps:**
1. Review available MCP servers in `.mcp.json`
2. Identify which servers are useful for your agent
3. Implement integration patterns from this document
4. Document your MCP usage in agent CLAUDE.md
5. Share learnings in memory system

---

*Part of the claude-code-agent repository*
*See root CLAUDE.md for repository structure*
*See docs/workflows/agent-ideation-workflow.md for building new agents*
