/**
 * Services barrel export.
 *
 * Central export point for all service modules.
 *
 * Usage:
 * ```typescript
 * // Import API client
 * import { portfolioAPI } from '@/services';
 *
 * // Import WebSocket client
 * import { wsClient } from '@/services';
 *
 * // Or use default export
 * import api from '@/services';
 * ```
 */

export { portfolioAPI, default as api } from './api';
export { wsClient, WebSocketClient } from './websocket';
