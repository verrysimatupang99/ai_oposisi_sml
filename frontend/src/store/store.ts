/**
 * Redux Store Configuration
 * 
 * This file configures the Redux store with all slices, middleware,
 * and development tools for the AI Tokoh Oposisi & Intelektual Kritis
 * frontend application.
 * 
 * Author: AI Assistant
 * Created: 2025-01-11
 */

import { configureStore } from '@reduxjs/toolkit';
import { combineReducers } from '@reduxjs/toolkit';
import {
  persistStore,
  persistReducer,
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER,
} from 'redux-persist';
import storage from 'redux-persist/lib/storage';

// Import slices
import authSlice from './slices/authSlice';
import chatSlice from './slices/chatSlice';
import analysisSlice from './slices/analysisSlice';
import personaSlice from './slices/personaSlice';
import ethicsSlice from './slices/ethicsSlice';
import uiSlice from './slices/uiSlice';

// Combine reducers
const rootReducer = combineReducers({
  auth: authSlice,
  chat: chatSlice,
  analysis: analysisSlice,
  persona: personaSlice,
  ethics: ethicsSlice,
  ui: uiSlice,
});

// Persist configuration
const persistConfig = {
  key: 'root',
  version: 1,
  storage,
  whitelist: ['auth', 'ui'], // Only persist auth and UI state
  blacklist: ['chat', 'analysis', 'persona', 'ethics'], // Don't persist these
};

// Create persisted reducer
const persistedReducer = persistReducer(persistConfig, rootReducer);

// Configure store
export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    }),
  devTools: process.env.NODE_ENV !== 'production',
});

// Create persistor
export const persistor = persistStore(store);

// Export types
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export default store;