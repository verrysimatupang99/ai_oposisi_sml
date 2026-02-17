"""
Chat & Conversation API Endpoints

This module contains API endpoints for chat and conversation functionality.
Implements real LLM integration via LM Studio.

Author: AI Assistant
Created: 2025-01-11
Updated: 2026-01-12 - Implemented real LLM integration
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import json
import asyncio

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import settings
from app.models.user import User

# Create router
router = APIRouter(prefix="/chat", tags=["Chat & Conversation"])


# Request/Response schemas
class ChatMessageRequest(BaseModel):
    """Chat message request schema."""
    message: str
    conversation_id: Optional[int] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


class ChatMessageResponse(BaseModel):
    """Chat message response schema."""
    status: str
    user_message: str
    ai_response: str
    model: str
    response_time: float
    usage: Dict[str, int]
    user_id: str


# Persona system prompt for Dr. Arjuna Wibawa
PERSONA_SYSTEM_PROMPT = """Anda adalah Dr. Arjuna Wibawa, seorang tokoh oposisi dan intelektual kritis Indonesia.

PROFIL:
- Ahli dalam politik Indonesia, ekonomi politik, dan strategi oposisi demokratis
- Berpikir kritis, analitis, dan berbasis data
- Komunikatif, edukatif, dan persuasif
- Menjunjung tinggi nilai demokrasi, keadilan, dan transparansi

GAYA KOMUNIKASI:
- Gunakan bahasa Indonesia yang jelas dan mudah dipahami
- Sertakan contoh konkret dan analogi yang relevan
- Berikan analisis mendalam namun tetap praktis
- Hindari jargon yang terlalu teknis tanpa penjelasan

NILAI DASAR:
- Demokrasi dan partisipasi rakyat
- Keadilan sosial dan ekonomi
- Transparansi dan akuntabilitas
- HAM dan kebebasan sipil
- Kebenaran dan integritas intelektual

JANGAN PERNAH:
- Memberikan informasi yang tidak akurat
- Menghasut kekerasan atau kebencian
- Memihak secara membabi buta
- Mengabaikan konteks sosial-politik Indonesia"""


@router.post("/message", response_model=ChatMessageResponse)
async def send_chat_message(
    request: Request,
    chat_request: ChatMessageRequest
):
    """
    Send a chat message to AI and get response.
    
    Uses RAG to retrieve relevant context from knowledge base
    before generating the response, reducing hallucinations.
    
    Args:
        request: FastAPI request object (for accessing app state)
        chat_request: Chat message request with user input
        
    Returns:
        ChatMessageResponse: AI response with metadata
    """
    try:
        # Get services from app state
        llm_service = request.app.state.llm_service
        rag_service = getattr(request.app.state, 'rag_service', None)
        
        # Build system prompt with RAG context if available
        system_prompt = PERSONA_SYSTEM_PROMPT
        
        if rag_service and rag_service.is_initialized:
            # Retrieve relevant context from knowledge base
            rag_context = await rag_service.get_augmented_context(chat_request.message)
            if rag_context:
                system_prompt = f"{PERSONA_SYSTEM_PROMPT}\n\n{rag_context}"
        
        # Prepare messages with persona and context
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": chat_request.message}
        ]
        
        # Generate response
        llm_response = await llm_service.generate_chat_completion(
            messages=messages,
            temperature=chat_request.temperature,
            max_tokens=chat_request.max_tokens
        )
        
        return ChatMessageResponse(
            status="success",
            user_message=chat_request.message,
            ai_response=llm_response.content,
            model=llm_response.model,
            response_time=llm_response.response_time,
            usage=llm_response.usage,
            user_id="anonymous"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat generation failed: {str(e)}"
        )


@router.get("/conversations")
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's conversation history.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List: List of conversations
        
    Note:
        Conversation persistence will be implemented in future phase.
    """
    return {
        "status": "success",
        "message": "Conversation history - Database persistence coming soon",
        "user_id": current_user.id,
        "conversations": []
    }


@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get specific conversation by ID.
    
    Args:
        conversation_id: Conversation ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dict: Conversation details
        
    Note:
        Conversation persistence will be implemented in future phase.
    """
    return {
        "status": "success", 
        "message": "Conversation details - Database persistence coming soon",
        "conversation_id": conversation_id,
        "user_id": current_user.id,
        "messages": []
    }


@router.post("/stream")
async def stream_chat_response(
    request: Request,
    chat_request: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Stream chat response from AI using Server-Sent Events.
    
    Args:
        request: FastAPI request object
        chat_request: Chat message request with user input
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        StreamingResponse: SSE stream of AI response chunks
    """
    async def generate_stream():
        try:
            # Get LLM service from app state
            llm_service = request.app.state.llm_service
            
            # Check if mock mode
            if llm_service.mock_mode:
                # In mock mode, yield a simple message
                mock_response = f"[MOCK MODE] Dr. Arjuna Wibawa: Pertanyaan tentang '{chat_request.message[:30]}...' menarik untuk dibahas."
                for char in mock_response:
                    yield f"data: {json.dumps({'content': char})}\n\n"
                    await asyncio.sleep(0.02)
                yield "data: [DONE]\n\n"
                return
            
            # Prepare messages with persona
            messages = [
                {"role": "system", "content": PERSONA_SYSTEM_PROMPT},
                {"role": "user", "content": chat_request.message}
            ]
            
            # Stream response
            async for chunk in llm_service.stream_chat_completion(
                messages=messages,
                temperature=chat_request.temperature,
                max_tokens=chat_request.max_tokens
            ):
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.get("/status")
async def get_chat_status(request: Request):
    """
    Get current chat/LLM service status.
    
    Returns:
        Dict: LLM service status information
    """
    llm_service = request.app.state.llm_service
    
    return {
        "status": "online",
        "llm_ready": llm_service.is_initialized,
        "mock_mode": llm_service.mock_mode,
        "model": settings.LM_STUDIO_MODEL,
        "url": settings.LM_STUDIO_URL
    }
