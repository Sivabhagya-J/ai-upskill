"""
Project model for project management.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from datetime import datetime

from ..database import Base


class ProjectStatus(str, enum.Enum):
    """Project status enumeration."""
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Project(Base):
    """
    Project model representing projects in the system.
    
    Attributes:
        id: Primary key
        name: Project name
        description: Project description
        owner_id: Foreign key to user who owns the project
        status: Current project status
        start_date: Project start date
        end_date: Project end date
        created_at: Project creation timestamp
        updated_at: Last update timestamp
    """
    
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=True, index=True)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PLANNING, nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="projects")
    workflow = relationship("Workflow", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', status='{self.status}')>"
    
    @property
    def is_active(self) -> bool:
        """Check if project is active (not completed or cancelled)."""
        return self.status not in [ProjectStatus.COMPLETED, ProjectStatus.CANCELLED]
    
    @property
    def task_count(self) -> int:
        """Get total number of tasks in the project."""
        return len(self.tasks) if self.tasks else 0
    
    @property
    def completed_task_count(self) -> int:
        """Get number of completed tasks in the project."""
        if not self.tasks:
            return 0
        return len([task for task in self.tasks if task.status == "completed"])
    
    @property
    def progress_percentage(self) -> float:
        """Calculate project progress percentage."""
        if not self.tasks:
            return 0.0
        total_tasks = len(self.tasks)
        completed_tasks = self.completed_task_count
        return (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0.0
    
    def to_dict(self):
        """Convert project to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "owner_id": self.owner_id,
            "owner_name": self.owner.full_name if self.owner else None,
            "workflow_id": self.workflow_id,
            "workflow_name": self.workflow.name if self.workflow else None,
            "status": self.status.value if self.status else None,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "task_count": self.task_count,
            "completed_task_count": self.completed_task_count,
            "progress_percentage": round(self.progress_percentage, 2),
            "is_active": self.is_active
        } 