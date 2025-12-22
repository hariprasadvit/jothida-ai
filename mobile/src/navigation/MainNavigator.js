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
  const bottomPadding = Math.max(insets.bottom, 10);

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
        tabBarInactiveTintColor: '#9ca3af',
        tabBarStyle: {
          backgroundColor: '#ffffff',
          borderTopWidth: 1,
          borderTopColor: '#f3f4f6',
          height: 60 + bottomPadding,
          paddingTop: 8,
          paddingBottom: bottomPadding,
        },
        tabBarIcon: ({ focused, color }) => {
          const config = TAB_CONFIG[route.name];
          const iconName = focused ? config.icon : config.iconOutline;
          return <Ionicons name={iconName} size={26} color={color} />;
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
