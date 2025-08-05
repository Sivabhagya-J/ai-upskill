"""
Configuration settings for the application using Pydantic Settings.
Follows the Singleton pattern for configuration management.
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator
import os


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Database
    database_url: str = "postgresql://postgres:root@localhost:5432/project_management"
    test_database_url: str = "postgresql://postgres:root@localhost:5432/project_management_test"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # Security
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Application
    debug: bool = True
    environment: str = "development"
    api_v1_str: str = "/api/v1"
    project_name: str = "Project Management Dashboard"
    version: str = "1.0.0"
    
    # CORS - Updated for production
    backend_cors_origins: List[str] = [
        "http://localhost:3000", 
        "http://localhost:3001", 
        "http://localhost:3002", 
        "http://localhost:3003", 
        "http://localhost:5173",
        "https://*.vercel.app",
        "https://*.railway.app",
        "https://*.render.com"
    ]
    
    # Email Configuration
    smtp_tls: bool = True
    smtp_port: int = 587
    smtp_host: Optional[str] = None
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    
    # Notification Settings
    smtp_server: Optional[str] = None
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    from_email: str = "noreply@projectmanagement.com"
    admin_email: Optional[str] = None
    
    # Analytics and Reporting
    analytics_enabled: bool = True
    report_export_enabled: bool = True
    chart_data_cache_ttl: int = 300  # 5 minutes
    
    # Workflow and Business Rules
    workflow_automation_enabled: bool = True
    business_rules_enabled: bool = True
    notification_automation_enabled: bool = True
    
    # Performance and Caching
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 1 hour
    query_optimization_enabled: bool = True
    
    # Logging
    log_level: str = "INFO"
    
    @validator("backend_cors_origins", pre=True)
    def assemble_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"


# Singleton instance of settings
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get the singleton settings instance.
    
    Returns:
        Settings: The application settings instance
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


# Export settings instance
settings = get_settings() 