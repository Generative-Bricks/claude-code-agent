# Operations Standards

> **Status:** Active
> **Purpose:** How to run, secure, and monitor the system. "If you are running the system, read this."

---

## 1. Observability

**Principle:** Standardize on OpenTelemetry (OTel). No proprietary lock-in.

### Traces (Required)
Create a root span per user request.
*   **Taxonomy:** `ai.request` $\rightarrow$ `ai.plan` $\rightarrow$ `ai.retrieve` $\rightarrow$ `ai.generate`.
*   **Attributes:** `gen_ai.system`, `gen_ai.request.model`, `ai.agent.id`, `user.session.id`.

### Metrics (Required)
*   **Latency:** p50/p90/p95/p99 by operation.
*   **Token Usage:** `input_tokens`, `output_tokens`.
*   **Cost:** Estimated USD cost.
*   **Quality:** `eval_score`, `win_rate`.

### Logs
*   **Format:** Structured JSON.
*   **Content:** Summaries, IDs, error codes. **NO PII/Secrets.**

---

## 2. Traceability

**Principle:** End-to-end provenance. Every output must be reproducible.

### Required Artifacts
For every interaction, capture:
1.  **System Prompt:** Versioned (`v2025.3.0`).
2.  **User Input:** Hash + Redacted content.
3.  **Context:** Document IDs, RAG index version.
4.  **Model Config:** Temp, Top-P, Seed.
5.  **Output:** Hash + Content.

### Reproducibility Procedure
1.  Fetch provenance bundle for `request.id`.
2.  Restore prompt, model, and context versions.
3.  Re-execute with same seed.
4.  Compare output.

---

## 3. Evaluation

**Principle:** Mix methods (Offline + Online + Human).

### Evaluation Framework
**Principle:** Mix methods (Offline + Online + Human).

#### 1. Outside-In (Black Box)
Evaluate the *outcome* against the user's intent.
*   **Metrics:** Acceptance Rate, Win Rate, Success Rate.
*   **Method:** A/B Tests, Human Feedback (Thumbs up/down).

#### 2. Inside-Out (Glass Box)
Evaluate the *process* and *trajectory*.
*   **Metrics:** Faithfulness, Context Precision, Tool Usage Efficiency.
*   **Method:** Tracing, RAGAS Metrics, Latency/Cost analysis.

### Offline (Pre-Deploy)
*   **Benchmarks:** HELM, MTEB.
*   **RAG Metrics:** Faithfulness, Context Precision/Recall (RAGAS).
*   **Safety:** Jailbreak resistance.

### Online (Post-Deploy)
*   **A/B Tests:** Randomized assignment.
*   **Shadow Traffic:** Run candidate silently to de-risk.
*   **Rollout:** Canary deployments.

### Human Feedback
*   **In-Product:** Thumbs up/down.
*   **Review Queues:** Expert review of low-confidence items.
*   **Feedback Loop:** Convert feedback into durable eval cases.

---

## 4. Security

**Principle:** Secure by default. Verify continuously.

### Core Requirements
*   **Least Privilege:** Agents/Users only get necessary access.
*   **Secrets:** Never commit secrets. Use vaults.
*   **Input Validation:** Sanitize all inputs (prevent XSS/Injection).

### AI Specifics
*   **Prompt Injection:** Treat all user input as untrusted.
*   **Data Leakage:** Redact PII before sending to LLM providers.
*   **Sandboxing:** Execute generated code in isolated environments.

---

## 5. Feedback Loops

**Principle:** Close the loop. Operational data drives development.

### The Pipeline
1.  **Collect:** Feedback via API/UI.
2.  **Convert:** Turn feedback into Eval Cases.
3.  **Optimize:** Use feedback to tune prompts (Few-Shot).
4.  **Update:** Deploy improved models/prompts.

### Metrics
*   **Acceptance Rate:** % of suggestions accepted by user.
*   **Win Rate:** A/B test performance.
*   **Defect Rate:** % of interactions flagged as unsafe/incorrect.
