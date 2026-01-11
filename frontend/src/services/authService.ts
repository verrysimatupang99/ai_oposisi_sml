/**
 * Authentication Service
 * 
 * Service layer for handling authentication API calls including
 * login, registration, logout, and token management for the AI
 * Tokoh Oposisi & Intelektual Kritis frontend.
 * 
 * Author: AI Assistant
 * Created: 2025-01-11
 */

import axios, { AxiosResponse } from 'axios';
import {
  LoginCredentials,
  RegisterData,
  TokenResponse,
  User,
  PasswordChangeData,
  LoginResponse,
  RegistrationResponse,
  LogoutResponse,
  PasswordChangeResponse,
  ApiError
} from '../types/auth';

// API base URL from environment
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired, remove it and redirect to login
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication service methods
export const authService = {
  // Login user
  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    try {
      const response: AxiosResponse<TokenResponse> = await api.post('/auth/login', credentials);
      return response.data;
    } catch (error: any) {
      throw error.response?.data || { detail: 'Login failed' };
    }
  },

  // Register user
  async register(userData: RegisterData): Promise<RegistrationResponse> {
    try {
      const response: AxiosResponse<RegistrationResponse> = await api.post('/auth/register', userData);
      return response.data;
    } catch (error: any) {
      throw error.response?.data || { detail: 'Registration failed' };
    }
  },

  // Logout user
  async logout(): Promise<LogoutResponse> {
    try {
      const response: AxiosResponse<LogoutResponse> = await api.post('/auth/logout');
      return response.data;
    } catch (error: any) {
      throw error.response?.data || { detail: 'Logout failed' };
    }
  },

  // Get current user
  async getCurrentUser(): Promise<User> {
    try {
      const response: AxiosResponse<User> = await api.get('/auth/me');
      return response.data;
    } catch (error: any) {
      throw error.response?.data || { detail: 'Failed to get user' };
    }
  },

  // Refresh token
  async refreshToken(refreshToken: string): Promise<TokenResponse> {
    try {
      const response: AxiosResponse<TokenResponse> = await api.post('/auth/refresh', {
        refresh_token: refreshToken
      });
      return response.data;
    } catch (error: any) {
      throw error.response?.data || { detail: 'Token refresh failed' };
    }
  },

  // Change password
  async changePassword(passwordData: PasswordChangeData): Promise<PasswordChangeResponse> {
    try {
      const response: AxiosResponse<PasswordChangeResponse> = await api.put('/auth/change-password', passwordData);
      return response.data;
    } catch (error: any) {
      throw error.response?.data || { detail: 'Password change failed' };
    }
  },

  // Validate token
  async validateToken(token: string): Promise<boolean> {
    try {
      const response = await api.get('/auth/validate-token', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      return response.status === 200;
    } catch (error) {
      return false;
    }
  }
};

// Utility functions
export const authUtils = {
  // Check if user is authenticated
  isAuthenticated(): boolean {
    const token = localStorage.getItem('accessToken');
    return !!token;
  },

  // Get current token
  getToken(): string | null {
    return localStorage.getItem('accessToken');
  },

  // Get refresh token
  getRefreshToken(): string | null {
    return localStorage.getItem('refreshToken');
  },

  // Clear all auth data
  clearAuth(): void {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  },

  // Set auth tokens
  setTokens(accessToken: string, refreshToken: string): void {
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
  }
};

export default authService;