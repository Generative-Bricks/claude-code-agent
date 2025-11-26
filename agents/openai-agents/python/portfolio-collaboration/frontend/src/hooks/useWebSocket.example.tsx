/**
 * Example Usage of useWebSocket Hook
 *
 * This file demonstrates various ways to use the useWebSocket hook
 * in your React components. Copy and adapt these patterns to your needs.
 *
 * NOT AN EXECUTABLE FILE - This is documentation only.
 */

/* eslint-disable @typescript-eslint/no-unused-vars */

import { useEffect, useState } from 'react';
import { useWebSocket } from './useWebSocket';
import type { AgentStreamEvent } from '@/types';

/**
 * Example 1: Basic Chat Component
 *
 * Simple component that sends messages and displays responses.
 */
export function BasicChatExample() {
  const { isConnected, messages, sendMessage } = useWebSocket();
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim()) {
      sendMessage(input);
      setInput('');
    }
  };

  return (
    <div className="chat-container">
      <div className="status">
        {isConnected ? (
          <span className="connected">Connected</span>
        ) : (
          <span className="disconnected">Disconnected</span>
        )}
      </div>

      <div className="messages">
        {messages.map(msg => (
          <div key={msg.timestamp} className={`message ${msg.event_type}`}>
            <span className="type">{msg.event_type}</span>
            <span className="content">{msg.content}</span>
          </div>
        ))}
      </div>

      <div className="input-area">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type a message..."
          disabled={!isConnected}
        />
        <button onClick={handleSend} disabled={!isConnected}>
          Send
        </button>
      </div>
    </div>
  );
}

/**
 * Example 2: Portfolio Analysis Component with Session
 *
 * Demonstrates sending an analysis request with session persistence.
 */
export function PortfolioAnalysisExample() {
  const { isConnected, messages, sendMessage, clearMessages, getLastMessage } =
    useWebSocket();
  const [sessionId] = useState(() => `session-${Date.now()}`);

  const analyzePortfolio = (clientId: string, portfolioId: string) => {
    const request = `Analyze portfolio ${portfolioId} for client ${clientId}`;
    sendMessage(request, sessionId);
  };

  const lastMessage = getLastMessage();
  const isCompleted = lastMessage?.event_type === 'complete';

  return (
    <div className="analysis-container">
      <h2>Portfolio Analysis</h2>

      <div className="actions">
        <button onClick={() => analyzePortfolio('CLT-2024-001', 'PORT-001')}>
          Analyze Conservative Portfolio
        </button>
        <button onClick={clearMessages}>Clear Results</button>
      </div>

      <div className="results">
        {isCompleted && <div className="success">Analysis Complete!</div>}

        {messages.map(msg => (
          <div key={msg.timestamp} className={`message ${msg.event_type}`}>
            <div className="timestamp">{new Date(msg.timestamp).toLocaleTimeString()}</div>
            <div className="event-type">{msg.event_type}</div>
            <div className="content">{msg.content}</div>
          </div>
        ))}
      </div>

      <div className="session-info">Session ID: {sessionId}</div>
    </div>
  );
}

/**
 * Example 3: Real-time Thinking Display
 *
 * Shows agent thinking process as it happens with a progress indicator.
 */
export function ThinkingDisplayExample() {
  const { messages, getMessagesByType } = useWebSocket();

  const thinkingMessages = getMessagesByType('thinking');
  const toolCalls = getMessagesByType('tool_call');
  const responses = getMessagesByType('response');

  return (
    <div className="thinking-display">
      <section>
        <h3>Thinking Process ({thinkingMessages.length})</h3>
        <ul>
          {thinkingMessages.map(msg => (
            <li key={msg.timestamp}>{msg.content}</li>
          ))}
        </ul>
      </section>

      <section>
        <h3>Tool Calls ({toolCalls.length})</h3>
        <ul>
          {toolCalls.map(msg => (
            <li key={msg.timestamp}>{msg.content}</li>
          ))}
        </ul>
      </section>

      <section>
        <h3>Responses ({responses.length})</h3>
        <ul>
          {responses.map(msg => (
            <li key={msg.timestamp}>{msg.content}</li>
          ))}
        </ul>
      </section>
    </div>
  );
}

/**
 * Example 4: Error Handling Component
 *
 * Demonstrates proper error handling and recovery.
 */
export function ErrorHandlingExample() {
  const { isConnected, messages, sendMessage } = useWebSocket();
  const [lastError, setLastError] = useState<AgentStreamEvent | null>(null);

  useEffect(() => {
    // Find the most recent error message
    const errors = messages.filter(msg => msg.event_type === 'error');
    if (errors.length > 0) {
      setLastError(errors[errors.length - 1]);
    }
  }, [messages]);

  return (
    <div className="error-handling">
      <div className="connection-status">
        {isConnected ? (
          <div className="status-good">Connection is stable</div>
        ) : (
          <div className="status-warning">
            Attempting to reconnect...
            <button onClick={() => window.location.reload()}>Reload Page</button>
          </div>
        )}
      </div>

      {lastError && (
        <div className="error-alert">
          <h3>Error Occurred</h3>
          <p>{lastError.content}</p>
          <button onClick={() => setLastError(null)}>Dismiss</button>
        </div>
      )}

      <button onClick={() => sendMessage('Test message')} disabled={!isConnected}>
        Send Test Message
      </button>
    </div>
  );
}

/**
 * Example 5: Message Streaming with Custom Event Handler
 *
 * Shows how to use the WebSocket client directly for custom event handling.
 */
export function CustomEventHandlerExample() {
  const { isConnected } = useWebSocket();
  const [customEvents, setCustomEvents] = useState<AgentStreamEvent[]>([]);

  useEffect(() => {
    // Import client directly for custom handling
    import('@/services/websocket').then(({ wsClient }) => {
      // Define custom handler that accumulates events
      const customHandler = (event: AgentStreamEvent) => {
        setCustomEvents(prev => [...prev, event]);

        // Custom logic: log tool calls differently
        if (event.event_type === 'tool_call') {
          console.log('🔧 Tool called:', event.content);
        }
      };

      // Register handler
      wsClient.on('all', customHandler);

      // Cleanup
      return () => {
        wsClient.off('all', customHandler);
      };
    });
  }, []);

  return (
    <div className="custom-events">
      <h2>Custom Event Handler</h2>
      <p>Total events processed: {customEvents.length}</p>
      <ul>
        {customEvents.map(evt => (
          <li key={evt.timestamp}>{evt.event_type}: {evt.content}</li>
        ))}
      </ul>
    </div>
  );
}

/**
 * Example 6: Conversation with Session Management
 *
 * Multi-turn conversation with session persistence.
 */
export function ConversationExample() {
  const { isConnected, messages, sendMessage, clearMessages } = useWebSocket();
  const [sessionId] = useState(() => `conversation-${Date.now()}`);
  const [conversationStage, setConversationStage] = useState<
    'initial' | 'awaiting_response' | 'complete'
  >('initial');

  const startConversation = () => {
    setConversationStage('awaiting_response');
    sendMessage(
      'I need to analyze a portfolio for a 45-year-old client with moderate risk tolerance',
      sessionId
    );
  };

  const askFollowUp = () => {
    sendMessage(
      'What is the tax impact of rebalancing to 60/40 stocks/bonds?',
      sessionId
    );
  };

  const endConversation = () => {
    setConversationStage('complete');
    clearMessages();
  };

  return (
    <div className="conversation">
      <h2>Multi-Turn Conversation</h2>

      <div className="conversation-messages">
        {messages.map(msg => (
          <div key={msg.timestamp} className={`message ${msg.event_type}`}>
            <strong>{msg.event_type.toUpperCase()}</strong>
            <p>{msg.content}</p>
          </div>
        ))}
      </div>

      <div className="conversation-controls">
        {conversationStage === 'initial' && (
          <button onClick={startConversation} disabled={!isConnected}>
            Start Analysis
          </button>
        )}

        {conversationStage === 'awaiting_response' && (
          <>
            <button onClick={askFollowUp} disabled={!isConnected}>
              Ask Follow-up
            </button>
            <button onClick={endConversation}>End Conversation</button>
          </>
        )}

        {conversationStage === 'complete' && (
          <button onClick={() => setConversationStage('initial')}>New Conversation</button>
        )}
      </div>
    </div>
  );
}

/**
 * Usage Tips:
 *
 * 1. Always check `isConnected` before sending messages
 * 2. Use `sessionId` to maintain conversation context
 * 3. Use `getMessagesByType()` to filter events
 * 4. Use `getLastMessage()` for latest event
 * 5. Call `clearMessages()` between conversations
 * 6. Handle errors gracefully - network issues will auto-reconnect
 * 7. Each component should have its own `useWebSocket()` hook instance
 * 8. The WebSocket client is a singleton - all instances share state
 *
 * Event Types:
 * - 'thinking': Agent is processing information
 * - 'tool_call': Agent is calling a tool or function
 * - 'response': Agent is generating a response
 * - 'complete': Analysis/task is complete
 * - 'error': An error occurred
 * - 'connected': WebSocket connected (special event)
 * - 'disconnected': WebSocket disconnected (special event)
 */
