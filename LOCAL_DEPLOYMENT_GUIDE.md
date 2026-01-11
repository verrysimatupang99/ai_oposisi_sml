# 🚀 LOCAL DEPLOYMENT GUIDE: AI TOKOH OPPOSISI

## 📋 HOW TO RUN LOCALLY

Panduan lengkap untuk menjalankan AI Tokoh Oposisi & Intelektual Kritis di lingkungan lokal Anda.

---

## 🛠️ PREREQUISITES

### **System Requirements**
- **OS**: Windows 10/11, macOS 10.15+, Linux Ubuntu 18.04+
- **RAM**: 16GB+ (rekomendasi), 8GB minimum
- **Storage**: 20GB+ free space
- **Python**: 3.10+ 
- **Node.js**: 16+ (untuk frontend)

### **Required Software**
```bash
# Python 3.10+
# Download from: https://www.python.org/downloads/

# Node.js 16+
# Download from: https://nodejs.org/

# Git (optional but recommended)
# Download from: https://git-scm.com/

# Docker (optional, untuk deployment container)
# Download from: https://www.docker.com/
```

---

## 📁 PROJECT STRUCTURE

Pastikan Anda memiliki struktur project seperti ini:
```
ai_oposisi_sml/
├── backend/                    # 🐍 FastAPI Backend
├── frontend/                   # 🌐 React Frontend  
├── ai_dataset/                 # 📚 Dataset politik
└── scripts/                    # 🛠️ Utility scripts
```

---

## 🚀 STEP-BY-STEP SETUP

### **Step 1: Clone or Setup Project**

```bash
# Jika menggunakan Git
git clone <repository-url>
cd ai_oposisi_sml

# Atau copy manual ke folder lokal
# Pastikan struktur folder sesuai
```

### **Step 2: Setup Backend (Python)**

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
copy .env.example .env
# atau di Linux/Mac:
cp .env.example .env

# Edit .env file and configure:
# - Database URL (PostgreSQL)
# - LLM settings (LM Studio)
# - Secret keys
```

### **Step 3: Setup Database**

#### **Option A: Local PostgreSQL**
```bash
# Install PostgreSQL
# Windows: Download from https://www.postgresql.org/download/windows/
# macOS: brew install postgresql
# Linux: sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
# Windows: Services -> Start PostgreSQL
# macOS: brew services start postgresql
# Linux: sudo systemctl start postgresql

# Create database and user
sudo -u postgres psql
CREATE DATABASE ai_oposisi;
CREATE USER ai_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ai_oposisi TO ai_user;
\q

# Update .env file:
DATABASE_URL="postgresql+asyncpg://ai_user:your_password@localhost:5432/ai_oposisi"
```

#### **Option B: SQLite (Development Only)**
```bash
# For development, you can use SQLite
# Update .env file:
DATABASE_URL="sqlite+aiosqlite:///./ai_oposisi.db"
```

### **Step 4: Setup LM Studio**

```bash
# 1. Download and install LM Studio
# Website: https://lmstudio.ai/

# 2. Install a political analysis model
# Recommended models:
# - Llama-3-8B-Instruct (best balance)
# - Mistral-7B-Instruct (fast and efficient)
# - Gemma-7B-IT (lightweight)

# 3. Start LM Studio server
# - Open LM Studio
# - Load your model
# - Go to Local Server tab
# - Enable "Allow remote connections"
# - Note the port (default: 1234)

# 4. Update .env file:
LLM_BASE_URL="http://localhost:1234/v1"
LLM_MODEL="llama-3-8b-instruct"  # Sesuaikan dengan model Anda
```

### **Step 5: Setup Frontend (React)**

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Edit .env file:
REACT_APP_API_URL="http://localhost:8000/api/v1"
REACT_APP_WS_URL="http://localhost:8000"
```

### **Step 6: Initialize Database**

```bash
# Back to backend directory
cd ../backend

# Run database migrations
python -c "
from app.core.database import init_db
import asyncio
asyncio.run(init_db())
print('Database initialized successfully!')
"
```

### **Step 7: Start Backend Server**

```bash
# Make sure virtual environment is activated
# venv\Scripts\activate (Windows)
# source venv/bin/activate (macOS/Linux)

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Expected output:
# INFO:     Started server process [12345]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### **Step 8: Start Frontend Server**

```bash
# In new terminal window
cd frontend

# Start frontend
npm start

# Expected output:
# Local:            http://localhost:3000
# On Your Network:  http://192.168.x.x:3000
```

---

## 🔧 CONFIGURATION

### **Backend Configuration (.env)**

```bash
# Application Settings
APP_NAME="AI Tokoh Oposisi & Intelektual Kritis"
APP_VERSION="1.0.0"
DEBUG=true

# Database Settings
DATABASE_URL="postgresql+asyncpg://ai_user:your_password@localhost:5432/ai_oposisi"
REDIS_URL="redis://localhost:6379/0"

# LLM Settings
LLM_BASE_URL="http://localhost:1234/v1"
LLM_MODEL="llama-3-8b-instruct"
LLM_MAX_TOKENS=2000
LLM_TEMPERATURE=0.7

# Security Settings
SECRET_KEY="your-secret-key-here-change-this"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Settings
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
```

### **Frontend Configuration (.env)**

```bash
REACT_APP_API_URL="http://localhost:8000/api/v1"
REACT_APP_WS_URL="http://localhost:8000"
REACT_APP_VERSION="1.0.0"
```

---

## 🧪 TESTING THE SETUP

### **Test Backend API**

```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","service":"ai-oposisi-backend","version":"1.0.0"}

# Test LM Studio connection
curl http://localhost:1234/v1/models

# Expected response should show your loaded model
```

### **Test Frontend**

Buka browser dan buka:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs (Swagger UI)
- **LM Studio**: http://localhost:1234

### **Test Full Integration**

1. **Buka frontend**: http://localhost:3000
2. **Register akun baru** atau gunakan akun demo
3. **Login ke sistem**
4. **Coba analisis politik**:
   - Masukkan pertanyaan: "Bagaimana dampak kebijakan subsidi energi terhadap perekonomian Indonesia?"
   - Pilih tipe analisis: "Ekonomi"
   - Klik "Mulai Analisis"
5. **Tunggu respons** dari Dr. Arjuna Wibawa

---

## 🐛 TROUBLESHOOTING

### **Common Issues & Solutions**

#### **Issue 1: Port Already in Use**
```bash
# Check what's using port 8000
# Windows: netstat -ano | findstr :8000
# macOS/Linux: lsof -i :8000

# Kill process using port
# Windows: taskkill /PID <PID> /F
# macOS/Linux: kill -9 <PID>
```

#### **Issue 2: Database Connection Error**
```bash
# Check PostgreSQL is running
# Windows: services.msc -> PostgreSQL
# macOS: brew services list | grep postgresql
# Linux: sudo systemctl status postgresql

# Test database connection
psql -h localhost -U ai_user -d ai_oposisi
```

#### **Issue 3: LM Studio Not Responding**
```bash
# Check LM Studio is running
# Check model is loaded
# Check "Allow remote connections" is enabled
# Check port 1234 is not blocked by firewall
```

#### **Issue 4: Frontend Can't Connect to Backend**
```bash
# Check backend is running on http://localhost:8000
# Check CORS settings in backend .env
# Check frontend .env has correct API URL
```

#### **Issue 5: Python Dependencies Error**
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# If still failing, try:
pip install --no-cache-dir -r requirements.txt
```

### **Debug Commands**

```bash
# Check Python version
python --version

# Check virtual environment
which python  # Should show venv path

# Check dependencies
pip list

# Check environment variables
echo $DATABASE_URL  # Linux/macOS
echo %DATABASE_URL%  # Windows

# Test API endpoints
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test&password=test"
```

---

## 🐳 DOCKER ALTERNATIVE

### **Using Docker Compose**

```bash
# Navigate to project root
cd ai_oposisi_sml

# Build and run all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Clean up
docker-compose down -v --remove-orphans
```

### **Docker Environment**

```bash
# Create .env file for Docker
cp .env.example .env

# Edit .env with your configuration
# Make sure to use service names for internal connections:
DATABASE_URL="postgresql+asyncpg://ai_user:password@postgres:5432/ai_oposisi"
REDIS_URL="redis://redis:6379/0"
LLM_BASE_URL="http://lm-studio:1234/v1"
```

---

## 🎯 PRODUCTION NOTES

### **For Production Deployment**

1. **Change all passwords and secrets**
2. **Use HTTPS with SSL certificates**
3. **Set DEBUG=false in production**
4. **Use production database (PostgreSQL)**
5. **Configure proper CORS settings**
6. **Set up monitoring and logging**
7. **Implement backup strategies**

### **Security Checklist**

- [ ] Change default passwords
- [ ] Use strong secret keys
- [ ] Enable HTTPS
- [ ] Configure firewall
- [ ] Set up monitoring
- [ ] Regular security updates
- [ ] Backup strategy

---

## 📞 SUPPORT

### **Getting Help**

1. **Check logs**:
   - Backend: `uvicorn logs`
   - Frontend: Browser console
   - LM Studio: LM Studio logs

2. **Common solutions**:
   - Restart all services
   - Check environment variables
   - Verify network connectivity
   - Check port availability

3. **Documentation**:
   - [Backend API Docs](http://localhost:8000/docs)
   - [Frontend README](frontend/README.md)
   - [LM Studio Documentation](https://docs.lmstudio.ai/)

---

## 🎉 SUCCESS!

Jika semua langkah di atas berhasil, Anda sekarang memiliki:

✅ **Backend API** berjalan di http://localhost:8000  
✅ **Frontend Web App** berjalan di http://localhost:3000  
✅ **LM Studio** berjalan di http://localhost:1234  
✅ **Database** terhubung dan siap digunakan  
✅ **Dr. Arjuna Wibawa** siap menganalisis politik!  

**Selamat! Anda sekarang memiliki AI Tokoh Oposisi & Intelektual Kritis yang berjalan secara lokal!** 🤖🇮🇩

---

## 🚀 NEXT STEPS

1. **Explore the application** - Coba semua fitur
2. **Customize persona** - Sesuaikan Dr. Arjuna Wibawa
3. **Add datasets** - Tambahkan dataset politik baru
4. **Monitor performance** - Pantau kinerja sistem
5. **Scale up** - Siapkan untuk deployment production

**Happy analyzing!** 📊✨