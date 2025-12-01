# Autonomous Coding Agent Demo

A minimal harness demonstrating long-running autonomous coding with the Claude Agent SDK. This demo implements a two-agent pattern (initializer + coding agent) that can build complete applications over multiple sessions.

Based on [Anthropic's autonomous-coding quickstart](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding), adapted with Playwright MCP for browser automation.

## Quick Start

```bash
# 1. Create virtual environment
uv venv
source .venv/Scripts/activate  # Windows Git Bash
# source .venv/bin/activate     # Linux/Mac

# 2. Install dependencies
uv pip install -r requirements.txt

# 3. Configure API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 4. Define your application (edit prompts/app_spec.txt)

# 5. Run the agent
python autonomous_agent_demo.py --project-dir ./my_app
```

## How It Works

### Two-Agent Pattern

1. **Initializer Agent (Session 1)**: Reads `app_spec.txt`, creates `feature_list.json` with 75 test cases, sets up project structure, and initializes git.

2. **Coding Agent (Sessions 2+)**: Picks up where the previous session left off, implements features one by one, and marks them as passing in `feature_list.json`.

### Session Management

- Each session runs with a fresh context window
- Progress is persisted via `feature_list.json` and git commits
- The agent auto-continues between sessions (3 second delay)
- Press `Ctrl+C` to pause; run the same command to resume

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--project-dir` | Directory for the project | `./autonomous_demo_project` |
| `--max-iterations` | Max agent iterations | Unlimited |
| `--model` | Claude model to use | `claude-sonnet-4-5-20250929` |

## Examples

```bash
# Start fresh project
python autonomous_agent_demo.py --project-dir ./my_app

# Limit iterations for testing
python autonomous_agent_demo.py --project-dir ./my_app --max-iterations 3

# Use a specific model
python autonomous_agent_demo.py --project-dir ./my_app --model claude-sonnet-4-5-20250929

# Continue existing project
python autonomous_agent_demo.py --project-dir ./my_app
```

## Timing Expectations

- **First session (initialization):** 5-15+ minutes generating test cases
- **Subsequent sessions:** 5-15 minutes each depending on complexity
- **Full app:** Many hours across multiple sessions for 75 features

## Security Model

Defense-in-depth approach (see `security.py`):

1. **OS-level Sandbox:** Bash commands run in isolated environment
2. **Filesystem Restrictions:** File operations restricted to project directory
3. **Bash Allowlist:** Only specific commands permitted

## Customization

### Change the Application

Edit `prompts/app_spec.txt` with your application specification.

### Adjust Feature Count

Edit `prompts/initializer_prompt.md` and change "75 features" to your desired count.

### Modify Allowed Commands

Edit `security.py` to add/remove commands from `ALLOWED_COMMANDS`.

## Troubleshooting

**"Appears to hang on first run"**: Normal. The initializer is generating detailed test cases. Watch for `[Tool: ...]` output.

**"Command blocked by security hook"**: The security system blocked a command not in the allowlist. Add it to `ALLOWED_COMMANDS` if needed.

**"API key not set"**: Ensure `ANTHROPIC_API_KEY` is set in your `.env` file.

## Files Reference

| File | Purpose |
|------|---------|
| `autonomous_agent_demo.py` | Main entry point |
| `agent.py` | Agent session logic |
| `client.py` | Claude SDK client configuration |
| `security.py` | Bash command allowlist |
| `progress.py` | Progress tracking |
| `prompts.py` | Prompt loading |
| `prompts/app_spec.txt` | Application specification |
| `prompts/initializer_prompt.md` | First session prompt |
| `prompts/coding_prompt.md` | Continuation prompt |

## See Also

- [CLAUDE.md](./CLAUDE.md) - Comprehensive documentation
- [Original quickstart](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)
