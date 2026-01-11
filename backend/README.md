# 🤖 AI Tokoh Oposisi & Intelektual Kritis - Backend

Backend service for the AI Tokoh Oposisi & Intelektual Kritis system, built with FastAPI.

## 🚀 Features

- **Authentication & Authorization**: JWT-based authentication with role-based access
- **LLM Integration**: Local LLM integration with LM Studio
- **Persona Engine**: Dr. Arjuna Wibawa persona management
- **Ethics Validation**: Strict content filtering and democracy protocols
- **Political Analysis**: Advanced political content analysis
- **Chat System**: Real-time chat with AI persona
- **Database**: PostgreSQL with SQLAlchemy ORM
- **API Documentation**: Auto-generated OpenAPI documentation

## 📋 Requirements

- Python 3.10+
- PostgreSQL
- Redis (optional, for caching)
- LM Studio (for local LLM)

## 🛠️ Installation

### 1. Clone and Setup

```bash
cd ai_oposisi_sml/backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Database Setup

```bash
# Run database migrations
alembic upgrade head
```

## 🔧 Configuration

### Environment Variables

```bash
# Application
APP_NAME="AI Tokoh Oposisi & Intelektual Kritis"
DEBUG=false
HOST="0.0.0.0"
PORT=8000

# Security
SECRET_KEY="your-secret-key-change-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL="postgresql://user:password@localhost:5432/ai_oposisi"
REDIS_URL="redis://localhost:6379/0"

# LLM Configuration
LM_STUDIO_URL="http://localhost:1234"
LM_STUDIO_MODEL="llama-2-7b-chat"
LM_STUDIO_TIMEOUT=60
LM_STUDIO_MAX_TOKENS=4000
LM_STUDIO_TEMPERATURE=0.7

# CORS
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:3001"]
ALLOWED_HOSTS=["localhost", "0.0.0.0", "127.0.0.1"]

# Ethics Configuration
ETHICS_ENABLED=true
ETHICS_STRICT_MODE=true
CONTENT_FILTER_ENABLED=true

# Persona Configuration
PERSONA_NAME="Dr. Arjuna Wibawa"
PERSONA_DESCRIPTION="Intelektual kritis dan tokoh oposisi virtual"
PERSONA_COMMUNICATION_STYLE="formal"
```

## 🚀 Running the Application

### Development

```bash
# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
# Run with gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📚 API Documentation

After starting the server, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/api/openapi.json

## 🔐 Authentication

### Register User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user123",
    "email": "user@example.com",
    "full_name": "User Name",
    "password": "SecurePass123!"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user123&password=SecurePass123!"
```

### Use Token

```bash
curl -X GET "http://localhost:8000/api/v1/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🤖 LLM Integration

### LM Studio Setup

1. Download and install [LM Studio](https://lmstudio.ai/)
2. Load your preferred model (e.g., Llama 2, Falcon)
3. Enable "Local Server" in LM Studio settings
4. Configure the model URL in `.env`

### Test LLM Connection

```bash
curl -X GET "http://localhost:8000/health"
```

## 🎭 Persona System

### Get Available Personas

```bash
curl -X GET "http://localhost:8000/api/v1/persona/list" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Generate Persona Response

```bash
curl -X POST "http://localhost:8000/api/v1/persona/response" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "persona_id": "dr_arjuna",
    "user_input": "Apa pendapat Anda tentang demokrasi di Indonesia?",
    "temperature": 0.7
  }'
```

## 🛡️ Ethics Validation

### Validate Content

```bash
curl -X POST "http://localhost:8000/api/v1/ethics/validate" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Pernyataan politik yang perlu divalidasi",
    "content_type": "text"
  }'
```

## 📊 Political Analysis

### Analyze Content

```bash
curl -X POST "http://localhost:8000/api/v1/analysis/political" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Analisis politik tentang kebijakan pemerintah",
    "analysis_type": "policy"
  }'
```

## 💬 Chat System

### Start Chat Session

```bash
curl -X POST "http://localhost:8000/api/v1/chat/session" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "session_name": "Political Discussion"
  }'
```

### Send Message

```bash
curl -X POST "http://localhost:8000/api/v1/chat/message" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session-uuid",
    "message": "Apa pendapat Anda tentang sistem pemilu di Indonesia?"
  }'
```

## 🗄️ Database

### Models

- **User**: User authentication and profile
- **ChatSession**: Chat session management
- **ChatMessage**: Conversation messages
- **PoliticalAnalysis**: Analysis results
- **Persona**: Persona configurations
- **EthicsValidation**: Validation results
- **SystemLog**: System events

### Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🔍 Monitoring

### Health Check

```bash
curl -X GET "http://localhost:8000/health"
```

### Logs

```bash
# View application logs
tail -f logs/app.log

# View error logs
tail -f logs/error.log

# View security logs
tail -f logs/security.log
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_auth.py
```

### Test Endpoints

```bash
# Test authentication
pytest tests/test_auth.py -v

# Test chat system
pytest tests/test_chat.py -v

# Test persona system
pytest tests/test_persona.py -v

# Test ethics validation
pytest tests/test_ethics.py -v
```

## 🐳 Docker

### Build Image

```bash
docker build -t ai-oposisi-backend .
```

### Run Container

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://..." \
  -e LM_STUDIO_URL="http://host.docker.internal:1234" \
  ai-oposisi-backend
```

### Docker Compose

```bash
docker-compose up -d
```

## 🔒 Security

### Best Practices

1. **Environment Variables**: Never commit `.env` files
2. **Secret Keys**: Use strong, unique secret keys in production
3. **HTTPS**: Always use HTTPS in production
4. **Rate Limiting**: Implement rate limiting for API endpoints
5. **Input Validation**: Validate all user inputs
6. **Error Handling**: Don't expose sensitive information in error messages

### Security Headers

The application includes security middleware:
- CORS configuration
- Trusted host validation
- Content security policies

## 📈 Performance

### Optimization Tips

1. **Database**: Use connection pooling
2. **Caching**: Implement Redis caching for frequently accessed data
3. **LLM**: Optimize model parameters and batch requests
4. **Async**: Use async endpoints for I/O operations
5. **Monitoring**: Monitor response times and resource usage

### Load Testing

```bash
# Install load testing tool
pip install locust

# Run load test
locust -f tests/load_test.py
```

## 🚨 Error Handling

### Common Errors

- **401 Unauthorized**: Invalid or missing authentication token
- **403 Forbidden**: Insufficient permissions
- **422 Unprocessable Entity**: Invalid request data
- **500 Internal Server Error**: Server-side error

### Debug Mode

```bash
# Enable debug mode
DEBUG=true
```

## 📞 Support

For support and questions:

1. Check the [API Documentation](http://localhost:8000/docs)
2. Review the [Error Logs](logs/error.log)
3. Check [GitHub Issues](https://github.com/your-repo/issues)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Run the test suite
6. Submit a pull request

## 📊 Metrics

### Key Performance Indicators

- **Response Time**: < 2 seconds for API calls
- **LLM Response Time**: < 5 seconds for AI responses
- **Uptime**: > 99% availability
- **Error Rate**: < 1% error rate
- **Security**: Zero security vulnerabilities

### Monitoring Dashboard

Access the monitoring dashboard at:
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000

---

**⚠️ PERINGATAN ETIKA**: Sistem ini **hanya untuk tujuan edukasi dan simulasi**. Dilarang digunakan untuk aktivitas politik nyata, memengaruhi opini publik, atau kampanye propaganda.