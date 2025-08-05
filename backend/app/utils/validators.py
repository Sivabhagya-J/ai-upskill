"""
Validation utilities for data validation.
"""

import re
from typing import Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    if len(email) > 255:
        return False, "Email is too long (max 255 characters)"
    
    return True, ""


def validate_password(password: str) -> Tuple[bool, str]:
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if len(password) > 128:
        return False, "Password is too long (max 128 characters)"
    
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    # Check for at least one digit
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    # Check for at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, ""


def validate_username(username: str) -> Tuple[bool, str]:
    """
    Validate username format.
    
    Args:
        username: Username to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not username:
        return False, "Username is required"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    
    if len(username) > 50:
        return False, "Username is too long (max 50 characters)"
    
    # Check for alphanumeric characters and underscores only
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    # Check for consecutive underscores
    if '__' in username:
        return False, "Username cannot contain consecutive underscores"
    
    # Check for leading/trailing underscores
    if username.startswith('_') or username.endswith('_'):
        return False, "Username cannot start or end with an underscore"
    
    return True, ""


def validate_project_name(name: str) -> Tuple[bool, str]:
    """
    Validate project name.
    
    Args:
        name: Project name to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not name:
        return False, "Project name is required"
    
    if len(name) < 1:
        return False, "Project name cannot be empty"
    
    if len(name) > 255:
        return False, "Project name is too long (max 255 characters)"
    
    return True, ""


def validate_task_title(title: str) -> Tuple[bool, str]:
    """
    Validate task title.
    
    Args:
        title: Task title to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not title:
        return False, "Task title is required"
    
    if len(title) < 1:
        return False, "Task title cannot be empty"
    
    if len(title) > 255:
        return False, "Task title is too long (max 255 characters)"
    
    return True, "" 