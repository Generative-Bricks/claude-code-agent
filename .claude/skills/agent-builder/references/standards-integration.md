# Standards Integration Guide

> **Purpose:** Map skill stages to standards and reference files

---

## Stage-to-Standards Mapping

| Stage | Standard Documents | Reference Files |
|-------|-------------------|-----------------|
| **1. BRAINSTORM** | CORE_FRAMEWORK.md, AGENTIC.md | principles-framework.md, agent-taxonomy.md |
| **2. DESIGN** | AGENTIC.md | agent-taxonomy.md, memory-strategies.md |
| **3. IMPLEMENT** | DEVELOPMENT.md | coding-standards.md |
| **4. TEST** | DEVELOPMENT.md, OPERATIONS.md | coding-standards.md, operations-guide.md |
| **5. DOCUMENT** | - | - |
| **6. DEPLOY** | AGENTIC.md, OPERATIONS.md | operations-guide.md |
| **7. OBSERVE** | OPERATIONS.md | operations-guide.md |
| **8. EVALUATE** | OPERATIONS.md | operations-guide.md |
| **9. ITERATE** | OPERATIONS.md | operations-guide.md |

---

## Progressive Hint Trigger Points

| Stage | Trigger | Hint | Reference |
|-------|---------|------|-----------|
| BRAINSTORM | Always | "Apply 6 Principles decision framework?" | principles-framework.md |
| BRAINSTORM | Always | "Classify with Agent Taxonomy (Level 0-4)?" | agent-taxonomy.md |
| DESIGN | Multi-agent | "Apply A2A protocol standards?" | agent-taxonomy.md |
| DESIGN | State needed | "Need memory strategy guidance (STM/LTM)?" | memory-strategies.md |
| DESIGN | Sensitive ops | "Apply security/identity standards?" | operations-guide.md |
| IMPLEMENT | Always | "Apply coding standards (lint/validation)?" | coding-standards.md |
| TEST | Always | "Apply testing pyramid (80/15/5)?" | coding-standards.md |
| DEPLOY | Always | "Apply deployment gates checklist?" | operations-guide.md |
| OBSERVE | Always | "Setup OpenTelemetry observability?" | operations-guide.md |
| EVALUATE | Always | "Define evaluation framework?" | operations-guide.md |
| ITERATE | Always | "Setup feedback loops?" | operations-guide.md |

---

## Quick Links

### Reference Files (Application Guides)
- [Principles Framework](./principles-framework.md) - 6 foundational principles
- [Agent Taxonomy](./agent-taxonomy.md) - Agent levels 0-4, A2A protocol
- [Memory Strategies](./memory-strategies.md) - STM/LTM/Hybrid, RAG vs NL2SQL
- [Coding Standards](./coding-standards.md) - Validation, testing, linting
- [Operations Guide](./operations-guide.md) - Deploy, Observe, Evaluate

### Source Documents (Full Standards)
- [CORE_FRAMEWORK.md](../../../../docs/principles/CORE_FRAMEWORK.md) - Biblical principles, cascade framework
- [AGENTIC.md](../../../../docs/standards/AGENTIC.md) - Agent architecture, lifecycle, memory, A2A
- [DEVELOPMENT.md](../../../../docs/standards/DEVELOPMENT.md) - Coding standards, testing, git
- [OPERATIONS.md](../../../../docs/standards/OPERATIONS.md) - Observability, evaluation, security

---

## When to Apply Standards

### Always Apply (Core)
- **Zod/Pydantic validation** - Every agent, every tool
- **Error handling** - Production-grade from day one
- **Basic logging** - Structured JSON, no PII

### Apply for Production
- **6 Principles check** - Verify design alignment
- **Testing pyramid** - 80/15/5 coverage
- **Deployment gates** - Before any release

### Apply for Enterprise/Mission-Critical
- **Full observability** - OTel traces, metrics, alerts
- **Evaluation framework** - Offline + Online + Human
- **SPIFFE identity** - Agent authentication
- **A2A protocol** - Multi-agent coordination

---

## Single Source of Truth

| Content | Authoritative Source | Reference (Guide) |
|---------|---------------------|-------------------|
| 6 Principles | docs/principles/CORE_FRAMEWORK.md | principles-framework.md |
| Agent Taxonomy | docs/standards/AGENTIC.md | agent-taxonomy.md |
| Memory Strategy | docs/standards/AGENTIC.md | memory-strategies.md |
| Coding Standards | docs/standards/DEVELOPMENT.md | coding-standards.md |
| Operations | docs/standards/OPERATIONS.md | operations-guide.md |

**Update Flow:**
1. Source documents are authoritative
2. Reference files provide agent-specific application guidance
3. Reference files link to sources for comprehensive reading
4. Updates to sources don't require skill changes
