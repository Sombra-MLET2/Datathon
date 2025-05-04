import React, { createContext, useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      const userEmail = localStorage.getItem('userEmail');
      setUser({ email: userEmail });
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      const response = await axios.post('/api/sessions/api-token', {
        email,
        password
      });
      
      const { access_token } = response.data;
      
      localStorage.setItem('token', access_token);
      localStorage.setItem('userEmail', email);
      
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      setUser({ email });
      return { success: true };
    } catch (error) {
      console.error('Login error:', error);
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Login failed. Please check your credentials.'
      };
    }
  };

  const register = async (email, password) => {
    try {
      await axios.post('/api/sessions/', {
        email,
        password
      });
      return { success: true };
    } catch (error) {
      console.error('Registration error:', error);
      return { 
        success: false, 
        message: error.response?.data?.message || 'Registration failed. Please try again.'
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userEmail');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
    navigate('/login');
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  return useContext(AuthContext);
};
