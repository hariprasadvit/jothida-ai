import React from 'react';
import { Platform, Text, View } from 'react-native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { CommonActions } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useLanguage } from '../context/LanguageContext';

import DashboardScreen from '../screens/DashboardScreen';
import AstroFeedScreen from '../screens/AstroFeedScreen';
import MatchingScreen from '../screens/MatchingScreen';
import UngalJothidanScreen from '../screens/UngalJothidanScreen';
import MuhurthamScreen from '../screens/MuhurthamScreen';
import ProfileScreen from '../screens/ProfileScreen';

const Tab = createBottomTabNavigator();

export default function MainNavigator() {
  const insets = useSafeAreaInsets();
  const { t, language } = useLanguage();
  const bottomPadding = Platform.OS === 'android' ? Math.max(insets.bottom, 10) : insets.bottom;

  // Very short labels that fit in bottom nav for all languages
  const getTabLabel = (routeName) => {
    const labels = {
      Dashboard: { en: 'Home', ta: 'முகப்பு', kn: 'ಮನೆ' },
      AstroFeed: { en: 'Feed', ta: 'கதை', kn: 'ಕಥೆ' },
      Matching: { en: 'Match', ta: 'ஜோடி', kn: 'ಜೋಡಿ' },
      UngalJothidan: { en: 'Daily', ta: 'தினம்', kn: 'ದಿನ' },
      Muhurtham: { en: 'Time', ta: 'நேரம்', kn: 'ಸಮಯ' },
      Profile: { en: 'Me', ta: 'நான்', kn: 'ನಾನು' },
    };
    return labels[routeName]?.[language] || labels[routeName]?.en || routeName;
  };

  return (
    <Tab.Navigator
      screenOptions={({ route, navigation }) => ({
        headerShown: false,
        tabBarActiveTintColor: '#f97316',
        tabBarInactiveTintColor: '#8b6f47',
        tabBarHideOnKeyboard: true,
        tabBarStyle: {
          backgroundColor: '#fff8f0',
          borderTopColor: '#e8d5c4',
          borderTopWidth: 1,
          paddingTop: 6,
          paddingBottom: Platform.OS === 'web' ? 8 : bottomPadding + 6,
          height: Platform.OS === 'web' ? 60 : 60 + bottomPadding,
          borderTopLeftRadius: 20,
          borderTopRightRadius: 20,
          ...(Platform.OS !== 'web' && {
            position: 'absolute',
            bottom: 0,
            left: 0,
            right: 0,
          }),
          shadowColor: '#d4a574',
          shadowOffset: { width: 0, height: -4 },
          shadowOpacity: 0.1,
          shadowRadius: 8,
          elevation: 8,
        },
        tabBarItemStyle: {
          paddingVertical: 2,
        },
        tabBarShowLabel: false,
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;

          if (route.name === 'Dashboard') {
            iconName = focused ? 'home' : 'home-outline';
          } else if (route.name === 'AstroFeed') {
            iconName = focused ? 'sparkles' : 'sparkles-outline';
          } else if (route.name === 'Matching') {
            iconName = focused ? 'heart' : 'heart-outline';
          } else if (route.name === 'UngalJothidan') {
            iconName = focused ? 'sunny' : 'sunny-outline';
          } else if (route.name === 'Muhurtham') {
            iconName = focused ? 'calendar' : 'calendar-outline';
          } else if (route.name === 'Profile') {
            iconName = focused ? 'person' : 'person-outline';
          }

          const label = getTabLabel(route.name);

          return (
            <View style={{ alignItems: 'center', justifyContent: 'center' }}>
              <View
                style={{
                  paddingHorizontal: 10,
                  paddingVertical: 4,
                  borderRadius: 12,
                  backgroundColor: focused ? '#fff7ed' : 'transparent',
                  borderWidth: focused ? 1 : 0,
                  borderColor: focused ? '#fed7aa' : 'transparent',
                }}
              >
                <Ionicons name={iconName} size={20} color={color} />
              </View>
              <Text
                style={{
                  marginTop: 2,
                  fontSize: 9,
                  fontWeight: focused ? '700' : '500',
                  color,
                  textAlign: 'center',
                }}
              >
                {label}
              </Text>
            </View>
          );
        },
      })}
    >
      <Tab.Screen
        name="Dashboard"
        component={DashboardScreen}
        options={{ tabBarLabel: t('home') }}
        listeners={({ navigation, route }) => ({
          tabPress: (e) => {
            const state = navigation.getState();
            // If already on this tab, reset it
            if (state.routes[state.index].name === route.name) {
              navigation.dispatch(
                CommonActions.reset({
                  index: 0,
                  routes: [{ name: route.name }],
                })
              );
            }
          },
        })}
      />
      <Tab.Screen
        name="AstroFeed"
        component={AstroFeedScreen}
        options={{ tabBarLabel: t('astroFeed') }}
        listeners={({ navigation, route }) => ({
          tabPress: (e) => {
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
        })}
      />
      <Tab.Screen
        name="Matching"
        component={MatchingScreen}
        options={{ tabBarLabel: t('matching') }}
        listeners={({ navigation, route }) => ({
          tabPress: (e) => {
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
        })}
      />
      <Tab.Screen
        name="UngalJothidan"
        component={UngalJothidanScreen}
        options={{ tabBarLabel: t('ungalJothidan') }}
        listeners={({ navigation, route }) => ({
          tabPress: (e) => {
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
        })}
      />
      <Tab.Screen
        name="Muhurtham"
        component={MuhurthamScreen}
        options={{ tabBarLabel: t('muhurtham') }}
        listeners={({ navigation, route }) => ({
          tabPress: (e) => {
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
        })}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{ tabBarLabel: t('profile') }}
        listeners={({ navigation, route }) => ({
          tabPress: (e) => {
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
        })}
      />
    </Tab.Navigator>
  );
}
