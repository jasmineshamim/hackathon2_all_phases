// Authentication utilities
export const authService = {
  setToken: (token: string) => {
    localStorage.setItem('auth_token', token);
  },

  getToken: (): string | null => {
    return localStorage.getItem('auth_token');
  },

  removeToken: () => {
    localStorage.removeItem('auth_token');
  },

  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('auth_token');
  },

  logout: () => {
    localStorage.removeItem('auth_token');
    window.location.href = '/login';
  },
};

export default authService;
