import 'dotenv/config';
import { Agent } from '@anthropic-ai/agent-sdk';
import { exampleSearchTool, exampleAnalysisTool, exampleFetchTool } from './tools/exampleTools.js';
import type { AgentState } from './types/index.js';

/**
 * Claude Agent SDK Template
 *
 * This template provides a starting point for building Claude agents.
 * Follow these steps to customize:
 *
 * 1. Update agent configuration below
 * 2. Replace example tools with your domain-specific tools
 * 3. Customize the system prompt
 * 4. Add subagents if needed
 * 5. Test and iterate
 *
 * See CLAUDE.md for detailed instructions
 */

// ============================================================================
// Agent Configuration
// ============================================================================

const agent = new Agent({
  // Agent name (displayed in console and logs)
  name: 'My Agent',

  // Model configuration
  model: 'claude-sonnet-4-5-20250929',

  // System prompt defines the agent's persona and behavior
  systemPrompt: `You are a helpful AI assistant.

Your role and expertise:
- [Describe your agent's role]
- [List key capabilities]
- [Specify domain expertise]

Your approach:
- Be clear and concise
- Ask clarifying questions when needed
- Use available tools to provide accurate information
- Admit when you don't know something

Available tools:
- example_search_tool: Search and query functionality
- example_analysis_tool: Perform calculations and analysis
- example_fetch_tool: Retrieve data from external sources

[Customize this prompt based on your agent's purpose]`,

  // Tool definitions
  tools: [
    {
      name: 'example_search_tool',
      description: 'Search for information based on a query. Use this when the user asks to find or search for something.',
      input_schema: {
        type: 'object',
        properties: {
          query: {
            type: 'string',
            description: 'The search query',
          },
          limit: {
            type: 'number',
            description: 'Maximum number of results to return (default: 10)',
          },
        },
        required: ['query'],
      },
      handler: async (input) => {
        return await exampleSearchTool(input);
      },
    },
    {
      name: 'example_analysis_tool',
      description: 'Perform mathematical operations on numeric data. Use this for calculations.',
      input_schema: {
        type: 'object',
        properties: {
          data: {
            type: 'array',
            items: { type: 'number' },
            description: 'Array of numbers to analyze',
          },
          operation: {
            type: 'string',
            enum: ['sum', 'average', 'max', 'min'],
            description: 'Operation to perform on the data',
          },
        },
        required: ['data', 'operation'],
      },
      handler: async (input) => {
        return await exampleAnalysisTool(input);
      },
    },
    {
      name: 'example_fetch_tool',
      description: 'Retrieve a specific resource by ID',
      input_schema: {
        type: 'object',
        properties: {
          resourceId: {
            type: 'string',
            description: 'The ID of the resource to fetch',
          },
        },
        required: ['resourceId'],
      },
      handler: async (input) => {
        return await exampleFetchTool(input);
      },
    },
  ],

  // Optional: Additional configuration
  // maxTokens: 4096,
  // temperature: 1.0,
});

// ============================================================================
// Optional: Subagent Configuration
// ============================================================================

// Example: Create a specialized subagent for complex analysis
// Uncomment and customize if you need subagents

/*
const analysisSubagent = new Agent({
  name: 'Analysis Specialist',
  model: 'claude-sonnet-4-5-20250929',
  systemPrompt: `You are a specialist in data analysis and calculations.
Your role is to perform deep analysis on data and provide detailed insights.
Focus on accuracy and thoroughness in your analysis.`,
  tools: [
    {
      name: 'detailed_analysis',
      description: 'Perform detailed analysis with statistical insights',
      input_schema: {
        type: 'object',
        properties: {
          data: { type: 'array', items: { type: 'number' } },
        },
        required: ['data'],
      },
      handler: async (input) => {
        // Implement detailed analysis
        return { analysis: 'detailed results' };
      },
    },
  ],
});

// Add subagent to main agent
agent.registerSubagent('analysis_specialist', analysisSubagent);
*/

// ============================================================================
// Main Execution
// ============================================================================

async function main() {
  // Check for API key
  if (!process.env.ANTHROPIC_API_KEY) {
    console.error('Error: ANTHROPIC_API_KEY environment variable is not set');
    console.error('Please create a .env file with your Anthropic API key');
    console.error('See .env.example for template');
    process.exit(1);
  }

  console.log('🤖 Agent initialized and ready!');
  console.log('Agent name:', agent.name);
  console.log('Model:', agent.model);
  console.log('Tools:', agent.tools.map(t => t.name).join(', '));
  console.log('');

  // Example: Run a test query
  // Uncomment to test your agent
  /*
  try {
    console.log('Testing agent with example query...\n');

    const response = await agent.run({
      messages: [
        {
          role: 'user',
          content: 'Hello! Can you search for example data and analyze the results?',
        },
      ],
    });

    console.log('Agent response:', response.content);
  } catch (error) {
    console.error('Error running agent:', error);
  }
  */

  // TODO: Implement your agent interaction logic
  // Options:
  // 1. CLI interface (read from stdin)
  // 2. HTTP API (Express/Fastify server)
  // 3. WebSocket server for real-time chat
  // 4. Deploy to Bedrock AgentCore
  //
  // See examples in agents/claude-sdk/typescript/ for inspiration

  console.log('Agent is running. Add your interaction logic here.');
  console.log('See CLAUDE.md for examples and deployment options.');
}

// ============================================================================
// Error Handling
// ============================================================================

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});

// ============================================================================
// Next Steps
// ============================================================================

/**
 * TODO: Customize this template
 *
 * 1. Define your agent's purpose and update system prompt
 * 2. Replace example tools with your domain-specific tools
 * 3. Update type definitions in src/types/index.ts
 * 4. Replace mock data in src/data/mockData.ts with real data sources
 * 5. Add subagents if needed for specialized tasks
 * 6. Implement your interaction interface (CLI, API, etc.)
 * 7. Add error handling and logging
 * 8. Write tests for your tools
 * 9. Update CLAUDE.md with your agent's documentation
 * 10. Deploy to your target environment
 *
 * Resources:
 * - docs/workflows/agent-ideation-workflow.md - Step-by-step development process
 * - docs/catalogs/common-tools-catalog.md - Reusable tool patterns
 * - docs/catalogs/mcp-integration-patterns.md - MCP server usage
 * - Root CLAUDE.md - Repository structure and guidelines
 */
