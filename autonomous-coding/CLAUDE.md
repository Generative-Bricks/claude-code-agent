# Autonomous Coding Agent

**Purpose:** A minimal harness demonstrating long-running autonomous coding with the Claude Agent SDK. Implements a two-agent pattern (initializer + coding agent) that can build complete applications over multiple sessions.

**Framework:** Claude Code SDK | **Language:** Python | **Status:** Production-Ready

**Source:** Adapted from [Anthropic's autonomous-coding quickstart](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)

---

## Table of Contents

- [Project Overview](#-project-overview)
- [Architecture](#-architecture)
- [Directory Structure](#-directory-structure)
- [Quick Start](#-quick-start)
- [How It Works](#-how-it-works)
- [Security Model](#-security-model)
- [Customization](#-customization)
- [Troubleshooting](#-troubleshooting)
- [Development Guidelines](#-development-guidelines)

---

## Project Overview

This autonomous coding agent demonstrates how to build long-running AI agents that can:

1. **Generate comprehensive test plans** from an application specification
2. **Implement features incrementally** across multiple sessions
3. **Verify implementations** through browser automation (Playwright)
4. **Track progress persistently** via JSON and git commits

### Key Adaptations from Original

| Aspect | Original | This Version |
|--------|----------|--------------|
| Browser automation | Puppeteer MCP | Playwright MCP |
| Feature count | 200 | 75 (configurable) |
| Python environment | pip | uv |

---

## Architecture

### Two-Agent Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTONOMOUS CODING SYSTEM                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐         ┌──────────────────┐              │
│  │  INITIALIZER     │         │  CODING AGENT    │              │
│  │  AGENT           │         │                  │              │
│  │                  │         │                  │              │
│  │  • Read spec     │  ───>   │  • Pick feature  │              │
│  │  • Generate 75   │         │  • Implement     │              │
│  │    test cases    │         │  • Test with     │              │
│  │  • Setup project │         │    Playwright    │              │
│  │  • Init git      │         │  • Mark passing  │              │
│  │                  │         │  • Commit        │              │
│  └──────────────────┘         └──────────────────┘              │
│         │                            │                           │
│         v                            v                           │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    feature_list.json                         ││
│  │  [{"id": 1, "name": "...", "passes": false}, ...]           ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Session Flow

1. **Session 1 (Initializer)**
   - Reads `app_spec.txt`
   - Creates `feature_list.json` with 75+ detailed test cases
   - Sets up project structure, `init.sh`, git repository

2. **Sessions 2+ (Coding Agent)**
   - Loads existing `feature_list.json`
   - Selects next unimplemented feature
   - Implements feature
   - Verifies with Playwright browser automation
   - Marks feature as passing
   - Commits and continues

### Security Layers (Defense in Depth)

```
┌─────────────────────────────────────────┐
│  Layer 1: OS-Level Sandbox              │
│  • Bash commands run in isolation       │
├─────────────────────────────────────────┤
│  Layer 2: Filesystem Restrictions       │
│  • File ops restricted to project_dir   │
├─────────────────────────────────────────┤
│  Layer 3: Bash Command Allowlist        │
│  • Only permitted commands can run      │
│  • Extra validation for pkill, chmod    │
└─────────────────────────────────────────┘
```

---

## Directory Structure

```
autonomous-coding/
├── .env.example                    # API key template
├── .gitignore                      # Standard Python + secrets
├── CLAUDE.md                       # THIS FILE
├── README.md                       # Quick start guide
├── requirements.txt                # Dependencies (claude-code-sdk)
│
├── autonomous_agent_demo.py        # Main entry point (CLI)
├── agent.py                        # Agent session logic (~150 lines)
├── client.py                       # Claude SDK client config (~80 lines)
├── security.py                     # Bash allowlist (~250 lines)
├── progress.py                     # Progress tracking (~50 lines)
├── prompts.py                      # Prompt loading (~30 lines)
├── test_security.py                # Security tests (~200 lines)
│
├── prompts/
│   ├── app_spec.txt                # YOUR APPLICATION SPEC (customize this!)
│   ├── initializer_prompt.md       # First session instructions
│   └── coding_prompt.md            # Continuation session instructions
│
└── generations/                    # Output directory for generated projects
    └── .gitkeep
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- uv (for virtual environment management)
- Anthropic API key

### Installation

```bash
# Navigate to project
cd autonomous-coding

# Create virtual environment
uv venv

# Activate (Windows Git Bash)
source .venv/Scripts/activate
# Or Linux/Mac: source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Define Your Application

Edit `prompts/app_spec.txt` with your application specification. Include:
- Application overview and purpose
- Technology stack (React, Node.js, etc.)
- Core features with descriptions
- UI/UX requirements
- Data models

### Run the Agent

```bash
# Start fresh project
python autonomous_agent_demo.py --project-dir ./my_app

# Limit iterations for testing
python autonomous_agent_demo.py --project-dir ./my_app --max-iterations 3

# Continue existing project
python autonomous_agent_demo.py --project-dir ./my_app
```

---

## How It Works

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--project-dir` | Directory for the project | `./autonomous_demo_project` |
| `--max-iterations` | Max agent iterations | Unlimited |
| `--model` | Claude model to use | `claude-sonnet-4-5-20250929` |

### Generated Project Structure

After running, `generations/my_app/` will contain:

```
my_app/
├── feature_list.json         # Test cases (source of truth)
├── app_spec.txt              # Copied specification
├── init.sh                   # Environment setup script
├── claude-progress.txt       # Session progress notes
├── .claude_settings.json     # Security settings
└── [application files]       # Generated application code
```

### Timing Expectations

- **First session:** 5-15+ minutes (generating test cases)
- **Subsequent sessions:** 5-15 minutes each
- **Full build:** Many hours across multiple sessions

---

## Security Model

### Allowed Bash Commands

```python
ALLOWED_COMMANDS = {
    # File inspection
    "ls", "cat", "head", "tail", "wc", "grep",
    # File operations
    "cp", "mkdir", "chmod",  # chmod only +x
    # Directory
    "pwd",
    # Node.js
    "npm", "node",
    # Git
    "git",
    # Process management
    "ps", "lsof", "sleep", "pkill",  # pkill only dev processes
    # Scripts
    "init.sh",  # Only ./init.sh
}
```

### Extra Validation

- **pkill**: Only allowed for dev processes (node, npm, vite, etc.)
- **chmod**: Only allowed with +x mode
- **init.sh**: Only ./init.sh or paths ending in /init.sh

### Running Security Tests

```bash
python -m pytest test_security.py -v
```

---

## Customization

### Change Feature Count

Edit `prompts/initializer_prompt.md`:
```markdown
# Change this line:
Create a JSON file containing **a minimum of 75 features total**

# To your desired count:
Create a JSON file containing **a minimum of 30 features total**
```

### Add Allowed Commands

Edit `security.py`:
```python
ALLOWED_COMMANDS = {
    # ... existing commands ...
    "your_new_command",  # Add your command
}
```

### Change Browser Automation

The Playwright MCP tools are configured in `client.py`:
```python
PLAYWRIGHT_TOOLS = [
    "mcp__playwright__browser_navigate",
    "mcp__playwright__browser_take_screenshot",
    # ... add or modify tools
]
```

---

## Troubleshooting

### "Appears to hang on first run"

This is normal. The initializer agent is generating detailed test cases, which takes significant time. Watch for `[Tool: ...]` output to confirm the agent is working.

### "Command blocked by security hook"

The agent tried to run a command not in the allowlist. Options:
1. Add the command to `ALLOWED_COMMANDS` in `security.py`
2. If it's a potentially dangerous command, don't add it

### "API key not set"

Ensure `ANTHROPIC_API_KEY` is set:
```bash
# Check if set
echo $ANTHROPIC_API_KEY

# Set it
export ANTHROPIC_API_KEY='your-api-key-here'
# Or add to .env file
```

### "Playwright MCP tools not working"

Ensure Playwright MCP is installed:
```bash
npx -y @anthropic-ai/mcp-server-playwright
```

---

## Development Guidelines

### Following the 6 Principles

This project embodies the repository's core principles:

1. **TRUTH** - All agent decisions are logged and observable
2. **HONOR** - Generated code respects user's specification
3. **EXCELLENCE** - Production-quality from inception
4. **SERVE** - Simple CLI interface, clear error messages
5. **PERSEVERE** - Resilient multi-session architecture
6. **SHARPEN** - Progress tracking and iterative improvement

### Code Quality

- Type hints where applicable
- Comprehensive docstrings
- Security-first approach
- Clean separation of concerns

### Testing

```bash
# Run security tests
python -m pytest test_security.py -v

# Verify imports
python -c "from security import bash_security_hook; print('OK')"
```

---

## See Also

- [README.md](./README.md) - Quick start guide
- [Original quickstart](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)
- [Claude Code SDK docs](https://docs.anthropic.com/claude/agent-sdk)

---

*Last updated: November 2025*
