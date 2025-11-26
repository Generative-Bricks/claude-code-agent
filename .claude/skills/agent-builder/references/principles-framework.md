# Foundational Principles Framework

> **Source:** [docs/principles/CORE_FRAMEWORK.md](../../../../docs/principles/CORE_FRAMEWORK.md)
> **Purpose:** Quick reference for applying the 6 Foundational Principles during agent design

---

## The 6 Foundational Principles

### 1. TRUTH
**Source:** *"I am the way, the truth, and the life"* (John 14:6)

**Core Value:** Radical transparency in all code, communication, and decisions.

**Agent Application:**
- Every agent decision must be observable and explainable
- No hidden logic, no silent failures
- Full tracing with context, options considered, and choice made

**Decision Rule:** Choose the solution that provides clearer observability.

---

### 2. HONOR
**Source:** *"Love the Lord your God... and love your neighbor as yourself"* (Matthew 22:36-40)

**Core Value:** Prioritize user needs and data sovereignty above technical elegance.

**Agent Application:**
- Client-side agents preferred when possible
- Zero-trust architecture with client-controlled boundaries
- Respect user privacy and data ownership

**Decision Rule:** Distributed storage honors client sovereignty, even if centralized is easier.

---

### 3. EXCELLENCE
**Source:** *"Whatever you do, work heartily, as for the Lord"* (Colossians 3:23)

**Core Value:** Production-grade from inception. "Good enough" is not enough.

**Agent Application:**
- No MVP agents - every agent handles edge cases from v1
- Retry logic and circuit breakers from day one
- Proper error handling, testing, and documentation from the start

**Decision Rule:** No "fix it later" mentality.

---

### 4. SERVE
**Source:** *"I have set you an example that you should wash one another's feet"* (John 13:14)

**Core Value:** Lead by removing obstacles for others (developers and users).

**Agent Application:**
- Sensible defaults for all configurations
- Single command to run locally with full debugging
- Framework handles complexity (state, retries) so developers focus on logic

**Decision Rule:** Make developer and user experience simpler, not harder.

---

### 5. PERSEVERE
**Source:** *"Run with perseverance the race marked out for us"* (Hebrews 12:1-3)

**Core Value:** Build resilient systems that handle failures gracefully.

**Agent Application:**
- Agents must operate with 50% tools unavailable
- Automatic state recovery after crashes
- Queue critical decisions locally when offline; sync when restored

**Decision Rule:** Graceful degradation over hard failure.

---

### 6. SHARPEN
**Source:** *"As iron sharpens iron, so one person sharpens another"* (Proverbs 27:17)

**Core Value:** Continuous improvement through feedback and mutual learning.

**Agent Application:**
- Agent decisions tracked with outcomes for pattern analysis
- Failed interactions automatically generate test cases
- Prompt versioning with A/B testing to evolve logic

**Decision Rule:** Every interaction is a learning opportunity.

---

## Decision Framework Priority Order

When facing architectural decisions, apply principles in this order:

```
1. TRUTH      → Is it observable?
2. HONOR      → Does it respect the client?
3. EXCELLENCE → Is it production-grade?
4. SERVE      → Is it simple for developers?
5. PERSEVERE  → Is it resilient?
6. SHARPEN    → Does it learn?
```

---

## Quick Decision Matrix

| Technical Decision | Primary Principle | Secondary Check |
|-------------------|------------------|-----------------|
| Agent vs Workflow | TRUTH (observability) | EXCELLENCE (reliability) |
| Client vs Server-side | HONOR (sovereignty) | SERVE (simplicity) |
| Security Architecture | HONOR (client-first) | PERSEVERE (resilient) |
| Testing Strategy | EXCELLENCE (quality) | SHARPEN (learning) |
| Tool Design | SERVE (developer UX) | TRUTH (transparency) |
| Scaling Approach | PERSEVERE (autonomy) | HONOR (isolation) |
| Error Handling | TRUTH (observable) | PERSEVERE (graceful) |
| State Management | PERSEVERE (resilient) | SERVE (simple) |

---

## The Cascade Framework

Every principle flows through a predictable cascade:

```
Foundational Source → Operative Force → Observable Pattern → Predictable Outcome
```

**Example (TRUTH):**
1. **Source:** Radical transparency
2. **Force:** Observable decision-making
3. **Pattern:** Full tracing, clear logging
4. **Outcome:** Deep trust, easy debugging

---

## Progressive Hint Integration

During the **BRAINSTORM** stage, you'll be asked:

> "Want to apply the 6 Principles decision framework?"

If you answer **Yes**, verify your design against these checkpoints:

- [ ] **TRUTH:** Can every agent decision be traced and explained?
- [ ] **HONOR:** Is client data sovereignty respected?
- [ ] **EXCELLENCE:** Is it production-grade from day one?
- [ ] **SERVE:** Does it simplify the developer/user experience?
- [ ] **PERSEVERE:** Can it handle partial failures gracefully?
- [ ] **SHARPEN:** Does it have feedback loops for improvement?

---

## Full Documentation

For the complete cascade framework breakdown and detailed guidance, see:
**[docs/principles/CORE_FRAMEWORK.md](../../../../docs/principles/CORE_FRAMEWORK.md)**
