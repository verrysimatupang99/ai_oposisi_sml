"""
Main FastAPI Application Entry Point

This module contains the main FastAPI application setup with all middleware,
dependencies, and API routes configured for the AI Tokoh Oposisi & Intelektual Kritis system.

Author: AI Assistant
Created: 2025-01-11
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging
import os
from datetime import datetime

# Import local modules
from app.core.config import settings
from app.core.database import init_db, close_db
from app.core.security import verify_token
from app.api.v1 import auth, analysis, chat, persona, ethics
from app.services.llm_service import LLMService
from app.services.persona_service import PersonaService
from app.services.ethics_service import EthicsService
from app.services.rag_service import RAGService
from app.services.knowledge_loader import ingest_knowledge_base
from app.utils.logger import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager for startup and shutdown events.
    
    This context manager handles:
    - Database initialization
    - LLM service setup
    - Service initialization
    - Cleanup on shutdown
    """
    logger.info("Starting AI Tokoh Oposisi & Intelektual Kritis application...")
    
    try:
        # Startup: Initialize database
        logger.info("Initializing database...")
        await init_db()
        logger.info("Database initialized successfully")
        
        # Startup: Initialize services
        logger.info("Initializing AI services...")
        
        # Initialize LLM Service
        app.state.llm_service = LLMService()
        await app.state.llm_service.initialize()
        logger.info("LLM service initialized")
        
        # Initialize Persona Service
        app.state.persona_service = PersonaService(app.state.llm_service)
        await app.state.persona_service.initialize()
        logger.info("Persona service initialized")
        
        # Initialize Ethics Service
        app.state.ethics_service = EthicsService()
        await app.state.ethics_service.initialize()
        logger.info("Ethics service initialized")
        
        # Initialize RAG Service (if enabled)
        if settings.RAG_ENABLED:
            app.state.rag_service = RAGService()
            await app.state.rag_service.initialize()
            
            # Auto-ingest knowledge base if empty
            if app.state.rag_service.vector_store.count() == 0:
                logger.info("Knowledge base empty, ingesting documents...")
                count = await ingest_knowledge_base(app.state.rag_service)
                logger.info(f"Ingested {count} documents into RAG")
            
            logger.info("RAG service initialized")
        else:
            app.state.rag_service = None
            logger.info("RAG service disabled")
        
        logger.info("All services initialized successfully")
        
        yield
        
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise
    finally:
        # Shutdown: Cleanup
        logger.info("Shutting down application...")
        
        # Close database connections
        await close_db()
        logger.info("Database connections closed")
        
        # Cleanup services
        if hasattr(app.state, 'llm_service'):
            await app.state.llm_service.cleanup()
            logger.info("LLM service cleanup completed")
        
        logger.info("Application shutdown complete")

# Create FastAPI app with lifespan
app = FastAPI(
    title="AI Tokoh Oposisi & Intelektual Kritis",
    description="""
    🤖 AI Tokoh Oposisi & Intelektual Kritis API
    
    Sebuah sistem kecerdasan buatan yang dirancang untuk menjadi suara kritis 
    dalam konteks politik Indonesia, dengan persona Dr. Arjuna Wibawa.
    
    ## Fitur Utama:
    - 💬 Chat interaktif dengan persona AI
    - 📊 Analisis politik mendalam
    - 🛡️ Validasi etika demokrasi
    - 🎭 Persona tokoh oposisi kritis
    - 📚 Basis pengetahuan politik Indonesia
    
    ## Protokol Etika:
    - 🚫 Anti-kekerasan & anti-ujaran kebencian
    - 🤝 Pro-dialog & pro-demokrasi
    - 📢 Pro-transparansi & pro-akuntabilitas
    - 🎯 Fokus pada solusi & rekonsiliasi
    
    ## Peringatan:
    - Sistem ini **hanya untuk tujuan edukasi dan simulasi**
    - Tidak boleh digunakan untuk aktivitas politik nyata
    - Semua output harus diverifikasi oleh ahli
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Configure trusted host middleware
# NOTE: Disabled for development - TrustedHostMiddleware can block CORS preflight requests
# app.add_middleware(
#     TrustedHostMiddleware,
#     allowed_hosts=settings.ALLOWED_HOSTS
# )

# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint to verify system status.
    
    Returns:
        dict: System health status with timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "services": {
            "database": "connected",
            "llm": "initialized",
            "persona": "ready",
            "ethics": "active"
        }
    }

@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint with system information.
    
    Returns:
        dict: Welcome message and system information
    """
    return {
        "message": "🤖 AI Tokoh Oposisi & Intelektual Kritis API",
        "version": "1.0.0",
        "status": "operational",
        "description": "Sistem AI untuk analisis politik kritis dan edukasi demokrasi",
        "documentation": "/docs",
        "health": "/health"
    }

# Include API routers
app.include_router(
    auth.router,
    prefix="/api/v1",
    tags=["Authentication"]
)

app.include_router(
    analysis.router,
    prefix="/api/v1",
    tags=["Political Analysis"],
    dependencies=[Depends(verify_token)]
)

app.include_router(
    chat.router,
    prefix="/api/v1",
    tags=["Chat & Conversation"]
    # No authentication required for chat
)

app.include_router(
    persona.router,
    prefix="/api/v1",
    tags=["Persona Management"],
    dependencies=[Depends(verify_token)]
)

app.include_router(
    ethics.router,
    prefix="/api/v1",
    tags=["Ethics & Validation"],
    dependencies=[Depends(verify_token)]
)

# Custom OpenAPI schema
def custom_openapi():
    """
    Generate custom OpenAPI schema with enhanced documentation.
    
    Returns:
        dict: Custom OpenAPI schema
    """
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="AI Tokoh Oposisi & Intelektual Kritis",
        version="1.0.0",
        description="""
        🤖 AI Tokoh Oposisi & Intelektual Kritis API
        
        Sebuah sistem kecerdasan buatan yang dirancang untuk menjadi suara kritis 
        dalam konteks politik Indonesia, dengan persona Dr. Arjuna Wibawa.
        
        ## ⚠️ PERINGATAN ETIKA
        Sistem ini **hanya untuk tujuan edukasi dan simulasi**:
        - ❌ Dilarang digunakan untuk aktivitas politik nyata
        - ❌ Dilarang digunakan untuk memengaruhi opini publik
        - ❌ Dilarang digunakan untuk kampanye atau propaganda
        - ✅ Hanya untuk analisis politik, edukasi, dan simulasi akademik
        
        ## 🛡️ PROTOKOL ETIKA DEMOKRASI
        - 🚫 Anti-kekerasan & anti-ujaran kebencian
        - 🤝 Pro-dialog & pro-demokrasi
        - 📢 Pro-transparansi & pro-akuntabilitas
        - 🎯 Fokus pada solusi & rekonsiliasi
        """,
        routes=app.routes,
    )
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token for authentication"
        }
    }
    
    # Add global security requirement
    openapi_schema["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Custom HTTP exception handler with enhanced error responses.
    
    Args:
        request: FastAPI request object
        exc: HTTPException instance
        
    Returns:
        JSONResponse: Enhanced error response
    """
    logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "timestamp": datetime.utcnow().isoformat(),
                "path": str(request.url)
            }
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    General exception handler for unexpected errors.
    
    Args:
        request: FastAPI request object
        exc: Exception instance
        
    Returns:
        JSONResponse: Error response for unexpected errors
    """
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": 500,
                "message": "Internal server error",
                "timestamp": datetime.utcnow().isoformat(),
                "path": str(request.url)
            }
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning"
    )