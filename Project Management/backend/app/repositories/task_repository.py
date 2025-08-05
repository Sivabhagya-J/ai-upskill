"""
Task repository for task-related data access operations.
"""

from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_

from .base import BaseRepository
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate


class TaskRepository(BaseRepository[Task]):
    """
    Task repository with task-specific data access operations.
    """
    
    def __init__(self, db: Session):
        super().__init__(db, Task)
    
    def get(self, id: int) -> Optional[Task]:
        """
        Get task by ID with relationships loaded.
        
        Args:
            id: Task ID
            
        Returns:
            Optional[Task]: Task if found, None otherwise
        """
        return (
            self.db.query(Task)
            .options(joinedload(Task.project), joinedload(Task.assignee))
            .filter(Task.id == id)
            .first()
        )
    
    def get_user_tasks(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """
        Get tasks from projects owned by a specific user.
        
        Args:
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Task]: List of user's tasks
        """
        return (
            self.db.query(Task)
            .options(joinedload(Task.project), joinedload(Task.assignee))
            .join(Task.project)
            .filter(Task.project.has(owner_id=user_id))
            .order_by(Task.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def count_user_tasks(self, user_id: int) -> int:
        """
        Count tasks from projects owned by a specific user.
        
        Args:
            user_id: User ID
            
        Returns:
            int: Number of user's tasks
        """
        return (
            self.db.query(Task)
            .join(Task.project)
            .filter(Task.project.has(owner_id=user_id))
            .count()
        )
    
    def get_assigned_tasks(
        self,
        assignee_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """
        Get tasks assigned to a specific user.
        
        Args:
            assignee_id: Assignee user ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Task]: List of assigned tasks
        """
        return (
            self.db.query(Task)
            .options(joinedload(Task.project), joinedload(Task.assignee))
            .filter(Task.assignee_id == assignee_id)
            .order_by(Task.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def count_assigned_tasks(self, assignee_id: int) -> int:
        """
        Count tasks assigned to a specific user.
        
        Args:
            assignee_id: Assignee user ID
            
        Returns:
            int: Number of assigned tasks
        """
        return (
            self.db.query(Task)
            .filter(Task.assignee_id == assignee_id)
            .count()
        )
    
    def get_project_tasks(
        self,
        project_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """
        Get tasks for a specific project.
        
        Args:
            project_id: Project ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Task]: List of project tasks
        """
        return (
            self.db.query(Task)
            .options(joinedload(Task.project), joinedload(Task.assignee))
            .filter(Task.project_id == project_id)
            .order_by(Task.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_tasks_by_status(
        self,
        user_id: int,
        status: str
    ) -> List[Task]:
        """
        Get tasks by status for a specific user.
        
        Args:
            user_id: User ID
            status: Task status
            
        Returns:
            List[Task]: List of tasks with specified status
        """
        return (
            self.db.query(Task)
            .options(joinedload(Task.project), joinedload(Task.assignee))
            .join(Task.project)
            .filter(
                and_(
                    Task.project.has(owner_id=user_id),
                    Task.status == status
                )
            )
            .order_by(Task.created_at.desc())
            .all()
        )
    
    def get_overdue_tasks(self, user_id: int) -> List[Task]:
        """
        Get overdue tasks for a specific user.
        
        Args:
            user_id: User ID
            
        Returns:
            List[Task]: List of overdue tasks
        """
        from datetime import datetime, timezone
        
        # Use timezone-aware datetime for comparison
        now = datetime.now(timezone.utc)
        
        return (
            self.db.query(Task)
            .options(joinedload(Task.project), joinedload(Task.assignee))
            .join(Task.project)
            .filter(
                and_(
                    Task.project.has(owner_id=user_id),
                    Task.due_date < now,
                    Task.status.in_(["todo", "in_progress", "review"])
                )
            )
            .order_by(Task.due_date.asc())
            .all()
        )
    
    def search_tasks(
        self,
        user_id: int,
        search_term: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """
        Search tasks by title or description for a specific user.
        
        Args:
            user_id: User ID
            search_term: Search term
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Task]: List of matching tasks
        """
        return (
            self.db.query(Task)
            .options(joinedload(Task.project), joinedload(Task.assignee))
            .join(Task.project)
            .filter(
                and_(
                    Task.project.has(owner_id=user_id),
                    Task.title.ilike(f"%{search_term}%")
                )
            )
            .order_by(Task.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create_task(
        self,
        task_data: TaskCreate,
        creator_id: int
    ) -> Task:
        """
        Create a new task.
        
        Args:
            task_data: Task creation data
            creator_id: Creator user ID
            
        Returns:
            Task: Created task
        """
        from datetime import datetime
        
        task_dict = task_data.dict()
        
        # Convert string dates to datetime objects
        if task_dict.get("due_date") and isinstance(task_dict["due_date"], str):
            try:
                # Handle both YYYY-MM-DD and ISO format
                date_str = task_dict["due_date"]
                if len(date_str) == 10:  # YYYY-MM-DD format
                    task_dict["due_date"] = datetime.strptime(date_str, "%Y-%m-%d")
                else:  # ISO format
                    task_dict["due_date"] = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except ValueError:
                task_dict["due_date"] = None
        
        db_task = Task(**task_dict)
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        
        # Return task with relationships loaded
        return self.get(db_task.id)
    
    def update(self, task: Task, task_update: TaskUpdate) -> Task:
        """
        Update a task with relationships loaded.
        
        Args:
            task: Task to update
            task_update: Update data
            
        Returns:
            Task: Updated task with relationships loaded
        """
        from datetime import datetime
        
        update_dict = task_update.dict(exclude_unset=True)
        
        # Convert string dates to datetime objects
        if update_dict.get("due_date") and isinstance(update_dict["due_date"], str):
            try:
                # Handle both YYYY-MM-DD and ISO format
                date_str = update_dict["due_date"]
                if len(date_str) == 10:  # YYYY-MM-DD format
                    update_dict["due_date"] = datetime.strptime(date_str, "%Y-%m-%d")
                else:  # ISO format
                    update_dict["due_date"] = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except ValueError:
                update_dict["due_date"] = None
        
        # Update task attributes
        for key, value in update_dict.items():
            setattr(task, key, value)
        
        self.db.commit()
        self.db.refresh(task)
        
        # Reload with relationships
        return self.get(task.id)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Get all tasks.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Task]: List of all tasks
        """
        return (
            self.db.query(Task)
            .options(joinedload(Task.project), joinedload(Task.assignee))
            .order_by(Task.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def count(self) -> int:
        """
        Count total tasks.
        
        Returns:
            int: Total number of tasks
        """
        return self.db.query(Task).count()
    
    def count_completed(self) -> int:
        """
        Count completed tasks.
        
        Returns:
            int: Number of completed tasks
        """
        return (
            self.db.query(Task)
            .filter(Task.status == "completed")
            .count()
        )
    
    def get_task_statistics(self, user_id: int) -> dict:
        """
        Get task statistics for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            dict: Task statistics
        """
        total_tasks = self.count_user_tasks(user_id)
        
        completed_tasks = (
            self.db.query(Task)
            .join(Task.project)
            .filter(
                and_(
                    Task.project.has(owner_id=user_id),
                    Task.status == "completed"
                )
            )
            .count()
        )
        
        overdue_tasks = len(self.get_overdue_tasks(user_id))
        
        tasks_by_status = {}
        status_counts = (
            self.db.query(Task.status, self.db.func.count(Task.id))
            .join(Task.project)
            .filter(Task.project.has(owner_id=user_id))
            .group_by(Task.status)
            .all()
        )
        
        for status, count in status_counts:
            tasks_by_status[status] = count
        
        tasks_by_priority = {}
        priority_counts = (
            self.db.query(Task.priority, self.db.func.count(Task.id))
            .join(Task.project)
            .filter(Task.project.has(owner_id=user_id))
            .group_by(Task.priority)
            .all()
        )
        
        for priority, count in priority_counts:
            tasks_by_priority[priority] = count
        
        recent_tasks = (
            self.db.query(Task)
            .join(Task.project)
            .filter(Task.project.has(owner_id=user_id))
            .order_by(Task.created_at.desc())
            .limit(5)
            .all()
        )
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "overdue_tasks": overdue_tasks,
            "tasks_by_status": tasks_by_status,
            "tasks_by_priority": tasks_by_priority,
            "recent_tasks": recent_tasks
        } 