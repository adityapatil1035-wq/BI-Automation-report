import axios from 'axios';

const API_BASE = (import.meta as any).env?.VITE_API_URL || (import.meta as any).env?.BACKEND_URL || '/api/v1';

export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to attach JWT bearer token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('bi_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
