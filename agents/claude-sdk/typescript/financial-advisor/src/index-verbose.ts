#!/usr/bin/env node

import 'dotenv/config';
import { query } from '@anthropic-ai/claude-agent-sdk';
import { annuityToolsServer } from './tools/annuity-tools.js';
import { sampleClients } from './data/mock-portfolios.js';

/**
 * Verbose version of the financial advisor agent
 * Shows detailed execution trace with tool calls and reasoning
 */

// Same configuration as main agent
const SYSTEM_PROMPT = `You are an expert financial advisor specializing in annuity allocation and retirement income planning.

## Your Role

You help clients make informed decisions about annuity investments by:
- Assessing annuity suitability based on individual circumstances
- Calculating projected payouts and returns
- Comparing different annuity types objectively
- Optimizing portfolio allocation for retirement income
- Analyzing tax implications and strategies

## Core Principles

1. **Fiduciary Responsibility** - Always act in the client's best interest
2. **Transparency** - Explain fees, limitations, and trade-offs clearly
3. **Holistic Analysis** - Consider the entire financial picture, not just annuities
4. **Education** - Help clients understand complex concepts in simple terms
5. **Compliance** - Ensure all recommendations meet suitability standards

## Typical Workflow

Follow this structured approach for consultations:

### 1. Discovery Phase
- Gather client information (age, savings, income, expenses, goals)
- Understand risk tolerance and investment objectives
- Review existing portfolio and annuity holdings
- Identify income needs and retirement timeline

### 2. Assessment Phase
- Analyze annuity suitability using assess_annuity_suitability tool
- Review current portfolio allocation
- Identify income gaps or protection needs
- Evaluate existing annuity exposure

### 3. Analysis Phase
- Calculate projected payouts for relevant options
- Compare annuity types (fixed, variable, indexed)
- Assess portfolio allocation recommendations
- Analyze tax implications (qualified vs non-qualified)

### 4. Recommendation Phase
- Present recommended annuity type and allocation percentage
- Explain pros, cons, and rationale clearly
- Highlight any warnings or concerns
- Discuss alternative approaches if applicable

### 5. Documentation Phase
- Summarize key findings and recommendations
- Document reasoning for compliance
- Provide action steps
- Set expectations for next steps

## Available Tools

You have access to specialized annuity analysis tools:
- **analyze_annuity_suitability** - Assess if annuity fits client profile
- **calculate_annuity_payout** - Project income from annuity investments
- **compare_annuity_types** - Compare fixed, variable, and indexed options
- **assess_portfolio_allocation** - Recommend optimal annuity percentage
- **evaluate_tax_implications** - Analyze tax benefits and RMD impacts
- **fetch_annuity_rates** - Get current market rates and products

## Specialized Subagents

You can delegate to specialized subagents when needed:
- **annuity-analyzer** - Deep product analysis and payout calculations
- **risk-assessor** - Portfolio risk and tax optimization

## Important Guidelines

- **Suitability first**: Always assess suitability before recommending products
- **Fee transparency**: Clearly explain all fees and surrender charges
- **Liquidity warning**: Remind clients about reduced liquidity with annuities
- **Age considerations**: Tailor recommendations to client life stage
- **Tax efficiency**: Consider qualified vs non-qualified implications
- **Over-allocation risk**: Warn if annuity exposure exceeds 40% of portfolio
- **Realistic projections**: Use conservative assumptions in calculations

## Sample Clients Available

For testing, you have access to 5 sample client profiles:
1. Sarah Johnson (62, conservative, $750k savings)
2. Michael Chen (58, moderate, $1.2M savings)
3. Linda Martinez (70, conservative, $450k savings)
4. David Thompson (55, aggressive, $900k savings)
5. Emily Rodriguez (67, moderate, $580k savings)

Use "sample-1", "sample-2", etc. or client names to access their profiles.

## Communication Style

- Use clear, jargon-free language
- Provide specific numbers and calculations
- Explain the "why" behind recommendations
- Present both benefits and drawbacks honestly
- Format key findings in organized sections

Remember: Your goal is to help clients make well-informed decisions about annuity allocation that align with their retirement income goals and risk tolerance.`;

const agentOptions = {
  model: 'claude-sonnet-4-5' as const,
  systemPrompt: SYSTEM_PROMPT,
  mcpServers: {
    'annuity-tools': annuityToolsServer
  },
  allowedTools: [
    'Read',
    'mcp__annuity-tools__analyze_annuity_suitability',
    'mcp__annuity-tools__calculate_annuity_payout',
    'mcp__annuity-tools__compare_annuity_types',
    'mcp__annuity-tools__assess_portfolio_allocation',
    'mcp__annuity-tools__evaluate_tax_implications',
    'mcp__annuity-tools__fetch_annuity_rates'
  ],
  agents: {
    'annuity-analyzer': {
      description: 'Expert in deep analysis of annuity products, suitability assessment, and payout calculations.',
      prompt: `You are an expert annuity analyst. Focus on detailed product analysis and accurate calculations.`,
      tools: [
        'Read',
        'mcp__annuity-tools__analyze_annuity_suitability',
        'mcp__annuity-tools__calculate_annuity_payout',
        'mcp__annuity-tools__compare_annuity_types',
        'mcp__annuity-tools__fetch_annuity_rates'
      ],
      model: 'sonnet' as const
    },
    'risk-assessor': {
      description: 'Portfolio risk analyst specializing in asset allocation and tax optimization.',
      prompt: `You are a portfolio risk assessment specialist. Focus on holistic analysis and tax efficiency.`,
      tools: [
        'Read',
        'mcp__annuity-tools__assess_portfolio_allocation',
        'mcp__annuity-tools__evaluate_tax_implications',
        'mcp__annuity-tools__fetch_annuity_rates'
      ],
      model: 'haiku' as const
    }
  },
  permissionMode: 'default' as const,
  workingDirectory: process.cwd()
};

// Execution trace
interface ExecutionStep {
  step: number;
  type: 'thinking' | 'tool_call' | 'subagent' | 'result';
  description: string;
  details?: any;
  timestamp: number;
}

const executionTrace: ExecutionStep[] = [];
let stepCounter = 0;

async function runFinancialAdvisorVerbose() {
  const args = process.argv.slice(2);
  const userPrompt = args.length > 0
    ? args.join(' ')
    : 'I need help understanding annuity allocation options';

  console.log('╔════════════════════════════════════════════════════════════════╗');
  console.log('║  Financial Advisor Agent - VERBOSE MODE (Execution Trace)    ║');
  console.log('╚════════════════════════════════════════════════════════════════╝\n');
  console.log(`📋 Query: ${userPrompt}\n`);
  console.log('─'.repeat(64) + '\n');

  const startTime = Date.now();

  try {
    const response = query({
      prompt: userPrompt,
      options: agentOptions
    });

    let sessionId: string | undefined;
    let currentToolCall: string | undefined;

    for await (const message of response) {
      if (message.type === 'system') {
        if ('session_id' in message) {
          sessionId = message.session_id as string;
          console.log(`✓ Session started: ${sessionId}\n`);
          executionTrace.push({
            step: ++stepCounter,
            type: 'result',
            description: 'Session initialized',
            details: { sessionId },
            timestamp: Date.now() - startTime
          });
        }
      } else if (message.type === 'assistant') {
        const msg = message.message as any;

        // Check if this is a tool call
        if (msg.content && Array.isArray(msg.content)) {
          for (const block of msg.content) {
            if (block.type === 'text') {
              console.log(`\n💭 Agent Thinking:\n${block.text}\n`);
              executionTrace.push({
                step: ++stepCounter,
                type: 'thinking',
                description: 'Agent reasoning',
                details: block.text,
                timestamp: Date.now() - startTime
              });
            } else if (block.type === 'tool_use') {
              currentToolCall = block.name;
              console.log(`\n🔧 Tool Call: ${block.name}`);
              console.log(`   Input: ${JSON.stringify(block.input, null, 2)}\n`);
              executionTrace.push({
                step: ++stepCounter,
                type: 'tool_call',
                description: `Calling ${block.name}`,
                details: { name: block.name, input: block.input },
                timestamp: Date.now() - startTime
              });
            }
          }
        }
      } else if (message.type === 'user') {
        // This is a tool result
        const msg = message.message as any;
        if (msg.content && Array.isArray(msg.content)) {
          for (const block of msg.content) {
            if (block.type === 'tool_result') {
              console.log(`✓ Tool Result: ${currentToolCall}`);
              console.log(`   ${block.content[0]?.text?.substring(0, 200)}...\n`);
              executionTrace.push({
                step: ++stepCounter,
                type: 'result',
                description: `${currentToolCall} completed`,
                details: { result: block.content[0]?.text },
                timestamp: Date.now() - startTime
              });
            }
          }
        }
      } else if (message.type === 'result') {
        const result = message as any;
        console.log('\n' + '─'.repeat(64));
        console.log('\n📊 EXECUTION SUMMARY\n');
        console.log(`Duration: ${result.duration_ms}ms`);
        console.log(`API Time: ${result.duration_api_ms}ms`);
        console.log(`Turns: ${result.num_turns}`);
        console.log(`Cost: $${result.total_cost_usd?.toFixed(4) || '0.0000'}`);
        console.log(`\nFinal Result:\n${result.result}\n`);

        // Print execution trace
        console.log('\n' + '═'.repeat(64));
        console.log('EXECUTION TRACE');
        console.log('═'.repeat(64) + '\n');

        executionTrace.forEach(step => {
          const icon = {
            'thinking': '💭',
            'tool_call': '🔧',
            'subagent': '🤖',
            'result': '✓'
          }[step.type];

          console.log(`${icon} Step ${step.step} [${step.timestamp}ms] - ${step.description}`);
          if (step.type === 'tool_call' && step.details) {
            console.log(`   Tool: ${step.details.name}`);
            console.log(`   Input: ${JSON.stringify(step.details.input)}`);
          }
        });

        console.log('\n' + '═'.repeat(64));
        console.log('\n✅ Consultation completed successfully\n');
      }
    }

  } catch (error) {
    console.error('\n❌ Fatal error:', error);
    process.exit(1);
  }
}

runFinancialAdvisorVerbose();
