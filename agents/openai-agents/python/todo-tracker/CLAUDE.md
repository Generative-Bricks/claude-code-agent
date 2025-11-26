# Todo Tracker Agent - Project Documentation

**Version:** 1.0.0
**Framework:** OpenAI Agents SDK (Python)
**Status:** Production-Ready
**Last Updated:** January 2025

---

## Project Overview

A production-ready AI-powered todo tracking agent built with the OpenAI Agents SDK. This agent helps users manage their tasks through natural language conversation.

**Purpose:** Demonstrate a simple yet complete agent implementation with persistent storage, comprehensive tooling, and intuitive UX.

**Key Features:**
- Natural language task management
- Full CRUD operations (Create, Read, Update, Delete)
- Search and filtering capabilities
- Persistent JSON storage
- Priority levels and due dates
- Tag-based organization
- Interactive CLI mode

---

## Directory Structure

```
todo-tracker/
├── src/
│   ├── __init__.py              # Package exports
│   ├── agent.py                 # Main agent definition (~100 lines)
│   ├── main.py                  # CLI entry point (~200 lines)
│   ├── models/
│   │   ├── __init__.py          # Model exports
│   │   └── schemas.py           # Pydantic models (~280 lines)
│   ├── services/
│   │   ├── __init__.py          # Service exports
│   │   └── storage.py           # JSON storage service (~230 lines)
│   └── tools/
│       ├── __init__.py          # Tool exports
│       └── todo_tools.py        # 6 agent tools (~400 lines)
├── data/
│   └── todos.json               # Persistent storage (auto-created)
├── tests/
│   └── __init__.py              # Test documentation
├── logs/
│   └── todo_tracker.log         # Application logs (auto-created)
├── .env.example                 # Environment template
├── requirements.txt             # Python dependencies
├── README.md                    # Quick start guide
└── CLAUDE.md                    # THIS FILE
```

**Total Code:** ~1,200 lines across models, services, tools, and CLI

---

## Architecture

### Data Flow

```
User Input (Natural Language)
       │
       ▼
┌─────────────────────────────┐
│    Todo Tracker Agent       │
│    (GPT-4o-mini)            │
│                             │
│  Instructions: Task mgmt    │
│  guidance with formatting   │
└──────────────┬──────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
    ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐
│add_todo│ │list    │ │search  │
│        │ │_todos  │ │_todos  │
└────┬───┘ └────┬───┘ └────┬───┘
     │          │          │
     └──────────┼──────────┘
                │
                ▼
        ┌───────────────┐
        │ TodoStorage   │
        │ (JSON File)   │
        └───────────────┘
                │
                ▼
        data/todos.json
```

### Component Responsibilities

| Component | File | Responsibility |
|-----------|------|----------------|
| Agent | `agent.py` | Natural language understanding, tool orchestration |
| Tools | `todo_tools.py` | 6 operations: add, list, complete, update, delete, search |
| Storage | `storage.py` | JSON file persistence with atomic writes |
| Models | `schemas.py` | Pydantic validation for all data structures |
| CLI | `main.py` | Interactive and command-line interfaces |

---

## Setup & Running

### Quick Start

```bash
# 1. Navigate to project
cd agents/openai-agents/python/todo-tracker

# 2. Create virtual environment
uv venv

# 3. Activate (Windows Git Bash)
source .venv/Scripts/activate

# 4. Install dependencies
uv pip install -r requirements.txt

# 5. Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 6. Run interactive mode
python -m src.main
```

### Usage Modes

**Interactive Mode (default):**
```bash
python -m src.main
```

**Single Command:**
```bash
python -m src.main -c "add a todo to buy groceries"
python -m src.main -c "show all my pending todos"
```

**Statistics:**
```bash
python -m src.main --stats
```

**Verbose Logging:**
```bash
python -m src.main --verbose
```

---

## Tools Reference

### 1. add_todo
Create a new todo item.

**Parameters:**
- `title` (required): Short description of the task
- `description` (optional): Detailed description
- `priority` (optional): low, medium, high, urgent (default: medium)
- `tags` (optional): List of categorization tags
- `due_date` (optional): ISO format deadline

**Example:**
```
"Add a high priority todo to finish report by Friday, tag it as work"
```

### 2. list_todos
List todos with optional filters.

**Parameters:**
- `status`: pending, in_progress, completed
- `priority`: low, medium, high, urgent
- `tag`: Filter by tag (partial match)
- `overdue_only`: Show only overdue items
- `sort_by`: created_at, due_date, priority, status
- `ascending`: Sort order

**Example:**
```
"Show all pending todos sorted by priority"
```

### 3. complete_todo
Mark a todo as completed.

**Parameters:**
- `todo_id`: ID of the todo to complete

**Example:**
```
"Mark todo abc123 as done"
```

### 4. update_todo
Modify an existing todo.

**Parameters:**
- `todo_id` (required): ID of todo to update
- `title`, `description`, `status`, `priority`, `tags`, `due_date` (all optional)

**Example:**
```
"Change priority of abc123 to urgent"
```

### 5. delete_todo
Remove a todo permanently.

**Parameters:**
- `todo_id`: ID of the todo to delete

**Example:**
```
"Delete todo abc123"
```

### 6. search_todos
Search todos by keyword.

**Parameters:**
- `query`: Search term (searches title, description, tags)

**Example:**
```
"Find todos about groceries"
```

---

## Data Models

### Todo
```python
class Todo:
    id: str                    # Unique 8-char identifier
    title: str                 # Task description (1-200 chars)
    description: Optional[str] # Details (up to 2000 chars)
    status: TodoStatus         # pending, in_progress, completed
    priority: TodoPriority     # low, medium, high, urgent
    tags: List[str]            # Categorization labels
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
```

### Storage Format (todos.json)
```json
{
  "todos": [
    {
      "id": "abc12345",
      "title": "Buy groceries",
      "status": "pending",
      "priority": "medium",
      "tags": ["shopping"],
      "created_at": "2024-01-15T10:00:00"
    }
  ],
  "last_updated": "2024-01-15T10:00:00",
  "count": 1
}
```

---

## Key Design Decisions

### 1. GPT-4o-mini Model Choice
**Decision:** Use `gpt-4o-mini` instead of `gpt-4o`

**Rationale:**
- Todo management is straightforward task routing
- Cost-effective for frequent interactions
- Fast response times for CLI usage
- Sufficient capability for tool selection

### 2. JSON File Storage
**Decision:** Simple JSON file instead of SQLite

**Rationale:**
- Easy to backup (just copy the file)
- Human-readable for debugging
- No database dependencies
- Atomic writes prevent corruption
- Sufficient for personal todo lists

### 3. Dual Function Pattern
**Decision:** Both `@function_tool` decorated and callable versions

**Rationale:**
- `@function_tool` versions for agent use
- `do_*` versions for direct Python calls
- Enables testing without agent invocation
- Supports batch operations outside agent context

### 4. Singleton Storage Pattern
**Decision:** Global storage instance via `get_storage()`

**Rationale:**
- Ensures consistent state across tools
- Allows easy testing via `reset_storage()`
- Prevents multiple file handles
- Simple dependency injection pattern

---

## Error Handling

### Storage Errors
- File not found: Auto-creates empty storage
- Invalid JSON: Returns empty list, logs error
- Write failure: Returns False, keeps original data

### Validation Errors
- Empty title: Rejected by Pydantic
- Invalid priority: Falls back to "medium"
- Invalid date: Logs warning, skips field
- Invalid status: Logs warning, skips update

### Agent Errors
- Tool failure: Returns error message in response
- Missing todo: Returns "not found" message
- API error: Logged, displayed to user

---

## Testing

### Run Tests
```bash
pytest tests/
```

### Manual Testing
```bash
# Test add
python -m src.main -c "add todo: test task"

# Test list
python -m src.main -c "show all todos"

# Test search
python -m src.main -c "search for test"

# Test stats
python -m src.main --stats
```

### Test Storage Directly
```python
from src.services.storage import reset_storage

# Create test storage
storage = reset_storage("test_todos.json")
storage.add(Todo(title="Test"))
todos = storage.get_all()
```

---

## Biblical Principles in Code

### TRUTH (John 14:6)
- **Where:** Transparent logging of all operations
- **Example:** Every tool logs its actions: `logger.info(f"Adding todo: {title}")`

### HONOR (Matthew 22:36-40)
- **Where:** User-first design with clear feedback
- **Example:** Friendly messages like "Congratulations on completing your task!"

### EXCELLENCE (Colossians 3:23)
- **Where:** Comprehensive validation and error handling
- **Example:** Pydantic models validate all inputs before storage

### SERVE (John 13:14)
- **Where:** Simple, intuitive interface
- **Example:** Natural language understanding with helpful prompts

### PERSEVERE (Hebrews 12:1-3)
- **Where:** Graceful error handling
- **Example:** Storage continues working even with corrupted JSON

### SHARPEN (Proverbs 27:17)
- **Where:** Clear documentation and testable code
- **Example:** Separate callable versions for testing

---

## Future Enhancements

- [ ] Add recurring todos
- [ ] Implement reminder notifications
- [ ] Add project/folder organization
- [ ] Support due time (not just date)
- [ ] Add time tracking for tasks
- [ ] Export to markdown/CSV
- [ ] Sync with external services (Google Tasks, Todoist)

---

## Troubleshooting

### "OPENAI_API_KEY not set"
```bash
cp .env.example .env
# Edit .env and add your API key
```

### "Module not found"
```bash
# Make sure you're in the right directory
cd agents/openai-agents/python/todo-tracker

# Reinstall dependencies
uv pip install -r requirements.txt
```

### "Permission denied on todos.json"
```bash
# Check file permissions
ls -la data/todos.json

# Fix if needed
chmod 644 data/todos.json
```

### Logs Location
```bash
# View recent logs
tail -f logs/todo_tracker.log
```

---

**Remember:** *"Whatever you do, work heartily, as for the Lord"* - Colossians 3:23

Keep your tasks organized, stay productive, and accomplish your goals!

---

*Last updated: January 2025*
*Project Status: Production-Ready*
