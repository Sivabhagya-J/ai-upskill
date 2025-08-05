"""
Workflows API routes for business logic and automation.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json

from ..database import get_db
from ..models.user import User
from ..models.workflow import Workflow, WorkflowInstance, BusinessRule
from ..schemas.workflow import (
    WorkflowCreate, WorkflowUpdate, WorkflowResponse, WorkflowList,
    WorkflowInstanceCreate, WorkflowInstanceUpdate, WorkflowInstanceResponse, WorkflowInstanceList,
    BusinessRuleCreate, BusinessRuleUpdate, BusinessRuleResponse, BusinessRuleList,
    WorkflowStatistics, WorkflowStageTransition
)
from ..repositories.workflow_repository import WorkflowRepository, WorkflowInstanceRepository, BusinessRuleRepository
from ..api.deps import get_current_active_user

router = APIRouter()


# Workflow endpoints
@router.get("/", response_model=WorkflowList)
async def get_workflows(
    skip: int = 0,
    limit: int = 100,
    workflow_type: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get list of workflows.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        workflow_type: Filter by workflow type
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        WorkflowList: Paginated list of workflows
    """
    workflow_repo = WorkflowRepository(db)
    
    if workflow_type:
        from ..models.workflow import WorkflowType
        try:
            workflow_type_enum = WorkflowType(workflow_type)
            workflows = workflow_repo.get_by_type(workflow_type_enum)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid workflow type")
    else:
        workflows = workflow_repo.get_active_workflows()
    
    total = len(workflows)
    paginated_workflows = workflows[skip:skip + limit]
    
    return WorkflowList(
        items=[WorkflowResponse.from_orm(workflow) for workflow in paginated_workflows],
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.post("/", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    workflow_data: WorkflowCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new workflow.
    
    Args:
        workflow_data: Workflow creation data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        WorkflowResponse: Created workflow information
    """
    workflow_repo = WorkflowRepository(db)
    workflow = workflow_repo.create_workflow(workflow_data)
    return WorkflowResponse.from_orm(workflow)


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get workflow by ID.
    
    Args:
        workflow_id: Workflow ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        WorkflowResponse: Workflow information
    """
    workflow_repo = WorkflowRepository(db)
    workflow = workflow_repo.get(workflow_id)
    
    if not workflow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    
    return WorkflowResponse.from_orm(workflow)


@router.put("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: int,
    workflow_update: WorkflowUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update workflow.
    
    Args:
        workflow_id: Workflow ID
        workflow_update: Workflow update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        WorkflowResponse: Updated workflow information
    """
    workflow_repo = WorkflowRepository(db)
    workflow = workflow_repo.get(workflow_id)
    
    if not workflow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    
    updated_workflow = workflow_repo.update_workflow(workflow, workflow_update)
    return WorkflowResponse.from_orm(updated_workflow)


@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workflow(
    workflow_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete workflow.
    
    Args:
        workflow_id: Workflow ID
        current_user: Current authenticated user
        db: Database session
    """
    workflow_repo = WorkflowRepository(db)
    workflow = workflow_repo.get(workflow_id)
    
    if not workflow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    
    workflow_repo.delete(workflow_id)


@router.get("/statistics/overview", response_model=WorkflowStatistics)
async def get_workflow_statistics(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get workflow statistics.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        WorkflowStatistics: Workflow statistics
    """
    workflow_repo = WorkflowRepository(db)
    stats = workflow_repo.get_workflow_statistics()
    
    return WorkflowStatistics(
        total_workflows=stats["total_workflows"],
        active_workflows=stats["active_workflows"],
        completed_workflows=0,  # This would need to be calculated based on completed instances
        workflows_by_type=stats["workflows_by_type"],
        workflows_by_stage={},  # This would need to be calculated from instances
        recent_workflows=[WorkflowResponse.from_orm(wf) for wf in stats["recent_workflows"]]
    )


# Workflow Instance endpoints
@router.get("/instances/", response_model=WorkflowInstanceList)
async def get_workflow_instances(
    skip: int = 0,
    limit: int = 100,
    project_id: int = None,
    workflow_id: int = None,
    stage: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get list of workflow instances.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        project_id: Filter by project ID
        workflow_id: Filter by workflow ID
        stage: Filter by current stage
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        WorkflowInstanceList: Paginated list of workflow instances
    """
    instance_repo = WorkflowInstanceRepository(db)
    
    if project_id:
        instances = instance_repo.get_by_project(project_id)
    elif workflow_id:
        instances = instance_repo.get_by_workflow(workflow_id)
    elif stage:
        instances = instance_repo.get_by_stage(stage)
    else:
        instances = instance_repo.get_all(skip=skip, limit=limit)
    
    total = len(instances)
    paginated_instances = instances[skip:skip + limit]
    
    return WorkflowInstanceList(
        items=[WorkflowInstanceResponse.from_orm(instance) for instance in paginated_instances],
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.post("/instances/", response_model=WorkflowInstanceResponse, status_code=status.HTTP_201_CREATED)
async def create_workflow_instance(
    instance_data: WorkflowInstanceCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new workflow instance.
    
    Args:
        instance_data: Workflow instance creation data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        WorkflowInstanceResponse: Created workflow instance information
    """
    instance_repo = WorkflowInstanceRepository(db)
    
    # Validate that the workflow exists
    workflow_repo = WorkflowRepository(db)
    workflow = workflow_repo.get(instance_data.workflow_id)
    if not workflow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    
    # Validate that the project exists
    from ..repositories.project_repository import ProjectRepository
    project_repo = ProjectRepository(db)
    project = project_repo.get(instance_data.project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    instance = instance_repo.create_workflow_instance(instance_data)
    return WorkflowInstanceResponse.from_orm(instance)


@router.get("/instances/{instance_id}", response_model=WorkflowInstanceResponse)
async def get_workflow_instance(
    instance_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get workflow instance by ID.
    
    Args:
        instance_id: Workflow instance ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        WorkflowInstanceResponse: Workflow instance information
    """
    instance_repo = WorkflowInstanceRepository(db)
    instance = instance_repo.get(instance_id)
    
    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow instance not found")
    
    return WorkflowInstanceResponse.from_orm(instance)


@router.put("/instances/{instance_id}", response_model=WorkflowInstanceResponse)
async def update_workflow_instance(
    instance_id: int,
    instance_update: WorkflowInstanceUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update workflow instance.
    
    Args:
        instance_id: Workflow instance ID
        instance_update: Workflow instance update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        WorkflowInstanceResponse: Updated workflow instance information
    """
    instance_repo = WorkflowInstanceRepository(db)
    instance = instance_repo.get(instance_id)
    
    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow instance not found")
    
    updated_instance = instance_repo.update_workflow_instance(instance, instance_update)
    return WorkflowInstanceResponse.from_orm(updated_instance)


@router.post("/instances/{instance_id}/transition", response_model=WorkflowInstanceResponse)
async def transition_workflow_stage(
    instance_id: int,
    transition_data: WorkflowStageTransition,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Transition workflow instance to a new stage.
    
    Args:
        instance_id: Workflow instance ID
        transition_data: Stage transition data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        WorkflowInstanceResponse: Updated workflow instance information
    """
    instance_repo = WorkflowInstanceRepository(db)
    
    # Validate that the instance exists
    instance = instance_repo.get(instance_id)
    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow instance not found")
    
    # Transition to new stage
    updated_instance = instance_repo.transition_stage(
        instance_id=instance_id,
        new_stage=transition_data.to_stage,
        transition_data=transition_data.transition_data,
        triggered_by=current_user.id
    )
    
    return WorkflowInstanceResponse.from_orm(updated_instance)


# Business Rule endpoints
@router.get("/rules/", response_model=BusinessRuleList)
async def get_business_rules(
    skip: int = 0,
    limit: int = 100,
    rule_type: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get list of business rules.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        rule_type: Filter by rule type
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        BusinessRuleList: Paginated list of business rules
    """
    rule_repo = BusinessRuleRepository(db)
    
    if rule_type:
        rules = rule_repo.get_by_type(rule_type)
    else:
        rules = rule_repo.get_active_rules()
    
    total = len(rules)
    paginated_rules = rules[skip:skip + limit]
    
    return BusinessRuleList(
        items=[BusinessRuleResponse.from_orm(rule) for rule in paginated_rules],
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.post("/rules/", response_model=BusinessRuleResponse, status_code=status.HTTP_201_CREATED)
async def create_business_rule(
    rule_data: BusinessRuleCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new business rule.
    
    Args:
        rule_data: Business rule creation data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        BusinessRuleResponse: Created business rule information
    """
    rule_repo = BusinessRuleRepository(db)
    rule = rule_repo.create_business_rule(rule_data)
    return BusinessRuleResponse.from_orm(rule)


@router.get("/rules/{rule_id}", response_model=BusinessRuleResponse)
async def get_business_rule(
    rule_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get business rule by ID.
    
    Args:
        rule_id: Business rule ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        BusinessRuleResponse: Business rule information
    """
    rule_repo = BusinessRuleRepository(db)
    rule = rule_repo.get(rule_id)
    
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business rule not found")
    
    return BusinessRuleResponse.from_orm(rule)


@router.put("/rules/{rule_id}", response_model=BusinessRuleResponse)
async def update_business_rule(
    rule_id: int,
    rule_update: BusinessRuleUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update business rule.
    
    Args:
        rule_id: Business rule ID
        rule_update: Business rule update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        BusinessRuleResponse: Updated business rule information
    """
    rule_repo = BusinessRuleRepository(db)
    rule = rule_repo.get(rule_id)
    
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business rule not found")
    
    updated_rule = rule_repo.update_business_rule(rule, rule_update)
    return BusinessRuleResponse.from_orm(updated_rule)


@router.delete("/rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_business_rule(
    rule_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete business rule.
    
    Args:
        rule_id: Business rule ID
        current_user: Current authenticated user
        db: Database session
    """
    rule_repo = BusinessRuleRepository(db)
    rule = rule_repo.get(rule_id)
    
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business rule not found")
    
    rule_repo.delete(rule_id)


@router.post("/rules/evaluate")
async def evaluate_business_rules(
    context: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Evaluate business rules against a context.
    
    Args:
        context: Context data for rule evaluation
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of triggered rules and their actions
    """
    rule_repo = BusinessRuleRepository(db)
    triggered_rules = rule_repo.evaluate_rules(context)
    
    return {
        "triggered_rules": triggered_rules,
        "total_triggered": len(triggered_rules)
    } 