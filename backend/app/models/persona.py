"""
Persona Model

This module contains the Persona model for storing persona configurations
in the AI Tokoh Oposisi & Intelektual Kritis system.

Author: AI Assistant
Created: 2025-01-11
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base, GUID, GUID
import uuid
from datetime import datetime
from app.core.database import Base, GUID

class Persona(Base):
    """Persona model for storing persona configurations."""
    
    __tablename__ = "personas"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    communication_style = Column(String(50))  # "formal", "casual", "academic"
    expertise_areas = Column(JSON, default=[])
    personality_traits = Column(JSON, default=[])
    values = Column(JSON, default=[])
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Persona(id={self.id}, name='{self.name}', style='{self.communication_style}')>"