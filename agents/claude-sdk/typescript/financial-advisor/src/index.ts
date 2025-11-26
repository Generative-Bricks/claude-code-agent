#!/usr/bin/env node

import 'dotenv/config';
import { query } from '@anthropic-ai/claude-agent-sdk';
import { annuityToolsServer } from './tools/annuity-tools.js';
import { sampleClients } from './data/mock-portfolios.js';

/**
 * Financial Advisor Agent - Annuity Allocation Specialist
 *
 * This agent assists with annuity allocation decisions following the typical
 * financial advisor workflow:
 * 1. Discovery - Gather client information
 * 2. Assessment - Analyze current situation
 * 3. Analysis - Evaluate annuity options
 * 4. Recommendation - Present allocation strategy
 * 5. Documentation - Generate summary report
 */

// Main system prompt for the financial advisor agent
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

// Configuration for the financial advisor agent
const agentOptions = {
  model: 'claude-sonnet-4-5' as const,
  systemPrompt: SYSTEM_PROMPT,

  // Custom MCP tools for annuity analysis
  mcpServers: {
    'annuity-tools': annuityToolsServer
  },

  // Allowed tools for the main agent
  allowedTools: [
    'Read',
    'mcp__annuity-tools__analyze_annuity_suitability',
    'mcp__annuity-tools__calculate_annuity_payout',
    'mcp__annuity-tools__compare_annuity_types',
    'mcp__annuity-tools__assess_portfolio_allocation',
    'mcp__annuity-tools__evaluate_tax_implications',
    'mcp__annuity-tools__fetch_annuity_rates'
  ],

  // Specialized subagents for complex tasks
  agents: {
    'annuity-analyzer': {
      description: 'Expert in deep analysis of annuity products, suitability assessment, and payout calculations. Use for comprehensive annuity evaluation and product comparison.',
      prompt: `You are an expert annuity analyst. Focus on:
- Detailed product analysis and feature comparison
- Accurate payout projections and calculations
- Suitability scoring based on client profile
- Fee and surrender charge analysis
Always provide specific numbers and clear reasoning for recommendations.`,
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
      description: 'Portfolio risk analyst specializing in asset allocation and tax optimization. Use for portfolio analysis and allocation recommendations.',
      prompt: `You are a portfolio risk assessment specialist. Focus on:
- Holistic portfolio allocation analysis
- Risk-appropriate annuity percentage recommendations
- Tax-efficient strategy development
- Diversification and liquidity considerations
Always check for over-allocation and ensure adequate liquid reserves.`,
      tools: [
        'Read',
        'mcp__annuity-tools__assess_portfolio_allocation',
        'mcp__annuity-tools__evaluate_tax_implications',
        'mcp__annuity-tools__fetch_annuity_rates'
      ],
      model: 'haiku' as const
    }
  },

  // Permission mode
  permissionMode: 'default' as const,

  // Set working directory to project root
  workingDirectory: process.cwd()
};

/**
 * Main function to run the financial advisor agent
 */
async function runFinancialAdvisor() {
  // Get prompt from command line args or use default
  const args = process.argv.slice(2);
  const userPrompt = args.length > 0
    ? args.join(' ')
    : 'I need help understanding annuity allocation options for retirement planning';

  console.log('╔════════════════════════════════════════════════════════════════╗');
  console.log('║     Financial Advisor Agent - Annuity Allocation Specialist   ║');
  console.log('╚════════════════════════════════════════════════════════════════╝\n');
  console.log(`📋 Query: ${userPrompt}\n`);
  console.log('─'.repeat(64) + '\n');

  try {
    // Start the query
    const response = query({
      prompt: userPrompt,
      options: agentOptions
    });

    // Process streaming responses
    for await (const message of response) {
      // Handle different message types from the SDK
      if (message.type === 'system') {
        // System messages (init, status, etc.)
        if ('session_id' in message) {
          console.log(`✓ Session started\n`);
        }
      } else if (message.type === 'assistant') {
        // Assistant responses - just print the message
        console.log(JSON.stringify(message, null, 2));
      } else {
        // Other message types - log for debugging
        console.log(`[${message.type}]`, JSON.stringify(message, null, 2));
      }
    }

    console.log('\n' + '─'.repeat(64));
    console.log('\n✅ Consultation completed successfully\n');

  } catch (error) {
    console.error('\n❌ Fatal error:', error);

    if (error instanceof Error) {
      if ('code' in error) {
        const errorCode = (error as any).code;
        if (errorCode === 'AUTHENTICATION_FAILED') {
          console.error('\n💡 Tip: Check your ANTHROPIC_API_KEY environment variable');
        } else if (errorCode === 'RATE_LIMIT_EXCEEDED') {
          console.error('\n💡 Tip: Rate limit exceeded, please try again later');
        }
      }
    }

    process.exit(1);
  }
}

// Example usage scenarios for testing
function printExamples() {
  console.log('\n📚 Example Usage:\n');
  console.log('1. General consultation:');
  console.log('   npm run advisor "I need help with annuity allocation"\n');
  console.log('2. Specific client analysis:');
  console.log('   npm run advisor "Analyze annuity suitability for Sarah Johnson"\n');
  console.log('3. Portfolio review:');
  console.log('   npm run advisor "Review portfolio allocation for 65-year-old with $500k savings"\n');
  console.log('4. Product comparison:');
  console.log('   npm run advisor "Compare fixed vs indexed annuities for moderate risk investor"\n');
  console.log('5. Tax analysis:');
  console.log('   npm run advisor "Analyze tax implications of $200k annuity investment"\n');
}

// Show examples if --help flag is present
if (process.argv.includes('--help') || process.argv.includes('-h')) {
  printExamples();
  process.exit(0);
}

// Show available sample clients if --clients flag is present
if (process.argv.includes('--clients')) {
  console.log('\n👥 Available Sample Clients:\n');
  sampleClients.forEach((client, index) => {
    console.log(`${index + 1}. ${client.name}`);
    console.log(`   Age: ${client.age} | Risk: ${client.riskTolerance} | Savings: $${client.currentSavings.toLocaleString()}`);
    console.log(`   Goals: ${client.investmentGoals.join(', ')}\n`);
  });
  process.exit(0);
}

// Run the agent
runFinancialAdvisor();
