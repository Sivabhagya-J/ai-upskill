"""
Pydantic schemas for user-related operations.
"""

from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime



class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr
    username: str
    full_name: str



class UserCreate(UserBase):
    """Schema for user creation."""
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @validator('username')
    def validate_username(cls, v):
        """Validate username format."""
        if not v.isalnum():
            raise ValueError('Username must contain only alphanumeric characters')
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return v


class UserUpdate(BaseModel):
    """Schema for user updates."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None

    password: Optional[str] = None
    is_active: Optional[bool] = None
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength if provided."""
        if v is not None and len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @validator('username')
    def validate_username(cls, v):
        """Validate username format if provided."""
        if v is not None:
            if not v.isalnum():
                raise ValueError('Username must contain only alphanumeric characters')
            if len(v) < 3:
                raise ValueError('Username must be at least 3 characters long')
        return v


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserToken(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class UserList(BaseModel):
    """Schema for paginated user list response."""
    items: list[UserResponse]
    total: int
    page: int
    size: int
    pages: int


class UserProfile(BaseModel):
    """Schema for user profile with additional info."""
    id: int
    email: EmailStr
    username: str
    full_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    project_count: int = 0
    task_count: int = 0

    
    class Config:
        from_attributes = True 