/**
 * Analysis Slice
 * Redux state management for political analysis functionality
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface AnalysisResult {
  id: string;
  query: string;
  response: string;
  timestamp: string;
  category: string;
}

interface AnalysisState {
  results: AnalysisResult[];
  currentAnalysis: AnalysisResult | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: AnalysisState = {
  results: [],
  currentAnalysis: null,
  isLoading: false,
  error: null,
};

const analysisSlice = createSlice({
  name: 'analysis',
  initialState,
  reducers: {
    addResult: (state, action: PayloadAction<AnalysisResult>) => {
      state.results.push(action.payload);
      state.currentAnalysis = action.payload;
    },
    setCurrentAnalysis: (state, action: PayloadAction<AnalysisResult | null>) => {
      state.currentAnalysis = action.payload;
    },
    clearResults: (state) => {
      state.results = [];
      state.currentAnalysis = null;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
});

export const {
  addResult,
  setCurrentAnalysis,
  clearResults,
  setLoading,
  setError,
} = analysisSlice.actions;

export default analysisSlice.reducer;
