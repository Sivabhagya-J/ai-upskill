"""
Pydantic schemas for task-related operations.
"""

from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

from .user import UserResponse
from .project import ProjectResponse


class TaskStatus(str, Enum):
    """Task status enumeration."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Task priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskBase(BaseModel):
    """Base task schema with common fields."""
    title: str
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[str] = None  # Changed from datetime to str to match frontend


class TaskCreate(TaskBase):
    """Schema for task creation."""
    project_id: int
    status: TaskStatus = TaskStatus.TODO
    due_date: Optional[str] = None  # Changed from datetime to str to match frontend
    
    @validator('title')
    def validate_title(cls, v):
        """Validate task title."""
        if not v or not v.strip():
            raise ValueError('Task title is required')
        if len(v) > 255:
            raise ValueError('Task title is too long (max 255 characters)')
        return v.strip()


class TaskUpdate(BaseModel):
    """Schema for task updates."""
    title: Optional[str] = None
    description: Optional[str] = None
    project_id: Optional[int] = None
    assignee_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None
    
    @validator('title')
    def validate_title(cls, v):
        """Validate task title if provided."""
        if v is not None:
            if not v.strip():
                raise ValueError('Task title cannot be empty')
            if len(v) > 255:
                raise ValueError('Task title is too long (max 255 characters)')
            return v.strip()
        return v


class TaskResponse(TaskBase):
    """Schema for task response."""
    id: int
    project_id: int
    project_name: Optional[str] = None
    assignee_name: Optional[str] = None
    status: TaskStatus
    due_date: Optional[datetime] = None  # Keep as datetime for response
    created_at: datetime
    updated_at: datetime
    is_overdue: bool = False

    is_completed: bool = False
    is_active: bool = True
    
    class Config:
        from_attributes = True
        
    @validator('due_date', pre=True)
    @classmethod
    def parse_due_date(cls, v):
        """Parse due_date from string to datetime if needed."""
        if isinstance(v, str):
            try:
                from datetime import datetime
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                return None
        return v


class TaskList(BaseModel):
    """Schema for paginated task list response."""
    items: List[TaskResponse]
    total: int
    page: int
    size: int
    pages: int





class TaskStatistics(BaseModel):
    """Schema for task statistics."""
    total_tasks: int
    completed_tasks: int
    overdue_tasks: int
    tasks_by_status: dict
    tasks_by_priority: dict
    recent_tasks: List[TaskResponse]


class TaskFilter(BaseModel):
    """Schema for task filtering."""
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee_id: Optional[int] = None
    project_id: Optional[int] = None
    search: Optional[str] = None
    page: int = 1
    size: int = 20 