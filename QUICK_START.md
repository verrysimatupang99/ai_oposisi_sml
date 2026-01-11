# 🚀 QUICK START GUIDE: AI TOKOH OPPOSISI & INTELEKTUAL KRITIS

## 📋 Prerequisites

Sebelum memulai, pastikan Anda memiliki:

- **Python 3.10+** - Untuk backend FastAPI
- **Node.js 16+** - Untuk frontend React
- **npm atau yarn** - Package manager
- **LM Studio** - Untuk local LLM (opsional untuk development)

## 🏃‍♂️ Langkah 1: Setup Cepat (5 Menit)

### 1. Clone dan Buka Proyek
```bash
cd C:/Coding/ai_oposisi_sml
```

### 2. Setup Backend (3 Menit)
```bash
# Buka terminal baru dan masuk ke backend
cd backend

# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
copy .env.example .env
# Edit .env jika perlu (opsional untuk development)

# Jalankan backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Setup Frontend (2 Menit)
```bash
# Buka terminal baru dan masuk ke frontend
cd ../frontend

# Install dependencies
npm install

# Jalankan frontend
npm start
```

## 🎯 Akses Aplikasi

Setelah semua service berjalan:

- **🌐 Frontend**: http://localhost:3000
- **🔌 Backend API**: http://localhost:8000
- **📚 API Documentation**: http://localhost:8000/docs

## 🔧 Konfigurasi Dasar

### Environment Variables (Opsional)

#### Backend (.env)
```bash
# Basic configuration (sudah default)
DEBUG=true
HOST=0.0.0.0
PORT=8000

# Database (default SQLite untuk development)
DATABASE_URL=sqlite:///./test.db

# LLM (default local)
LM_STUDIO_URL=http://192.168.110.162:1234
LM_STUDIO_MODEL=meta-llama-3-8b-instruct-bpe-fix

# Security
SECRET_KEY=your-secret-key-change-in-production
```

#### Frontend (.env)
```bash
# Basic configuration
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_WS_URL=ws://localhost:8000/ws
```

## 🤖 Setup LM Studio (Opsional)

Jika ingin menggunakan AI dengan LLM:

1. **Download LM Studio**: https://lmstudio.ai/
2. **Install dan buka aplikasi**
3. **Download model** (rekomendasi):
   - Llama 2 7B Chat
   - Falcon 7B
   - Atau model lain yang support
4. **Load model** di LM Studio
5. **Enable Local Server** di settings LM Studio
6. **Default URL**: http://localhost:1234

## 🎮 Mencoba Fitur

### 1. Daftar dan Login
1. Buka http://localhost:3000
2. Klik "Daftar di sini" atau gunakan demo account:
   - Username: `demo`
   - Password: `Demo123!`
3. Login ke dashboard

### 2. Coba Chat dengan Dr. Arjuna
1. Klik menu "Chat"
2. Ketik pesan seperti: "Apa pendapat Anda tentang demokrasi di Indonesia?"
3. Tunggu respons dari AI

### 3. Coba Analisis Politik
1. Klik menu "Analysis"
2. Masukkan teks politik untuk dianalisis
3. Lihat hasil analisis dari AI

### 4. Eksplorasi Fitur Lain
- **Persona**: Lihat dan konfigurasi persona AI
- **Ethics**: Lihat validasi etika konten
- **Profile**: Kelola profil pengguna

## 🐛 Troubleshooting Cepat

### Backend Error
```bash
# Jika backend error, coba:
pip install -r requirements.txt --force-reinstall
# atau
python -m pip install --upgrade pip
```

### Frontend Error
```bash
# Jika frontend error, coba:
rm -rf node_modules package-lock.json
npm install
npm start
```

### Port Already in Use
```bash
# Cek port 8000
netstat -ano | findstr :8000
# Cek port 3000
netstat -ano | findstr :3000

# Jika port terpakai, matikan proses atau ganti port di:
# Backend: app/main.py (ubah PORT=8000)
# Frontend: frontend/.env (ubah REACT_APP_API_URL)
```

### LM Studio Connection Error
```bash
# Pastikan LM Studio running di http://localhost:1234
# Cek di browser: http://localhost:1234/v1/models
# Jika error, restart LM Studio dan enable Local Server
```

## 🎯 Demo Account

Untuk testing cepat, gunakan:

```bash
Username: demo
Password: Demo123!
```

## 📁 Struktur Folder Penting

```
ai_oposisi_sml/
├── backend/          # FastAPI backend
│   ├── app/          # Source code backend
│   ├── venv/         # Virtual environment
│   └── requirements.txt
├── frontend/         # React frontend
│   ├── src/          # Source code frontend
│   ├── node_modules/ # Dependencies
│   └── package.json
└── docs/             # Documentation
```

## 🚀 Development Tips

### Backend Development
```bash
# Jalankan dengan auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Lihat API docs
# Buka: http://localhost:8000/docs

# Test API
curl http://localhost:8000/health
```

### Frontend Development
```bash
# Jalankan development server
npm start

# Build production
npm run build

# Lihat linting
npm run lint
```

## 🎉 Selamat!

Anda sekarang memiliki sistem AI Tokoh Oposisi & Intelektual Kritis yang berjalan di local machine!

### Fitur yang Sudah Bisa Digunakan:
- ✅ Authentication (Login/Register)
- ✅ Chat dengan AI Persona (Dr. Arjuna Wibawa)
- ✅ Political Analysis
- ✅ Ethics Validation
- ✅ Responsive UI
- ✅ Real-time updates

### Next Steps:
1. **Explore**: Coba semua fitur yang tersedia
2. **Customize**: Sesuaikan persona dan konfigurasi
3. **Develop**: Tambahkan fitur baru sesuai kebutuhan
4. **Deploy**: Deploy ke production jika siap

---

**⚠️ PERINGATAN ETIKA**: Sistem ini **hanya untuk tujuan edukasi dan simulasi**. Dilarang digunakan untuk aktivitas politik nyata, memengaruhi opini publik, atau kampanye propaganda.

**[Kembali ke Deployment Guide](DEPLOYMENT_GUIDE.md) untuk setup production** 🚀