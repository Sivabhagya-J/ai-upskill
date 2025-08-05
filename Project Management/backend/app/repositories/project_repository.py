"""
Project repository for project-related data access operations.
"""

from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_

from .base import BaseRepository
from ..models.project import Project
from ..schemas.project import ProjectCreate, ProjectUpdate


class ProjectRepository(BaseRepository[Project]):
    """
    Project repository with project-specific data access operations.
    """
    
    def __init__(self, db: Session):
        super().__init__(db, Project)
    
    def get(self, id: int) -> Optional[Project]:
        """
        Get project by ID with tasks loaded.
        
        Args:
            id: Project ID
            
        Returns:
            Optional[Project]: Project if found, None otherwise
        """
        return (
            self.db.query(Project)
            .options(joinedload(Project.tasks))
            .filter(Project.id == id)
            .first()
        )
    
    def get_user_projects(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Project]:
        """
        Get projects owned by a specific user.
        
        Args:
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Project]: List of user's projects
        """
        return (
            self.db.query(Project)
            .options(joinedload(Project.tasks))
            .filter(Project.owner_id == user_id)
            .order_by(Project.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def count_user_projects(self, user_id: int) -> int:
        """
        Count projects owned by a specific user.
        
        Args:
            user_id: User ID
            
        Returns:
            int: Number of user's projects
        """
        return (
            self.db.query(Project)
            .filter(Project.owner_id == user_id)
            .count()
        )
    
    def get_active_projects(self, user_id: int) -> List[Project]:
        """
        Get active projects owned by a specific user.
        
        Args:
            user_id: User ID
            
        Returns:
            List[Project]: List of active projects
        """
        return (
            self.db.query(Project)
            .options(joinedload(Project.tasks))
            .filter(
                and_(
                    Project.owner_id == user_id,
                    Project.status.in_(["planning", "in_progress"])
                )
            )
            .order_by(Project.created_at.desc())
            .all()
        )
    
    def get_projects_by_status(
        self,
        user_id: int,
        status: str
    ) -> List[Project]:
        """
        Get projects by status for a specific user.
        
        Args:
            user_id: User ID
            status: Project status
            
        Returns:
            List[Project]: List of projects with specified status
        """
        return (
            self.db.query(Project)
            .options(joinedload(Project.tasks))
            .filter(
                and_(
                    Project.owner_id == user_id,
                    Project.status == status
                )
            )
            .order_by(Project.created_at.desc())
            .all()
        )
    
    def search_projects(
        self,
        user_id: int,
        search_term: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Project]:
        """
        Search projects by name or description for a specific user.
        
        Args:
            user_id: User ID
            search_term: Search term
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Project]: List of matching projects
        """
        return (
            self.db.query(Project)
            .options(joinedload(Project.tasks))
            .filter(
                and_(
                    Project.owner_id == user_id,
                    Project.name.ilike(f"%{search_term}%")
                )
            )
            .order_by(Project.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create_project(
        self,
        project_data: ProjectCreate,
        owner_id: int
    ) -> Project:
        """
        Create a new project with owner.
        
        Args:
            project_data: Project creation data
            owner_id: Owner user ID
            
        Returns:
            Project: Created project
        """
        from datetime import datetime
        
        project_dict = project_data.dict()
        project_dict["owner_id"] = owner_id
        
        # Convert string dates to datetime objects
        if project_dict.get("start_date") and isinstance(project_dict["start_date"], str):
            try:
                # Handle both YYYY-MM-DD and ISO format
                date_str = project_dict["start_date"]
                if len(date_str) == 10:  # YYYY-MM-DD format
                    project_dict["start_date"] = datetime.strptime(date_str, "%Y-%m-%d")
                else:  # ISO format
                    project_dict["start_date"] = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except ValueError:
                project_dict["start_date"] = None
        
        if project_dict.get("end_date") and isinstance(project_dict["end_date"], str):
            try:
                # Handle both YYYY-MM-DD and ISO format
                date_str = project_dict["end_date"]
                if len(date_str) == 10:  # YYYY-MM-DD format
                    project_dict["end_date"] = datetime.strptime(date_str, "%Y-%m-%d")
                else:  # ISO format
                    project_dict["end_date"] = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except ValueError:
                project_dict["end_date"] = None
        
        db_project = Project(**project_dict)
        self.db.add(db_project)
        self.db.commit()
        self.db.refresh(db_project)
        return db_project
    
    def get_project_statistics(self, user_id: int) -> dict:
        """
        Get project statistics for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            dict: Project statistics
        """
        total_projects = self.count_user_projects(user_id)
        
        active_projects = (
            self.db.query(Project)
            .filter(
                and_(
                    Project.owner_id == user_id,
                    Project.status.in_(["planning", "in_progress"])
                )
            )
            .count()
        )
        
        completed_projects = (
            self.db.query(Project)
            .filter(
                and_(
                    Project.owner_id == user_id,
                    Project.status == "completed"
                )
            )
            .count()
        )
        
        projects_by_status = {}
        status_counts = (
            self.db.query(Project.status, self.db.func.count(Project.id))
            .filter(Project.owner_id == user_id)
            .group_by(Project.status)
            .all()
        )
        
        for status, count in status_counts:
            projects_by_status[status] = count
        
        recent_projects = (
            self.db.query(Project)
            .options(joinedload(Project.tasks))
            .filter(Project.owner_id == user_id)
            .order_by(Project.created_at.desc())
            .limit(5)
            .all()
        )
        
        return {
            "total_projects": total_projects,
            "active_projects": active_projects,
            "completed_projects": completed_projects,
            "projects_by_status": projects_by_status,
            "recent_projects": recent_projects
        }
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """
        Get all projects.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Project]: List of all projects
        """
        return (
            self.db.query(Project)
            .options(joinedload(Project.tasks))
            .order_by(Project.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def count(self) -> int:
        """
        Count total projects.
        
        Returns:
            int: Total number of projects
        """
        return self.db.query(Project).count()
    
    def count_active(self) -> int:
        """
        Count active projects.
        
        Returns:
            int: Number of active projects
        """
        return (
            self.db.query(Project)
            .filter(Project.status.in_(["planning", "in_progress"]))
            .count()
        )
    
    def update_project(
        self,
        project: Project,
        project_update: ProjectUpdate
    ) -> Project:
        """
        Update a project.
        
        Args:
            project: Project to update
            project_update: Update data
            
        Returns:
            Project: Updated project
        """
        from datetime import datetime
        
        update_dict = project_update.dict(exclude_unset=True)
        
        # Convert string dates to datetime objects
        if update_dict.get("start_date") and isinstance(update_dict["start_date"], str):
            try:
                # Handle both YYYY-MM-DD and ISO format
                date_str = update_dict["start_date"]
                if len(date_str) == 10:  # YYYY-MM-DD format
                    update_dict["start_date"] = datetime.strptime(date_str, "%Y-%m-%d")
                else:  # ISO format
                    update_dict["start_date"] = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except ValueError:
                update_dict["start_date"] = None
        
        if update_dict.get("end_date") and isinstance(update_dict["end_date"], str):
            try:
                # Handle both YYYY-MM-DD and ISO format
                date_str = update_dict["end_date"]
                if len(date_str) == 10:  # YYYY-MM-DD format
                    update_dict["end_date"] = datetime.strptime(date_str, "%Y-%m-%d")
                else:  # ISO format
                    update_dict["end_date"] = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except ValueError:
                update_dict["end_date"] = None
        
        # Update project attributes
        for key, value in update_dict.items():
            setattr(project, key, value)
        
        self.db.commit()
        self.db.refresh(project)
        return project 