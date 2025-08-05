"""
Workflow repository for workflow-related data access operations.
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, func, desc
import json
from datetime import datetime

from .base import BaseRepository
from ..models.workflow import Workflow, WorkflowInstance, BusinessRule, WorkflowType, WorkflowStage
from ..schemas.workflow import (
    WorkflowCreate, WorkflowUpdate, WorkflowInstanceCreate, WorkflowInstanceUpdate,
    BusinessRuleCreate, BusinessRuleUpdate
)


class WorkflowRepository(BaseRepository[Workflow]):
    """
    Workflow repository with workflow-specific data access operations.
    """
    
    def __init__(self, db: Session):
        super().__init__(db, Workflow)
    
    def get(self, id: int) -> Optional[Workflow]:
        """
        Get workflow by ID.
        
        Args:
            id: Workflow ID
            
        Returns:
            Optional[Workflow]: Workflow if found, None otherwise
        """
        return self.db.query(Workflow).filter(Workflow.id == id).first()
    
    def get_by_type(self, workflow_type: WorkflowType) -> List[Workflow]:
        """
        Get workflows by type.
        
        Args:
            workflow_type: Workflow type
            
        Returns:
            List[Workflow]: List of workflows of the specified type
        """
        return (
            self.db.query(Workflow)
            .filter(and_(Workflow.type == workflow_type, Workflow.is_active == True))
            .order_by(desc(Workflow.created_at))
            .all()
        )
    
    def get_active_workflows(self) -> List[Workflow]:
        """
        Get all active workflows.
        
        Returns:
            List[Workflow]: List of active workflows
        """
        return (
            self.db.query(Workflow)
            .filter(Workflow.is_active == True)
            .order_by(desc(Workflow.created_at))
            .all()
        )
    
    def create_workflow(self, workflow_data: WorkflowCreate) -> Workflow:
        """
        Create a new workflow.
        
        Args:
            workflow_data: Workflow creation data
            
        Returns:
            Workflow: Created workflow
        """
        workflow_dict = workflow_data.dict()
        db_workflow = Workflow(**workflow_dict)
        self.db.add(db_workflow)
        self.db.commit()
        self.db.refresh(db_workflow)
        return db_workflow
    
    def update_workflow(self, workflow: Workflow, workflow_update: WorkflowUpdate) -> Workflow:
        """
        Update a workflow.
        
        Args:
            workflow: Workflow to update
            workflow_update: Update data
            
        Returns:
            Workflow: Updated workflow
        """
        update_dict = workflow_update.dict(exclude_unset=True)
        
        for field, value in update_dict.items():
            setattr(workflow, field, value)
        
        self.db.commit()
        self.db.refresh(workflow)
        return workflow
    
    def get_workflow_statistics(self) -> Dict[str, Any]:
        """
        Get workflow statistics.
        
        Returns:
            Dict[str, Any]: Workflow statistics
        """
        total_workflows = self.db.query(Workflow).count()
        active_workflows = self.db.query(Workflow).filter(Workflow.is_active == True).count()
        
        # Get workflows by type
        workflows_by_type = {}
        for workflow_type in WorkflowType:
            count = self.db.query(Workflow).filter(Workflow.type == workflow_type).count()
            workflows_by_type[workflow_type.value] = count
        
        # Get recent workflows
        recent_workflows = (
            self.db.query(Workflow)
            .filter(Workflow.is_active == True)
            .order_by(desc(Workflow.created_at))
            .limit(5)
            .all()
        )
        
        return {
            "total_workflows": total_workflows,
            "active_workflows": active_workflows,
            "workflows_by_type": workflows_by_type,
            "recent_workflows": recent_workflows
        }


class WorkflowInstanceRepository(BaseRepository[WorkflowInstance]):
    """
    Workflow instance repository with workflow instance-specific data access operations.
    """
    
    def __init__(self, db: Session):
        super().__init__(db, WorkflowInstance)
    
    def get(self, id: int) -> Optional[WorkflowInstance]:
        """
        Get workflow instance by ID with relationships loaded.
        
        Args:
            id: Workflow instance ID
            
        Returns:
            Optional[WorkflowInstance]: Workflow instance if found, None otherwise
        """
        return (
            self.db.query(WorkflowInstance)
            .options(joinedload(WorkflowInstance.workflow), joinedload(WorkflowInstance.project))
            .filter(WorkflowInstance.id == id)
            .first()
        )
    
    def get_by_project(self, project_id: int) -> List[WorkflowInstance]:
        """
        Get workflow instances by project ID.
        
        Args:
            project_id: Project ID
            
        Returns:
            List[WorkflowInstance]: List of workflow instances for the project
        """
        return (
            self.db.query(WorkflowInstance)
            .options(joinedload(WorkflowInstance.workflow), joinedload(WorkflowInstance.project))
            .filter(WorkflowInstance.project_id == project_id)
            .order_by(desc(WorkflowInstance.created_at))
            .all()
        )
    
    def get_by_workflow(self, workflow_id: int) -> List[WorkflowInstance]:
        """
        Get workflow instances by workflow ID.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            List[WorkflowInstance]: List of workflow instances for the workflow
        """
        return (
            self.db.query(WorkflowInstance)
            .options(joinedload(WorkflowInstance.workflow), joinedload(WorkflowInstance.project))
            .filter(WorkflowInstance.workflow_id == workflow_id)
            .order_by(desc(WorkflowInstance.created_at))
            .all()
        )
    
    def get_by_stage(self, stage: str) -> List[WorkflowInstance]:
        """
        Get workflow instances by current stage.
        
        Args:
            stage: Current stage
            
        Returns:
            List[WorkflowInstance]: List of workflow instances in the specified stage
        """
        return (
            self.db.query(WorkflowInstance)
            .options(joinedload(WorkflowInstance.workflow), joinedload(WorkflowInstance.project))
            .filter(WorkflowInstance.current_stage == stage)
            .order_by(desc(WorkflowInstance.created_at))
            .all()
        )
    
    def create_workflow_instance(self, instance_data: WorkflowInstanceCreate) -> WorkflowInstance:
        """
        Create a new workflow instance.
        
        Args:
            instance_data: Workflow instance creation data
            
        Returns:
            WorkflowInstance: Created workflow instance
        """
        instance_dict = instance_data.dict()
        db_instance = WorkflowInstance(**instance_dict)
        self.db.add(db_instance)
        self.db.commit()
        self.db.refresh(db_instance)
        
        # Return instance with relationships loaded
        return self.get(db_instance.id)
    
    def update_workflow_instance(self, instance: WorkflowInstance, instance_update: WorkflowInstanceUpdate) -> WorkflowInstance:
        """
        Update a workflow instance.
        
        Args:
            instance: Workflow instance to update
            instance_update: Update data
            
        Returns:
            WorkflowInstance: Updated workflow instance
        """
        update_dict = instance_update.dict(exclude_unset=True)
        
        for field, value in update_dict.items():
            setattr(instance, field, value)
        
        self.db.commit()
        self.db.refresh(instance)
        
        # Return instance with relationships loaded
        return self.get(instance.id)
    
    def transition_stage(self, instance_id: int, new_stage: str, transition_data: Optional[Dict[str, Any]] = None, triggered_by: Optional[int] = None) -> WorkflowInstance:
        """
        Transition workflow instance to a new stage.
        
        Args:
            instance_id: Workflow instance ID
            new_stage: New stage
            transition_data: Optional transition data
            triggered_by: User ID who triggered the transition
            
        Returns:
            WorkflowInstance: Updated workflow instance
        """
        instance = self.get(instance_id)
        if not instance:
            raise ValueError("Workflow instance not found")
        
        # Create transition record
        transition_record = {
            "from_stage": instance.current_stage,
            "to_stage": new_stage,
            "timestamp": datetime.utcnow().isoformat(),
            "triggered_by": triggered_by,
            "data": transition_data or {}
        }
        
        # Update history
        history = instance.history or []
        history.append(transition_record)
        instance.history = history
        
        # Update stage data if provided
        if transition_data:
            current_data = instance.stage_data or {}
            current_data.update(transition_data)
            instance.stage_data = current_data
        
        instance.current_stage = new_stage
        self.db.commit()
        self.db.refresh(instance)
        
        return self.get(instance.id)
    
    def get_workflow_instance_statistics(self) -> Dict[str, Any]:
        """
        Get workflow instance statistics.
        
        Returns:
            Dict[str, Any]: Workflow instance statistics
        """
        total_instances = self.db.query(WorkflowInstance).count()
        completed_instances = self.db.query(WorkflowInstance).filter(WorkflowInstance.is_completed == True).count()
        
        # Get instances by stage
        instances_by_stage = {}
        for stage in WorkflowStage:
            count = self.db.query(WorkflowInstance).filter(WorkflowInstance.current_stage == stage.value).count()
            instances_by_stage[stage.value] = count
        
        return {
            "total_instances": total_instances,
            "completed_instances": completed_instances,
            "instances_by_stage": instances_by_stage
        }


class BusinessRuleRepository(BaseRepository[BusinessRule]):
    """
    Business rule repository with business rule-specific data access operations.
    """
    
    def __init__(self, db: Session):
        super().__init__(db, BusinessRule)
    
    def get(self, id: int) -> Optional[BusinessRule]:
        """
        Get business rule by ID.
        
        Args:
            id: Business rule ID
            
        Returns:
            Optional[BusinessRule]: Business rule if found, None otherwise
        """
        return self.db.query(BusinessRule).filter(BusinessRule.id == id).first()
    
    def get_by_type(self, rule_type: str) -> List[BusinessRule]:
        """
        Get business rules by type.
        
        Args:
            rule_type: Rule type
            
        Returns:
            List[BusinessRule]: List of business rules of the specified type
        """
        return (
            self.db.query(BusinessRule)
            .filter(and_(BusinessRule.rule_type == rule_type, BusinessRule.is_active == True))
            .order_by(desc(BusinessRule.created_at))
            .all()
        )
    
    def get_active_rules(self) -> List[BusinessRule]:
        """
        Get all active business rules.
        
        Returns:
            List[BusinessRule]: List of active business rules
        """
        return (
            self.db.query(BusinessRule)
            .filter(BusinessRule.is_active == True)
            .order_by(desc(BusinessRule.created_at))
            .all()
        )
    
    def create_business_rule(self, rule_data: BusinessRuleCreate) -> BusinessRule:
        """
        Create a new business rule.
        
        Args:
            rule_data: Business rule creation data
            
        Returns:
            BusinessRule: Created business rule
        """
        rule_dict = rule_data.dict()
        db_rule = BusinessRule(**rule_dict)
        self.db.add(db_rule)
        self.db.commit()
        self.db.refresh(db_rule)
        return db_rule
    
    def update_business_rule(self, rule: BusinessRule, rule_update: BusinessRuleUpdate) -> BusinessRule:
        """
        Update a business rule.
        
        Args:
            rule: Business rule to update
            rule_update: Update data
            
        Returns:
            BusinessRule: Updated business rule
        """
        update_dict = rule_update.dict(exclude_unset=True)
        
        for field, value in update_dict.items():
            setattr(rule, field, value)
        
        self.db.commit()
        self.db.refresh(rule)
        return rule
    
    def evaluate_rules(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Evaluate business rules against a context.
        
        Args:
            context: Context data for rule evaluation
            
        Returns:
            List[Dict[str, Any]]: List of triggered rules and their actions
        """
        active_rules = self.get_active_rules()
        triggered_rules = []
        
        for rule in active_rules:
            if self._evaluate_conditions(rule.conditions, context):
                triggered_rules.append({
                    "rule_id": rule.id,
                    "rule_name": rule.name,
                    "rule_type": rule.rule_type,
                    "actions": rule.actions
                })
        
        return triggered_rules
    
    def _evaluate_conditions(self, conditions: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """
        Evaluate rule conditions against context.
        
        Args:
            conditions: Rule conditions
            context: Context data
            
        Returns:
            bool: True if conditions are met, False otherwise
        """
        # Simple condition evaluation - can be extended with more complex logic
        for key, expected_value in conditions.items():
            if key not in context:
                return False
            if context[key] != expected_value:
                return False
        return True 