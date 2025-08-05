"""
Workflow model for business logic and pipeline stages.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from ..database import Base


class WorkflowStage(str, enum.Enum):
    """Workflow stage enumeration."""
    LEAD = "lead"
    QUALIFICATION = "qualification"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"
    DEVELOPMENT = "development"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"


class WorkflowType(str, enum.Enum):
    """Workflow type enumeration."""
    SALES = "sales"
    SUPPORT = "support"
    DEVELOPMENT = "development"
    MARKETING = "marketing"
    OPERATIONS = "operations"


class Workflow(Base):
    """
    Workflow model for business process management.
    
    Attributes:
        id: Primary key
        name: Workflow name
        description: Workflow description
        type: Workflow type (sales, support, etc.)
        stages: Workflow stages configuration (JSON)
        rules: Business rules configuration (JSON)
        is_active: Whether the workflow is active
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    
    __tablename__ = "workflows"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    type = Column(Enum(WorkflowType), nullable=False, index=True)
    stages = Column(JSON, nullable=False)  # JSON configuration of stages
    rules = Column(JSON, nullable=True)  # JSON configuration of business rules
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    projects = relationship("Project", back_populates="workflow")
    instances = relationship("WorkflowInstance", back_populates="workflow")
    
    def __repr__(self):
        return f"<Workflow(id={self.id}, name='{self.name}', type='{self.type}')>"
    
    def to_dict(self):
        """Convert workflow to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type.value,
            "stages": self.stages,
            "rules": self.rules,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class WorkflowInstance(Base):
    """
    Workflow instance model for tracking individual workflow executions.
    
    Attributes:
        id: Primary key
        workflow_id: Foreign key to workflow
        project_id: Foreign key to project
        current_stage: Current stage in the workflow
        stage_data: JSON data for current stage
        history: JSON array of stage transitions
        is_completed: Whether the workflow is completed
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    
    __tablename__ = "workflow_instances"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    current_stage = Column(String(100), nullable=False, index=True)
    stage_data = Column(JSON, nullable=True)  # JSON data for current stage
    history = Column(JSON, nullable=True)  # JSON array of stage transitions
    is_completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    workflow = relationship("Workflow", back_populates="instances")
    project = relationship("Project")
    
    def __repr__(self):
        return f"<WorkflowInstance(id={self.id}, workflow_id={self.workflow_id}, current_stage='{self.current_stage}')>"
    
    def to_dict(self):
        """Convert workflow instance to dictionary representation."""
        return {
            "id": self.id,
            "workflow_id": self.workflow_id,
            "project_id": self.project_id,
            "current_stage": self.current_stage,
            "stage_data": self.stage_data,
            "history": self.history,
            "is_completed": self.is_completed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class BusinessRule(Base):
    """
    Business rule model for enforcing business logic.
    
    Attributes:
        id: Primary key
        name: Rule name
        description: Rule description
        rule_type: Type of rule (validation, automation, notification)
        conditions: JSON conditions for rule evaluation
        actions: JSON actions to take when conditions are met
        is_active: Whether the rule is active
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    
    __tablename__ = "business_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    rule_type = Column(String(50), nullable=False, index=True)  # validation, automation, notification
    conditions = Column(JSON, nullable=False)  # JSON conditions for rule evaluation
    actions = Column(JSON, nullable=False)  # JSON actions to take
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<BusinessRule(id={self.id}, name='{self.name}', type='{self.rule_type}')>"
    
    def to_dict(self):
        """Convert business rule to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "rule_type": self.rule_type,
            "conditions": self.conditions,
            "actions": self.actions,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        } 