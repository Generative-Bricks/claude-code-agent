"""
Main Entry Point for Google Drive Agent.

Provides a simple command-line interface for interacting with the agent.

Usage:
    python src/main.py                    # Interactive mode
    python src/main.py "your question"    # Single query mode
"""

import sys
import asyncio
from agent import GoogleDriveAgent
from strands.models.gemini import GeminiModel
from config.settings import settings


def print_banner():
    """Print welcome banner."""
    print("\n" + "="*70)
    print("🤖 Google Drive Document Assistant")
    print("="*70)
    print("\nI can help you search, browse, and understand your Google Drive files.")
    print("\nCommands:")
    print("  - Type your question naturally")
    print("  - 'cache stats' - Show cache statistics")
    print("  - 'cache clear' - Clear cached content")
    print("  - 'quit' or 'exit' - Exit the program")
    print("\n" + "="*70 + "\n")


async def interactive_mode(agent: GoogleDriveAgent):
    """
    Run agent in interactive mode (REPL).

    User can type multiple questions in a conversation loop.
    """
    print_banner()

    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()

            if not user_input:
                continue

            # Handle special commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break

            elif user_input.lower() == 'cache stats':
                stats = agent.get_cache_stats()
                print(f"\n📊 Cache Statistics:")
                print(f"   Files: {stats.get('file_count', 0)}")
                print(f"   Size: {stats.get('total_size_mb', 0)} MB")
                print(f"   Location: {stats.get('cache_dir', 'N/A')}")
                continue

            elif user_input.lower() == 'cache clear':
                agent.clear_cache()
                continue

            # Process user query with agent
            print("\n🤖 Assistant: ", end='', flush=True)

            # Stream response for better UX
            full_response = ""
            async for event in agent.stream(user_input):
                # Handle different event types
                if content := event.get("content"):
                    print(content, end='', flush=True)
                    full_response += content

                elif tool_use := event.get("tool_use"):
                    tool_name = tool_use.get("name", "unknown")
                    print(f"\n🔧 Using tool: {tool_name}...", flush=True)

                elif tool_result := event.get("tool_result"):
                    # Tool completed (optional: show result)
                    pass

            print("\n")  # New line after response

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break

        except Exception as e:
            print(f"\n❌ Error: {e}")


async def single_query_mode(agent: GoogleDriveAgent, query: str):
    """
    Run agent with a single query and exit.

    Args:
        agent: GoogleDriveAgent instance
        query: User's question
    """
    print(f"\n💬 Query: {query}\n")
    print("🤖 Assistant: ", end='', flush=True)

    try:
        # Stream response
        async for event in agent.stream(query):
            if content := event.get("content"):
                print(content, end='', flush=True)

            elif tool_use := event.get("tool_use"):
                tool_name = tool_use.get("name", "unknown")
                print(f"\n🔧 Using tool: {tool_name}...", flush=True)

        print("\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")


async def main():
    """Main entry point."""
    try:
        # Initialize Gemini model
        model = GeminiModel(
            client_args={
                "api_key": settings.GOOGLE_API_KEY,
            },
            model_id="gemini-2.5-flash",
            params={
                "temperature": 0.7,
                "max_output_tokens": 2048,
            }
        )

        # Initialize agent with Gemini model
        agent = GoogleDriveAgent(
            model_id=model,  # Pass model object instead of string
            enable_cache=True
        )

        # Check if query was provided as command-line argument
        if len(sys.argv) > 1:
            # Single query mode
            query = " ".join(sys.argv[1:])
            await single_query_mode(agent, query)
        else:
            # Interactive mode
            await interactive_mode(agent)

    except FileNotFoundError as e:
        print(f"\n❌ Setup Error: {e}")
        print("\n📋 Please complete Google Drive API setup:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a project and enable Google Drive API")
        print("3. Create OAuth 2.0 credentials (Desktop app)")
        print("4. Download credentials.json to ./credentials/")
        print("\nSee README.md for detailed instructions.")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # Run async main function
    asyncio.run(main())
