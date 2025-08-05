"""
Database configuration and session management.
Implements Singleton pattern for database connection.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from typing import Optional
import logging

from .config import settings

logger = logging.getLogger(__name__)

# Create SQLAlchemy engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.debug,
    poolclass=StaticPool if settings.environment == "test" else None
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Import all models to ensure they are registered with SQLAlchemy
from .models import user, project, task, workflow


class DatabaseManager:
    """
    Database manager implementing Singleton pattern.
    Manages database connections and sessions.
    """
    
    _instance: Optional['DatabaseManager'] = None
    _engine = None
    _session_factory = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._engine = engine
            self._session_factory = SessionLocal
    
    @property
    def engine(self):
        """Get the database engine."""
        return self._engine
    
    @property
    def session_factory(self):
        """Get the session factory."""
        return self._session_factory
    
    def get_session(self):
        """
        Get a new database session.
        
        Returns:
            Session: SQLAlchemy session
        """
        return self._session_factory()
    
    def close_session(self, session):
        """
        Close a database session.
        
        Args:
            session: SQLAlchemy session to close
        """
        if session:
            session.close()
    
    def create_tables(self):
        """Create all tables in the database."""
        try:
            Base.metadata.create_all(bind=self._engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            raise
    
    def drop_tables(self):
        """Drop all tables in the database."""
        try:
            Base.metadata.drop_all(bind=self._engine)
            logger.info("Database tables dropped successfully")
        except Exception as e:
            logger.error(f"Error dropping database tables: {e}")
            raise


# Global database manager instance
db_manager = DatabaseManager()


def get_db():
    """
    Dependency function to get database session.
    Yields a database session and ensures it's closed.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = db_manager.get_session()
    try:
        yield db
    finally:
        db_manager.close_session(db)


def init_db():
    """Initialize the database with tables."""
    db_manager.create_tables()


def reset_db():
    """Reset the database by dropping and recreating tables."""
    db_manager.drop_tables()
    db_manager.create_tables() 