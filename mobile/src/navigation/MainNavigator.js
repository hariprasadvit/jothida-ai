import React from 'react';
import { Platform, View, StyleSheet } from 'react-native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { CommonActions } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import DashboardScreen from '../screens/DashboardScreen';
import AstroFeedScreen from '../screens/AstroFeedScreen';
import MatchingScreen from '../screens/MatchingScreen';
import UngalJothidanScreen from '../screens/UngalJothidanScreen';
import MuhurthamScreen from '../screens/MuhurthamScreen';
import ProfileScreen from '../screens/ProfileScreen';

const Tab = createBottomTabNavigator();

const TAB_CONFIG = {
  Dashboard: { icon: 'home', iconOutline: 'home-outline' },
  AstroFeed: { icon: 'sparkles', iconOutline: 'sparkles-outline' },
  Matching: { icon: 'heart', iconOutline: 'heart-outline' },
  UngalJothidan: { icon: 'sunny', iconOutline: 'sunny-outline' },
  Muhurtham: { icon: 'calendar', iconOutline: 'calendar-outline' },
  Profile: { icon: 'person', iconOutline: 'person-outline' },
};

export default function MainNavigator() {
  const insets = useSafeAreaInsets();
  const bottomPadding = Platform.OS === 'android' ? Math.max(insets.bottom, 12) : insets.bottom;

  const resetTabListener = ({ navigation, route }) => ({
    tabPress: () => {
      const state = navigation.getState();
      if (state.routes[state.index].name === route.name) {
        navigation.dispatch(
          CommonActions.reset({
            index: 0,
            routes: [{ name: route.name }],
          })
        );
      }
    },
  });

  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarShowLabel: false,
        tabBarHideOnKeyboard: true,
        tabBarActiveTintColor: '#ea580c',
        tabBarInactiveTintColor: '#b8a99a',
        tabBarStyle: {
          backgroundColor: '#fffaf5',
          borderTopWidth: 0,
          paddingTop: 12,
          paddingBottom: Platform.OS === 'web' ? 12 : bottomPadding + 8,
          height: Platform.OS === 'web' ? 70 : 70 + bottomPadding,
          elevation: 20,
          shadowColor: '#000',
          shadowOffset: { width: 0, height: -4 },
          shadowOpacity: 0.08,
          shadowRadius: 12,
          ...(Platform.OS !== 'web' && {
            position: 'absolute',
            bottom: 0,
            left: 0,
            right: 0,
          }),
        },
        tabBarIcon: ({ focused, color }) => {
          const config = TAB_CONFIG[route.name];
          const iconName = focused ? config.icon : config.iconOutline;

          return (
            <View style={[styles.iconContainer, focused && styles.iconContainerActive]}>
              <Ionicons name={iconName} size={24} color={color} />
              {focused && <View style={styles.activeIndicator} />}
            </View>
          );
        },
      })}
    >
      <Tab.Screen
        name="Dashboard"
        component={DashboardScreen}
        listeners={resetTabListener}
      />
      <Tab.Screen
        name="AstroFeed"
        component={AstroFeedScreen}
        listeners={resetTabListener}
      />
      <Tab.Screen
        name="Matching"
        component={MatchingScreen}
        listeners={resetTabListener}
      />
      <Tab.Screen
        name="UngalJothidan"
        component={UngalJothidanScreen}
        listeners={resetTabListener}
      />
      <Tab.Screen
        name="Muhurtham"
        component={MuhurthamScreen}
        listeners={resetTabListener}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        listeners={resetTabListener}
      />
    </Tab.Navigator>
  );
}

const styles = StyleSheet.create({
  iconContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  iconContainerActive: {
    backgroundColor: '#fff7ed',
  },
  activeIndicator: {
    position: 'absolute',
    bottom: 2,
    width: 4,
    height: 4,
    borderRadius: 2,
    backgroundColor: '#ea580c',
  },
});
