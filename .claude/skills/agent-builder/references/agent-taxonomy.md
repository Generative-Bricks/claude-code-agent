# Agent Taxonomy Reference

> **Source:** [docs/standards/AGENTIC.md](../../../../docs/standards/AGENTIC.md)
> **Purpose:** Classify agents by capability level and understand core components

---

## Agent Levels (0-4)

| Level | Name | Description | Tools | Orchestration | Examples |
|-------|------|-------------|-------|---------------|----------|
| **0** | Reasoning | LLM only | 0 | None | Chat assistants, planning, Q&A |
| **1** | Connected | LLM + Tools | 1-3 | Simple | Document Q&A, search, retrieval |
| **2** | Strategic | Multi-step planning | 4-7 | Context management | Financial analysis, FIA Analyzer |
| **3** | Collaborative | Multi-agent systems | 8+ | Manager/Worker | Portfolio Collaboration |
| **4** | Self-Evolving | Dynamic tool creation | Variable | Self-improvement | Meta-agents |

---

## Core Components

Every agent has four core components:

```
1. Model ("Brain")       → The LLM (Claude, GPT, Gemini)
2. Tools ("Hands")       → Capabilities (Search, APIs, Code Exec)
3. Orchestration ("Nervous System") → State management, loops, memory
4. Deployment ("Body")   → Hosting, security, logging
```

### Component Matrix by Level

| Level | Model | Tools | Orchestration | Deployment |
|-------|-------|-------|---------------|------------|
| 0 | Single LLM | None | Stateless | Simple API |
| 1 | Single LLM | 1-3 tools | In-memory state | API + tool auth |
| 2 | Single LLM | 4-7 tools | Session state | API + persistence |
| 3 | Multiple LLMs | 8+ tools | Shared state, A2A | Distributed |
| 4 | Self-selecting | Dynamic | Self-managing | Autonomous |

---

## Mapping to Existing Complexity Estimation

| Agent-Builder Complexity | Agent Level | Characteristics |
|--------------------------|-------------|-----------------|
| **Low** | Level 0-1 | 1-3 tools, 0 subagents, simple workflow |
| **Medium** | Level 2 | 4-7 tools, 0-2 subagents, multi-stage |
| **High** | Level 3+ | 8+ tools, 3+ subagents, multi-agent |

---

## Agent Boundaries (Best Practices)

From AGENTIC.md:

1. **Explicit Purpose:** Every agent must have a `name`, `description`, and `instruction`
2. **Specialization:** Prefer specialized sub-agents over monolithic "God agents"
3. **Configuration:** Declarative (YAML/JSON) agent definitions

---

## A2A Protocol (Level 3+ Agents)

For multi-agent systems, use the Agent-to-Agent (A2A) Protocol:

### Agent Cards
Agents publish capabilities to a central Registry:
- **Capabilities:** What the agent can do
- **Inputs:** Expected input format
- **Outputs:** Return format

### Communication
- **Protocol:** JSON-RPC 2.0 over HTTP/gRPC
- **Handshake:** Capability negotiation before task delegation
- **State:** Shared state instance for coordination (not implicit context)

### Multi-Agent Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **Graph** | Structured flows with conditional logic | Cycles allowed |
| **Swarm** | Collaborative, open-ended problem solving | Exploration |
| **Workflow** | Deterministic DAGs, parallel execution | Pipeline tasks |
| **Hierarchical** | Manager agent delegating to workers | Portfolio analysis |

---

## Security & Identity

### SPIFFE Identity
- **Requirement:** Every agent needs a SPIFFE ID for authentication
- **Purpose:** Secure agent-to-agent communication

### Access Control
- **Principle:** Least privilege - agents only get tools they *need*
- **Implementation:** Use `allowed_tools` to reduce context window usage

### Sandboxing
- **Rule:** Code execution must happen in isolated sandboxes
- **Traceability:** Every action logged with `agent.id` and `trace.id`

---

## Progressive Hint Integration

During the **BRAINSTORM** stage, you'll be asked:

> "Want to classify using Agent Taxonomy (Level 0-4)?"

If you answer **Yes**, determine:

1. **What Level?**
   - [ ] Level 0: LLM only (reasoning, planning)
   - [ ] Level 1: LLM + Tools (connected)
   - [ ] Level 2: Multi-step planning (strategic)
   - [ ] Level 3: Multi-agent (collaborative)
   - [ ] Level 4: Self-evolving (dynamic)

2. **For Level 3+:**
   - [ ] Will agents use A2A protocol?
   - [ ] What multi-agent pattern? (Graph/Swarm/Workflow/Hierarchical)
   - [ ] How will shared state be managed?

3. **Security:**
   - [ ] Does agent need SPIFFE identity?
   - [ ] What tools should be in `allowed_tools`?
   - [ ] Is code execution sandboxed?

---

## Examples from Repository

| Agent | Level | Tools | Pattern |
|-------|-------|-------|---------|
| Financial Advisor | 2 (Strategic) | 6 | Subagent specialization |
| Google Drive Agent | 1 (Connected) | 3 | Direct context |
| FIA Analyzer | 2 (Strategic) | 3 | Service-based |
| Portfolio Collaboration | 3 (Collaborative) | 4 core | Parallel + Handoff |
| OpportunityIQ | 2 (Strategic) | 5 | 3-layer architecture |

---

## Full Documentation

For complete agent standards including lifecycle management, see:
**[docs/standards/AGENTIC.md](../../../../docs/standards/AGENTIC.md)**
