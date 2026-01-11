"""
Ethics Validation Model

This module contains the EthicsValidation model for storing validation results
in the AI Tokoh Oposisi & Intelektual Kritis system.

Author: AI Assistant
Created: 2025-01-11
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base, GUID, GUID
import uuid
from datetime import datetime
from app.core.database import Base, GUID

class EthicsValidation(Base):
    """Ethics validation model for storing validation results."""
    
    __tablename__ = "ethics_validations"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    content = Column(Text, nullable=False)
    validation_type = Column(String(50))  # "content", "response", "analysis"
    is_valid = Column(Boolean, nullable=False)
    violations = Column(JSON, default=[])
    confidence_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<EthicsValidation(id={self.id}, is_valid={self.is_valid}, type='{self.validation_type}')>"