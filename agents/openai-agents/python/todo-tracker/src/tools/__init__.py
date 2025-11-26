"""Tools package - Agent tools for Todo Tracker."""

from src.tools.todo_tools import (
    add_todo,
    complete_todo,
    delete_todo,
    do_add_todo,
    do_complete_todo,
    do_delete_todo,
    do_list_todos,
    do_search_todos,
    do_update_todo,
    list_todos,
    search_todos,
    update_todo,
)

__all__ = [
    # Agent tools (decorated)
    "add_todo",
    "complete_todo",
    "delete_todo",
    "list_todos",
    "search_todos",
    "update_todo",
    # Callable versions (for direct use)
    "do_add_todo",
    "do_complete_todo",
    "do_delete_todo",
    "do_list_todos",
    "do_search_todos",
    "do_update_todo",
]
