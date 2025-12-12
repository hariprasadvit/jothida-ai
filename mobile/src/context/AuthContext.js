import React, { createContext, useContext, useState, useEffect } from 'react';
import { Platform } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import AsyncStorage from '@react-native-async-storage/async-storage';

const AuthContext = createContext(null);

// Storage helper that works on both web and native
const storage = {
  getItem: async (key) => {
    if (Platform.OS === 'web') {
      return AsyncStorage.getItem(key);
    }
    return SecureStore.getItemAsync(key);
  },
  setItem: async (key, value) => {
    if (Platform.OS === 'web') {
      return AsyncStorage.setItem(key, value);
    }
    return SecureStore.setItemAsync(key, value);
  },
  deleteItem: async (key) => {
    if (Platform.OS === 'web') {
      return AsyncStorage.removeItem(key);
    }
    return SecureStore.deleteItemAsync(key);
  },
};

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userProfile, setUserProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const token = await storage.getItem('authToken');
      const profile = await storage.getItem('userProfile');

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
      await storage.setItem('authToken', token);
      await storage.setItem('userProfile', JSON.stringify(profile));
      setIsAuthenticated(true);
      setUserProfile(profile);
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  const logout = async () => {
    try {
      // First update state to trigger UI change immediately
      setIsAuthenticated(false);
      setUserProfile(null);

      // Then clear storage (non-blocking for UI)
      await storage.deleteItem('authToken');
      await storage.deleteItem('userProfile');

      console.log('Logout successful - storage cleared');
    } catch (error) {
      console.error('Logout error:', error);
      // Even if storage fails, keep the user logged out in UI
      // They will need to re-login on app restart anyway
    }
  };

  const updateProfile = async (profile) => {
    try {
      await storage.setItem('userProfile', JSON.stringify(profile));
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
