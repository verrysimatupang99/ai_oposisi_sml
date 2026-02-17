"""
Ethics Service

This module contains the ethics service for managing content validation,
ethics protocols, and democracy compliance for the AI Tokoh Oposisi & 
Intelektual Kritis system.

Author: AI Assistant
Created: 2025-01-11
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import re
from enum import Enum

from app.core.config import settings
from app.services.llm_service import LLMService
from app.utils.logger import ethics_logger
from app.models.ethics_validation import EthicsValidation
from sqlalchemy.orm import Session

class ViolationType(Enum):
    """Types of ethics violations."""
    HATE_SPEECH = "hate_speech"
    VIOLENCE = "violence"
    MISINFORMATION = "misinformation"
    HARASSMENT = "harassment"
    ILLEGAL_CONTENT = "illegal_content"
    POLITICAL_MANIPULATION = "political_manipulation"
    DEMOCRACY_THREAT = "democracy_threat"
    OTHER = "other"

class EthicsStatus(Enum):
    """Ethics validation status."""
    VALID = "valid"
    VIOLATION = "violation"
    WARNING = "warning"
    REVIEW_REQUIRED = "review_required"

class EthicsService:
    """Service for managing ethics validation and content filtering."""
    
    def __init__(self):
        """Initialize ethics service."""
        self.logger = logging.getLogger(__name__)
        self.violation_patterns = self._load_violation_patterns()
        self.democracy_protocols = self._load_democracy_protocols()
        
    async def initialize(self):
        """
        Initialize ethics service.
        
        Loads violation patterns and democracy protocols.
        """
        try:
            self.logger.info("Initializing Ethics service...")
            
            # Validate configuration
            if not settings.ETHICS_ENABLED:
                self.logger.warning("Ethics validation is disabled in configuration")
            
            self.logger.info("Ethics service initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize ethics service: {e}")
            raise
    
    def _load_violation_patterns(self) -> Dict[str, List[str]]:
        """
        Load violation detection patterns.
        
        Returns:
            Dict[str, List[str]]: Dictionary of violation patterns
        """
        return {
            ViolationType.HATE_SPEECH.value: [
                r'\b(hate|hateful|racist|nazi|kkk|white\s+power|black\s+power)\b',
                r'\b(discriminat|prejudice|bigot|extremist)\b',
                r'\b(ethnic\s+cleansing|genocide|holocaust)\b'
            ],
            ViolationType.VIOLENCE.value: [
                r'\b(kill|murder|assassin|terrorist|bomb|explosive)\b',
                r'\b(war|battle|fight|violence|aggression)\b',
                r'\b(weapon|gun|knife|poison|arsenal)\b'
            ],
            ViolationType.MISINFORMATION.value: [
                r'\b(fake\s+news|conspiracy|hoax|false\s+information)\b',
                r'\b(lie|deception|fraud|scam)\b',
                r'\b(unverified\s+claim|baseless\s+rumor)\b'
            ],
            ViolationType.HARASSMENT.value: [
                r'\b(bully|harass|threaten|intimidate)\b',
                r'\b(stalk|cyberbully|online\s+abuse)\b',
                r'\b(insult|mock|ridicule|humiliate)\b'
            ],
            ViolationType.ILLEGAL_CONTENT.value: [
                r'\b(illegal|crime|criminal|fraud|corruption)\b',
                r'\b(drug|narcotic|substance|addiction)\b',
                r'\b(hack|crack|piracy|copyright)\b'
            ],
            ViolationType.POLITICAL_MANIPULATION.value: [
                r'\b(manipulat|propaganda|brainwash|indoctrinat)\b',
                r'\b(vote\s+fraud|election\s+rigging|ballot\s+stuffing)\b',
                r'\b(bribe|corrupt|kickback|embezzle)\b'
            ],
            ViolationType.DEMOCRACY_THREAT.value: [
                r'\b(dictator|authoritarian|totalitarian|tyranny)\b',
                r'\b(coup|revolution|overthrow|insurgency)\b',
                r'\b(censorship|suppression|oppression|repression)\b'
            ]
        }
    
    def _load_democracy_protocols(self) -> Dict[str, Any]:
        """
        Load democracy protocols and guidelines.
        
        Returns:
            Dict[str, Any]: Democracy protocols configuration
        """
        return {
            "core_principles": [
                "Respect for democratic institutions",
                "Protection of human rights and freedoms",
                "Promotion of peaceful dialogue",
                "Support for rule of law",
                "Encouragement of civic participation"
            ],
            "prohibited_actions": [
                "Inciting violence or hatred",
                "Spreading misinformation",
                "Undermining democratic processes",
                "Promoting authoritarian ideologies",
                "Encouraging illegal activities"
            ],
            "required_behaviors": [
                "Provide factual information",
                "Encourage critical thinking",
                "Promote peaceful solutions",
                "Respect diverse opinions",
                "Support democratic values"
            ],
            "response_guidelines": {
                "educational": "Provide educational content about democratic principles",
                "redirect": "Redirect conversation to constructive topics",
                "warn": "Issue warning about inappropriate content",
                "block": "Block harmful content and notify administrators"
            }
        }
    
    async def validate_content(
        self,
        content: str,
        content_type: str = "text",
        strict_mode: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Validate content against ethics protocols.
        
        Args:
            content (str): Content to validate
            content_type (str): Type of content ("text", "response", "analysis")
            strict_mode (Optional[bool]): Whether to use strict validation
            
        Returns:
            Dict[str, Any]: Validation results
        """
        try:
            # Use configuration strict mode if not specified
            if strict_mode is None:
                strict_mode = settings.ETHICS_STRICT_MODE
            
            # Initialize validation results
            validation_results = {
                "is_valid": True,
                "violations": [],
                "confidence_score": 0.0,
                "suggested_action": "allow",
                "details": {
                    "content_type": content_type,
                    "content_length": len(content),
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
            
            # Skip validation if disabled
            if not settings.ETHICS_ENABLED:
                validation_results["is_valid"] = True
                validation_results["suggested_action"] = "bypass"
                return validation_results
            
            # Check for violations
            violations = self._detect_violations(content, strict_mode)
            
            if violations:
                validation_results["is_valid"] = False
                validation_results["violations"] = violations
                validation_results["confidence_score"] = self._calculate_confidence(violations)
                validation_results["suggested_action"] = self._determine_action(violations, strict_mode)
                
                # Log violation
                ethics_logger.log_validation_result(
                    content_type=content_type,
                    is_valid=False,
                    violations=[v["type"] for v in violations],
                    confidence=validation_results["confidence_score"],
                    details=validation_results["details"]
                )
            else:
                validation_results["confidence_score"] = 1.0
                
                # Log successful validation
                ethics_logger.log_validation_result(
                    content_type=content_type,
                    is_valid=True,
                    violations=[],
                    confidence=validation_results["confidence_score"],
                    details=validation_results["details"]
                )
            
            self.logger.info(f"Content validation completed. Valid: {validation_results['is_valid']}")
            return validation_results
            
        except Exception as e:
            self.logger.error(f"Content validation failed: {e}")
            raise
    
    def _detect_violations(self, content: str, strict_mode: bool) -> List[Dict[str, Any]]:
        """
        Detect violations in content.
        
        Args:
            content (str): Content to analyze
            strict_mode (bool): Whether to use strict detection
            
        Returns:
            List[Dict[str, Any]]: List of detected violations
        """
        violations = []
        content_lower = content.lower()
        
        for violation_type, patterns in self.violation_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content_lower, re.IGNORECASE):
                    confidence = self._calculate_violation_confidence(pattern, content_lower, strict_mode)
                    
                    if confidence > 0.5:  # Threshold for violation detection
                        violations.append({
                            "type": violation_type,
                            "pattern": pattern,
                            "confidence": confidence,
                            "message": self._get_violation_message(violation_type)
                        })
        
        return violations
    
    def _calculate_violation_confidence(self, pattern: str, content: str, strict_mode: bool) -> float:
        """
        Calculate confidence score for violation detection.
        
        Args:
            pattern (str): Regex pattern used for detection
            content (str): Content being analyzed
            strict_mode (bool): Whether strict mode is enabled
            
        Returns:
            float: Confidence score (0.0 to 1.0)
        """
        matches = re.findall(pattern, content, re.IGNORECASE)
        
        if not matches:
            return 0.0
        
        # Base confidence based on number of matches
        base_confidence = min(len(matches) * 0.3, 0.8)
        
        # Adjust based on strict mode
        if strict_mode:
            base_confidence += 0.2
        
        # Context analysis for higher confidence
        context_bonus = self._analyze_context(pattern, content)
        
        return min(base_confidence + context_bonus, 1.0)
    
    def _analyze_context(self, pattern: str, content: str) -> float:
        """
        Analyze context around detected patterns for higher confidence.
        
        Args:
            pattern (str): Pattern that was matched
            content (str): Full content being analyzed
            
        Returns:
            float: Context bonus (0.0 to 0.3)
        """
        # Look for intensifying words or phrases around the match
        intensifiers = [
            r'\b(extreme|very|really|truly|absolutely)\b',
            r'\b(always|never|completely|totally)\b',
            r'\b(must|should|shall|will)\b'
        ]
        
        for intensifier in intensifiers:
            if re.search(intensifier, content, re.IGNORECASE):
                return 0.2
        
        return 0.0
    
    def _get_violation_message(self, violation_type: str) -> str:
        """
        Get violation message for a specific violation type.
        
        Args:
            violation_type (str): Type of violation
            
        Returns:
            str: Violation message
        """
        messages = {
            "hate_speech": "Konten mengandung ujaran kebencian atau diskriminasi",
            "violence": "Konten mengandung ancaman kekerasan atau ajakan kekerasan",
            "misinformation": "Konten mengandung informasi palsu atau hoaks",
            "harassment": "Konten mengandung pelecehan atau perundungan",
            "illegal_content": "Konten mengandung promosi aktivitas ilegal",
            "political_manipulation": "Konten mengandung manipulasi politik atau propaganda",
            "democracy_threat": "Konten mengancam nilai-nilai demokrasi"
        }
        
        return messages.get(violation_type, "Konten melanggar protokol etika")
    
    def _calculate_confidence(self, violations: List[Dict[str, Any]]) -> float:
        """
        Calculate overall confidence score for violations.
        
        Args:
            violations (List[Dict[str, Any]]): List of violations
            
        Returns:
            float: Overall confidence score
        """
        if not violations:
            return 1.0
        
        # Calculate weighted average confidence
        total_confidence = sum(v["confidence"] for v in violations)
        max_confidence = max(v["confidence"] for v in violations)
        
        # Weighted average with emphasis on highest confidence
        return (total_confidence / len(violations) * 0.7) + (max_confidence * 0.3)
    
    def _determine_action(self, violations: List[Dict[str, Any]], strict_mode: bool) -> str:
        """
        Determine suggested action based on violations.
        
        Args:
            violations (List[Dict[str, Any]]): List of violations
            strict_mode (bool): Whether strict mode is enabled
            
        Returns:
            str: Suggested action
        """
        if not violations:
            return "allow"
        
        # Check for severe violations
        severe_violations = [
            "violence", "hate_speech", "democracy_threat", "illegal_content"
        ]
        
        has_severe = any(v["type"] in severe_violations for v in violations)
        
        if has_severe or strict_mode:
            return "block"
        elif len(violations) > 2:
            return "warn"
        else:
            return "modify"
    
    async def validate_response(
        self,
        response: str,
        user_input: str,
        context: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Validate AI response for ethics compliance.
        
        Args:
            response (str): AI response to validate
            user_input (str): Original user input
            context (Optional[List[Dict[str, str]]]): Conversation context
            
        Returns:
            Dict[str, Any]: Validation results
        """
        try:
            # Combine user input and response for comprehensive validation
            combined_content = f"User: {user_input}\n\nAI: {response}"
            
            validation_results = await self.validate_content(
                content=combined_content,
                content_type="response",
                strict_mode=True  # Always use strict mode for responses
            )
            
            # Additional response-specific checks
            if validation_results["is_valid"]:
                response_checks = self._check_response_compliance(response, user_input)
                validation_results["response_compliance"] = response_checks
                
                if not response_checks["compliant"]:
                    validation_results["is_valid"] = False
                    validation_results["violations"].extend(response_checks["violations"])
            
            return validation_results
            
        except Exception as e:
            self.logger.error(f"Response validation failed: {e}")
            raise
    
    def _check_response_compliance(self, response: str, user_input: str) -> Dict[str, Any]:
        """
        Check response compliance with specific guidelines.
        
        Args:
            response (str): AI response
            user_input (str): User input
            
        Returns:
            Dict[str, Any]: Compliance check results
        """
        compliance = {
            "compliant": True,
            "violations": [],
            "issues": []
        }
        
        # Check for appropriate disclaimers
        if any(keyword in user_input.lower() for keyword in ["saran", "rekomendasi", "pendapat"]):
            if not any(phrase in response.lower() for phrase in [
                "sebagai informasi", "sebagai referensi", "menurut pendapat saya",
                "sebagai masukan", "sebagai bahan pertimbangan"
            ]):
                compliance["issues"].append("Response lacks appropriate disclaimer")
        
        # Check for factual accuracy claims
        if re.search(r'\b(fact|truth|reality|actually)\b', response, re.IGNORECASE):
            if not any(phrase in response.lower() for phrase in [
                "berdasarkan data", "menurut sumber", "dilaporkan bahwa", "diketahui bahwa"
            ]):
                compliance["issues"].append("Response makes unverified factual claims")
        
        # Check for balanced perspective
        if any(keyword in user_input.lower() for keyword in ["pendapat", "opini", "menurut anda"]):
            if not any(phrase in response.lower() for phrase in [
                "dari sudut pandang", "menurut beberapa", "ada pendapat yang", "beberapa pihak"
            ]):
                compliance["issues"].append("Response lacks balanced perspective")
        
        # Mark as non-compliant if there are issues
        if compliance["issues"]:
            compliance["compliant"] = False
            compliance["violations"].append({
                "type": "response_quality",
                "message": "Response quality issues detected",
                "issues": compliance["issues"]
            })
        
        return compliance
    
    async def get_ethics_report(self) -> Dict[str, Any]:
        """
        Get ethics service status and statistics.
        
        Returns:
            Dict[str, Any]: Ethics service report
        """
        return {
            "service_status": "active" if settings.ETHICS_ENABLED else "disabled",
            "strict_mode": settings.ETHICS_STRICT_MODE,
            "content_filter_enabled": settings.CONTENT_FILTER_ENABLED,
            "violation_patterns_count": len(self.violation_patterns),
            "democracy_protocols_loaded": len(self.democracy_protocols) > 0,
            "timestamp": datetime.utcnow().isoformat()
        }

# Export ethics service
__all__ = ["EthicsService", "ViolationType", "EthicsStatus"]