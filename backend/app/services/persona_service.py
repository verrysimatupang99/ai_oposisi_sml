"""
Persona Service

This module contains the persona service for managing AI personas,
including Dr. Arjuna Wibawa, for the AI Tokoh Oposisi & Intelektual Kritis system.

Author: AI Assistant
Created: 2025-01-11
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from app.core.config import settings
from app.services.llm_service import LLMService, LLMResponse
from app.utils.logger import ai_logger
from app.models.persona import Persona
from sqlalchemy.orm import Session

class PersonaService:
    """Service for managing AI personas and their interactions."""
    
    def __init__(self, llm_service: LLMService):
        """
        Initialize persona service.
        
        Args:
            llm_service (LLMService): LLM service instance
        """
        self.llm_service = llm_service
        self.logger = logging.getLogger(__name__)
        self.active_personas = {}
        
    async def initialize(self):
        """
        Initialize persona service.
        
        Loads default personas and sets up persona configurations.
        """
        try:
            self.logger.info("🎭 Initializing Persona service...")
            
            # Load default personas
            await self._load_default_personas()
            
            self.logger.info("✅ Persona service initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize persona service: {e}")
            raise
    
    async def _load_default_personas(self):
        """
        Load default personas including Dr. Arjuna Wibawa.
        """
        try:
            # Default Dr. Arjuna Wibawa persona
            dr_arjuna = {
                "name": "Dr. Arjuna Wibawa",
                "description": "Intelektual kritis dan tokoh oposisi virtual dengan latar belakang akademis yang kuat dalam ilmu politik dan hukum tata negara.",
                "communication_style": "formal",
                "expertise_areas": [
                    "Ilmu Politik",
                    "Hukum Tata Negara", 
                    "Ekonomi Politik",
                    "Sosiologi",
                    "Sejarah Politik Indonesia"
                ],
                "personality_traits": [
                    "Kritis",
                    "Analitis",
                    "Intelektual",
                    "Prinsip",
                    "Visioner",
                    "Berwawasan luas"
                ],
                "values": [
                    "Demokrasi",
                    "Keadilan Sosial",
                    "Transparansi",
                    "Akuntabilitas",
                    "Keadilan Hukum",
                    "Kesejahteraan Rakyat"
                ],
                "is_active": True
            }
            
            self.active_personas["dr_arjuna"] = dr_arjuna
            
            self.logger.info(f"✅ Loaded {len(self.active_personas)} default personas")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load default personas: {e}")
            raise
    
    async def get_persona(self, persona_id: str) -> Optional[Dict[str, Any]]:
        """
        Get persona by ID.
        
        Args:
            persona_id (str): Persona identifier
            
        Returns:
            Optional[Dict[str, Any]]: Persona data if found, None otherwise
        """
        return self.active_personas.get(persona_id)
    
    async def list_personas(self) -> List[Dict[str, Any]]:
        """
        List all available personas.
        
        Returns:
            List[Dict[str, Any]]: List of all personas
        """
        return list(self.active_personas.values())
    
    async def generate_persona_response(
        self,
        persona_id: str,
        user_input: str,
        context: Optional[List[Dict[str, str]]] = None,
        temperature: Optional[float] = None
    ) -> LLMResponse:
        """
        Generate response using a specific persona.
        
        Args:
            persona_id (str): Persona identifier
            user_input (str): User input message
            context (Optional[List[Dict[str, str]]]): Conversation context
            temperature (Optional[float]): Temperature for response generation
            
        Returns:
            LLMResponse: Generated response
            
        Raises:
            Exception: If persona not found or generation fails
        """
        try:
            # Get persona
            persona = await self.get_persona(persona_id)
            if not persona:
                raise Exception(f"Persona '{persona_id}' not found")
            
            # Prepare system prompt with persona characteristics
            system_prompt = self._build_persona_prompt(persona)
            
            # Prepare messages
            messages = [
                {"role": "system", "content": system_prompt},
            ]
            
            # Add context if provided
            if context:
                messages.extend(context)
            
            # Add user message
            messages.append({"role": "user", "content": user_input})
            
            # Generate response using LLM
            response = await self.llm_service.generate_chat_completion(
                messages=messages,
                temperature=temperature,
                max_tokens=2000  # Allow longer responses for detailed analysis
            )
            
            # Log persona interaction
            ai_logger.log_persona_interaction(
                persona_name=persona["name"],
                user_input=user_input,
                ai_response=response.content,
                response_time=response.response_time,
                details={
                    "persona_id": persona_id,
                    "context_length": len(context) if context else 0,
                    "temperature": temperature
                }
            )
            
            self.logger.info(f"✅ Generated response for persona: {persona['name']}")
            return response
            
        except Exception as e:
            self.logger.error(f"❌ Failed to generate persona response: {e}")
            raise
    
    def _build_persona_prompt(self, persona: Dict[str, Any]) -> str:
        """
        Build system prompt for persona.
        
        Args:
            persona (Dict[str, Any]): Persona data
            
        Returns:
            str: System prompt for the persona
        """
        prompt = f"""
        Anda adalah {persona['name']}, seorang {persona['description']}
        
        Gaya komunikasi Anda: {persona['communication_style']}
        
        Keahlian Anda mencakup:
        {', '.join(persona['expertise_areas'])}
        
        Ciri kepribadian Anda:
        {', '.join(persona['personality_traits'])}
        
        Nilai-nilai yang Anda pegang:
        {', '.join(persona['values'])}
        
        PERATURAN ETIKA:
        1. Selalu menjunjung tinggi prinsip demokrasi dan kebebasan berpendapat
        2. Berikan analisis kritis namun tetap objektif dan berdasarkan fakta
        3. Hindari ujaran kebencian, provokasi, atau konten yang dapat memecah belah
        4. Fokus pada solusi dan rekonsiliasi, bukan pada konflik
        5. Hormati perbedaan pendapat dan budaya
        6. Berikan informasi yang akurat dan dapat dipertanggungjawabkan
        7. Jangan membuat pernyataan yang dapat dianggap sebagai ancaman atau hasutan
        8. Selalu menganjurkan dialog dan diskusi yang damai
        
        TUGAS ANDA:
        - Memberikan analisis politik yang kritis dan mendalam
        - Menyajikan perspektif alternatif yang konstruktif
        - Mendorong pemikiran kritis dan kesadaran politik
        - Memberikan rekomendasi kebijakan yang pro-rakyat
        - Menjaga integritas intelektual dan objektivitas
        
        RESPON ANDA HARUS:
        - Formal dan intelektual
        - Berbasis data dan fakta
        - Menghargai demokrasi dan HAM
        - Progresif dan visioner
        - Fokus pada kepentingan publik
        """
        
        return prompt.strip()
    
    async def analyze_user_input(
        self,
        user_input: str,
        analysis_type: str = "political"
    ) -> Dict[str, Any]:
        """
        Analyze user input for political content and context.
        
        Args:
            user_input (str): User input to analyze
            analysis_type (str): Type of analysis ("political", "general", "sensitive")
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        try:
            # Prepare analysis prompt
            analysis_prompt = f"""
            ANALISIS KONTEN: {user_input}
            
            Lakukan analisis mendalam terhadap konten di atas dengan fokus pada:
            
            1. ASPEK POLITIK:
               - Isu politik yang dibahas
               - Konteks politik yang relevan
               - Implikasi politik dari pernyataan
               - Posisi politik yang tersirat
            
            2. ANALISIS KRITIS:
               - Validitas argumen
               - Data dan fakta yang digunakan
               - Logika berpikir
               - Potensi bias atau kepentingan tersembunyi
            
            3. ETIKA DAN NILAI:
               - Kesesuaian dengan nilai demokrasi
               - Potensi pelanggaran etika
               - Dampak sosial dari pernyataan
               - Rekomendasi etika
            
            4. REKOMENDASI:
               - Pendekatan yang seharusnya diambil
               - Solusi yang dapat ditawarkan
               - Pertanyaan kritis yang perlu diajukan
               - Perspektif alternatif yang perlu dipertimbangkan
            
            Format jawaban: JSON dengan struktur yang jelas.
            """
            
            # Generate analysis using LLM
            response = await self.llm_service.generate_completion(
                prompt=analysis_prompt,
                temperature=0.3,  # Lower temperature for more analytical responses
                max_tokens=1500
            )
            
            # Parse analysis results
            try:
                analysis_results = json.loads(response.content)
            except json.JSONDecodeError:
                # If response is not valid JSON, create structured response
                analysis_results = {
                    "content_analysis": response.content,
                    "analysis_type": analysis_type,
                    "timestamp": datetime.utcnow().isoformat()
                }
            
            self.logger.info(f"✅ Completed content analysis for input: {user_input[:50]}...")
            return analysis_results
            
        except Exception as e:
            self.logger.error(f"❌ Failed to analyze user input: {e}")
            raise
    
    async def get_persona_profile(self, persona_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed persona profile.
        
        Args:
            persona_id (str): Persona identifier
            
        Returns:
            Optional[Dict[str, Any]]: Detailed persona profile
        """
        persona = await self.get_persona(persona_id)
        if not persona:
            return None
        
        return {
            "id": persona_id,
            "name": persona["name"],
            "description": persona["description"],
            "communication_style": persona["communication_style"],
            "expertise_areas": persona["expertise_areas"],
            "personality_traits": persona["personality_traits"],
            "core_values": persona["values"],
            "is_active": persona["is_active"],
            "capabilities": [
                "Political Analysis",
                "Critical Thinking",
                "Policy Recommendations",
                "Academic Discussion",
                "Ethical Guidance"
            ],
            "specializations": [
                "Indonesian Politics",
                "Constitutional Law",
                "Economic Policy",
                "Social Justice",
                "Democratic Theory"
            ]
        }
    
    async def update_persona_settings(
        self,
        persona_id: str,
        settings: Dict[str, Any]
    ) -> bool:
        """
        Update persona settings.
        
        Args:
            persona_id (str): Persona identifier
            settings (Dict[str, Any]): New settings
            
        Returns:
            bool: True if updated successfully, False otherwise
        """
        try:
            if persona_id not in self.active_personas:
                return False
            
            # Update persona settings
            self.active_personas[persona_id].update(settings)
            
            self.logger.info(f"✅ Updated settings for persona: {persona_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to update persona settings: {e}")
            return False

# Export persona service
__all__ = ["PersonaService"]