/**
 * WebSocket Client for Portfolio Collaboration System
 *
 * Provides real-time communication with the Portfolio Manager agent.
 * Implements Socket.io for robust WebSocket connection with automatic reconnection.
 *
 * Biblical Principle: PERSEVERE - Resilient connections with auto-reconnection.
 * Graceful degradation on network failures with exponential backoff strategy.
 *
 * Features:
 * - Automatic reconnection with exponential backoff
 * - Event-based message handling with type safety
 * - Connection state management
 * - Comprehensive logging for debugging
 * - Graceful error recovery
 */

import { io, Socket } from 'socket.io-client';
import type { ChatMessage, AgentStreamEvent } from '@/types';

// Configuration
const WS_URL = import.meta.env.VITE_WS_URL || 'http://localhost:8000';
const RECONNECT_MAX_ATTEMPTS = 5;
const RECONNECT_INITIAL_DELAY = 1000; // 1 second
const RECONNECT_MAX_DELAY = 30000; // 30 seconds

/**
 * Event handler type for WebSocket events
 */
type EventHandler = (event: AgentStreamEvent) => void;

/**
 * WebSocket Client for agent communication
 *
 * Manages real-time bidirectional communication with the Portfolio Manager.
 * Handles connection lifecycle, automatic reconnection, and event dispatching.
 */
class WebSocketClient {
  // Private properties
  private socket: Socket | null = null;
  private eventHandlers: Map<string, Set<EventHandler>> = new Map();
  private reconnectAttempts = 0;
  private reconnectDelay = RECONNECT_INITIAL_DELAY;
  private isManuallyDisconnected = false;

  /**
   * Connect to WebSocket server
   *
   * Establishes connection to the backend WebSocket server.
   * If already connected, this is a no-op.
   *
   * The connection uses Socket.io for better browser compatibility
   * and automatic fallback to polling if WebSocket is unavailable.
   */
  connect(): void {
    // Already connected, don't reconnect
    if (this.socket?.connected) {
      console.log('[WebSocket] Already connected');
      return;
    }

    // Reset manual disconnect flag
    this.isManuallyDisconnected = false;

    console.log('[WebSocket] Connecting to', WS_URL);

    // Create Socket.io connection with configuration
    this.socket = io(WS_URL, {
      reconnection: true,
      reconnectionDelay: this.reconnectDelay,
      reconnectionDelayMax: RECONNECT_MAX_DELAY,
      reconnectionAttempts: RECONNECT_MAX_ATTEMPTS,
      transports: ['websocket', 'polling'], // Try WebSocket first, then fallback to polling
    });

    // Handle successful connection
    this.socket.on('connect', () => {
      console.log('[WebSocket] Connected successfully');
      // Reset retry logic on successful connection
      this.reconnectAttempts = 0;
      this.reconnectDelay = RECONNECT_INITIAL_DELAY;
      // Emit a special event for UI to know we're connected
      this.emit('connected', {
        event_type: 'complete',
        content: 'WebSocket connected',
        timestamp: new Date().toISOString(),
      });
    });

    // Handle incoming messages
    this.socket.on('message', (data: unknown) => {
      try {
        // Parse the event data
        const streamEvent = this.parseEvent(data);
        console.log(
          '[WebSocket] Received event:',
          streamEvent.event_type,
          streamEvent.content.substring(0, 50) + '...'
        );

        // Dispatch to registered handlers
        this.dispatchEvent(streamEvent);
      } catch (error) {
        console.error('[WebSocket] Failed to parse message:', error);
      }
    });

    // Handle stream events (alternative message format)
    this.socket.on('stream_event', (data: unknown) => {
      try {
        const streamEvent = this.parseEvent(data);
        console.log('[WebSocket] Received stream event:', streamEvent.event_type);
        this.dispatchEvent(streamEvent);
      } catch (error) {
        console.error('[WebSocket] Failed to parse stream event:', error);
      }
    });

    // Handle connection errors
    this.socket.on('connect_error', (error: Error) => {
      console.error('[WebSocket] Connection error:', error.message);
    });

    // Handle disconnection
    this.socket.on('disconnect', (reason: string) => {
      console.log('[WebSocket] Disconnected:', reason);

      // Don't attempt reconnection if manually disconnected
      if (this.isManuallyDisconnected) {
        console.log('[WebSocket] Manual disconnect - not reconnecting');
        return;
      }

      // Emit disconnection event
      this.emit('disconnected', {
        event_type: 'error',
        content: `Disconnected: ${reason}`,
        timestamp: new Date().toISOString(),
      });
    });

    // Handle reconnection attempts
    this.socket.on('reconnect_attempt', () => {
      this.reconnectAttempts++;
      console.log(
        `[WebSocket] Reconnection attempt ${this.reconnectAttempts}/${RECONNECT_MAX_ATTEMPTS}`
      );
    });

    // Handle reconnection failure
    this.socket.on('reconnect_failed', () => {
      console.error('[WebSocket] Reconnection failed after max attempts');
      this.emit('reconnection_failed', {
        event_type: 'error',
        content: `Failed to reconnect after ${RECONNECT_MAX_ATTEMPTS} attempts`,
        timestamp: new Date().toISOString(),
      });
    });
  }

  /**
   * Disconnect from WebSocket server
   *
   * Closes the connection gracefully.
   * Sets a flag to prevent automatic reconnection.
   */
  disconnect(): void {
    if (this.socket) {
      console.log('[WebSocket] Disconnecting');
      this.isManuallyDisconnected = true;
      this.socket.disconnect();
      this.socket = null;
    }
  }

  /**
   * Send a chat message to the agent
   *
   * Sends a user message to the Portfolio Manager agent.
   * The message is wrapped in a ChatMessage structure and sent via WebSocket.
   *
   * @param message - The user's message
   * @param sessionId - Optional session ID for conversation continuity
   */
  sendMessage(message: string, sessionId?: string): void {
    // Check connection status
    if (!this.socket?.connected) {
      console.error('[WebSocket] Not connected. Cannot send message.');
      return;
    }

    // Create message object
    const chatMessage: ChatMessage = {
      message,
      session_id: sessionId,
    };

    console.log('[WebSocket] Sending message:', message.substring(0, 50) + '...');

    // Send via Socket.io
    try {
      this.socket.emit('message', chatMessage);
    } catch (error) {
      console.error('[WebSocket] Failed to send message:', error);
    }
  }

  /**
   * Register an event handler
   *
   * Registers a callback function to be called when events of a specific type are received.
   * Multiple handlers can be registered for the same event type.
   *
   * Special event types:
   * - 'connected': Emitted when WebSocket connects
   * - 'disconnected': Emitted when WebSocket disconnects
   * - 'reconnection_failed': Emitted when auto-reconnection fails
   * - 'all': Called for all events
   *
   * @param eventType - Event type to listen for ('thinking', 'tool_call', 'response', 'complete', 'error', 'connected', 'disconnected', 'all')
   * @param handler - Handler function to call when event is received
   */
  on(eventType: string, handler: EventHandler): void {
    // Initialize Set if this is the first handler for this event type
    if (!this.eventHandlers.has(eventType)) {
      this.eventHandlers.set(eventType, new Set());
    }

    // Add handler to the Set (prevents duplicates)
    this.eventHandlers.get(eventType)!.add(handler);

    console.log(`[WebSocket] Registered handler for event type: ${eventType}`);
  }

  /**
   * Unregister an event handler
   *
   * Removes a previously registered event handler.
   * If the handler is not found, this is a no-op.
   *
   * @param eventType - Event type to stop listening for
   * @param handler - Handler function to remove
   */
  off(eventType: string, handler: EventHandler): void {
    const handlers = this.eventHandlers.get(eventType);
    if (handlers) {
      const removed = handlers.delete(handler);
      if (removed) {
        console.log(`[WebSocket] Unregistered handler for event type: ${eventType}`);
      }
      // Clean up empty Sets
      if (handlers.size === 0) {
        this.eventHandlers.delete(eventType);
      }
    }
  }

  /**
   * Get connection status
   *
   * @returns true if WebSocket is connected, false otherwise
   */
  get isConnected(): boolean {
    return this.socket?.connected ?? false;
  }

  /**
   * Get the current Socket.io instance
   *
   * Used internally and for advanced use cases.
   *
   * @returns The Socket instance or null if not connected
   */
  getSocket(): Socket | null {
    return this.socket;
  }

  /**
   * Parse and validate incoming event data
   *
   * Validates that the event has the required structure.
   * Throws an error if validation fails.
   *
   * @param data - Raw event data from WebSocket
   * @returns Parsed AgentStreamEvent
   * @throws Error if data is invalid
   */
  private parseEvent(data: unknown): AgentStreamEvent {
    // Type guard and validation
    if (typeof data !== 'object' || data === null) {
      throw new Error('Invalid event data: expected object');
    }

    const event = data as Record<string, unknown>;

    // Validate required fields
    if (typeof event.event_type !== 'string') {
      throw new Error('Invalid event: missing or invalid event_type');
    }
    if (typeof event.content !== 'string') {
      throw new Error('Invalid event: missing or invalid content');
    }
    if (typeof event.timestamp !== 'string') {
      throw new Error('Invalid event: missing or invalid timestamp');
    }

    // Return validated event
    return {
      event_type: event.event_type as AgentStreamEvent['event_type'],
      content: event.content,
      timestamp: event.timestamp,
      metadata: event.metadata as Record<string, unknown> | undefined,
    };
  }

  /**
   * Dispatch an event to all registered handlers
   *
   * Calls all handlers registered for:
   * 1. The specific event type
   * 2. The 'all' type (receives all events)
   *
   * @param streamEvent - The event to dispatch
   */
  private dispatchEvent(streamEvent: AgentStreamEvent): void {
    // Get handlers for this specific event type
    const specificHandlers = this.eventHandlers.get(streamEvent.event_type) || new Set();
    specificHandlers.forEach(handler => {
      try {
        handler(streamEvent);
      } catch (error) {
        console.error('[WebSocket] Handler error:', error);
      }
    });

    // Get handlers for 'all' event type
    const allHandlers = this.eventHandlers.get('all') || new Set();
    allHandlers.forEach(handler => {
      try {
        handler(streamEvent);
      } catch (error) {
        console.error('[WebSocket] Handler error:', error);
      }
    });
  }

  /**
   * Emit an event (internal use)
   *
   * Used internally to emit special events like 'connected' and 'disconnected'.
   *
   * @param eventType - Event type
   * @param event - Event data
   */
  private emit(eventType: string, event: AgentStreamEvent): void {
    // Create a synthetic event with the given type
    const synthEvent: AgentStreamEvent = {
      ...event,
      event_type: eventType as AgentStreamEvent['event_type'],
    };
    this.dispatchEvent(synthEvent);
  }
}

// Create and export singleton instance
const wsClient = new WebSocketClient();

// Connect automatically on import
wsClient.connect();

export { wsClient, WebSocketClient };
export default wsClient;
