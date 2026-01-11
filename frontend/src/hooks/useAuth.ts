/**
 * Authentication Hook
 * 
 * Custom hook for managing authentication state and actions
 * in the AI Tokoh Oposisi & Intelektual Kritis frontend.
 * 
 * Author: AI Assistant
 * Created: 2025-01-11
 */

import { useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../store/store';
import { loginUser, logoutUser, getCurrentUser } from '../store/slices/authSlice';

export const useAuth = () => {
  const dispatch = useDispatch<AppDispatch>();
  const authState = useSelector((state: RootState) => state.auth);

  // Login function
  const login = useCallback(async (credentials: { username: string; password: string }) => {
    try {
      const result = await dispatch(loginUser(credentials)).unwrap();
      return result;
    } catch (error) {
      throw error;
    }
  }, [dispatch]);

  // Logout function
  const logout = useCallback(async () => {
    try {
      await dispatch(logoutUser()).unwrap();
    } catch (error) {
      console.error('Logout error:', error);
    }
  }, [dispatch]);

  // Get current user function
  const fetchCurrentUser = useCallback(async () => {
    try {
      const result = await dispatch(getCurrentUser()).unwrap();
      return result;
    } catch (error) {
      console.error('Fetch user error:', error);
      throw error;
    }
  }, [dispatch]);

  // Check if user has specific role
  const hasRole = useCallback((role: string) => {
    if (!authState.user) return false;
    // Add role checking logic here if needed
    return true;
  }, [authState.user]);

  // Check if user is superuser
  const isSuperuser = useCallback(() => {
    return authState.user?.is_superuser || false;
  }, [authState.user]);

  // Clear auth errors
  const clearError = useCallback(() => {
    // Dispatch clear error action if needed
  }, []);

  return {
    // State
    user: authState.user,
    isAuthenticated: authState.isAuthenticated,
    isLoading: authState.isLoading,
    error: authState.error,
    token: authState.token,

    // Actions
    login,
    logout,
    fetchCurrentUser,
    hasRole,
    isSuperuser,
    clearError,
  };
};