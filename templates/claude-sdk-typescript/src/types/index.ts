import { z } from 'zod';

/**
 * Type definitions and Zod schemas for the agent
 *
 * This file contains:
 * - Input/output schemas for tools
 * - TypeScript types derived from schemas
 * - Data models used throughout the agent
 */

// ============================================================================
// Example Tool Schema
// ============================================================================

// Example: Define input schema for a tool
export const ExampleToolInputSchema = z.object({
  query: z.string().min(1, 'Query is required'),
  limit: z.number().int().positive().max(100).optional().default(10),
  options: z.object({
    sortBy: z.enum(['relevance', 'date', 'popularity']).optional(),
    includeMetadata: z.boolean().optional().default(false),
  }).optional(),
});

// Derive TypeScript type from schema
export type ExampleToolInput = z.infer<typeof ExampleToolInputSchema>;

// Example: Define output type
export interface ExampleToolOutput {
  results: Array<{
    id: string;
    title: string;
    description: string;
    score: number;
  }>;
  metadata: {
    totalCount: number;
    processingTime: number;
  };
}

// ============================================================================
// Agent State (if needed)
// ============================================================================

// Example: Define agent state for multi-turn conversations
export interface AgentState {
  conversationStage: 'initial' | 'gathering' | 'processing' | 'completed';
  collectedData: Record<string, any>;
  userPreferences?: Record<string, any>;
}

// ============================================================================
// Common Data Models
// ============================================================================

// Add your domain-specific data models here
// Example:
export interface User {
  id: string;
  name: string;
  email: string;
  preferences: Record<string, any>;
}

// ============================================================================
// Error Types
// ============================================================================

export class AgentError extends Error {
  constructor(
    message: string,
    public code: string,
    public details?: Record<string, any>
  ) {
    super(message);
    this.name = 'AgentError';
  }
}
