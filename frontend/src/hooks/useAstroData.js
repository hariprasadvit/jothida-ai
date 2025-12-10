/**
 * Custom hook for astrology data
 * Fetches from API when available, computes locally when offline
 */

import { useState, useEffect, useCallback } from 'react';
import { useQuery } from '@tanstack/react-query';
import { panchangamAPI, jathagamAPI, getCityCoordinates } from '../services/api';

/**
 * Hook for today's panchangam and dashboard data
 */
export function useDashboardData(userProfile) {
  const coords = userProfile?.birthPlace
    ? getCityCoordinates(userProfile.birthPlace)
    : { lat: 13.0827, lon: 80.2707 };

  // Fetch panchangam
  const panchangamQuery = useQuery({
    queryKey: ['panchangam', 'today', coords.lat, coords.lon],
    queryFn: () => panchangamAPI.getToday(coords.lat, coords.lon),
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 1,
  });

  // Fetch time energy data
  const timeEnergyQuery = useQuery({
    queryKey: ['timeEnergy', coords.lat, coords.lon],
    queryFn: () => panchangamAPI.getTimeEnergy(null, coords.lat, coords.lon),
    staleTime: 5 * 60 * 1000,
    retry: 1,
  });

  // Fetch jathagam if user profile exists
  const jathagamQuery = useQuery({
    queryKey: ['jathagam', userProfile?.name, userProfile?.birthDate],
    queryFn: () => jathagamAPI.generate(userProfile),
    enabled: !!userProfile?.name && !!userProfile?.birthDate && !!userProfile?.birthTime,
    staleTime: 24 * 60 * 60 * 1000, // 24 hours - birth chart doesn't change
    retry: 1,
  });

  // Compute overall score from various factors
  const computeOverallScore = useCallback(() => {
    let score = 50; // Base score

    if (panchangamQuery.data?.overall_score) {
      score = panchangamQuery.data.overall_score;
    }

    // Adjust based on jathagam if available
    if (jathagamQuery.data?.overall_strength) {
      score = (score + jathagamQuery.data.overall_strength) / 2;
    }

    return Math.round(score);
  }, [panchangamQuery.data, jathagamQuery.data]);

  // Format data for dashboard
  const dashboardData = {
    // Panchangam data
    panchangam: panchangamQuery.data || getDefaultPanchangam(),

    // Time energy (hourly data)
    timeEnergy: timeEnergyQuery.data || getDefaultTimeEnergy(),

    // Planet data from jathagam
    planets: jathagamQuery.data?.planets || [],

    // Life areas
    lifeAreas: computeLifeAreas(jathagamQuery.data),

    // Overall score
    overallScore: computeOverallScore(),

    // User's rasi and nakshatra
    userRasi: jathagamQuery.data?.moon_sign?.rasi_tamil || userProfile?.rasi || null,
    userNakshatra: jathagamQuery.data?.moon_sign?.nakshatra || userProfile?.nakshatra || null,

    // Current dasha
    currentDasha: jathagamQuery.data?.dasha?.current || null,

    // Yogas
    yogas: jathagamQuery.data?.yogas || [],

    // Loading states
    isLoading: panchangamQuery.isLoading || timeEnergyQuery.isLoading,
    isJathagamLoading: jathagamQuery.isLoading,

    // Error states
    error: panchangamQuery.error || timeEnergyQuery.error,
    isOffline: panchangamQuery.isError && timeEnergyQuery.isError,
  };

  return dashboardData;
}

/**
 * Compute life areas from jathagam data
 */
function computeLifeAreas(jathagam) {
  if (!jathagam?.planets) {
    return getDefaultLifeAreas();
  }

  const planets = jathagam.planets;
  const getPlanetStrength = (name) => {
    const planet = planets.find(p => p.planet === name);
    return planet?.strength || 50;
  };

  return [
    {
      name: 'காதல்',
      icon: 'Heart',
      score: Math.round((getPlanetStrength('Venus') + getPlanetStrength('Moon')) / 2),
      color: '#dc2626'
    },
    {
      name: 'தொழில்',
      icon: 'Briefcase',
      score: Math.round((getPlanetStrength('Saturn') + getPlanetStrength('Sun')) / 2),
      color: '#ea580c'
    },
    {
      name: 'கல்வி',
      icon: 'GraduationCap',
      score: Math.round((getPlanetStrength('Jupiter') + getPlanetStrength('Mercury')) / 2),
      color: '#ca8a04'
    },
    {
      name: 'குடும்பம்',
      icon: 'Home',
      score: Math.round(getPlanetStrength('Moon')),
      color: '#16a34a'
    },
  ];
}

/**
 * Default panchangam when API is unavailable
 */
function getDefaultPanchangam() {
  const now = new Date();
  const hour = now.getHours();

  // Determine current time period
  let period = { label: 'சாதாரண நேரம்', status: 'neutral' };
  if (hour >= 15 && hour < 17) {
    period = { label: 'ராகு காலம்', status: 'rahu' };
  } else if (hour >= 9 && hour < 11) {
    period = { label: 'நல்ல நேரம்', status: 'good' };
  }

  return {
    date: now.toISOString().split('T')[0],
    tamil_month: getTamilMonth(now),
    tamil_date: now.getDate().toString(),
    vaaram: getTamilDay(now.getDay()),
    tithi: { name: 'சப்தமி', paksha: 'Shukla' },
    nakshatra: { name: 'Uttara Phalguni', tamil: 'உத்திரம்', pada: 2 },
    yoga: { name: 'Siddha' },
    rahu_kalam: computeRahuKalam(now),
    nalla_neram: computeNallaNeram(now),
    overall_score: 65,
    period
  };
}

/**
 * Default time energy data
 */
function getDefaultTimeEnergy() {
  const data = [];
  const now = new Date();
  const currentHour = now.getHours();

  for (let hour = 6; hour <= 21; hour++) {
    const isRahu = hour >= 15 && hour <= 16;
    const isNalla = (hour >= 9 && hour <= 10) || (hour >= 14 && hour <= 15);

    let energy;
    if (isRahu) {
      energy = 25;
    } else if (isNalla) {
      energy = 90;
    } else {
      energy = 50 + Math.sin(hour / 3) * 20;
    }

    data.push({
      time: `${hour}:00`,
      hour,
      energy_score: Math.round(energy),
      is_rahu_kalam: isRahu,
      is_nalla_neram: isNalla,
      is_current: hour === currentHour
    });
  }

  return data;
}

/**
 * Default life areas
 */
function getDefaultLifeAreas() {
  return [
    { name: 'காதல்', icon: 'Heart', score: 65, color: '#dc2626' },
    { name: 'தொழில்', icon: 'Briefcase', score: 70, color: '#ea580c' },
    { name: 'கல்வி', icon: 'GraduationCap', score: 75, color: '#ca8a04' },
    { name: 'குடும்பம்', icon: 'Home', score: 60, color: '#16a34a' },
  ];
}

/**
 * Get Tamil month name
 */
function getTamilMonth(date) {
  const months = [
    'தை', 'மாசி', 'பங்குனி', 'சித்திரை', 'வைகாசி', 'ஆனி',
    'ஆடி', 'ஆவணி', 'புரட்டாசி', 'ஐப்பசி', 'கார்த்திகை', 'மார்கழி'
  ];
  // Approximate - Tamil months start mid-month
  const month = date.getMonth();
  const day = date.getDate();
  const adjustedMonth = day >= 15 ? (month + 1) % 12 : month;
  return months[adjustedMonth];
}

/**
 * Get Tamil day name
 */
function getTamilDay(dayIndex) {
  const days = ['ஞாயிறு', 'திங்கள்', 'செவ்வாய்', 'புதன்', 'வியாழன்', 'வெள்ளி', 'சனி'];
  return days[dayIndex];
}

/**
 * Compute Rahu Kalam based on day of week
 */
function computeRahuKalam(date) {
  // Rahu Kalam periods (1/8th of day starting from sunrise ~6am)
  const rahuPeriods = [8, 2, 7, 5, 6, 4, 3]; // Sun, Mon, Tue, Wed, Thu, Fri, Sat
  const period = rahuPeriods[date.getDay()];

  const startHour = 6 + (period - 1) * 1.5;
  const endHour = startHour + 1.5;

  return {
    start: `${Math.floor(startHour)}:${(startHour % 1) * 60 === 0 ? '00' : '30'}`,
    end: `${Math.floor(endHour)}:${(endHour % 1) * 60 === 0 ? '00' : '30'}`
  };
}

/**
 * Compute Nalla Neram (simplified)
 */
function computeNallaNeram(date) {
  const goodPeriods = {
    0: [[7, 8.5], [13, 14.5]],    // Sunday
    1: [[8, 9.5], [14, 15.5]],    // Monday
    2: [[9, 10.5], [15, 16.5]],   // Tuesday
    3: [[10, 11.5], [16, 17.5]],  // Wednesday
    4: [[7, 8.5], [13, 14.5]],    // Thursday
    5: [[8, 9.5], [14, 15.5]],    // Friday
    6: [[9, 10.5], [15, 16.5]],   // Saturday
  };

  const periods = goodPeriods[date.getDay()] || [[9, 10.5]];

  return periods.map(([start, end]) => ({
    start: `${Math.floor(start)}:${(start % 1) * 60 === 0 ? '00' : '30'}`,
    end: `${Math.floor(end)}:${(end % 1) * 60 === 0 ? '00' : '30'}`
  }));
}

export default useDashboardData;
