import axios, { AxiosInstance, AxiosError } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Chat API
export const chatAPI = {
  sendMessage: async (message: string, conversationId?: string) => {
    const response = await apiClient.post('/chat', {
      message,
      conversation_id: conversationId,
    });
    return response.data;
  },

  getConversations: async (limit = 20, offset = 0) => {
    const response = await apiClient.get('/chat/conversations', {
      params: { limit, offset },
    });
    return response.data;
  },

  getConversationMessages: async (conversationId: string, limit = 50, offset = 0) => {
    const response = await apiClient.get(`/chat/conversations/${conversationId}/messages`, {
      params: { limit, offset },
    });
    return response.data;
  },
};

// Todo API
export const todoAPI = {
  getTodos: async (status?: string, priority?: string) => {
    const response = await apiClient.get('/todos', {
      params: { status, priority },
    });
    return response.data;
  },

  createTodo: async (data: {
    title: string;
    description?: string;
    priority?: string;
    due_date?: string;
  }) => {
    const response = await apiClient.post('/todos', data);
    return response.data;
  },

  updateTodo: async (
    todoId: number,
    data: {
      title?: string;
      description?: string;
      status?: string;
      priority?: string;
      due_date?: string;
    }
  ) => {
    const response = await apiClient.put(`/todos/${todoId}`, data);
    return response.data;
  },

  deleteTodo: async (todoId: number) => {
    const response = await apiClient.delete(`/todos/${todoId}`);
    return response.data;
  },

  toggleTodoStatus: async (todoId: number) => {
    const response = await apiClient.put(`/todos/${todoId}/toggle-status`);
    return response.data;
  },
};

export default apiClient;
