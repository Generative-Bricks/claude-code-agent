/**
 * Mock data for development and testing
 *
 * This file contains sample data to use during development.
 * Replace with actual API calls or database queries in production.
 *
 * Benefits of mock data:
 * - Faster development (no external dependencies)
 * - Consistent test scenarios
 * - Clear API integration points
 * - Easy to understand data structure
 */

import type { User } from '../types/index.js';

// ============================================================================
// Example Users
// ============================================================================

export const mockUsers: User[] = [
  {
    id: 'user-1',
    name: 'John Doe',
    email: 'john@example.com',
    preferences: {
      theme: 'dark',
      notifications: true,
    },
  },
  {
    id: 'user-2',
    name: 'Jane Smith',
    email: 'jane@example.com',
    preferences: {
      theme: 'light',
      notifications: false,
    },
  },
];

// ============================================================================
// Example Data Items
// ============================================================================

export const mockDataItems = [
  {
    id: 'item-1',
    title: 'First Item',
    description: 'This is the first example item',
    category: 'example',
    createdAt: '2025-01-01T00:00:00Z',
  },
  {
    id: 'item-2',
    title: 'Second Item',
    description: 'This is the second example item',
    category: 'example',
    createdAt: '2025-01-02T00:00:00Z',
  },
  {
    id: 'item-3',
    title: 'Third Item',
    description: 'This is the third example item',
    category: 'sample',
    createdAt: '2025-01-03T00:00:00Z',
  },
];

// ============================================================================
// Helper Functions
// ============================================================================

/**
 * Simulate API delay for realistic testing
 */
export function simulateDelay(ms: number = 100): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Find user by ID (simulates database query)
 */
export async function findUserById(id: string): Promise<User | undefined> {
  await simulateDelay();
  return mockUsers.find(user => user.id === id);
}

/**
 * Find data items by category (simulates database query)
 */
export async function findItemsByCategory(category: string) {
  await simulateDelay();
  return mockDataItems.filter(item => item.category === category);
}

// ============================================================================
// Integration Points
// ============================================================================

/**
 * TODO: Replace with actual API integration
 *
 * When ready for production:
 * 1. Replace mock functions with real API calls
 * 2. Add proper error handling
 * 3. Implement authentication if needed
 * 4. Add retry logic for failed requests
 * 5. Consider caching frequently accessed data
 *
 * Example:
 *
 * export async function findUserById(id: string): Promise<User | undefined> {
 *   const response = await fetch(`${API_BASE_URL}/users/${id}`, {
 *     headers: {
 *       'Authorization': `Bearer ${process.env.API_KEY}`,
 *     },
 *   });
 *
 *   if (!response.ok) {
 *     throw new Error(`Failed to fetch user: ${response.statusText}`);
 *   }
 *
 *   return await response.json();
 * }
 */

export const API_INTEGRATION_NOTES = `
Replace mock data with real API calls in production.

Files to update:
- src/data/mockData.ts - Replace with actual data fetching
- src/tools/*.ts - Update tool implementations to use real APIs
- .env - Add API keys and configuration

Mock data benefits:
- Fast development without external dependencies
- Consistent test scenarios
- Clear data structure examples
- Easy to swap with real implementation
`;
