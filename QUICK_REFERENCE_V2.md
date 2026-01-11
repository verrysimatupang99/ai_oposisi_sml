# 🚀 QUICK REFERENCE - POST CONSOLIDATION

**Version**: 2.0.0 (Consolidated Structure)  
**Date**: January 2025  
**Status**: Ready for Phase 2

---

## 📂 NEW PROJECT LOCATION

**Everything is now in ONE directory:**

```
C:\Coding\ai_oposisi_sml\
```

**Old directory (NO LONGER USED):**
```
C:\Coding\ai_dataset\  ❌ OBSOLETE
```

---

## 📁 KEY DIRECTORIES

| Directory | Purpose | Contents |
|-----------|---------|----------|
| `backend/` | FastAPI application | API, services, models |
| `frontend/` | React application | Components, pages, store |
| `data/` | ⭐ **NEW** Knowledge base | Datasets, persona, docs |
| `data/datasets/` | Political datasets | 15 MD files + 6 PDFs |
| `data/persona/` | Persona definition | persona_utama.md |
| `data/docs/` | Master plans | Planning documents |

---

## 🔧 CONFIGURATION CHANGES

### **Backend Paths (Updated)**

```python
# File: backend/app/core/config.py

# OLD (v1.0)
DATASET_PATH: str = "./datasets"
KNOWLEDGE_BASE_PATH: str = "./knowledge_base"

# NEW (v2.0)
DATASET_PATH: str = str(DATA_DIR / "datasets")
PERSONA_PATH: str = str(DATA_DIR / "persona" / "persona_utama.md")
DOCS_PATH: str = str(DATA_DIR / "docs")
```

### **Access in Code**

```python
from app.core.config import settings

# Load datasets
datasets_dir = settings.DATASET_PATH  # Points to data/datasets/

# Load persona
persona_file = settings.PERSONA_PATH  # Points to data/persona/persona_utama.md

# Load docs
docs_dir = settings.DOCS_PATH  # Points to data/docs/
```

---

## 🚀 QUICK COMMANDS

### **Navigate to Project**
```bash
cd C:\Coding\ai_oposisi_sml
```

### **Start Backend**
```bash
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Start Frontend**
```bash
cd frontend
npm run dev
```

### **Access Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### **View Datasets**
```bash
cd data\datasets
dir *.md
```

### **View Persona**
```bash
notepad data\persona\persona_utama.md
```

---

## 📚 DOCUMENTATION FILES

| File | Location | Description |
|------|----------|-------------|
| **Main README** | `README.md` | Complete project overview (v2.0) |
| **Data README** | `data/README.md` | Dataset documentation |
| **Consolidation Report** | `CONSOLIDATION_REPORT.md` | This consolidation details |
| **Quick Start** | `QUICK_START.md` | Getting started guide |
| **Architecture** | `ARCHITECTURE_PLAN.md` | System design |
| **LLM Integration** | `LM_STUDIO_INTEGRATION.md` | LLM setup |

---

## ✅ WHAT CHANGED

### **✅ Added**
- `data/` directory with all datasets
- `data/README.md` - Dataset documentation
- `.gitignore` - Git ignore rules
- `CONSOLIDATION_REPORT.md` - Migration report
- Updated `README.md` (v2.0)

### **🔄 Updated**
- `backend/app/core/config.py` - Path configuration
- All documentation references

### **❌ Removed/Obsolete**
- `C:\Coding\ai_dataset\` - No longer used

---

## 🎯 PHASE 2 DEVELOPMENT

### **Resume Development**

You can now continue Phase 2 with the consolidated structure:

**Remaining Tasks:**
1. ✅ Project consolidation (DONE)
2. Dataset processing pipeline
3. Persona engine implementation
4. Ethics validation layer
5. Semantic search & RAG
6. Web interface components

**Start Here:**
```bash
cd C:\Coding\ai_oposisi_sml
code .  # Open in VS Code

# Or read the implementation plan
notepad IMPLEMENTATION_PHASE_2.md
```

---

## 🔍 FIND FILES QUICKLY

### **Datasets**
```bash
# All datasets
dir data\datasets\*.md

# Specific dataset
notepad "data\datasets\Dataset Keempat_*.md"
```

### **Persona**
```bash
notepad data\persona\persona_utama.md
```

### **Master Plans**
```bash
dir data\docs\*.md
notepad "data\docs\Master Plan_*.md"
```

### **Backend Code**
```bash
dir backend\app\*.py /s
```

### **Frontend Code**
```bash
dir frontend\src\*.tsx /s
```

---

## 🛠️ TROUBLESHOOTING

### **Issue: Backend can't find datasets**
```bash
# Check path
cd C:\Coding\ai_oposisi_sml
dir data\datasets

# Verify config
python -c "from backend.app.core.config import settings; print(settings.DATASET_PATH)"
```

### **Issue: Old path references**
```bash
# Search for old paths
cd backend
findstr /s "ai_dataset" *.py

# Update to use settings.DATASET_PATH
```

### **Issue: Frontend can't connect**
```bash
# Check backend is running
curl http://localhost:8000/health

# Check CORS settings
# Edit backend/app/core/config.py: ALLOWED_ORIGINS
```

---

## 📋 CHECKLIST

**After Consolidation:**

- [ ] Read `CONSOLIDATION_REPORT.md`
- [ ] Review updated `README.md`
- [ ] Check `data/README.md`
- [ ] Verify backend starts successfully
- [ ] Verify frontend starts successfully
- [ ] Test dataset loading (when implemented)
- [ ] Optional: Delete old `ai_dataset/` directory

**Before Phase 2:**

- [ ] Understand new directory structure
- [ ] Review path configuration
- [ ] Set up development environment
- [ ] Read Phase 2 implementation plan

---

## 🎯 COMMON TASKS

### **View All Datasets**
```powershell
Get-ChildItem -Path "C:\Coding\ai_oposisi_sml\data\datasets" -Filter "*.md" | Select-Object Name
```

### **Count Dataset Lines**
```powershell
(Get-Content "C:\Coding\ai_oposisi_sml\data\datasets\*.md" | Measure-Object -Line).Lines
```

### **Check Data Size**
```powershell
(Get-ChildItem -Path "C:\Coding\ai_oposisi_sml\data" -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
```

### **Grep Datasets**
```bash
# Search all datasets for a term
cd data\datasets
findstr /i "demokrasi" *.md
```

---

## 🔗 USEFUL LINKS

**Local:**
- Project Root: `C:\Coding\ai_oposisi_sml`
- Datasets: `C:\Coding\ai_oposisi_sml\data\datasets`
- Backend: `C:\Coding\ai_oposisi_sml\backend`
- Frontend: `C:\Coding\ai_oposisi_sml\frontend`

**When Running:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

---

## ⚡ QUICK TIPS

1. **Always start from project root**: `cd C:\Coding\ai_oposisi_sml`
2. **Use relative paths**: Backend config handles path resolution
3. **Read the data README**: `data/README.md` has dataset details
4. **Check logs**: `backend/logs/` for troubleshooting
5. **Use API docs**: http://localhost:8000/docs for testing

---

## 📞 NEED HELP?

1. Read `README.md` (main documentation)
2. Check `TROUBLESHOOTING.md`
3. Review `CONSOLIDATION_REPORT.md`
4. Look at code comments in `backend/app/`

---

**Version**: 2.0.0  
**Updated**: January 2025  
**Structure**: Consolidated ✅

---

**Happy Coding! 🚀**
