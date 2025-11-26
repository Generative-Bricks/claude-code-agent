#!/usr/bin/env python3
"""
Utility to inspect OpenAI Agents SDK result object structure.

This helps understand what information is available about tool calls and token usage.
"""

from agents import Runner

# Print the result object attributes
print("OpenAI Agents SDK Result Object Attributes:")
print("=" * 80)
print("\nCommon attributes you can check:")
print("  - result.final_output    : Final response text")
print("  - result.messages        : All messages exchanged")
print("  - result.usage           : Token usage statistics")
print("  - result.run_id          : Unique run identifier")
print("\nTo see tool calls:")
print("  Loop through result.messages and check for tool_calls attribute")
print("\nTo see token usage:")
print("  Access result.usage['prompt_tokens'], result.usage['completion_tokens']")
print("=" * 80)

print("\n\nExample inspection code:")
print("-" * 80)
print("""
# After running analysis:
result = Runner.run(agent, input=message, session=session)

# Check what's available
print("Available attributes:", dir(result))

# Token usage
if hasattr(result, 'usage'):
    print(f"Total tokens: {result.usage.get('total_tokens', 0)}")

# Tool calls
if hasattr(result, 'messages'):
    for msg in result.messages:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tc in msg.tool_calls:
                print(f"Tool: {tc.function.name}")
                print(f"Args: {tc.function.arguments}")
""")
print("-" * 80)
