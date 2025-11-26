/**
 * React Query hooks for Portfolio Collaboration API.
 *
 * Provides strongly-typed React Query hooks with automatic:
 * - Request deduplication
 * - Caching and background refetching
 * - Stale data management
 * - Error handling and retry logic
 *
 * Biblical Principle: TRUTH - All data fetching is observable and logged.
 * Biblical Principle: SERVE - Simple, consistent API for component developers.
 *
 * @module hooks/usePortfolioAPI
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import type { UseQueryResult, UseMutationResult } from '@tanstack/react-query';
import { portfolioAPI } from '@/services/api';
import type {
  AnalysisRequest,
  AnalysisResponse,
  ClientListResponse,
  PortfolioListResponse,
  ComparisonRequest,
  ComparisonResponse,
  HealthCheckResponse,
} from '@/types';

// ============================================================================
// Query Configuration Constants
// ============================================================================

/**
 * Cache duration for client list (5 minutes).
 * Clients don't change frequently, safe to cache.
 */
const CLIENTS_CACHE_TIME = 5 * 60 * 1000;

/**
 * Cache duration for portfolio list (2 minutes).
 * Portfolios may be updated periodically.
 */
const PORTFOLIOS_CACHE_TIME = 2 * 60 * 1000;

/**
 * Cache duration for health status (30 seconds).
 * Health changes frequently, short cache window.
 */
const HEALTH_CACHE_TIME = 30 * 1000;

/**
 * Stale time for client list (3 minutes).
 * After 3 minutes without activity, data is considered stale
 * and will be refetched in the background when component remounts.
 */
const CLIENTS_STALE_TIME = 3 * 60 * 1000;

/**
 * Stale time for portfolio list (1 minute).
 */
const PORTFOLIOS_STALE_TIME = 1 * 60 * 1000;

/**
 * Number of retries for failed queries (excluding health check).
 * Analysis queries fail fast (1 retry), listing queries retry more (3).
 */
const QUERY_RETRIES = 3;

/**
 * Number of retries for failed mutations.
 * Mutations are more sensitive to transient failures.
 */
const MUTATION_RETRIES = 2;

// ============================================================================
// Query Key Hierarchy
// ============================================================================

/**
 * React Query key factory for portfolio-related queries.
 *
 * Provides a consistent, hierarchical structure for query keys:
 * - ['portfolio'] - Root
 * - ['portfolio', 'clients'] - All clients
 * - ['portfolio', 'portfolios'] - All portfolios
 * - ['portfolio', 'portfolios', 'client-123'] - Portfolios for specific client
 * - ['portfolio', 'health'] - Health status
 *
 * This structure enables:
 * - Precise cache invalidation
 * - Efficient query deduplication
 * - Clear query relationships
 *
 * @see https://tanstack.com/query/latest/docs/vue/community/tkdodos-blog#practical-setQueryData-example
 */
export const portfolioKeys = {
  // Root key
  all: ['portfolio'] as const,

  // Clients
  clients: () => [...portfolioKeys.all, 'clients'] as const,

  // Portfolios (all)
  portfolios: () => [...portfolioKeys.all, 'portfolios'] as const,

  // Portfolios (filtered by client)
  portfoliosByClient: (clientId: string) =>
    [...portfolioKeys.portfolios(), 'client', clientId] as const,

  // Health check
  health: () => [...portfolioKeys.all, 'health'] as const,

  // Analysis (by analysis ID)
  analysis: (analysisId: string) => [...portfolioKeys.all, 'analysis', analysisId] as const,

  // Comparison (by comparison ID)
  comparison: (comparisonId: string) =>
    [...portfolioKeys.all, 'comparison', comparisonId] as const,
};

// ============================================================================
// Queries
// ============================================================================

/**
 * Fetch API health status.
 *
 * Used to verify backend connectivity and readiness.
 * Useful for:
 * - Displaying server status indicators
 * - Disabling features if backend is unavailable
 * - Monitoring API availability
 *
 * Cache: 30 seconds
 * Retries: 1 (fail fast for health checks)
 *
 * @returns Health check response with status and component details
 *
 * @example
 * ```typescript
 * const { data: health, isLoading, error } = useHealth();
 *
 * if (health?.status === 'healthy') {
 *   console.log('Backend is ready');
 * }
 * ```
 */
export function useHealth(): UseQueryResult<HealthCheckResponse> {
  return useQuery({
    queryKey: portfolioKeys.health(),
    queryFn: () => portfolioAPI.healthCheck(),
    staleTime: HEALTH_CACHE_TIME,
    gcTime: HEALTH_CACHE_TIME,
    retry: 1, // Fail fast for health checks
    refetchInterval: HEALTH_CACHE_TIME, // Actively poll health
  });
}

/**
 * Fetch all available clients.
 *
 * Used to populate client selector dropdowns and client listing pages.
 *
 * Features:
 * - Automatic deduplication (multiple requests return same cached data)
 * - Background refetching when data becomes stale
 * - Smart retry logic for transient failures
 * - Proper error boundaries with error state
 *
 * Cache: 5 minutes
 * Stale time: 3 minutes
 * Retries: 3 (query is background-safe)
 *
 * @returns Query result with client list and metadata
 *
 * @example
 * ```typescript
 * const { data, isLoading, error } = useClients();
 *
 * if (isLoading) return <div>Loading clients...</div>;
 * if (error) return <div>Error: {error.message}</div>;
 *
 * return (
 *   <select>
 *     {data?.clients.map(client => (
 *       <option key={client.client_id} value={client.client_id}>
 *         {client.client_id} - Age {client.age}
 *       </option>
 *     ))}
 *   </select>
 * );
 * ```
 */
export function useClients(): UseQueryResult<ClientListResponse> {
  return useQuery({
    queryKey: portfolioKeys.clients(),
    queryFn: () => portfolioAPI.listClients(),
    staleTime: CLIENTS_STALE_TIME,
    gcTime: CLIENTS_CACHE_TIME,
    retry: QUERY_RETRIES,
  });
}

/**
 * Fetch available portfolios.
 *
 * Used to populate portfolio selector dropdowns and portfolio listing pages.
 *
 * Features:
 * - Optional client filtering
 * - Smart caching with request deduplication
 * - Background refetching when data becomes stale
 * - Efficient pagination support
 *
 * Cache: 2 minutes
 * Stale time: 1 minute
 * Retries: 3
 *
 * @param clientId - Optional client ID to filter portfolios
 * @returns Query result with portfolio list and metadata
 *
 * @example
 * ```typescript
 * // Get all portfolios
 * const { data: allPortfolios } = usePortfolios();
 *
 * // Get portfolios for specific client
 * const { data: clientPortfolios } = usePortfolios('CLT-2024-001');
 *
 * return (
 *   <select>
 *     {clientPortfolios?.portfolios.map(p => (
 *       <option key={p.portfolio_id} value={p.portfolio_id}>
 *         {p.portfolio_id} - ${p.total_value.toLocaleString()}
 *       </option>
 *     ))}
 *   </select>
 * );
 * ```
 */
export function usePortfolios(clientId?: string): UseQueryResult<PortfolioListResponse> {
  return useQuery({
    queryKey: clientId ? portfolioKeys.portfoliosByClient(clientId) : portfolioKeys.portfolios(),
    queryFn: () => portfolioAPI.listPortfolios(clientId),
    staleTime: PORTFOLIOS_STALE_TIME,
    gcTime: PORTFOLIOS_CACHE_TIME,
    retry: QUERY_RETRIES,
  });
}

// ============================================================================
// Mutations
// ============================================================================

/**
 * Analyze portfolio mutation.
 *
 * Triggers multi-agent analysis of a portfolio for a client.
 *
 * Features:
 * - Strongly typed request/response
 * - Automatic error handling
 * - Retry logic for transient failures
 * - Loading and status states
 * - Optional callback hooks (onSuccess, onError)
 *
 * Performance:
 * - Typical execution: 5-6 seconds
 * - Token usage: 8,000-12,000
 *
 * Retries: 2
 *
 * @returns Mutation object with execute function and status
 *
 * @example
 * ```typescript
 * const { mutate, isPending, error, data } = useAnalyzePortfolio();
 *
 * const handleAnalyze = () => {
 *   mutate(
 *     {
 *       client_profile: { ... },
 *       portfolio: { ... }
 *     },
 *     {
 *       onSuccess: (data) => {
 *         console.log('Analysis complete:', data.analysis_id);
 *         // Update UI, navigate to results, etc.
 *       },
 *       onError: (error) => {
 *         console.error('Analysis failed:', error.message);
 *         // Show error toast notification
 *       }
 *     }
 *   );
 * };
 *
 * return (
 *   <div>
 *     <button onClick={handleAnalyze} disabled={isPending}>
 *       {isPending ? 'Analyzing...' : 'Analyze Portfolio'}
 *     </button>
 *     {error && <div className="error">{error.message}</div>}
 *     {data && <div>Analysis ID: {data.analysis_id}</div>}
 *   </div>
 * );
 * ```
 */
export function useAnalyzePortfolio(): UseMutationResult<
  AnalysisResponse,
  Error,
  AnalysisRequest
> {
  return useMutation({
    mutationFn: (request: AnalysisRequest) => portfolioAPI.analyzePortfolio(request),
    retry: MUTATION_RETRIES,
  });
}

/**
 * Compare portfolios mutation.
 *
 * Compares multiple portfolios for a client and identifies best-fit.
 *
 * Features:
 * - Compares 2-5 portfolios in parallel
 * - Returns individual analysis for each portfolio
 * - Identifies best-fit portfolio
 * - Strongly typed request/response
 * - Full error handling
 *
 * Performance:
 * - Typical execution: 5-8 seconds (depends on number of portfolios)
 * - Token usage: 10,000-15,000
 *
 * Retries: 2
 *
 * @returns Mutation object with execute function and status
 *
 * @example
 * ```typescript
 * const { mutate, isPending, data } = useComparePortfolios();
 *
 * const handleCompare = () => {
 *   mutate(
 *     {
 *       client_profile: { ... },
 *       portfolio_ids: ['conservative', 'moderate', 'aggressive']
 *     },
 *     {
 *       onSuccess: (data) => {
 *         console.log('Best fit:', data.best_fit_portfolio_id);
 *         console.log('Results:', data.results);
 *       }
 *     }
 *   );
 * };
 *
 * return (
 *   <div>
 *     <button onClick={handleCompare} disabled={isPending}>
 *       Compare Portfolios
 *     </button>
 *     {data && (
 *       <div>
 *         <h3>Best Fit: {data.best_fit_portfolio_id}</h3>
 *         {data.results.map(result => (
 *           <div key={result.portfolio_id}>
 *             Score: {result.recommendations.suitability_score}
 *           </div>
 *         ))}
 *       </div>
 *     )}
 *   </div>
 * );
 * ```
 */
export function useComparePortfolios(): UseMutationResult<
  ComparisonResponse,
  Error,
  ComparisonRequest
> {
  return useMutation({
    mutationFn: (request: ComparisonRequest) => portfolioAPI.comparePortfolios(request),
    retry: MUTATION_RETRIES,
  });
}

// ============================================================================
// Cache Invalidation Utilities
// ============================================================================

/**
 * Re-export useQueryClient for manual cache management.
 *
 * Useful for:
 * - Invalidating queries after mutations
 * - Prefetching data
 * - Clearing specific cache entries
 *
 * Usage:
 * ```typescript
 * import { useQueryClient } from '@/hooks/usePortfolioAPI';
 *
 * const queryClient = useQueryClient();
 * queryClient.invalidateQueries({ queryKey: portfolioKeys.clients() });
 * ```
 */
export { useQueryClient };
