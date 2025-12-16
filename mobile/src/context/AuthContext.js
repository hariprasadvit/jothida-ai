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

// Generate unique ID for profiles
const generateProfileId = () => {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
};

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userProfile, setUserProfile] = useState(null); // Currently selected profile
  const [allProfiles, setAllProfiles] = useState([]); // All saved profiles
  const [selectedProfileId, setSelectedProfileId] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const token = await storage.getItem('authToken');
      const profilesJson = await storage.getItem('allProfiles');
      const selectedId = await storage.getItem('selectedProfileId');

      // Migration: Check for old single profile format
      const oldProfile = await storage.getItem('userProfile');

      if (token || profilesJson || oldProfile) {
        setIsAuthenticated(true);

        let profiles = [];

        if (profilesJson) {
          profiles = JSON.parse(profilesJson);
        } else if (oldProfile) {
          // Migrate old single profile to new multi-profile format
          const migrated = JSON.parse(oldProfile);
          migrated.id = migrated.id || generateProfileId();
          migrated.isPrimary = true;
          profiles = [migrated];
          // Save migrated profiles
          await storage.setItem('allProfiles', JSON.stringify(profiles));
          await storage.setItem('selectedProfileId', migrated.id);
          // Clean up old format
          await storage.deleteItem('userProfile');
        }

        setAllProfiles(profiles);

        // Set selected profile
        if (profiles.length > 0) {
          const selectedProfile = selectedId
            ? profiles.find(p => p.id === selectedId) || profiles[0]
            : profiles[0];
          setSelectedProfileId(selectedProfile.id);
          setUserProfile(selectedProfile);
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
      // Add ID to profile if not present
      const newProfile = {
        ...profile,
        id: profile.id || generateProfileId(),
        isPrimary: true,
        createdAt: new Date().toISOString(),
      };

      await storage.setItem('authToken', token);
      await storage.setItem('allProfiles', JSON.stringify([newProfile]));
      await storage.setItem('selectedProfileId', newProfile.id);

      setIsAuthenticated(true);
      setAllProfiles([newProfile]);
      setSelectedProfileId(newProfile.id);
      setUserProfile(newProfile);
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  const logout = async () => {
    try {
      // First update state to trigger UI change immediately
      setIsAuthenticated(false);
      setUserProfile(null);
      setAllProfiles([]);
      setSelectedProfileId(null);

      // Then clear storage (non-blocking for UI)
      await storage.deleteItem('authToken');
      await storage.deleteItem('allProfiles');
      await storage.deleteItem('selectedProfileId');
      await storage.deleteItem('userProfile'); // Clean up old format if exists

      console.log('Logout successful - storage cleared');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  // Update currently selected profile
  const updateProfile = async (profile) => {
    try {
      const updatedProfiles = allProfiles.map(p =>
        p.id === selectedProfileId ? { ...profile, id: selectedProfileId } : p
      );

      await storage.setItem('allProfiles', JSON.stringify(updatedProfiles));
      setAllProfiles(updatedProfiles);
      setUserProfile({ ...profile, id: selectedProfileId });
    } catch (error) {
      console.error('Update profile error:', error);
    }
  };

  // Add a new profile (family member, friend, etc.)
  const addProfile = async (profile) => {
    try {
      const newProfile = {
        ...profile,
        id: generateProfileId(),
        isPrimary: false,
        createdAt: new Date().toISOString(),
      };

      const updatedProfiles = [...allProfiles, newProfile];
      await storage.setItem('allProfiles', JSON.stringify(updatedProfiles));
      setAllProfiles(updatedProfiles);

      return newProfile;
    } catch (error) {
      console.error('Add profile error:', error);
      throw error;
    }
  };

  // Switch to a different profile
  const switchProfile = async (profileId) => {
    try {
      const profile = allProfiles.find(p => p.id === profileId);
      if (profile) {
        await storage.setItem('selectedProfileId', profileId);
        setSelectedProfileId(profileId);
        setUserProfile(profile);
        return profile;
      }
    } catch (error) {
      console.error('Switch profile error:', error);
    }
  };

  // Delete a profile (cannot delete primary profile if it's the only one)
  const deleteProfile = async (profileId) => {
    try {
      const profileToDelete = allProfiles.find(p => p.id === profileId);

      // Prevent deleting the only profile or primary profile
      if (allProfiles.length === 1) {
        throw new Error('Cannot delete the only profile');
      }

      const updatedProfiles = allProfiles.filter(p => p.id !== profileId);
      await storage.setItem('allProfiles', JSON.stringify(updatedProfiles));
      setAllProfiles(updatedProfiles);

      // If we deleted the currently selected profile, switch to another one
      if (selectedProfileId === profileId) {
        const newSelected = updatedProfiles.find(p => p.isPrimary) || updatedProfiles[0];
        await switchProfile(newSelected.id);
      }

      return true;
    } catch (error) {
      console.error('Delete profile error:', error);
      throw error;
    }
  };

  // Get profile count
  const getProfileCount = () => allProfiles.length;

  return (
    <AuthContext.Provider value={{
      isAuthenticated,
      userProfile,
      allProfiles,
      selectedProfileId,
      loading,
      login,
      logout,
      updateProfile,
      addProfile,
      switchProfile,
      deleteProfile,
      getProfileCount,
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
