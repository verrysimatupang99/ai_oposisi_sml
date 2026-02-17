"""
Configuration Module

This module contains all configuration settings for the AI Tokoh Oposisi & Intelektual Kritis system.
It uses pydantic-settings for environment-based configuration management.

Author: AI Assistant
Created: 2025-01-11
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache
from pathlib import Path
import os

# Base directory (project root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data"

class Settings(BaseSettings):
    """Application settings with environment-based configuration."""
    
    # Application
    APP_NAME: str = "AI Tokoh Oposisi & Intelektual Kritis"
    APP_VERSION: str = "2.0.0"  # Updated for consolidated structure
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    # Use SQLite for development by default, PostgreSQL for production
    DATABASE_URL: str = "sqlite:///./ai_oposisi.db"  # Changed to SQLite
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # LLM Configuration
    LM_STUDIO_URL: str = "http://192.168.110.156:1234"  # LM Studio server IP
    LM_STUDIO_MODEL: str = "llama-3.2-1b-instruct"  # Llama 3.2 1B Instruct model
    LM_STUDIO_TIMEOUT: int = 60
    LM_STUDIO_MAX_TOKENS: int = 2048  # Reduced for 1B model
    LM_STUDIO_TEMPERATURE: float = 0.7
    
    # RAG Configuration
    RAG_ENABLED: bool = True
    RAG_TOP_K: int = 3  # Number of documents to retrieve
    RAG_SIMILARITY_THRESHOLD: float = 0.3  # Minimum relevance score
    EMBEDDING_MODEL: str = "text-embedding-nomic-embed-text-v1.5"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001", "http://localhost:5173"]
    ALLOWED_HOSTS: List[str] = ["localhost", "0.0.0.0", "127.0.0.1"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Dataset Paths (Updated for consolidated structure)
    DATASET_PATH: str = str(DATA_DIR / "datasets")
    PERSONA_PATH: str = str(DATA_DIR / "persona" / "persona_utama.md")
    DOCS_PATH: str = str(DATA_DIR / "docs")
    KNOWLEDGE_BASE_PATH: str = str(DATA_DIR / "knowledge_base")  # For processed data
    
    # Ethics Configuration
    ETHICS_ENABLED: bool = True
    ETHICS_STRICT_MODE: bool = True
    CONTENT_FILTER_ENABLED: bool = True
    
    # Persona Configuration
    PERSONA_NAME: str = "Dr. Arjuna Wibawa"
    PERSONA_DESCRIPTION: str = "Intelektual kritis dan tokoh oposisi virtual"
    PERSONA_COMMUNICATION_STYLE: str = "formal"
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["text/plain", "application/pdf", "text/markdown"]
    
    # Cache
    CACHE_TTL: int = 300  # 5 minutes
    
    # External APIs
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """
    Get cached application settings.
    
    Returns:
        Settings: Application configuration instance
    """
    return Settings()

# Create global settings instance
settings = get_settings()

# Export for convenience
__all__ = ["Settings", "get_settings", "settings"]