"""
Todo management tools for the Todo Tracker Agent.

This module provides the 6 core tools for todo management:
1. add_todo - Create a new todo item
2. list_todos - List all or filtered todos
3. complete_todo - Mark a todo as completed
4. update_todo - Update an existing todo
5. delete_todo - Remove a todo
6. search_todos - Search todos by keyword

Biblical Principle: SERVE - Tools designed to make task management simple and effective.
Biblical Principle: EXCELLENCE - Comprehensive validation and error handling.
"""

import logging
from datetime import datetime
from typing import List, Optional

from agents import function_tool

from src.models.schemas import (
    Todo,
    TodoCreate,
    TodoFilter,
    TodoList,
    TodoPriority,
    TodoResponse,
    TodoSearchResult,
    TodoStatus,
    TodoUpdate,
)
from src.services.storage import get_storage

# ============================================================================
# Logging Configuration
# ============================================================================

logger = logging.getLogger(__name__)


# ============================================================================
# Helper Functions (Callable versions for direct use)
# ============================================================================


def do_add_todo(
    title: str,
    description: Optional[str] = None,
    priority: str = "medium",
    tags: Optional[List[str]] = None,
    due_date: Optional[str] = None,
) -> TodoResponse:
    """
    Core implementation for adding a new todo.

    Args:
        title: Short description of the task
        description: Detailed description (optional)
        priority: Priority level (low, medium, high, urgent)
        tags: List of tags for categorization
        due_date: Deadline in ISO format (optional)

    Returns:
        TodoResponse with success status and created todo
    """
    logger.info(f"Adding todo: {title}")

    try:
        # Parse priority
        try:
            priority_enum = TodoPriority(priority.lower())
        except ValueError:
            priority_enum = TodoPriority.MEDIUM

        # Parse due date if provided
        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = datetime.fromisoformat(due_date)
            except ValueError:
                logger.warning(f"Invalid due_date format: {due_date}")

        # Create todo
        todo = Todo(
            title=title,
            description=description,
            priority=priority_enum,
            tags=tags or [],
            due_date=parsed_due_date,
        )

        # Save to storage
        storage = get_storage()
        success = storage.add(todo)

        if success:
            logger.info(f"Created todo: {todo.id}")
            return TodoResponse(
                success=True,
                message=f"Created todo '{title}' with ID {todo.id}",
                todo=todo,
            )
        else:
            return TodoResponse(
                success=False,
                message="Failed to save todo to storage",
                todo=None,
            )

    except Exception as e:
        logger.error(f"Error creating todo: {e}")
        return TodoResponse(
            success=False,
            message=f"Error creating todo: {str(e)}",
            todo=None,
        )


def do_list_todos(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tag: Optional[str] = None,
    overdue_only: bool = False,
    sort_by: str = "created_at",
    ascending: bool = True,
) -> TodoList:
    """
    Core implementation for listing todos with optional filters.

    Args:
        status: Filter by status (pending, in_progress, completed)
        priority: Filter by priority (low, medium, high, urgent)
        tag: Filter by tag (partial match)
        overdue_only: Show only overdue todos
        sort_by: Field to sort by (created_at, due_date, priority, status)
        ascending: Sort order

    Returns:
        TodoList with matching todos and statistics
    """
    logger.info("Listing todos with filters")

    storage = get_storage()
    todos = storage.get_all()

    # Apply filters
    filtered_todos = []
    for todo in todos:
        # Status filter
        if status:
            try:
                status_enum = TodoStatus(status.lower())
                if todo.status != status_enum:
                    continue
            except ValueError:
                pass

        # Priority filter
        if priority:
            try:
                priority_enum = TodoPriority(priority.lower())
                if todo.priority != priority_enum:
                    continue
            except ValueError:
                pass

        # Tag filter (partial match)
        if tag:
            tag_lower = tag.lower()
            if not any(tag_lower in t.lower() for t in todo.tags):
                continue

        # Overdue filter
        if overdue_only:
            if not todo.due_date:
                continue
            if todo.due_date >= datetime.now():
                continue
            if todo.status == TodoStatus.COMPLETED:
                continue

        filtered_todos.append(todo)

    # Sort todos
    def get_sort_key(t: Todo):
        if sort_by == "due_date":
            return t.due_date or datetime.max
        elif sort_by == "priority":
            # Map priority to numeric for sorting
            priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
            return priority_order.get(t.priority.value, 2)
        elif sort_by == "status":
            status_order = {"in_progress": 0, "pending": 1, "completed": 2}
            return status_order.get(t.status.value, 1)
        else:  # created_at
            return t.created_at

    filtered_todos.sort(key=get_sort_key, reverse=not ascending)

    # Calculate statistics
    pending = sum(1 for t in filtered_todos if t.status == TodoStatus.PENDING)
    completed = sum(1 for t in filtered_todos if t.status == TodoStatus.COMPLETED)

    return TodoList(
        todos=filtered_todos,
        total_count=len(filtered_todos),
        pending_count=pending,
        completed_count=completed,
    )


def do_complete_todo(todo_id: str) -> TodoResponse:
    """
    Core implementation for marking a todo as completed.

    Args:
        todo_id: ID of the todo to complete

    Returns:
        TodoResponse with success status and updated todo
    """
    logger.info(f"Completing todo: {todo_id}")

    storage = get_storage()
    todo = storage.get_by_id(todo_id)

    if not todo:
        return TodoResponse(
            success=False,
            message=f"Todo with ID '{todo_id}' not found",
            todo=None,
        )

    if todo.status == TodoStatus.COMPLETED:
        return TodoResponse(
            success=True,
            message=f"Todo '{todo.title}' is already completed",
            todo=todo,
        )

    # Update status and timestamps
    todo.status = TodoStatus.COMPLETED
    todo.completed_at = datetime.now()
    todo.updated_at = datetime.now()

    success = storage.update(todo)

    if success:
        logger.info(f"Completed todo: {todo_id}")
        return TodoResponse(
            success=True,
            message=f"Marked '{todo.title}' as completed",
            todo=todo,
        )
    else:
        return TodoResponse(
            success=False,
            message="Failed to update todo in storage",
            todo=None,
        )


def do_update_todo(
    todo_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tags: Optional[List[str]] = None,
    due_date: Optional[str] = None,
) -> TodoResponse:
    """
    Core implementation for updating an existing todo.

    Args:
        todo_id: ID of the todo to update
        title: New title (optional)
        description: New description (optional)
        status: New status (optional)
        priority: New priority (optional)
        tags: New tags (optional, replaces existing)
        due_date: New due date in ISO format (optional)

    Returns:
        TodoResponse with success status and updated todo
    """
    logger.info(f"Updating todo: {todo_id}")

    storage = get_storage()
    todo = storage.get_by_id(todo_id)

    if not todo:
        return TodoResponse(
            success=False,
            message=f"Todo with ID '{todo_id}' not found",
            todo=None,
        )

    # Apply updates
    if title:
        todo.title = title

    if description is not None:
        todo.description = description

    if status:
        try:
            new_status = TodoStatus(status.lower())
            todo.status = new_status
            if new_status == TodoStatus.COMPLETED and not todo.completed_at:
                todo.completed_at = datetime.now()
        except ValueError:
            logger.warning(f"Invalid status: {status}")

    if priority:
        try:
            todo.priority = TodoPriority(priority.lower())
        except ValueError:
            logger.warning(f"Invalid priority: {priority}")

    if tags is not None:
        todo.tags = [t.lower().strip() for t in tags if t.strip()]

    if due_date:
        try:
            todo.due_date = datetime.fromisoformat(due_date)
        except ValueError:
            logger.warning(f"Invalid due_date format: {due_date}")

    # Update timestamp
    todo.updated_at = datetime.now()

    success = storage.update(todo)

    if success:
        logger.info(f"Updated todo: {todo_id}")
        return TodoResponse(
            success=True,
            message=f"Updated todo '{todo.title}'",
            todo=todo,
        )
    else:
        return TodoResponse(
            success=False,
            message="Failed to update todo in storage",
            todo=None,
        )


def do_delete_todo(todo_id: str) -> TodoResponse:
    """
    Core implementation for deleting a todo.

    Args:
        todo_id: ID of the todo to delete

    Returns:
        TodoResponse with success status
    """
    logger.info(f"Deleting todo: {todo_id}")

    storage = get_storage()
    todo = storage.get_by_id(todo_id)

    if not todo:
        return TodoResponse(
            success=False,
            message=f"Todo with ID '{todo_id}' not found",
            todo=None,
        )

    success = storage.delete(todo_id)

    if success:
        logger.info(f"Deleted todo: {todo_id}")
        return TodoResponse(
            success=True,
            message=f"Deleted todo '{todo.title}'",
            todo=todo,
        )
    else:
        return TodoResponse(
            success=False,
            message="Failed to delete todo from storage",
            todo=None,
        )


def do_search_todos(query: str) -> TodoSearchResult:
    """
    Core implementation for searching todos.

    Searches in title, description, and tags.

    Args:
        query: Search query string

    Returns:
        TodoSearchResult with matching todos
    """
    logger.info(f"Searching todos: {query}")

    storage = get_storage()
    todos = storage.get_all()

    query_lower = query.lower()
    matches = []

    for todo in todos:
        # Search in title
        if query_lower in todo.title.lower():
            matches.append(todo)
            continue

        # Search in description
        if todo.description and query_lower in todo.description.lower():
            matches.append(todo)
            continue

        # Search in tags
        if any(query_lower in tag.lower() for tag in todo.tags):
            matches.append(todo)
            continue

    return TodoSearchResult(
        query=query,
        matches=matches,
        match_count=len(matches),
    )


# ============================================================================
# Agent Tools (Decorated versions for agent use)
# ============================================================================


@function_tool
def add_todo(
    title: str,
    description: Optional[str] = None,
    priority: str = "medium",
    tags: Optional[List[str]] = None,
    due_date: Optional[str] = None,
) -> TodoResponse:
    """
    Add a new todo item to the list.

    Use this tool when the user wants to create a new task or reminder.

    Args:
        title: Short description of the task (required)
        description: Detailed description of what needs to be done (optional)
        priority: Priority level - low, medium, high, or urgent (default: medium)
        tags: List of tags for categorization like ["work", "urgent"] (optional)
        due_date: Deadline in ISO format like "2024-12-31" or "2024-12-31T14:00:00" (optional)

    Returns:
        TodoResponse with the created todo item

    Example:
        add_todo(
            title="Buy groceries",
            description="Milk, eggs, bread",
            priority="high",
            tags=["shopping", "personal"],
            due_date="2024-01-20"
        )
    """
    return do_add_todo(title, description, priority, tags, due_date)


@function_tool
def list_todos(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tag: Optional[str] = None,
    overdue_only: bool = False,
    sort_by: str = "created_at",
    ascending: bool = True,
) -> TodoList:
    """
    List all todos with optional filtering and sorting.

    Use this tool when the user wants to see their todos.

    Args:
        status: Filter by status - pending, in_progress, or completed (optional)
        priority: Filter by priority - low, medium, high, or urgent (optional)
        tag: Filter by tag name, supports partial matching (optional)
        overdue_only: If True, only show overdue todos (default: False)
        sort_by: Sort field - created_at, due_date, priority, or status (default: created_at)
        ascending: Sort order - True for ascending, False for descending (default: True)

    Returns:
        TodoList with matching todos and statistics

    Example:
        list_todos(status="pending", sort_by="priority", ascending=False)
    """
    return do_list_todos(status, priority, tag, overdue_only, sort_by, ascending)


@function_tool
def complete_todo(todo_id: str) -> TodoResponse:
    """
    Mark a todo as completed.

    Use this tool when the user has finished a task and wants to mark it done.

    Args:
        todo_id: The unique ID of the todo to complete

    Returns:
        TodoResponse with the updated todo

    Example:
        complete_todo(todo_id="abc12345")
    """
    return do_complete_todo(todo_id)


@function_tool
def update_todo(
    todo_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tags: Optional[List[str]] = None,
    due_date: Optional[str] = None,
) -> TodoResponse:
    """
    Update an existing todo item.

    Use this tool when the user wants to modify a task's details.
    Only provided fields will be updated.

    Args:
        todo_id: The unique ID of the todo to update (required)
        title: New title for the task (optional)
        description: New description (optional)
        status: New status - pending, in_progress, or completed (optional)
        priority: New priority - low, medium, high, or urgent (optional)
        tags: New tags list, replaces existing tags (optional)
        due_date: New deadline in ISO format (optional)

    Returns:
        TodoResponse with the updated todo

    Example:
        update_todo(
            todo_id="abc12345",
            priority="urgent",
            due_date="2024-01-15"
        )
    """
    return do_update_todo(todo_id, title, description, status, priority, tags, due_date)


@function_tool
def delete_todo(todo_id: str) -> TodoResponse:
    """
    Delete a todo item permanently.

    Use this tool when the user wants to remove a task from their list.
    This action cannot be undone.

    Args:
        todo_id: The unique ID of the todo to delete

    Returns:
        TodoResponse confirming deletion

    Example:
        delete_todo(todo_id="abc12345")
    """
    return do_delete_todo(todo_id)


@function_tool
def search_todos(query: str) -> TodoSearchResult:
    """
    Search todos by keyword.

    Use this tool when the user wants to find specific todos.
    Searches in title, description, and tags.

    Args:
        query: Search term to look for

    Returns:
        TodoSearchResult with matching todos

    Example:
        search_todos(query="groceries")
    """
    return do_search_todos(query)
