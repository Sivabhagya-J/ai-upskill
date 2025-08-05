#!/usr/bin/env python3
"""
Script to create test users in the database.
This resolves the foreign key violation when creating tasks with assignee_id.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db
from app.models.user import User
from app.utils.security import get_password_hash

def create_test_users():
    """Create test users in the database."""
    db = next(get_db())
    
    try:
        # Check if users already exist
        existing_users = db.query(User).all()
        print(f"Found {len(existing_users)} existing users")
        
        if len(existing_users) >= 3:
            print("Test users already exist. Skipping creation.")
            return
        
        # Create test users
        test_users = [
            {
                "username": "john_doe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "password_hash": get_password_hash("password123"),
                "is_active": True
            },
            {
                "username": "jane_smith",
                "email": "jane@example.com",
                "full_name": "Jane Smith",
                "password_hash": get_password_hash("password123"),
                "is_active": True
            },
            {
                "username": "mike_johnson",
                "email": "mike@example.com",
                "full_name": "Mike Johnson",
                "password_hash": get_password_hash("password123"),
                "is_active": True
            }
        ]
        
        for user_data in test_users:
            # Check if user already exists
            existing_user = db.query(User).filter(
                (User.email == user_data["email"]) | 
                (User.username == user_data["username"])
            ).first()
            
            if existing_user:
                print(f"User {user_data['username']} already exists")
                continue
            
            # Create new user
            user = User(**user_data)
            db.add(user)
            print(f"Created user: {user_data['username']}")
        
        db.commit()
        print("Test users created successfully!")
        
        # Verify users were created
        all_users = db.query(User).all()
        print(f"Total users in database: {len(all_users)}")
        for user in all_users:
            print(f"User {user.id}: {user.username} ({user.email})")
            
    except Exception as e:
        print(f"Error creating test users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_users() 