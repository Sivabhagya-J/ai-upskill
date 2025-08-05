"""
Analytics service for dashboard data and reporting.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
import json

from ..models.project import Project
from ..models.task import Task
from ..models.user import User
from ..models.workflow import WorkflowInstance
from ..repositories.project_repository import ProjectRepository
from ..repositories.task_repository import TaskRepository
from ..repositories.user_repository import UserRepository
from ..repositories.workflow_repository import WorkflowInstanceRepository


class AnalyticsService:
    """
    Service for generating analytics and dashboard data.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.project_repo = ProjectRepository(db)
        self.task_repo = TaskRepository(db)
        self.user_repo = UserRepository(db)
        self.workflow_repo = WorkflowInstanceRepository(db)
    
    def get_dashboard_overview(self, user_id: int) -> Dict[str, Any]:
        """
        Get dashboard overview statistics.
        
        Args:
            user_id: User ID for personalized data
            
        Returns:
            Dict containing dashboard overview data
        """
        # Get user's projects
        user_projects = self.project_repo.get_user_projects(user_id)
        
        # Get user's tasks
        user_tasks = self.task_repo.get_user_tasks(user_id)
        
        # Calculate project statistics
        total_projects = len(user_projects)
        active_projects = len([p for p in user_projects if p.status in ['in_progress', 'planning']])
        completed_projects = len([p for p in user_projects if p.status == 'completed'])
        
        # Calculate task statistics
        total_tasks = len(user_tasks)
        active_tasks = len([t for t in user_tasks if t.status in ['todo', 'in_progress', 'review']])
        completed_tasks = len([t for t in user_tasks if t.status == 'completed'])
        overdue_tasks = len([t for t in user_tasks if self._is_task_overdue(t)])
        
        # Calculate completion rates
        project_completion_rate = (completed_projects / total_projects * 100) if total_projects > 0 else 0
        task_completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            "projects": {
                "total": total_projects,
                "active": active_projects,
                "completed": completed_projects,
                "completion_rate": round(project_completion_rate, 1)
            },
            "tasks": {
                "total": total_tasks,
                "active": active_tasks,
                "completed": completed_tasks,
                "overdue": overdue_tasks,
                "completion_rate": round(task_completion_rate, 1)
            },
            "recent_activity": self._get_recent_activity(user_id),
            "upcoming_deadlines": self._get_upcoming_deadlines(user_id),
            "performance_metrics": self._get_performance_metrics(user_id)
        }
    
    def get_project_analytics(self, project_id: int) -> Dict[str, Any]:
        """
        Get detailed analytics for a specific project.
        
        Args:
            project_id: Project ID
            
        Returns:
            Dict containing project analytics
        """
        project = self.project_repo.get(project_id)
        if not project:
            return {}
        
        # Get project tasks
        project_tasks = self.task_repo.get_project_tasks(project_id)
        
        # Task status distribution
        task_status_distribution = {}
        for task in project_tasks:
            status = task.status
            task_status_distribution[status] = task_status_distribution.get(status, 0) + 1
        
        # Task priority distribution
        task_priority_distribution = {}
        for task in project_tasks:
            priority = task.priority
            task_priority_distribution[priority] = task_priority_distribution.get(priority, 0) + 1
        
        # Calculate progress
        total_tasks = len(project_tasks)
        completed_tasks = len([t for t in project_tasks if t.status == 'completed'])
        progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Get assignee performance
        assignee_performance = self._get_assignee_performance(project_tasks)
        
        # Get timeline data
        timeline_data = self._get_project_timeline(project)
        
        return {
            "project_info": {
                "id": project.id,
                "name": project.name,
                "status": project.status,
                "progress_percentage": round(progress_percentage, 1)
            },
            "task_statistics": {
                "total": total_tasks,
                "completed": completed_tasks,
                "active": total_tasks - completed_tasks,
                "status_distribution": task_status_distribution,
                "priority_distribution": task_priority_distribution
            },
            "assignee_performance": assignee_performance,
            "timeline": timeline_data
        }
    
    def get_user_performance_analytics(self, user_id: int, date_range: Optional[str] = None) -> Dict[str, Any]:
        """
        Get user performance analytics.
        
        Args:
            user_id: User ID
            date_range: Optional date range filter (e.g., "30d", "7d")
            
        Returns:
            Dict containing user performance analytics
        """
        # Get user's tasks
        user_tasks = self.task_repo.get_user_tasks(user_id)
        
        # Apply date filter if specified
        if date_range:
            user_tasks = self._filter_tasks_by_date_range(user_tasks, date_range)
        
        # Calculate performance metrics
        total_tasks = len(user_tasks)
        completed_tasks = len([t for t in user_tasks if t.status == 'completed'])
        overdue_tasks = len([t for t in user_tasks if self._is_task_overdue(t)])
        
        # Calculate average completion time
        completion_times = []
        for task in user_tasks:
            if task.status == 'completed' and task.updated_at:
                # This is a simplified calculation - in a real system you'd track actual completion time
                completion_times.append(1)  # Placeholder
        
        avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else 0
        
        # Get productivity trends
        productivity_trends = self._get_productivity_trends(user_id, date_range)
        
        # Get task distribution by project
        task_distribution = {}
        for task in user_tasks:
            project_name = task.project.name if task.project else "Unknown"
            task_distribution[project_name] = task_distribution.get(project_name, 0) + 1
        
        return {
            "overview": {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "overdue_tasks": overdue_tasks,
                "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
                "avg_completion_time": round(avg_completion_time, 1)
            },
            "productivity_trends": productivity_trends,
            "task_distribution": task_distribution,
            "recent_activity": self._get_user_recent_activity(user_id, date_range)
        }
    
    def get_team_analytics(self, team_members: List[int]) -> Dict[str, Any]:
        """
        Get team analytics.
        
        Args:
            team_members: List of user IDs in the team
            
        Returns:
            Dict containing team analytics
        """
        team_data = []
        
        for user_id in team_members:
            user = self.user_repo.get(user_id)
            if user:
                user_tasks = self.task_repo.get_user_tasks(user_id)
                completed_tasks = len([t for t in user_tasks if t.status == 'completed'])
                total_tasks = len(user_tasks)
                
                team_data.append({
                    "user_id": user_id,
                    "user_name": user.full_name,
                    "total_tasks": total_tasks,
                    "completed_tasks": completed_tasks,
                    "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
                })
        
        # Calculate team averages
        if team_data:
            avg_completion_rate = sum(member["completion_rate"] for member in team_data) / len(team_data)
            total_team_tasks = sum(member["total_tasks"] for member in team_data)
            total_team_completed = sum(member["completed_tasks"] for member in team_data)
        else:
            avg_completion_rate = 0
            total_team_tasks = 0
            total_team_completed = 0
        
        return {
            "team_overview": {
                "total_members": len(team_data),
                "total_tasks": total_team_tasks,
                "total_completed": total_team_completed,
                "avg_completion_rate": round(avg_completion_rate, 1)
            },
            "member_performance": team_data
        }
    
    def generate_report(self, report_type: str, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate various types of reports.
        
        Args:
            report_type: Type of report to generate
            filters: Optional filters for the report
            
        Returns:
            Dict containing report data
        """
        if report_type == "project_summary":
            return self._generate_project_summary_report(filters)
        elif report_type == "task_performance":
            return self._generate_task_performance_report(filters)
        elif report_type == "user_productivity":
            return self._generate_user_productivity_report(filters)
        elif report_type == "workflow_analytics":
            return self._generate_workflow_analytics_report(filters)
        else:
            return {"error": "Unknown report type"}
    
    def _is_task_overdue(self, task: Task) -> bool:
        """Check if a task is overdue."""
        if not task.due_date or task.status == 'completed':
            return False
        return datetime.now() > task.due_date
    
    def _get_recent_activity(self, user_id: int) -> List[Dict[str, Any]]:
        """Get recent activity for a user."""
        # This would typically query an activity log table
        # For now, return recent tasks and projects
        recent_tasks = self.task_repo.get_user_tasks(user_id, limit=5)
        recent_projects = self.project_repo.get_user_projects(user_id, limit=5)
        
        activities = []
        
        for task in recent_tasks:
            activities.append({
                "type": "task",
                "id": task.id,
                "title": task.title,
                "status": task.status,
                "timestamp": task.updated_at.isoformat() if task.updated_at else None
            })
        
        for project in recent_projects:
            activities.append({
                "type": "project",
                "id": project.id,
                "title": project.name,
                "status": project.status,
                "timestamp": project.updated_at.isoformat() if project.updated_at else None
            })
        
        # Sort by timestamp
        activities.sort(key=lambda x: x["timestamp"] or "", reverse=True)
        return activities[:10]
    
    def _get_upcoming_deadlines(self, user_id: int) -> List[Dict[str, Any]]:
        """Get upcoming deadlines for a user."""
        user_tasks = self.task_repo.get_user_tasks(user_id)
        upcoming_deadlines = []
        
        for task in user_tasks:
            if task.due_date and task.status != 'completed':
                days_until_due = (task.due_date - datetime.now()).days
                if 0 <= days_until_due <= 7:  # Due within a week
                    upcoming_deadlines.append({
                        "task_id": task.id,
                        "task_title": task.title,
                        "project_name": task.project.name if task.project else "Unknown",
                        "due_date": task.due_date.isoformat(),
                        "days_until_due": days_until_due
                    })
        
        # Sort by due date
        upcoming_deadlines.sort(key=lambda x: x["days_until_due"])
        return upcoming_deadlines[:5]
    
    def _get_performance_metrics(self, user_id: int) -> Dict[str, Any]:
        """Get performance metrics for a user."""
        user_tasks = self.task_repo.get_user_tasks(user_id)
        
        # Calculate metrics
        total_tasks = len(user_tasks)
        completed_tasks = len([t for t in user_tasks if t.status == 'completed'])
        overdue_tasks = len([t for t in user_tasks if self._is_task_overdue(t)])
        
        # Calculate efficiency (tasks completed on time)
        on_time_completions = 0
        for task in user_tasks:
            if task.status == 'completed' and not self._is_task_overdue(task):
                on_time_completions += 1
        
        efficiency_rate = (on_time_completions / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            "efficiency_rate": round(efficiency_rate, 1),
            "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            "overdue_rate": (overdue_tasks / total_tasks * 100) if total_tasks > 0 else 0
        }
    
    def _get_assignee_performance(self, tasks: List[Task]) -> Dict[str, Any]:
        """Get performance data by assignee."""
        assignee_stats = {}
        
        for task in tasks:
            if task.assignee_id:
                assignee_name = task.assignee.full_name if task.assignee else "Unknown"
                if assignee_name not in assignee_stats:
                    assignee_stats[assignee_name] = {
                        "total_tasks": 0,
                        "completed_tasks": 0,
                        "overdue_tasks": 0
                    }
                
                assignee_stats[assignee_name]["total_tasks"] += 1
                if task.status == 'completed':
                    assignee_stats[assignee_name]["completed_tasks"] += 1
                if self._is_task_overdue(task):
                    assignee_stats[assignee_name]["overdue_tasks"] += 1
        
        # Calculate completion rates
        for assignee in assignee_stats:
            total = assignee_stats[assignee]["total_tasks"]
            completed = assignee_stats[assignee]["completed_tasks"]
            assignee_stats[assignee]["completion_rate"] = (completed / total * 100) if total > 0 else 0
        
        return assignee_stats
    
    def _get_project_timeline(self, project: Project) -> List[Dict[str, Any]]:
        """Get timeline data for a project."""
        # This would typically query project milestones and events
        # For now, return basic project timeline
        timeline = [
            {
                "date": project.created_at.isoformat() if project.created_at else None,
                "event": "Project Created",
                "description": f"Project '{project.name}' was created"
            }
        ]
        
        if project.updated_at and project.updated_at != project.created_at:
            timeline.append({
                "date": project.updated_at.isoformat(),
                "event": "Project Updated",
                "description": f"Project '{project.name}' was last updated"
            })
        
        return timeline
    
    def _get_productivity_trends(self, user_id: int, date_range: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get productivity trends for a user."""
        # This would typically calculate trends over time
        # For now, return placeholder data
        return [
            {"date": "2024-01-01", "tasks_completed": 5},
            {"date": "2024-01-02", "tasks_completed": 8},
            {"date": "2024-01-03", "tasks_completed": 3},
            {"date": "2024-01-04", "tasks_completed": 7},
            {"date": "2024-01-05", "tasks_completed": 6}
        ]
    
    def _get_user_recent_activity(self, user_id: int, date_range: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get recent activity for a user."""
        return self._get_recent_activity(user_id)
    
    def _filter_tasks_by_date_range(self, tasks: List[Task], date_range: str) -> List[Task]:
        """Filter tasks by date range."""
        now = datetime.now()
        
        if date_range == "7d":
            cutoff_date = now - timedelta(days=7)
        elif date_range == "30d":
            cutoff_date = now - timedelta(days=30)
        elif date_range == "90d":
            cutoff_date = now - timedelta(days=90)
        else:
            return tasks
        
        return [task for task in tasks if task.created_at and task.created_at >= cutoff_date]
    
    def _generate_project_summary_report(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate project summary report."""
        projects = self.project_repo.get_all()
        
        report_data = {
            "total_projects": len(projects),
            "active_projects": len([p for p in projects if p.status in ['in_progress', 'planning']]),
            "completed_projects": len([p for p in projects if p.status == 'completed']),
            "projects_by_status": {},
            "projects_by_priority": {}
        }
        
        for project in projects:
            # Status distribution
            status = project.status
            report_data["projects_by_status"][status] = report_data["projects_by_status"].get(status, 0) + 1
        
        return report_data
    
    def _generate_task_performance_report(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate task performance report."""
        tasks = self.task_repo.get_all()
        
        report_data = {
            "total_tasks": len(tasks),
            "completed_tasks": len([t for t in tasks if t.status == 'completed']),
            "overdue_tasks": len([t for t in tasks if self._is_task_overdue(t)]),
            "tasks_by_status": {},
            "tasks_by_priority": {}
        }
        
        for task in tasks:
            # Status distribution
            status = task.status
            report_data["tasks_by_status"][status] = report_data["tasks_by_status"].get(status, 0) + 1
            
            # Priority distribution
            priority = task.priority
            report_data["tasks_by_priority"][priority] = report_data["tasks_by_priority"].get(priority, 0) + 1
        
        return report_data
    
    def _generate_user_productivity_report(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate user productivity report."""
        users = self.user_repo.get_all()
        
        report_data = {
            "total_users": len(users),
            "user_performance": []
        }
        
        for user in users:
            user_tasks = self.task_repo.get_user_tasks(user.id)
            completed_tasks = len([t for t in user_tasks if t.status == 'completed'])
            total_tasks = len(user_tasks)
            
            report_data["user_performance"].append({
                "user_id": user.id,
                "user_name": user.full_name,
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            })
        
        return report_data
    
    def _generate_workflow_analytics_report(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate workflow analytics report."""
        workflow_instances = self.workflow_repo.get_all()
        
        report_data = {
            "total_instances": len(workflow_instances),
            "completed_instances": len([w for w in workflow_instances if w.is_completed]),
            "instances_by_stage": {},
            "workflow_performance": {}
        }
        
        for instance in workflow_instances:
            # Stage distribution
            stage = instance.current_stage
            report_data["instances_by_stage"][stage] = report_data["instances_by_stage"].get(stage, 0) + 1
        
        return report_data 