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
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box, Typography, Container, Button } from '@mui/material';
import { Home as HomeIcon } from '@mui/icons-material';

// Temporary Home/Welcome page
const WelcomePage: React.FC = () => {
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
          <Button variant="contained" size="large">
            Mulai Chat
          </Button>
          <Button variant="outlined" size="large">
            Analisis Politik
          </Button>
        </Box>
        <Box mt={4}>
          <Typography variant="caption" color="text.disabled">
            ✅ Backend: Connected | ✅ LLM: Llama 3 8B | ✅ Database: Ready
          </Typography>
        </Box>
      </Box>
    </Container>
  );
};

const App: React.FC = () => {
  return (
    <div className="app">
      <Routes>
        <Route path="/" element={<WelcomePage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
};

export default App;