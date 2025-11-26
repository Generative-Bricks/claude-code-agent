# Operations Guide

> **Source:** [docs/standards/OPERATIONS.md](../../../../docs/standards/OPERATIONS.md) + [docs/standards/AGENTIC.md](../../../../docs/standards/AGENTIC.md)
> **Purpose:** Guide for DEPLOY, OBSERVE, and EVALUATE stages

---

## Stage 7: DEPLOY

### Deployment Gates

Before deploying any agent, pass these gates in order:

```
1. Offline Evals  →  Benchmarks, safety testing
2. Red Team       →  Adversarial testing
3. Staging        →  Integration testing
4. Production     →  Gradual rollout
```

### Rollout Strategy

| Phase | Traffic | Duration | Rollback Trigger |
|-------|---------|----------|------------------|
| Canary | 1% | 1-4 hours | Any guardrail breach |
| Limited | 10% | 1-2 days | Error rate > 1% |
| Gradual | 50% | 1-2 days | p99 latency spike |
| Full | 100% | Ongoing | Monitoring alerts |

### Rollback Plan

**Automatic rollback triggers:**
- Guardrail breach (safety violation)
- Error rate exceeds threshold
- p99 latency exceeds SLA
- Quality score drops below threshold

**Manual rollback procedure:**
1. Redirect traffic to previous version
2. Preserve logs for investigation
3. Create incident report
4. Fix and re-deploy through gates

### Agent Identity & Inventory

- **SPIFFE ID:** Register agent identity for authentication
- **Inventory:** Document agent in central inventory:
  - Name, description, owner
  - Tools and capabilities
  - Dependencies
  - SLA requirements

---

## Stage 8: OBSERVE

### OpenTelemetry (OTel) Standard

**Principle:** Standardize on OTel. No proprietary lock-in.

### Traces (Required)

Create a root span per user request with this taxonomy:

```
ai.request → ai.plan → ai.retrieve → ai.generate
```

**Required Attributes:**
| Attribute | Description |
|-----------|-------------|
| `gen_ai.system` | LLM provider (anthropic, openai) |
| `gen_ai.request.model` | Model ID (claude-sonnet-4) |
| `ai.agent.id` | Agent identifier |
| `user.session.id` | User session |

### Metrics (Required)

| Metric | Description | Percentiles |
|--------|-------------|-------------|
| **Latency** | Response time | p50/p90/p95/p99 |
| **Token Usage** | `input_tokens`, `output_tokens` | sum, avg |
| **Cost** | Estimated USD | sum, avg |
| **Quality** | `eval_score`, `win_rate` | avg |

### Logs

- **Format:** Structured JSON
- **Content:** Summaries, IDs, error codes
- **NEVER LOG:** PII, secrets, full prompts with user data

---

## Stage 9: EVALUATE

### Evaluation Framework

Mix methods for comprehensive evaluation:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    OFFLINE      │     │     ONLINE      │     │     HUMAN       │
│  (Pre-Deploy)   │     │  (Post-Deploy)  │     │   (Feedback)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Outside-In Evaluation (Black Box)

Evaluate the **outcome** against user's intent:

| Metric | Description | Target |
|--------|-------------|--------|
| Acceptance Rate | % suggestions accepted | >80% |
| Win Rate | A/B test performance | >50% |
| Success Rate | Task completion | >90% |

**Method:** A/B tests, human feedback (thumbs up/down)

### Inside-Out Evaluation (Glass Box)

Evaluate the **process** and trajectory:

| Metric | Description | Tool |
|--------|-------------|------|
| Faithfulness | Answer matches context | RAGAS |
| Context Precision | Relevant context retrieved | RAGAS |
| Tool Efficiency | Tools used appropriately | Tracing |

**Method:** Tracing analysis, latency/cost review

### Offline Evaluation (Pre-Deploy)

- **Benchmarks:** HELM, MTEB (if applicable)
- **RAG Metrics:** Faithfulness, Context Precision/Recall
- **Safety:** Jailbreak resistance testing

### Online Evaluation (Post-Deploy)

| Method | Description | Risk |
|--------|-------------|------|
| A/B Test | Randomized assignment | Medium |
| Shadow Traffic | Run candidate silently | Low |
| Canary | Gradual rollout | Low |

### Human Feedback Loop

```
Collect → Convert → Optimize → Update
   ↓         ↓          ↓         ↓
In-product  Eval     Few-shot   Deploy
feedback    cases    tuning     improved
```

- **In-Product:** Thumbs up/down
- **Review Queues:** Expert review of low-confidence items
- **Feedback → Eval Cases:** Convert feedback into durable tests

---

## Security Hardening

### AI-Specific Security

| Threat | Mitigation |
|--------|------------|
| **Prompt Injection** | Treat all user input as untrusted |
| **Data Leakage** | Redact PII before sending to LLM |
| **Code Execution** | Isolated sandboxes only |
| **Secret Exposure** | Never commit secrets, use vaults |

### General Security

- **Least Privilege:** Agents only get necessary access
- **Input Validation:** Sanitize all inputs (prevent XSS/Injection)
- **Secrets:** Never commit secrets, use environment variables

---

## Progressive Hint Integration

### DEPLOY Stage

> "Apply deployment gates checklist?"

If **Yes:**
- [ ] Offline evaluations passed (benchmarks, safety)
- [ ] Red team testing completed
- [ ] Staging integration tests passing
- [ ] Rollback plan documented
- [ ] Agent identity registered (if applicable)
- [ ] Agent documented in inventory

### OBSERVE Stage

> "Setup OpenTelemetry observability?"

If **Yes:**
- [ ] Root span per request created
- [ ] Trace taxonomy followed (ai.request → ai.plan → ...)
- [ ] Required attributes present (model, agent.id, session.id)
- [ ] Latency metrics configured (p50/p90/p95/p99)
- [ ] Token usage tracked
- [ ] No PII in logs

### EVALUATE Stage

> "Define evaluation framework (Offline/Online/Human)?"

If **Yes:**
- [ ] Success metrics defined (Acceptance Rate, Win Rate)
- [ ] Offline benchmarks identified
- [ ] Online evaluation strategy chosen (A/B, Shadow, Canary)
- [ ] Human feedback collection planned
- [ ] Feedback → Eval Case pipeline defined

---

## Full Documentation

For complete operations standards, see:
**[docs/standards/OPERATIONS.md](../../../../docs/standards/OPERATIONS.md)**

For agent lifecycle and security, see:
**[docs/standards/AGENTIC.md](../../../../docs/standards/AGENTIC.md)**
