import { ExampleToolInputSchema, type ExampleToolInput, type ExampleToolOutput, AgentError } from '../types/index.js';

/**
 * Example tool implementations
 *
 * This file contains example tools demonstrating best practices:
 * - Input validation with Zod
 * - Proper error handling
 * - Structured output
 * - Clear documentation
 *
 * Replace these examples with your own domain-specific tools.
 */

/**
 * Example Tool: Search or query functionality
 *
 * This demonstrates a common pattern for search/query tools
 * Replace with your actual implementation
 */
export async function exampleSearchTool(
  input: ExampleToolInput
): Promise<ExampleToolOutput> {
  try {
    // Validate input using Zod schema
    const validated = ExampleToolInputSchema.parse(input);

    // TODO: Replace with your actual implementation
    // Example: Call external API, query database, etc.

    // Mock implementation for demonstration
    const results = [
      {
        id: '1',
        title: 'Example Result 1',
        description: 'This is a mock result for demonstration',
        score: 95,
      },
      {
        id: '2',
        title: 'Example Result 2',
        description: 'Replace this with your actual data',
        score: 87,
      },
    ].slice(0, validated.limit);

    return {
      results,
      metadata: {
        totalCount: results.length,
        processingTime: Date.now(),
      },
    };
  } catch (error) {
    // Handle validation errors
    if (error instanceof Error) {
      throw new AgentError(
        `Search failed: ${error.message}`,
        'SEARCH_ERROR',
        { originalError: error.message }
      );
    }
    throw error;
  }
}

/**
 * Example Tool: Data analysis or calculation
 *
 * This demonstrates a calculation/analysis tool pattern
 */
export async function exampleAnalysisTool(input: {
  data: number[];
  operation: 'sum' | 'average' | 'max' | 'min';
}): Promise<{ result: number; operation: string }> {
  try {
    if (!input.data || input.data.length === 0) {
      throw new AgentError(
        'Data array is required and cannot be empty',
        'INVALID_INPUT'
      );
    }

    let result: number;

    switch (input.operation) {
      case 'sum':
        result = input.data.reduce((acc, val) => acc + val, 0);
        break;
      case 'average':
        result = input.data.reduce((acc, val) => acc + val, 0) / input.data.length;
        break;
      case 'max':
        result = Math.max(...input.data);
        break;
      case 'min':
        result = Math.min(...input.data);
        break;
      default:
        throw new AgentError(
          `Unknown operation: ${input.operation}`,
          'UNKNOWN_OPERATION'
        );
    }

    return {
      result,
      operation: input.operation,
    };
  } catch (error) {
    if (error instanceof AgentError) {
      throw error;
    }
    throw new AgentError(
      'Analysis failed',
      'ANALYSIS_ERROR',
      { originalError: error }
    );
  }
}

/**
 * Example Tool: Data retrieval
 *
 * This demonstrates fetching data from external sources
 */
export async function exampleFetchTool(input: {
  resourceId: string;
}): Promise<{ resource: any; fetchedAt: string }> {
  try {
    if (!input.resourceId) {
      throw new AgentError('Resource ID is required', 'INVALID_INPUT');
    }

    // TODO: Replace with actual API call
    // Example: const response = await fetch(`https://api.example.com/resource/${input.resourceId}`);

    // Mock implementation
    const resource = {
      id: input.resourceId,
      name: 'Example Resource',
      data: {
        // Your resource data
      },
    };

    return {
      resource,
      fetchedAt: new Date().toISOString(),
    };
  } catch (error) {
    if (error instanceof AgentError) {
      throw error;
    }
    throw new AgentError(
      'Failed to fetch resource',
      'FETCH_ERROR',
      { resourceId: input.resourceId, originalError: error }
    );
  }
}

/**
 * Add your own tools below
 *
 * Tool Design Best Practices:
 * 1. Keep tools focused (one clear purpose per tool)
 * 2. Validate all inputs with Zod schemas
 * 3. Return structured data (not just strings)
 * 4. Include comprehensive error handling
 * 5. Add clear JSDoc comments
 * 6. Use TypeScript types for safety
 *
 * Example template for a new tool:
 *
 * export async function myCustomTool(
 *   input: MyToolInput
 * ): Promise<MyToolOutput> {
 *   try {
 *     // Validate input
 *     const validated = MyToolInputSchema.parse(input);
 *
 *     // Implement tool logic
 *     // ...
 *
 *     // Return structured output
 *     return {
 *       // your output
 *     };
 *   } catch (error) {
 *     throw new AgentError(
 *       'Tool failed',
 *       'TOOL_ERROR',
 *       { originalError: error }
 *     );
 *   }
 * }
 */
