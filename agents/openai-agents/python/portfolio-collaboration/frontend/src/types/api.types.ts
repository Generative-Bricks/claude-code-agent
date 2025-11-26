/**
 * API request/response types for Portfolio Collaboration System.
 *
 * These types define the contract between the React frontend and FastAPI backend.
 * They will match the API schemas once created in src/api/schemas.py
 *
 * All types use snake_case to match Python JSON serialization.
 */

import type {
  ClientProfile,
  Portfolio,
  PortfolioRecommendations,
} from './portfolio.types';

// ============================================================================
// Analysis Endpoint
// ============================================================================

/**
 * Request body for portfolio analysis.
 * POST /api/analyze
 */
export interface AnalysisRequest {
  client_profile: ClientProfile;
  portfolio: Portfolio;
}

/**
 * Response from portfolio analysis.
 * POST /api/analyze
 */
export interface AnalysisResponse {
  success: boolean;
  recommendations: PortfolioRecommendations;
  analysis_id: string;
  timestamp: string;  // ISO format
  execution_time_seconds: number;
}

// ============================================================================
// Client Listing Endpoint
// ============================================================================

/**
 * Summary information for a single client.
 * Used in client listing responses.
 */
export interface ClientSummary {
  client_id: string;
  age: number;
  risk_tolerance: string;
  net_worth?: number;
  time_horizon: number;  // years
}

/**
 * Response from client listing endpoint.
 * GET /api/clients
 */
export interface ClientListResponse {
  clients: ClientSummary[];
  total: number;
}

// ============================================================================
// Portfolio Listing Endpoint
// ============================================================================

/**
 * Summary information for a single portfolio.
 * Used in portfolio listing responses.
 */
export interface PortfolioSummary {
  portfolio_id: string;
  client_id: string;
  total_value: number;
  holdings_count: number;
  benchmark: string;
}

/**
 * Response from portfolio listing endpoint.
 * GET /api/portfolios?client_id={id}
 */
export interface PortfolioListResponse {
  portfolios: PortfolioSummary[];
  total: number;
}

// ============================================================================
// Portfolio Comparison Endpoint
// ============================================================================

/**
 * Request body for comparing multiple portfolios.
 * POST /api/compare
 */
export interface ComparisonRequest {
  client_profile: ClientProfile;
  portfolio_ids: string[];  // 2-5 portfolio IDs
}

/**
 * Single portfolio comparison result.
 */
export interface ComparisonResult {
  portfolio_id: string;
  recommendations: PortfolioRecommendations;
}

/**
 * Response from portfolio comparison.
 * POST /api/compare
 */
export interface ComparisonResponse {
  success: boolean;
  results: ComparisonResult[];
  best_fit_portfolio_id: string;
  timestamp: string;  // ISO format
}

// ============================================================================
// WebSocket Messages
// ============================================================================

/**
 * Type of agent streaming events.
 */
export type AgentEventType =
  | 'thinking'    // Agent is processing
  | 'tool_call'   // Agent is calling a tool
  | 'response'    // Agent is generating response
  | 'complete'    // Analysis complete
  | 'error';      // Error occurred

/**
 * Chat message sent to WebSocket.
 * WebSocket send payload
 */
export interface ChatMessage {
  message: string;
  session_id?: string;
}

/**
 * Agent streaming event from WebSocket.
 * WebSocket receive payload
 */
export interface AgentStreamEvent {
  event_type: AgentEventType;
  content: string;
  timestamp: string;  // ISO format
  metadata?: Record<string, any>;
}

// ============================================================================
// Error Response
// ============================================================================

/**
 * Standard error response format.
 * Returned on 4xx/5xx status codes
 */
export interface ErrorResponse {
  error: string;  // Error category
  message: string;  // Human-readable message
  type: string;  // Exception type (e.g., "ValueError")
  timestamp: string;  // ISO format
  details?: Record<string, any>;  // Additional error details
}

// ============================================================================
// Health Check
// ============================================================================

/**
 * API health status.
 */
export type HealthStatus = 'healthy' | 'degraded' | 'unhealthy';

/**
 * Health check response.
 * GET /health
 */
export interface HealthCheckResponse {
  status: HealthStatus;
  api_version: string;
  openai_configured: boolean;
  timestamp: string;  // ISO format
  checks?: Record<string, boolean>;  // Individual health checks
}

// ============================================================================
// Root Endpoint
// ============================================================================

/**
 * Root API information.
 * GET /
 */
export interface RootResponse {
  name: string;
  version: string;
  status: string;
  docs: string;  // URL to API documentation
}
