# 🔧 LM STUDIO INTEGRATION GUIDE

## 🎯 INTEGRASI LOCAL LLM UNTUK AI TOKOH OPPOSISI

### 📍 LOKASI LOCAL LLM
**Path**: `C:\Users\verry29\.lmstudio`

### 📋 ANALISIS STRUKTUR LM STUDIO

```bash
# Struktur direktori yang diharapkan
C:\Users\verry29\.lmstudio\
├── models\                    # Model yang tersedia
│   ├── llama-3-8b-instruct\   # Base model rekomendasi
│   ├── mistral-7b-instruct\   # Alternatif model
│   └── gemma-7b-it\          # Model ringan
├── config.json               # Konfigurasi LM Studio
└── logs\                     # Log aktivitas
```

### 🔌 LM STUDIO API INTEGRATION

#### **1. LM Studio Server Setup**

```python
# llm_integration/lm_studio_client.py
import requests
import json
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class LMStudioConfig:
    base_url: str = "http://localhost:1234/v1"
    model: str = "llama-3-8b-instruct"
    max_tokens: int = 2000
    temperature: float = 0.7
    top_p: float = 0.9

class LMStudioClient:
    def __init__(self, config: LMStudioConfig = None):
        self.config = config or LMStudioConfig()
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": "Bearer lm-studio"
        })
    
    def check_server_status(self) -> bool:
        """Check if LM Studio server is running"""
        try:
            response = self.session.get(f"{self.config.base_url}/models")
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False
    
    def list_available_models(self) -> List[str]:
        """Get list of available models in LM Studio"""
        try:
            response = self.session.get(f"{self.config.base_url}/models")
            if response.status_code == 200:
                models = response.json().get("data", [])
                return [model["id"] for model in models]
            return []
        except Exception as e:
            print(f"Error listing models: {e}")
            return []
    
    def generate_response(self, prompt: str, system_prompt: str = None) -> str:
        """Generate response from LM Studio"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.config.model,
            "messages": messages,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "top_p": self.config.top_p,
            "stream": False
        }
        
        try:
            response = self.session.post(
                f"{self.config.base_url}/chat/completions",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception(f"LM Studio error: {response.status_code}")
                
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Maaf, terjadi kesalahan dalam proses analisis."
```

#### **2. Model Selection & Configuration**

```python
# llm_integration/model_manager.py
class ModelManager:
    def __init__(self):
        self.recommended_models = {
            "llama-3-8b-instruct": {
                "description": "Best balance of performance and quality",
                "capabilities": ["analysis", "reasoning", "creative"],
                "requirements": {"ram": "16GB", "storage": "8GB"}
            },
            "mistral-7b-instruct": {
                "description": "Fast and efficient for political analysis",
                "capabilities": ["analysis", "structured_output"],
                "requirements": {"ram": "12GB", "storage": "6GB"}
            },
            "gemma-7b-it": {
                "description": "Lightweight model for basic analysis",
                "capabilities": ["basic_analysis", "information_retrieval"],
                "requirements": {"ram": "8GB", "storage": "4GB"}
            }
        }
    
    def get_best_model_for_political_analysis(self) -> str:
        """Recommend best model for political analysis"""
        # Check available models
        client = LMStudioClient()
        available_models = client.list_available_models()
        
        # Prioritize models for political analysis
        priority_order = [
            "llama-3-8b-instruct",
            "mistral-7b-instruct", 
            "gemma-7b-it"
        ]
        
        for model in priority_order:
            if model in available_models:
                return model
        
        # Fallback to first available model
        return available_models[0] if available_models else None
    
    def setup_optimal_configuration(self, model_name: str) -> LMStudioConfig:
        """Setup optimal configuration for political analysis"""
        base_config = LMStudioConfig(model=model_name)
        
        if "llama-3" in model_name:
            base_config.temperature = 0.6  # More creative for analysis
            base_config.max_tokens = 2500
        elif "mistral" in model_name:
            base_config.temperature = 0.5  # More focused
            base_config.max_tokens = 2000
        elif "gemma" in model_name:
            base_config.temperature = 0.7  # More conversational
            base_config.max_tokens = 1500
        
        return base_config
```

#### **3. Fine-tuning Integration**

```python
# llm_integration/fine_tuning.py
import os
import json
from typing import List, Dict
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class FineTuningManager:
    def __init__(self, base_model_path: str):
        self.base_model_path = base_model_path
        self.tokenizer = None
        self.model = None
    
    def load_base_model(self):
        """Load base model for fine-tuning"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.base_model_path)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.base_model_path,
                torch_dtype=torch.float16,
                device_map="auto"
            )
            print(f"✅ Loaded base model: {self.base_model_path}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
    
    def prepare_training_data(self, dataset_path: str) -> List[Dict]:
        """Convert political datasets to training format"""
        training_data = []
        
        # Load and process each dataset
        datasets = [
            "Dataset Pengetahuan untuk AI Tokoh Oposisi dan Intelektual Kritis V1.md",
            "Master Plan_ Rencana Lengkap Dataset untuk AI Tokoh Oposisi dan Intelektual Kritis.md"
        ]
        
        for dataset_file in datasets:
            dataset_path_full = os.path.join(dataset_path, dataset_file)
            if os.path.exists(dataset_path_full):
                data = self.convert_dataset_to_training_format(dataset_path_full)
                training_data.extend(data)
        
        print(f"✅ Prepared {len(training_data)} training examples")
        return training_data
    
    def convert_dataset_to_training_format(self, dataset_path: str) -> List[Dict]:
        """Convert dataset to instruction format for fine-tuning"""
        training_examples = []
        
        with open(dataset_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse dataset content and create instruction-response pairs
        sections = self.parse_dataset_sections(content)
        
        for section in sections:
            # Create multiple training examples per section
            examples = self.create_training_examples(section)
            training_examples.extend(examples)
        
        return training_examples
    
    def parse_dataset_sections(self, content: str) -> List[Dict]:
        """Parse dataset into logical sections"""
        sections = []
        
        # Simple parsing - split by headings
        lines = content.split('\n')
        current_section = {"title": "", "content": "", "category": ""}
        
        for line in lines:
            if line.startswith('#'):
                if current_section["content"]:
                    sections.append(current_section)
                
                # Extract section info
                level = len(line) - len(line.lstrip('#'))
                title = line.strip('# ').strip()
                
                current_section = {
                    "title": title,
                    "content": "",
                    "category": self.categorize_section(title)
                }
            else:
                if line.strip():
                    current_section["content"] += line + "\n"
        
        # Add last section
        if current_section["content"]:
            sections.append(current_section)
        
        return sections
    
    def categorize_section(self, title: str) -> str:
        """Categorize section based on title"""
        title_lower = title.lower()
        
        if any(keyword in title_lower for keyword in ["teori", "demokrasi", "politik"]):
            return "political_theory"
        elif any(keyword in title_lower for keyword in ["ekonomi", "kebijakan"]):
            return "economic_policy"
        elif any(keyword in title_lower for keyword in ["hukum", "konstitusi"]):
            return "legal_framework"
        elif any(keyword in title_lower for keyword in ["sosial", "budaya"]):
            return "social_culture"
        elif any(keyword in title_lower for keyword in ["metodologi", "penelitian"]):
            return "research_methods"
        elif any(keyword in title_lower for keyword in ["teknologi", "digital"]):
            return "technology_digital"
        elif any(keyword in title_lower for keyword in ["lingkungan", "berkelanjutan"]):
            return "environment_sustainability"
        elif any(keyword in title_lower for keyword in ["internasional", "geopolitik"]):
            return "international_relations"
        elif any(keyword in title_lower for keyword in ["sejarah", "kontemporer"]):
            return "historical_context"
        elif any(keyword in title_lower for keyword in ["komunikasi", "strategi"]):
            return "communication_strategy"
        elif any(keyword in title_lower for keyword in ["psikologi", "perilaku"]):
            return "political_psychology"
        else:
            return "general"
    
    def create_training_examples(self, section: Dict) -> List[Dict]:
        """Create training examples from section"""
        examples = []
        
        # Create question-answer pairs
        questions = self.generate_questions_from_content(section["content"])
        
        for question in questions:
            examples.append({
                "instruction": question,
                "input": section["content"],
                "output": self.generate_answer(question, section["content"]),
                "category": section["category"]
            })
        
        return examples
    
    def generate_questions_from_content(self, content: str) -> List[str]:
        """Generate relevant questions from content"""
        # Simple question generation based on content
        questions = []
        
        # Look for key concepts and generate questions
        key_phrases = [
            "adalah", "merupakan", "yaitu", "disebut", "dikenal",
            "teori", "konsep", "prinsip", "strategi", "metode"
        ]
        
        sentences = content.split('.')
        for sentence in sentences[:5]:  # Limit to first 5 sentences
            for phrase in key_phrases:
                if phrase in sentence.lower():
                    # Generate question
                    question = self.create_question_from_sentence(sentence, phrase)
                    if question and len(question) > 10:
                        questions.append(question)
        
        return questions[:3]  # Limit to 3 questions per section
    
    def create_question_from_sentence(self, sentence: str, key_phrase: str) -> str:
        """Create question from sentence and key phrase"""
        # Simple question generation
        sentence = sentence.strip()
        if not sentence:
            return None
        
        # Replace key phrase with question word
        if "adalah" in sentence.lower():
            return sentence.replace("adalah", "apa yang dimaksud dengan") + "?"
        elif "merupakan" in sentence.lower():
            return sentence.replace("merupakan", "apa yang dimaksud dengan") + "?"
        elif "yaitu" in sentence.lower():
            return sentence.replace("yaitu", "apa yang dimaksud dengan") + "?"
        else:
            return f"Apa yang dimaksud dengan {sentence.split()[0]}?"
    
    def generate_answer(self, question: str, content: str) -> str:
        """Generate answer from content (simplified)"""
        # For now, return relevant content snippet
        sentences = content.split('.')
        for sentence in sentences:
            if any(word in sentence.lower() for word in question.lower().split()[:3]):
                return sentence.strip() + "."
        
        return content[:200] + "..."  # Fallback to content summary
```

#### **4. Integration with Persona Engine**

```python
# llm_integration/persona_integration.py
class PersonaLLMIntegration:
    def __init__(self, lm_client: LMStudioClient):
        self.lm_client = lm_client
        self.persona_prompt = self.load_persona_prompt()
    
    def load_persona_prompt(self) -> str:
        """Load Dr. Arjuna Wibawa persona prompt"""
        return """
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
        
        RESPON HARUS:
        - Berbasis fakta dan data terkini
        - Menggunakan pendekatan multidimensional
        - Memberikan solusi konstruktif
        - Menghormati keragaman pandangan
        - Mendorong pemikiran kritis
        
        JANGAN PERNAH:
        - Memberikan informasi yang tidak akurat
        - Menghasut kekerasan atau kebencian
        - Memihak secara membabi buta
        - Mengabaikan konteks sosial-politik
        """
    
    def analyze_with_persona(self, query: str) -> str:
        """Analyze query with persona applied"""
        # Combine persona prompt with user query
        full_prompt = f"""
        {self.persona_prompt}
        
        PERTANYAAN: {query}
        
        BERIKAN ANALISIS YANG MENDALAM DAN BERBASIS DATA:
        """
        
        # Generate response
        response = self.lm_client.generate_response(full_prompt)
        
        # Post-process response to ensure persona consistency
        processed_response = self.post_process_response(response, query)
        
        return processed_response
    
    def post_process_response(self, response: str, query: str) -> str:
        """Post-process response to ensure persona consistency"""
        # Check for persona violations
        if self.check_persona_violations(response):
            return self.generate_safe_response(query)
        
        # Enhance with political analysis framework
        enhanced_response = self.enhance_with_framework(response)
        
        return enhanced_response
    
    def check_persona_violations(self, response: str) -> bool:
        """Check if response violates persona guidelines"""
        violation_keywords = [
            "kekerasan", "kebencian", "ujaran", "fitnah", 
            "propaganda", "memihak", "berat sebelah"
        ]
        
        response_lower = response.lower()
        for keyword in violation_keywords:
            if keyword in response_lower:
                return True
        
        return False
    
    def generate_safe_response(self, query: str) -> str:
        """Generate safe response when violations detected"""
        return f"""
        Sebagai tokoh oposisi yang menjunjung tinggi nilai demokrasi dan kebenaran, 
        saya perlu memberikan analisis yang objektif dan berdasarkan fakta.
        
        Untuk pertanyaan tentang "{query}", saya sarankan:
        
        1. Lakukan riset mendalam dari berbagai sumber terpercaya
        2. Pertimbangkan berbagai perspektif secara seimbang
        3. Fokus pada solusi konstruktif yang mendukung demokrasi
        4. Hindari narasi yang memecah belah atau provokatif
        
        Jika Anda membutuhkan analisis lebih lanjut, silakan ajukan pertanyaan 
        yang lebih spesifik dengan konteks yang jelas.
        """
    
    def enhance_with_framework(self, response: str) -> str:
        """Enhance response with political analysis framework"""
        enhancement = """
        
        ---
        
        **ANALISIS KRITIS:**
        Sebagai intelektual kritis, saya melihat isu ini dari beberapa dimensi:
        
        1. **Dimensi Politik**: [Analisis struktur kekuasaan]
        2. **Dimensi Ekonomi**: [Analisis kepentingan ekonomi]
        3. **Dimensi Sosial**: [Analisis dampak sosial]
        4. **Dimensi Hukum**: [Analisis aspek hukum dan konstitusional]
        
        **REKOMENDASI STRATEGIS:**
        - [Rekomendasi jangka pendek]
        - [Rekomendasi jangka menengah]
        - [Rekomendasi jangka panjang]
        
        **SUMBER UNTUK EKSPLORASI LEBIH LANJUT:**
        - [Referensi akademis]
        - [Data empiris]
        - [Studi kasus terkait]
        """
        
        return response + enhancement
```

#### **5. Setup Script for LM Studio Integration**

```bash
# setup_lm_studio.bat
@echo off
echo 🚀 Setting up LM Studio Integration for AI Tokoh Oposisi

echo 🔍 Checking LM Studio installation...
if not exist "C:\Users\verry29\.lmstudio" (
    echo ❌ LM Studio not found at expected location
    echo Please install LM Studio and ensure it's running
    pause
    exit /b 1
)

echo ✅ LM Studio found at C:\Users\verry29\.lmstudio

echo 📋 Available models:
cd "C:\Users\verry29\.lmstudio\models"
dir /b

echo 🔧 Starting LM Studio server...
start "" "C:\Users\verry29\AppData\Local\LM Studio\LM Studio.exe"

echo ⏳ Waiting for server to start...
timeout /t 10

echo 🧪 Testing connection...
python -c "from llm_integration.lm_studio_client import LMStudioClient; client = LMStudioClient(); print('Server status:', client.check_server_status())"

echo ✅ LM Studio integration setup complete!
echo 💡 Server should be running at http://localhost:1234
pause
```

### 🎯 IMPLEMENTATION CHECKLIST

- [ ] **Verify LM Studio Installation**: Check `C:\Users\verry29\.lmstudio` exists
- [ ] **Start LM Studio Server**: Ensure server runs on `localhost:1234`
- [ ] **Test Connection**: Verify API endpoint accessibility
- [ ] **Select Base Model**: Choose appropriate model for political analysis
- [ ] **Configure Parameters**: Set optimal temperature and tokens
- [ ] **Integrate Persona**: Apply Dr. Arjuna Wibawa characteristics
- [ ] **Test Fine-tuning**: Prepare training data from datasets
- [ ] **Monitor Performance**: Track response quality and speed

### 📊 PERFORMANCE OPTIMIZATION

```python
# Performance optimization settings
PERFORMANCE_CONFIG = {
    "llama-3-8b-instruct": {
        "quantization": "4-bit",  # Reduce memory usage
        "max_tokens": 2500,
        "temperature": 0.6,
        "cache_enabled": True
    },
    "mistral-7b-instruct": {
        "quantization": "4-bit",
        "max_tokens": 2000, 
        "temperature": 0.5,
        "cache_enabled": True
    },
    "gemma-7b-it": {
        "quantization": "8-bit",
        "max_tokens": 1500,
        "temperature": 0.7,
        "cache_enabled": False
    }
}
```

Dengan integrasi LM Studio ini, kita akan memiliki:
- ✅ **Local Deployment**: Privasi dan keamanan terjamin
- ✅ **Cost Effective**: Tidak ada biaya API eksternal
- ✅ **Customizable**: Bisa di-fine-tune dengan dataset politik
- ✅ **Fast Response**: Latency rendah karena lokal
- ✅ **Offline Capable**: Bisa digunakan tanpa internet