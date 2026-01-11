# 📚 DATA DIRECTORY - AI TOKOH OPOSISI & INTELEKTUAL KRITIS

> Knowledge base, datasets, and persona definitions for the AI Opposition Figure & Critical Intellectual system.

---

## 📁 DIRECTORY STRUCTURE

```
data/
├── 📂 datasets/           # 15 comprehensive political datasets
│   ├── Dataset 1-15 (MD) # Markdown format (primary)
│   └── *.pdf              # PDF backups (6 files)
│
├── 📂 persona/            # Persona definition
│   └── persona_utama.md   # Dr. Arjuna Wibawa character
│
└── 📂 docs/               # Master plans & documentation
    ├── Master Plan_*.md
    ├── DOKUMEN LENGKAP_*.md
    ├── REPORT SUMMARY_*.md
    └── Hornet.md
```

---

## 📊 DATASETS OVERVIEW

### **15 Comprehensive Datasets (5 Clusters)**

#### 🎯 **Cluster A: Intellectual Foundation (Dataset 1-3)**
1. **Dataset Pengetahuan V1** - Political theory & academic frameworks
2. **Dataset Kedua** - Practical cases & operational techniques
3. **Dataset Ketiga** - Power psychology & counter-intelligence

#### 🇮🇩 **Cluster B: Indonesian Context (Dataset 4-6)**
4. **Dataset Keempat** - Indonesia deep dive - contemporary politics
5. **Dataset Kelima** - Political economy - Soeharto to now
6. **Dataset Keenam** - Political culture & civil society

#### ⚔️ **Cluster C: Warfare & Operations (Dataset 7-9)**
7. **Dataset Ketujuh** - Digital warfare & cyber operations
8. **Dataset Kedelapan** - Regional geopolitics & international relations
9. **Dataset Kesembilan** - Crisis management & emergency response

#### 🌍 **Cluster D: Communication & Law (Dataset 10-11)**
10. **Dataset Kesepuluh** - Media relations & public communication
11. **Dataset Kesebelas** - Legal framework & constitutional law

#### 🛠️ **Cluster E: Advanced Capabilities (Dataset 12-15)**
12. **Dataset Keduabelas** - Organizational development & leadership
13. **Dataset Ketigabelas** - Advanced research methods & intelligence analysis
14. **Dataset Keempatbelas** - International relations & diplomatic strategy
15. **Dataset Kelimabelas** - Future scenarios & strategic planning

---

## 🎭 PERSONA DEFINITION

### **Dr. Arjuna Wibawa**

**File**: `persona/persona_utama.md`

**Character Profile:**
- **Role**: Tokoh Oposisi Konstruktif & Intelektual Kritis
- **Expertise**: Indonesian politics, strategic analysis, democracy
- **Communication Style**: Analytical, persuasive, educational
- **Core Values**: Democracy, justice, transparency, accountability
- **Approach**: Data-driven, empathetic, solution-focused

**Key Characteristics:**
- Deep knowledge of Indonesian political history
- Multi-dimensional analysis capability
- Ethical framework grounded in democracy
- Empati sosial & kearifan strategis
- Code-switching for different audiences

---

## 📋 DOCUMENTATION FILES

### **Master Planning Documents**

Located in `docs/` directory:

1. **Master Plan_*.md** - Complete dataset planning & structure
2. **DOKUMEN LENGKAP_*.md** - Comprehensive master document (266KB)
3. **REPORT SUMMARY_*.md** - Executive summary & overview
4. **Hornet.md** - Additional technical documentation

These documents provide:
- Dataset architecture & organization
- Implementation guidelines
- Content coverage maps
- Ethics protocols
- Research methodology

---

## 🔧 USAGE IN APPLICATION

### **Backend Integration**

The datasets are processed by the backend services:

```python
# Load datasets
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DATASETS_DIR = DATA_DIR / "datasets"
PERSONA_FILE = DATA_DIR / "persona" / "persona_utama.md"

# Use in services
from app.services.dataset_processor import DatasetProcessor

processor = DatasetProcessor(DATASETS_DIR)
datasets = await processor.load_all_datasets()
```

### **Service Layer**

- **`services/knowledge_service.py`** - Loads and indexes datasets
- **`services/persona_service.py`** - Applies persona characteristics
- **`services/embedding_service.py`** - Generates vector embeddings
- **`services/dataset_processor.py`** - Processes raw markdown data

### **API Access**

Datasets are accessible through API endpoints:

```bash
GET  /api/v1/datasets        # List all datasets
GET  /api/v1/datasets/{id}   # Get specific dataset
GET  /api/v1/persona         # Get persona profile
POST /api/v1/analysis        # Analyze with dataset context
```

---

## 📊 STATISTICS

| Category | Count | Size |
|----------|-------|------|
| **Dataset Files (MD)** | 15 | ~1.8 MB |
| **PDF Backups** | 6 | ~1.4 MB |
| **Persona Files** | 1 | ~10 KB |
| **Documentation** | 4 | ~280 KB |
| **Total** | 26 files | 2.32 MB |

---

## 🔄 UPDATE WORKFLOW

### **Adding New Datasets**

1. Create new dataset file in `datasets/` directory
2. Follow naming convention: `Dataset [Name]_*.md`
3. Update this README
4. Run backend reprocessing script
5. Rebuild embeddings

### **Updating Existing Datasets**

1. Edit dataset file in `datasets/` directory
2. Document changes in commit message
3. Backend will auto-reload with `--reload` flag
4. Rebuild embeddings if significant changes

### **Modifying Persona**

1. Edit `persona/persona_utama.md`
2. Test consistency with validation script
3. Backend services auto-reload
4. Verify persona application in responses

---

## 🛡️ DATA INTEGRITY

### **Quality Assurance**

- All datasets undergo quality validation
- Cross-reference with authoritative sources
- Regular updates to maintain accuracy
- Version control for all changes

### **Backup Strategy**

- PDF backups for critical datasets
- Git version control
- Regular backups to cloud storage (optional)
- Disaster recovery procedures documented

---

## 📚 DATASET PROCESSING PIPELINE

```
Raw Datasets (MD)
    │
    ▼
Text Extraction & Cleaning
    │
    ▼
Tokenization & Normalization
    │
    ▼
Embedding Generation (Vector DB)
    │
    ▼
Knowledge Graph Construction
    │
    ▼
RAG-Ready Knowledge Base
    │
    ▼
API Access Layer
```

---

## 🔍 SEARCH & RETRIEVAL

### **Semantic Search**

Datasets are indexed in vector database (ChromaDB) for:
- Semantic similarity search
- Context-aware retrieval
- Multi-query expansion
- Hybrid search (keyword + semantic)

### **RAG (Retrieval-Augmented Generation)**

Used in:
- Political analysis queries
- Chat responses
- Research assistance
- Policy recommendations

---

## ⚠️ IMPORTANT NOTES

### **Usage Guidelines**

✅ **Allowed:**
- Educational research & analysis
- Academic simulation & study
- Policy research & recommendations
- Training & capacity building

❌ **Prohibited:**
- Real political campaigns
- Public opinion manipulation
- Propaganda & disinformation
- Electoral interference

### **Data Handling**

- All data is **open for educational use**
- Proper attribution required
- Regular updates recommended
- Ethical use mandatory

---

## 🔗 RELATED FILES

- **Application**: `../backend/app/main.py`
- **Services**: `../backend/app/services/`
- **Configuration**: `../backend/app/core/config.py`
- **Documentation**: Project root `*.md` files

---

## 📞 MAINTENANCE

### **Regular Tasks**

- **Weekly**: Check for data updates
- **Monthly**: Validate data accuracy
- **Quarterly**: Major dataset review
- **Yearly**: Comprehensive audit

### **Contacts**

For dataset updates or issues:
- Check backend logs: `../backend/logs/`
- Review documentation: `docs/` directory
- Update tracking: Git commit history

---

**Last Updated**: January 2025  
**Version**: 2.0 (Consolidated Structure)  
**Location**: `ai_oposisi_sml/data/`

---

**End of Document** 📚
