/**
 * React Hook for WebSocket Management
 *
 * Provides a simple, type-safe interface for components to use WebSocket functionality.
 * Handles automatic connection/disconnection lifecycle and event management.
 *
 * Biblical Principle: SERVE - Make developer experience simpler, not harder.
 * This hook abstracts away WebSocket complexity so components can focus on business logic.
 *
 * Usage:
 *
 *   function ChatComponent() {
 *     const { isConnected, messages, sendMessage, clearMessages } = useWebSocket();
 *
 *     return (
 *       <div>
 *         {isConnected && <span>Connected</span>}
 *         {messages.map(msg => <p key={msg.timestamp}>{msg.content}</p>)}
 *         <button onClick={() => sendMessage("Hello")}>Send</button>
 *       </div>
 *     );
 *   }
 */

import { useEffect, useState, useCallback, useRef } from 'react';
import { wsClient } from '@/services/websocket';
import type { AgentStreamEvent } from '@/types';

/**
 * Return type for useWebSocket hook
 */
export interface UseWebSocketReturn {
  // Connection state
  isConnected: boolean;

  // Message history
  messages: AgentStreamEvent[];

  // Actions
  sendMessage: (message: string, sessionId?: string) => void;
  clearMessages: () => void;

  // Advanced
  getLastMessage: () => AgentStreamEvent | undefined;
  getMessagesByType: (eventType: string) => AgentStreamEvent[];
}

/**
 * React hook for WebSocket communication
 *
 * Provides reactive access to WebSocket state and messaging capabilities.
 * Automatically manages connection lifecycle (connects on mount, cleans up on unmount).
 *
 * Key features:
 * - Automatic connection on component mount
 * - Automatic cleanup on component unmount
 * - Connection status tracking
 * - Message history management
 * - Type-safe event handling
 * - Graceful disconnection handling
 *
 * @returns UseWebSocketReturn - WebSocket interface for components
 *
 * @example
 *   const { isConnected, messages, sendMessage } = useWebSocket();
 *
 *   useEffect(() => {
 *     if (isConnected) {
 *       sendMessage('Analyze portfolio', 'session-123');
 *     }
 *   }, [isConnected, sendMessage]);
 */
export function useWebSocket(): UseWebSocketReturn {
  // State management
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState<AgentStreamEvent[]>([]);

  // Use ref to track if component is mounted
  const isMountedRef = useRef(true);

  // Connection monitoring interval (in milliseconds)
  const CONNECTION_CHECK_INTERVAL = 1000;

  /**
   * Effect: Handle connection lifecycle
   *
   * Sets up WebSocket connection, monitors connection state, and cleans up on unmount.
   */
  useEffect(() => {
    console.log('[useWebSocket] Mounting component');

    // Start periodic connection status check
    const connectionCheckInterval = setInterval(() => {
      // Only update state if component is still mounted
      if (isMountedRef.current) {
        setIsConnected(wsClient.isConnected);
      }
    }, CONNECTION_CHECK_INTERVAL);

    // Define event handler for all incoming events
    const handleStreamEvent = (event: AgentStreamEvent) => {
      if (isMountedRef.current) {
        // Add event to message history
        setMessages(prevMessages => {
          // Prevent duplicate messages by checking timestamp
          // (in case of duplicate events from server)
          const isDuplicate = prevMessages.some(
            msg => msg.timestamp === event.timestamp && msg.content === event.content
          );
          if (isDuplicate) {
            console.log('[useWebSocket] Ignoring duplicate message');
            return prevMessages;
          }
          return [...prevMessages, event];
        });

        // Log event for debugging
        console.log(`[useWebSocket] Event received: ${event.event_type}`);
      }
    };

    // Register handler for all events
    wsClient.on('all', handleStreamEvent);

    // Initial connection check
    setIsConnected(wsClient.isConnected);

    // Cleanup on unmount
    return () => {
      console.log('[useWebSocket] Unmounting component');
      isMountedRef.current = false;

      // Unregister event handler
      wsClient.off('all', handleStreamEvent);

      // Clear connection check interval
      clearInterval(connectionCheckInterval);

      // NOTE: We don't call wsClient.disconnect() here to maintain persistent connection
      // across component remounts. If you need to disconnect, call it explicitly.
    };
  }, []);

  /**
   * Send a message to the agent
   *
   * Validates message before sending and logs the action.
   *
   * @param message - Message text to send
   * @param sessionId - Optional session ID for conversation continuity
   */
  const sendMessage = useCallback((message: string, sessionId?: string) => {
    // Validation
    if (!message || message.trim().length === 0) {
      console.warn('[useWebSocket] Attempted to send empty message');
      return;
    }

    // Check connection before sending
    if (!wsClient.isConnected) {
      console.error('[useWebSocket] Cannot send message: not connected');
      return;
    }

    // Send via WebSocket client
    console.log('[useWebSocket] Sending message:', message.substring(0, 50) + '...');
    wsClient.sendMessage(message, sessionId);
  }, []);

  /**
   * Clear message history
   *
   * Resets the local message buffer without affecting the server.
   * Useful for starting a new conversation or clearing the UI.
   */
  const clearMessages = useCallback(() => {
    console.log('[useWebSocket] Clearing message history');
    setMessages([]);
  }, []);

  /**
   * Get the most recent message
   *
   * @returns The last message in history, or undefined if no messages
   */
  const getLastMessage = useCallback((): AgentStreamEvent | undefined => {
    return messages.length > 0 ? messages[messages.length - 1] : undefined;
  }, [messages]);

  /**
   * Filter messages by event type
   *
   * Useful for getting specific types of events (e.g., all 'error' events).
   *
   * @param eventType - Event type to filter for
   * @returns Array of matching events
   */
  const getMessagesByType = useCallback(
    (eventType: string): AgentStreamEvent[] => {
      return messages.filter(msg => msg.event_type === eventType);
    },
    [messages]
  );

  return {
    isConnected,
    messages,
    sendMessage,
    clearMessages,
    getLastMessage,
    getMessagesByType,
  };
}

export default useWebSocket;
