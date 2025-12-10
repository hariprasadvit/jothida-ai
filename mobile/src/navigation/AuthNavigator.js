import React, { useState, useEffect } from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import * as SecureStore from 'expo-secure-store';

import SplashScreen from '../screens/SplashScreen';
import OnboardingScreen from '../screens/OnboardingScreen';
import LoginScreen from '../screens/LoginScreen';
import RegisterScreen from '../screens/RegisterScreen';

const Stack = createNativeStackNavigator();

export default function AuthNavigator() {
  const [showSplash, setShowSplash] = useState(true);
  const [hasSeenOnboarding, setHasSeenOnboarding] = useState(null);

  useEffect(() => {
    checkOnboardingStatus();
  }, []);

  const checkOnboardingStatus = async () => {
    try {
      const status = await SecureStore.getItemAsync('onboardingComplete');
      setHasSeenOnboarding(status === 'true');
    } catch (error) {
      console.error('Error checking onboarding status:', error);
      setHasSeenOnboarding(false);
    }
  };

  const handleSplashFinish = () => {
    setShowSplash(false);
  };

  // Show splash screen first
  if (showSplash) {
    return <SplashScreen onFinish={handleSplashFinish} />;
  }

  // Wait for onboarding check
  if (hasSeenOnboarding === null) {
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
