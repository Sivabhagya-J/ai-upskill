"""
Pydantic schemas for project-related operations.
"""

from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

from .user import UserResponse


class ProjectStatus(str, Enum):
    """Project status enumeration."""
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProjectBase(BaseModel):
    """Base project schema with common fields."""
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Schema for project creation."""
    workflow_id: Optional[int] = None
    
    @validator('name')
    def validate_name(cls, v):
        """Validate project name."""
        if not v or not v.strip():
            raise ValueError('Project name is required')
        if len(v) > 255:
            raise ValueError('Project name is too long (max 255 characters)')
        return v.strip()


class ProjectUpdate(BaseModel):
    """Schema for project updates."""
    name: Optional[str] = None
    description: Optional[str] = None
    workflow_id: Optional[int] = None
    status: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    
    @validator('name')
    def validate_name(cls, v):
        """Validate project name if provided."""
        if v is not None:
            if not v.strip():
                raise ValueError('Project name cannot be empty')
            if len(v) > 255:
                raise ValueError('Project name is too long (max 255 characters)')
            return v.strip()
        return v


class ProjectResponse(ProjectBase):
    """Schema for project response."""
    id: int
    owner_id: int
    owner_name: Optional[str] = None
    workflow_id: Optional[int] = None
    workflow_name: Optional[str] = None
    status: ProjectStatus
    start_date: Optional[datetime] = None  # Changed from string to datetime
    end_date: Optional[datetime] = None    # Changed from string to datetime
    created_at: datetime
    updated_at: datetime
    task_count: int = 0
    completed_task_count: int = 0
    progress_percentage: float = 0.0
    is_active: bool = True
    
    class Config:
        from_attributes = True


class ProjectList(BaseModel):
    """Schema for paginated project list response."""
    items: List[ProjectResponse]
    total: int
    page: int
    size: int
    pages: int


class ProjectWithTasks(ProjectResponse):
    """Schema for project with tasks included."""
    tasks: List['TaskResponse'] = []


class ProjectStatistics(BaseModel):
    """Schema for project statistics."""
    total_projects: int
    active_projects: int
    completed_projects: int
    projects_by_status: dict
    recent_projects: List[ProjectResponse] 