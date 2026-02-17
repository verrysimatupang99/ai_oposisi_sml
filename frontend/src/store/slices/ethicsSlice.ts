/**
 * Ethics Slice
 * Redux state management for ethics validation
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface EthicsValidation {
  id: string;
  content: string;
  isValid: boolean;
  violations: string[];
  timestamp: string;
}

interface EthicsState {
  validations: EthicsValidation[];
  lastValidation: EthicsValidation | null;
  isEnabled: boolean;
  strictMode: boolean;
  isLoading: boolean;
  error: string | null;
}

const initialState: EthicsState = {
  validations: [],
  lastValidation: null,
  isEnabled: true,
  strictMode: true,
  isLoading: false,
  error: null,
};

const ethicsSlice = createSlice({
  name: 'ethics',
  initialState,
  reducers: {
    addValidation: (state, action: PayloadAction<EthicsValidation>) => {
      state.validations.push(action.payload);
      state.lastValidation = action.payload;
    },
    setEnabled: (state, action: PayloadAction<boolean>) => {
      state.isEnabled = action.payload;
    },
    setStrictMode: (state, action: PayloadAction<boolean>) => {
      state.strictMode = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    clearValidations: (state) => {
      state.validations = [];
      state.lastValidation = null;
    },
  },
});

export const {
  addValidation,
  setEnabled,
  setStrictMode,
  setLoading,
  setError,
  clearValidations,
} = ethicsSlice.actions;

export default ethicsSlice.reducer;
