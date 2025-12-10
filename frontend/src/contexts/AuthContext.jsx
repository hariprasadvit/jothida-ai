/**
 * Auth Context - Manages authentication state
 */

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check auth status on mount
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      setLoading(true);
      const userData = await authAPI.getCurrentUser();
      if (userData) {
        setUser(userData);
        setIsAuthenticated(true);
      } else {
        setUser(null);
        setIsAuthenticated(false);
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      setUser(null);
      setIsAuthenticated(false);
    } finally {
      setLoading(false);
    }
  };

  const loginWithGoogle = useCallback(async () => {
    try {
      const { auth_url } = await authAPI.getGoogleLoginUrl();
      // Redirect to Google OAuth
      window.location.href = auth_url;
    } catch (error) {
      console.error('Google login failed:', error);
      throw error;
    }
  }, []);

  const handleAuthCallback = useCallback(async (token, isNewUser) => {
    if (token) {
      localStorage.setItem('authToken', token);
      await checkAuth();
      return { success: true, isNewUser: isNewUser === 'true' };
    }
    return { success: false };
  }, []);

  const logout = useCallback(async () => {
    try {
      await authAPI.logout();
      setUser(null);
      setIsAuthenticated(false);
      // Clear local storage
      localStorage.removeItem('authToken');
      localStorage.removeItem('userProfile');
      localStorage.removeItem('onboardingComplete');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  }, []);

  const updateAstroProfile = useCallback(async (profileData) => {
    try {
      const result = await authAPI.createAstroProfile(profileData);
      // Refresh user data
      await checkAuth();
      return result;
    } catch (error) {
      console.error('Profile update failed:', error);
      throw error;
    }
  }, []);

  // Get user profile for astrology calculations
  const getUserProfile = useCallback(() => {
    if (user?.astro_profile) {
      return {
        name: user.name,
        birthDate: user.astro_profile.birth_date,
        birthTime: user.astro_profile.birth_time,
        birthPlace: user.astro_profile.birth_place,
        rasi: user.astro_profile.rasi_tamil || user.astro_profile.rasi,
        nakshatra: user.astro_profile.nakshatra_tamil || user.astro_profile.nakshatra,
        gender: user.gender
      };
    }
    // Fallback to localStorage for non-authenticated users
    const stored = localStorage.getItem('userProfile');
    return stored ? JSON.parse(stored) : null;
  }, [user]);

  const value = {
    user,
    loading,
    isAuthenticated,
    loginWithGoogle,
    handleAuthCallback,
    logout,
    updateAstroProfile,
    getUserProfile,
    checkAuth,
    hasAstroProfile: user?.has_astro_profile || false
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export default AuthContext;
