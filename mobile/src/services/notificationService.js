/**
 * Transit Notification Service
 * Handles push notifications for planetary transit alerts
 */

import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import { Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Configure notification behavior
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

const NOTIFICATION_STORAGE_KEY = '@jothida_notifications';

class NotificationService {
  constructor() {
    this.expoPushToken = null;
    this.notificationListener = null;
    this.responseListener = null;
  }

  /**
   * Initialize notifications and request permissions
   */
  async initialize() {
    try {
      // Check if physical device (notifications don't work on simulator)
      if (!Device.isDevice) {
        console.log('Push notifications require a physical device');
        return false;
      }

      // Request permissions
      const { status: existingStatus } = await Notifications.getPermissionsAsync();
      let finalStatus = existingStatus;

      if (existingStatus !== 'granted') {
        const { status } = await Notifications.requestPermissionsAsync();
        finalStatus = status;
      }

      if (finalStatus !== 'granted') {
        console.log('Notification permission not granted');
        return false;
      }

      // Get push token
      const token = await Notifications.getExpoPushTokenAsync();
      this.expoPushToken = token.data;

      // Android-specific channel
      if (Platform.OS === 'android') {
        await Notifications.setNotificationChannelAsync('transits', {
          name: 'கிரக கோச்சாரம்',
          importance: Notifications.AndroidImportance.HIGH,
          vibrationPattern: [0, 250, 250, 250],
          lightColor: '#38bdf8',
        });
      }

      // Set up listeners
      this.setupListeners();

      return true;
    } catch (error) {
      console.error('Error initializing notifications:', error);
      return false;
    }
  }

  /**
   * Set up notification listeners
   */
  setupListeners() {
    // Handle notification received while app is foregrounded
    this.notificationListener = Notifications.addNotificationReceivedListener(notification => {
      console.log('Notification received:', notification);
    });

    // Handle user interaction with notification
    this.responseListener = Notifications.addNotificationResponseReceivedListener(response => {
      const data = response.notification.request.content.data;
      console.log('Notification response:', data);
      // Handle navigation based on notification type
      if (data.type === 'moon_transit') {
        // Navigate to transits section
      }
    });
  }

  /**
   * Clean up listeners
   */
  cleanup() {
    if (this.notificationListener) {
      Notifications.removeNotificationSubscription(this.notificationListener);
    }
    if (this.responseListener) {
      Notifications.removeNotificationSubscription(this.responseListener);
    }
  }

  /**
   * Schedule a moon transit notification
   */
  async scheduleMoonTransitNotification(nextSign, hoursRemaining, energy) {
    try {
      // Don't schedule if more than 24 hours away
      if (hoursRemaining > 24) return;

      // Cancel existing moon transit notifications
      await this.cancelNotificationsByType('moon_transit');

      // Schedule notification 30 minutes before transit
      const triggerSeconds = Math.max((hoursRemaining - 0.5) * 3600, 60);

      const notificationId = await Notifications.scheduleNotificationAsync({
        content: {
          title: `🌙 சந்திரன் ${nextSign.name} நுழைவு`,
          body: `30 நிமிடத்தில் ${energy.mood} காலம் தொடங்கும்! ${energy.icon}`,
          data: { type: 'moon_transit', sign: nextSign },
          sound: true,
          badge: 1,
        },
        trigger: {
          seconds: triggerSeconds,
          channelId: 'transits',
        },
      });

      // Store notification info
      await this.storeNotification({
        id: notificationId,
        type: 'moon_transit',
        scheduledAt: new Date().toISOString(),
        triggerIn: triggerSeconds,
      });

      return notificationId;
    } catch (error) {
      console.error('Error scheduling moon transit notification:', error);
      return null;
    }
  }

  /**
   * Schedule a retrograde notification
   */
  async scheduleRetrogradeNotification(planet, daysUntil, isStart = true) {
    try {
      // Only notify for retrogrades starting within 3 days
      if (daysUntil > 3) return;

      const notificationId = await Notifications.scheduleNotificationAsync({
        content: {
          title: isStart
            ? `⚠️ ${planet.tamil} வக்ரம் தொடங்குகிறது`
            : `✅ ${planet.tamil} வக்ரம் முடிகிறது`,
          body: isStart
            ? `${daysUntil} நாட்களில் ${planet.tamil} வக்ர நிலைக்கு செல்கிறார். கவனமாக இருங்கள்.`
            : `${planet.tamil} நேர் கதியில் செல்கிறார். நல்ல நேரம்!`,
          data: { type: 'retrograde', planet: planet.name },
          sound: true,
        },
        trigger: {
          seconds: daysUntil * 24 * 3600 - 3600, // 1 hour before
          channelId: 'transits',
        },
      });

      return notificationId;
    } catch (error) {
      console.error('Error scheduling retrograde notification:', error);
      return null;
    }
  }

  /**
   * Send immediate notification
   */
  async sendImmediateNotification(title, body, data = {}) {
    try {
      await Notifications.scheduleNotificationAsync({
        content: {
          title,
          body,
          data,
          sound: true,
        },
        trigger: null, // Immediate
      });
    } catch (error) {
      console.error('Error sending immediate notification:', error);
    }
  }

  /**
   * Cancel notifications by type
   */
  async cancelNotificationsByType(type) {
    try {
      const stored = await this.getStoredNotifications();
      const toCancel = stored.filter(n => n.type === type);

      for (const notification of toCancel) {
        await Notifications.cancelScheduledNotificationAsync(notification.id);
      }

      // Update storage
      const remaining = stored.filter(n => n.type !== type);
      await AsyncStorage.setItem(NOTIFICATION_STORAGE_KEY, JSON.stringify(remaining));
    } catch (error) {
      console.error('Error canceling notifications:', error);
    }
  }

  /**
   * Cancel all scheduled notifications
   */
  async cancelAllNotifications() {
    try {
      await Notifications.cancelAllScheduledNotificationsAsync();
      await AsyncStorage.removeItem(NOTIFICATION_STORAGE_KEY);
    } catch (error) {
      console.error('Error canceling all notifications:', error);
    }
  }

  /**
   * Store notification info
   */
  async storeNotification(notification) {
    try {
      const stored = await this.getStoredNotifications();
      stored.push(notification);
      await AsyncStorage.setItem(NOTIFICATION_STORAGE_KEY, JSON.stringify(stored));
    } catch (error) {
      console.error('Error storing notification:', error);
    }
  }

  /**
   * Get stored notifications
   */
  async getStoredNotifications() {
    try {
      const stored = await AsyncStorage.getItem(NOTIFICATION_STORAGE_KEY);
      return stored ? JSON.parse(stored) : [];
    } catch (error) {
      console.error('Error getting stored notifications:', error);
      return [];
    }
  }

  /**
   * Check and update transit notifications based on current data
   */
  async updateTransitNotifications(transitsMap) {
    if (!transitsMap) return;

    // Moon transit notification
    if (transitsMap.moon_transit) {
      const { time_to_transit, next_sign_name, energy } = transitsMap.moon_transit;
      if (time_to_transit && time_to_transit.total_hours <= 6) {
        await this.scheduleMoonTransitNotification(
          { name: next_sign_name },
          time_to_transit.total_hours,
          energy || { mood: 'மாற்றம்', icon: '🌙' }
        );
      }
    }

    // Retrograde notifications
    if (transitsMap.retrogrades) {
      for (const retro of transitsMap.retrogrades) {
        if (retro.status === 'upcoming' && retro.days_until <= 3) {
          await this.scheduleRetrogradeNotification(
            { name: retro.planet, tamil: retro.tamil },
            retro.days_until,
            true
          );
        }
      }
    }
  }
}

// Export singleton instance
export default new NotificationService();
