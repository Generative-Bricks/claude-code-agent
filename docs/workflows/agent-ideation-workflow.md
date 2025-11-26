# Agent Ideation Workflow

**Purpose:** A structured, step-by-step process for transforming an agent idea into a production-ready implementation.

**Philosophy:** Break everything into extremely manageable tasks. Excellence doesn't mean complexity - it means doing simple things extremely well.

---

## Overview

```
BRAINSTORM → DESIGN → IMPLEMENT → TEST → DOCUMENT → ITERATE
```

Each stage has clear inputs, activities, and outputs. Follow this workflow to ensure consistent, high-quality agent development.

---

## Stage 1: BRAINSTORM 🧠

**Goal:** Define the problem space and success criteria

### Activities

1. **Identify the Use Case**
   - What problem does this agent solve?
   - Who are the users?
   - What makes this valuable?

2. **Define Success Criteria**
   - What does "done" look like?
   - How will you measure success?
   - What are the edge cases?

3. **Research Existing Solutions**
   - Check `docs/comparisons/agent-comparison-matrix.md` for similar agents
   - Review `docs/catalogs/common-tools-catalog.md` for reusable patterns
   - Search `docs/memory/memory.jsonl` for relevant learnings

4. **Choose SDK/Framework**
   - Claude SDK - Best for Anthropic Claude integration
   - Strands Agents - Best for model-agnostic approaches
   - LangGraph - Best for complex stateful workflows
   - Others based on specific needs

5. **Choose Language**
   - TypeScript - Preferred for type safety and Bun integration
   - Python - Good for data science and ML integrations
   - Consider team expertise and ecosystem

### Outputs

- [ ] One-sentence problem statement
- [ ] Clear success criteria (3-5 measurable goals)
- [ ] Selected SDK/framework and language
- [ ] List of potential tools needed

### Example

**Problem Statement:** "Financial advisors need help analyzing annuity products for retirement planning."

**Success Criteria:**
- Agent can evaluate client suitability for annuities
- Agent can compare different annuity types
- Agent can calculate income projections
- Agent can provide tax implications analysis
- Agent can recommend optimal portfolio allocation

**SDK/Language:** Claude SDK + TypeScript (type safety + production-grade)

---

## Stage 2: DESIGN 🎨

**Goal:** Create a clear architectural blueprint before writing code

### Activities

1. **Define Agent Persona & Role**
   - What expertise does the agent have?
   - What is its communication style?
   - What are its limitations?

2. **Design Tool Set**
   - List all tools needed (be minimal - start with 3-5)
   - Define input/output schema for each tool
   - Identify reusable tools from catalog
   - Keep tools focused (one purpose per tool)

3. **Plan Workflow**
   - What are the conversation stages?
   - How does the agent progress through stages?
   - What information is collected at each stage?
   - Example: Discovery → Assessment → Analysis → Recommendation → Documentation

4. **Consider Subagents**
   - Do you need specialized subagents?
   - What tasks require deep reasoning (Sonnet)?
   - What tasks can be optimized quickly (Haiku)?
   - Can subagents run in parallel?

5. **Design Data Model**
   - What data structures are needed?
   - How will state be managed?
   - Where will data come from (APIs, databases, mock data)?
   - Plan for type safety (Zod schemas, TypeScript interfaces)

6. **Plan MCP Integration**
   - Which MCP servers will the agent use?
   - How will the agent fetch documentation (Context7)?
   - Any custom MCP tools needed?

### Outputs

- [ ] Agent persona and role description
- [ ] Tool list with input/output schemas
- [ ] Workflow diagram or stage description
- [ ] Subagent plan (if needed)
- [ ] Data model design
- [ ] MCP integration plan

### Design Checklist

- [ ] Can I explain the agent's purpose in 1-2 sentences?
- [ ] Are all tools necessary? (Remove "nice to have" tools)
- [ ] Is the workflow clear and linear?
- [ ] Have I kept it simple?

### Example (Financial Advisor Agent)

**Persona:** "Expert financial advisor specializing in annuity products and retirement income planning"

**Tools:**
1. `analyze_annuity_suitability` - Input: client profile, Output: suitability score
2. `calculate_annuity_payout` - Input: annuity details, Output: income projections
3. `compare_annuity_types` - Input: annuity types, Output: comparison matrix
4. `assess_portfolio_allocation` - Input: portfolio, Output: allocation recommendations
5. `evaluate_tax_implications` - Input: scenario, Output: tax analysis
6. `fetch_annuity_rates` - Input: criteria, Output: current rates

**Workflow:** Discovery → Assessment → Analysis → Recommendation → Documentation

**Subagents:**
- Sonnet subagent for deep suitability analysis
- Haiku subagent for portfolio optimization calculations

---

## Stage 3: IMPLEMENT ⚙️

**Goal:** Build the agent incrementally with production-quality code

### Activities

1. **Set Up Project Structure**
   ```bash
   # Copy appropriate template
   cp -r templates/claude-sdk-typescript agents/claude-sdk/typescript/my-agent
   cd agents/claude-sdk/typescript/my-agent

   # Install dependencies
   bun install  # or uv venv && uv pip install for Python

   # Configure environment
   cp .env.example .env
   # Edit .env with API keys
   ```

2. **Build Tools First**
   - Start with one tool at a time
   - Implement input validation (Zod schemas for TypeScript)
   - Add error handling from the start
   - Test each tool individually
   - Document the tool's purpose and usage

3. **Implement Agent Logic**
   - Set up agent configuration
   - Define system prompt and persona
   - Implement tool handlers
   - Add workflow stage logic
   - Keep it simple - no premature optimization

4. **Add Subagents (if needed)**
   - Create subagent configurations
   - Define clear responsibilities
   - Implement communication patterns
   - Test subagent integration

5. **Implement State Management**
   - Define state structure
   - Add state persistence if needed
   - Keep state minimal and clear

6. **Add Mock Data (optional)**
   - Create realistic mock data for testing
   - Structure identically to expected API responses
   - Document where to replace with real APIs

### Implementation Best Practices

**Keep Functions Small:**
```typescript
// ✅ Good - focused and clear
function calculateAnnuityPayout(amount: number, rate: number): number {
  return amount * (rate / 100);
}

// ❌ Bad - doing too much
function calculateEverything(data: any): any {
  // 100 lines of mixed calculations
}
```

**Use Type Safety:**
```typescript
// ✅ Good - Zod schema validation
const AnnuityInputSchema = z.object({
  amount: z.number().positive(),
  rate: z.number().min(0).max(100),
  term: z.number().positive().int()
});

// ❌ Bad - no validation
function analyze(input: any) { ... }
```

**Handle Errors Properly:**
```typescript
// ✅ Good - specific error handling
try {
  const result = await fetchRates();
  return result;
} catch (error) {
  if (error instanceof NetworkError) {
    return { error: "Network unavailable. Please try again." };
  }
  throw error;
}

// ❌ Bad - silent failures
try {
  const result = await fetchRates();
} catch {
  return null;  // No context about what failed
}
```

### Outputs

- [ ] Working agent implementation
- [ ] All tools implemented with validation
- [ ] Error handling in place
- [ ] Type-safe code (TypeScript) or type hints (Python)
- [ ] Code follows naming conventions

---

## Stage 4: TEST 🧪

**Goal:** Verify agent behavior, performance, and edge cases

### Activities

1. **Unit Test Tools**
   - Test each tool individually
   - Verify input validation works
   - Test error conditions
   - Ensure outputs match schema

2. **Integration Test Agent**
   - Run complete workflows
   - Test multi-turn conversations
   - Verify subagent integration
   - Test state management

3. **Test Edge Cases**
   - Invalid inputs
   - Missing data
   - API failures
   - Timeout scenarios
   - Unexpected user inputs

4. **Performance Test**
   - Measure response times
   - Check token usage
   - Verify subagent efficiency
   - Identify bottlenecks

5. **Manual QA**
   - Run realistic scenarios
   - Test user experience
   - Verify output quality
   - Check conversation flow

### Testing Checklist

- [ ] All tools handle errors gracefully
- [ ] Agent responds appropriately to invalid inputs
- [ ] Workflow progresses logically
- [ ] Subagents (if used) work correctly
- [ ] Performance is acceptable
- [ ] Edge cases are handled

### Example Test Scenarios

**Financial Advisor Agent:**
- Client with no retirement savings (edge case)
- Client with complex tax situation
- Request for annuity types not in database
- Multiple recommendation requests in one conversation
- Invalid age or income data

---

## Stage 5: DOCUMENT 📝

**Goal:** Create comprehensive documentation for future reference

### Activities

1. **Create Agent CLAUDE.md**
   - Project overview and purpose
   - Directory structure
   - Setup instructions
   - Tool descriptions
   - Workflow explanation
   - Example usage
   - Known limitations

2. **Update Root Documentation**
   - Add agent to root CLAUDE.md "Existing Agents" section
   - Create entry in `docs/comparisons/agent-comparison-matrix.md`
   - Add reusable patterns to `docs/catalogs/common-tools-catalog.md`
   - Document MCP usage in `docs/catalogs/mcp-integration-patterns.md`

3. **Update Memory System**
   - Add agent entity to `docs/memory/memory.jsonl`
   - Document architectural decisions
   - Capture patterns discovered
   - Record learnings and gotchas

4. **Write README.md**
   - Quick start guide
   - Installation instructions
   - Usage examples
   - Configuration options

### Documentation Standards

- Keep it concise and purposeful
- Include working code examples
- Document the "why" not just the "what"
- Use clear markdown formatting
- Keep documentation current

### Outputs

- [ ] Comprehensive CLAUDE.md in agent directory
- [ ] Updated root CLAUDE.md
- [ ] Agent comparison matrix entry
- [ ] Memory system updated
- [ ] README.md with quick start

---

## Stage 6: ITERATE 🔄

**Goal:** Improve based on usage and feedback

### Activities

1. **Collect Feedback**
   - User feedback
   - Performance metrics
   - Error logs
   - Usage patterns

2. **Identify Improvements**
   - What worked well?
   - What didn't work?
   - What's missing?
   - What's confusing?

3. **Make Incremental Updates**
   - Fix bugs found
   - Add missing tools (if needed)
   - Improve prompts
   - Optimize performance
   - Refactor for clarity

4. **Update Documentation**
   - Document changes
   - Update version numbers
   - Add new learnings to memory
   - Update comparison matrix

5. **Share Learnings**
   - Update common tools catalog with new patterns
   - Document gotchas in memory system
   - Share insights with team

### Iteration Principles

- Make small, focused changes
- Test after each change
- Document improvements
- Don't over-engineer based on hypothetical needs

---

## Success Indicators

You've successfully completed the workflow when:

✅ The agent solves the stated problem effectively
✅ Code is simple, readable, and maintainable
✅ All edge cases are handled gracefully
✅ Documentation is comprehensive and current
✅ Patterns are captured for reuse
✅ Memory system is updated with learnings
✅ The agent can be easily understood by others

---

## Anti-Patterns to Avoid

🚩 **Skipping the Design Phase**
- Don't jump straight to coding
- Take time to think through architecture
- Design saves time in implementation

🚩 **Building All Tools at Once**
- Build and test incrementally
- One tool at a time
- Verify before moving forward

🚩 **Postponing Documentation**
- Document as you build
- Don't leave it for "later"
- Future you will thank present you

🚩 **Over-Engineering**
- Start simple
- Add complexity only when needed
- YAGNI (You Aren't Gonna Need It)

🚩 **Ignoring Edge Cases**
- Think about failure scenarios
- Handle errors from the start
- Test unusual inputs

---

## Quick Reference

| Stage | Key Question | Output |
|-------|-------------|---------|
| **Brainstorm** | What problem am I solving? | Problem statement + success criteria |
| **Design** | How will I solve it? | Architecture blueprint |
| **Implement** | Build it simply | Working agent code |
| **Test** | Does it work? | Verified behavior |
| **Document** | How do I use it? | Comprehensive docs |
| **Iterate** | How can I improve? | Refined implementation |

---

**Remember:** Excellence is doing simple things extremely well. Keep each stage focused, manageable, and production-quality from the start.

---

*Part of the claude-code-agent repository*
*See root CLAUDE.md for repository structure and guidelines*
