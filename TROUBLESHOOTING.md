# 🔧 TROUBLESHOOTING GUIDE: AI TOKOH OPPOSISI & INTELEKTUAL KRITIS

## 🚨 Common Issues & Solutions

### 1. Virtual Environment Creation Error

**Error**: `unable to create directory 'C:\Coding\ai_oposisi_sml\backend\venv\Scripts\activate'`

**Solutions**:

#### Solution A: Run as Administrator
```bash
# Buka Command Prompt sebagai Administrator
# Klik Start > ketik "cmd" > Klik kanan > Run as administrator

cd C:\Coding\ai_oposisi_sml\backend
python -m venv venv
```

#### Solution B: Use Different Directory
```bash
# Coba buat virtual environment di tempat lain
cd C:\Coding\ai_oposisi_sml\backend
python -m venv C:\temp\ai_oposisi_venv
```

#### Solution C: Use Conda (if installed)
```bash
# Jika punya Anaconda/Miniconda
conda create -n ai_oposisi python=3.10
conda activate ai_oposisi
```

#### Solution D: Use pipenv
```bash
# Install pipenv jika belum ada
pip install pipenv

# Buat environment dengan pipenv
cd C:\Coding\ai_oposisi_sml\backend
pipenv --python 3.10
pipenv install
pipenv shell
```

### 2. Permission Issues

**Error**: Access denied or permission errors

**Solutions**:
```bash
# Run Command Prompt as Administrator
# Atau ubah permission folder
# Klik kanan folder > Properties > Security > Edit > Beri full control
```

### 3. Python Not Found

**Error**: 'python' is not recognized as an internal or external command

**Solutions**:
```bash
# Cek apakah Python terinstall
python --version
# atau
py --version

# Jika error, coba:
py -3.10 --version

# Atau cari lokasi Python
where python
# atau
where py
```

### 4. Requirements Installation Error

**Error**: Failed to install requirements

**Solutions**:
```bash
# Update pip dulu
python -m pip install --upgrade pip

# Install requirements dengan force
pip install -r requirements.txt --force-reinstall --no-cache-dir

# Jika masih error, install satu per satu
pip install fastapi
pip install uvicorn[standard]
pip install sqlalchemy
# ... dan seterusnya
```

### 5. Port Already in Use

**Error**: Address already in use

**Solutions**:
```bash
# Cek proses yang menggunakan port 8000
netstat -ano | findstr :8000

# Matikan proses (ganti PID dengan yang muncul)
taskkill /PID [PID] /F

# Atau ganti port di app/main.py
# Ubah: PORT = 8000 menjadi PORT = 8001
```

### 6. Database Connection Error

**Error**: Cannot connect to database

**Solutions**:
```bash
# Untuk development, gunakan SQLite (default)
# Edit .env file:
DATABASE_URL=sqlite:///./test.db

# Atau install PostgreSQL jika ingin pakai PostgreSQL
# Download dari: https://www.postgresql.org/download/windows/
```

### 7. Frontend npm Error

**Error**: npm install failed

**Solutions**:
```bash
# Hapus node_modules dan package-lock.json
rm -rf node_modules package-lock.json

# Install ulang dengan clean cache
npm cache clean --force
npm install

# Jika masih error, coba:
npm install --legacy-peer-deps
```

### 8. LM Studio Connection Error

**Error**: Cannot connect to LM Studio

**Solutions**:
```bash
# Pastikan LM Studio running
# Buka browser: http://localhost:1234

# Cek apakah model sudah terload
# Di LM Studio, pastikan model sudah aktif

# Cek firewall
# Pastikan port 1234 tidak diblokir firewall

# Coba restart LM Studio
# Tutup dan buka kembali LM Studio
```

## 🐛 Step-by-Step Fix

### Complete Reset & Setup

```bash
# 1. Hapus semua virtual environment
cd C:\Coding\ai_oposisi_sml\backend
rmdir /s /q venv

# 2. Buat virtual environment baru
python -m venv venv

# 3. Aktifkan virtual environment
venv\Scripts\activate

# 4. Update pip
python -m pip install --upgrade pip

# 5. Install requirements
pip install -r requirements.txt

# 6. Jalankan backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Alternative: Use Docker

Jika masih ada masalah, gunakan Docker:

```bash
# 1. Install Docker Desktop
# Download dari: https://www.docker.com/products/docker-desktop

# 2. Jalankan semua service dengan Docker
cd C:\Coding\ai_oposisi_sml
docker-compose up -d

# 3. Akses aplikasi
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

## 📋 System Requirements Check

### Python Version
```bash
python --version
# Harus: Python 3.10 atau lebih baru
```

### Node.js Version
```bash
node --version
# Harus: Node.js 16 atau lebih baru

npm --version
# Harus: npm 7 atau lebih baru
```

### Disk Space
```bash
# Pastikan ada cukup ruang disk
# Backend: ~100MB
# Frontend: ~200MB
# LM Studio: ~5-10GB (tergantung model)
```

## 🆘 Advanced Troubleshooting

### Check Python Installation
```bash
# Cek apakah Python benar-benar terinstall
where python
where py

# Cek environment variables
echo %PATH%

# Cek apakah Python ada di PATH
python --version
```

### Check Virtual Environment
```bash
# Cek apakah virtual environment aktif
echo %VIRTUAL_ENV%

# Jika tidak ada output, berarti virtual environment belum aktif
# Aktifkan lagi: venv\Scripts\activate
```

### Check Dependencies
```bash
# Cek dependencies yang terinstall
pip list

# Cek versi spesifik
pip show fastapi
pip show uvicorn
```

### Check Port Availability
```bash
# Cek semua port yang digunakan
netstat -ano

# Cek port spesifik
netstat -ano | findstr :8000
netstat -ano | findstr :3000
netstat -ano | findstr :1234
```

## 📞 Support

### Jika Masih Error:

1. **Screenshot error** yang muncul
2. **Copy-paste error message** lengkap
3. **Cek system specs**:
   - Windows version
   - Python version
   - Node.js version
   - Disk space available

### Common Error Messages:

- **"python: command not found"** → Python belum terinstall atau tidak di PATH
- **"pip is not recognized"** → pip belum terinstall atau tidak di PATH  
- **"permission denied"** → Jalankan sebagai administrator
- **"port already in use"** → Port sudah dipakai proses lain
- **"module not found"** → Dependencies belum terinstall

---

**⚠️ Jika semua solusi di atas tidak berhasil, coba:**

1. **Restart komputer**
2. **Update Windows**
3. **Install ulang Python**
4. **Gunakan Docker sebagai alternatif**

**[Kembali ke Quick Start](QUICK_START.md) setelah masalah teratasi!** 🚀