"""
Analytics API routes for dashboard data and reporting.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import json

from ..database import get_db
from ..models.user import User
from ..services.analytics_service import AnalyticsService
from ..api.deps import get_current_active_user

router = APIRouter()


@router.get("/dashboard/overview")
async def get_dashboard_overview(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get dashboard overview statistics.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dict containing dashboard overview data
    """
    analytics_service = AnalyticsService(db)
    return analytics_service.get_dashboard_overview(current_user.id)


@router.get("/projects/{project_id}/analytics")
async def get_project_analytics(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed analytics for a specific project.
    
    Args:
        project_id: Project ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dict containing project analytics
    """
    analytics_service = AnalyticsService(db)
    analytics = analytics_service.get_project_analytics(project_id)
    
    if not analytics:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    return analytics


@router.get("/users/{user_id}/performance")
async def get_user_performance_analytics(
    user_id: int,
    date_range: Optional[str] = Query(None, description="Date range filter (e.g., '30d', '7d')"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get user performance analytics.
    
    Args:
        user_id: User ID
        date_range: Optional date range filter
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dict containing user performance analytics
    """
    analytics_service = AnalyticsService(db)
    return analytics_service.get_user_performance_analytics(user_id, date_range)


@router.get("/users/me/performance")
async def get_my_performance_analytics(
    date_range: Optional[str] = Query(None, description="Date range filter (e.g., '30d', '7d')"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's performance analytics.
    
    Args:
        date_range: Optional date range filter
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dict containing current user's performance analytics
    """
    analytics_service = AnalyticsService(db)
    return analytics_service.get_user_performance_analytics(current_user.id, date_range)


@router.post("/teams/analytics")
async def get_team_analytics(
    team_members: list[int],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get team analytics.
    
    Args:
        team_members: List of user IDs in the team
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dict containing team analytics
    """
    analytics_service = AnalyticsService(db)
    return analytics_service.get_team_analytics(team_members)


@router.get("/reports/{report_type}")
async def generate_report(
    report_type: str,
    filters: Optional[Dict[str, Any]] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Generate various types of reports.
    
    Args:
        report_type: Type of report to generate
        filters: Optional filters for the report
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dict containing report data
    """
    analytics_service = AnalyticsService(db)
    report = analytics_service.generate_report(report_type, filters)
    
    if "error" in report:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=report["error"])
    
    return report


@router.get("/charts/task-status-distribution")
async def get_task_status_distribution(
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get task status distribution for charts.
    
    Args:
        project_id: Optional project ID filter
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dict containing task status distribution data
    """
    analytics_service = AnalyticsService(db)
    
    if project_id:
        analytics = analytics_service.get_project_analytics(project_id)
        if not analytics:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return {
            "labels": list(analytics["task_statistics"]["status_distribution"].keys()),
            "data": list(analytics["task_statistics"]["status_distribution"].values())
        }
    else:
        # Get overall task status distribution
        from ..repositories.task_repository import TaskRepository
        task_repo = TaskRepository(db)
        all_tasks = task_repo.get_all()
        
        status_distribution = {}
        for task in all_tasks:
            status = task.status
            status_distribution[status] = status_distribution.get(status, 0) + 1
        
        return {
            "labels": list(status_distribution.keys()),
            "data": list(status_distribution.values())
        }


@router.get("/charts/task-priority-distribution")
async def get_task_priority_distribution(
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get task priority distribution for charts.
    
    Args:
        project_id: Optional project ID filter
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dict containing task priority distribution data
    """
    analytics_service = AnalyticsService(db)
    
    if project_id:
        analytics = analytics_service.get_project_analytics(project_id)
        if not analytics:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return {
            "labels": list(analytics["task_statistics"]["priority_distribution"].keys()),
            "data": list(analytics["task_statistics"]["priority_distribution"].values())
        }
    else:
        # Get overall task priority distribution
        from ..repositories.task_repository import TaskRepository
        task_repo = TaskRepository(db)
        all_tasks = task_repo.get_all()
        
        priority_distribution = {}
        for task in all_tasks:
            priority = task.priority
            priority_distribution[priority] = priority_distribution.get(priority, 0) + 1
        
        return {
            "labels": list(priority_distribution.keys()),
            "data": list(priority_distribution.values())
        }


@router.get("/charts/productivity-trends")
async def get_productivity_trends(
    user_id: Optional[int] = Query(None, description="User ID (defaults to current user)"),
    date_range: Optional[str] = Query("30d", description="Date range filter"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get productivity trends for charts.
    
    Args:
        user_id: Optional user ID (defaults to current user)
        date_range: Date range filter
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dict containing productivity trends data
    """
    if user_id is None:
        user_id = current_user.id
    
    analytics_service = AnalyticsService(db)
    analytics = analytics_service.get_user_performance_analytics(user_id, date_range)
    
    return {
        "labels": [trend["date"] for trend in analytics["productivity_trends"]],
        "data": [trend["tasks_completed"] for trend in analytics["productivity_trends"]]
    }


@router.get("/charts/project-progress")
async def get_project_progress(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get project progress for charts.
    
    Args:
        project_id: Project ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dict containing project progress data
    """
    analytics_service = AnalyticsService(db)
    analytics = analytics_service.get_project_analytics(project_id)
    
    if not analytics:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    return {
        "project_name": analytics["project_info"]["name"],
        "progress_percentage": analytics["project_info"]["progress_percentage"],
        "total_tasks": analytics["task_statistics"]["total"],
        "completed_tasks": analytics["task_statistics"]["completed"],
        "active_tasks": analytics["task_statistics"]["active"]
    }


@router.get("/metrics/kpi")
async def get_kpi_metrics(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get KPI metrics for dashboard.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dict containing KPI metrics
    """
    analytics_service = AnalyticsService(db)
    dashboard_data = analytics_service.get_dashboard_overview(current_user.id)
    
    return {
        "project_completion_rate": dashboard_data["projects"]["completion_rate"],
        "task_completion_rate": dashboard_data["tasks"]["completion_rate"],
        "overdue_tasks": dashboard_data["tasks"]["overdue"],
        "total_active_projects": dashboard_data["projects"]["active"],
        "efficiency_rate": dashboard_data["performance_metrics"]["efficiency_rate"]
    }


@router.get("/export/{report_type}")
async def export_report(
    report_type: str,
    format: str = Query("json", description="Export format (json, csv, pdf)"),
    filters: Optional[Dict[str, Any]] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Export reports in various formats.
    
    Args:
        report_type: Type of report to export
        format: Export format
        filters: Optional filters for the report
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Report data in requested format
    """
    analytics_service = AnalyticsService(db)
    report = analytics_service.generate_report(report_type, filters)
    
    if "error" in report:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=report["error"])
    
    if format == "json":
        return report
    elif format == "csv":
        # Convert to CSV format
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        if report_type == "user_productivity":
            writer.writerow(["User ID", "User Name", "Total Tasks", "Completed Tasks", "Completion Rate"])
            for user in report["user_performance"]:
                writer.writerow([
                    user["user_id"],
                    user["user_name"],
                    user["total_tasks"],
                    user["completed_tasks"],
                    f"{user['completion_rate']:.1f}%"
                ])
        
        output.seek(0)
        return {"csv_data": output.getvalue()}
    elif format == "pdf":
        # For PDF export, you would typically use a library like reportlab
        # For now, return the JSON data with a note
        return {
            "message": "PDF export not implemented yet",
            "data": report
        }
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported format") 