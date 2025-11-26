# Monitoring Tool Calls & Token Usage

This guide shows you how to see what tools were called and how many tokens were used during portfolio analysis.

---

## Quick Start

### 1. **Interactive Mode with Metrics** (Recommended)

Interactive mode automatically logs tool calls and token usage:

```bash
# Run analysis in interactive mode
python -m src.main --interactive --client CLT-2024-001 --portfolio conservative
```

**What you'll see:**
```
================================================================================
EXECUTION METRICS:
================================================================================
Token Usage:
  - Prompt tokens: 4,523
  - Completion tokens: 1,847
  - Total tokens: 6,370

Tools Called (2):
  1. run_comprehensive_analysis
  2. generate_client_report
================================================================================
```

### 2. **Verbose Mode**

Enable DEBUG-level logging for maximum detail:

```bash
python -m src.main --verbose --interactive --client CLT-2024-001 --portfolio conservative
```

This shows:
- All agent decisions
- Tool input/output
- Detailed execution flow
- Token counts at each step

### 3. **Check Log Files**

All execution details are saved to logs:

```bash
# View analysis logs
tail -f logs/portfolio_analysis.log

# Search for specific information
grep "Tool" logs/portfolio_analysis.log
grep "tokens" logs/portfolio_analysis.log
```

---

## Understanding Batch Mode

**Batch mode** (non-interactive) calls tools directly without the OpenAI Agents SDK Runner, so it doesn't track token usage automatically.

### Current Batch Mode Limitations:
- ❌ No automatic token tracking
- ❌ No tool call history
- ✅ Faster execution
- ✅ Suitable for automation

### To Track Metrics in Batch Mode:

Option 1: **Use Interactive Mode Instead**
```bash
python -m src.main --interactive --client CLT-2024-001 --portfolio conservative
```

Option 2: **Add Manual Tracking** (requires code changes)
- Wrap each tool call with logging
- Use tiktoken library to estimate tokens
- Track start/end times

---

## Detailed Metrics Breakdown

### Token Usage

**What the numbers mean:**
- **Prompt tokens**: Input sent to the model (your request + context)
- **Completion tokens**: Model's response (agent output)
- **Total tokens**: Sum of prompt + completion

**Cost calculation:**
```
For GPT-4o:
- Prompt: $5 / 1M tokens
- Completion: $15 / 1M tokens

Example (6,370 total tokens):
Cost = (4,523 × $5 / 1M) + (1,847 × $15 / 1M)
     = $0.023 + $0.028
     = $0.051 (~5 cents)
```

### Tool Calls

**Available tools in this system:**

**Portfolio Manager:**
1. `run_comprehensive_analysis` - Orchestrates all specialists
2. `generate_client_report` - Creates markdown reports

**Risk Analyst:**
3. `analyze_portfolio_risk` - Calculates volatility, VaR, beta

**Compliance Officer:**
4. `perform_compliance_check` - Validates regulatory requirements

**Performance Analyst:**
5. `analyze_portfolio_performance` - Calculates returns, Sharpe ratio

**Equity Specialist:**
6. `perform_equity_deep_dive` - Deep sector/valuation analysis

---

## Programmatic Access

### Inspect Result Object (Python)

```python
from agents import Runner
from src.agents.portfolio_manager import portfolio_manager_agent

# Run analysis
result = Runner.run(
    portfolio_manager_agent,
    input="Analyze portfolio for CLT-2024-001",
    session=session,
    context={"client_profile": client.model_dump(), "portfolio": portfolio.model_dump()}
)

# Check available attributes
print("Result attributes:", dir(result))

# Token usage
if hasattr(result, 'usage'):
    print(f"Total tokens: {result.usage.get('total_tokens', 0)}")
    print(f"Prompt tokens: {result.usage.get('prompt_tokens', 0)}")
    print(f"Completion tokens: {result.usage.get('completion_tokens', 0)}")

# Tool calls
if hasattr(result, 'messages'):
    for msg in result.messages:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tc in msg.tool_calls:
                print(f"Tool: {tc.function.name}")
                print(f"Args: {tc.function.arguments}")
```

### Inspect from Log Files (Shell)

```bash
# Count tool calls
grep -c "Tool" logs/portfolio_analysis.log

# Extract all tool names
grep "Running comprehensive analysis\|Generating report" logs/portfolio_analysis.log

# Find token usage
grep -i "token" logs/portfolio_analysis.log

# Get execution times
grep "Analysis complete" logs/portfolio_analysis.log
```

---

## Performance Benchmarks

### Expected Metrics (Conservative Portfolio, 9 Holdings)

**Interactive Mode:**
- Tokens: ~6,000-8,000 total
- Time: ~5-7 seconds
- Tools: 2 calls (analysis + report)

**Batch Mode:**
- Tokens: Not tracked (direct function calls)
- Time: ~3-5 seconds
- Tools: 2 function executions

**Parallel Specialist Execution:**
- Time savings: ~65% (5s vs 15s sequential)
- Tokens: Same as sequential (parallelism doesn't increase tokens)

---

## Troubleshooting

### "Can't see token usage in batch mode"
**Solution**: Use `--interactive` flag instead

### "Logs show incomplete information"
**Solution**: Add `--verbose` flag for DEBUG-level logging

### "Want to estimate costs before running"
**Estimation**:
- Small portfolio (5-10 holdings): ~5,000-8,000 tokens (~$0.05)
- Medium portfolio (10-20 holdings): ~8,000-12,000 tokens (~$0.08)
- Large portfolio (20+ holdings): ~12,000-20,000 tokens (~$0.12)

### "Need historical metrics"
**Solution**: Check `logs/portfolio_analysis.log` - all runs are logged

---

## Advanced: Custom Metrics Collection

If you need custom metrics tracking, create a wrapper:

```python
# custom_metrics.py
import time
from typing import Any, Dict

class MetricsCollector:
    def __init__(self):
        self.metrics: Dict[str, Any] = {
            "tool_calls": [],
            "start_time": None,
            "end_time": None,
            "tokens": {}
        }

    def start(self):
        self.metrics["start_time"] = time.time()

    def track_tool(self, tool_name: str, args: dict, result: Any):
        self.metrics["tool_calls"].append({
            "name": tool_name,
            "args": args,
            "result_type": type(result).__name__
        })

    def end(self, result):
        self.metrics["end_time"] = time.time()
        if hasattr(result, 'usage'):
            self.metrics["tokens"] = result.usage

    def summary(self):
        duration = self.metrics["end_time"] - self.metrics["start_time"]
        return {
            "duration_seconds": round(duration, 2),
            "tools_called": len(self.metrics["tool_calls"]),
            "total_tokens": self.metrics["tokens"].get("total_tokens", 0)
        }
```

---

## Summary

**To see tool calls and token usage:**

1. **Easiest**: Run with `--interactive` flag
2. **Most detail**: Add `--verbose` flag
3. **Historical**: Check `logs/portfolio_analysis.log`
4. **Programmatic**: Inspect `result.usage` and `result.messages`

**Key locations:**
- Live output: Terminal/console
- Detailed logs: `logs/portfolio_analysis.log`
- Metrics code: `src/main.py:292-318`
- Utility script: `inspect_result.py`

---

*Last updated: January 2025*
