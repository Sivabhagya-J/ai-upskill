"""
Tasks API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.user import User
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskList
from ..repositories.task_repository import TaskRepository
from ..api.deps import get_current_active_user


router = APIRouter()


@router.get("/", response_model=TaskList)
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get list of user's tasks.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        TaskList: Paginated list of tasks
    """
    task_repo = TaskRepository(db)
    tasks = task_repo.get_user_tasks(
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    total = task_repo.count_user_tasks(current_user.id)
    
    return TaskList(
        items=[TaskResponse.from_orm(task) for task in tasks],
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/my-tasks", response_model=TaskList)
async def get_my_tasks(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get list of tasks assigned to current user.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        TaskList: Paginated list of assigned tasks
    """
    task_repo = TaskRepository(db)
    tasks = task_repo.get_assigned_tasks(
        assignee_id=current_user.id,
        skip=skip,
        limit=limit
    )
    total = task_repo.count_assigned_tasks(current_user.id)
    
    return TaskList(
        items=[TaskResponse.from_orm(task) for task in tasks],
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new task.
    
    Args:
        task_data: Task creation data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        TaskResponse: Created task information
        
    Raises:
        HTTPException: If validation fails or project not found
    """
    from ..repositories.project_repository import ProjectRepository
    
    task_repo = TaskRepository(db)
    project_repo = ProjectRepository(db)
    
    # Validate that the project exists and user has access to it
    project = project_repo.get(task_data.project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to create tasks in this project"
        )
    
    # Validate assignee_id if provided
    if task_data.assignee_id is not None:
        from ..repositories.user_repository import UserRepository
        user_repo = UserRepository(db)
        assignee = user_repo.get(task_data.assignee_id)
        if not assignee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assignee not found"
            )
    
    # Create the task
    task = task_repo.create_task(task_data, current_user.id)
    return TaskResponse.from_orm(task)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get task by ID.
    
    Args:
        task_id: Task ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        TaskResponse: Task information
        
    Raises:
        HTTPException: If task not found or access denied
    """
    task_repo = TaskRepository(db)
    task = task_repo.get(task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    

    return TaskResponse.from_orm(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update task.
    
    Args:
        task_id: Task ID
        task_update: Task update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        TaskResponse: Updated task information
        
    Raises:
        HTTPException: If task not found, access denied, or validation fails
    """
    task_repo = TaskRepository(db)
    task = task_repo.get(task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Validate assignee_id if provided
    if task_update.assignee_id is not None:
        from ..repositories.user_repository import UserRepository
        user_repo = UserRepository(db)
        assignee = user_repo.get(task_update.assignee_id)
        if not assignee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assignee not found"
            )
    
    # Update task
    updated_task = task_repo.update(task, task_update)
    return TaskResponse.from_orm(updated_task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete task.
    
    Args:
        task_id: Task ID
        current_user: Current authenticated user
        db: Database session
        
    Raises:
        HTTPException: If task not found or access denied
    """
    task_repo = TaskRepository(db)
    task = task_repo.get(task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    

    
    # Delete task
    task_repo.delete(task_id) 