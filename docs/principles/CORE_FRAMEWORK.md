# Generative Bricks Core Framework

> **Status:** Active
> **Purpose:** The central source of truth for the Generative Bricks philosophy, cascading from biblical foundations to technical implementation.

---

## 1. Foundational Sources (The "Why")

Our entire operational and technical methodology is built on 6 Foundational Principles derived from Scripture. These are not just values; they are the **sources** from which all our decisions flow.

### 1. TRUTH
**Source:** *"I am the way, the truth, and the life"* (John 14:6)
**Core Value:** Radical transparency in all code, communication, and decisions.
**In Practice:** Every decision must be observable and explainable. No hidden logic, no silent failures.

### 2. HONOR
**Source:** *"Love the Lord your God... and love your neighbor as yourself"* (Matthew 22:36-40)
**Core Value:** Prioritize user needs and data sovereignty above technical elegance or profit.
**In Practice:** Client data sovereignty, user-first design, and respect for privacy.

### 3. EXCELLENCE
**Source:** *"Whatever you do, work heartily, as for the Lord"* (Colossians 3:23)
**Core Value:** Production-grade from inception. "Good enough" is not enough.
**In Practice:** No "fix it later" mentality. Proper error handling, testing, and documentation from the start.

### 4. SERVE
**Source:** *"I have set you an example that you should wash one another's feet"* (John 13:14)
**Core Value:** Lead by removing obstacles for others (developers and users).
**In Practice:** Make developer and user experience simpler. Clear APIs, sensible defaults, helpful error messages.

### 5. PERSEVERE
**Source:** *"Run with perseverance the race marked out for us"* (Hebrews 12:1-3)
**Core Value:** Build resilient systems that handle failures gracefully and keep running.
**In Practice:** Retry logic, fallback strategies, graceful degradation, and autonomous recovery.

### 6. SHARPEN
**Source:** *"As iron sharpens iron, so one person sharpens another"* (Proverbs 27:17)
**Core Value:** Continuous improvement through feedback and mutual learning.
**In Practice:** Metrics collection, A/B testing, regular refactoring, and learning from every interaction.

---

## 2. The Cascade Framework (The "How")

We do not just "have" values; we apply them through a predictable cascade.

**Foundational Sources → Operative Forces → Observable Patterns → Predictable Outcomes**

### The Flow
1.  **Foundational Sources:** The unchangeable truth we start with (e.g., TRUTH).
2.  **Operative Forces:** How that truth changes our behavior (e.g., "Radical transparency").
3.  **Observable Patterns:** What others see us doing (e.g., "Honest assessment of risks").
4.  **Predictable Outcomes:** The result we can expect (e.g., "Deep client trust").

*(See `principles/02-complete-cascade-framework.md` in archive for the full detailed breakdown of each principle)*

---

## 3. Software Development Principles (The "What")

We translate the 6 Foundational Principles into concrete technical standards for building autonomous agentic systems.

### 1. TRUTH → Transparent Observability Principle
*\"Every agent action must be traceable, auditable, and explainable\"*
*   **Agent Design:** Every decision point must log context, options considered, and choice made.
*   **Infrastructure:** Full observability stack (metrics, logs, traces) required from day one.
*   **Decision Rule:** Choose the solution that provides clearer observability.

### 2. HONOR → Client-First Architecture Principle
*\"Design decisions must prioritize client data sovereignty and success over technical elegance\"*
*   **Architecture:** Client-side agents preferred when possible.
*   **Security:** Zero-trust architecture with client-controlled access boundaries.
*   **Decision Rule:** Distributed storage honors client sovereignty, even if centralized is easier.

### 3. EXCELLENCE → Reliability-First Engineering Principle
*\"Every component must be production-grade from inception\"*
*   **No MVP Agents:** Every agent must handle edge cases from v1.
*   **Testing:** Chaos engineering and failure injection from development phase.
*   **Decision Rule:** Retry logic and circuit breakers must be present from v1.

### 4. SERVE → Developer Empowerment Principle
*\"Framework design must reduce complexity for developers\"*
*   **Design:** Sensible defaults for all configurations.
*   **Experience:** Single command to run locally with full debugging.
*   **Decision Rule:** The framework should handle complexity (state, retries) so developers focus on logic.

### 5. PERSEVERE → Resilient Autonomy Principle
*\"Agents must continue operating correctly during partial system failures\"*
*   **Resilience:** Agents must operate with 50% tools unavailable or intermittent network.
*   **Autonomy:** Automatic state recovery after crashes.
*   **Decision Rule:** Queue critical decisions locally when offline; sync when restored.

### 6. SHARPEN → Continuous Learning Principle
*\"Systems must evolve through operational feedback\"*
*   **Learning:** Agent decisions tracked with outcomes for pattern analysis.
*   **Improvement:** Failed interactions automatically generate test cases.
*   **Decision Rule:** Implement prompt versioning with A/B testing to evolve logic.

---

## 4. Decision Framework Summary

When facing architectural decisions, apply principles in this order:

1.  **TRUTH:** Is it observable?
2.  **HONOR:** Does it respect the client?
3.  **EXCELLENCE:** Is it production-grade?
4.  **SERVE:** Is it simple for developers?
5.  **PERSEVERE:** Is it resilient?
6.  **SHARPEN:** Does it learn?

| Technical Decision | Primary Principle | Secondary Check |
|-------------------|------------------|-----------------|
| Agent vs Workflow | TRUTH (observability) | EXCELLENCE (reliability) |
| Client vs Server-side | HONOR (sovereignty) | SERVE (simplicity) |
| Security Architecture | HONOR (client-first) | PERSEVERE (resilient) |
| Testing Strategy | EXCELLENCE (quality) | SHARPEN (learning) |
| Tool Design | SERVE (developer UX) | TRUTH (transparency) |
| Scaling Approach | PERSEVERE (autonomy) | HONOR (isolation) |
