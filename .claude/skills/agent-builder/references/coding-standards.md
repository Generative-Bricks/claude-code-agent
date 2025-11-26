# Coding Standards Reference

> **Source:** [docs/standards/DEVELOPMENT.md](../../../../docs/standards/DEVELOPMENT.md)
> **Purpose:** Quick reference for coding standards, validation, and testing

---

## Core Philosophy

1. **Readability First:** Optimize for the next reader. Explicit > Clever.
2. **Single Responsibility:** Each module/class/function does one thing well.
3. **DRY:** Extract duplication into well-named functions.
4. **KISS:** Avoid speculative abstractions (YAGNI).
5. **Fail Loudly:** Validate inputs, handle errors at boundaries.

---

## Language Baselines

### TypeScript / JavaScript
| Aspect | Standard |
|--------|----------|
| Style | Strict mode, ES modules, `async/await` |
| Lint | ESLint |
| Format | Prettier |
| Testing | Vitest (preferred) or Jest |
| **Validation** | **Zod (mandatory for all external inputs)** |

### Python
| Aspect | Standard |
|--------|----------|
| Style | PEP 8, Type hints (PEP 484) |
| Lint | Ruff |
| Format | Black |
| Types | MyPy |
| Testing | pytest |
| **Validation** | **Pydantic (mandatory for all data models)** |

### Shell (bash)
| Aspect | Standard |
|--------|----------|
| Style | `set -Eeuo pipefail`, quote variables |
| Lint | ShellCheck |

---

## Naming Conventions

| Element | TypeScript | Python |
|---------|------------|--------|
| Variables/Functions | `camelCase` | `snake_case` |
| Classes | `PascalCase` | `PascalCase` |
| Constants | `UPPER_CASE` | `UPPER_CASE` |
| Files | `camelCase.ts` | `snake_case.py` |
| Docs | `kebab-case.md` | `kebab-case.md` |

**Naming Best Practices:**
- `fetchUser` > `getData` (be specific)
- `timeoutMs` > `timeout` (include units)

---

## Data Validation Standards

### Python: Pydantic (Mandatory)

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(ge=0)
    email: str = Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
```

**Use For:** Agent models, API request/response, Config

### TypeScript: Zod (Mandatory)

```typescript
import { z } from 'zod';

const UserSchema = z.object({
  name: z.string().min(1),
  age: z.number().min(0),
  email: z.string().email()
});

type User = z.infer<typeof UserSchema>;
```

**Use For:** MCP Tools, API inputs, Tool parameters

---

## Testing Pyramid

```
        /\
       /E2E\        5%  - Full system flows
      /-----\
     /Integr-\     15%  - Real DB/API interactions
    / ation   \
   /-----------\
  /   Unit      \  80%  - Fast, isolated, mocked
 /_______________\
```

### Testing Principles
- **AAA:** Arrange, Act, Assert
- **Deterministic:** No flaky tests allowed
- **Coverage:** Aim for 80%+, but value quality over quantity

---

## Error Handling

1. **Throw Domain Errors:** Don't return `null`. Throw `UserNotFoundError`.
2. **Context:** Include IDs and actionable messages.
3. **Log:** Log at appropriate levels (ERROR vs WARN).

```python
# Bad
return None

# Good
raise UserNotFoundError(f"User {user_id} not found in database")
```

---

## Git Workflow

### Branching
- **Trunk-Based:** Short-lived feature branches
- **Naming:** `feat/login`, `fix/api-timeout`

### Commits (Conventional Commits)
```
feat(auth): add login endpoint
fix(api): handle timeout gracefully
chore: update dependencies
docs: add API documentation
refactor: extract user validation
test: add unit tests for auth
```

### Pull Requests
- **Author:** Contextual description, self-review first
- **Reviewer:** Focus on correctness, clarity, security

---

## Linting/Tooling Matrix

| Language | Lint | Format | Type Check |
|----------|------|--------|------------|
| **TS/JS** | ESLint | Prettier | `tsc` |
| **Python** | Ruff | Black | MyPy |
| **Shell** | ShellCheck | shfmt | - |
| **Markdown** | markdownlint | Prettier | - |
| **YAML** | yamllint | Prettier | - |

**Policy:** CI fails on any lint error. No warnings allowed in main.

---

## Progressive Hint Integration

During the **IMPLEMENT** stage, you'll be asked:

> "Apply coding standards (lint/format/validation)?"

If you answer **Yes**, ensure:

- [ ] **Validation:** Zod (TS) or Pydantic (Python) for all inputs
- [ ] **Linting:** ESLint (TS) or Ruff (Python) configured
- [ ] **Formatting:** Prettier (TS) or Black (Python) configured
- [ ] **Type Checking:** tsc (TS) or MyPy (Python) passing
- [ ] **Naming:** Following conventions for language

During the **TEST** stage, you'll be asked:

> "Apply testing pyramid (80/15/5) standards?"

If you answer **Yes**, ensure:

- [ ] **Unit Tests:** 80% coverage target, isolated, mocked
- [ ] **Integration Tests:** 15% coverage, real dependencies
- [ ] **E2E Tests:** 5% coverage, full workflows
- [ ] **No Flaky Tests:** Deterministic results

---

## Full Documentation

For complete development standards, see:
**[docs/standards/DEVELOPMENT.md](../../../../docs/standards/DEVELOPMENT.md)**
