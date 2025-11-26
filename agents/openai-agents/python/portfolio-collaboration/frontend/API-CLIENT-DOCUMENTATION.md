# REST API Client Documentation

## Overview

This document covers the comprehensive REST API client for the Portfolio Collaboration System frontend. The client provides type-safe, production-grade API communication with the FastAPI backend using Axios and React Query.

**Location:** `/frontend/src/services/api.ts` and `/frontend/src/hooks/usePortfolioAPI.ts`

**Status:** Production-Ready

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Architecture](#architecture)
3. [API Client (`api.ts`)](#api-client-apits)
4. [React Query Hooks (`usePortfolioAPI.ts`)](#react-query-hooks-useportfolioapits)
5. [Usage Examples](#usage-examples)
6. [Error Handling](#error-handling)
7. [Caching Strategy](#caching-strategy)
8. [Configuration](#configuration)

---

## Quick Start

### Basic Usage

```typescript
// Import the API client
import { portfolioAPI } from '@/services/api';

// Or import React Query hooks
import { useClients, useAnalyzePortfolio } from '@/hooks/usePortfolioAPI';

// Make a direct API call
const health = await portfolioAPI.healthCheck();

// Or use React Query for automatic caching/refetching
const { data, isLoading, error } = useClients();
```

### Installation

No additional installation needed - dependencies are already in `package.json`:

```json
{
  "axios": "^1.13.2",
  "@tanstack/react-query": "^5.90.9"
}
```

---

## Architecture

### Three-Layer Design

```
┌─────────────────────────────────────────┐
│        React Components                 │
│   (Call React Query hooks)              │
└────────────────┬────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────┐
│   React Query Hooks (usePortfolioAPI)  │
│   - Query keys hierarchy                │
│   - Cache management                    │
│   - Auto-refetch logic                  │
└────────────────┬────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────┐
│    Axios API Client (portfolioAPI)     │
│    - Request/response interceptors      │
│    - Error handling                     │
│    - Logging & debugging                │
└────────────────┬────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────┐
│    FastAPI Backend (Python)             │
│    http://localhost:8000                │
└─────────────────────────────────────────┘
```

### Design Principles

**TRUTH** (John 14:6)
- All API interactions logged transparently
- Request/response lifecycle visible in console
- Error details exposed to developers

**SERVE** (John 13:14)
- Simple, intuitive hooks for components
- Automatic error handling and retries
- Sensible defaults that work out-of-box

**PERSEVERE** (Hebrews 12:1-3)
- Graceful error recovery
- Retry logic for transient failures
- Exponential backoff strategy

---

## API Client (`api.ts`)

### Overview

The `PortfolioAPI` class provides type-safe methods for all backend endpoints.

**Location:** `/frontend/src/services/api.ts`

**Singleton Instance:** `portfolioAPI`

### Endpoints

#### 1. Health Check

```typescript
const health = await portfolioAPI.healthCheck();

// Response:
{
  status: 'healthy' | 'degraded' | 'unhealthy',
  api_version: '1.0.0',
  openai_configured: true,
  timestamp: '2025-01-19T10:30:45.123Z',
  checks?: {
    openai: true,
    database: true,
    mcp_server: false
  }
}
```

**Use Case:** Check if backend is ready before rendering UI

```typescript
const { data: health } = useHealth();

if (health?.status !== 'healthy') {
  return <div>Backend is temporarily unavailable</div>;
}
```

#### 2. Analyze Portfolio

```typescript
const result = await portfolioAPI.analyzePortfolio({
  client_profile: { ... },
  portfolio: { ... }
});

// Response:
{
  success: true,
  recommendations: {
    suitability_score: { ... },
    risk_analysis: { ... },
    compliance_report: { ... },
    performance_report: { ... },
    recommendations: [...]
  },
  analysis_id: 'anal-2025-01-19-001',
  timestamp: '2025-01-19T10:30:45.123Z',
  execution_time_seconds: 5.2
}
```

**Performance:** 5-6 seconds typical

**Tokens Used:** 8,000-12,000 per analysis

**Use Case:** Analyze a portfolio for a client

```typescript
const { mutate: analyzePortfolio, isPending, data, error } = useAnalyzePortfolio();

analyzePortfolio(
  {
    client_profile: selectedClient,
    portfolio: selectedPortfolio
  },
  {
    onSuccess: (result) => {
      console.log('Score:', result.recommendations.suitability_score.overall_score);
    }
  }
);
```

#### 3. List Clients

```typescript
const response = await portfolioAPI.listClients();

// Response:
{
  clients: [
    {
      client_id: 'CLT-2024-001',
      age: 45,
      risk_tolerance: 'moderate',
      net_worth: 500000,
      time_horizon: 20
    },
    ...
  ],
  total: 3
}
```

**Use Case:** Populate client dropdown selector

```typescript
const { data: clientsResponse, isLoading } = useClients();

{isLoading ? (
  <span>Loading clients...</span>
) : (
  <select>
    {clientsResponse?.clients.map(client => (
      <option key={client.client_id} value={client.client_id}>
        {client.client_id} - Age {client.age}
      </option>
    ))}
  </select>
)}
```

#### 4. List Portfolios

```typescript
const response = await portfolioAPI.listPortfolios('CLT-2024-001');

// Response:
{
  portfolios: [
    {
      portfolio_id: 'conservative',
      client_id: 'CLT-2024-001',
      total_value: 500000,
      holdings_count: 12,
      benchmark: 'SPY'
    },
    ...
  ],
  total: 3
}
```

**Parameters:**
- `clientId` (optional): Filter by client

**Use Case:** Show portfolios for selected client

```typescript
const { data: portfolios } = usePortfolios(selectedClientId);
```

#### 5. Compare Portfolios

```typescript
const result = await portfolioAPI.comparePortfolios({
  client_profile: { ... },
  portfolio_ids: ['conservative', 'moderate', 'aggressive']
});

// Response:
{
  success: true,
  results: [
    {
      portfolio_id: 'conservative',
      recommendations: { ... }
    },
    {
      portfolio_id: 'moderate',
      recommendations: { ... }
    }
  ],
  best_fit_portfolio_id: 'moderate',
  timestamp: '2025-01-19T10:30:45.123Z'
}
```

**Use Case:** Help clients compare portfolio options

```typescript
const { mutate: comparePortfolios, data: comparison } = useComparePortfolios();

comparePortfolios({
  client_profile: selectedClient,
  portfolio_ids: selectedPortfolioIds
});

// Display results with best-fit highlighted
comparison?.results.forEach(result => {
  console.log(
    result.portfolio_id,
    result.recommendations.suitability_score.overall_score
  );
});
```

### Interceptors

The API client includes automatic request/response logging:

**Request Logging:**
```
[API] 2025-01-19T10:30:45.123Z | REQUEST | POST /api/analyze | Payload size: 2048B
```

**Response Logging:**
```
[API] 2025-01-19T10:30:50.456Z | RESPONSE | 200 POST /api/analyze
```

**Error Logging:**
```
[API] 2025-01-19T10:30:50.456Z | ERROR | HTTP 500 | Type: InternalServerError | Server error occurred
[API] Error details: { "validation_error": "..." }
```

---

## React Query Hooks (`usePortfolioAPI.ts`)

### Overview

React Query hooks wrap the API client with automatic caching, background refetching, and state management.

**Location:** `/frontend/src/hooks/usePortfolioAPI.ts`

### Query Keys

Hierarchical query keys enable precise cache invalidation:

```typescript
// Root
portfolioKeys.all
// ['portfolio']

// Clients
portfolioKeys.clients()
// ['portfolio', 'clients']

// Portfolios (all)
portfolioKeys.portfolios()
// ['portfolio', 'portfolios']

// Portfolios (filtered by client)
portfolioKeys.portfoliosByClient('CLT-2024-001')
// ['portfolio', 'portfolios', 'client', 'CLT-2024-001']

// Health check
portfolioKeys.health()
// ['portfolio', 'health']
```

### Hook: `useHealth()`

Check API health status with auto-polling.

```typescript
const { data: health, isLoading, error } = useHealth();

// Cache: 30 seconds
// Stale time: 30 seconds
// Auto-refetch: Every 30 seconds
// Retries: 1 (fail fast for health checks)
```

**Use Cases:**
- Display server status indicator
- Disable features if backend unavailable
- Monitor API availability

### Hook: `useClients()`

Fetch all available clients.

```typescript
const { data: response, isLoading, error } = useClients();

// Cache: 5 minutes
// Stale time: 3 minutes
// Retries: 3

const clients = response?.clients || [];
const totalClients = response?.total || 0;
```

**Features:**
- Automatic request deduplication
- Background refetching when stale
- Smart retry logic

### Hook: `usePortfolios(clientId?)`

Fetch portfolios with optional client filter.

```typescript
// Get all portfolios
const { data } = usePortfolios();

// Get portfolios for specific client
const { data } = usePortfolios('CLT-2024-001');

// Conditional query execution
const { data: portfolios, isLoading } = usePortfolios(
  selectedClientId ? selectedClientId : undefined
);
```

**Properties:**
- Cache: 2 minutes
- Stale time: 1 minute
- Retries: 3

### Mutation: `useAnalyzePortfolio()`

Submit portfolio for analysis.

```typescript
const {
  mutate: analyzePortfolio,
  mutateAsync: analyzePortfolioAsync,
  isPending,
  error,
  data,
  status
} = useAnalyzePortfolio();

// Simple usage
analyzePortfolio({
  client_profile: client,
  portfolio: portfolio
});

// With callbacks
analyzePortfolio(request, {
  onSuccess: (result) => {
    console.log('Analysis complete');
  },
  onError: (error) => {
    console.error('Analysis failed:', error.message);
  },
  onSettled: () => {
    // Always called (success or error)
  }
});

// Async usage
try {
  const result = await analyzePortfolioAsync(request);
} catch (error) {
  console.error(error);
}
```

**States:**
- `isPending`: Loading state
- `error`: Error object (null if success)
- `data`: Result (null until success)
- `status`: 'idle' | 'pending' | 'success' | 'error'

### Mutation: `useComparePortfolios()`

Compare multiple portfolios.

```typescript
const { mutate: comparePortfolios, data: comparison } = useComparePortfolios();

comparePortfolios({
  client_profile: selectedClient,
  portfolio_ids: ['conservative', 'moderate', 'aggressive']
});

// Access best-fit recommendation
if (comparison) {
  console.log('Best fit:', comparison.best_fit_portfolio_id);
}
```

### Manual Cache Management

```typescript
import { useQueryClient } from '@/hooks/usePortfolioAPI';

const queryClient = useQueryClient();

// Invalidate specific query
queryClient.invalidateQueries({
  queryKey: portfolioKeys.clients()
});

// Invalidate all portfolio queries
queryClient.invalidateQueries({
  queryKey: portfolioKeys.all
});

// Prefetch data
await queryClient.prefetchQuery({
  queryKey: portfolioKeys.clients(),
  queryFn: () => portfolioAPI.listClients()
});

// Get cached data
const cachedClients = queryClient.getQueryData(portfolioKeys.clients());

// Clear cache
queryClient.removeQueries({
  queryKey: portfolioKeys.clients()
});
```

---

## Usage Examples

### Example 1: Client Selector

```typescript
import { useClients } from '@/hooks/usePortfolioAPI';

export function ClientSelector() {
  const { data, isLoading, error } = useClients();

  if (isLoading) return <div>Loading clients...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <select>
      <option value="">Select a client...</option>
      {data?.clients.map(client => (
        <option key={client.client_id} value={client.client_id}>
          {client.client_id} - Age {client.age}
        </option>
      ))}
    </select>
  );
}
```

### Example 2: Portfolio Analysis

```typescript
import { useAnalyzePortfolio } from '@/hooks/usePortfolioAPI';

export function AnalysisForm() {
  const { mutate, isPending, data, error } = useAnalyzePortfolio();

  const handleAnalyze = () => {
    mutate({
      client_profile: selectedClient,
      portfolio: selectedPortfolio
    });
  };

  return (
    <div>
      <button onClick={handleAnalyze} disabled={isPending}>
        {isPending ? 'Analyzing...' : 'Analyze Portfolio'}
      </button>

      {error && <div className="error">{error.message}</div>}

      {data && (
        <div className="results">
          <h3>Analysis Results</h3>
          <p>Score: {data.recommendations.suitability_score.overall_score}/100</p>
          <p>Time: {data.execution_time_seconds.toFixed(2)}s</p>
        </div>
      )}
    </div>
  );
}
```

### Example 3: Coordinated Queries

```typescript
import { useClients, usePortfolios } from '@/hooks/usePortfolioAPI';

export function ClientPortfolioForm() {
  const [selectedClientId, setSelectedClientId] = useState<string | null>(null);

  const { data: clients, isLoading: clientsLoading } = useClients();
  const { data: portfolios, isLoading: portfoliosLoading } = usePortfolios(
    selectedClientId || undefined
  );

  const isLoading = clientsLoading || (selectedClientId ? portfoliosLoading : false);

  return (
    <>
      <select
        value={selectedClientId || ''}
        onChange={(e) => setSelectedClientId(e.target.value || null)}
      >
        <option>Select client...</option>
        {clients?.clients.map(c => (
          <option key={c.client_id} value={c.client_id}>
            {c.client_id}
          </option>
        ))}
      </select>

      {selectedClientId && (
        <select disabled={portfoliosLoading}>
          <option>
            {portfoliosLoading ? 'Loading portfolios...' : 'Select portfolio...'}
          </option>
          {portfolios?.portfolios.map(p => (
            <option key={p.portfolio_id} value={p.portfolio_id}>
              {p.portfolio_id}
            </option>
          ))}
        </select>
      )}
    </>
  );
}
```

### Example 4: Manual Retry Logic

```typescript
import { useAnalyzePortfolio, useQueryClient } from '@/hooks/usePortfolioAPI';

export function AnalysisWithRetry() {
  const [retryCount, setRetryCount] = useState(0);
  const queryClient = useQueryClient();

  const { mutate, error, isPending } = useAnalyzePortfolio();

  const handleRetry = () => {
    if (retryCount < 3) {
      setRetryCount(prev => prev + 1);
      mutate(previousRequest);
    }
  };

  return (
    <div>
      {error && (
        <>
          <p>Analysis failed: {error.message}</p>
          <button onClick={handleRetry} disabled={retryCount >= 3 || isPending}>
            Retry ({retryCount}/3)
          </button>
        </>
      )}
    </div>
  );
}
```

See `/frontend/src/examples/useAPIClientExample.tsx` for comprehensive usage patterns.

---

## Error Handling

### Error Response Format

```typescript
interface ErrorResponse {
  error: string;        // 'ValidationError', 'ServerError', etc.
  message: string;      // Human-readable message
  type: string;         // Exception type
  timestamp: string;    // ISO format
  details?: Record<string, any>;  // Additional details
}
```

### Error Types

**Network Errors:**
```typescript
// No response from server
error.message = 'Network Error'
error.code = 'ECONNREFUSED' | 'ECONNABORTED' | 'ETIMEDOUT'
```

**Client Errors (4xx):**
```typescript
// Invalid request
error.response.status = 400
error.response.data.message = 'Invalid client profile'
```

**Server Errors (5xx):**
```typescript
// Server failure
error.response.status = 500
error.response.data.message = 'Internal server error'
```

### Error Handling Pattern

```typescript
const { mutate, error } = useAnalyzePortfolio();

// Handle errors in callback
mutate(request, {
  onError: (error) => {
    if (error.response?.status === 400) {
      // Validation error - show to user
      toast.error('Invalid client profile');
    } else if (error.response?.status >= 500) {
      // Server error - retry
      toast.error('Server error, please try again');
      setTimeout(() => mutate(request), 2000);
    } else if (!error.response) {
      // Network error
      toast.error('Connection failed, please check internet');
    }
  }
});
```

### Retry Strategy

**Query Retries:** 3 attempts with exponential backoff
**Mutation Retries:** 2 attempts
**Health Check Retries:** 1 attempt (fail fast)

---

## Caching Strategy

### Cache Durations

| Query | Cache | Stale Time | Retries |
|-------|-------|-----------|---------|
| Health Check | 30s | 30s | 1 |
| Clients | 5m | 3m | 3 |
| Portfolios | 2m | 1m | 3 |

### Cache Behavior

**After Data Becomes Stale:**
1. Component shows old data (gray out or muted)
2. Background refetch triggered
3. New data received → UI updates automatically

**Cache Invalidation:**
```typescript
// After mutation succeeds
queryClient.invalidateQueries({
  queryKey: portfolioKeys.clients()
});
```

### Disabling Cache

```typescript
// For a specific query
const { data } = useQuery({
  queryKey: ['key'],
  queryFn: fn,
  staleTime: 0,      // Always stale
  gcTime: 0          // Don't cache
});

// For all queries
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 0,
      gcTime: 0
    }
  }
});
```

---

## Configuration

### Environment Variables

Create `.env.local`:

```env
# API endpoint
VITE_API_BASE_URL=http://localhost:8000

# WebSocket endpoint (for real-time features)
VITE_WS_URL=http://localhost:8000
```

### Defaults

```typescript
// API base URL
http://localhost:8000

// Request timeout
30 seconds

// Cache sizes
See Caching Strategy section above
```

### Axios Configuration

```typescript
// In src/services/api.ts

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
});
```

### React Query Configuration

```typescript
// In your root component (e.g., App.tsx)

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60,          // 1 minute
      gcTime: 1000 * 60 * 5,         // 5 minutes
      retry: 3,                       // 3 retries
      refetchOnWindowFocus: true      // Refetch when window regains focus
    },
    mutations: {
      retry: 2                        // 2 retries for mutations
    }
  }
});

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      {/* Your app */}
    </QueryClientProvider>
  );
}
```

---

## Testing

### Unit Testing

```typescript
import { describe, it, expect, vi } from 'vitest';
import { portfolioAPI } from '@/services/api';

describe('portfolioAPI', () => {
  it('should fetch clients', async () => {
    const result = await portfolioAPI.listClients();
    expect(result).toHaveProperty('clients');
    expect(result).toHaveProperty('total');
  });

  it('should handle errors', async () => {
    vi.mock('axios');
    await expect(portfolioAPI.listClients()).rejects.toThrow();
  });
});
```

### Hook Testing

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClientProvider, QueryClient } from '@tanstack/react-query';
import { useClients } from '@/hooks/usePortfolioAPI';

const queryClient = new QueryClient();

describe('useClients', () => {
  it('should fetch clients', async () => {
    const { result } = renderHook(() => useClients(), {
      wrapper: ({ children }) => (
        <QueryClientProvider client={queryClient}>
          {children}
        </QueryClientProvider>
      )
    });

    await waitFor(() => {
      expect(result.current.data).toBeDefined();
    });
  });
});
```

---

## Troubleshooting

### Issue: "Cannot find module '@/types'"

**Solution:** Ensure vite.config.ts has path alias:
```typescript
resolve: {
  alias: {
    '@': path.resolve(__dirname, './src'),
  }
}
```

### Issue: API calls not going through

**Solution:** Check vite.config.ts proxy configuration:
```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

### Issue: Stale cache not refetching

**Solution:** Check staleTime vs gcTime:
```typescript
// Wrong: data never becomes stale
const { data } = useQuery({
  staleTime: 1000 * 60 * 60  // 1 hour
});

// Correct: becomes stale after 3 minutes
const { data } = useClients();  // staleTime: 3 minutes
```

### Issue: "Timeout of 30000ms exceeded"

**Solution:** Backend is slow or unresponsive. Check:
1. Backend is running: `curl http://localhost:8000/health`
2. Network connectivity
3. Increase timeout in `src/services/api.ts`

---

## Performance Tips

### 1. Avoid Refetching on Mount

```typescript
// Bad: Refetches every time component mounts
const { data } = useClients();

// Good: Uses cached data if less than 3 minutes old
const { data } = useClients();  // staleTime configured
```

### 2. Batch Requests

```typescript
// Bad: Multiple independent requests
const clients = await portfolioAPI.listClients();
const portfolios = await portfolioAPI.listPortfolios();

// Good: Parallel requests
const [clients, portfolios] = await Promise.all([
  portfolioAPI.listClients(),
  portfolioAPI.listPortfolios()
]);
```

### 3. Prefetch Critical Data

```typescript
const queryClient = useQueryClient();

// Prefetch before navigation
const handleNavigateToAnalysis = async () => {
  await queryClient.prefetchQuery({
    queryKey: portfolioKeys.clients(),
    queryFn: () => portfolioAPI.listClients()
  });
  navigate('/analysis');
};
```

---

## Biblical Principles in Implementation

### TRUTH (John 14:6)
All API interactions are logged transparently so developers can see exactly what's happening.

### SERVE (John 13:14)
Simple hooks with sensible defaults make it easy for component developers to integrate API calls.

### PERSEVERE (Hebrews 12:1-3)
Graceful error recovery with retry logic ensures the app handles failures gracefully.

### EXCELLENCE (Colossians 3:23)
Production-grade from inception with full type safety, error handling, and testing.

---

**Last Updated:** January 2025

**Files:**
- `/frontend/src/services/api.ts` - API client (354 lines)
- `/frontend/src/services/index.ts` - Barrel export
- `/frontend/src/hooks/usePortfolioAPI.ts` - React Query hooks (410 lines)
- `/frontend/src/examples/useAPIClientExample.tsx` - Usage examples (480+ lines)
