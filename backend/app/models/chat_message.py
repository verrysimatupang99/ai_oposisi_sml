"""
Chat Message Model

This module contains the ChatMessage model for conversation messages
in the AI Tokoh Oposisi & Intelektual Kritis system.

Author: AI Assistant
Created: 2025-01-11
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base, GUID, GUID
import uuid
from datetime import datetime
from app.core.database import Base, GUID

class ChatMessage(Base):
    """Chat message model for conversation messages."""
    
    __tablename__ = "chat_messages"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    session_id = Column(GUID(), ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    message_type = Column(String(50), default="text")  # "text", "analysis", "persona"
    metadata_ = Column(JSON, default={})  # Additional metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("ChatSession", back_populates="messages")
    
    def __repr__(self):
        return f"<ChatMessage(id={self.id}, session_id={self.session_id}, role='{self.role}')>"