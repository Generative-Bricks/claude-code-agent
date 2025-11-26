"""
Pydantic models for the Todo Tracker Agent.

This module defines all data structures used for todo items,
ensuring type safety and data validation throughout the workflow.

Biblical Principle: TRUTH - All data structures are explicitly defined and validated.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ============================================================================
# Base Model Configuration
# ============================================================================


class BaseModelWithConfig(BaseModel):
    """
    Base model with configuration for OpenAI Agents SDK compatibility.

    The OpenAI Agents SDK requires strict JSON schemas without additionalProperties.
    This configuration ensures Pydantic v2 models are compatible.
    """

    model_config = ConfigDict(
        extra="forbid",  # Don't allow extra fields
        use_enum_values=False,  # Keep enum objects, not values
    )

    @classmethod
    def model_json_schema(cls, **kwargs):
        """Override to remove additionalProperties from schema."""
        schema = super().model_json_schema(**kwargs)

        # Remove additionalProperties from the schema
        def remove_additional_properties(obj):
            if isinstance(obj, dict):
                obj.pop("additionalProperties", None)
                for value in obj.values():
                    remove_additional_properties(value)
            elif isinstance(obj, list):
                for item in obj:
                    remove_additional_properties(item)

        remove_additional_properties(schema)
        return schema


# ============================================================================
# Enumerations
# ============================================================================


class TodoStatus(str, Enum):
    """Todo item status options."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TodoPriority(str, Enum):
    """Todo item priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


# ============================================================================
# Todo Models
# ============================================================================


class Todo(BaseModelWithConfig):
    """
    Individual todo item with all attributes.

    Attributes:
        id: Unique identifier for the todo
        title: Short description of the task
        description: Optional detailed description
        status: Current status (pending, in_progress, completed)
        priority: Importance level (low, medium, high, urgent)
        tags: Categories or labels for organization
        due_date: Optional deadline for the task
        created_at: When the todo was created
        updated_at: When the todo was last modified
        completed_at: When the todo was marked complete
    """

    id: str = Field(
        default_factory=lambda: str(uuid4())[:8],
        description="Unique identifier for the todo",
    )
    title: str = Field(
        ..., min_length=1, max_length=200, description="Short description of the task"
    )
    description: Optional[str] = Field(
        default=None, max_length=2000, description="Detailed description of the task"
    )
    status: TodoStatus = Field(
        default=TodoStatus.PENDING, description="Current status of the todo"
    )
    priority: TodoPriority = Field(
        default=TodoPriority.MEDIUM, description="Priority level of the todo"
    )
    tags: List[str] = Field(
        default_factory=list, description="Tags for categorization"
    )
    due_date: Optional[datetime] = Field(
        default=None, description="Deadline for the task"
    )
    created_at: datetime = Field(
        default_factory=datetime.now, description="When the todo was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="When the todo was last modified"
    )
    completed_at: Optional[datetime] = Field(
        default=None, description="When the todo was marked complete"
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Ensure title is not empty or just whitespace."""
        if not v.strip():
            raise ValueError("Title cannot be empty or just whitespace")
        return v.strip()

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: List[str]) -> List[str]:
        """Ensure tags are lowercase and stripped."""
        return [tag.lower().strip() for tag in v if tag.strip()]


class TodoCreate(BaseModelWithConfig):
    """
    Input model for creating a new todo.

    Only includes fields that can be set during creation.
    """

    title: str = Field(
        ..., min_length=1, max_length=200, description="Short description of the task"
    )
    description: Optional[str] = Field(
        default=None, max_length=2000, description="Detailed description of the task"
    )
    priority: TodoPriority = Field(
        default=TodoPriority.MEDIUM, description="Priority level of the todo"
    )
    tags: List[str] = Field(
        default_factory=list, description="Tags for categorization"
    )
    due_date: Optional[datetime] = Field(
        default=None, description="Deadline for the task"
    )


class TodoUpdate(BaseModelWithConfig):
    """
    Input model for updating an existing todo.

    All fields are optional - only specified fields will be updated.
    """

    title: Optional[str] = Field(
        default=None, min_length=1, max_length=200, description="New title for the task"
    )
    description: Optional[str] = Field(
        default=None, max_length=2000, description="New description for the task"
    )
    status: Optional[TodoStatus] = Field(
        default=None, description="New status for the todo"
    )
    priority: Optional[TodoPriority] = Field(
        default=None, description="New priority level"
    )
    tags: Optional[List[str]] = Field(
        default=None, description="New tags (replaces existing)"
    )
    due_date: Optional[datetime] = Field(
        default=None, description="New deadline for the task"
    )


class TodoFilter(BaseModelWithConfig):
    """
    Filter options for listing todos.

    All fields are optional - only specified filters will be applied.
    """

    status: Optional[TodoStatus] = Field(
        default=None, description="Filter by status"
    )
    priority: Optional[TodoPriority] = Field(
        default=None, description="Filter by priority"
    )
    tag: Optional[str] = Field(
        default=None, description="Filter by tag (partial match)"
    )
    overdue_only: bool = Field(
        default=False, description="Show only overdue todos"
    )
    sort_by: str = Field(
        default="created_at",
        description="Sort field (created_at, due_date, priority, status)",
    )
    ascending: bool = Field(
        default=True, description="Sort order (True=ascending, False=descending)"
    )


class TodoList(BaseModelWithConfig):
    """
    Container for a list of todos with metadata.

    Used for listing and search results.
    """

    todos: List[Todo] = Field(
        default_factory=list, description="List of todo items"
    )
    total_count: int = Field(
        default=0, description="Total number of todos matching filter"
    )
    pending_count: int = Field(
        default=0, description="Number of pending todos"
    )
    completed_count: int = Field(
        default=0, description="Number of completed todos"
    )


class TodoSearchResult(BaseModelWithConfig):
    """
    Search result with matching todos and search metadata.
    """

    query: str = Field(..., description="Search query used")
    matches: List[Todo] = Field(
        default_factory=list, description="Matching todo items"
    )
    match_count: int = Field(
        default=0, description="Number of matches found"
    )


# ============================================================================
# Response Models
# ============================================================================


class TodoResponse(BaseModelWithConfig):
    """
    Response model for single todo operations.
    """

    success: bool = Field(..., description="Whether the operation succeeded")
    message: str = Field(..., description="Human-readable message about the operation")
    todo: Optional[Todo] = Field(
        default=None, description="The todo item (if applicable)"
    )


class TodoListResponse(BaseModelWithConfig):
    """
    Response model for list operations.
    """

    success: bool = Field(..., description="Whether the operation succeeded")
    message: str = Field(..., description="Human-readable message about the operation")
    data: Optional[TodoList] = Field(
        default=None, description="List of todos with metadata"
    )
