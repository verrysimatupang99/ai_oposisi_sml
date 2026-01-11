/**
 * Main Application Entry Point - MINIMAL VERSION
 * 
 * This file contains the main React application setup with Redux store,
 * routing configuration, and theme provider for the AI Tokoh Oposisi
 * & Intelektual Kritis frontend.
 * 
 * Author: AI Assistant
 * Created: 2025-01-11
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';

// Import store and theme
import { store } from './store/store';
import { theme } from './styles/theme';

// Import main app component
import App from './App';

// Import global styles
import './styles/globals.css';

// Create root element
const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

// Render application
root.render(
  <React.StrictMode>
    <Provider store={store}>
      <BrowserRouter>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <App />
        </ThemeProvider>
      </BrowserRouter>
    </Provider>
  </React.StrictMode>
);

export default root;