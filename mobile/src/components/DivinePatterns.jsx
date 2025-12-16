import React from 'react';
import { Svg, Path, Circle, G, Defs, Pattern, Rect } from 'react-native-svg';
import { View, StyleSheet } from 'react-native';

// 1. Kolam / Mandala Pattern (Subtle Background)
export const KolamPattern = ({ color = "#e8d5c4", opacity = 0.15, style }) => (
  <View style={[styles.absoluteFill, style, { opacity, zIndex: 0 }]} pointerEvents="none">
    <Svg height="100%" width="100%">
      <Defs>
        <Pattern id="kolam" x="0" y="0" width="60" height="60" patternUnits="userSpaceOnUse">
          <Path
            d="M30 0 C30 15 45 30 60 30 C45 30 30 45 30 60 C30 45 15 30 0 30 C15 30 30 15 30 0"
            fill="none"
            stroke={color}
            strokeWidth="2"
          />
          <Circle cx="30" cy="30" r="3" fill={color} />
        </Pattern>
      </Defs>
      <Rect x="0" y="0" width="100%" height="100%" fill="url(#kolam)" />
    </Svg>
  </View>
);

// 2. Lotus Corner Decoration
export const LotusCorner = ({ color = "#d4a574", size = 60, style }) => (
  <View style={[style, { width: size, height: size, zIndex: 10 }]} pointerEvents="none">
    <Svg width="100%" height="100%" viewBox="0 0 100 100">
      <Path
        d="M0 0 Q50 0 50 50 Q0 50 0 0 M0 0 Q0 50 50 50 Q50 0 0 0"
        fill="none"
        stroke={color}
        strokeWidth="1.5"
        opacity="0.5"
      />
      <Path
        d="M0 0 C20 0 40 10 50 30 C60 10 80 0 100 0 L100 100 L0 100 Z"
        fill={color}
        opacity="0.2"
      />
      <Path
        d="M10 10 Q50 10 50 50 Q10 50 10 10"
        fill="none"
        stroke={color}
        strokeWidth="2.5"
      />
    </Svg>
  </View>
);

// 3. Om Symbol Watermark
export const OmWatermark = ({ color = "#f97316", size = 120, style }) => (
  <View style={[style, { width: size, height: size, opacity: 0.1, zIndex: 0 }]} pointerEvents="none">
    <Svg width="100%" height="100%" viewBox="0 0 500 500">
      <Path
        d="M250 100 C200 100 150 150 150 200 C150 250 200 250 200 250 C150 250 100 300 100 350 C100 450 250 450 250 350 M250 250 C300 250 350 300 350 350 M350 200 Q400 100 450 150 M350 100 Q400 50 450 100"
        fill="none"
        stroke={color}
        strokeWidth="25"
        strokeLinecap="round"
      />
    </Svg>
  </View>
);

// 4. Decorative Divider (Traditional Border)
export const DivineDivider = ({ color = "#d4a574" }) => (
  <View style={{ height: 20, width: '100%', overflow: 'hidden', marginVertical: 12, alignItems: 'center', justifyContent: 'center' }}>
    <Svg height="100%" width="100%">
      <Defs>
        <Pattern id="border" x="0" y="0" width="40" height="20" patternUnits="userSpaceOnUse">
          <Path
            d="M0 10 Q10 0 20 10 Q30 20 40 10"
            fill="none"
            stroke={color}
            strokeWidth="2"
            opacity="0.6"
          />
          <Circle cx="20" cy="10" r="2" fill={color} opacity="0.8" />
        </Pattern>
      </Defs>
      <Rect x="0" y="0" width="100%" height="100%" fill="url(#border)" />
    </Svg>
  </View>
);

const styles = StyleSheet.create({
  absoluteFill: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    zIndex: -1,
  },
});
