"""
User repository for user-related data access operations.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from .base import BaseRepository
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[User]):
    """
    User repository with user-specific data access operations.
    """
    
    def __init__(self, db: Session):
        super().__init__(db, User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            email: User email
            
        Returns:
            Optional[User]: User if found, None otherwise
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            username: User username
            
        Returns:
            Optional[User]: User if found, None otherwise
        """
        return self.db.query(User).filter(User.username == username).first()
    
    def create_user(self, user_data: UserCreate, hashed_password: str = None) -> User:
        """
        Create a new user.
        
        Args:
            user_data: User creation data
            hashed_password: Pre-hashed password (optional)
            
        Returns:
            User: Created user
        """
        from ..utils.security import get_password_hash
        
        user_dict = user_data.dict()
        
        # Remove password field from user_dict as User model doesn't have it
        password = user_dict.pop("password", None)
        
        # Handle password hashing
        if hashed_password:
            user_dict["password_hash"] = hashed_password
        elif password:
            user_dict["password_hash"] = get_password_hash(password)
        else:
            raise ValueError("Password is required")
        

        
        db_user = User(**user_dict)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update_user_password(self, user: User, new_password: str) -> User:
        """
        Update user password.
        
        Args:
            user: User to update
            new_password: New password
            
        Returns:
            User: Updated user
        """
        from ..utils.security import get_password_hash
        
        user.password_hash = get_password_hash(new_password)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all users with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[User]: List of users
        """
        return (
            self.db.query(User)
            .filter(User.is_active == True)
            .order_by(User.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def search_users(self, search_term: str, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Search users by name or email.
        
        Args:
            search_term: Search term
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[User]: List of matching users
        """
        return (
            self.db.query(User)
            .filter(
                and_(
                    User.is_active == True,
                    (User.full_name.ilike(f"%{search_term}%") | 
                     User.email.ilike(f"%{search_term}%") |
                     User.username.ilike(f"%{search_term}%"))
                )
            )
            .order_by(User.full_name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
 