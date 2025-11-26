# Agent Builder Quality Checklists

This document provides comprehensive quality checklists for each stage of agent development. Use these checklists to ensure your agent meets production standards before moving to the next stage.

## Table of Contents

1. [Before Starting Checklist](#before-starting-checklist)
2. [Design Complete Checklist](#design-complete-checklist)
3. [Implementation Ready Checklist](#implementation-ready-checklist)
4. [Code Quality Checklist](#code-quality-checklist)
5. [Testing Complete Checklist](#testing-complete-checklist)
6. [Documentation Complete Checklist](#documentation-complete-checklist)
7. [Production Ready Checklist](#production-ready-checklist)
8. [Deployment Checklist](#deployment-checklist) (Stage 6)
9. [Observability Checklist](#observability-checklist) (Stage 7)
10. [Evaluation Checklist](#evaluation-checklist) (Stage 8)
11. [Iteration Checklist](#iteration-checklist) (Stage 9)

---

## Before Starting Checklist

**Purpose**: Ensure you have a clear understanding before writing any code

### Problem Definition

- [ ] Can explain the agent's purpose in 1-2 sentences
- [ ] Identified specific problem being solved
- [ ] Know who the primary users are
- [ ] Understand what makes this valuable (time savings, cost reduction, etc.)

### Success Criteria

- [ ] Defined 3-5 measurable success criteria
- [ ] Each criterion has a clear success threshold
- [ ] Identified key edge cases that must be handled
- [ ] Documented acceptable limitations

### Research

- [ ] Checked for similar existing agents in comparison matrix
- [ ] Reviewed common tools catalog for reusable patterns
- [ ] Searched memory system for relevant learnings
- [ ] Confirmed this is the simplest solution that could work

### Technical Decisions

- [ ] SDK selected with clear rationale
- [ ] Language selected with clear rationale
- [ ] Complexity level estimated (Low/Medium/High)
- [ ] Tool count estimated (start with 3-5)
- [ ] Subagent approach decided (0-2 for most agents)

### Time Estimation

- [ ] Realistic time estimate based on complexity
  - Low: 4-8 hours
  - Medium: 10-20 hours
  - High: 30-60+ hours

---

## Design Complete Checklist

**Purpose**: Ensure architectural design is thorough before implementation

### Agent Persona

- [ ] Agent role clearly defined
- [ ] Expertise areas documented
- [ ] Communication style defined
- [ ] Limitations explicitly stated
- [ ] Safety constraints documented (what agent will never do)

### Tool Design

- [ ] 3-5 tools designed (start small, add more if needed)
- [ ] Each tool has single, clear responsibility
- [ ] Tool names follow verb + noun pattern
- [ ] Input parameters defined with types
- [ ] Output structure defined with types
- [ ] Validation schema planned (Zod/Pydantic)
- [ ] Error conditions identified
- [ ] Example usage provided for each tool

### Workflow Design

- [ ] Workflow stages clearly defined
- [ ] Stage progression logic documented
- [ ] Information collected at each stage identified
- [ ] Error handling strategy for each stage
- [ ] Completion criteria defined

### Data Model

- [ ] Core data entities identified
- [ ] Data relationships mapped
- [ ] Validation requirements defined
- [ ] State management approach decided
- [ ] Type safety strategy planned (Zod/Pydantic)

### Pattern Selection

- [ ] Validation pattern selected (Zod/Pydantic) ✅ Required
- [ ] Subagent pattern selected (if applicable)
- [ ] Data pattern selected (Mock Data First recommended)
- [ ] Architecture pattern selected (Service-Based for medium+ complexity)
- [ ] Scoring pattern selected (if applicable)
- [ ] Each pattern selection justified

### Subagent Plan (if applicable)

- [ ] Subagent responsibilities clearly defined
- [ ] Model selection justified (Sonnet vs Haiku)
- [ ] Communication pattern defined
- [ ] Context passing strategy planned
- [ ] Success criteria for subagent tasks defined

### Integration Plan

- [ ] MCP servers identified (if needed)
- [ ] External APIs documented (if needed)
- [ ] Mock data approach defined
- [ ] Real data integration points marked

### Documentation

- [ ] Design decisions documented with rationale
- [ ] Known limitations identified
- [ ] Edge cases documented
- [ ] Future enhancement ideas captured

---

## Implementation Ready Checklist

**Purpose**: Verify you're ready to start coding

### Project Structure

- [ ] Template selected and copied
- [ ] Directories created
- [ ] Package manager initialized (npm/Bun for TS, uv for Python)
- [ ] Dependencies identified

### Environment

- [ ] `.env.example` created with required keys
- [ ] `.gitignore` configured
- [ ] Git repository initialized
- [ ] Editor/IDE configured

### First Tool Ready

- [ ] Simplest tool identified to implement first
- [ ] Input schema designed
- [ ] Output schema designed
- [ ] Mock data prepared (if needed)
- [ ] Test cases planned

---

## Code Quality Checklist

**Purpose**: Ensure code meets production standards

### Type Safety

#### TypeScript
- [ ] Strict mode enabled in `tsconfig.json`
- [ ] No `any` types used
- [ ] All function parameters typed
- [ ] All return types explicit
- [ ] Zod schemas for all tool inputs

#### Python
- [ ] Type hints on all functions
- [ ] Pydantic models for all data
- [ ] No `# type: ignore` without justification
- [ ] Mypy or pyright passing

### Validation

- [ ] All tool inputs validated (Zod/Pydantic)
- [ ] Validation errors have clear messages
- [ ] Invalid inputs handled gracefully
- [ ] Edge cases in validation considered

### Error Handling

- [ ] Try-catch blocks around all external calls
- [ ] Specific error handling (not generic `catch (error)`)
- [ ] Error messages are actionable
- [ ] Errors don't expose sensitive information
- [ ] Graceful degradation on failures

### Naming Conventions

- [ ] Functions use descriptive verb + noun names
- [ ] Variables are self-documenting
- [ ] Constants in UPPER_SNAKE_CASE
- [ ] File names follow language conventions:
  - TypeScript: camelCase.ts
  - Python: snake_case.py
  - Docs: kebab-case.md

### Code Organization

- [ ] One purpose per file
- [ ] Functions are small and focused (<50 lines)
- [ ] Duplication eliminated (DRY principle)
- [ ] Clear separation of concerns
- [ ] Imports organized and clean

### Comments

- [ ] Comments explain "why" not "what"
- [ ] Complex logic has explanatory comments
- [ ] Business rules documented
- [ ] Edge cases explained
- [ ] TODOs marked for future work

### Mock Data

- [ ] Structured identically to production API
- [ ] Includes success cases
- [ ] Includes edge cases
- [ ] Clear TODO comments for production replacement
- [ ] Both mock and real supported via env config

---

## Testing Complete Checklist

**Purpose**: Verify agent behavior is correct

### Unit Tests (Tools)

- [ ] All tools have at least one happy path test
- [ ] Invalid input tests for each tool
- [ ] Edge case tests for critical tools
- [ ] Error condition tests
- [ ] Optional parameter tests
- [ ] Test coverage >60% for production agents

### Integration Tests (Workflows)

- [ ] Happy path workflow test
- [ ] Multi-turn conversation test
- [ ] Subagent integration test (if applicable)
- [ ] State management test (if applicable)
- [ ] End-to-end workflow test

### Edge Case Tests

- [ ] Missing data scenarios tested
- [ ] Invalid type inputs tested
- [ ] Extreme values tested (very large, very small, zero, negative)
- [ ] Empty arrays/objects tested
- [ ] Null/undefined handling tested
- [ ] Special characters in strings tested

### Performance Tests

- [ ] Response time per tool measured (<1s for simple, <5s for complex)
- [ ] End-to-end workflow time measured (<2min target)
- [ ] Token usage measured
- [ ] Memory usage acceptable
- [ ] Parallel execution verified (if applicable)

### Manual QA

- [ ] Happy path workflow works end-to-end
- [ ] Agent provides clear explanations
- [ ] Error messages are helpful and actionable
- [ ] Agent asks for clarification when needed
- [ ] Output format is correct
- [ ] Agent stays within defined scope
- [ ] Agent respects limitations
- [ ] Conversation flow feels natural

---

## Documentation Complete Checklist

**Purpose**: Ensure comprehensive documentation exists

### Agent CLAUDE.md

- [ ] Purpose clearly stated (1-2 sentences)
- [ ] Framework and version documented
- [ ] Language and version documented
- [ ] Status indicated (Development/Production-Ready/version)
- [ ] Overview (2-3 paragraphs)
- [ ] Complete directory structure
- [ ] Features list
- [ ] Tool descriptions with examples
- [ ] Workflow explanation
- [ ] Setup instructions (step-by-step)
- [ ] Usage examples
- [ ] Testing approach documented
- [ ] Known limitations documented
- [ ] Key architectural decisions documented with rationale
- [ ] Future enhancements noted

### README.md

- [ ] Brief description (1-2 paragraphs)
- [ ] Quick start section with commands
- [ ] Installation steps
- [ ] Configuration steps
- [ ] Basic usage example
- [ ] Link to comprehensive CLAUDE.md
- [ ] License information (if applicable)

### Inline Documentation

- [ ] All functions have docstrings/JSDoc comments
- [ ] Complex logic explained with inline comments
- [ ] Business rules documented
- [ ] Edge cases explained
- [ ] TODOs marked for future work

### Supporting Documentation

- [ ] Comparison matrix entry prepared (if applicable)
- [ ] Memory system entries prepared (entities, relations, observations)
- [ ] Tool catalog contributions prepared (reusable patterns)
- [ ] MCP integration patterns documented (if applicable)

### Code Comments

- [ ] Comments up to date (no outdated comments)
- [ ] Complex algorithms explained
- [ ] Why, not what (avoid obvious comments)
- [ ] Business logic rationale documented

---

## Production Ready Checklist

**Purpose**: Final verification before deployment

### Functionality

- [ ] All tools work correctly
- [ ] All workflows complete successfully
- [ ] Subagents function correctly (if applicable)
- [ ] State management works (if applicable)
- [ ] Error handling prevents crashes
- [ ] Graceful degradation on failures

### Code Quality

- [ ] Type safety throughout (no `any` in TS, type hints in Python)
- [ ] Input validation on all tools (Zod/Pydantic)
- [ ] Error handling comprehensive
- [ ] Naming conventions followed consistently
- [ ] Code is readable and maintainable
- [ ] No hardcoded secrets or credentials
- [ ] Environment variables used for config

### Testing

- [ ] Unit tests passing (critical tools covered)
- [ ] Integration tests passing (workflows covered)
- [ ] Edge cases handled
- [ ] Performance acceptable
  - Tool responses: <1s (simple) or <5s (complex)
  - Workflows: <2 minutes
- [ ] Manual QA scenarios verified

### Documentation

- [ ] Comprehensive CLAUDE.md in agent directory
- [ ] README.md with quick start
- [ ] Root CLAUDE.md updated with agent entry
- [ ] Comparison matrix entry added (if applicable)
- [ ] Memory system updated with learnings
- [ ] Tool catalog updated with patterns (if applicable)

### Security

- [ ] No secrets in code
- [ ] Environment variables for sensitive config
- [ ] Input validation prevents injection
- [ ] Error messages don't leak sensitive info
- [ ] API keys properly secured

### Deployment

- [ ] Dependencies documented
- [ ] Installation tested on clean environment
- [ ] Environment setup documented
- [ ] Deployment instructions clear
- [ ] Rollback plan exists (if applicable)

### User Experience

- [ ] Clear, helpful responses
- [ ] Actionable error messages
- [ ] Asks for clarification when needed
- [ ] Stays within defined scope
- [ ] Respects limitations
- [ ] Natural conversation flow

### Compliance (if applicable)

- [ ] Regulatory requirements met
- [ ] Data privacy respected
- [ ] User consent obtained
- [ ] Audit trail exists (if needed)

---

## Deployment Checklist

**Purpose**: Ensure safe and controlled production release (Stage 6: DEPLOY)

### Deployment Gates

- [ ] Offline evaluations passing (benchmarks, safety tests)
- [ ] Red team review complete (if applicable)
- [ ] Staging environment tested
- [ ] Production readiness confirmed

### Rollout Strategy

- [ ] Rollout plan defined:
  - [ ] Canary (1%) - Initial exposure
  - [ ] Limited (10%) - Early validation
  - [ ] Gradual (50%) - Wider testing
  - [ ] Full (100%) - Complete rollout
- [ ] Success metrics for each phase defined
- [ ] Rollback triggers identified

### Rollback Planning

- [ ] Automatic rollback triggers configured:
  - [ ] Error rate threshold (e.g., >5%)
  - [ ] Latency threshold (e.g., p99 >10s)
  - [ ] Success rate threshold (e.g., <90%)
- [ ] Manual rollback procedure documented
- [ ] Rollback tested successfully

### Agent Identity (Enterprise)

- [ ] SPIFFE ID registered (if applicable)
- [ ] Agent added to central inventory
- [ ] Ownership and team documented
- [ ] Escalation contacts defined

### Security Hardening

- [ ] Input validation active
- [ ] Output sanitization configured
- [ ] Rate limiting configured
- [ ] Audit logging enabled
- [ ] Secrets management verified

---

## Observability Checklist

**Purpose**: Ensure comprehensive production monitoring (Stage 7: OBSERVE)

### Tracing Setup

- [ ] OpenTelemetry configured
- [ ] Root span created per request
- [ ] Required attributes set:
  - [ ] `gen_ai.system` (e.g., "claude", "openai")
  - [ ] `gen_ai.request.model`
  - [ ] `gen_ai.response.model`
  - [ ] `gen_ai.usage.input_tokens`
  - [ ] `gen_ai.usage.output_tokens`
- [ ] Tool calls captured as child spans
- [ ] Subagent calls captured as child spans

### Metrics Configuration

- [ ] Latency metrics enabled:
  - [ ] p50, p90, p95, p99 latency
  - [ ] Time-to-first-token (streaming)
- [ ] Token usage tracked:
  - [ ] Input tokens per request
  - [ ] Output tokens per request
  - [ ] Total tokens per session
- [ ] Cost metrics calculated (if applicable)
- [ ] Error rate metrics enabled

### Logging Standards

- [ ] Structured JSON logging configured
- [ ] Log levels appropriate:
  - [ ] ERROR: Failures requiring attention
  - [ ] WARN: Degraded but functional
  - [ ] INFO: Normal operation milestones
  - [ ] DEBUG: Detailed troubleshooting
- [ ] PII sanitization active (no user data in logs)
- [ ] Trace correlation IDs included

### Alerting

- [ ] Error rate alerts configured
- [ ] Latency alerts configured
- [ ] Availability alerts configured
- [ ] Alert escalation path defined
- [ ] On-call rotation established (if applicable)

### Dashboards

- [ ] Health dashboard created:
  - [ ] Request volume
  - [ ] Error rate
  - [ ] Latency percentiles
  - [ ] Token usage
- [ ] Business metrics dashboard (if applicable)

---

## Evaluation Checklist

**Purpose**: Assess agent performance comprehensively (Stage 8: EVALUATE)

### Offline Evaluation

- [ ] Benchmark suite created:
  - [ ] Task-specific test cases
  - [ ] Expected outcomes defined
  - [ ] Pass/fail criteria established
- [ ] RAG metrics (if applicable):
  - [ ] Context relevance
  - [ ] Answer faithfulness
  - [ ] Answer relevance
- [ ] Safety testing:
  - [ ] Jailbreak resistance
  - [ ] Harmful content detection
  - [ ] PII handling verification

### Online Evaluation

- [ ] A/B testing framework (if applicable):
  - [ ] Control vs treatment defined
  - [ ] Sample size calculated
  - [ ] Duration planned
- [ ] Shadow traffic testing (if applicable)
- [ ] Canary analysis metrics defined

### Human Feedback

- [ ] In-product feedback mechanism:
  - [ ] Thumbs up/down
  - [ ] Optional text feedback
  - [ ] Rating scale (if needed)
- [ ] Review queue process (for flagged outputs)
- [ ] Feedback storage and analysis pipeline

### Success Metrics

- [ ] Primary metrics defined:
  - [ ] Task completion rate
  - [ ] User acceptance rate
  - [ ] Error rate
- [ ] Secondary metrics defined:
  - [ ] Session length
  - [ ] Return user rate
  - [ ] Tool usage patterns

### Feedback Loop

- [ ] Feedback → Eval case pipeline established
- [ ] Regular review cadence defined
- [ ] Improvement tracking mechanism

---

## Iteration Checklist

**Purpose**: Ensure continuous improvement process (Stage 9: ITERATE)

### Feedback Collection

- [ ] User feedback aggregated
- [ ] Error logs reviewed
- [ ] Performance metrics analyzed
- [ ] Usage patterns identified

### Improvement Identification

- [ ] What worked well documented
- [ ] What didn't work documented
- [ ] Missing features identified
- [ ] Performance bottlenecks identified

### Incremental Updates

- [ ] Bug fixes prioritized
- [ ] New tools planned (if needed)
- [ ] Prompt improvements identified
- [ ] Configuration tuning planned

### Documentation Updates

- [ ] CLAUDE.md updated with learnings
- [ ] README.md current
- [ ] API documentation current
- [ ] Known issues documented

### Learning Capture

- [ ] Memory system updated with learnings
- [ ] Patterns catalog updated (if applicable)
- [ ] Comparison matrix updated
- [ ] Team knowledge shared

### Feedback Loop Closure

- [ ] Feedback converted to eval cases
- [ ] Eval cases added to benchmark suite
- [ ] Regression tests created
- [ ] Improvement verified

---

## Quality Gates

### Gate 1: Before Design → Implementation

**Must Pass**:
- [ ] All items in "Before Starting Checklist"
- [ ] All items in "Design Complete Checklist"
- [ ] All items in "Implementation Ready Checklist"

**Decision**: Proceed to implementation or revisit design?

---

### Gate 2: Implementation → Testing

**Must Pass**:
- [ ] All items in "Code Quality Checklist"
- [ ] All tools implemented
- [ ] No compilation errors
- [ ] No obvious runtime errors

**Decision**: Proceed to testing or fix code issues?

---

### Gate 3: Testing → Documentation

**Must Pass**:
- [ ] All items in "Testing Complete Checklist"
- [ ] All tests passing
- [ ] Performance acceptable
- [ ] Manual QA successful

**Decision**: Proceed to documentation or fix test failures?

---

### Gate 4: Documentation → Production

**Must Pass**:
- [ ] All items in "Documentation Complete Checklist"
- [ ] All items in "Production Ready Checklist"
- [ ] Final review complete

**Decision**: Deploy to production or iterate?

---

## Quick Reference: Minimum Viable Quality

For rapid prototyping, this is the **absolute minimum** to consider an agent "functional":

### Minimum Viable Agent
- [ ] Agent purpose clear (1 sentence)
- [ ] 1-3 tools working
- [ ] Input validation (Zod/Pydantic)
- [ ] Basic error handling
- [ ] Happy path tested manually
- [ ] README.md with setup and usage

**Time**: 2-4 hours

**Use for**: Prototypes, demos, internal experiments

---

## Production-Grade Quality

For production deployment, meet **all** items in:
- [ ] Code Quality Checklist
- [ ] Testing Complete Checklist
- [ ] Documentation Complete Checklist
- [ ] Production Ready Checklist

**Time**: Additional 4-8 hours beyond prototype

**Use for**: Customer-facing agents, mission-critical systems

---

## Checklist Usage Guide

### During Development

**1. Before Starting**: Print "Before Starting Checklist" and verify all items

**2. After Design**: Print "Design Complete Checklist" and verify all items

**3. During Implementation**: Reference "Code Quality Checklist" continuously

**4. After Implementation**: Print "Testing Complete Checklist" and verify all items

**5. Before Documentation**: Ensure all tests passing

**6. After Documentation**: Print "Documentation Complete Checklist" and verify all items

**7. Before Production**: Print "Production Ready Checklist" and verify **every single item**

### As Team Review

Use these checklists for peer reviews:

**Code Review**: Use "Code Quality Checklist"

**Testing Review**: Use "Testing Complete Checklist"

**Documentation Review**: Use "Documentation Complete Checklist"

**Production Review**: Use "Production Ready Checklist"

---

## Common Quality Issues and Solutions

### Issue: Type Safety

**Problem**: Using `any` types or missing type hints

**Solution**:
- TypeScript: Enable strict mode, use Zod for runtime validation
- Python: Add type hints, use Pydantic for validation, run mypy

---

### Issue: Poor Error Handling

**Problem**: Generic catch blocks, unclear error messages

**Solution**:
- Specific error types
- Actionable error messages
- Graceful degradation
- User-friendly feedback

---

### Issue: Inadequate Testing

**Problem**: Only happy path tested, edge cases ignored

**Solution**:
- Test invalid inputs
- Test edge cases (null, empty, extreme values)
- Test error conditions
- Aim for 60%+ coverage

---

### Issue: Incomplete Documentation

**Problem**: Missing setup instructions, unclear usage

**Solution**:
- Complete CLAUDE.md with all sections
- README.md with quick start
- Inline comments for complex logic
- Examples for all tools

---

### Issue: Over-Engineering

**Problem**: Too complex for requirements

**Solution**:
- Simplify
- Remove unnecessary features
- Use proven patterns only when needed
- Start with 3-5 tools, not 15

---

## Summary

These checklists ensure:
- ✅ Clear problem definition before coding
- ✅ Thorough design before implementation
- ✅ Production-grade code quality
- ✅ Comprehensive testing
- ✅ Complete documentation
- ✅ Production readiness verification

Use them at each quality gate to maintain high standards throughout the agent development lifecycle.

**Remember**: Quality is not about perfection—it's about meeting requirements consistently and reliably.
