/**
 * Example Usage Patterns for Portfolio API Client
 *
 * This file demonstrates best practices for using the Portfolio API
 * and React Query hooks in components.
 *
 * Do NOT use this as production code - it's for reference only.
 * Copy patterns into your own components.
 */

import { useState } from 'react';
import {
  useClients,
  usePortfolios,
  useAnalyzePortfolio,
  useComparePortfolios,
  portfolioKeys,
  useQueryClient,
  useHealth,
} from '@/hooks/usePortfolioAPI';
import type { ClientProfile, Portfolio, AnalysisRequest, ComparisonRequest } from '@/types';

// ============================================================================
// Example 1: Simple Client Selector
// ============================================================================

/**
 * Example: Display loading/error states and client list.
 *
 * Demonstrates:
 * - useClients hook with loading/error handling
 * - Proper TypeScript typing
 * - Conditional rendering patterns
 */
export function ClientSelectorExample() {
  const { data, isLoading, error } = useClients();

  if (isLoading) {
    return <div>Loading clients...</div>;
  }

  if (error) {
    return <div className="error">Failed to load clients: {error.message}</div>;
  }

  return (
    <select>
      <option value="">Select a client...</option>
      {data?.clients.map((client) => (
        <option key={client.client_id} value={client.client_id}>
          {client.client_id} - Age {client.age}, Risk: {client.risk_tolerance}
        </option>
      ))}
    </select>
  );
}

// ============================================================================
// Example 2: Portfolio Selector with Client Filter
// ============================================================================

/**
 * Example: Filter portfolios by selected client.
 *
 * Demonstrates:
 * - Conditional query execution (only fetch if clientId provided)
 * - Dynamic query keys for filtered results
 * - Disabling queries when filters are empty
 */
export function PortfolioSelectorExample({ clientId }: { clientId?: string }) {
  const { data, isLoading, error } = usePortfolios(clientId);

  if (!clientId) {
    return <select disabled><option>Select a client first...</option></select>;
  }

  if (isLoading) {
    return <select disabled><option>Loading portfolios...</option></select>;
  }

  if (error) {
    return <select disabled><option>Error loading portfolios</option></select>;
  }

  return (
    <select>
      <option value="">Select a portfolio...</option>
      {data?.portfolios.map((portfolio) => (
        <option key={portfolio.portfolio_id} value={portfolio.portfolio_id}>
          {portfolio.portfolio_id} - ${portfolio.total_value.toLocaleString()} ({portfolio.holdings_count} holdings)
        </option>
      ))}
    </select>
  );
}

// ============================================================================
// Example 3: Analysis Submission with Loading States
// ============================================================================

/**
 * Example: Trigger portfolio analysis with proper loading/error handling.
 *
 * Demonstrates:
 * - useMutation for POST requests
 * - Handling mutation pending/loading states
 * - Error handling and user feedback
 * - Success callback to navigate or update UI
 * - Proper TypeScript typing for request/response
 */
export function AnalysisFormExample() {
  const [selectedClient, _setSelectedClient] = useState<ClientProfile | null>(null);
  const [selectedPortfolio, _setSelectedPortfolio] = useState<Portfolio | null>(null);

  const { mutate: analyzePortfolio, isPending, error, data } = useAnalyzePortfolio();

  const handleSubmit = () => {
    if (!selectedClient || !selectedPortfolio) {
      alert('Please select both client and portfolio');
      return;
    }

    const request: AnalysisRequest = {
      client_profile: selectedClient,
      portfolio: selectedPortfolio,
    };

    // Call mutation with success/error handlers
    analyzePortfolio(request, {
      onSuccess: (result) => {
        console.log('Analysis complete:', result.analysis_id);
        console.log('Suitability score:', result.recommendations.suitability_score);
        // Navigate to results page, show success toast, etc.
      },
      onError: (error) => {
        console.error('Analysis failed:', error.message);
        // Show error toast notification
      },
    });
  };

  return (
    <div className="analysis-form">
      <h2>Portfolio Analysis</h2>

      {/* Loading state */}
      {isPending && <div className="spinner">Analyzing portfolio...</div>}

      {/* Error state */}
      {error && (
        <div className="error">
          <h3>Analysis Failed</h3>
          <p>{error.message}</p>
        </div>
      )}

      {/* Success state */}
      {data && (
        <div className="success">
          <h3>Analysis Complete!</h3>
          <p>Analysis ID: {data.analysis_id}</p>
          <p>Suitability Score: {data.recommendations.suitability_score.overall_score}/100</p>
          <p>Interpretation: {data.recommendations.suitability_score.interpretation}</p>
          <p>Execution Time: {data.execution_time_seconds.toFixed(2)}s</p>
        </div>
      )}

      {/* Form (disabled during submission) */}
      {!isPending && !data && (
        <>
          <button onClick={handleSubmit} disabled={!selectedClient || !selectedPortfolio}>
            Analyze Portfolio
          </button>
        </>
      )}
    </div>
  );
}

// ============================================================================
// Example 4: Portfolio Comparison
// ============================================================================

/**
 * Example: Compare multiple portfolios side-by-side.
 *
 * Demonstrates:
 * - useComparePortfolios mutation
 * - Handling multiple results in response
 * - Displaying comparison results
 * - Best-fit recommendation highlighting
 */
export function PortfolioComparisonExample() {
  const [clientProfile, _setClientProfile] = useState<ClientProfile | null>(null);
  const [selectedPortfolioIds, _setSelectedPortfolioIds] = useState<string[]>([]);

  const { mutate: comparePortfolios, isPending, data } = useComparePortfolios();

  const handleCompare = () => {
    if (!clientProfile || selectedPortfolioIds.length < 2) {
      alert('Select at least 2 portfolios to compare');
      return;
    }

    const request: ComparisonRequest = {
      client_profile: clientProfile,
      portfolio_ids: selectedPortfolioIds,
    };

    comparePortfolios(request);
  };

  return (
    <div className="comparison-container">
      <h2>Compare Portfolios</h2>

      {isPending && <div>Comparing {selectedPortfolioIds.length} portfolios...</div>}

      {data && (
        <div className="results">
          <h3>Comparison Results</h3>

          <div className="best-fit">
            <h4>Best Fit: {data.best_fit_portfolio_id}</h4>
          </div>

          <table>
            <thead>
              <tr>
                <th>Portfolio ID</th>
                <th>Suitability Score</th>
                <th>Interpretation</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {data.results.map((result) => (
                <tr
                  key={result.portfolio_id}
                  className={result.portfolio_id === data.best_fit_portfolio_id ? 'best-fit' : ''}
                >
                  <td>{result.portfolio_id}</td>
                  <td>{result.recommendations.suitability_score.overall_score}/100</td>
                  <td>{result.recommendations.suitability_score.interpretation}</td>
                  <td>
                    {result.portfolio_id === data.best_fit_portfolio_id ? (
                      <strong>RECOMMENDED</strong>
                    ) : (
                      'Alternative'
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <button onClick={handleCompare} disabled={selectedPortfolioIds.length < 2 || isPending}>
        Compare Selected Portfolios
      </button>
    </div>
  );
}

// ============================================================================
// Example 5: Manual Cache Invalidation
// ============================================================================

/**
 * Example: Manually invalidate cache after mutations.
 *
 * Demonstrates:
 * - useQueryClient hook for cache management
 * - Invalidating specific query keys
 * - Triggering background refetch
 * - Useful after mutations that affect listing data
 */
export function RefreshDataExample() {
  const queryClient = useQueryClient();

  const handleRefreshClients = () => {
    // Invalidate all client queries
    // This will cause useClients() hooks to show loading state
    // and refetch in the background
    queryClient.invalidateQueries({ queryKey: portfolioKeys.clients() });
  };

  const handleRefreshAllData = () => {
    // Invalidate multiple query types at once
    queryClient.invalidateQueries({ queryKey: portfolioKeys.all });
  };

  const handlePrefetchClients = async () => {
    // Prefetch data before user needs it
    // Useful for navigation, showing spinners, etc.
    await queryClient.prefetchQuery({
      queryKey: portfolioKeys.clients(),
      queryFn: async () => {
        // Data will be fetched and cached
        return Promise.resolve({ clients: [], total: 0 });
      },
    });
  };

  return (
    <div className="cache-controls">
      <button onClick={handleRefreshClients}>Refresh Clients</button>
      <button onClick={handleRefreshAllData}>Refresh All Data</button>
      <button onClick={handlePrefetchClients}>Prefetch Clients</button>
    </div>
  );
}

// ============================================================================
// Example 6: Health Check / API Status
// ============================================================================

/**
 * Example: Display API health status.
 *
 * Demonstrates:
 * - useHealth hook for monitoring API status
 * - Displaying component health checks
 * - Disabling features when backend is unavailable
 */
export function APIStatusIndicatorExample() {
  const { data: health, isLoading } = useHealth();

  if (isLoading) {
    return <div className="status">Checking API status...</div>;
  }

  const statusColor = health?.status === 'healthy' ? 'green' : 'yellow';
  const statusLabel =
    health?.status === 'healthy'
      ? 'API Ready'
      : health?.status === 'degraded'
        ? 'API Degraded'
        : 'API Down';

  return (
    <div className={`status status-${statusColor}`}>
      <span>{statusLabel}</span>
      {health?.checks && (
        <details>
          <summary>Component Status</summary>
          <ul>
            {Object.entries(health.checks).map(([name, status]) => (
              <li key={name}>
                {name}: <span className={status ? 'ok' : 'error'}>{status ? '✓' : '✗'}</span>
              </li>
            ))}
          </ul>
        </details>
      )}
    </div>
  );
}

// ============================================================================
// Example 7: Error Recovery Pattern
// ============================================================================

/**
 * Example: Implement retry logic for failed requests.
 *
 * Demonstrates:
 * - Catching and handling errors
 * - Implementing manual retry logic
 * - Exponential backoff
 * - Giving users control over retries
 */
export function ErrorRecoveryExample() {
  const [retryCount, setRetryCount] = useState(0);
  const MAX_RETRIES = 3;

  const { mutate: _analyzePortfolio, error, isPending } = useAnalyzePortfolio();

  const handleRetry = () => {
    if (retryCount < MAX_RETRIES) {
      setRetryCount((prev) => prev + 1);
      // Re-trigger the analysis mutation
      // analyzePortfolio(previousRequest);
    }
  };

  return (
    <div className="error-recovery">
      {error && (
        <div className="error-message">
          <h3>Analysis Failed</h3>
          <p>{error.message}</p>

          {retryCount < MAX_RETRIES && (
            <button onClick={handleRetry} disabled={isPending}>
              Retry ({retryCount + 1}/{MAX_RETRIES})
            </button>
          )}

          {retryCount >= MAX_RETRIES && <p>Maximum retries exceeded. Please try again later.</p>}
        </div>
      )}
    </div>
  );
}

// ============================================================================
// Example 8: Combining Multiple Queries
// ============================================================================

/**
 * Example: Coordinate multiple queries for complex workflows.
 *
 * Demonstrates:
 * - Using multiple hooks together
 * - Combining loading/error states
 * - Sequential data dependencies
 * - Coordinated user flows
 */
export function ComplexWorkflowExample() {
  const [selectedClientId, setSelectedClientId] = useState<string | null>(null);

  // First query: Get all clients
  const {
    data: clientsData,
    isLoading: clientsLoading,
    error: clientsError,
  } = useClients();

  // Second query: Get portfolios for selected client (only if client selected)
  const {
    data: portfoliosData,
    isLoading: portfoliosLoading,
    error: portfoliosError,
  } = usePortfolios(selectedClientId || undefined);

  // Overall loading state
  const isLoading = clientsLoading || (selectedClientId ? portfoliosLoading : false);
  const error = clientsError || (selectedClientId ? portfoliosError : null);

  return (
    <div className="workflow">
      <h2>Portfolio Analysis Workflow</h2>

      {isLoading && <div>Loading...</div>}
      {error && <div className="error">{error.message}</div>}

      {!isLoading && !error && (
        <>
          <section>
            <h3>Step 1: Select Client</h3>
            <select
              value={selectedClientId || ''}
              onChange={(e) => setSelectedClientId(e.target.value || null)}
            >
              <option value="">Choose a client...</option>
              {clientsData?.clients.map((client) => (
                <option key={client.client_id} value={client.client_id}>
                  {client.client_id}
                </option>
              ))}
            </select>
          </section>

          {selectedClientId && (
            <section>
              <h3>Step 2: Select Portfolio</h3>
              <select>
                <option>Choose a portfolio...</option>
                {portfoliosData?.portfolios.map((portfolio) => (
                  <option key={portfolio.portfolio_id} value={portfolio.portfolio_id}>
                    {portfolio.portfolio_id}
                  </option>
                ))}
              </select>
            </section>
          )}

          {selectedClientId && (
            <section>
              <h3>Step 3: Analyze</h3>
              <button>Run Analysis</button>
            </section>
          )}
        </>
      )}
    </div>
  );
}
