"""
WebSocket API Routes for Portfolio Collaboration System.

Provides WebSocket endpoint for real-time agent chat and streaming responses.

Biblical Principle: SERVE - Real-time interaction for better user experience.
Biblical Principle: PERSEVERE - Resilient connection handling with reconnection support.
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime
from typing import Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState

from src.api.schemas import AgentStreamEvent, ChatMessage

logger = logging.getLogger(__name__)
router = APIRouter()

# Active WebSocket connections
active_connections: Dict[str, WebSocket] = {}


@router.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for interactive agent chat.

    Protocol:
    1. Client connects
    2. Server sends welcome event
    3. Client sends ChatMessage JSON
    4. Server streams AgentStreamEvent JSON responses
    5. Server sends complete event when done

    Biblical Principle: EXCELLENCE - Production-ready WebSocket handling.
    Biblical Principle: TRUTH - Transparent logging of all connections and messages.
    """
    # Accept connection
    await websocket.accept()

    # Generate session ID
    session_id = str(uuid.uuid4())
    active_connections[session_id] = websocket

    logger.info(f"WebSocket connected: {session_id}")

    try:
        # Send welcome message
        await send_event(
            websocket,
            event_type="response",
            content=f"Connected to Portfolio Manager. Session ID: {session_id}"
        )

        # Main message loop
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = ChatMessage.model_validate_json(data)

            logger.info(f"Received message from {session_id}: {message.message[:50]}...")

            # For MVP, send a simple acknowledgment
            # TODO: In Wave 4, integrate with Portfolio Manager agent streaming
            # This is where we'll call:
            # async for event in stream_agent_response(message):
            #     await send_event(websocket, event.type, event.content, event.metadata)

            await send_event(
                websocket,
                event_type="thinking",
                content="Processing your request..."
            )

            await asyncio.sleep(0.5)

            await send_event(
                websocket,
                event_type="response",
                content=f"Echo: {message.message}\n\n(Agent streaming will be implemented in Wave 4)"
            )

            await send_event(
                websocket,
                event_type="complete",
                content="Response complete"
            )

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error for {session_id}: {e}", exc_info=True)
        try:
            await send_event(
                websocket,
                event_type="error",
                content=f"Error: {str(e)}"
            )
        except Exception:
            # Connection might already be closed
            logger.error(f"Failed to send error event to {session_id}")
    finally:
        # Cleanup
        if session_id in active_connections:
            del active_connections[session_id]

        if websocket.client_state == WebSocketState.CONNECTED:
            try:
                await websocket.close()
            except Exception:
                logger.warning(f"Failed to close WebSocket for {session_id}")


async def send_event(
    websocket: WebSocket,
    event_type: str,
    content: str,
    metadata: dict = None
):
    """
    Send an AgentStreamEvent to the client.

    Args:
        websocket: WebSocket connection to send to
        event_type: Type of event (thinking, tool_call, response, complete, error)
        content: Event content/message
        metadata: Optional event-specific metadata

    Raises:
        Exception: If send fails (connection closed, etc.)

    Biblical Principle: TRUTH - All events are transparently structured and logged.
    """
    event = AgentStreamEvent(
        event_type=event_type,
        content=content,
        timestamp=datetime.utcnow(),
        metadata=metadata
    )

    await websocket.send_text(event.model_dump_json())
