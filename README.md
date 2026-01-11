# 🚀 AI TOKOH OPOSISI & INTELEKTUAL KRITIS

> Sistem AI untuk edukasi politik dengan persona **Dr. Arjuna Wibawa** - Tokoh oposisi konstruktif dan intelektual kritis.

**Status**: 🔄 Phase 2 - Active Development (60% Complete)  
**Version**: 2.0.0 (Consolidated Structure)  
**Last Updated**: January 2025

---

## 📋 QUICK INFO

| Aspek | Detail |
|-------|--------|
| **Architecture** | Hybrid: Web App + API + Local LLM |
| **Backend** | FastAPI + Python 3.10+ |
| **Frontend** | React 18 + TypeScript + Vite |
| **AI/ML** | LM Studio + Llama-3/Mistral/Gemma |
| **Database** | PostgreSQL + ChromaDB (Vector) |
| **Datasets** | 15 modules, 300+ pages (2.32 MB) |
| **Location** | `C:\Coding\ai_oposisi_sml` |

---

## 📁 PROJECT STRUCTURE

```
ai_oposisi_sml/
├── 📂 backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/v1/               # REST API endpoints
│   │   ├── core/                 # Configuration & security
│   │   ├── models/               # Database models
│   │   ├── services/             # Business logic
│   │   ├── schemas/              # Pydantic schemas
│   │   ├── utils/                # Utilities
│   │   └── main.py               # Entry point
│   ├── requirements.txt
│   ├── venv/
│   └── README.md
│
├── 📂 frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/           # UI components
│   │   ├── pages/                # Page views
│   │   ├── services/             # API clients
│   │   ├── store/                # Redux state
│   │   └── main.tsx              # Entry point
│   ├── package.json
│   └── README.md
│
├── 📂 data/                       # ⭐ NEW: Knowledge Base
│   ├── datasets/                 # 15 political datasets
│   ├── persona/                  # Dr. Arjuna Wibawa definition
│   ├── docs/                     # Master plans & docs
│   └── README.md
│
├── 📄 Documentation Files/        # Project documentation
│   ├── ARCHITECTURE_PLAN.md
│   ├── PROJECT_STRUCTURE.md
│   ├── QUICK_START.md
│   ├── IMPLEMENTATION_PLAN.md
│   ├── LM_STUDIO_INTEGRATION.md
│   ├── DEPLOYMENT_GUIDE.md
│   └── ...and more
│
├── 📄 docker-compose.yml
├── 📄 .gitignore
└── 📄 README.md                   # This file
```

---

## 🎯 KEY FEATURES

### 1. 💬 Interactive Chat with AI Persona
- Conversational AI dengan persona Dr. Arjuna Wibawa
- Context-aware responses menggunakan RAG
- Multi-turn conversations dengan memory
- Real-time streaming responses

### 2. 📊 Deep Political Analysis
- Analisis situasi politik Indonesia
- Data-driven insights dari 15 datasets
- Historical context integration
- Predictive modeling capabilities

### 3. 🛡️ Democracy Ethics Validation
- Real-time content filtering
- Democracy protocols enforcement
- Anti-violence & anti-hate speech detection
- Transparency & accountability checks

### 4. 🎭 Persona Engine
- Dr. Arjuna Wibawa character consistency
- Analytical & educational communication style
- Values: democracy, justice, transparency, accountability
- Adaptive communication for different audiences

### 5. 📚 Comprehensive Knowledge Base
- **15 datasets** politik Indonesia (2.32 MB)
- **300+ pages** curated content
- **5 clusters**: Foundation, Indonesia Context, Warfare, Communication, Advanced
- Semantic search dengan vector embeddings

### 6. 🔍 RAG (Retrieval-Augmented Generation)
- Vector-based semantic search
- Context-aware information retrieval
- Multi-source knowledge integration
- Hybrid search (keyword + semantic)

---

## 🏗️ ARCHITECTURE

```
┌─────────────────────────────────────────────────────┐
│  USER INTERFACES                                    │
│  Web Dashboard │ API │ (Future: Mobile, CLI)       │
└──────────────┬──────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────┐
│  API GATEWAY & ROUTING (FastAPI)                    │
└──────────────┬──────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────┐
│  CORE SERVICES                                      │
│  ├─ LLM Service (LM Studio)                        │
│  ├─ Persona Service (Dr. Arjuna)                   │
│  ├─ Ethics Service (Democracy protocols)           │
│  ├─ Knowledge Service (Dataset processing)         │
│  └─ Analysis Service (Political insights)          │
└──────────────┬──────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────┐
│  DATA LAYER                                         │
│  ├─ PostgreSQL (Users, analytics, metadata)        │
│  ├─ ChromaDB (Vector embeddings, RAG)              │
│  ├─ Redis (Caching, sessions)                      │
│  └─ Local Storage (data/ directory)                │
└──────────────┬──────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────┐
│  LOCAL LLM (Privacy-First)                          │
│  ├─ LM Studio Server                                │
│  ├─ Base Models: Llama-3, Mistral, Gemma           │
│  ├─ Fine-tuned with political datasets              │
│  └─ Quantized for efficiency (4-bit/8-bit)         │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 QUICK START

### **Prerequisites**

```bash
✅ Python 3.10+
✅ Node.js 16+
✅ 8GB+ RAM
✅ 10GB+ disk space
✅ (Optional) LM Studio for local LLM
```

### **Installation**

**1. Clone & Navigate**
```bash
cd C:\Coding\ai_oposisi_sml
```

**2. Backend Setup**
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate          # Windows
# source venv/bin/activate       # Linux/Mac
pip install -r requirements.txt
```

**3. Frontend Setup**
```bash
cd ../frontend
npm install
```

**4. Environment Configuration**
```bash
# Backend (optional for development)
cd backend
copy .env.example .env
# Edit .env if needed

# Frontend (optional)
cd ../frontend
copy .env.example .env
```

### **Running the Application**

**Terminal 1 - Backend:**
```bash
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### **Access Points**

- 🌐 **Frontend**: http://localhost:3000
- 🔌 **Backend API**: http://localhost:8000
- 📚 **API Documentation**: http://localhost:8000/docs (Swagger UI)
- 📖 **API ReDoc**: http://localhost:8000/redoc
- ❤️ **Health Check**: http://localhost:8000/health

---

## 📊 DATASETS

### **15 Comprehensive Political Datasets**

Located in `data/datasets/` directory:

**🎯 Cluster A: Intellectual Foundation**
1. Political Theory & Academic Frameworks
2. Practical Cases & Operational Techniques
3. Power Psychology & Counter-Intelligence

**🇮🇩 Cluster B: Indonesian Context**
4. Indonesia Deep Dive - Contemporary Politics
5. Political Economy - Soeharto to Now
6. Political Culture & Civil Society

**⚔️ Cluster C: Warfare & Operations**
7. Digital Warfare & Cyber Operations
8. Regional Geopolitics & International Relations
9. Crisis Management & Emergency Response

**🌍 Cluster D: Communication & Law**
10. Media Relations & Public Communication
11. Legal Framework & Constitutional Law

**🛠️ Cluster E: Advanced Capabilities**
12. Organizational Development & Leadership
13. Advanced Research Methods & Intelligence
14. International Relations & Diplomatic Strategy
15. Future Scenarios & Strategic Planning

**📄 See**: `data/README.md` for complete details

---

## 🔧 TECH STACK

### **Backend**
- **Framework**: FastAPI 0.104.1 (Async, high-performance)
- **Database**: PostgreSQL 15+ (Relational) + ChromaDB (Vector)
- **Authentication**: JWT + OAuth2 (python-jose)
- **ORM**: SQLAlchemy 2.0.23 + Alembic (migrations)
- **Testing**: pytest + pytest-asyncio
- **Code Quality**: black, flake8, mypy
- **Logging**: structlog
- **HTTP**: httpx (async client)

### **Frontend**
- **Framework**: React 18.2 + TypeScript 5.2
- **Build Tool**: Vite 5.0 (Fast HMR)
- **UI Library**: Material-UI (@mui/material) 5.14
- **State**: Redux Toolkit 1.9
- **Routing**: React Router DOM 6.18
- **Charts**: Chart.js, Recharts, D3.js
- **Forms**: react-hook-form 7.48
- **Real-time**: Socket.IO Client 4.7

### **AI/ML**
- **LLM Platform**: LM Studio (Local deployment)
- **Base Models**: Llama-3-8B, Mistral-7B, Gemma-7B
- **Fine-tuning**: LoRA (Low-Rank Adaptation)
- **Quantization**: 4-bit/8-bit for efficiency
- **Vector DB**: ChromaDB (Embeddings & RAG)
- **Embeddings**: sentence-transformers

### **DevOps**
- **Containerization**: Docker + Docker Compose
- **Orchestration**: Kubernetes (planned)
- **Monitoring**: Prometheus + Grafana (planned)
- **CI/CD**: GitHub Actions (planned)

---

## 📋 API ENDPOINTS

### **Authentication**
```
POST   /api/v1/auth/register      # User registration
POST   /api/v1/auth/login         # User login
POST   /api/v1/auth/refresh       # Refresh token
GET    /api/v1/auth/me            # Current user
```

### **Chat & Conversation**
```
POST   /api/v1/chat/message       # Send message
GET    /api/v1/chat/conversations # List conversations
POST   /api/v1/chat/stream        # Stream response
```

### **Political Analysis**
```
POST   /api/v1/analysis/analyze   # Analyze query
GET    /api/v1/analysis/history   # Analysis history
```

### **Persona & Ethics**
```
GET    /api/v1/persona/profile    # Get persona
POST   /api/v1/ethics/check       # Validate content
```

### **System**
```
GET    /                          # System info
GET    /health                    # Health check
GET    /docs                      # Swagger UI
```

---

## 📈 DEVELOPMENT ROADMAP

### **✅ Phase 1: Foundation (Week 1-2) - COMPLETE**
- [x] Project structure setup
- [x] Basic FastAPI backend
- [x] React frontend skeleton
- [x] Development environment
- [x] **Data consolidation** (NEW in v2.0)

### **🔄 Phase 2: Core Features (Week 3-4) - 60% COMPLETE**
- [x] Authentication system
- [x] API endpoints structure
- [ ] Dataset processing pipeline
- [ ] Persona engine implementation
- [ ] Ethics validation layer
- [ ] Semantic search & RAG
- [ ] Web interface components

### **📅 Phase 3: Advanced Features (Week 5-6) - PLANNED**
- [ ] RAG optimization
- [ ] Real-time analytics dashboard
- [ ] Mobile responsive design
- [ ] Performance optimization
- [ ] Advanced LLM integration
- [ ] User feedback system

### **📅 Phase 4: Production Ready (Week 7-8) - PLANNED**
- [ ] Security hardening
- [ ] Monitoring & logging
- [ ] Comprehensive testing
- [ ] CI/CD pipeline
- [ ] Production deployment
- [ ] Documentation completion

---

## 🛡️ ETHICS PROTOCOLS

### **Core Principles**

1. **Anti-Violence & Anti-Hate Speech**
   - Zero tolerance for violence advocacy
   - Automated hate speech detection
   - Content moderation system

2. **Pro-Dialogue & Pro-Democracy**
   - Encourage constructive discussion
   - Respect diverse opinions
   - Facilitate democratic discourse

3. **Pro-Transparency & Accountability**
   - Clear information sources
   - Transparent methodology
   - Accountable decision-making

4. **Solution-Focused & Reconciliation**
   - Problem-solving orientation
   - Bridge-building approach
   - Long-term sustainability focus

### **Usage Guidelines**

✅ **ALLOWED:**
- Political education & research
- Academic simulation & study
- Policy analysis & recommendations
- Training & capacity building

❌ **PROHIBITED:**
- Real political campaigns
- Public opinion manipulation
- Propaganda & disinformation
- Electoral interference

---

## 🔍 TROUBLESHOOTING

### **Common Issues**

**Backend won't start:**
```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check logs
tail -f logs/app.log
```

**Frontend errors:**
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version  # Should be 16+
```

**Dataset not loading:**
```bash
# Verify data directory
ls data/datasets/  # Should show 15 .md files

# Check permissions
chmod -R 755 data/
```

**LLM connection failed:**
```bash
# Ensure LM Studio is running
# Check http://localhost:1234

# Update config
# Edit backend/.env: LM_STUDIO_URL=http://localhost:1234
```

**📄 See**: `TROUBLESHOOTING.md` for detailed solutions

---

## 📚 DOCUMENTATION

### **For Developers**
- `ARCHITECTURE_PLAN.md` - System architecture
- `PROJECT_STRUCTURE.md` - Complete structure
- `IMPLEMENTATION_PLAN.md` - Development roadmap
- `LM_STUDIO_INTEGRATION.md` - LLM setup guide

### **For Users**
- `QUICK_START.md` - Getting started (5 minutes)
- `WEB_INTERFACE_PLAN.md` - UI/UX guide
- `/docs` endpoint - Interactive API documentation

### **For Deployment**
- `DEPLOYMENT_GUIDE.md` - Production deployment
- `LOCAL_DEPLOYMENT_GUIDE.md` - Local setup
- `docker-compose.yml` - Docker configuration

### **Data & Content**
- `data/README.md` - Dataset documentation
- `data/persona/persona_utama.md` - Persona definition
- `data/docs/` - Master plans & documentation

---

## 🎯 PROJECT METRICS

| Metric | Value |
|--------|-------|
| **Overall Progress** | ~40% |
| **Datasets** | 15 modules (2.32 MB) |
| **Code Files** | 12,500+ files |
| **API Endpoints** | 20+ endpoints |
| **Documentation** | 20+ MD files |
| **Code Lines** | ~10,000+ lines |
| **Test Coverage** | TBD |

---

## 🔮 FUTURE ENHANCEMENTS

### **Short-term (3 months)**
- Complete Phase 3 & 4 implementation
- Mobile app (React Native)
- Advanced analytics dashboard
- Multi-language support (English)

### **Medium-term (6 months)**
- Kubernetes deployment
- Multi-model LLM support
- Graph database for advanced RAG
- Collaborative features

### **Long-term (1 year+)**
- Federated learning for privacy
- Blockchain for transparency
- AR/VR political simulation
- Global expansion

---

## 👥 TEAM

**Development Team:**
- Backend Developer (Python/FastAPI)
- Frontend Developer (React/TypeScript)
- ML Engineer (LLM integration)
- DevOps Engineer (Deployment)

**Subject Matter Experts:**
- Political Analyst (Dataset curation)
- Ethics Advisor (Democracy protocols)
- UX/UI Designer (User experience)

---

## 📞 SUPPORT

### **Getting Help**
- 📖 Check documentation in project root
- 🐛 Report issues (when repo is public)
- 💬 Discussion forum (planned)
- 📧 Contact maintainers

### **Contributing**
- Follow coding standards
- Write tests for new features
- Update documentation
- Submit pull requests

---

## 📄 LICENSE

**Educational and Research Use Only**

This project is intended for educational and research purposes only.  
Any use for real political activities, campaigns, or public opinion manipulation is strictly prohibited.

---

## 🙏 ACKNOWLEDGMENTS

- FastAPI community for excellent framework
- React & TypeScript community
- LM Studio for local LLM deployment
- Material-UI for beautiful components
- Open source contributors worldwide

---

## 🔗 QUICK COMMANDS

```bash
# Start development
cd backend && uvicorn app.main:app --reload
cd frontend && npm run dev

# Run tests
cd backend && pytest
cd frontend && npm test

# Build for production
cd backend && docker build -t ai-oposisi-backend .
cd frontend && npm run build

# View logs
cd backend && tail -f logs/app.log

# Check health
curl http://localhost:8000/health
```

---

**Version**: 2.0.0 (Consolidated Structure)  
**Last Updated**: January 2025  
**Status**: Active Development  
**Location**: `C:\Coding\ai_oposisi_sml`

---

**Made with ❤️ for Indonesian Democracy Education** 🇮🇩

---

**End of README** 🎉
