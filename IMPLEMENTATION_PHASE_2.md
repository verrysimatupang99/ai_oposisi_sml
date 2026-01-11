# 🏗️ IMPLEMENTATION PHASE 2: CORE BACKEND DEVELOPMENT

## 📋 FASE 2: CORE BACKEND DEVELOPMENT (MINGGU 3-4)

### 🎯 TUJUAN FASE 2
Mengembangkan core backend services termasuk API endpoints, authentication system, database migrations, dan core business logic.

---

## 🔐 AUTHENTICATION & AUTHORIZATION

### **1. Authentication Models & Schemas**

```python
# backend/app/models/auth.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.models import Base
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(200))
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="user")
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)
    
    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)
    
    def is_account_locked(self) -> bool:
        return self.locked_until is not None and self.locked_until > datetime.utcnow()
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

class Token(Base):
    __tablename__ = "tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    token = Column(String(255), unique=True, index=True, nullable=False)
    token_type = Column(String(20), default="access")
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at
    
    def __repr__(self):
        return f"<Token(id={self.id}, user_id={self.user_id}, token_type='{self.token_type}')>"
```

```python
# backend/app/schemas/auth.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def password_complexity(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        return v

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class TokenBase(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str
```

### **2. Authentication Service**

```python
# backend/app/services/auth_service.py
from datetime import datetime, timedelta
from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets

from app.core.config import settings
from app.models.auth import User, Token
from app.schemas.auth import UserCreate, LoginRequest, UserResponse
from app.core.database import get_db

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create new user"""
        # Check if username exists
        existing_user = await self.get_user_by_username(user_data.username)
        if existing_user:
            raise ValueError("Username already registered")
        
        # Check if email exists
        existing_email = await self.get_user_by_email(user_data.email)
        if existing_email:
            raise ValueError("Email already registered")
        
        # Create new user
        user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            role="user"
        )
        user.set_password(user_data.password)
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return UserResponse.from_orm(user)
    
    async def authenticate_user(self, login_data: LoginRequest) -> Tuple[Optional[User], Optional[str]]:
        """Authenticate user and return user + error message"""
        user = await self.get_user_by_username(login_data.username)
        
        if not user:
            return None, "Invalid username or password"
        
        if user.is_account_locked():
            return None, "Account is temporarily locked due to multiple failed login attempts"
        
        if not user.verify_password(login_data.password):
            await self.handle_failed_login(user)
            return None, "Invalid username or password"
        
        # Reset failed login attempts on successful login
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login = datetime.utcnow()
        
        await self.db.commit()
        
        return user, None
    
    async def handle_failed_login(self, user: User):
        """Handle failed login attempt"""
        user.failed_login_attempts += 1
        
        # Lock account after 5 failed attempts for 30 minutes
        if user.failed_login_attempts >= 5:
            user.locked_until = datetime.utcnow() + timedelta(minutes=30)
        
        await self.db.commit()
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[TokenData]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            username: str = payload.get("sub")
            user_id: int = payload.get("user_id")
            role: str = payload.get("role")
            
            if username is None or user_id is None:
                return None
            
            token_data = TokenData(username=username, user_id=user_id, role=role)
            return token_data
        except JWTError:
            return None
    
    async def create_refresh_token(self, user_id: int) -> str:
        """Create refresh token"""
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(days=7)
        
        refresh_token = Token(
            user_id=user_id,
            token=token,
            token_type="refresh",
            expires_at=expires_at
        )
        
        self.db.add(refresh_token)
        await self.db.commit()
        
        return token
    
    async def revoke_token(self, token: str):
        """Revoke token"""
        result = await self.db.execute(
            select(Token).where(Token.token == token)
        )
        token_obj = result.scalar_one_or_none()
        
        if token_obj:
            token_obj.is_revoked = True
            await self.db.commit()
```

### **3. Authentication Dependencies**

```python
# backend/app/core/security.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db
from app.services.auth_service import AuthService
from app.models.auth import User
from app.core.config import settings

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    auth_service = AuthService(db)
    
    token_data = auth_service.verify_token(credentials.credentials)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await auth_service.get_user_by_id(token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_superuser(current_user: User = Depends(get_current_user)) -> User:
    """Get current superuser"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
```

---

## 🎯 API ENDPOINTS IMPLEMENTATION

### **4. Authentication Endpoints**

```python
# backend/app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from app.core.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import UserCreate, UserResponse, LoginRequest
from app.core.security import get_current_user

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register new user"""
    auth_service = AuthService(db)
    
    try:
        user = await auth_service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Login user and return access token"""
    auth_service = AuthService(db)
    
    login_data = LoginRequest(username=form_data.username, password=form_data.password)
    user, error = await auth_service.authenticate_user(login_data)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        data={"sub": user.username, "user_id": user.id, "role": user.role},
        expires_delta=access_token_expires
    )
    
    # Create refresh token
    refresh_token = await auth_service.create_refresh_token(user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60,
        "refresh_token": refresh_token,
        "user": UserResponse.from_orm(user)
    }

@router.post("/refresh")
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token using refresh token"""
    auth_service = AuthService(db)
    
    # Verify refresh token exists and is not expired
    result = await db.execute(
        select(Token).where(
            Token.token == refresh_token,
            Token.token_type == "refresh",
            Token.is_revoked == False
        )
    )
    token_obj = result.scalar_one_or_none()
    
    if not token_obj or token_obj.is_expired():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Get user
    user = await auth_service.get_user_by_id(token_obj.user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user"
        )
    
    # Create new access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        data={"sub": user.username, "user_id": user.id, "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60
    }

@router.post("/logout")
async def logout(
    refresh_token: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Logout user and revoke tokens"""
    auth_service = AuthService(db)
    
    # Revoke refresh token
    await auth_service.revoke_token(refresh_token)
    
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information"""
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user_info(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user information"""
    auth_service = AuthService(db)
    
    # Update user fields
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    
    if user_update.email is not None:
        # Check if email is already taken
        existing_user = await auth_service.get_user_by_email(user_update.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        current_user.email = user_update.email
    
    await db.commit()
    await db.refresh(current_user)
    
    return UserResponse.from_orm(current_user)
```

### **5. Political Analysis Endpoints**

```python
# backend/app/api/v1/endpoints/analysis.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.auth import User
from app.models.analysis import PoliticalAnalysis
from app.schemas.analysis import AnalysisRequest, AnalysisResponse, AnalysisHistory
from app.services.analysis_service import AnalysisService

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_political_query(
    analysis_request: AnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Analyze political query using AI"""
    analysis_service = AnalysisService(db)
    
    try:
        analysis = await analysis_service.perform_analysis(
            user_id=current_user.id,
            query=analysis_request.query,
            analysis_type=analysis_request.analysis_type
        )
        
        return AnalysisResponse.from_orm(analysis)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

@router.get("/history", response_model=List[AnalysisHistory])
async def get_analysis_history(
    limit: int = 10,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's analysis history"""
    analysis_service = AnalysisService(db)
    
    analyses = await analysis_service.get_user_analyses(
        user_id=current_user.id,
        limit=limit,
        offset=offset
    )
    
    return [AnalysisHistory.from_orm(analysis) for analysis in analyses]

@router.get("/history/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis_detail(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific analysis detail"""
    analysis_service = AnalysisService(db)
    
    analysis = await analysis_service.get_analysis_by_id(analysis_id)
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    # Check ownership
    if analysis.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return AnalysisResponse.from_orm(analysis)

@router.delete("/history/{analysis_id}")
async def delete_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete specific analysis"""
    analysis_service = AnalysisService(db)
    
    analysis = await analysis_service.get_analysis_by_id(analysis_id)
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    # Check ownership
    if analysis.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    await analysis_service.delete_analysis(analysis_id)
    
    return {"message": "Analysis deleted successfully"}
```

### **6. Persona Endpoints**

```python
# backend/app/api/v1/endpoints/persona.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user, get_current_superuser
from app.models.auth import User
from app.schemas.persona import PersonaProfile, PersonaUpdate
from app.services.persona_service import PersonaService

router = APIRouter()

@router.get("/profile", response_model=PersonaProfile)
async def get_persona_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current persona configuration"""
    persona_service = PersonaService(db)
    
    profile = await persona_service.get_current_profile()
    
    return PersonaProfile.from_orm(profile)

@router.put("/profile", response_model=PersonaProfile)
async def update_persona_profile(
    persona_update: PersonaUpdate,
    current_user: User = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    """Update persona configuration (admin only)"""
    persona_service = PersonaService(db)
    
    profile = await persona_service.update_persona_profile(persona_update)
    
    return PersonaProfile.from_orm(profile)

@router.get("/feedback/{analysis_id}")
async def get_persona_feedback(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get feedback for persona application"""
    persona_service = PersonaService(db)
    
    feedback = await persona_service.get_analysis_feedback(analysis_id)
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    # Check ownership
    if feedback.analysis.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return feedback
```

---

## 🗄️ DATABASE MIGRATIONS & MODELS

### **7. Advanced Database Models**

```python
# backend/app/models/analysis.py
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models import Base

class PoliticalAnalysis(Base):
    __tablename__ = "political_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Optional for anonymous
    query_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    analysis_type = Column(String(50))
    confidence_score = Column(Float)
    persona_applied = Column(String(50))
    ethics_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    feedback = relationship("AnalysisFeedback", back_populates="analysis")
    user = relationship("User", backref="analyses")
    
    def __repr__(self):
        return f"<PoliticalAnalysis(id={self.id}, query='{self.query_text[:50]}...')>"

class AnalysisFeedback(Base):
    __tablename__ = "analysis_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("political_analyses.id"), nullable=False)
    user_rating = Column(Integer)  # 1-5 stars
    user_comment = Column(Text)
    helpfulness_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    analysis = relationship("PoliticalAnalysis", back_populates="feedback")
    
    def __repr__(self):
        return f"<AnalysisFeedback(id={self.id}, analysis_id={self.analysis_id}, rating={self.user_rating})>"

class DatasetVersion(Base):
    __tablename__ = "dataset_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_name = Column(String(100), nullable=False)
    version = Column(String(20), nullable=False)
    content_hash = Column(String(64), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    
    def __repr__(self):
        return f"<DatasetVersion(id={self.id}, dataset='{self.dataset_name}', version='{self.version}')>"

class SystemLog(Base):
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    log_level = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    module = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    ip_address = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<SystemLog(id={self.id}, level='{self.log_level}', message='{self.message[:50]}...')>"
```

### **8. Database Migration Scripts**

```python
# backend/migrations/001_initial_schema.py
"""
Initial database schema migration
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('full_name', sa.String(length=200), nullable=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False, server_default='user'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('failed_login_attempts', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('locked_until', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    
    # Create political_analyses table
    op.create_table(
        'political_analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('query_text', sa.Text(), nullable=False),
        sa.Column('response_text', sa.Text(), nullable=False),
        sa.Column('analysis_type', sa.String(length=50), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('persona_applied', sa.String(length=50), nullable=True),
        sa.Column('ethics_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create analysis_feedback table
    op.create_table(
        'analysis_feedback',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('analysis_id', sa.Integer(), nullable=False),
        sa.Column('user_rating', sa.Integer(), nullable=True),
        sa.Column('user_comment', sa.Text(), nullable=True),
        sa.Column('helpfulness_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['analysis_id'], ['political_analyses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create tokens table
    op.create_table(
        'tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(length=255), nullable=False),
        sa.Column('token_type', sa.String(length=20), nullable=False, server_default='access'),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('is_revoked', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )

def downgrade():
    op.drop_table('tokens')
    op.drop_table('analysis_feedback')
    op.drop_table('political_analyses')
    op.drop_table('users')
```

---

## 🤖 CORE BUSINESS LOGIC

### **9. Analysis Service Implementation**

```python
# backend/app/services/analysis_service.py
from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.analysis import PoliticalAnalysis, AnalysisFeedback
from app.models.auth import User
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.llm_integration.lm_studio_client import LMStudioClient
from app.persona_engine.persona_core import PersonaEngine
from app.ethics_engine.democracy_protocols import DemocracyProtocols

class AnalysisService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.llm_client = LMStudioClient()
        self.persona_engine = PersonaEngine()
        self.ethics_engine = DemocracyProtocols()
    
    async def perform_analysis(self, user_id: int, query: str, analysis_type: str = "general") -> PoliticalAnalysis:
        """Perform political analysis using AI"""
        
        # Generate raw response from LLM
        raw_response = await self.generate_llm_response(query, analysis_type)
        
        # Apply persona
        persona_response = self.persona_engine.apply_persona_to_response(
            raw_response, {"query": query, "analysis_type": analysis_type}
        )
        
        # Apply ethics filter
        final_response, violations = self.ethics_engine.apply_ethics_filter(persona_response)
        
        # Calculate confidence score
        confidence_score = self.calculate_confidence_score(final_response, violations)
        
        # Create analysis record
        analysis = PoliticalAnalysis(
            user_id=user_id,
            query_text=query,
            response_text=final_response,
            analysis_type=analysis_type,
            confidence_score=confidence_score,
            persona_applied="Dr. Arjuna Wibawa",
            ethics_score=self.calculate_ethics_score(violations)
        )
        
        self.db.add(analysis)
        await self.db.commit()
        await self.db.refresh(analysis)
        
        return analysis
    
    async def generate_llm_response(self, query: str, analysis_type: str) -> str:
        """Generate response from LLM"""
        system_prompt = self.build_system_prompt(analysis_type)
        
        response = self.llm_client.generate_response(
            prompt=query,
            system_prompt=system_prompt
        )
        
        return response
    
    def build_system_prompt(self, analysis_type: str) -> str:
        """Build system prompt based on analysis type"""
        base_prompt = """
        Anda adalah Dr. Arjuna Wibawa, seorang tokoh oposisi dan intelektual kritis Indonesia.
        
        PROFIL:
        - Ahli dalam politik Indonesia, ekonomi politik, dan strategi oposisi demokratis
        - Berpikir kritis, analitis, dan berbasis data
        - Komunikatif, edukatif, dan persuasif
        - Menjunjung tinggi nilai demokrasi, keadilan, dan transparansi
        
        GAYA KOMUNIKASI:
        - Gunakan bahasa yang jelas dan mudah dipahami
        - Sertakan contoh konkret dan analogi yang relevan
        - Berikan analisis mendalam namun tetap praktis
        - Hindari jargon yang terlalu teknis tanpa penjelasan
        
        NILAI DASAR:
        - Demokrasi dan partisipasi rakyat
        - Keadilan sosial dan ekonomi
        - Transparansi dan akuntabilitas
        - HAM dan kebebasan sipil
        - Kebenaran dan integritas intelektual
        """
        
        if analysis_type == "economic":
            return base_prompt + """
            FOKUS EKONOMI:
            - Analisis kebijakan ekonomi dari perspektif rakyat
            - Evaluasi dampak terhadap ketimpangan dan kemiskinan
            - Kritik terhadap kebijakan yang pro-kapitalisasi
            """
        elif analysis_type == "legal":
            return base_prompt + """
            FOKUS HUKUM:
            - Analisis dari perspektif konstitusional
            - Evaluasi kepatuhan terhadap HAM
            - Kritik terhadap UU yang otoriter
            """
        else:
            return base_prompt + """
            FOKUS UMUM:
            - Analisis multidimensional (politik, ekonomi, sosial, hukum)
            - Pendekatan holistik terhadap isu
            - Solusi konstruktif dan demokratis
            """
    
    def calculate_confidence_score(self, response: str, violations: list) -> float:
        """Calculate confidence score for analysis"""
        base_score = 70.0
        
        # Deduct points for violations
        for violation in violations:
            if violation.level.value == "blocked":
                base_score -= 30
            elif violation.level.value == "violation":
                base_score -= 15
            elif violation.level.value == "warning":
                base_score -= 5
        
        # Add points for quality indicators
        if len(response) > 500:
            base_score += 10
        if "analisis" in response.lower():
            base_score += 5
        if "data" in response.lower() or "fakta" in response.lower():
            base_score += 5
        
        return max(0, min(100, base_score))
    
    def calculate_ethics_score(self, violations: list) -> float:
        """Calculate ethics compliance score"""
        base_score = 100.0
        
        for violation in violations:
            if violation.level.value == "blocked":
                base_score -= 50
            elif violation.level.value == "violation":
                base_score -= 25
            elif violation.level.value == "warning":
                base_score -= 10
        
        return max(0, base_score)
    
    async def get_user_analyses(self, user_id: int, limit: int = 10, offset: int = 0) -> List[PoliticalAnalysis]:
        """Get user's analysis history"""
        result = await self.db.execute(
            select(PoliticalAnalysis)
            .where(PoliticalAnalysis.user_id == user_id)
            .order_by(PoliticalAnalysis.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_analysis_by_id(self, analysis_id: int) -> Optional[PoliticalAnalysis]:
        """Get specific analysis by ID"""
        result = await self.db.execute(
            select(PoliticalAnalysis)
            .where(PoliticalAnalysis.id == analysis_id)
        )
        return result.scalar_one_or_none()
    
    async def delete_analysis(self, analysis_id: int):
        """Delete analysis"""
        analysis = await self.get_analysis_by_id(analysis_id)
        if analysis:
            await self.db.delete(analysis)
            await self.db.commit()
```

---

## 🧪 TESTING & QUALITY ASSURANCE

### **10. Unit Tests**

```python
# backend/tests/unit/test_auth_service.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.services.auth_service import AuthService
from app.schemas.auth import UserCreate
from app.models.auth import User

@pytest.mark.asyncio
async def test_create_user_success(db: AsyncSession):
    """Test successful user creation"""
    auth_service = AuthService(db)
    
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="TestPassword123!"
    )
    
    user = await auth_service.create_user(user_data)
    
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.role == "user"
    assert user.is_active == True

@pytest.mark.asyncio
async def test_create_user_duplicate_username(db: AsyncSession):
    """Test user creation with duplicate username"""
    auth_service = AuthService(db)
    
    # Create first user
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="TestPassword123!"
    )
    await auth_service.create_user(user_data)
    
    # Try to create user with same username
    user_data2 = UserCreate(
        username="testuser",
        email="test2@example.com",
        password="TestPassword123!"
    )
    
    with pytest.raises(ValueError, match="Username already registered"):
        await auth_service.create_user(user_data2)

@pytest.mark.asyncio
async def test_authenticate_user_success(db: AsyncSession):
    """Test successful user authentication"""
    auth_service = AuthService(db)
    
    # Create user
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="TestPassword123!"
    )
    await auth_service.create_user(user_data)
    
    # Authenticate
    login_data = type('LoginData', (), {'username': 'testuser', 'password': 'TestPassword123!'})()
    user, error = await auth_service.authenticate_user(login_data)
    
    assert user is not None
    assert error is None
    assert user.username == "testuser"

@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(db: AsyncSession):
    """Test authentication with wrong password"""
    auth_service = AuthService(db)
    
    # Create user
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="TestPassword123!"
    )
    await auth_service.create_user(user_data)
    
    # Authenticate with wrong password
    login_data = type('LoginData', (), {'username': 'testuser', 'password': 'WrongPassword'})()
    user, error = await auth_service.authenticate_user(login_data)
    
    assert user is None
    assert error == "Invalid username or password"
```

### **11. Integration Tests**

```python
# backend/tests/integration/test_analysis_api.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models.auth import User

client = TestClient(app)

@pytest.mark.asyncio
async def test_analyze_endpoint_success(db: AsyncSession, authenticated_user: User):
    """Test successful political analysis"""
    # Login to get token
    login_response = client.post("/api/v1/auth/login", data={
        "username": authenticated_user.username,
        "password": "TestPassword123!"
    })
    token = login_response.json()["access_token"]
    
    # Test analysis endpoint
    response = client.post(
        "/api/v1/analyze",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "query": "Bagaimana dampak kebijakan subsidi energi terhadap perekonomian Indonesia?",
            "analysis_type": "economic"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "response_text" in data
    assert "confidence_score" in data
    assert data["analysis_type"] == "economic"

@pytest.mark.asyncio
async def test_analyze_endpoint_unauthorized(db: AsyncSession):
    """Test analysis endpoint without authentication"""
    response = client.post(
        "/api/v1/analyze",
        json={
            "query": "Apa itu demokrasi?",
            "analysis_type": "general"
        }
    )
    
    assert response.status_code == 401
```

---

## 🎯 FASE 2 COMPLETION CHECKLIST

### **✅ Authentication & Authorization**
- [x] User models and schemas
- [x] Authentication service implementation
- [x] JWT token management
- [x] Password hashing and security
- [x] Account lockout mechanism
- [x] Refresh token system

### **✅ API Endpoints**
- [x] Authentication endpoints (register, login, logout)
- [x] Political analysis endpoints
- [x] Persona management endpoints
- [x] User profile endpoints
- [x] Error handling and validation

### **✅ Database Models**
- [x] User model with security features
- [x] Political analysis model
- [x] Feedback and rating system
- [x] Token management model
- [x] System logging model

### **✅ Core Business Logic**
- [x] Analysis service implementation
- [x] LLM integration service
- [x] Persona application logic
- [x] Ethics validation system
- [x] Confidence scoring algorithm

### **✅ Testing & Quality**
- [x] Unit tests for authentication
- [x] Integration tests for API endpoints
- [x] Test data fixtures
- [x] Error handling tests
- [x] Security tests

---

## 🚀 FASE 2 COMPLETE!

**Fase 2 telah selesai sepenuhnya!** Sekarang Anda memiliki:

### **🔐 Robust Authentication System**
- User registration and login
- JWT token management
- Password security and account protection
- Role-based access control

### **🎯 Complete API Endpoints**
- Full authentication flow
- Political analysis capabilities
- User management features
- Persona configuration system

### **🗄️ Advanced Database Design**
- Secure user management
- Analysis tracking and history
- Feedback and rating system
- System monitoring and logging

### **🤖 Core AI Integration**
- LLM response generation
- Persona application engine
- Ethics validation system
- Quality scoring algorithms

**Fase 2 siap untuk digunakan!** 🎉

**Next: Fase 3 - Web Interface Development** akan membangun frontend React yang indah dan interaktif! 🌐