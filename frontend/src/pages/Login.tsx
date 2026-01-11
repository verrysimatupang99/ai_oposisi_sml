/**
 * Login Page
 * 
 * Login page component for user authentication in the AI
 * Tokoh Oposisi & Intelektual Kritis frontend.
 * 
 * Author: AI Assistant
 * Created: 2025-01-11
 */

import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import {
  Box,
  Button,
  Container,
  TextField,
  Typography,
  Paper,
  Alert,
  InputAdornment,
  IconButton
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { useForm } from 'react-hook-form';
import { toast } from 'react-hot-toast';

// Import hooks and services
import { useAuth } from '../hooks/useAuth';
import { LoginCredentials } from '../types/auth';

// Import styles
import '../styles/pages/Login.css';

const Login: React.FC = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();
  const { loginUser, isLoading } = useAuth();

  const [showPassword, setShowPassword] = useState(false);

  // React Hook Form setup
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<LoginCredentials>();

  // Handle form submission
  const onSubmit = async (data: LoginCredentials) => {
    try {
      await loginUser(data);
      toast.success('Login successful!');
      
      // Redirect to intended page or dashboard
      const from = location.state?.from?.pathname || '/dashboard';
      navigate(from, { replace: true });
    } catch (error: any) {
      toast.error(error.detail || 'Login failed. Please check your credentials.');
    }
  };

  // Handle Google OAuth login
  const handleGoogleLogin = () => {
    // TODO: Implement Google OAuth
    toast.error('Google OAuth not implemented yet.');
  };

  return (
    <Box className="login-page">
      <Container maxWidth="sm">
        <Paper className="login-container" elevation={3}>
          <Box className="login-header">
            <Typography variant="h4" component="h1" className="login-title">
              🤖 AI Tokoh Oposisi
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              Masuk ke akun Anda
            </Typography>
          </Box>

          <form onSubmit={handleSubmit(onSubmit)} className="login-form">
            <TextField
              fullWidth
              label="Username"
              variant="outlined"
              margin="normal"
              {...register('username', {
                required: 'Username is required',
                minLength: {
                  value: 3,
                  message: 'Username must be at least 3 characters'
                }
              })}
              error={!!errors.username}
              helperText={errors.username?.message}
              disabled={isLoading}
            />

            <TextField
              fullWidth
              label="Password"
              type={showPassword ? 'text' : 'password'}
              variant="outlined"
              margin="normal"
              {...register('password', {
                required: 'Password is required',
                minLength: {
                  value: 8,
                  message: 'Password must be at least 8 characters'
                }
              })}
              error={!!errors.password}
              helperText={errors.password?.message}
              disabled={isLoading}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      onClick={() => setShowPassword(!showPassword)}
                      edge="end"
                      disabled={isLoading}
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={isLoading}
              className="login-button"
            >
              {isLoading ? 'Signing In...' : 'Sign In'}
            </Button>

            {/* Google OAuth Button */}
            <Button
              fullWidth
              variant="outlined"
              size="large"
              onClick={handleGoogleLogin}
              disabled={isLoading}
              startIcon={<i className="fab fa-google"></i>}
              sx={{ mt: 2 }}
            >
              Sign in with Google
            </Button>
          </form>

          {/* Error Display */}
          {location.state?.error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {location.state.error}
            </Alert>
          )}

          {/* Registration Link */}
          <Box className="login-footer">
            <Typography variant="body2" color="text.secondary">
              Belum punya akun?{' '}
              <Link to="/register" className="login-link">
                Daftar di sini
              </Link>
            </Typography>
          </Box>

          {/* Demo Account Info */}
          <Box className="demo-info">
            <Typography variant="caption" color="text.secondary">
              💡 Untuk demo: Gunakan username "demo" dan password "Demo123!"
            </Typography>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
};

export default Login;