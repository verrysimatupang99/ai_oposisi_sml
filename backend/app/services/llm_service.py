"""
LLM Service

This module contains the LLM service for managing local LLM integration
with LM Studio for the AI Tokoh Oposisi & Intelektual Kritis system.

Author: AI Assistant
Created: 2025-01-11
"""

import httpx
import json
import logging
from typing import Dict, Any, List, Optional, AsyncGenerator
from datetime import datetime
import asyncio
from dataclasses import dataclass
from enum import Enum

from app.core.config import settings
from app.utils.logger import ai_logger

class LLMStatus(Enum):
    """LLM service status enum."""
    INITIALIZING = "initializing"
    READY = "ready"
    ERROR = "error"
    OFFLINE = "offline"

@dataclass
class LLMResponse:
    """LLM response data structure."""
    content: str
    model: str
    usage: Dict[str, int]
    response_time: float
    finish_reason: str

class LLMService:
    """Service for managing local LLM integration with LM Studio."""
    
    def __init__(self):
        """Initialize LLM service."""
        self.status = LLMStatus.INITIALIZING
        self.client = None
        self.model_info = None
        self.is_initialized = False
        self.logger = logging.getLogger(__name__)
        
    async def initialize(self):
        """
        Initialize the LLM service.
        
        Sets up HTTP client and validates LM Studio connection.
        For development: LM Studio is optional - runs in mock mode if not available.
        """
        try:
            self.logger.info("🤖 Initializing LLM service...")
            
            # Create HTTP client with timeout
            self.client = httpx.AsyncClient(
                base_url=settings.LM_STUDIO_URL,
                timeout=settings.LM_STUDIO_TIMEOUT
            )
            
            # Test connection and get model info
            await self._test_connection()
            
            self.status = LLMStatus.READY
            self.is_initialized = True
            
            self.logger.info("✅ LLM service initialized successfully")
            ai_logger.logger.info("LLM service initialized")
            
        except Exception as e:
            # For development: Don't fail if LM Studio is not available
            self.logger.warning(f"⚠️  LLM Studio not available: {e}")
            self.logger.info("📝 Running in MOCK mode - LLM requests will return mock responses")
            self.status = LLMStatus.ERROR
            self.is_initialized = False
            # Don't raise - allow app to continue without LLM for development
            # In production, you may want to uncomment the line below:
            # raise
    
    async def _test_connection(self):
        """
        Test connection to LM Studio and get model information.
        
        Raises:
            Exception: If connection fails or model is not available
        """
        try:
            # Test if LM Studio is running
            response = await self.client.get("/v1/models")
            
            if response.status_code != 200:
                raise Exception(f"LM Studio connection failed: {response.status_code}")
            
            models_data = response.json()
            
            # Check if the configured model is available
            available_models = [model["id"] for model in models_data.get("data", [])]
            
            if settings.LM_STUDIO_MODEL not in available_models:
                raise Exception(f"Model {settings.LM_STUDIO_MODEL} not available. Available models: {available_models}")
            
            # Get model details
            self.model_info = {
                "id": settings.LM_STUDIO_MODEL,
                "name": settings.LM_STUDIO_MODEL,
                "capabilities": ["chat", "completion"],
                "max_tokens": settings.LM_STUDIO_MAX_TOKENS
            }
            
            self.logger.info(f"✅ LM Studio connection successful. Using model: {settings.LM_STUDIO_MODEL}")
            
        except httpx.RequestError as e:
            raise Exception(f"LM Studio connection error: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid response from LM Studio: {e}")
        except Exception as e:
            raise Exception(f"LM Studio test failed: {e}")
    
    async def generate_chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> LLMResponse:
        """
        Generate chat completion using the local LLM.
        
        Args:
            messages (List[Dict[str, str]]): Chat messages
            temperature (Optional[float]): Temperature for randomness
            max_tokens (Optional[int]): Maximum tokens to generate
            stream (bool): Whether to stream responses
            
        Returns:
            LLMResponse: Generated response
            
        Raises:
            Exception: If generation fails
        """
        if not self.is_initialized:
            raise Exception("LLM service not initialized")
        
        start_time = datetime.utcnow()
        
        try:
            # Prepare request payload
            payload = {
                "model": settings.LM_STUDIO_MODEL,
                "messages": messages,
                "temperature": temperature or settings.LM_STUDIO_TEMPERATURE,
                "max_tokens": max_tokens or settings.LM_STUDIO_MAX_TOKENS,
                "stream": stream
            }
            
            self.logger.debug(f"Sending request to LM Studio: {payload}")
            
            # Make request to LM Studio
            response = await self.client.post("/v1/chat/completions", json=payload)
            
            if response.status_code != 200:
                raise Exception(f"LM Studio API error: {response.status_code} - {response.text}")
            
            response_data = response.json()
            
            # Parse response
            content = response_data["choices"][0]["message"]["content"]
            usage = response_data.get("usage", {})
            finish_reason = response_data["choices"][0]["finish_reason"]
            
            response_time = (datetime.utcnow() - start_time).total_seconds()
            
            llm_response = LLMResponse(
                content=content,
                model=settings.LM_STUDIO_MODEL,
                usage=usage,
                response_time=response_time,
                finish_reason=finish_reason
            )
            
            # Log the interaction
            ai_logger.log_model_interaction(
                model_name=settings.LM_STUDIO_MODEL,
                prompt=messages[-1]["content"] if messages else "",
                response=content,
                response_time=response_time,
                tokens_used=usage.get("total_tokens", 0),
                details={
                    "messages_count": len(messages),
                    "temperature": payload["temperature"],
                    "max_tokens": payload["max_tokens"]
                }
            )
            
            self.logger.info(f"✅ Chat completion generated in {response_time:.2f}s")
            return llm_response
            
        except Exception as e:
            self.logger.error(f"❌ Chat completion failed: {e}")
            ai_logger.log_model_error(settings.LM_STUDIO_MODEL, str(e))
            raise
    
    async def generate_completion(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> LLMResponse:
        """
        Generate text completion using the local LLM.
        
        Args:
            prompt (str): Input prompt
            temperature (Optional[float]): Temperature for randomness
            max_tokens (Optional[int]): Maximum tokens to generate
            
        Returns:
            LLMResponse: Generated response
            
        Raises:
            Exception: If generation fails
        """
        if not self.is_initialized:
            raise Exception("LLM service not initialized")
        
        start_time = datetime.utcnow()
        
        try:
            # Prepare request payload
            payload = {
                "model": settings.LM_STUDIO_MODEL,
                "prompt": prompt,
                "temperature": temperature or settings.LM_STUDIO_TEMPERATURE,
                "max_tokens": max_tokens or settings.LM_STUDIO_MAX_TOKENS
            }
            
            self.logger.debug(f"Sending completion request to LM Studio: {payload}")
            
            # Make request to LM Studio
            response = await self.client.post("/v1/completions", json=payload)
            
            if response.status_code != 200:
                raise Exception(f"LM Studio API error: {response.status_code} - {response.text}")
            
            response_data = response.json()
            
            # Parse response
            content = response_data["choices"][0]["text"]
            usage = response_data.get("usage", {})
            finish_reason = response_data["choices"][0]["finish_reason"]
            
            response_time = (datetime.utcnow() - start_time).total_seconds()
            
            llm_response = LLMResponse(
                content=content,
                model=settings.LM_STUDIO_MODEL,
                usage=usage,
                response_time=response_time,
                finish_reason=finish_reason
            )
            
            # Log the interaction
            ai_logger.log_model_interaction(
                model_name=settings.LM_STUDIO_MODEL,
                prompt=prompt,
                response=content,
                response_time=response_time,
                tokens_used=usage.get("total_tokens", 0),
                details={
                    "temperature": payload["temperature"],
                    "max_tokens": payload["max_tokens"]
                }
            )
            
            self.logger.info(f"✅ Completion generated in {response_time:.2f}s")
            return llm_response
            
        except Exception as e:
            self.logger.error(f"❌ Completion failed: {e}")
            ai_logger.log_model_error(settings.LM_STUDIO_MODEL, str(e))
            raise
    
    async def stream_chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream chat completion responses from the local LLM.
        
        Args:
            messages (List[Dict[str, str]]): Chat messages
            temperature (Optional[float]): Temperature for randomness
            max_tokens (Optional[int]): Maximum tokens to generate
            
        Yields:
            str: Streamed response chunks
            
        Raises:
            Exception: If streaming fails
        """
        if not self.is_initialized:
            raise Exception("LLM service not initialized")
        
        try:
            # Prepare request payload
            payload = {
                "model": settings.LM_STUDIO_MODEL,
                "messages": messages,
                "temperature": temperature or settings.LM_STUDIO_TEMPERATURE,
                "max_tokens": max_tokens or settings.LM_STUDIO_MAX_TOKENS,
                "stream": True
            }
            
            self.logger.debug(f"Starting stream to LM Studio: {payload}")
            
            # Make streaming request to LM Studio
            async with self.client.stream("POST", "/v1/chat/completions", json=payload) as response:
                if response.status_code != 200:
                    raise Exception(f"LM Studio streaming error: {response.status_code}")
                
                # Process streaming response
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]  # Remove "data: " prefix
                        if data == "[DONE]":
                            break
                        
                        try:
                            chunk = json.loads(data)
                            if "choices" in chunk and len(chunk["choices"]) > 0:
                                delta = chunk["choices"][0].get("delta", {})
                                if "content" in delta:
                                    yield delta["content"]
                        except json.JSONDecodeError:
                            continue
            
            self.logger.info("✅ Streaming completed successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Streaming failed: {e}")
            ai_logger.log_model_error(settings.LM_STUDIO_MODEL, str(e))
            raise
    
    async def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model.
        
        Returns:
            Dict[str, Any]: Model information
        """
        if not self.is_initialized:
            raise Exception("LLM service not initialized")
        
        return {
            "model": self.model_info,
            "status": self.status.value,
            "is_initialized": self.is_initialized,
            "config": {
                "url": settings.LM_STUDIO_URL,
                "model": settings.LM_STUDIO_MODEL,
                "timeout": settings.LM_STUDIO_TIMEOUT,
                "max_tokens": settings.LM_STUDIO_MAX_TOKENS,
                "temperature": settings.LM_STUDIO_TEMPERATURE
            }
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on the LLM service.
        
        Returns:
            Dict[str, Any]: Health check results
        """
        try:
            if not self.is_initialized:
                return {
                    "status": "error",
                    "message": "Service not initialized",
                    "timestamp": datetime.utcnow().isoformat()
                }
            
            # Test model availability
            await self._test_connection()
            
            return {
                "status": "healthy",
                "model": settings.LM_STUDIO_MODEL,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def cleanup(self):
        """
        Cleanup LLM service resources.
        """
        try:
            if self.client:
                await self.client.aclose()
                self.logger.info("✅ LLM service cleanup completed")
        except Exception as e:
            self.logger.error(f"❌ LLM service cleanup failed: {e}")
    
    def is_ready(self) -> bool:
        """
        Check if the LLM service is ready.
        
        Returns:
            bool: True if ready, False otherwise
        """
        return self.is_initialized and self.status == LLMStatus.READY

# Export LLM service
__all__ = ["LLMService", "LLMResponse", "LLMStatus"]