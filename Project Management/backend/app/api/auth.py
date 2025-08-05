"""
Authentication API routes.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserLogin, UserToken, UserResponse
from ..repositories.user_repository import UserRepository
from ..utils.security import verify_password, get_password_hash, create_access_token
from ..utils.validators import validate_email, validate_password, validate_username
from .deps import get_current_user

router = APIRouter()
security = HTTPBearer()


@router.post("/signup", response_model=UserToken, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user account.
    
    Args:
        user_data: User registration data
        db: Database session
        
    Returns:
        UserToken: User token with access token and user info
        
    Raises:
        HTTPException: If validation fails or user already exists
    """
    # Validate input data
    email_valid, email_error = validate_email(user_data.email)
    if not email_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=email_error
        )
    
    password_valid, password_error = validate_password(user_data.password)
    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=password_error
        )
    
    username_valid, username_error = validate_username(user_data.username)
    if not username_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=username_error
        )
    
    # Check if user already exists
    user_repo = UserRepository(db)
    
    existing_user = user_repo.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    existing_username = user_repo.get_by_username(user_data.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    user = user_repo.create_user(user_data)
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return UserToken(
        access_token=access_token,
        token_type="bearer",
        expires_in=30 * 60,  # 30 minutes in seconds
        user=UserResponse.from_orm(user)
    )


@router.post("/login", response_model=UserToken)
async def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return access token.
    
    Args:
        user_credentials: User login credentials
        db: Database session
        
    Returns:
        UserToken: User token with access token and user info
        
    Raises:
        HTTPException: If credentials are invalid
    """
    user_repo = UserRepository(db)
    
    # Get user by email
    user = user_repo.get_by_email(user_credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return UserToken(
        access_token=access_token,
        token_type="bearer",
        expires_in=30 * 60,  # 30 minutes in seconds
        user=UserResponse.from_orm(user)
    )


@router.post("/refresh", response_model=UserToken)
async def refresh_token(
    current_token: str = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Refresh access token.
    
    Args:
        current_token: Current access token
        db: Database session
        
    Returns:
        UserToken: New user token with refreshed access token
        
    Raises:
        HTTPException: If token is invalid
    """
    # This would typically validate the refresh token
    # For now, we'll just create a new token if the current one is valid
    from ..api.deps import get_current_user
    
    try:
        current_user = get_current_user(current_token, db)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create new access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(current_user.id)},
        expires_delta=access_token_expires
    )
    
    return UserToken(
        access_token=access_token,
        token_type="bearer",
        expires_in=30 * 60,  # 30 minutes in seconds
        user=UserResponse.from_orm(current_user)
    )


@router.post("/logout")
async def logout():
    """
    Logout user (client should discard token).
    
    Returns:
        dict: Success message
    """
    # In a real application, you might want to blacklist the token
    # For now, we'll just return a success message
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserResponse: Current user information
    """
    return UserResponse.from_orm(current_user)


@router.post("/reset-password")
async def reset_user_password(
    email: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    """
    Reset user password (for development/testing purposes).
    
    Args:
        email: User's email
        new_password: New password
        db: Database session
        
    Returns:
        dict: Success message
    """
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Hash the new password
    hashed_password = get_password_hash(new_password)
    
    # Update the user's password
    success = user_repo.update_user_password(user.id, hashed_password)
    
    if success:
        return {"message": f"Password updated successfully for user {email}"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update password"
        ) 