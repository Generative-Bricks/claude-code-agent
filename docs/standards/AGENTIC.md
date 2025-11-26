# Agent Standards

> **Status:** Active
> **Purpose:** The unified theory of Agentic Systems. "If you are building an agent, read this."

---

## 1. Agent Architecture

### Core Components
1.  **Model ("Brain"):** The LLM (Claude, Gemini, GPT).
2.  **Tools ("Hands"):** Capabilities (Search, APIs, Code Exec).
3.  **Orchestration ("Nervous System"):** State management, loops, memory.
4.  **Deployment ("Body"):** Hosting, security, logging.

### Taxonomy
*   **Level 0 (Reasoning):** LLM only. Q&A, Planning.
*   **Level 1 (Connected):** LLM + Tools. Retrieval, Actions.
*   **Level 2 (Strategic):** Multi-step planning, Context management.
*   **Level 3 (Collaborative):** Multi-agent systems, Manager/Worker.
*   **Level 4 (Self-Evolving):** Dynamic tool creation, Self-improvement.

### Boundaries
*   **Explicit Purpose:** Every agent must have a `name`, `description`, and `instruction`.
*   **Specialization:** Prefer specialized sub-agents over monolithic "God agents".
*   **Configuration:** Declarative (YAML/JSON) agent definitions.

---

## 2. Agent Lifecycle

### Creation
*   **Register Identity:** Every agent needs a SPIFFE ID.
*   **Inventory:** Document in the Agent Inventory.

### Deployment
*   **Gates:** Offline Evals $\rightarrow$ Red Team $\rightarrow$ Staging.
*   **Rollout:** Canary (1% $\rightarrow$ 100%).
*   **Rollback:** Automatic rollback on guardrail breach.

### Retirement
*   **Migration:** Plan traffic migration before shutdown.
*   **Archive:** Archive data and configs.

---

## 3. Memory & Knowledge

### Memory Strategy (Context)
*   **Short-Term (STM):** Session-scoped. <100ms retrieval. Raw events.
*   **Long-Term (LTM):** Cross-session. User preferences, facts. Semantic search.
*   **Hybrid:** Use both when needed.

### Base Knowledge (Facts)
*   **RAG (Vector DB):** Unstructured data (docs, policies). Chunk size 500-2000 tokens.
*   **NL2SQL:** Structured data (analytics, reporting). Strict schema validation.

---

## 4. Multi-Agent Coordination

### Patterns
1.  **Graph:** Structured flows with conditional logic (Cycles allowed).
2.  **Swarm:** Collaborative, open-ended problem solving.
3.  **Workflow:** Deterministic DAGs, parallel execution.
4.  **Hierarchical:** Manager agent delegating to worker agents.

### Communication (A2A)
**Standard:** Use the Agent-to-Agent (A2A) Protocol.
*   **Discovery:** Agents publish **Agent Cards** (Capabilities, Inputs, Outputs) to a central Registry.
*   **Protocol:** JSON-RPC 2.0 over HTTP/gRPC.
*   **Handshake:** Capability negotiation before task delegation.
*   **State:** Shared state instance for coordination (not implicit context).

---

## 5. Tools & MCP

### Model Context Protocol (MCP)
**Default Integration Pattern:** Prefer MCP servers over ad-hoc tools.
*   **Resources:** Data access (`mcp://`).
*   **Tools:** Functions (`call_tool`).
*   **Prompts:** Templates (`get_prompt`).

### Tool Implementation
*   **Native Tools:** Use platform natives (Google Search, Code Interpreter) for speed.
*   **Custom Functions:** Use Pydantic/Zod for validation.
*   **Safety:**
    *   **Idempotent:** Read-only tools should be safe to retry.
    *   **Approval:** Sensitive actions require Human-in-the-Loop (HITL).
    *   **Filtering:** Use `allowed_tools` to reduce context window usage.

---

## 6. Security & Identity

*   **Identity:** Agents must authenticate via SPIFFE.
*   **Access Control:** Least privilege. Agents only get tools they *need*.
*   **Sandboxing:** Code execution must happen in isolated sandboxes.
*   **Traceability:** Every action must be logged with `agent.id` and `trace.id`.
