"""
System Log Model

This module contains the SystemLog model for logging system events
in the AI Tokoh Oposisi & Intelektual Kritis system.

Author: AI Assistant
Created: 2025-01-11
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base, GUID, GUID
import uuid
from datetime import datetime
from app.core.database import Base, GUID

class SystemLog(Base):
    """System log model for logging system events."""
    
    __tablename__ = "system_logs"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    level = Column(String(20), nullable=False)  # "INFO", "WARNING", "ERROR", "DEBUG"
    message = Column(Text, nullable=False)
    module = Column(String(100))
    function = Column(String(100))
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    metadata_ = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<SystemLog(id={self.id}, level='{self.level}', message='{self.message[:50]}...')>"