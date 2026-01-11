"""
Logging Utilities

This module contains logging configuration and utilities for the
AI Tokoh Oposisi & Intelektual Kritis system.

Author: AI Assistant
Created: 2025-01-11
"""

import logging
import logging.config
import os
from datetime import datetime
from typing import Dict, Any, Optional
import json

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'simple': {
            'format': '%(levelname)s - %(message)s'
        },
        'json': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(module)s - %(funcName)s - %(lineno)d'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': 'logs/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'encoding': 'utf8'
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'detailed',
            'filename': 'logs/error.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'encoding': 'utf8'
        },
        'security_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'json',
            'filename': 'logs/security.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'encoding': 'utf8'
        }
    },
    'loggers': {
        'app': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
            'propagate': False
        },
        'app.security': {
            'level': 'INFO',
            'handlers': ['security_file'],
            'propagate': False
        },
        'app.ai': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
            'propagate': False
        },
        'app.ethics': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
            'propagate': False
        },
        'uvicorn': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False
        },
        'uvicorn.error': {
            'level': 'INFO',
            'handlers': ['console', 'error_file'],
            'propagate': False
        },
        'uvicorn.access': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    }
}

def setup_logging():
    """
    Setup logging configuration.
    
    Creates log directories if they don't exist and configures logging
    based on the LOGGING_CONFIG dictionary.
    """
    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Created log directory: {log_dir}")
    
    # Configure logging
    logging.config.dictConfig(LOGGING_CONFIG)
    
    # Get root logger
    logger = logging.getLogger()
    logger.info("Logging configuration loaded successfully")

class SecurityLogger:
    """
    Security-focused logger for logging security events.
    
    This class provides methods for logging security-related events
    with structured data for analysis and monitoring.
    """
    
    def __init__(self):
        self.logger = logging.getLogger('app.security')
    
    def log_authentication(self, username: str, success: bool, ip_address: Optional[str] = None, 
                          user_agent: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        """
        Log authentication events.
        
        Args:
            username (str): Username
            success (bool): Whether authentication was successful
            ip_address (Optional[str]): IP address of the request
            user_agent (Optional[str]): User agent string
            details (Optional[Dict[str, Any]]): Additional details
        """
        event_data = {
            'event_type': 'authentication',
            'username': username,
            'success': success,
            'timestamp': datetime.utcnow().isoformat(),
            'ip_address': ip_address,
            'user_agent': user_agent,
            'details': details or {}
        }
        
        if success:
            self.logger.info(f"Authentication successful: {json.dumps(event_data)}")
        else:
            self.logger.warning(f"Authentication failed: {json.dumps(event_data)}")
    
    def log_authorization(self, username: str, resource: str, action: str, 
                         allowed: bool, details: Optional[Dict[str, Any]] = None):
        """
        Log authorization events.
        
        Args:
            username (str): Username
            resource (str): Resource being accessed
            action (str): Action being performed
            allowed (bool): Whether access was allowed
            details (Optional[Dict[str, Any]]): Additional details
        """
        event_data = {
            'event_type': 'authorization',
            'username': username,
            'resource': resource,
            'action': action,
            'allowed': allowed,
            'timestamp': datetime.utcnow().isoformat(),
            'details': details or {}
        }
        
        if allowed:
            self.logger.info(f"Authorization granted: {json.dumps(event_data)}")
        else:
            self.logger.warning(f"Authorization denied: {json.dumps(event_data)}")
    
    def log_data_access(self, username: str, data_type: str, action: str,
                       success: bool, details: Optional[Dict[str, Any]] = None):
        """
        Log data access events.
        
        Args:
            username (str): Username
            data_type (str): Type of data accessed
            action (str): Action performed (read, write, delete)
            success (bool): Whether the action was successful
            details (Optional[Dict[str, Any]]): Additional details
        """
        event_data = {
            'event_type': 'data_access',
            'username': username,
            'data_type': data_type,
            'action': action,
            'success': success,
            'timestamp': datetime.utcnow().isoformat(),
            'details': details or {}
        }
        
        if success:
            self.logger.info(f"Data access successful: {json.dumps(event_data)}")
        else:
            self.logger.error(f"Data access failed: {json.dumps(event_data)}")
    
    def log_ethics_violation(self, content: str, violations: list, 
                           confidence: float, details: Optional[Dict[str, Any]] = None):
        """
        Log ethics violations.
        
        Args:
            content (str): Content that violated ethics
            violations (list): List of violations detected
            confidence (float): Confidence score of violation detection
            details (Optional[Dict[str, Any]]): Additional details
        """
        event_data = {
            'event_type': 'ethics_violation',
            'violations': violations,
            'confidence': confidence,
            'timestamp': datetime.utcnow().isoformat(),
            'content_preview': content[:100] + '...' if len(content) > 100 else content,
            'details': details or {}
        }
        
        self.logger.warning(f"Ethics violation detected: {json.dumps(event_data)}")

class AILogger:
    """
    AI-focused logger for logging AI-related events.
    
    This class provides methods for logging AI model interactions,
    responses, and performance metrics.
    """
    
    def __init__(self):
        self.logger = logging.getLogger('app.ai')
    
    def log_model_interaction(self, model_name: str, prompt: str, response: str,
                            response_time: float, tokens_used: int, 
                            details: Optional[Dict[str, Any]] = None):
        """
        Log AI model interactions.
        
        Args:
            model_name (str): Name of the AI model
            prompt (str): Input prompt
            response (str): Model response
            response_time (float): Time taken for response in seconds
            tokens_used (int): Number of tokens used
            details (Optional[Dict[str, Any]]): Additional details
        """
        event_data = {
            'event_type': 'model_interaction',
            'model_name': model_name,
            'prompt_preview': prompt[:100] + '...' if len(prompt) > 100 else prompt,
            'response_preview': response[:100] + '...' if len(response) > 100 else response,
            'response_time': response_time,
            'tokens_used': tokens_used,
            'timestamp': datetime.utcnow().isoformat(),
            'details': details or {}
        }
        
        self.logger.info(f"Model interaction: {json.dumps(event_data)}")
    
    def log_model_error(self, model_name: str, error: str, 
                       details: Optional[Dict[str, Any]] = None):
        """
        Log AI model errors.
        
        Args:
            model_name (str): Name of the AI model
            error (str): Error message
            details (Optional[Dict[str, Any]]): Additional details
        """
        event_data = {
            'event_type': 'model_error',
            'model_name': model_name,
            'error': error,
            'timestamp': datetime.utcnow().isoformat(),
            'details': details or {}
        }
        
        self.logger.error(f"Model error: {json.dumps(event_data)}")
    
    def log_persona_interaction(self, persona_name: str, user_input: str, 
                              ai_response: str, response_time: float,
                              details: Optional[Dict[str, Any]] = None):
        """
        Log persona interactions.
        
        Args:
            persona_name (str): Name of the persona
            user_input (str): User input
            ai_response (str): AI response
            response_time (float): Time taken for response
            details (Optional[Dict[str, Any]]): Additional details
        """
        event_data = {
            'event_type': 'persona_interaction',
            'persona_name': persona_name,
            'user_input_preview': user_input[:100] + '...' if len(user_input) > 100 else user_input,
            'ai_response_preview': ai_response[:100] + '...' if len(ai_response) > 100 else ai_response,
            'response_time': response_time,
            'timestamp': datetime.utcnow().isoformat(),
            'details': details or {}
        }
        
        self.logger.info(f"Persona interaction: {json.dumps(event_data)}")

class EthicsLogger:
    """
    Ethics-focused logger for logging ethics validation events.
    
    This class provides methods for logging ethics validation results
    and policy enforcement actions.
    """
    
    def __init__(self):
        self.logger = logging.getLogger('app.ethics')
    
    def log_validation_result(self, content_type: str, is_valid: bool, 
                            violations: list, confidence: float,
                            details: Optional[Dict[str, Any]] = None):
        """
        Log ethics validation results.
        
        Args:
            content_type (str): Type of content being validated
            is_valid (bool): Whether content passed validation
            violations (list): List of violations (if any)
            confidence (float): Confidence score of validation
            details (Optional[Dict[str, Any]]): Additional details
        """
        event_data = {
            'event_type': 'ethics_validation',
            'content_type': content_type,
            'is_valid': is_valid,
            'violations': violations,
            'confidence': confidence,
            'timestamp': datetime.utcnow().isoformat(),
            'details': details or {}
        }
        
        if is_valid:
            self.logger.info(f"Content validation passed: {json.dumps(event_data)}")
        else:
            self.logger.warning(f"Content validation failed: {json.dumps(event_data)}")
    
    def log_policy_enforcement(self, policy_name: str, action: str, 
                             content_preview: str, details: Optional[Dict[str, Any]] = None):
        """
        Log policy enforcement actions.
        
        Args:
            policy_name (str): Name of the policy enforced
            action (str): Action taken (blocked, modified, flagged)
            content_preview (str): Preview of the content
            details (Optional[Dict[str, Any]]): Additional details
        """
        event_data = {
            'event_type': 'policy_enforcement',
            'policy_name': policy_name,
            'action': action,
            'content_preview': content_preview,
            'timestamp': datetime.utcnow().isoformat(),
            'details': details or {}
        }
        
        self.logger.info(f"Policy enforcement: {json.dumps(event_data)}")

# Create global logger instances
security_logger = SecurityLogger()
ai_logger = AILogger()
ethics_logger = EthicsLogger()

# Export logger classes and instances
__all__ = [
    "setup_logging", "SecurityLogger", "AILogger", "EthicsLogger",
    "security_logger", "ai_logger", "ethics_logger"
]