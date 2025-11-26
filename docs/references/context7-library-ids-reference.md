# Context7 Library IDs Reference

This document provides a comprehensive reference of common Context7 library IDs used during AI development research. All library IDs have been verified using the Context7 `resolve-library-id` tool.

## Verified Library IDs

### Google AI & Gemini

| Library ID | Description | Code Snippets | Trust Score |
|------------|-------------|---------------|-------------|
| `/websites/ai_google_dev_gemini-api` | The Gemini API provides access to Google's advanced AI models for text, image, speech, and video generation and understanding | 3,388 | 7.5 |
| `/google-gemini/cookbook` | A cookbook providing a structured learning path with hands-on tutorials and practical examples for using the Gemini API, covering quick starts, specific features, and complex use cases | 1,898 | 7.8 |
| `/websites/google_github_io_adk-docs` | The Agent Development Kit (ADK) is a flexible framework for building and deploying AI agents, optimized for Gemini and the Google ecosystem | 1,600 | 7.5 |
| `/google/a2a` | An open protocol enabling communication and interoperability between opaque agentic applications, allowing agents to discover capabilities and collaborate securely. Official specification: [https://a2a-protocol.org/latest/specification/](https://a2a-protocol.org/latest/specification/) | 184 | 8.9 |

**Additional Google/Gemini Resources:**
- `/google/adk-python` - Agent Development Kit for Python (154 snippets, 8.9 trust)
- `/google/adk-go` - Agent Development Kit for Go (21 snippets, 9.6 trust)
- `/google/adk-java` - Agent Development Kit for Java (49 snippets, 8.9 trust)
- `/google/adk-samples` - Ready-to-use agents built on ADK (454 snippets, 8.9 trust)
- `/google/mcp-security` - Model Context Protocol servers for Google's security products and services (2,367 snippets, 8.9 trust)

### Anthropic & Claude

| Library ID | Description | Code Snippets | Trust Score |
|------------|-------------|---------------|-------------|
| `/anthropics/claude-code` | Claude Code is an agentic terminal tool that understands your codebase to help you code faster by executing tasks, explaining code, and handling git workflows | 37 | 8.8 |
| `/websites/code_claude` | Claude Code is a command-line interface and web-based tool that enables developers to interact with Claude AI for code analysis, generation, and debugging | 212 | 7.5 |
| `/anthropics/anthropic-cookbook` | The Anthropic Cookbook provides code and guides for developers to build with Claude, offering easily integrable code snippets and explanations for various AI tasks | 865 | 8.8 |
| `/anthropics/anthropic-quickstarts` | A collection of projects designed to help developers quickly get started building applications using the Anthropic API, featuring examples like customer support agents and financial data analysts | 41 | 8.8 |

**Additional Anthropic Resources:**
- `/anthropics/anthropic-sdk-python` - Official Python SDK for Anthropic API (93 snippets, 8.8 trust)
- `/anthropics/anthropic-sdk-typescript` - Official TypeScript SDK for Anthropic API (106 snippets, 8.8 trust)
- `/anthropics/anthropic-sdk-go` - Official Go SDK for Anthropic API (95 snippets, 8.8 trust)
- `/anthropics/skills` - Anthropic Skills for specialized tasks (317 snippets, 8.5 trust)
- `/anthropics/courses` - Educational courses for working with Claude SDK (840 snippets, 8.8 trust)
- `/websites/claude_en` - Claude documentation on Model Context Protocol (MCP) - an open protocol standardizing how applications provide context to LLMs (2,169 snippets, 7.5 trust)

### Strands Agents

| Library ID | Description | Code Snippets | Trust Score |
|------------|-------------|---------------|-------------|
| `/strands-agents/sdk-python` | Strands Agents is a model-driven SDK for building and running AI agents with a flexible, lightweight, and model-agnostic approach, supporting advanced capabilities and seamless MCP server integration | 38 | 5.1 |
| `/strands-agents/docs` | Strands Agents is a framework for building and running AI agents with a model-driven approach, enabling development in just a few lines of code | 573 | 5.1 |

**Additional Strands Resources:**
- `/strands-agents/tools` - Ready-to-use tools for file operations, shell integration, memory, API interactions (96 snippets, 5.1 trust)
- `/strands-agents/samples` - Collection of examples demonstrating model-driven agent building (736 snippets, 5.1 trust)
- `/strands-agents/agent-builder` - Interactive toolkit for building, testing, and extending AI agents (12 snippets, 5.1 trust)

## Additional Common Library IDs for Research

### OpenAI

| Library ID | Description | Code Snippets | Trust Score |
|------------|-------------|---------------|-------------|
| `/openai/openai-python` | The OpenAI Python library provides convenient access to the OpenAI REST API from any Python 3.8+ application | 335 | 9.1 |
| `/openai/openai-node` | A TypeScript and JavaScript library providing convenient access to the OpenAI REST API | 244 | 9.1 |
| `/websites/platform_openai` | The OpenAI API provides access to advanced AI models for natural language processing, image generation, and more | 382,518 | 9.5 |
| `/openai/codex` | OpenAI Codex CLI is a lightweight, local coding agent that runs in your terminal, enabling users to interact with AI models for coding tasks | 202 | 9.1 |
| `/openai/openai-agents-python` | The OpenAI Agents SDK is a framework for building multi-agent workflows, supporting various LLMs and featuring agents, handoffs, guardrails, sessions, and tracing | 203 | 9.1 |
| `/openai/openai-cookbook` | Example code and guides for accomplishing common tasks with the OpenAI API, written primarily in Python | 3,855 | 9.1 |

**Additional OpenAI Resources:**
- `/openai/openai-apps-sdk-examples` - Example UI components and Model Context Protocol (MCP) servers for the OpenAI Apps SDK (27 snippets, 9.1 trust)

### LangChain & LangGraph

| Library ID | Description | Code Snippets | Trust Score |
|------------|-------------|---------------|-------------|
| `/langchain-ai/langchainjs` | LangChain JavaScript/TypeScript framework for building applications powered by large language models | 381 | 9.2 |
| `/websites/langchain_oss_python_langchain` | LangChain Python framework designed to simplify the creation of applications powered by large language models | 420 | 7.5 |
| `/langchain-ai/langgraph` | LangGraph is a low-level orchestration framework for building, managing, and deploying long-running, stateful agents | 2,104 | 9.2 |
| `/langchain-ai/langgraphjs` | LangGraph JS is a JavaScript SDK for building stateful, multi-actor applications with large language models | 1,134 | 9.2 |

**Additional LangChain Resources:**
- `/langchain-ai/langchain-community` - Community-maintained LangChain integrations (18 snippets, 9.2 trust)
- `/langchain-ai/langchain-google` - Packages for integrating Google products with LangChain (60 snippets, 9.2 trust)
- `/websites/smith_langchain` - LangSmith platform for building and refining production-grade LLM applications (1,155 snippets, 7.5 trust)

### Vercel AI SDK & Next.js

| Library ID | Description | Code Snippets | Trust Score |
|------------|-------------|---------------|-------------|
| `/vercel/ai` | The AI Toolkit for TypeScript. From the creators of Next.js, the AI SDK is a free open-source library for building AI-powered applications and agents | 2,377 | 10 |
| `/vercel/next.js` | Next.js enables you to create full-stack web applications by extending the latest React features and integrating powerful Rust-based JavaScript tooling | 3,050 | 10 |
| `/websites/ai-sdk_dev` | AI SDK is a TypeScript toolkit by Vercel designed to help developers build AI-powered applications and agents | 779 | 7.5 |
| `/websites/aisdkagents` | AI SDK Agents offers full-stack, production-ready patterns for building agents, workflows, and tool calling using Vercel AI SDK v6 | 432 | 7.5 |

### React

| Library ID | Description | Code Snippets | Trust Score |
|------------|-------------|---------------|-------------|
| `/reactjs/react.dev` | React.dev is the official documentation website for React, a JavaScript library for building user interfaces | 2,836 | 10 |
| `/websites/react_dev` | React is a JavaScript library for building user interfaces, allowing developers to create interactive web and native applications | 1,923 | 9.0 |

### Supabase

| Library ID | Description | Code Snippets | Trust Score |
|------------|-------------|---------------|-------------|
| `/supabase/supabase` | Supabase is the Postgres development platform, offering features like hosted Postgres, authentication, auto-generated APIs, functions, and file storage using enterprise-grade open source tools | 4,552 | 10 |
| `/websites/supabase` | Supabase is an open-source backend platform providing a full Postgres database, authentication, storage, real-time, and edge functions to help developers build applications quickly | 23,710 | 7.5 |
| `/websites/supabase_com-docs` | Supabase is an open-source Postgres development platform that provides all the backend features needed to build a product, including a full database, authentication, storage, real-time functionality, and edge functions | 21,395 | - |

**Additional Supabase Resources:**
- `/supabase/supabase-js` - Isomorphic JavaScript client for Supabase (182 snippets, 9.5 trust)
- `/supabase/supabase-py` - Python client for Supabase (62 snippets, 9.5 trust)
- `/supabase/supabase-swift` - Swift client library for Supabase (23 snippets, 9.5 trust)
- `/supabase/cli` - Command-line interface tool for managing Supabase projects (48 snippets, 9.5 trust)
- `/supabase/ui` - React UI library with pre-built components for Supabase (15 snippets, 9.5 trust)
- `/supabase/auth` - Go-based authentication and user management server (64 snippets, 9.5 trust)
- `/supabase/realtime` - Realtime enables sending ephemeral messages and listening to Postgres changes over WebSockets (37 snippets, 9.5 trust)

### Model Context Protocol (MCP)

| Library ID | Description | Code Snippets | Trust Score |
|------------|-------------|---------------|-------------|
| `/websites/modelcontextprotocol_io` | An open protocol that standardizes how applications provide context to LLMs, enabling seamless integration with data sources and tools for building AI agents and complex workflows | 29 | 7.5 |
| `/modelcontextprotocol/modelcontextprotocol` | The specification and protocol schema for the Model Context Protocol, with schemas defined in TypeScript and available as JSON Schema | 754 | 7.8 |
| `/modelcontextprotocol/python-sdk` | The MCP Python SDK implements the Model Context Protocol, enabling applications to provide standardized context for LLMs, build MCP clients, and create MCP servers | 124 | 7.8 |
| `/modelcontextprotocol/typescript-sdk` | The MCP TypeScript SDK implements the Model Context Protocol, enabling easy creation of clients and servers for standardized LLM context exchange | 49 | 7.8 |

**Additional MCP Resources:**
- `/websites/modelcontextprotocol_io_specification` - MCP specification for defining and managing context for models (611 snippets, 7.5 trust)
- `/websites/claude_en` - Claude documentation on MCP (2,169 snippets, 7.5 trust)
- `/google/mcp-security` - Google's MCP servers for security products and services (2,367 snippets, 8.9 trust)
- `/openai/openai-apps-sdk-examples` - OpenAI Apps SDK examples with MCP servers (27 snippets, 9.1 trust)
- `/tsadoq/a2a-mcp-tutorial` - Tutorial on using Model Context Protocol by Anthropic and Agent2Agent Protocol by Google (43 snippets, 9 trust)

## Usage

To use these library IDs with Context7, you can fetch documentation using the `get-library-docs` tool:

```python
# Example: Fetch Gemini API documentation
get-library-docs(context7CompatibleLibraryID="/websites/ai_google_dev_gemini-api")

# Example: Fetch Gemini Cookbook documentation
get-library-docs(context7CompatibleLibraryID="/google-gemini/cookbook")

# Example: Fetch OpenAI Codex documentation
get-library-docs(context7CompatibleLibraryID="/openai/codex")

# Example: Fetch OpenAI Agents Python documentation
get-library-docs(context7CompatibleLibraryID="/openai/openai-agents-python")

# Example: Fetch Claude Code documentation
get-library-docs(context7CompatibleLibraryID="/anthropics/claude-code")

# Example: Fetch Supabase documentation
get-library-docs(context7CompatibleLibraryID="/supabase/supabase")

# Example: Fetch Model Context Protocol documentation
get-library-docs(context7CompatibleLibraryID="/websites/modelcontextprotocol_io")

# Example: Fetch A2A Protocol documentation
get-library-docs(context7CompatibleLibraryID="/google/a2a")
```

## Verification

All library IDs in this document have been verified using the Context7 `resolve-library-id` tool. The tool translates general library names into specific Context7-compatible library IDs, ensuring accurate documentation retrieval.

## References

- [Context7 Libraries](https://context7.com/libraries) - Browse all available libraries
- [Context7 Documentation](https://deepwiki.com/upstash/context7) - Context7 MCP server documentation
- [Context7 GitHub](https://github.com/upstash/context7) - Context7 source code and examples
- [A2A Protocol Specification](https://a2a-protocol.org/latest/specification/) - Official A2A (Agent2Agent) Protocol specification

## Notes

- Library IDs follow the format `/organization/project` or `/websites/domain-path`
- Some libraries have version-specific IDs (e.g., `/org/project/version`)
- Trust scores indicate the authority and reliability of the documentation source
- Code snippet counts show the amount of example code available in the documentation

---

*Last updated: Based on Context7 library resolution as of current date*
*All library IDs verified using Context7 resolve-library-id tool*

