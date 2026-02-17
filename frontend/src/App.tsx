/**
 * Main App Component - MINIMAL VERSION
 * 
 * Root component that sets up routing, layout, and global state
 * management for the AI Tokoh Oposisi & Intelektual Kritis frontend.
 * 
 * Author: AI Assistant
 * Created: 2025-01-11
 */

import React from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { Box, Typography, Container, Button } from '@mui/material';
import { Home as HomeIcon, Login as LoginIcon } from '@mui/icons-material';
import AuthPage from './pages/AuthPage';

// Temporary Home/Welcome page
const WelcomePage: React.FC = () => {
  const navigate = useNavigate();
  
  return (
    <Container maxWidth="lg">
      <Box
        display="flex"
        flexDirection="column"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
        textAlign="center"
        gap={3}
      >
        <HomeIcon sx={{ fontSize: 80, color: 'primary.main' }} />
        <Typography variant="h2" component="h1" gutterBottom>
          🎭 AI Tokoh Oposisi & Intelektual Kritis
        </Typography>
        <Typography variant="h5" color="text.secondary" gutterBottom>
          Dr. Arjuna Wibawa - Persona AI
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ maxWidth: 600 }}>
          Selamat datang di sistem AI yang mewakili tokoh oposisi konstruktif
          dan intelektual kritis Indonesia.
        </Typography>
        <Box display="flex" gap={2} mt={2}>
          <Button variant="contained" size="large" onClick={() => navigate('/chat')}>
            Mulai Chat
          </Button>
          <Button variant="outlined" size="large" onClick={() => navigate('/analysis')}>
            Analisis Politik
          </Button>
        </Box>
        <Box display="flex" gap={2} mt={2}>
          <Button 
            variant="text" 
            startIcon={<LoginIcon />}
            onClick={() => navigate('/auth')}
          >
            Masuk / Daftar
          </Button>
        </Box>
        <Box mt={4}>
          <Typography variant="caption" color="text.disabled">
            ✅ Backend: Connected | ✅ LLM: Llama 3.2 1B | ✅ Database: Ready
          </Typography>
        </Box>
      </Box>
    </Container>
  );
};

// Chat Page - No Authentication Required
const ChatPage: React.FC = () => {
  const navigate = useNavigate();
  const [message, setMessage] = React.useState('');
  const [messages, setMessages] = React.useState<{role: string, content: string}[]>([]);
  const [loading, setLoading] = React.useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;
    
    const userMessage = message;
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setMessage('');
    setLoading(true);
    
    try {
      const response = await fetch('/api/v1/chat/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: data.ai_response 
      }]);
      
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Maaf, terjadi kesalahan saat menghubungi server. Silakan coba lagi.' 
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Box display="flex" alignItems="center" gap={2} mb={3}>
        <Button variant="text" onClick={() => navigate('/')}>← Kembali</Button>
        <Typography variant="h4">💬 Chat dengan Dr. Arjuna Wibawa</Typography>
      </Box>
      
      <Box sx={{ 
        height: '60vh', 
        overflowY: 'auto', 
        bgcolor: 'background.paper', 
        borderRadius: 2, 
        p: 2, 
        mb: 2 
      }}>
        {messages.length === 0 && (
          <Typography color="text.secondary" textAlign="center" mt={10}>
            Mulai percakapan dengan Dr. Arjuna Wibawa...
          </Typography>
        )}
        {messages.map((msg, idx) => (
          <Box key={idx} sx={{ 
            mb: 2, 
            p: 2, 
            borderRadius: 2, 
            bgcolor: msg.role === 'user' ? 'primary.dark' : 'grey.800',
            maxWidth: '80%',
            ml: msg.role === 'user' ? 'auto' : 0
          }}>
            <Typography variant="caption" color="text.secondary">
              {msg.role === 'user' ? 'Anda' : 'Dr. Arjuna Wibawa'}
            </Typography>
            <Typography>{msg.content}</Typography>
          </Box>
        ))}
        {loading && <Typography color="text.secondary">Dr. Arjuna sedang mengetik...</Typography>}
      </Box>
      
      <Box display="flex" gap={2}>
        <Box 
          component="input"
          id="chat-input"
          name="chat-message"
          value={message}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setMessage(e.target.value)}
          onKeyPress={(e: React.KeyboardEvent) => e.key === 'Enter' && sendMessage()}
          placeholder="Ketik pesan Anda..."
          sx={{ 
            flex: 1, 
            p: 2, 
            borderRadius: 2, 
            border: '1px solid', 
            borderColor: 'grey.600',
            bgcolor: 'background.paper',
            color: 'text.primary',
            fontSize: '1rem'
          }}
        />
        <Button variant="contained" onClick={sendMessage} disabled={loading}>
          Kirim
        </Button>
      </Box>
    </Container>
  );
};

// Analysis Page
const AnalysisPage: React.FC = () => {
  const navigate = useNavigate();
  
  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Box display="flex" alignItems="center" gap={2} mb={3}>
        <Button variant="text" onClick={() => navigate('/')}>← Kembali</Button>
        <Typography variant="h4">📊 Analisis Politik</Typography>
      </Box>
      
      <Box sx={{ bgcolor: 'background.paper', borderRadius: 2, p: 4, textAlign: 'center' }}>
        <Typography variant="h6" gutterBottom>
          Fitur Analisis Politik
        </Typography>
        <Typography color="text.secondary" mb={3}>
          Analisis mendalam tentang situasi politik Indonesia dengan pendekatan kritis dan berbasis data.
        </Typography>
        <Typography variant="body2" color="text.disabled">
          🚧 Coming Soon - Fitur dalam pengembangan
        </Typography>
      </Box>
    </Container>
  );
};

const App: React.FC = () => {
  return (
    <div className="app">
      <Routes>
        <Route path="/" element={<WelcomePage />} />
        <Route path="/auth" element={<AuthPage />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/analysis" element={<AnalysisPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
};

export default App;