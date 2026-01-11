# 🚀 DEPLOYMENT GUIDE: AI TOKOH OPPOSISI & INTELEKTUAL KRITIS

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Monitoring & Logging](#monitoring--logging)
7. [Security Considerations](#security-considerations)
8. [Troubleshooting](#troubleshooting)

---

## 🛠️ Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, or Windows
- **Docker**: Version 20.10+
- **Docker Compose**: Version 2.0+
- **Node.js**: Version 16+ (for frontend development)
- **Python**: Version 3.10+ (for backend development)
- **LM Studio**: For local LLM integration

### External Dependencies
- **PostgreSQL**: Database server
- **Redis**: Cache server
- **LM Studio**: Local LLM server (optional for production)

---

## 🏗️ Local Development Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd ai_oposisi_sml
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Environment setup
cp .env.example .env
# Edit .env with your configuration

# Database setup
alembic upgrade head

# Run backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install

# Environment setup
cp .env.example .env
# Edit .env with your configuration

# Run frontend
npm start
```

### 4. LM Studio Setup
1. Download and install [LM Studio](https://lmstudio.ai/)
2. Load your preferred model (e.g., Llama 2, Falcon)
3. Enable "Local Server" in LM Studio settings
4. Configure model URL in `.env` files

### 5. Access Applications
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **LM Studio**: http://localhost:1234

---

## 🐳 Docker Deployment

### 1. Quick Start
```bash
# Clone repository
git clone <repository-url>
cd ai_oposisi_sml

# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 2. Service Management
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View service status
docker-compose ps

# View logs for specific service
docker-compose logs backend
docker-compose logs frontend
```

### 3. Database Management
```bash
# Access PostgreSQL
docker-compose exec postgres psql -U ai_user -d ai_oposisi

# Access Redis
docker-compose exec redis redis-cli

# Backup database
docker-compose exec postgres pg_dump -U ai_user ai_oposisi > backup.sql

# Restore database
docker-compose exec -T postgres psql -U ai_user -d ai_oposisi < backup.sql
```

### 4. Application Logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f backend
```

---

## 🚀 Production Deployment

### 1. Environment Preparation
```bash
# Create production environment file
cp .env.example .env.production

# Configure production settings
# - Set DEBUG=false
# - Use strong SECRET_KEY
# - Configure production database
# - Set up SSL certificates
```

### 2. Production Docker Compose
```bash
# Use production compose file
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Or modify docker-compose.yml for production:
# - Remove volume mounts for code
# - Use production images
# - Configure SSL
# - Set up monitoring
```

### 3. Nginx Configuration
```bash
# Create nginx configuration
mkdir -p nginx/ssl
cp nginx/nginx.conf.example nginx/nginx.conf

# Configure SSL certificates
# - Obtain SSL certificate from Let's Encrypt or other CA
# - Place certificates in nginx/ssl/
# - Update nginx.conf with certificate paths
```

### 4. Database Production Setup
```bash
# Use external PostgreSQL server
# Update DATABASE_URL in environment variables
# Configure database backups
# Set up database monitoring
```

### 5. Monitoring Setup
```bash
# Start monitoring services
docker-compose up -d prometheus grafana

# Access monitoring dashboards
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3001
# - Default Grafana credentials: admin/admin123
```

---

## ⚙️ Environment Configuration

### Backend Environment Variables
```bash
# Application
APP_NAME="AI Tokoh Oposisi & Intelektual Kritis"
DEBUG=false
HOST=0.0.0.0
PORT=8000

# Security
SECRET_KEY=your-production-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL=postgresql://user:password@postgres:5432/ai_oposisi
REDIS_URL=redis://redis:6379/0

# LLM Configuration
LM_STUDIO_URL=http://host.docker.internal:1234
LM_STUDIO_MODEL=llama-2-7b-chat
LM_STUDIO_TIMEOUT=60
LM_STUDIO_MAX_TOKENS=4000
LM_STUDIO_TEMPERATURE=0.7

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://your-domain.com
ALLOWED_HOSTS=localhost,your-domain.com

# Ethics Configuration
ETHICS_ENABLED=true
ETHICS_STRICT_MODE=true
CONTENT_FILTER_ENABLED=true

# Logging
LOG_LEVEL=INFO
```

### Frontend Environment Variables
```bash
# API Configuration
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_WS_URL=ws://localhost:8000/ws

# Application
REACT_APP_NAME="AI Tokoh Oposisi & Intelektual Kritis"
REACT_APP_VERSION=1.0.0

# Features
REACT_APP_ENABLE_ANALYTICS=false
REACT_APP_ENABLE_NOTIFICATIONS=true
REACT_APP_ENABLE_PWA=true
```

---

## 📊 Monitoring & Logging

### 1. Application Monitoring
```bash
# Health checks
curl http://localhost:8000/health
curl http://localhost:3000

# Metrics endpoint (if implemented)
curl http://localhost:8000/metrics
```

### 2. Log Management
```bash
# View application logs
docker-compose logs backend
docker-compose logs frontend

# Log rotation setup
# Configure logrotate for production logs
sudo cp monitoring/logrotate.d/ai-oposisi /etc/logrotate.d/
```

### 3. Performance Monitoring
```bash
# Prometheus metrics
# Access: http://localhost:9090

# Grafana dashboards
# Access: http://localhost:3001
# Import dashboard configurations from monitoring/grafana/
```

### 4. Database Monitoring
```bash
# PostgreSQL monitoring
docker-compose exec postgres psql -U ai_user -d ai_oposisi -c "SELECT * FROM pg_stat_activity;"

# Redis monitoring
docker-compose exec redis redis-cli info
```

---

## 🔒 Security Considerations

### 1. SSL/TLS Configuration
```bash
# Generate SSL certificates
sudo apt install certbot
sudo certbot certonly --standalone -d your-domain.com

# Configure Nginx with SSL
# Update nginx/nginx.conf with SSL certificate paths
```

### 2. Firewall Configuration
```bash
# Ubuntu/Debian
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=22/tcp
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --reload
```

### 3. Security Headers
```bash
# Configure security headers in Nginx
# Add to nginx.conf:
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
```

### 4. Database Security
```bash
# Use strong passwords
# Enable SSL for database connections
# Configure database user permissions
# Regular security updates
```

### 5. Application Security
```bash
# Use environment variables for secrets
# Enable CORS restrictions
# Implement rate limiting
# Regular security audits
# Keep dependencies updated
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Database Connection Errors
```bash
# Check database status
docker-compose ps postgres

# Check database logs
docker-compose logs postgres

# Test database connection
docker-compose exec postgres pg_isready -U ai_user -d ai_oposisi
```

#### 2. LLM Connection Errors
```bash
# Check LM Studio is running
curl http://localhost:1234/v1/models

# Verify model is loaded
# Check LM Studio interface

# Test LLM connection
curl -X POST http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "llama-2-7b-chat", "messages": [{"role": "user", "content": "Hello"}]}'
```

#### 3. Frontend Build Errors
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check environment variables
cat .env

# Build frontend
npm run build
```

#### 4. Docker Issues
```bash
# Check Docker status
sudo systemctl status docker

# Check Docker Compose version
docker-compose --version

# Clean up Docker resources
docker system prune -a
```

#### 5. Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
sudo chmod -R 755 .

# Fix Docker permissions
sudo usermod -aG docker $USER
# Logout and login again
```

### Performance Issues

#### 1. Slow API Responses
```bash
# Check database performance
docker-compose exec postgres psql -U ai_user -d ai_oposisi -c "EXPLAIN ANALYZE SELECT * FROM users;"

# Check Redis performance
docker-compose exec redis redis-cli info stats

# Monitor resource usage
docker stats
```

#### 2. High Memory Usage
```bash
# Check memory usage
docker stats

# Optimize Docker images
# Use multi-stage builds
# Remove unnecessary dependencies
```

#### 3. High CPU Usage
```bash
# Monitor CPU usage
docker stats

# Check for infinite loops
# Review application logs
# Optimize algorithms
```

### Debug Mode

#### 1. Enable Debug Logging
```bash
# Backend debug mode
DEBUG=true
LOG_LEVEL=DEBUG

# Frontend debug mode
REACT_APP_DEBUG=true
```

#### 2. Development Tools
```bash
# Backend debugging
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

# Frontend debugging
npm start
# Open browser dev tools
```

---

## 📞 Support

### Documentation
- [Backend API Documentation](http://localhost:8000/docs)
- [Frontend README](frontend/README.md)
- [Backend README](backend/README.md)

### Logs Location
- **Backend Logs**: `logs/app.log`, `logs/error.log`
- **Frontend Logs**: Browser console
- **Docker Logs**: `docker-compose logs`

### Monitoring
- **Health Checks**: `/health` endpoints
- **Metrics**: Prometheus and Grafana
- **Alerts**: Configure in Grafana

### Emergency Procedures
1. **Service Down**: Check Docker status and restart services
2. **Database Issues**: Check database logs and connections
3. **Security Breach**: Immediately change all secrets and investigate logs
4. **Performance Issues**: Check resource usage and optimize

---

**⚠️ PERINGATAN ETIKA**: Sistem ini **hanya untuk tujuan edukasi dan simulasi**. Dilarang digunakan untuk aktivitas politik nyata, memengaruhi opini publik, atau kampanye propaganda.

**[Kembali ke README Utama](README.md)**