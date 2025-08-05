"""
Projects API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.user import User
from ..models.project import Project
from ..schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectList
from ..repositories.project_repository import ProjectRepository
from ..api.deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=ProjectList)
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get list of user's projects.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ProjectList: Paginated list of projects
    """
    project_repo = ProjectRepository(db)
    projects = project_repo.get_user_projects(
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    total = project_repo.count_user_projects(current_user.id)
    
    return ProjectList(
        items=[ProjectResponse.from_orm(project) for project in projects],
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new project.
    
    Args:
        project_data: Project creation data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ProjectResponse: Created project information
        
    Raises:
        HTTPException: If validation fails
    """
    project_repo = ProjectRepository(db)
    
    # Create project with current user as owner
    project = project_repo.create_project(project_data, current_user.id)
    return ProjectResponse.from_orm(project)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get project by ID.
    
    Args:
        project_id: Project ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ProjectResponse: Project information
        
    Raises:
        HTTPException: If project not found or access denied
    """
    project_repo = ProjectRepository(db)
    project = project_repo.get(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check if user has access to this project
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return ProjectResponse.from_orm(project)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update project.
    
    Args:
        project_id: Project ID
        project_update: Project update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ProjectResponse: Updated project information
        
    Raises:
        HTTPException: If project not found, access denied, or validation fails
    """
    project_repo = ProjectRepository(db)
    project = project_repo.get(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check if user has access to this project
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update project
    updated_project = project_repo.update_project(project, project_update)
    return ProjectResponse.from_orm(updated_project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete project.
    
    Args:
        project_id: Project ID
        current_user: Current authenticated user
        db: Database session
        
    Raises:
        HTTPException: If project not found or access denied
    """
    project_repo = ProjectRepository(db)
    project = project_repo.get(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check if user has access to this project
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Delete project
    project_repo.delete(project_id) 