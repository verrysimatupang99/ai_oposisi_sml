"""
Database Configuration and Models

This module contains database configuration, connection management,
and SQLAlchemy models for the AI Tokoh Oposisi & Intelektual Kritis system.

Author: AI Assistant
Created: 2025-01-11
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, JSON, Float, ForeignKey, TypeDecorator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PostgreSQL_UUID
from sqlalchemy.types import CHAR
import uuid
from datetime import datetime
from typing import AsyncGenerator
import asyncpg
import asyncio
from app.core.config import settings
import logging

# Setup logging
logger = logging.getLogger(__name__)

# Custom UUID type that works with both SQLite and PostgreSQL
class GUID(TypeDecorator):
    """
    Platform-independent GUID type.
    
    Uses PostgreSQL's UUID type, otherwise uses CHAR(36), storing as stringified hex values.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PostgreSQL_UUID())
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            else:
                return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value

# SQLAlchemy Base
Base = declarative_base()

# Database URL
DATABASE_URL = settings.DATABASE_URL

# Determine if using SQLite
is_sqlite = DATABASE_URL.startswith("sqlite")

# Create engine with appropriate settings
if is_sqlite:
    # SQLite specific configuration
    engine = create_engine(
        DATABASE_URL,
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False}  # Needed for SQLite
    )
else:
    # PostgreSQL specific configuration
    engine = create_engine(
        DATABASE_URL,
        echo=settings.DEBUG,
        pool_size=20,
        max_overflow=0,
        pool_pre_ping=True,
        pool_recycle=3600
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Async database setup (only for PostgreSQL)
if not is_sqlite:
    async_engine = create_engine(
        DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
        echo=settings.DEBUG,
        pool_size=20,
        max_overflow=0,
        pool_pre_ping=True,
        pool_recycle=3600
    )
    
    AsyncSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        class_=Session
    )
else:
    # For SQLite, use sync engine for async operations too
    async_engine = engine
    AsyncSessionLocal = SessionLocal

# Dependency to get database session
def get_db() -> Session:
    """
    Get database session dependency.
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db() -> AsyncGenerator[Session, None]:
    """
    Get async database session dependency.
    
    Yields:
        AsyncSession: Async database session
    """
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

async def init_db():
    """
    Initialize database tables.
    
    Creates all tables defined in the models.
    """
    try:
        logger.info("🗄️  Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Failed to create database tables: {e}")
        raise

async def close_db():
    """
    Close database connections.
    """
    try:
        logger.info("🗄️  Closing database connections...")
        engine.dispose()
        logger.info("✅ Database connections closed")
    except Exception as e:
        logger.error(f"❌ Failed to close database connections: {e}")

# Import models to avoid circular imports
from app.models.user import User
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage
from app.models.political_analysis import PoliticalAnalysis
from app.models.persona import Persona
from app.models.ethics_validation import EthicsValidation
from app.models.system_log import SystemLog

# Re-export models for convenience
__all__ = [
    "Base", "engine", "SessionLocal", "get_db", "get_async_db",
    "init_db", "close_db", "User", "ChatSession", "ChatMessage",
    "PoliticalAnalysis", "Persona", "EthicsValidation", "SystemLog",
    "create_tables", "drop_tables", "reset_database"
]

# Database utility functions
async def create_tables():
    """
    Create all database tables.
    """
    try:
        logger.info("🗄️  Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ All database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Failed to create database tables: {e}")
        raise

async def drop_tables():
    """
    Drop all database tables.
    """
    try:
        logger.info("🗑️  Dropping database tables...")
        Base.metadata.drop_all(bind=engine)
        logger.info("✅ All database tables dropped successfully")
    except Exception as e:
        logger.error(f"❌ Failed to drop database tables: {e}")
        raise

async def reset_database():
    """
    Reset database by dropping and recreating all tables.
    """
    await drop_tables()
    await create_tables()

# Export models and utilities
__all__ = [
    "Base", "engine", "SessionLocal", "get_db", "get_async_db",
    "init_db", "close_db", "User", "ChatSession", "ChatMessage",
    "PoliticalAnalysis", "Persona", "EthicsValidation", "SystemLog",
    "create_tables", "drop_tables", "reset_database"
]