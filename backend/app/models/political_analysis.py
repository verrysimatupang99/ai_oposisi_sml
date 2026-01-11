"""
Political Analysis Model

This module contains the PoliticalAnalysis model for storing analysis results
in the AI Tokoh Oposisi & Intelektual Kritis system.

Author: AI Assistant
Created: 2025-01-11
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base, GUID, GUID
import uuid
from datetime import datetime
from app.core.database import Base, GUID

class PoliticalAnalysis(Base):
    """Political analysis model for storing analysis results."""
    
    __tablename__ = "political_analyses"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    analysis_type = Column(String(50), nullable=False)  # "election", "policy", "event"
    content = Column(Text, nullable=False)
    summary = Column(Text)
    keywords = Column(JSON, default=[])
    confidence_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="analyses")
    
    def __repr__(self):
        return f"<PoliticalAnalysis(id={self.id}, title='{self.title}', type='{self.analysis_type}')>"