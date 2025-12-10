import React, { createContext, useContext, useState, useEffect } from 'react';
import * as SecureStore from 'expo-secure-store';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userProfile, setUserProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const token = await SecureStore.getItemAsync('authToken');
      const profile = await SecureStore.getItemAsync('userProfile');

      if (token || profile) {
        setIsAuthenticated(true);
        if (profile) {
          setUserProfile(JSON.parse(profile));
        }
      }
    } catch (error) {
      console.error('Auth check error:', error);
    } finally {
      setLoading(false);
    }
  };

  const login = async (token, profile) => {
    try {
      await SecureStore.setItemAsync('authToken', token);
      await SecureStore.setItemAsync('userProfile', JSON.stringify(profile));
      setIsAuthenticated(true);
      setUserProfile(profile);
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  const logout = async () => {
    try {
      await SecureStore.deleteItemAsync('authToken');
      await SecureStore.deleteItemAsync('userProfile');
      setIsAuthenticated(false);
      setUserProfile(null);
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const updateProfile = async (profile) => {
    try {
      await SecureStore.setItemAsync('userProfile', JSON.stringify(profile));
      setUserProfile(profile);
    } catch (error) {
      console.error('Update profile error:', error);
    }
  };

  return (
    <AuthContext.Provider value={{
      isAuthenticated,
      userProfile,
      loading,
      login,
      logout,
      updateProfile,
      checkAuth
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
