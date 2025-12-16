// Unified Color Theme for Jothida AI Dashboard
// Use these colors across all components for consistency

export const THEME_COLORS = {
  // Primary palette - Warm earthy tones
  primary: {
    main: '#f97316',        // Orange
    light: '#fb923c',
    lighter: '#fdba74',
    lightest: '#fed7aa',
    dark: '#ea580c',
    darker: '#c2410c',
  },
  
  // Secondary palette - Deep browns
  secondary: {
    main: '#6b5644',        // Brown
    light: '#8b6f47',
    lighter: '#b8997a',
    lightest: '#d4a574',
    dark: '#5a4838',
  },
  
  // Background colors
  background: {
    primary: '#ffffff',
    secondary: '#fef6ed',
    tertiary: '#fff8f0',
    accent: '#f4e4d7',
    gradient: ['#faf7f2', '#f5edd5', '#fff8f0'],
  },
  
  // Border colors
  border: {
    light: '#fed7aa',
    medium: '#e8d5c4',
    dark: '#d4a574',
  },
  
  // Text colors
  text: {
    primary: '#1f2937',     // Dark gray
    secondary: '#6b5644',   // Brown
    tertiary: '#8b6f47',    // Light brown
    muted: '#6b7280',       // Gray
    light: '#9ca3af',       // Light gray
  },
  
  // Status colors
  status: {
    success: {
      main: '#16a34a',
      light: '#22c55e',
      bg: '#dcfce7',
      border: '#bbf7d0',
    },
    warning: {
      main: '#ca8a04',
      light: '#eab308',
      bg: '#fef3c7',
      border: '#fde68a',
    },
    error: {
      main: '#dc2626',
      light: '#ef4444',
      bg: '#fee2e2',
      border: '#fecaca',
    },
    info: {
      main: '#2563eb',
      light: '#3b82f6',
      bg: '#dbeafe',
      border: '#bfdbfe',
    },
  },
  
  // Planet-specific colors (for Planet Positions)
  planets: {
    Sun: {
      gradient: ['#fff7ed', '#ffedd5'],
      border: '#fb923c',
      text: '#9a3412',
      icon: '#ea580c',
    },
    Moon: {
      gradient: ['#f5f3ff', '#ede9fe'],
      border: '#c4b5fd',
      text: '#5b21b6',
      icon: '#7c3aed',
    },
    Mars: {
      gradient: ['#fee2e2', '#fecaca'],
      border: '#fca5a5',
      text: '#991b1b',
      icon: '#dc2626',
    },
    Mercury: {
      gradient: ['#dcfce7', '#bbf7d0'],
      border: '#86efac',
      text: '#166534',
      icon: '#16a34a',
    },
    Jupiter: {
      gradient: ['#fef9c3', '#fef08a'],
      border: '#fde047',
      text: '#854d0e',
      icon: '#ca8a04',
    },
    Venus: {
      gradient: ['#fce7f3', '#fbcfe8'],
      border: '#f9a8d4',
      text: '#831843',
      icon: '#be185d',
    },
    Saturn: {
      gradient: ['#e0e7ff', '#c7d2fe'],
      border: '#a5b4fc',
      text: '#3730a3',
      icon: '#4f46e5',
    },
    Rahu: {
      gradient: ['#fef3c7', '#fde68a'],
      border: '#fcd34d',
      text: '#78350f',
      icon: '#b45309',
    },
    Ketu: {
      gradient: ['#dbeafe', '#bfdbfe'],
      border: '#93c5fd',
      text: '#1e40af',
      icon: '#2563eb',
    },
  },
  
  // Chakra colors
  chakra: {
    crown: '#9333ea',
    thirdEye: '#4f46e5',
    throat: '#0ea5e9',
    heart: '#22c55e',
    solarPlexus: '#eab308',
    sacral: '#f97316',
    root: '#ef4444',
  },
  
  // Dasha colors
  dasha: {
    gradient: ['#faf5ff', '#f3e8ff'],
    border: '#e9d5ff',
    text: '#5b21b6',
    icon: '#7c3aed',
  },
  
  // Aura/Energy colors based on score
  aura: {
    excellent: {
      main: '#16a34a',
      gradient: ['#dcfce7', '#bbf7d0'],
      border: '#86efac',
    },
    good: {
      main: '#ca8a04',
      gradient: ['#fef9c3', '#fef08a'],
      border: '#fde047',
    },
    moderate: {
      main: '#f97316',
      gradient: ['#fff7ed', '#ffedd5'],
      border: '#fdba74',
    },
    low: {
      main: '#dc2626',
      gradient: ['#fee2e2', '#fecaca'],
      border: '#fca5a5',
    },
  },
};

// Shadow configurations
export const SHADOWS = {
  sm: {
    shadowColor: '#d4a574',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.08,
    shadowRadius: 2,
    elevation: 1,
  },
  md: {
    shadowColor: '#d4a574',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  lg: {
    shadowColor: '#d4a574',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.12,
    shadowRadius: 8,
    elevation: 3,
  },
  xl: {
    shadowColor: '#d4a574',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.12,
    shadowRadius: 12,
    elevation: 4,
  },
};

// Border radius
export const RADIUS = {
  xs: 8,
  sm: 12,
  md: 16,
  lg: 20,
  xl: 24,
  full: 9999,
};

// Spacing scale
export const SPACING = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  xxl: 24,
};

// Typography
export const TYPOGRAPHY = {
  size: {
    xs: 10,
    sm: 11,
    md: 12,
    base: 13,
    lg: 14,
    xl: 16,
    xxl: 18,
    xxxl: 20,
  },
  weight: {
    regular: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
    extrabold: '800',
    black: '900',
  },
  lineHeight: {
    tight: 1.2,
    normal: 1.5,
    relaxed: 1.75,
  },
};

// Helper function to get aura color based on score
export const getAuraColorByScore = (score) => {
  if (score >= 75) return THEME_COLORS.aura.excellent;
  if (score >= 60) return THEME_COLORS.aura.good;
  if (score >= 45) return THEME_COLORS.aura.moderate;
  return THEME_COLORS.aura.low;
};

// Helper function to get status color based on score
export const getStatusByScore = (score) => {
  if (score >= 75) return THEME_COLORS.status.success;
  if (score >= 60) return THEME_COLORS.status.info;
  if (score >= 45) return THEME_COLORS.status.warning;
  return THEME_COLORS.status.error;
};

// Export default theme object
export default {
  colors: THEME_COLORS,
  shadows: SHADOWS,
  radius: RADIUS,
  spacing: SPACING,
  typography: TYPOGRAPHY,
  helpers: {
    getAuraColorByScore,
    getStatusByScore,
  },
};
