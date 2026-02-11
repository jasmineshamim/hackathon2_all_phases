"""TypeScript type definitions for API responses."""

// Common response types
export interface APIResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: APIError;
}

export interface APIError {
  code: string;
  message: string;
  details?: Record<string, any>;
}

// Todo types
export interface Todo {
  id: number;
  title: string;
  description?: string;
  status: 'pending' | 'completed';
  priority: 'low' | 'medium' | 'high';
  due_date?: string;
  created_at: string;
  updated_at: string;
}

export interface TodoCreateRequest {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';
  due_date?: string;
}

export interface TodoUpdateRequest {
  title?: string;
  description?: string;
  status?: 'pending' | 'completed';
  priority?: 'low' | 'medium' | 'high';
  due_date?: string;
}

export interface TodoListResponse {
  todos: Todo[];
  total: number;
}

// Chat types
export interface ChatMessageRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatMessageResponse {
  response: string;
  conversation_id: string;
  next_action?: {
    type: string;
    payload: Record<string, any>;
  };
}

// Conversation types
export interface Conversation {
  id: string;
  title?: string;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface ConversationListResponse {
  conversations: Conversation[];
  total: number;
}

export interface MessageListResponse {
  messages: Message[];
}

// User types
export interface User {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// Auth types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface RegisterRequest {
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
}

// Health check types
export interface HealthCheckResponse {
  status: 'healthy' | 'unhealthy';
  timestamp: string;
  version: string;
  service: string;
  environment?: string;
}

export interface DatabaseHealthResponse {
  status: 'healthy' | 'unhealthy';
  database: 'connected' | 'disconnected';
  timestamp: string;
  error?: string;
}
