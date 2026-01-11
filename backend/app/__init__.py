"""
AI Tokoh Oposisi & Intelektual Kritis Application Package

This package contains the main FastAPI application for the AI Tokoh Oposisi & 
Intelektual Kritis system, including all backend services, API endpoints, 
and core functionality.

Author: AI Assistant
Created: 2025-01-11
"""

# Application version
__version__ = "1.0.0"
__author__ = "AI Assistant"
__description__ = "AI Tokoh Oposisi & Intelektual Kritis Backend Application"

# Import main application
from .main import app

# Import core modules
from .core import config, database, security
from .utils import logger

# Import services
from .services import llm_service, persona_service, ethics_service

# Import API modules
from .api import v1

# Export main application and key components
__all__ = [
    "app",
    "config", "database", "security",
    "logger",
    "llm_service", "persona_service", "ethics_service",
    "v1"
]