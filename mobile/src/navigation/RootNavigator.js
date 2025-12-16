import React from 'react';
import { View } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import GaneshaLoader from '../components/GaneshaLoader';
import { useAuth } from '../context/AuthContext';

import AuthNavigator from './AuthNavigator';
import MainNavigator from './MainNavigator';
import RemedyScreen from '../screens/RemedyScreen';
import UngalJothidanScreen from '../screens/UngalJothidanScreen';
import ChakraScreen from '../screens/ChakraScreen';

const Stack = createNativeStackNavigator();

export default function RootNavigator() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <View style={{ flex: 1 }}>
        <LinearGradient colors={['#faf7f2', '#f5ede5', '#fff8f0']} style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
          <GaneshaLoader label="Loading" />
        </LinearGradient>
      </View>
    );
  }

  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      {isAuthenticated ? (
        <>
          <Stack.Screen name="Main" component={MainNavigator} />
          <Stack.Screen
            name="Remedy"
            component={RemedyScreen}
            options={{
              presentation: 'modal',
              animation: 'slide_from_bottom',
            }}
          />
          <Stack.Screen
            name="UngalJothidan"
            component={UngalJothidanScreen}
            options={{
              presentation: 'card',
              animation: 'slide_from_right',
            }}
          />
          <Stack.Screen
            name="Chakra"
            component={ChakraScreen}
            options={{
              presentation: 'card',
              animation: 'slide_from_right',
            }}
          />
        </>
      ) : (
        <Stack.Screen name="Auth" component={AuthNavigator} />
      )}
    </Stack.Navigator>
  );
}
