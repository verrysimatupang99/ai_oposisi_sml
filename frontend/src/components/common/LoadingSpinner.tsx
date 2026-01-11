/**
 * Loading Spinner Component
 * 
 * Reusable loading spinner component with different sizes and styles
 * for the AI Tokoh Oposisi & Intelektual Kritis frontend.
 * 
 * Author: AI Assistant
 * Created: 2025-01-11
 */

import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';

interface LoadingSpinnerProps {
  size?: 'small' | 'medium' | 'large';
  text?: string;
  fullScreen?: boolean;
  center?: boolean;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'medium',
  text,
  fullScreen = false,
  center = true
}) => {
  // Size mapping
  const sizeMap = {
    small: 20,
    medium: 40,
    large: 60
  };

  const spinnerSize = sizeMap[size];

  const content = (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      gap={2}
    >
      <CircularProgress 
        size={spinnerSize}
        thickness={4}
        sx={{
          color: 'primary.main',
        }}
      />
      {text && (
        <Typography 
          variant="body2" 
          color="text.secondary"
          sx={{
            fontWeight: 500,
            opacity: 0.8
          }}
        >
          {text}
        </Typography>
      )}
    </Box>
  );

  if (fullScreen) {
    return (
      <Box
        position="fixed"
        top={0}
        left={0}
        right={0}
        bottom={0}
        display="flex"
        alignItems="center"
        justifyContent="center"
        bgcolor="rgba(255, 255, 255, 0.8)"
        zIndex={9999}
      >
        {content}
      </Box>
    );
  }

  if (center) {
    return (
      <Box
        display="flex"
        alignItems="center"
        justifyContent="center"
        minHeight="200px"
        width="100%"
      >
        {content}
      </Box>
    );
  }

  return content;
};

export default LoadingSpinner;