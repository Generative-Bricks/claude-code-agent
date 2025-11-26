# Todo Tracker Agent

AI-powered task management through natural language conversation.

## Quick Start

```bash
# Setup
uv venv
source .venv/Scripts/activate  # Windows Git Bash
uv pip install -r requirements.txt

# Configure
cp .env.example .env
# Add your OPENAI_API_KEY to .env

# Run
python -m src.main
```

## Features

- **Add todos** with titles, descriptions, priorities, tags, and due dates
- **List todos** with filtering by status, priority, tags, or overdue items
- **Complete todos** to mark tasks as done
- **Update todos** to modify any field
- **Delete todos** to remove items
- **Search todos** by keyword in title, description, or tags

## Usage Examples

```
You: Add a high priority todo to finish report by Friday
Assistant: Created todo 'finish report' with ID abc12345

You: Show all my pending todos
Assistant: You have 3 pending todos...

You: Mark abc12345 as done
Assistant: Marked 'finish report' as completed!

You: Find todos about work
Assistant: Found 2 todos matching 'work'...
```

## Commands

| Command | Description |
|---------|-------------|
| `stats` | Show todo statistics |
| `help` | Show usage tips |
| `quit` | Exit the application |

## CLI Options

```bash
# Interactive mode (default)
python -m src.main

# Single command
python -m src.main -c "add todo to buy milk"

# Show statistics
python -m src.main --stats

# Verbose logging
python -m src.main --verbose
```

## Documentation

See [CLAUDE.md](CLAUDE.md) for detailed documentation.
