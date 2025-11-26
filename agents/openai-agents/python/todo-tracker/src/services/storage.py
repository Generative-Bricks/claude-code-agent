"""
JSON file storage service for Todo Tracker.

Provides persistent storage of todos in a JSON file with
atomic operations and proper error handling.

Biblical Principle: PERSEVERE - Reliable storage that handles failures gracefully.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from src.models.schemas import Todo, TodoList, TodoStatus

# ============================================================================
# Logging Configuration
# ============================================================================

logger = logging.getLogger(__name__)


# ============================================================================
# Storage Service
# ============================================================================


class TodoStorage:
    """
    JSON file-based storage service for todos.

    Provides CRUD operations with atomic file writes and
    proper error handling for data persistence.

    Attributes:
        file_path: Path to the JSON storage file
    """

    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize the storage service.

        Args:
            file_path: Path to JSON file (default: data/todos.json)
        """
        # Determine file path from environment or default
        if file_path is None:
            file_path = os.environ.get("TODO_FILE_PATH", "data/todos.json")

        self.file_path = Path(file_path)

        # Ensure directory exists
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        # Create empty file if it doesn't exist
        if not self.file_path.exists():
            self._write_todos([])
            logger.info(f"Created new todo storage file: {self.file_path}")

    # ========================================================================
    # Private Methods
    # ========================================================================

    def _read_todos(self) -> List[Dict]:
        """
        Read todos from JSON file.

        Returns:
            List of todo dictionaries from file
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("todos", [])
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {self.file_path}: {e}")
            return []
        except FileNotFoundError:
            logger.warning(f"Todo file not found: {self.file_path}")
            return []
        except Exception as e:
            logger.error(f"Error reading todos: {e}")
            return []

    def _write_todos(self, todos: List[Dict]) -> bool:
        """
        Write todos to JSON file atomically.

        Uses a temp file + rename pattern to prevent data corruption.

        Args:
            todos: List of todo dictionaries to write

        Returns:
            True if write succeeded, False otherwise
        """
        try:
            # Write to temp file first
            temp_path = self.file_path.with_suffix(".tmp")

            data = {
                "todos": todos,
                "last_updated": datetime.now().isoformat(),
                "count": len(todos),
            }

            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)

            # Atomic rename
            temp_path.replace(self.file_path)

            logger.debug(f"Wrote {len(todos)} todos to {self.file_path}")
            return True

        except Exception as e:
            logger.error(f"Error writing todos: {e}")
            return False

    def _todo_to_dict(self, todo: Todo) -> Dict:
        """Convert Todo model to dictionary for storage."""
        return todo.model_dump(mode="json")

    def _dict_to_todo(self, data: Dict) -> Optional[Todo]:
        """Convert dictionary to Todo model."""
        try:
            return Todo(**data)
        except Exception as e:
            logger.warning(f"Invalid todo data: {e}")
            return None

    # ========================================================================
    # Public Methods - CRUD Operations
    # ========================================================================

    def get_all(self) -> List[Todo]:
        """
        Get all todos from storage.

        Returns:
            List of Todo objects
        """
        raw_todos = self._read_todos()
        todos = []

        for raw in raw_todos:
            todo = self._dict_to_todo(raw)
            if todo:
                todos.append(todo)

        return todos

    def get_by_id(self, todo_id: str) -> Optional[Todo]:
        """
        Get a specific todo by ID.

        Args:
            todo_id: Unique identifier of the todo

        Returns:
            Todo object if found, None otherwise
        """
        todos = self.get_all()

        for todo in todos:
            if todo.id == todo_id:
                return todo

        return None

    def add(self, todo: Todo) -> bool:
        """
        Add a new todo to storage.

        Args:
            todo: Todo object to add

        Returns:
            True if added successfully, False otherwise
        """
        todos = self._read_todos()
        todos.append(self._todo_to_dict(todo))
        return self._write_todos(todos)

    def update(self, todo: Todo) -> bool:
        """
        Update an existing todo.

        Args:
            todo: Todo object with updated values

        Returns:
            True if updated successfully, False otherwise
        """
        todos = self._read_todos()
        updated = False

        for i, existing in enumerate(todos):
            if existing.get("id") == todo.id:
                todos[i] = self._todo_to_dict(todo)
                updated = True
                break

        if updated:
            return self._write_todos(todos)

        logger.warning(f"Todo not found for update: {todo.id}")
        return False

    def delete(self, todo_id: str) -> bool:
        """
        Delete a todo by ID.

        Args:
            todo_id: ID of todo to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        todos = self._read_todos()
        original_count = len(todos)

        todos = [t for t in todos if t.get("id") != todo_id]

        if len(todos) < original_count:
            return self._write_todos(todos)

        logger.warning(f"Todo not found for deletion: {todo_id}")
        return False

    def clear_completed(self) -> int:
        """
        Remove all completed todos.

        Returns:
            Number of todos removed
        """
        todos = self._read_todos()
        original_count = len(todos)

        todos = [
            t
            for t in todos
            if t.get("status") != TodoStatus.COMPLETED.value
        ]

        removed = original_count - len(todos)

        if removed > 0:
            self._write_todos(todos)

        return removed

    def get_stats(self) -> Dict:
        """
        Get statistics about todos.

        Returns:
            Dictionary with count statistics
        """
        todos = self.get_all()

        pending = sum(1 for t in todos if t.status == TodoStatus.PENDING)
        in_progress = sum(1 for t in todos if t.status == TodoStatus.IN_PROGRESS)
        completed = sum(1 for t in todos if t.status == TodoStatus.COMPLETED)
        overdue = sum(
            1
            for t in todos
            if t.due_date
            and t.due_date < datetime.now()
            and t.status != TodoStatus.COMPLETED
        )

        return {
            "total": len(todos),
            "pending": pending,
            "in_progress": in_progress,
            "completed": completed,
            "overdue": overdue,
        }


# ============================================================================
# Singleton Storage Instance
# ============================================================================

# Global storage instance for use across the application
_storage_instance: Optional[TodoStorage] = None


def get_storage() -> TodoStorage:
    """
    Get the singleton storage instance.

    Returns:
        TodoStorage instance
    """
    global _storage_instance

    if _storage_instance is None:
        _storage_instance = TodoStorage()

    return _storage_instance


def reset_storage(file_path: Optional[str] = None) -> TodoStorage:
    """
    Reset the storage instance (useful for testing).

    Args:
        file_path: Optional new file path

    Returns:
        New TodoStorage instance
    """
    global _storage_instance
    _storage_instance = TodoStorage(file_path)
    return _storage_instance
