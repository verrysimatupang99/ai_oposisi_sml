/**
 * Persona Slice
 * Redux state management for Dr. Arjuna Wibawa persona
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface PersonaProfile {
  name: string;
  description: string;
  communicationStyle: string;
  values: string[];
}

interface PersonaState {
  profile: PersonaProfile;
  isLoading: boolean;
  error: string | null;
}

const initialState: PersonaState = {
  profile: {
    name: 'Dr. Arjuna Wibawa',
    description: 'Intelektual kritis dan tokoh oposisi virtual',
    communicationStyle: 'formal',
    values: ['demokrasi', 'keadilan', 'transparansi', 'akuntabilitas'],
  },
  isLoading: false,
  error: null,
};

const personaSlice = createSlice({
  name: 'persona',
  initialState,
  reducers: {
    setProfile: (state, action: PayloadAction<PersonaProfile>) => {
      state.profile = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
});

export const { setProfile, setLoading, setError } = personaSlice.actions;

export default personaSlice.reducer;
