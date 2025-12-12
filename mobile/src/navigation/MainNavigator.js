import React from 'react';
import { Platform } from 'react-native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useLanguage } from '../context/LanguageContext';

import DashboardScreen from '../screens/DashboardScreen';
import AstroFeedScreen from '../screens/AstroFeedScreen';
import MatchingScreen from '../screens/MatchingScreen';
import ChatScreen from '../screens/ChatScreen';
import MuhurthamScreen from '../screens/MuhurthamScreen';
import ProfileScreen from '../screens/ProfileScreen';

const Tab = createBottomTabNavigator();

export default function MainNavigator() {
  const insets = useSafeAreaInsets();
  const { t } = useLanguage();
  const bottomPadding = Platform.OS === 'android' ? Math.max(insets.bottom, 10) : insets.bottom;

  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarActiveTintColor: '#f97316',
        tabBarInactiveTintColor: '#9ca3af',
        tabBarStyle: {
          backgroundColor: '#ffffff',
          borderTopColor: '#fed7aa',
          borderTopWidth: 1,
          paddingTop: 5,
          paddingBottom: Platform.OS === 'web' ? 5 : bottomPadding + 5,
          height: Platform.OS === 'web' ? 60 : 60 + bottomPadding,
          ...(Platform.OS !== 'web' && {
            position: 'absolute',
            bottom: 0,
            left: 0,
            right: 0,
          }),
          elevation: 8,
          shadowColor: '#000',
          shadowOffset: { width: 0, height: -2 },
          shadowOpacity: 0.1,
          shadowRadius: 4,
        },
        tabBarLabelStyle: {
          fontSize: 10,
          fontWeight: '600',
        },
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;

          if (route.name === 'Dashboard') {
            iconName = focused ? 'home' : 'home-outline';
          } else if (route.name === 'AstroFeed') {
            iconName = focused ? 'sparkles' : 'sparkles-outline';
          } else if (route.name === 'Matching') {
            iconName = focused ? 'heart' : 'heart-outline';
          } else if (route.name === 'Chat') {
            iconName = focused ? 'chatbubbles' : 'chatbubbles-outline';
          } else if (route.name === 'Muhurtham') {
            iconName = focused ? 'calendar' : 'calendar-outline';
          } else if (route.name === 'Profile') {
            iconName = focused ? 'person' : 'person-outline';
          }

          return <Ionicons name={iconName} size={size} color={color} />;
        },
      })}
    >
      <Tab.Screen
        name="Dashboard"
        component={DashboardScreen}
        options={{ tabBarLabel: t('home') }}
      />
      <Tab.Screen
        name="AstroFeed"
        component={AstroFeedScreen}
        options={{ tabBarLabel: t('astroFeed') }}
      />
      <Tab.Screen
        name="Matching"
        component={MatchingScreen}
        options={{ tabBarLabel: t('matching') }}
      />
      <Tab.Screen
        name="Chat"
        component={ChatScreen}
        options={{ tabBarLabel: t('chat') }}
      />
      <Tab.Screen
        name="Muhurtham"
        component={MuhurthamScreen}
        options={{ tabBarLabel: t('muhurtham') }}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{ tabBarLabel: t('profile') }}
      />
    </Tab.Navigator>
  );
}
