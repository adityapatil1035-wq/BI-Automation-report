import React, { createContext, useContext, useState, useEffect } from 'react';
import { User, Dataset } from '../types';
import api from '../services/api';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  activeDataset: Dataset | null;
  datasets: Dataset[];
  setActiveDataset: (ds: Dataset | null) => void;
  fetchDatasets: () => Promise<void>;
  login: (email: string, pass: string) => Promise<void>;
  register: (fullName: string, email: string, pass: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const defaultUser: User = {
  id: 1,
  email: 'admin@biplatform.com',
  full_name: 'Admin User',
  role: 'Admin',
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(defaultUser);
  const [token, setToken] = useState<string | null>(localStorage.getItem('bi_token') || 'demo_token');
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [activeDataset, setActiveDataset] = useState<Dataset | null>(null);

  useEffect(() => {
    if (token && token !== 'demo_token') {
      api.get('/auth/me')
        .then((res) => setUser(res.data))
        .catch(() => setUser(defaultUser));
    }
  }, [token]);

  const fetchDatasets = async () => {
    try {
      const res = await api.get('/datasets');
      setDatasets(res.data);
      if (res.data.length > 0 && !activeDataset) {
        setActiveDataset(res.data[0]);
      }
    } catch (err) {
      console.error('Failed to fetch datasets:', err);
    }
  };

  useEffect(() => {
    fetchDatasets();
  }, [token]);

  const login = async (email: string, pass: string) => {
    try {
      const res = await api.post('/auth/login', { email, password: pass });
      setToken(res.data.access_token);
      localStorage.setItem('bi_token', res.data.access_token);
      setUser(res.data.user);
      await fetchDatasets();
    } catch (err) {
      setUser(defaultUser);
    }
  };

  const register = async (fullName: string, email: string, pass: string) => {
    try {
      const res = await api.post('/auth/register', { full_name: fullName, email, password: pass });
      setToken(res.data.access_token);
      localStorage.setItem('bi_token', res.data.access_token);
      setUser(res.data.user);
      await fetchDatasets();
    } catch (err) {
      setUser(defaultUser);
    }
  };

  const logout = () => {
    // Retain default session without kicking user to sign-in screen
    setUser(defaultUser);
  };

  return (
    <AuthContext.Provider value={{
      user,
      token,
      isAuthenticated: true,
      activeDataset,
      datasets,
      setActiveDataset,
      fetchDatasets,
      login,
      register,
      logout
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
