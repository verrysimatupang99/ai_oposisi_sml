/**
 * Auth Page - Login & Register
 * 
 * Combined authentication page with login and register forms
 * for AI Tokoh Oposisi & Intelektual Kritis
 */

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  Paper,
  Tabs,
  Tab,
  Alert,
  CircularProgress,
} from '@mui/material';
import { Person as PersonIcon } from '@mui/icons-material';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div hidden={value !== index} {...other}>
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );
}

const AuthPage: React.FC = () => {
  const navigate = useNavigate();
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Login form state
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPassword, setLoginPassword] = useState('');

  // Register form state
  const [regUsername, setRegUsername] = useState('');
  const [regEmail, setRegEmail] = useState('');
  const [regPassword, setRegPassword] = useState('');
  const [regConfirmPassword, setRegConfirmPassword] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      // OAuth2 expects form data with 'username' and 'password' fields
      const formData = new URLSearchParams();
      formData.append('username', loginEmail); // Email used as username
      formData.append('password', loginPassword);

      const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData.toString(),
      });

      const data = await response.json();

      if (!response.ok) {
        // Handle different error formats
        if (typeof data.detail === 'string') {
          throw new Error(data.detail);
        } else if (Array.isArray(data.detail)) {
          const messages = data.detail.map((err: any) => err.msg || JSON.stringify(err)).join(', ');
          throw new Error(messages);
        }
        throw new Error('Login gagal');
      }

      // Save tokens
      localStorage.setItem('accessToken', data.access_token);
      localStorage.setItem('refreshToken', data.refresh_token);
      
      setSuccess('Login berhasil! Mengalihkan...');
      setTimeout(() => navigate('/chat'), 1000);
    } catch (err: any) {
      setError(err.message || 'Login gagal');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (regPassword !== regConfirmPassword) {
      setError('Password tidak cocok');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: regUsername,
          email: regEmail,
          password: regPassword,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        // Handle validation errors from FastAPI
        if (data.detail && Array.isArray(data.detail)) {
          const messages = data.detail.map((err: any) => err.msg || err.message).join(', ');
          throw new Error(messages);
        }
        throw new Error(data.detail || 'Registrasi gagal');
      }

      setSuccess('Registrasi berhasil! Silakan login.');
      setTabValue(0); // Switch to login tab
      setRegUsername('');
      setRegEmail('');
      setRegPassword('');
      setRegConfirmPassword('');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ py: 8 }}>
      <Box textAlign="center" mb={4}>
        <PersonIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
        <Typography variant="h4" gutterBottom>
          🎭 AI Tokoh Oposisi
        </Typography>
        <Typography color="text.secondary">
          Masuk atau daftar untuk mengakses fitur lengkap
        </Typography>
      </Box>

      <Paper elevation={3} sx={{ p: 4, borderRadius: 3 }}>
        <Tabs
          value={tabValue}
          onChange={(_, newValue) => {
            setTabValue(newValue);
            setError(null);
            setSuccess(null);
          }}
          centered
          sx={{ mb: 2 }}
        >
          <Tab label="Masuk" />
          <Tab label="Daftar" />
        </Tabs>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {success && (
          <Alert severity="success" sx={{ mb: 2 }}>
            {success}
          </Alert>
        )}

        {/* Login Tab */}
        <TabPanel value={tabValue} index={0}>
          <form onSubmit={handleLogin}>
            <TextField
              fullWidth
              label="Username"
              value={loginEmail}
              onChange={(e) => setLoginEmail(e.target.value)}
              margin="normal"
              required
              autoComplete="username"
            />
            <TextField
              fullWidth
              label="Password"
              type="password"
              value={loginPassword}
              onChange={(e) => setLoginPassword(e.target.value)}
              margin="normal"
              required
              autoComplete="current-password"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={loading}
              sx={{ mt: 3 }}
            >
              {loading ? <CircularProgress size={24} /> : 'Masuk'}
            </Button>
          </form>
        </TabPanel>

        {/* Register Tab */}
        <TabPanel value={tabValue} index={1}>
          <form onSubmit={handleRegister}>
            <TextField
              fullWidth
              label="Username"
              value={regUsername}
              onChange={(e) => setRegUsername(e.target.value)}
              margin="normal"
              required
              autoComplete="username"
            />
            <TextField
              fullWidth
              label="Email"
              type="email"
              value={regEmail}
              onChange={(e) => setRegEmail(e.target.value)}
              margin="normal"
              required
              autoComplete="email"
            />
            <TextField
              fullWidth
              label="Password"
              type="password"
              value={regPassword}
              onChange={(e) => setRegPassword(e.target.value)}
              margin="normal"
              required
              autoComplete="new-password"
              helperText="Min 8 karakter, harus ada huruf besar, huruf kecil, angka, dan simbol (!@#$%)"
            />
            <TextField
              fullWidth
              label="Konfirmasi Password"
              type="password"
              value={regConfirmPassword}
              onChange={(e) => setRegConfirmPassword(e.target.value)}
              margin="normal"
              required
              autoComplete="new-password"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={loading}
              sx={{ mt: 3 }}
            >
              {loading ? <CircularProgress size={24} /> : 'Daftar'}
            </Button>
          </form>
        </TabPanel>

        <Box textAlign="center" mt={3}>
          <Button variant="text" onClick={() => navigate('/')}>
            ← Kembali ke Beranda
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default AuthPage;
