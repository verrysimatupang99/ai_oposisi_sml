"""
Authentication API Endpoints

This module contains authentication-related API endpoints for the
AI Tokoh Oposisi & Intelektual Kritis system.

Author: AI Assistant
Created: 2025-01-11
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
# from typing import Dict, Any (Removed unused imports)

from app.core.database import get_db
from app.core.security import (
    authenticate_user, create_access_token, create_refresh_token,
    hash_password, is_valid_username, is_valid_email, is_valid_password,
    get_current_user
)
from app.core.config import settings
from app.models.user import User
from app.schemas.auth import UserCreate, UserResponse, Token, TokenRefresh
from app.utils.logger import security_logger
import logging

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    
    Args:
        user_data (UserCreate): User registration data
        db (Session): Database session
        
    Returns:
        UserResponse: Created user information
        
    Raises:
        HTTPException: If registration fails
    """
    try:
        # Validate input data
        if not is_valid_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid username format"
            )
        
        if not is_valid_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )
        
        if not is_valid_password(user_data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters with uppercase, lowercase, digit, and special character"
            )
        
        # Check if username already exists
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = hash_password(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Log registration event
        security_logger.log_authentication(
            username=new_user.username,
            success=True,
            details={
                "action": "registration",
                "full_name": new_user.full_name,
                "email": new_user.email
            }
        )
        
        return UserResponse(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            full_name=new_user.full_name,
            is_active=new_user.is_active,
            created_at=new_user.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        security_logger.log_authentication(
            username=user_data.username,
            success=False,
            details={
                "action": "registration",
                "error": str(e)
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return access tokens.
    """
    import traceback
    try:
        logger.info(f"Attempting login for user: {form_data.username}")
        # Authenticate user
        user = authenticate_user(db, form_data.username, form_data.password)
        
        if not user:
            logger.warning(f"Login failed for {form_data.username}: Invalid credentials")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        logger.info(f"Login successful for {form_data.username}, creating tokens")
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "username": user.username},
            expires_delta=access_token_expires
        )
        
        # Create refresh token
        refresh_token = create_refresh_token(
            data={"sub": str(user.id), "username": user.username}
        )
        
        logger.info("Tokens created successfully")
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser,
                "created_at": user.created_at,
                "updated_at": user.updated_at
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login unexpected error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}"
        )

@router.post("/refresh", response_model=Token)
async def refresh_token(
    token_data: TokenRefresh,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    
    Args:
        token_data (TokenRefresh): Refresh token data
        db (Session): Database session
        
    Returns:
        Token: New access and refresh tokens
        
    Raises:
        HTTPException: If token refresh fails
    """
    try:
        from jose import jwt, JWTError
        
        # Verify refresh token
        try:
            payload = jwt.decode(
                token_data.refresh_token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM]
            )
            
            # Check if token type is refresh token
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            user_id: str = payload.get("sub")
            username: str = payload.get("username")
            
            if user_id is None or username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify user still exists and is active
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create new access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "username": user.username},
            expires_delta=access_token_expires
        )
        
        # Create new refresh token
        refresh_token = create_refresh_token(
            data={"sub": str(user.id), "username": user.username}
        )
        
        # Log token refresh
        security_logger.log_authentication(
            username=user.username,
            success=True,
            details={
                "action": "token_refresh",
                "user_id": str(user.id)
            }
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        security_logger.log_authentication(
            username="unknown",
            success=False,
            details={
                "action": "token_refresh",
                "error": str(e)
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user information.
    
    Args:
        current_user (User): Current authenticated user
        
    Returns:
        UserResponse: Current user information
    """
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )

@router.post("/logout")
async def logout_user(
    current_user: User = Depends(get_current_user)
):
    """
    Logout user (client-side token removal).
    
    Args:
        current_user (User): Current authenticated user
        
    Returns:
        Dict[str, str]: Success message
    """
    # Log logout event
    security_logger.log_authentication(
        username=current_user.username,
        success=True,
        details={
            "action": "logout",
            "user_id": str(current_user.id)
        }
    )
    
    return {"message": "Successfully logged out"}

@router.put("/change-password")
async def change_password(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change user password.
    
    Args:
        current_user (User): Current authenticated user
        db (Session): Database session
        
    Returns:
        Dict[str, str]: Success message
        
    Raises:
        HTTPException: If password change fails
    """
    try:
        # Implementation for password change
        # This would typically require current password verification
        # and new password validation
        
        return {"message": "Password change functionality"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed"
        )

# Export router
__all__ = ["router"]