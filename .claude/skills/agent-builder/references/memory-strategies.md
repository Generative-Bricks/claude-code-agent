# Memory Strategies Reference

> **Source:** [docs/standards/AGENTIC.md](../../../../docs/standards/AGENTIC.md) (Section 3)
> **Purpose:** Choose the right memory strategy for your agent

---

## Memory Types

### Short-Term Memory (STM)
- **Scope:** Session-scoped
- **Retrieval:** <100ms
- **Content:** Raw events, current conversation
- **Persistence:** Lost when session ends
- **Use When:** Single-session interactions, stateless APIs

### Long-Term Memory (LTM)
- **Scope:** Cross-session
- **Content:** User preferences, learned facts, historical patterns
- **Retrieval:** Semantic search
- **Persistence:** Permanent until explicitly removed
- **Use When:** Returning users, personalization, learning agents

### Hybrid (STM + LTM)
- **Scope:** Both session and cross-session
- **Content:** Current context + historical knowledge
- **Use When:** Complex workflows with returning users

---

## Memory Decision Matrix

| Scenario | Memory Type | Rationale |
|----------|-------------|-----------|
| One-shot Q&A | None/STM | No persistence needed |
| Multi-turn conversation | STM | Session context only |
| Returning user preferences | LTM | Cross-session persistence |
| Learning from interactions | LTM | Pattern storage |
| Complex analysis with history | Hybrid | Both contexts needed |

---

## Base Knowledge Strategies

### RAG (Retrieval-Augmented Generation)

**Use For:** Unstructured data (documents, policies, FAQs)

**Best Practices:**
- Chunk size: 500-2000 tokens
- Vector database for semantic search
- Embed context in prompts

**When to Use RAG:**
- Large document collections (100+ documents)
- Semantic search needed
- Documents change frequently

**When to Skip RAG:**
- Small document collections (<20 documents)
- Exact match queries
- Single document fits in context window

### NL2SQL (Natural Language to SQL)

**Use For:** Structured data (analytics, reporting, databases)

**Best Practices:**
- Strict schema validation
- Query sanitization
- Result formatting

**When to Use:**
- Tabular data queries
- Analytics dashboards
- Database reporting

---

## Direct Context Pattern (No RAG)

From existing agents in this repository:

**When Direct Context Works:**
- Working with 1 file at a time
- Documents are 5-20 pages each
- Entire document fits in LLM context window
- User doesn't need semantic search across 100s of documents

**Benefits:**
- 3-step workflow vs 7+ steps with RAG
- No vector database infrastructure
- Simpler architecture

**Example:** Google Drive Agent uses direct context passing

---

## Progressive Hint Integration

During the **DESIGN** stage, you'll be asked:

> "Need memory strategy guidance (STM/LTM)?"

If you answer **Yes**, determine:

1. **Session Requirements:**
   - [ ] Single-session only → STM or None
   - [ ] Returning users → LTM needed
   - [ ] Both → Hybrid

2. **Knowledge Base:**
   - [ ] No external knowledge → None
   - [ ] Small doc collection (<20 docs) → Direct context
   - [ ] Large doc collection (100+ docs) → RAG
   - [ ] Structured database → NL2SQL

3. **Persistence:**
   - [ ] No persistence needed
   - [ ] Session state only
   - [ ] User preferences (cross-session)
   - [ ] Learning/improvement (cross-session)

---

## Implementation Patterns

### STM Implementation
```python
# In-memory session state
class SessionState:
    conversation_history: list[Message]
    current_context: dict
    tool_results: list[ToolResult]
```

### LTM Implementation
```python
# Persistent user memory
class UserMemory:
    user_id: str
    preferences: dict
    learned_facts: list[Fact]
    interaction_history: list[InteractionSummary]
```

### Hybrid Implementation
```python
# Combined memory
class AgentMemory:
    session: SessionState  # STM
    user: UserMemory       # LTM

    def get_context(self) -> str:
        return combine(self.session, self.user)
```

---

## Full Documentation

For complete memory and knowledge standards, see:
**[docs/standards/AGENTIC.md](../../../../docs/standards/AGENTIC.md)** (Section 3: Memory & Knowledge)
