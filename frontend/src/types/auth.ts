/**
 * Authentication Types
 * 
 * TypeScript type definitions for authentication-related data
 * structures in the AI Tokoh Oposisi & Intelektual Kritis frontend.
 * 
 * Author: AI Assistant
 * Created: 2025-01-11
 */

import { UUID } from 'crypto';

// User types
export interface User {
  id: UUID;
  username: string;
  email: string;
  full_name: string | null;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
}

// Authentication state
export interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

// Login credentials
export interface LoginCredentials {
  username: string;
  password: string;
}

// Registration data
export interface RegisterData {
  username: string;
  email: string;
  full_name?: string;
  password: string;
}

// Token response
export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

// Password change data
export interface PasswordChangeData {
  current_password: string;
  new_password: string;
}

// Login response
export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

// Registration response
export interface RegistrationResponse {
  message: string;
  user: User;
}

// Logout response
export interface LogoutResponse {
  message: string;
}

// Password change response
export interface PasswordChangeResponse {
  message: string;
}

// API error response
export interface ApiError {
  detail: string;
  status_code?: number;
  errors?: ValidationError[];
}

// Validation error
export interface ValidationError {
  field: string;
  message: string;
}

// JWT payload
export interface JWTPayload {
  sub: string; // user id
  username: string;
  exp: number;
  type?: string; // "access" or "refresh"
}