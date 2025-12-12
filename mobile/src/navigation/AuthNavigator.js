import React, { useState, useEffect } from 'react';
import { Platform } from 'react-native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import * as SecureStore from 'expo-secure-store';
import AsyncStorage from '@react-native-async-storage/async-storage';

import SplashScreen from '../screens/SplashScreen';
import LanguageSelectionScreen from '../screens/LanguageSelectionScreen';
import OnboardingScreen from '../screens/OnboardingScreen';
import LoginScreen from '../screens/LoginScreen';
import RegisterScreen from '../screens/RegisterScreen';

const Stack = createNativeStackNavigator();

// Storage helper for web compatibility
const getStorageItem = async (key) => {
  if (Platform.OS === 'web') {
    return AsyncStorage.getItem(key);
  }
  return SecureStore.getItemAsync(key);
};

export default function AuthNavigator() {
  const [showSplash, setShowSplash] = useState(true);
  const [showLanguageSelection, setShowLanguageSelection] = useState(false);
  const [hasSeenOnboarding, setHasSeenOnboarding] = useState(null);
  const [hasSelectedLanguage, setHasSelectedLanguage] = useState(null);

  useEffect(() => {
    checkInitialStatus();
  }, []);

  const checkInitialStatus = async () => {
    try {
      // Check if user has already selected a language
      const languageSelected = await AsyncStorage.getItem('languageSelected');
      setHasSelectedLanguage(languageSelected === 'true');

      // Check onboarding status
      const onboardingStatus = await getStorageItem('onboardingComplete');
      setHasSeenOnboarding(onboardingStatus === 'true');
    } catch (error) {
      console.error('Error checking initial status:', error);
      setHasSelectedLanguage(false);
      setHasSeenOnboarding(false);
    }
  };

  const handleSplashFinish = () => {
    setShowSplash(false);
    // Show language selection if not selected before
    if (!hasSelectedLanguage) {
      setShowLanguageSelection(true);
    }
  };

  const handleLanguageSelected = async () => {
    try {
      await AsyncStorage.setItem('languageSelected', 'true');
      setHasSelectedLanguage(true);
      setShowLanguageSelection(false);
    } catch (error) {
      console.error('Error saving language selection:', error);
      setShowLanguageSelection(false);
    }
  };

  // Show splash screen first
  if (showSplash) {
    return <SplashScreen onFinish={handleSplashFinish} />;
  }

  // Show language selection if needed
  if (showLanguageSelection || (hasSelectedLanguage === false && !showSplash)) {
    return <LanguageSelectionScreen onLanguageSelected={handleLanguageSelected} />;
  }

  // Wait for status checks
  if (hasSeenOnboarding === null || hasSelectedLanguage === null) {
    return null;
  }

  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: false,
        animation: 'fade',
      }}
      initialRouteName={hasSeenOnboarding ? 'Login' : 'Onboarding'}
    >
      <Stack.Screen name="Onboarding" component={OnboardingScreen} />
      <Stack.Screen name="Login" component={LoginScreen} />
      <Stack.Screen name="Register" component={RegisterScreen} />
    </Stack.Navigator>
  );
}
