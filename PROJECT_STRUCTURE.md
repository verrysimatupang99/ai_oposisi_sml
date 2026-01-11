# 📁 PROJECT STRUCTURE: AI TOKOH OPPOSISI & INTELEKTUAL KRITIS

## 🏗️ COMPLETE PROJECT ARCHITECTURE

### **📁 ROOT DIRECTORY STRUCTURE**

```
ai_oposisi_sml/
├── 📁 backend/                    # FastAPI Backend Application
│   ├── 📁 app/                   # Main application package
│   │   ├── 📁 api/              # API endpoints
│   │   │   ├── 📁 v1/           # API version 1
│   │   │   │   ├── auth.py      # Authentication endpoints
│   │   │   │   ├── analysis.py  # Political analysis endpoints
│   │   │   │   ├── chat.py      # Chat endpoints
│   │   │   │   ├── persona.py   # Persona endpoints
│   │   │   │   └── ethics.py    # Ethics validation endpoints
│   │   │   └── v2/              # Future API version
│   │   ├── 📁 core/             # Core configuration
│   │   │   ├── config.py        # Application configuration
│   │   │   ├── security.py      # Security utilities
│   │   │   └── database.py      # Database configuration
│   │   ├── 📁 models/           # Database models
│   │   │   ├── user.py          # User model
│   │   │   ├── analysis.py      # Analysis model
│   │   │   ├── chat.py          # Chat model
│   │   │   ├── persona.py       # Persona model
│   │   │   └── ethics.py        # Ethics model
│   │   ├── 📁 services/         # Business logic
│   │   │   ├── auth_service.py  # Authentication service
│   │   │   ├── analysis_service.py  # Analysis service
│   │   │   ├── chat_service.py  # Chat service
│   │   │   ├── persona_service.py   # Persona service
│   │   │   └── ethics_service.py    # Ethics service
│   │   ├── 📁 dependencies/     # Dependency injection
│   │   │   ├── database.py      # Database dependency
│   │   │   └── auth.py          # Authentication dependency
│   │   ├── 📁 utils/            # Utility functions
│   │   │   ├── logger.py        # Logging utilities
│   │   │   ├── validators.py    # Input validation
│   │   │   └── helpers.py       # Helper functions
│   │   └── main.py              # FastAPI application entry point
│   ├── 📁 llm/                  # LLM Integration
│   │   ├── 📁 clients/          # LLM clients
│   │   │   ├── lm_studio.py     # LM Studio client
│   │   │   └── openai.py        # OpenAI client (optional)
│   │   ├── 📁 models/           # Model configurations
│   │   │   ├── model_config.py  # Model settings
│   │   │   └── prompt_templates.py  # Prompt templates
│   │   └── 📁 processors/       # Data processors
│   │       ├── text_processor.py    # Text processing
│   │       └── response_generator.py  # Response generation
│   ├── 📁 ai/                   # AI Components
│   │   ├── 📁 persona/          # Persona Engine
│   │   │   ├── engine.py        # Persona engine
│   │   │   ├── dr_arjuna.py     # Dr. Arjuna Wibawa persona
│   │   │   └── templates.py     # Persona templates
│   │   ├── 📁 ethics/           # Ethics Engine
│   │   │   ├── validator.py     # Ethics validation
│   │   │   ├── democracy_protocols.py  # Democracy protocols
│   │   │   └── content_filter.py  # Content filtering
│   │   └── 📁 knowledge/        # Knowledge Base
│   │       ├── dataset_processor.py  # Dataset processing
│   │       ├── knowledge_base.py     # Knowledge management
│   │       └── context_manager.py    # Context management
│   ├── 📁 tests/                # Backend tests
│   │   ├── 📁 api/              # API tests
│   │   ├── 📁 services/         # Service tests
│   │   └── 📁 integration/      # Integration tests
│   ├── 📁 migrations/           # Database migrations
│   ├── 📁 static/               # Static files
│   ├── 📁 templates/            # HTML templates
│   ├── 📄 requirements.txt      # Python dependencies
│   ├── 📄 Dockerfile            # Docker configuration
│   └── 📄 README.md             # Backend documentation
│
├── 📁 frontend/                 # React Frontend Application
│   ├── 📁 public/               # Public assets
│   │   ├── 📄 index.html        # Main HTML file
│   │   ├── 📄 favicon.ico       # Favicon
│   │   └── 📁 assets/           # Static assets
│   ├── 📁 src/                  # Source code
│   │   ├── 📁 components/       # React components
│   │   │   ├── 📁 common/       # Common components
│   │   │   │   ├── Button.jsx   # Custom button
│   │   │   │   ├── Input.jsx    # Custom input
│   │   │   │   ├── Modal.jsx    # Modal component
│   │   │   │   └── Loading.jsx  # Loading component
│   │   │   ├── 📁 layout/       # Layout components
│   │   │   │   ├── Header.jsx   # Header component
│   │   │   │   ├── Sidebar.jsx  # Sidebar component
│   │   │   │   └── Footer.jsx   # Footer component
│   │   │   ├── 📁 dashboard/    # Dashboard components
│   │   │   │   ├── Dashboard.jsx  # Main dashboard
│   │   │   │   ├── Overview.jsx   # Overview component
│   │   │   │   └── Stats.jsx      # Statistics component
│   │   │   ├── 📁 chat/         # Chat components
│   │   │   │   ├── ChatInterface.jsx  # Main chat interface
│   │   │   │   ├── Message.jsx      # Message component
│   │   │   │   ├── InputArea.jsx    # Input area
│   │   │   │   └── ConversationHistory.jsx  # History component
│   │   │   ├── 📁 analysis/     # Analysis components
│   │   │   │   ├── AnalysisPanel.jsx  # Analysis panel
│   │   │   │   ├── PoliticalAnalysis.jsx  # Political analysis
│   │   │   │   └── DataVisualization.jsx  # Data visualization
│   │   │   ├── 📁 persona/      # Persona components
│   │   │   │   ├── PersonaProfile.jsx  # Persona profile
│   │   │   │   ├── PersonaChat.jsx     # Persona chat
│   │   │   │   └── PersonaSettings.jsx # Persona settings
│   │   │   └── 📁 ethics/       # Ethics components
│   │   │       ├── EthicsValidator.jsx  # Ethics validation
│   │   │       └── ContentFilter.jsx    # Content filtering
│   │   ├── 📁 pages/            # Page components
│   │   │   ├── Home.jsx         # Home page
│   │   │   ├── Dashboard.jsx    # Dashboard page
│   │   │   ├── Chat.jsx         # Chat page
│   │   │   ├── Analysis.jsx     # Analysis page
│   │   │   ├── Persona.jsx      # Persona page
│   │   │   ├── Ethics.jsx       # Ethics page
│   │   │   ├── Login.jsx        # Login page
│   │   │   └── Register.jsx     # Register page
│   │   ├── 📁 services/         # API services
│   │   │   ├── api.js           # API client
│   │   │   ├── auth.js          # Authentication service
│   │   │   ├── analysis.js      # Analysis service
│   │   │   ├── chat.js          # Chat service
│   │   │   ├── persona.js       # Persona service
│   │   │   └── ethics.js        # Ethics service
│   │   ├── 📁 store/            # State management
│   │   │   ├── 📁 slices/       # Redux slices
│   │   │   │   ├── authSlice.js     # Authentication state
│   │   │   │   ├── chatSlice.js     # Chat state
│   │   │   │   ├── analysisSlice.js # Analysis state
│   │   │   │   ├── personaSlice.js  # Persona state
│   │   │   │   └── ethicsSlice.js   # Ethics state
│   │   │   ├── 📁 middleware/   # Custom middleware
│   │   │   └── store.js         # Store configuration
│   │   ├── 📁 hooks/            # Custom hooks
│   │   │   ├── useAuth.js       # Authentication hook
│   │   │   ├── useChat.js       # Chat hook
│   │   │   ├── useAnalysis.js   # Analysis hook
│   │   │   └── usePersona.js    # Persona hook
│   │   ├── 📁 utils/            # Utility functions
│   │   │   ├── helpers.js       # Helper functions
│   │   │   ├── formatters.js    # Data formatters
│   │   │   └── validators.js    # Form validators
│   │   ├── 📁 styles/           # Styling
│   │   │   ├── 📁 components/   # Component styles
│   │   │   ├── 📁 pages/        # Page styles
│   │   │   ├── 📁 themes/       # Theme configurations
│   │   │   └── 📁 globals.css   # Global styles
│   │   ├── 📁 config/           # Configuration
│   │   │   ├── routes.js        # Route configuration
│   │   │   ├── theme.js         # Theme configuration
│   │   │   └── constants.js     # Application constants
│   │   ├── 📁 tests/            # Frontend tests
│   │   │   ├── 📁 components/   # Component tests
│   │   │   ├── 📁 pages/        # Page tests
│   │   │   └── 📁 utils/        # Utility tests
│   │   ├── App.jsx              # Main App component
│   │   ├── index.js             # Entry point
│   │   └── reportWebVitals.js   # Performance monitoring
│   ├── 📄 package.json          # Node.js dependencies
│   ├── 📄 Dockerfile            # Docker configuration
│   ├── 📄 .env.example          # Environment variables template
│   └── 📄 README.md             # Frontend documentation
│
├── 📁 data_processing/          # Dataset Processing Pipeline
│   ├── 📁 processors/           # Data processors
│   │   ├── dataset_processor.py     # Main dataset processor
│   │   ├── text_cleaner.py          # Text cleaning utilities
│   │   ├── format_converter.py      # Format conversion
│   │   └── quality_checker.py       # Data quality validation
│   ├── 📁 pipelines/            # Processing pipelines
│   │   ├── political_analysis.py    # Political analysis pipeline
│   │   ├── persona_training.py      # Persona training pipeline
│   │   └── ethics_validation.py     # Ethics validation pipeline
│   ├── 📁 utils/                # Utilities
│   │   ├── file_handler.py          # File handling utilities
│   │   ├── progress_tracker.py      # Progress tracking
│   │   └── error_handler.py         # Error handling
│   ├── 📄 process_all_datasets.py   # Main processing script
│   └── 📄 README.md                 # Data processing documentation
│
├── 📁 deployment/               # Deployment Configuration
│   ├── 📁 docker/               # Docker configurations
│   │   ├── 📁 compose/          # Docker Compose files
│   │   │   ├── docker-compose.yml   # Development compose
│   │   │   ├── docker-compose.prod.yml  # Production compose
│   │   │   └── docker-compose.override.yml  # Override compose
│   │   ├── 📁 images/           # Custom Docker images
│   │   │   ├── backend.Dockerfile   # Backend image
│   │   │   └── frontend.Dockerfile  # Frontend image
│   │   └── 📁 scripts/          # Docker scripts
│   │       ├── build.sh         # Build script
│   │       └── deploy.sh        # Deploy script
│   ├── 📁 kubernetes/           # Kubernetes configurations
│   │   ├── 📁 manifests/        # Kubernetes manifests
│   │   │   ├── deployment.yaml  # Application deployment
│   │   │   ├── service.yaml     # Service configuration
│   │   │   ├── ingress.yaml     # Ingress configuration
│   │   │   └── configmap.yaml   # Configuration map
│   │   └── 📁 scripts/          # Kubernetes scripts
│   │       ├── apply.sh         # Apply configurations
│   │       └── delete.sh        # Delete configurations
│   ├── 📁 cloud/                # Cloud deployment
│   │   ├── 📁 aws/              # AWS configurations
│   │   │   ├── 📄 cloudformation.yaml  # CloudFormation template
│   │   │   └── 📄 terraform/    # Terraform configurations
│   │   ├── 📁 gcp/              # Google Cloud configurations
│   │   │   ├── 📄 deployment.yaml  # Deployment configuration
│   │   │   └── 📄 terraform/    # Terraform configurations
│   │   └── 📁 azure/            # Azure configurations
│   │       ├── 📄 arm-template.json  # ARM template
│   │       └── 📄 terraform/    # Terraform configurations
│   ├── 📁 scripts/              # Deployment scripts
│   │   ├── 📄 deploy-local.sh   # Local deployment
│   │   ├── 📄 deploy-staging.sh # Staging deployment
│   │   ├── 📄 deploy-production.sh  # Production deployment
│   │   └── 📄 rollback.sh       # Rollback script
│   └── 📄 README.md             # Deployment documentation
│
├── 📁 docs/                     # Documentation
│   ├── 📁 api/                  # API documentation
│   │   ├── 📄 openapi.yaml      # OpenAPI specification
│   │   ├── 📄 endpoints.md      # Endpoint documentation
│   │   └── 📄 examples.md       # API examples
│   ├── 📁 user/                 # User documentation
│   │   ├── 📄 user_guide.md     # User guide
│   │   ├── 📄 faq.md            # Frequently asked questions
│   │   └── 📄 troubleshooting.md  # Troubleshooting guide
│   ├── 📁 developer/            # Developer documentation
│   │   ├── 📄 setup.md          # Development setup
│   │   ├── 📄 coding_standards.md  # Coding standards
│   │   ├── 📄 testing.md        # Testing guidelines
│   │   └── 📄 deployment.md     # Deployment guide
│   ├── 📁 architecture/         # Architecture documentation
│   │   ├── 📄 system_architecture.md  # System architecture
│   │   ├── 📄 data_flow.md      # Data flow diagrams
│   │   └── 📄 component_design.md  # Component design
│   └── 📄 README.md             # Documentation overview
│
├── 📁 tests/                    # Integration tests
│   ├── 📁 e2e/                  # End-to-end tests
│   │   ├── 📁 scenarios/        # Test scenarios
│   │   │   ├── auth.scenario.js     # Authentication scenarios
│   │   │   ├── chat.scenario.js     # Chat scenarios
│   │   │   ├── analysis.scenario.js # Analysis scenarios
│   │   │   └── persona.scenario.js  # Persona scenarios
│   │   └── 📁 utils/            # Test utilities
│   ├── 📁 performance/          # Performance tests
│   │   ├── 📁 load/             # Load testing
│   │   ├── 📁 stress/           # Stress testing
│   │   └── 📁 benchmark/        # Benchmarking
│   └── 📁 security/             # Security tests
│       ├── 📁 auth/             # Authentication tests
│       ├── 📁 data/             # Data protection tests
│       └── 📁 network/          # Network security tests
│
├── 📁 monitoring/               # Monitoring & Observability
│   ├── 📁 logs/                 # Log management
│   │   ├── 📄 log_config.py     # Log configuration
│   │   └── 📄 log_analyzer.py   # Log analysis utilities
│   ├── 📁 metrics/              # Metrics collection
│   │   ├── 📄 metrics_collector.py  # Metrics collection
│   │   ├── 📄 performance_metrics.py  # Performance metrics
│   │   └── 📄 business_metrics.py   # Business metrics
│   ├── 📁 alerts/               # Alerting system
│   │   ├── 📄 alert_rules.yaml  # Alert rules configuration
│   │   └── 📄 alert_handlers.py # Alert handling
│   └── 📄 monitoring_config.py  # Monitoring configuration
│
├── 📁 scripts/                  # Utility scripts
│   ├── 📄 setup.sh              # Project setup script
│   ├── 📄 build.sh              # Build script
│   ├── 📄 test.sh               # Test script
│   ├── 📄 deploy.sh             # Deployment script
│   ├── 📄 backup.sh             # Backup script
│   └── 📄 cleanup.sh            # Cleanup script
│
├── 📄 .gitignore                # Git ignore file
├── 📄 .env.example              # Environment variables template
├── 📄 docker-compose.yml        # Docker Compose configuration
├── 📄 README.md                 # Project README
└── 📄 LICENSE                   # Project license
```

---

## 🎯 KEY COMPONENTS EXPLANATION

### **Backend (FastAPI)**
- **API Endpoints**: RESTful APIs for all functionality
- **Services**: Business logic separation
- **Models**: Database ORM models
- **LLM Integration**: Local LLM with LM Studio
- **AI Components**: Persona and ethics engines

### **Frontend (React)**
- **Components**: Modular, reusable components
- **State Management**: Redux for global state
- **API Integration**: Axios for backend communication
- **Styling**: Material-UI with custom themes
- **Responsive Design**: Mobile-first approach

### **Data Processing**
- **Dataset Processing**: Convert 15 datasets to training format
- **Quality Validation**: Ensure data quality
- **Pipeline Management**: Automated processing workflows

### **Deployment**
- **Docker**: Containerized deployment
- **Kubernetes**: Orchestration for scaling
- **Cloud**: Multi-cloud deployment support
- **CI/CD**: Automated testing and deployment

### **Monitoring**
- **Logging**: Centralized logging system
- **Metrics**: Performance and business metrics
- **Alerts**: Proactive monitoring and alerting

---

## 🚀 GETTING STARTED

### **Prerequisites**
- Python 3.10+
- Node.js 16+
- Docker
- LM Studio (for local LLM)

### **Quick Start**
```bash
# 1. Clone and setup
git clone <repository-url>
cd ai_oposisi_sml

# 2. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# 3. Frontend setup
cd ../frontend
npm install

# 4. Environment setup
cp .env.example .env
# Edit .env with your configuration

# 5. Run development servers
# Backend
uvicorn app.main:app --reload

# Frontend
npm start

# 6. Access applications
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

---

## 📊 TECHNOLOGY STACK

### **Backend**
- **Framework**: FastAPI
- **Database**: PostgreSQL + Redis
- **Authentication**: JWT + OAuth2
- **AI Integration**: LM Studio API
- **Testing**: pytest
- **ORM**: SQLAlchemy

### **Frontend**
- **Framework**: React.js
- **State Management**: Redux Toolkit
- **Styling**: Material-UI + Custom CSS
- **Charts**: Chart.js + D3.js
- **Testing**: Jest + React Testing Library

### **Infrastructure**
- **Container**: Docker
- **Orchestration**: Docker Compose + Kubernetes
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack
- **Security**: HTTPS, CORS, Rate limiting

---

## 🎯 NEXT STEPS

**Ready to implement this structure?** 

1. **Approve this project structure**
2. **Start with Phase 1**: Create directory structure and basic files
3. **Implement backend**: FastAPI application with core services
4. **Build frontend**: React application with all components
5. **Integrate AI**: LM Studio and persona engines
6. **Test & Deploy**: Comprehensive testing and deployment

**[Let's start building! 🚀](#)**