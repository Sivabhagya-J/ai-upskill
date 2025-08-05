"""
Notification service for automated processes and alerts.
"""

import smtplib
import json
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from ..config import settings
from ..models.user import User
from ..models.project import Project
from ..models.task import Task

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Service for handling notifications and alerts.
    """
    
    def __init__(self):
        self.smtp_server = settings.smtp_server
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
        self.from_email = settings.from_email
    
    async def send_email_notification(
        self,
        to_emails: List[str],
        subject: str,
        body: str,
        html_body: Optional[str] = None
    ) -> bool:
        """
        Send email notification.
        
        Args:
            to_emails: List of recipient email addresses
            subject: Email subject
            body: Plain text email body
            html_body: HTML email body (optional)
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            if not self.smtp_server or not self.smtp_username:
                logger.warning("SMTP configuration not set up")
                return False
            
            msg = MimeMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = ', '.join(to_emails)
            
            # Add plain text part
            text_part = MimeText(body, 'plain')
            msg.attach(text_part)
            
            # Add HTML part if provided
            if html_body:
                html_part = MimeText(html_body, 'html')
                msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email notification sent to {to_emails}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
            return False
    
    async def send_task_assignment_notification(
        self,
        task: Task,
        assignee: User,
        project: Project
    ) -> bool:
        """
        Send notification when a task is assigned.
        
        Args:
            task: Assigned task
            assignee: User assigned to the task
            project: Project containing the task
            
        Returns:
            bool: True if notification sent successfully
        """
        subject = f"New Task Assignment: {task.title}"
        
        body = f"""
        Hello {assignee.full_name},
        
        You have been assigned a new task:
        
        Task: {task.title}
        Project: {project.name}
        Priority: {task.priority}
        Due Date: {task.due_date.strftime('%Y-%m-%d') if task.due_date else 'No due date'}
        
        Description:
        {task.description or 'No description provided'}
        
        Please log in to the project management system to view and update this task.
        
        Best regards,
        Project Management Team
        """
        
        html_body = f"""
        <html>
        <body>
            <h2>New Task Assignment</h2>
            <p>Hello {assignee.full_name},</p>
            <p>You have been assigned a new task:</p>
            <ul>
                <li><strong>Task:</strong> {task.title}</li>
                <li><strong>Project:</strong> {project.name}</li>
                <li><strong>Priority:</strong> {task.priority}</li>
                <li><strong>Due Date:</strong> {task.due_date.strftime('%Y-%m-%d') if task.due_date else 'No due date'}</li>
            </ul>
            <p><strong>Description:</strong></p>
            <p>{task.description or 'No description provided'}</p>
            <p>Please log in to the project management system to view and update this task.</p>
            <p>Best regards,<br>Project Management Team</p>
        </body>
        </html>
        """
        
        return await self.send_email_notification(
            to_emails=[assignee.email],
            subject=subject,
            body=body,
            html_body=html_body
        )
    
    async def send_task_due_reminder(
        self,
        task: Task,
        assignee: User,
        project: Project,
        days_until_due: int
    ) -> bool:
        """
        Send reminder for upcoming task due date.
        
        Args:
            task: Task with upcoming due date
            assignee: User assigned to the task
            project: Project containing the task
            days_until_due: Number of days until due date
            
        Returns:
            bool: True if notification sent successfully
        """
        subject = f"Task Due Reminder: {task.title}"
        
        body = f"""
        Hello {assignee.full_name},
        
        This is a reminder that your task is due soon:
        
        Task: {task.title}
        Project: {project.name}
        Due Date: {task.due_date.strftime('%Y-%m-%d')}
        Days Until Due: {days_until_due}
        
        Please ensure this task is completed on time.
        
        Best regards,
        Project Management Team
        """
        
        html_body = f"""
        <html>
        <body>
            <h2>Task Due Reminder</h2>
            <p>Hello {assignee.full_name},</p>
            <p>This is a reminder that your task is due soon:</p>
            <ul>
                <li><strong>Task:</strong> {task.title}</li>
                <li><strong>Project:</strong> {project.name}</li>
                <li><strong>Due Date:</strong> {task.due_date.strftime('%Y-%m-%d')}</li>
                <li><strong>Days Until Due:</strong> {days_until_due}</li>
            </ul>
            <p>Please ensure this task is completed on time.</p>
            <p>Best regards,<br>Project Management Team</p>
        </body>
        </html>
        """
        
        return await self.send_email_notification(
            to_emails=[assignee.email],
            subject=subject,
            body=body,
            html_body=html_body
        )
    
    async def send_project_status_update(
        self,
        project: Project,
        status: str,
        recipients: List[User]
    ) -> bool:
        """
        Send project status update notification.
        
        Args:
            project: Project with status update
            status: New project status
            recipients: List of users to notify
            
        Returns:
            bool: True if notification sent successfully
        """
        subject = f"Project Status Update: {project.name}"
        
        body = f"""
        Project Status Update
        
        Project: {project.name}
        New Status: {status}
        Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        
        Description: {project.description or 'No description provided'}
        
        Best regards,
        Project Management Team
        """
        
        html_body = f"""
        <html>
        <body>
            <h2>Project Status Update</h2>
            <ul>
                <li><strong>Project:</strong> {project.name}</li>
                <li><strong>New Status:</strong> {status}</li>
                <li><strong>Updated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</li>
            </ul>
            <p><strong>Description:</strong></p>
            <p>{project.description or 'No description provided'}</p>
            <p>Best regards,<br>Project Management Team</p>
        </body>
        </html>
        """
        
        recipient_emails = [user.email for user in recipients]
        return await self.send_email_notification(
            to_emails=recipient_emails,
            subject=subject,
            body=body,
            html_body=html_body
        )
    
    async def send_workflow_transition_notification(
        self,
        workflow_instance: Any,
        from_stage: str,
        to_stage: str,
        triggered_by: User,
        recipients: List[User]
    ) -> bool:
        """
        Send notification for workflow stage transition.
        
        Args:
            workflow_instance: Workflow instance that transitioned
            from_stage: Previous stage
            to_stage: New stage
            triggered_by: User who triggered the transition
            recipients: List of users to notify
            
        Returns:
            bool: True if notification sent successfully
        """
        subject = f"Workflow Transition: {workflow_instance.workflow.name}"
        
        body = f"""
        Workflow Stage Transition
        
        Workflow: {workflow_instance.workflow.name}
        Project: {workflow_instance.project.name}
        From Stage: {from_stage}
        To Stage: {to_stage}
        Triggered By: {triggered_by.full_name}
        Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        
        Best regards,
        Project Management Team
        """
        
        html_body = f"""
        <html>
        <body>
            <h2>Workflow Stage Transition</h2>
            <ul>
                <li><strong>Workflow:</strong> {workflow_instance.workflow.name}</li>
                <li><strong>Project:</strong> {workflow_instance.project.name}</li>
                <li><strong>From Stage:</strong> {from_stage}</li>
                <li><strong>To Stage:</strong> {to_stage}</li>
                <li><strong>Triggered By:</strong> {triggered_by.full_name}</li>
                <li><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</li>
            </ul>
            <p>Best regards,<br>Project Management Team</p>
        </body>
        </html>
        """
        
        recipient_emails = [user.email for user in recipients]
        return await self.send_email_notification(
            to_emails=recipient_emails,
            subject=subject,
            body=body,
            html_body=html_body
        )
    
    async def send_system_alert(
        self,
        alert_type: str,
        message: str,
        severity: str = "info",
        recipients: List[str] = None
    ) -> bool:
        """
        Send system alert notification.
        
        Args:
            alert_type: Type of alert
            message: Alert message
            severity: Alert severity (info, warning, error)
            recipients: List of email addresses to notify
            
        Returns:
            bool: True if notification sent successfully
        """
        if not recipients:
            recipients = [settings.admin_email] if settings.admin_email else []
        
        if not recipients:
            logger.warning("No recipients specified for system alert")
            return False
        
        subject = f"System Alert [{severity.upper()}]: {alert_type}"
        
        body = f"""
        System Alert
        
        Type: {alert_type}
        Severity: {severity}
        Message: {message}
        Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        This is an automated system notification.
        """
        
        html_body = f"""
        <html>
        <body>
            <h2>System Alert</h2>
            <ul>
                <li><strong>Type:</strong> {alert_type}</li>
                <li><strong>Severity:</strong> {severity}</li>
                <li><strong>Message:</strong> {message}</li>
                <li><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
            </ul>
            <p><em>This is an automated system notification.</em></p>
        </body>
        </html>
        """
        
        return await self.send_email_notification(
            to_emails=recipients,
            subject=subject,
            body=body,
            html_body=html_body
        )


# Global notification service instance
notification_service = NotificationService() 