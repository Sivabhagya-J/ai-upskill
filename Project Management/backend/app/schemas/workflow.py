"""
Pydantic schemas for workflow-related operations.
"""

from pydantic import BaseModel, validator, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum

from .user import UserResponse
from .project import ProjectResponse


class WorkflowType(str, Enum):
    """Workflow type enumeration."""
    SALES = "sales"
    SUPPORT = "support"
    DEVELOPMENT = "development"
    MARKETING = "marketing"
    OPERATIONS = "operations"


class WorkflowStage(str, Enum):
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


class RuleType(str, Enum):
    """Business rule type enumeration."""
    VALIDATION = "validation"
    AUTOMATION = "automation"
    NOTIFICATION = "notification"


class WorkflowBase(BaseModel):
    """Base workflow schema with common fields."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    type: WorkflowType
    stages: Dict[str, Any] = Field(..., description="JSON configuration of stages")
    rules: Optional[Dict[str, Any]] = Field(None, description="JSON configuration of business rules")
    is_active: bool = True


class WorkflowCreate(WorkflowBase):
    """Schema for workflow creation."""
    
    @validator('name')
    def validate_name(cls, v):
        """Validate workflow name."""
        if not v or not v.strip():
            raise ValueError('Workflow name is required')
        if len(v) > 255:
            raise ValueError('Workflow name is too long (max 255 characters)')
        return v.strip()
    
    @validator('stages')
    def validate_stages(cls, v):
        """Validate stages configuration."""
        if not isinstance(v, dict):
            raise ValueError('Stages must be a JSON object')
        if not v:
            raise ValueError('At least one stage must be defined')
        return v


class WorkflowUpdate(BaseModel):
    """Schema for workflow updates."""
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[WorkflowType] = None
    stages: Optional[Dict[str, Any]] = None
    rules: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    
    @validator('name')
    def validate_name(cls, v):
        """Validate workflow name if provided."""
        if v is not None:
            if not v.strip():
                raise ValueError('Workflow name cannot be empty')
            if len(v) > 255:
                raise ValueError('Workflow name is too long (max 255 characters)')
            return v.strip()
        return v


class WorkflowResponse(WorkflowBase):
    """Schema for workflow response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class WorkflowList(BaseModel):
    """Schema for paginated workflow list response."""
    items: List[WorkflowResponse]
    total: int
    page: int
    size: int
    pages: int


class WorkflowInstanceBase(BaseModel):
    """Base workflow instance schema with common fields."""
    workflow_id: int
    project_id: int
    current_stage: str = Field(..., min_length=1, max_length=100)
    stage_data: Optional[Dict[str, Any]] = None
    history: Optional[List[Dict[str, Any]]] = None
    is_completed: bool = False


class WorkflowInstanceCreate(WorkflowInstanceBase):
    """Schema for workflow instance creation."""
    
    @validator('current_stage')
    def validate_current_stage(cls, v):
        """Validate current stage."""
        if not v or not v.strip():
            raise ValueError('Current stage is required')
        return v.strip()


class WorkflowInstanceUpdate(BaseModel):
    """Schema for workflow instance updates."""
    current_stage: Optional[str] = None
    stage_data: Optional[Dict[str, Any]] = None
    history: Optional[List[Dict[str, Any]]] = None
    is_completed: Optional[bool] = None
    
    @validator('current_stage')
    def validate_current_stage(cls, v):
        """Validate current stage if provided."""
        if v is not None:
            if not v.strip():
                raise ValueError('Current stage cannot be empty')
            return v.strip()
        return v


class WorkflowInstanceResponse(WorkflowInstanceBase):
    """Schema for workflow instance response."""
    id: int
    workflow: Optional[WorkflowResponse] = None
    project: Optional[ProjectResponse] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class WorkflowInstanceList(BaseModel):
    """Schema for paginated workflow instance list response."""
    items: List[WorkflowInstanceResponse]
    total: int
    page: int
    size: int
    pages: int


class BusinessRuleBase(BaseModel):
    """Base business rule schema with common fields."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    rule_type: RuleType
    conditions: Dict[str, Any] = Field(..., description="JSON conditions for rule evaluation")
    actions: Dict[str, Any] = Field(..., description="JSON actions to take")
    is_active: bool = True


class BusinessRuleCreate(BusinessRuleBase):
    """Schema for business rule creation."""
    
    @validator('name')
    def validate_name(cls, v):
        """Validate rule name."""
        if not v or not v.strip():
            raise ValueError('Rule name is required')
        if len(v) > 255:
            raise ValueError('Rule name is too long (max 255 characters)')
        return v.strip()
    
    @validator('conditions')
    def validate_conditions(cls, v):
        """Validate conditions configuration."""
        if not isinstance(v, dict):
            raise ValueError('Conditions must be a JSON object')
        return v
    
    @validator('actions')
    def validate_actions(cls, v):
        """Validate actions configuration."""
        if not isinstance(v, dict):
            raise ValueError('Actions must be a JSON object')
        return v


class BusinessRuleUpdate(BaseModel):
    """Schema for business rule updates."""
    name: Optional[str] = None
    description: Optional[str] = None
    rule_type: Optional[RuleType] = None
    conditions: Optional[Dict[str, Any]] = None
    actions: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    
    @validator('name')
    def validate_name(cls, v):
        """Validate rule name if provided."""
        if v is not None:
            if not v.strip():
                raise ValueError('Rule name cannot be empty')
            if len(v) > 255:
                raise ValueError('Rule name is too long (max 255 characters)')
            return v.strip()
        return v


class BusinessRuleResponse(BusinessRuleBase):
    """Schema for business rule response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BusinessRuleList(BaseModel):
    """Schema for paginated business rule list response."""
    items: List[BusinessRuleResponse]
    total: int
    page: int
    size: int
    pages: int


class WorkflowStatistics(BaseModel):
    """Schema for workflow statistics."""
    total_workflows: int
    active_workflows: int
    completed_workflows: int
    workflows_by_type: Dict[str, int]
    workflows_by_stage: Dict[str, int]
    recent_workflows: List[WorkflowResponse]


class WorkflowStageTransition(BaseModel):
    """Schema for workflow stage transitions."""
    from_stage: str
    to_stage: str
    transition_data: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    triggered_by: Optional[int] = None  # User ID who triggered the transition


class NotificationConfig(BaseModel):
    """Schema for notification configuration."""
    email_enabled: bool = True
    in_app_enabled: bool = True
    slack_enabled: bool = False
    recipients: List[str] = Field(default_factory=list)
    template: Optional[str] = None


class AutomationConfig(BaseModel):
    """Schema for automation configuration."""
    trigger_events: List[str] = Field(default_factory=list)
    conditions: Dict[str, Any] = Field(default_factory=dict)
    actions: List[Dict[str, Any]] = Field(default_factory=list)
    is_active: bool = True 