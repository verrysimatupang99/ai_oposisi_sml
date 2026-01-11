# 🌐 WEB INTERFACE IMPLEMENTATION PLAN

## 🎯 HYBRID WEB APPLICATION FOR AI TOKOH OPPOSISI

### 📋 PROJECT OVERVIEW
Membangun web interface modern dengan React.js yang menyediakan:
- **Dashboard Analisis Politik** - Platform interaktif untuk analisis politik
- **Persona Interaction** - Interaksi dengan Dr. Arjuna Wibawa
- **Real-time Analytics** - Visualisasi data politik real-time
- **Content Management** - Sistem manajemen konten untuk dataset

---

## 🏗️ FRONTEND ARCHITECTURE

### **1. REACT APPLICATION STRUCTURE**

```
frontend/
├── public/
│   ├── index.html
│   ├── manifest.json
│   └── robots.txt
├── src/
│   ├── components/
│   │   ├── Dashboard/
│   │   │   ├── MainDashboard.jsx
│   │   │   ├── PoliticalAnalysis.jsx
│   │   │   ├── TrendAnalysis.jsx
│   │   │   └── LiveUpdates.jsx
│   │   ├── Persona/
│   │   │   ├── PersonaProfile.jsx
│   │   │   ├── Conversation.jsx
│   │   │   ├── EthicsChecker.jsx
│   │   │   └── FeedbackSystem.jsx
│   │   ├── Analysis/
│   │   │   ├── QueryInput.jsx
│   │   │   ├── ResponseDisplay.jsx
│   │   │   ├── SourceCitation.jsx
│   │   │   └── ConfidenceMeter.jsx
│   │   ├── DataVisualization/
│   │   │   ├── PoliticalCharts.jsx
│   │   │   ├── SentimentAnalysis.jsx
│   │   │   ├── NetworkGraph.jsx
│   │   │   └── Timeline.jsx
│   │   ├── ContentManagement/
│   │   │   ├── DatasetViewer.jsx
│   │   │   ├── ContentEditor.jsx
│   │   │   ├── UpdateScheduler.jsx
│   │   │   └── VersionControl.jsx
│   │   ├── UserInterface/
│   │   │   ├── Navigation.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── ThemeSwitcher.jsx
│   │   │   └── Notifications.jsx
│   │   └── Shared/
│   │       ├── LoadingSpinner.jsx
│   │       ├── ErrorBoundary.jsx
│   │       ├── Modal.jsx
│   │       └── Toast.jsx
│   ├── services/
│   │   ├── api.js              # API client
│   │   ├── llm.js              # LLM integration
│   │   ├── analytics.js        # Analytics service
│   │   └── auth.js             # Authentication
│   ├── store/
│   │   ├── slices/
│   │   │   ├── analysisSlice.js
│   │   │   ├── personaSlice.js
│   │   │   ├── datasetSlice.js
│   │   │   ├── userSlice.js
│   │   │   └── uiSlice.js
│   │   └── store.js
│   ├── hooks/
│   │   ├── useAnalysis.js
│   │   ├── usePersona.js
│   │   ├── useDataset.js
│   │   └── useAuth.js
│   ├── utils/
│   │   ├── formatters.js
│   │   ├── validators.js
│   │   ├── constants.js
│   │   └── helpers.js
│   ├── styles/
│   │   ├── globals.css
│   │   ├── theme.css
│   │   └── components/
│   ├── App.js
│   └── index.js
├── package.json
└── README.md
```

### **2. CORE COMPONENTS IMPLEMENTATION**

#### **Main Dashboard Component**

```jsx
// src/components/Dashboard/MainDashboard.jsx
import React, { useState, useEffect } from 'react';
import { Box, Grid, Paper, Typography, Chip } from '@mui/material';
import { 
  TrendingUp, 
  Psychology, 
  Gavel, 
  Public, 
  Security 
} from '@mui/icons-material';
import PoliticalAnalysis from './PoliticalAnalysis';
import TrendAnalysis from './TrendAnalysis';
import LiveUpdates from './LiveUpdates';
import { useAnalysis } from '../../hooks/useAnalysis';

const MainDashboard = () => {
  const { analysisHistory, loading } = useAnalysis();
  const [activeTab, setActiveTab] = useState('analysis');

  const dashboardStats = [
    {
      title: 'Analisis Politik',
      value: analysisHistory.length,
      icon: <Psychology />,
      color: 'primary'
    },
    {
      title: 'Tren Politik',
      value: '15',
      icon: <TrendingUp />,
      color: 'success'
    },
    {
      title: 'Kebijakan Terkini',
      value: '23',
      icon: <Gavel />,
      color: 'warning'
    },
    {
      title: 'Isu Internasional',
      value: '8',
      icon: <Public />,
      color: 'info'
    }
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          🤖 AI Tokoh Oposisi & Intelektual Kritis
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Platform analisis politik berbasis kecerdasan buatan dengan pendekatan kritis dan konstruktif
        </Typography>
      </Box>

      {/* Dashboard Stats */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {dashboardStats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Paper 
              elevation={3} 
              sx={{ 
                p: 3, 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'space-between',
                transition: 'transform 0.2s',
                '&:hover': { transform: 'translateY(-4px)' }
              }}
            >
              <Box>
                <Typography variant="h6" color="text.secondary">
                  {stat.title}
                </Typography>
                <Typography variant="h4" color={`${stat.color}.main`}>
                  {stat.value}
                </Typography>
              </Box>
              <Box 
                sx={{ 
                  p: 2, 
                  bgcolor: `${stat.color}.light`, 
                  borderRadius: '50%',
                  color: `${stat.color}.main`
                }}
              >
                {stat.icon}
              </Box>
            </Paper>
          </Grid>
        ))}
      </Grid>

      {/* Main Content */}
      <Grid container spacing={3}>
        <Grid item xs={12} lg={8}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              📊 Analisis Politik Terkini
            </Typography>
            <PoliticalAnalysis />
          </Paper>
          
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              📈 Trend Politik
            </Typography>
            <TrendAnalysis />
          </Paper>
        </Grid>

        <Grid item xs={12} lg={4}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              🔄 Update Terkini
            </Typography>
            <LiveUpdates />
          </Paper>
          
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              🎯 Quick Actions
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              <Chip label="Analisis Baru" color="primary" clickable />
              <Chip label="Cek Kebijakan" color="secondary" clickable />
              <Chip label="Update Dataset" variant="outlined" clickable />
              <Chip label="Export Laporan" variant="outlined" clickable />
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default MainDashboard;
```

#### **Political Analysis Component**

```jsx
// src/components/Dashboard/PoliticalAnalysis.jsx
import React, { useState } from 'react';
import { 
  TextField, 
  Button, 
  Card, 
  CardContent, 
  Typography,
  Chip,
  Box,
  LinearProgress
} from '@mui/material';
import { Send, AccessTime, CheckCircle } from '@mui/icons-material';
import { useAnalysis } from '../../hooks/useAnalysis';

const PoliticalAnalysis = () => {
  const [query, setQuery] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const { analyzeQuery, recentAnalysis } = useAnalysis();

  const handleAnalyze = async () => {
    if (!query.trim()) return;

    setIsAnalyzing(true);
    try {
      await analyzeQuery(query);
    } finally {
      setIsAnalyzing(false);
      setQuery('');
    }
  };

  const getConfidenceColor = (score) => {
    if (score >= 80) return 'success';
    if (score >= 60) return 'warning';
    return 'error';
  };

  return (
    <Box>
      {/* Query Input */}
      <Box sx={{ mb: 3 }}>
        <TextField
          fullWidth
          multiline
          rows={3}
          placeholder="Masukkan pertanyaan atau isu politik yang ingin dianalisis... 
Contoh: 'Bagaimana dampak kebijakan subsidi energi terhadap perekonomian Indonesia?'"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          variant="outlined"
          disabled={isAnalyzing}
        />
        <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
          <Button
            variant="contained"
            endIcon={<Send />}
            onClick={handleAnalyze}
            disabled={!query.trim() || isAnalyzing}
            size="large"
          >
            {isAnalyzing ? 'Menganalisis...' : 'Mulai Analisis'}
          </Button>
        </Box>
        
        {isAnalyzing && (
          <Box sx={{ mt: 2 }}>
            <LinearProgress />
            <Typography variant="caption" color="text.secondary">
              Sedang menganalisis dengan pendekatan multidimensional...
            </Typography>
          </Box>
        )}
      </Box>

      {/* Recent Analysis */}
      {recentAnalysis.length > 0 && (
        <Box>
          <Typography variant="subtitle1" gutterBottom sx={{ mb: 2 }}>
            📋 Analisis Terakhir
          </Typography>
          {recentAnalysis.slice(0, 3).map((analysis, index) => (
            <Card key={index} sx={{ mb: 2, borderLeft: 4, borderColor: 'primary.main' }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                  <Typography variant="subtitle2" color="text.secondary">
                    <AccessTime fontSize="small" /> {new Date(analysis.timestamp).toLocaleString()}
                  </Typography>
                  <Chip 
                    label={`Skor: ${analysis.confidence}%`} 
                    color={getConfidenceColor(analysis.confidence)}
                    size="small"
                  />
                </Box>
                <Typography variant="body2" sx={{ mb: 1, fontStyle: 'italic' }}>
                  "{analysis.query}"
                </Typography>
                <Typography variant="body1">
                  {analysis.response.substring(0, 150)}...
                </Typography>
                <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                  <Chip label={analysis.type} size="small" variant="outlined" />
                  <Chip label="Dr. Arjuna Wibawa" size="small" color="primary" />
                  <Chip label="Verified" size="small" color="success" icon={<CheckCircle />} />
                </Box>
              </CardContent>
            </Card>
          ))}
        </Box>
      )}
    </Box>
  );
};

export default PoliticalAnalysis;
```

#### **Persona Interaction Component**

```jsx
// src/components/Persona/Conversation.jsx
import React, { useState, useRef, useEffect } from 'react';
import { 
  Box, 
  TextField, 
  Button, 
  List, 
  ListItem, 
  Typography,
  Avatar,
  Chip,
  IconButton
} from '@mui/material';
import { Send, Psychology, Security, EmojiObjects } from '@mui/icons-material';
import { usePersona } from '../../hooks/usePersona';

const Conversation = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const { personaResponse, isResponding } = usePersona();
  const messagesEndRef = useRef(null);

  const handleSendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: message,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setMessage('');

    // Simulate AI response
    setTimeout(() => {
      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: personaResponse || "Terima kasih atas pertanyaan Anda. Sebagai tokoh oposisi, saya akan memberikan analisis kritis berdasarkan data dan prinsip demokrasi.",
        timestamp: new Date(),
        confidence: 85,
        sources: ['Dataset Politik', 'Analisis Ekonomi', 'Studi Hukum']
      };
      
      setMessages(prev => [...prev, aiMessage]);
    }, 1000);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const getPersonaAvatar = (type) => {
    if (type === 'user') return '👤';
    return '🧠'; // Dr. Arjuna Wibawa
  };

  return (
    <Box sx={{ height: '600px', display: 'flex', flexDirection: 'column' }}>
      {/* Conversation Header */}
      <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider', bgcolor: 'background.paper' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Box>
            <Typography variant="h6">🤖 Dr. Arjuna Wibawa</Typography>
            <Typography variant="caption" color="text.secondary">
              Tokoh Oposisi & Intelektual Kritis
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Chip icon={<Psychology />} label="Kritis" size="small" />
            <Chip icon={<Security />} label="Demokratis" size="small" color="success" />
            <Chip icon={<EmojiObjects />} label="Analitis" size="small" variant="outlined" />
          </Box>
        </Box>
      </Box>

      {/* Messages */}
      <Box sx={{ flex: 1, overflow: 'auto', p: 2, bgcolor: 'grey.50' }}>
        <List>
          {messages.map((msg) => (
            <ListItem 
              key={msg.id} 
              sx={{ 
                display: 'flex', 
                justifyContent: msg.type === 'user' ? 'flex-end' : 'flex-start',
                mb: 1
              }}
            >
              <Box
                sx={{
                  display: 'flex',
                  flexDirection: msg.type === 'user' ? 'row-reverse' : 'row',
                  alignItems: 'flex-start',
                  gap: 1,
                  maxWidth: '70%'
                }}
              >
                <Avatar sx={{ bgcolor: msg.type === 'user' ? 'primary.main' : 'secondary.main' }}>
                  {getPersonaAvatar(msg.type)}
                </Avatar>
                <Box>
                  <Box
                    sx={{
                      p: 1.5,
                      borderRadius: 2,
                      bgcolor: msg.type === 'user' ? 'primary.light' : 'background.paper',
                      color: msg.type === 'user' ? 'primary.contrastText' : 'text.primary',
                      boxShadow: 1
                    }}
                  >
                    <Typography variant="body2">{msg.content}</Typography>
                    {msg.type === 'ai' && (
                      <>
                        <Box sx={{ mt: 1, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                          {msg.sources.map((source, index) => (
                            <Chip key={index} label={source} size="small" variant="outlined" />
                          ))}
                        </Box>
                        <Box sx={{ mt: 1, display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Chip 
                            label={`Kepercayaan: ${msg.confidence}%`} 
                            size="small" 
                            color={msg.confidence > 70 ? 'success' : 'warning'}
                          />
                        </Box>
                      </>
                    )}
                  </Box>
                  <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5 }}>
                    {msg.timestamp.toLocaleTimeString()}
                  </Typography>
                </Box>
              </Box>
            </ListItem>
          ))}
          {isResponding && (
            <ListItem sx={{ justifyContent: 'flex-start' }}>
              <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                <Avatar>🧠</Avatar>
                <Box sx={{ p: 1, bgcolor: 'background.paper', borderRadius: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    Sedang mengetik...
                  </Typography>
                </Box>
              </Box>
            </ListItem>
          )}
          <div ref={messagesEndRef} />
        </List>
      </Box>

      {/* Input Area */}
      <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider', bgcolor: 'background.paper' }}>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Tanyakan sesuatu tentang politik, kebijakan, atau isu sosial..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            disabled={isResponding}
          />
          <Button
            variant="contained"
            endIcon={<Send />}
            onClick={handleSendMessage}
            disabled={!message.trim() || isResponding}
            size="large"
          >
            Kirim
          </Button>
        </Box>
        <Typography variant="caption" color="text.secondary" sx={{ mt: 1 }}>
          💡 Tips: Ajukan pertanyaan spesifik untuk analisis yang lebih mendalam
        </Typography>
      </Box>
    </Box>
  );
};

export default Conversation;
```

### **3. STATE MANAGEMENT (Redux Toolkit)**

```javascript
// src/store/slices/analysisSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { analyzePoliticalQuery } from '../../services/api';

const initialState = {
  analyses: [],
  loading: false,
  error: null,
  currentAnalysis: null,
  history: []
};

export const performAnalysis = createAsyncThunk(
  'analysis/perform',
  async (queryData, { rejectWithValue }) => {
    try {
      const response = await analyzePoliticalQuery(queryData);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

const analysisSlice = createSlice({
  name: 'analysis',
  initialState,
  reducers: {
    clearCurrentAnalysis: (state) => {
      state.currentAnalysis = null;
    },
    addToHistory: (state, action) => {
      state.history.unshift(action.payload);
      if (state.history.length > 50) {
        state.history.pop();
      }
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(performAnalysis.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(performAnalysis.fulfilled, (state, action) => {
        state.loading = false;
        state.currentAnalysis = action.payload;
        state.analyses.push(action.payload);
        state.history.unshift({
          ...action.payload,
          timestamp: new Date().toISOString()
        });
      })
      .addCase(performAnalysis.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  }
});

export const { clearCurrentAnalysis, addToHistory } = analysisSlice.actions;
export default analysisSlice.reducer;
```

### **4. API SERVICES**

```javascript
// src/services/api.js
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor for auth
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const politicalAnalysisAPI = {
  analyze: (queryData) => api.post('/analyze', queryData),
  getHistory: () => api.get('/analysis/history'),
  getTrends: () => api.get('/trends'),
  checkEthics: (content) => api.post('/ethics/check', { content })
};

export const personaAPI = {
  getProfile: () => api.get('/persona/profile'),
  updatePreferences: (preferences) => api.put('/persona/preferences', preferences),
  getFeedback: (analysisId) => api.get(`/persona/feedback/${analysisId}`)
};

export const datasetAPI = {
  getStatus: () => api.get('/datasets/status'),
  updateContent: (updateData) => api.post('/datasets/update', updateData),
  getVersionHistory: () => api.get('/datasets/versions')
};

export default api;
```

### **5. PACKAGE.JSON CONFIGURATION**

```json
{
  "name": "ai-oposisi-web",
  "version": "1.0.0",
  "description": "Web interface for AI Tokoh Oposisi & Intelektual Kritis",
  "private": true,
  "dependencies": {
    "@emotion/react": "^11.11.1",
    "@emotion/styled": "^11.11.0",
    "@mui/icons-material": "^5.14.11",
    "@mui/material": "^5.14.13",
    "@reduxjs/toolkit": "^1.9.7",
    "axios": "^1.6.2",
    "chart.js": "^4.4.1",
    "d3": "^7.8.5",
    "react": "^18.2.0",
    "react-chartjs-2": "^5.2.0",
    "react-dom": "^18.2.0",
    "react-redux": "^8.1.3",
    "react-router-dom": "^6.18.0",
    "recharts": "^2.8.0",
    "socket.io-client": "^4.7.4",
    "web-vitals": "^3.4.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@vitejs/plugin-react": "^4.1.1",
    "eslint": "^8.53.0",
    "eslint-plugin-react": "^7.33.2",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.4",
    "vite": "^5.0.0"
  },
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint .",
    "test": "vitest"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ],
    "plugins": ["react-hooks"]
  }
}
```

### **6. STYLING & THEMING**

```css
/* src/styles/theme.css */
:root {
  --primary-color: #1a73e8;
  --secondary-color: #34a853;
  --accent-color: #ff6d01;
  --background-color: #f8f9fa;
  --surface-color: #ffffff;
  --text-primary: #202124;
  --text-secondary: #5f6368;
  --border-color: #dadce0;
}

/* Dark theme */
[data-theme="dark"] {
  --primary-color: #4285f4;
  --secondary-color: #188038;
  --accent-color: #fbbc04;
  --background-color: #121212;
  --surface-color: #1e1e1e;
  --text-primary: #e8eaed;
  --text-secondary: #9aa0a6;
  --border-color: #3c4043;
}

/* Component-specific styles */
.political-analysis-card {
  transition: all 0.3s ease;
  border: 1px solid var(--border-color);
}

.political-analysis-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.confidence-meter {
  height: 4px;
  border-radius: 2px;
  background-color: var(--border-color);
}

.confidence-meter-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.5s ease;
}

/* Animation classes */
.fade-in {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Responsive design */
@media (max-width: 768px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  
  .analysis-sidebar {
    display: none;
  }
}
```

### **7. DEPLOYMENT CONFIGURATION**

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/socket.io': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        ws: true
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@mui/material', '@mui/icons-material'],
          state: ['@reduxjs/toolkit', 'react-redux'],
          charts: ['chart.js', 'react-chartjs-2', 'recharts']
        }
      }
    }
  }
})
```

### **8. TESTING STRATEGY**

```javascript
// src/__tests__/components/PoliticalAnalysis.test.js
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import PoliticalAnalysis from '../components/Dashboard/PoliticalAnalysis';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import analysisReducer from '../store/slices/analysisSlice';

const mockStore = configureStore({
  reducer: {
    analysis: analysisReducer
  }
});

describe('PoliticalAnalysis Component', () => {
  test('renders query input field', () => {
    render(
      <Provider store={mockStore}>
        <PoliticalAnalysis />
      </Provider>
    );
    
    expect(screen.getByPlaceholderText(/Masukkan pertanyaan/i)).toBeInTheDocument();
  });

  test('shows loading state during analysis', async () => {
    render(
      <Provider store={mockStore}>
        <PoliticalAnalysis />
      </Provider>
    );
    
    const input = screen.getByPlaceholderText(/Masukkan pertanyaan/i);
    const button = screen.getByText(/Mulai Analisis/i);
    
    fireEvent.change(input, { target: { value: 'Test query' } });
    fireEvent.click(button);
    
    expect(screen.getByText(/Menganalisis/i)).toBeInTheDocument();
  });
});
```

---

## 🎯 IMPLEMENTATION MILESTONES

### **Week 1: Foundation**
- [ ] Setup React project with TypeScript
- [ ] Configure Redux Toolkit state management
- [ ] Implement basic routing and navigation
- [ ] Create component structure and layout

### **Week 2: Core Features**
- [ ] Implement Political Analysis component
- [ ] Create Persona Interaction interface
- [ ] Build Data Visualization components
- [ ] Integrate with backend API

### **Week 3: Advanced Features**
- [ ] Implement real-time updates with WebSocket
- [ ] Add content management system
- [ ] Create analytics dashboard
- [ ] Implement user authentication

### **Week 4: Polish & Optimization**
- [ ] Add responsive design and mobile support
- [ ] Implement performance optimizations
- [ ] Add comprehensive testing
- [ ] Prepare for deployment

---

## 🚀 SUCCESS CRITERIA

### **Functional Requirements**
- ✅ **User Authentication**: Secure login and user management
- ✅ **Political Analysis**: Real-time analysis with confidence scoring
- ✅ **Persona Interaction**: Natural conversation with Dr. Arjuna Wibawa
- ✅ **Data Visualization**: Interactive charts and graphs
- ✅ **Content Management**: Easy dataset updates and versioning

### **Non-Functional Requirements**
- ✅ **Performance**: < 3 second response time
- ✅ **Scalability**: Support 1000+ concurrent users
- ✅ **Security**: OAuth2 authentication and data encryption
- ✅ **Accessibility**: WCAG 2.1 AA compliance
- ✅ **Mobile Support**: Responsive design for all devices

### **User Experience Goals**
- ✅ **Intuitive Interface**: Easy to use for non-technical users
- ✅ **Fast Interactions**: Smooth animations and transitions
- ✅ **Clear Feedback**: Informative loading states and error messages
- ✅ **Personalization**: Customizable interface and preferences

Dengan web interface ini, pengguna akan memiliki:
- 🎯 **Platform Interaktif** untuk analisis politik
- 🤖 **Interaksi Personal** dengan AI tokoh oposisi
- 📊 **Visualisasi Data** yang informatif dan menarik
- 🔒 **Keamanan & Privasi** terjamin dengan local LLM