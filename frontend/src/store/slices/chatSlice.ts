/**
 * Chat Slice
 * Redux state management for chat functionality
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
}

interface ChatState {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  currentConversationId: string | null;
}

const initialState: ChatState = {
  messages: [],
  isLoading: false,
  error: null,
  currentConversationId: null,
};

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    addMessage: (state, action: PayloadAction<Message>) => {
      state.messages.push(action.payload);
    },
    setMessages: (state, action: PayloadAction<Message[]>) => {
      state.messages = action.payload;
    },
    clearMessages: (state) => {
      state.messages = [];
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    setConversationId: (state, action: PayloadAction<string | null>) => {
      state.currentConversationId = action.payload;
    },
  },
});

export const {
  addMessage,
  setMessages,
  clearMessages,
  setLoading,
  setError,
  setConversationId,
} = chatSlice.actions;

export default chatSlice.reducer;
