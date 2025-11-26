"""
Quick test script for WebSocket endpoint.

Tests the /api/ws/chat WebSocket endpoint with sample messages.

Biblical Principle: EXCELLENCE - Test thoroughly before marking complete.
Biblical Principle: TRUTH - Verify actual behavior, don't assume it works.

Usage:
    python -m src.api.routes.test_websocket
"""

import asyncio
import json
import sys

try:
    import websockets
except ImportError:
    print("ERROR: websockets package not installed")
    print("Install with: uv pip install websockets")
    sys.exit(1)


async def test_websocket():
    """
    Test WebSocket connection and message exchange.

    Tests:
    1. Connection establishment
    2. Welcome message reception
    3. Sending chat message
    4. Receiving streaming events
    5. Graceful disconnection
    """
    uri = "ws://localhost:8000/api/ws/chat"

    print("=" * 80)
    print("WebSocket Test Script")
    print("=" * 80)
    print(f"Connecting to: {uri}")
    print()

    try:
        async with websockets.connect(uri) as ws:
            print("✓ Connection established")
            print()

            # Receive welcome message
            welcome = await ws.recv()
            welcome_event = json.loads(welcome)
            print(f"[{welcome_event['event_type'].upper()}] {welcome_event['content']}")
            print()

            # Send test message
            test_message = {
                "message": "Analyze portfolio conservative for client CLT-2024-001"
            }
            print(f"Sending: {test_message['message']}")
            await ws.send(json.dumps(test_message))
            print()

            # Receive responses until complete
            while True:
                response = await ws.recv()
                event = json.loads(response)

                timestamp = event.get('timestamp', 'N/A')
                event_type = event['event_type'].upper()
                content = event['content']

                print(f"[{event_type}] {content}")

                if event.get('metadata'):
                    print(f"  Metadata: {event['metadata']}")

                if event['event_type'] == 'complete':
                    break

            print()
            print("✓ Test completed successfully")

    except websockets.exceptions.WebSocketException as e:
        print(f"❌ WebSocket error: {e}")
        print()
        print("Troubleshooting:")
        print("1. Is the API server running? (python -m src.api.main)")
        print("2. Is the port correct? (default: 8000)")
        print("3. Check logs/api.log for server errors")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print("Response was not valid JSON")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print("⚠️  Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


async def test_multiple_messages():
    """
    Test sending multiple messages in same connection.

    Verifies:
    - Connection persistence
    - Session state management
    - Multiple message handling
    """
    uri = "ws://localhost:8000/api/ws/chat"

    print()
    print("=" * 80)
    print("Multiple Messages Test")
    print("=" * 80)
    print()

    async with websockets.connect(uri) as ws:
        # Receive welcome
        welcome = await ws.recv()
        print(f"Connected: {json.loads(welcome)['content']}")
        print()

        # Send multiple messages
        messages = [
            "What's the risk profile of my conservative portfolio?",
            "How does it compare to my aggressive portfolio?",
            "Generate a report for both."
        ]

        for i, msg in enumerate(messages, 1):
            print(f"Message {i}: {msg}")
            await ws.send(json.dumps({"message": msg}))

            # Collect all events for this message
            while True:
                response = await ws.recv()
                event = json.loads(response)
                print(f"  [{event['event_type'].upper()}] {event['content'][:50]}...")

                if event['event_type'] == 'complete':
                    break

            print()

        print("✓ Multiple messages test completed")


if __name__ == "__main__":
    print()
    print("Starting WebSocket tests...")
    print()

    # Run basic test
    asyncio.run(test_websocket())

    # Run multiple messages test
    asyncio.run(test_multiple_messages())

    print()
    print("=" * 80)
    print("All tests passed!")
    print("=" * 80)
    print()
