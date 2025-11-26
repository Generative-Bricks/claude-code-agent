/**
 * Central export point for all TypeScript types.
 *
 * Usage:
 *   import { ClientProfile, AnalysisRequest } from '@/types';
 */

// ============================================================================
// Portfolio Domain Types (from portfolio.types.ts)
// ============================================================================

export type {
  // Enumerations
  RiskTolerance,
  AssetClass,
  RiskRating,
  ComplianceStatus,
  SuitabilityInterpretation,

  // Client & Portfolio Models
  ClientProfile,
  Holding,
  Portfolio,

  // Agent Analysis Output Models
  RiskAnalysis,
  ComplianceReport,
  PerformanceReport,

  // Synthesis & Suitability Models
  SuitabilityScore,

  // Final Recommendations
  PortfolioRecommendations,

  // Tool Input/Output Models
  ParallelAnalysisInput,
  ParallelAnalysisOutput,

  // Equity Specialist Models
  EquityDeepDiveRequest,
  EquityDeepDiveReport,
} from './portfolio.types';

// ============================================================================
// API Types (from api.types.ts)
// ============================================================================

export type {
  // Analysis Endpoint
  AnalysisRequest,
  AnalysisResponse,

  // Client Listing
  ClientSummary,
  ClientListResponse,

  // Portfolio Listing
  PortfolioSummary,
  PortfolioListResponse,

  // Comparison Endpoint
  ComparisonRequest,
  ComparisonResult,
  ComparisonResponse,

  // WebSocket Messages
  AgentEventType,
  ChatMessage,
  AgentStreamEvent,

  // Error Response
  ErrorResponse,

  // Health Check
  HealthStatus,
  HealthCheckResponse,

  // Root Endpoint
  RootResponse,
} from './api.types';
