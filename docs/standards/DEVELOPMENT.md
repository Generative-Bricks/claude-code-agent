# Development Standards

> **Status:** Active
> **Purpose:** The canonical source for how we write code. "If you are writing code, read this."

---

## 1. Core Philosophy

*   **Readability First:** Optimize for the next reader. Explicit > Clever.
*   **Single Responsibility:** Each module/class/function does one thing well.
*   **DRY (Don't Repeat Yourself):** Extract duplication into well-named functions.
*   **KISS (Keep It Simple, Stupid):** Avoid speculative abstractions (YAGNI).
*   **Fail Loudly:** Validate inputs, handle errors at boundaries.

---

## 2. Language Baselines

### TypeScript / JavaScript
*   **Style:** Strict mode, ES modules, `async/await`.
*   **Lint/Format:** ESLint + Prettier.
*   **Testing:** Vitest (preferred) or Jest.
*   **Validation:** **Zod** is mandatory for all external inputs (APIs, Tools).

### Python
*   **Style:** PEP 8, Type hints (PEP 484) for public APIs.
*   **Lint/Format:** Ruff (lint) + Black (format) + MyPy (types).
*   **Testing:** pytest.
*   **Validation:** **Pydantic** is mandatory for all data models and Agents.

### Shell (bash)
*   **Style:** `set -Eeuo pipefail`. Quote variables.
*   **Lint:** ShellCheck.

---

## 3. Coding Standards

### Naming Conventions
*   **Clarity:** `fetchUser` > `getData`. `timeoutMs` > `timeout`.
*   **Casing:**
    *   Variables/Functions: `camelCase` (TS), `snake_case` (Python).
    *   Classes: `PascalCase`.
    *   Constants: `UPPER_CASE`.
    *   Files: `kebab-case` (docs), `snake_case` (Python), `camelCase` (TS filenames).

### Error Handling
*   **Throw Domain Errors:** Don't just return `null`. Throw `UserNotFoundError`.
*   **Context:** Include IDs and actionable messages.
*   **Log:** Log at appropriate levels (ERROR vs WARN).

---

## 4. Data Validation Standards

### Python: Pydantic
**Mandatory for:** Agent models, API request/response, Config.
*   Use `BaseModel` for all structures.
*   Use `Field` for constraints (`ge=0`, `min_length=1`).
*   Use `model_dump()` for serialization.

```python
class User(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(ge=0)
```

### TypeScript: Zod
**Mandatory for:** MCP Tools, API inputs.
*   Use `safeParse()` for user input to handle errors gracefully.
*   Infer types from schemas: `type User = z.infer<typeof UserSchema>`.

```typescript
const UserSchema = z.object({
  name: z.string().min(1),
  age: z.number().min(0)
});
```

---

## 5. Testing Standards

### The Pyramid
1.  **Unit (80%):** Fast, isolated, mocked dependencies.
2.  **Integration (15%):** Real DB/API interactions.
3.  **E2E (5%):** Full system flows.

### Principles
*   **AAA:** Arrange, Act, Assert.
*   **Deterministic:** No flaky tests allowed.
*   **Coverage:** Aim for 80%+, but value quality over quantity.

---

## 6. Git & Review Process

### Branching
*   **Trunk-Based:** Short-lived feature branches (`feat/login`, `fix/api`).
*   **PRs:** Small, atomic changes. One logical change per PR.

### Commits (Conventional Commits)
*   `feat(auth): add login endpoint`
*   `fix(api): handle timeout gracefully`
*   `chore: update dependencies`

### Code Review
*   **Author:** Contextual description, self-review first.
*   **Reviewer:** Focus on correctness, clarity, and security. Be kind and actionable.

---

## 7. Linting & Tooling Matrix

| Language | Lint | Format | Type Check |
| :--- | :--- | :--- | :--- |
| **TS/JS** | ESLint | Prettier | `tsc` |
| **Python** | Ruff | Black | MyPy |
| **Shell** | ShellCheck | shfmt | - |
| **Markdown** | markdownlint | Prettier | - |
| **YAML** | yamllint | Prettier | - |

**Policy:** CI fails on any lint error. No warnings allowed in main.
