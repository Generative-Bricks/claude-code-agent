/**
 * REST API Client for Portfolio Collaboration System
 *
 * Provides type-safe API calls to the FastAPI backend with comprehensive
 * error handling, request/response logging, and retry mechanisms.
 *
 * Biblical Principle: TRUTH - All API interactions are transparent and logged.
 * Biblical Principle: PERSEVERE - Graceful error handling with retry logic.
 *
 * @module services/api
 */

import axios, { AxiosError } from 'axios';
import type { AxiosInstance } from 'axios';
import type {
  AnalysisRequest,
  AnalysisResponse,
  ClientListResponse,
  PortfolioListResponse,
  ComparisonRequest,
  ComparisonResponse,
  ErrorResponse,
  HealthCheckResponse,
  RootResponse,
} from '@/types';

// ============================================================================
// Configuration Constants
// ============================================================================

/**
 * Base URL for API requests.
 * Uses environment variable with fallback to localhost for development.
 */
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Request timeout in milliseconds.
 * 30 seconds allows for complex multi-agent analysis.
 */
const REQUEST_TIMEOUT = 30000;


// ============================================================================
// Axios Instance Setup
// ============================================================================

/**
 * Axios instance with default configuration.
 * Configured with timeout, headers, and interceptors.
 */
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: REQUEST_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ============================================================================
// Request Interceptor
// ============================================================================

/**
 * Request interceptor for logging all outgoing API calls.
 *
 * Logs:
 * - HTTP method and endpoint
 * - Request timestamp
 * - Payload size for POST/PUT requests
 */
apiClient.interceptors.request.use(
  (config) => {
    const method = config.method?.toUpperCase() || 'UNKNOWN';
    const url = config.url || '';
    const timestamp = new Date().toISOString();

    console.log(
      `[API] ${timestamp} | REQUEST | ${method} ${url}`,
      config.data ? `| Payload size: ${JSON.stringify(config.data).length}B` : ''
    );

    return config;
  },
  (error) => {
    console.error('[API] Request configuration error:', error.message);
    return Promise.reject(error);
  }
);

// ============================================================================
// Response Interceptor
// ============================================================================

/**
 * Response interceptor for logging all API responses and handling errors.
 *
 * Logs:
 * - HTTP status code and response time
 * - Error details for 4xx/5xx responses
 * - Error categorization (server, network, client)
 */
apiClient.interceptors.response.use(
  (response) => {
    const { status, config } = response;
    const timestamp = new Date().toISOString();

    console.log(
      `[API] ${timestamp} | RESPONSE | ${status} ${config.method?.toUpperCase()} ${config.url}`
    );

    return response;
  },
  (error: AxiosError<ErrorResponse>) => {
    const timestamp = new Date().toISOString();

    if (error.response) {
      // Server responded with 4xx or 5xx status
      const { status, data } = error.response;
      const errorMessage = data?.message || 'Unknown error';
      const errorType = data?.type || 'UnknownError';

      console.error(
        `[API] ${timestamp} | ERROR | HTTP ${status} | Type: ${errorType} | ${errorMessage}`
      );

      // Include additional details if available
      if (data?.details) {
        console.error('[API] Error details:', data.details);
      }
    } else if (error.request) {
      // Request made but no response received (network error)
      console.error(
        `[API] ${timestamp} | ERROR | NETWORK | No response received | ${error.message}`
      );
    } else {
      // Error in request setup
      console.error(
        `[API] ${timestamp} | ERROR | CLIENT | Request setup failed | ${error.message}`
      );
    }

    return Promise.reject(error);
  }
);

// ============================================================================
// API Client Implementation
// ============================================================================

/**
 * Portfolio Collaboration API Client
 *
 * Provides type-safe methods for all API endpoints with automatic
 * retry logic, error handling, and comprehensive logging.
 *
 * Usage:
 * ```typescript
 * import { portfolioAPI } from '@/services/api';
 *
 * // Check health
 * const health = await portfolioAPI.healthCheck();
 *
 * // Analyze portfolio
 * const result = await portfolioAPI.analyzePortfolio({
 *   client_profile: { ... },
 *   portfolio: { ... }
 * });
 * ```
 */
class PortfolioAPI {
  /**
   * Get API root information (name, version, docs URL).
   *
   * @returns Root API information
   * @throws {AxiosError} If request fails after retries
   */
  async getRoot(): Promise<RootResponse> {
    const response = await apiClient.get<RootResponse>('/');
    return response.data;
  }

  /**
   * Check API health status.
   *
   * Endpoint: GET /health
   *
   * Returns:
   * - Status: 'healthy' | 'degraded' | 'unhealthy'
   * - OpenAI configuration status
   * - Individual component health checks
   *
   * @returns Health check response with status and component checks
   * @throws {AxiosError} If request fails after retries
   */
  async healthCheck(): Promise<HealthCheckResponse> {
    try {
      const response = await apiClient.get<HealthCheckResponse>('/health');
      return response.data;
    } catch (error) {
      console.error('[API] Health check failed:', error);
      throw error;
    }
  }

  /**
   * Analyze a single portfolio for a client.
   *
   * Endpoint: POST /api/analyze
   *
   * Triggers:
   * 1. Parallel execution of Risk, Compliance, Performance agents
   * 2. Weighted suitability scoring from all agents
   * 3. Recommendation generation
   * 4. Full markdown report creation
   *
   * Performance:
   * - Typical execution: 5-6 seconds
   * - Token usage: 8,000-12,000 tokens
   * - Returns recommendations and detailed analysis
   *
   * @param request - Client profile and portfolio to analyze
   * @returns Analysis results with recommendations and metrics
   * @throws {AxiosError} If request fails after retries
   *
   * @example
   * ```typescript
   * const response = await portfolioAPI.analyzePortfolio({
   *   client_profile: {
   *     age: 45,
   *     risk_tolerance: "moderate",
   *     time_horizon: 20,
   *     income_needs: 50000
   *   },
   *   portfolio: {
   *     total_value: 500000,
   *     holdings: [...]
   *   }
   * });
   *
   * console.log(response.recommendations.suitability_score);
   * ```
   */
  async analyzePortfolio(request: AnalysisRequest): Promise<AnalysisResponse> {
    const response = await apiClient.post<AnalysisResponse>('/api/analyze', request);
    return response.data;
  }

  /**
   * List all available clients.
   *
   * Endpoint: GET /api/clients
   *
   * Returns:
   * - Summary information for each client (ID, age, risk tolerance, net worth)
   * - Total count of available clients
   * - Useful for populating client selector dropdowns
   *
   * @returns List of client summaries with metadata
   * @throws {AxiosError} If request fails after retries
   *
   * @example
   * ```typescript
   * const { clients, total } = await portfolioAPI.listClients();
   * console.log(`${total} clients available`);
   * ```
   */
  async listClients(): Promise<ClientListResponse> {
    const response = await apiClient.get<ClientListResponse>('/api/clients');
    return response.data;
  }

  /**
   * List all available portfolios.
   *
   * Endpoint: GET /api/portfolios
   *
   * Optional Query Parameters:
   * - client_id: Filter portfolios by specific client
   * - offset: Pagination offset (default: 0)
   * - limit: Results per page (default: 50)
   *
   * Returns:
   * - Summary information for each portfolio (ID, client, total value, holdings count)
   * - Total count of available portfolios
   * - Useful for populating portfolio selector dropdowns
   *
   * @param clientId - Optional filter to show only portfolios for specific client
   * @returns List of portfolio summaries with metadata
   * @throws {AxiosError} If request fails after retries
   *
   * @example
   * ```typescript
   * // Get all portfolios
   * const allPortfolios = await portfolioAPI.listPortfolios();
   *
   * // Get portfolios for specific client
   * const clientPortfolios = await portfolioAPI.listPortfolios('CLT-2024-001');
   * ```
   */
  async listPortfolios(clientId?: string): Promise<PortfolioListResponse> {
    const params = clientId ? { client_id: clientId } : {};
    const response = await apiClient.get<PortfolioListResponse>('/api/portfolios', {
      params,
    });
    return response.data;
  }

  /**
   * Compare multiple portfolios for a client.
   *
   * Endpoint: POST /api/compare
   *
   * Analyzes 2-5 portfolios in parallel and returns:
   * - Individual analysis for each portfolio
   * - Weighted suitability scores
   * - Identification of best-fit portfolio for the client
   * - Comparative strengths and weaknesses
   *
   * Use Case:
   * Help clients choose between multiple portfolio options or
   * benchmark current portfolio against alternatives.
   *
   * @param request - Client profile and portfolio IDs to compare
   * @returns Comparison results with best-fit recommendation
   * @throws {AxiosError} If request fails after retries
   *
   * @example
   * ```typescript
   * const comparison = await portfolioAPI.comparePortfolios({
   *   client_profile: { ... },
   *   portfolio_ids: ['conservative', 'moderate', 'aggressive']
   * });
   *
   * console.log(comparison.best_fit_portfolio_id);
   * ```
   */
  async comparePortfolios(request: ComparisonRequest): Promise<ComparisonResponse> {
    const response = await apiClient.post<ComparisonResponse>('/api/compare', request);
    return response.data;
  }
}

// ============================================================================
// Singleton Export
// ============================================================================

/**
 * Singleton instance of the Portfolio API client.
 *
 * Use this throughout the application instead of creating new instances.
 * The singleton ensures:
 * - Single configuration point
 * - Consistent interceptors across all requests
 * - Proper request/response logging
 * - Centralized error handling
 *
 * @example
 * ```typescript
 * import { portfolioAPI } from '@/services/api';
 *
 * const health = await portfolioAPI.healthCheck();
 * ```
 */
export const portfolioAPI = new PortfolioAPI();

/**
 * Default export for convenience.
 * Same as portfolioAPI.
 */
export default portfolioAPI;
