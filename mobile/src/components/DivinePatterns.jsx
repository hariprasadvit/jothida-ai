import React from 'react';
import { Svg, Path, Circle, G, Defs, Pattern, Rect } from 'react-native-svg';
import { View, StyleSheet } from 'react-native';

// 1. Kolam / Mandala Pattern (Subtle Background)
export const KolamPattern = ({ color = "#e8d5c4", opacity = 0.15, style }) => (
  <View style={[styles.absoluteFill, style, { opacity }]}>
    <Svg height="100%" width="100%">
      <Defs>
        <Pattern id="kolam" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
          <Path
            d="M20 0 C20 10 30 20 40 20 C30 20 20 30 20 40 C20 30 10 20 0 20 C10 20 20 10 20 0"
            fill="none"
            stroke={color}
            strokeWidth="1.5"
          />
          <Circle cx="20" cy="20" r="2" fill={color} />
        </Pattern>
      </Defs>
      <Rect x="0" y="0" width="100%" height="100%" fill="url(#kolam)" />
    </Svg>
  </View>
);

// 2. Lotus Corner Decoration
export const LotusCorner = ({ color = "#d4a574", size = 60, style }) => (
  <View style={[style, { width: size, height: size }]}>
    <Svg width="100%" height="100%" viewBox="0 0 100 100">
      <Path
        d="M0 0 Q50 0 50 50 Q0 50 0 0 M0 0 Q0 50 50 50 Q50 0 0 0"
        fill="none"
        stroke={color}
        strokeWidth="1"
        opacity="0.3"
      />
      <Path
        d="M0 0 C20 0 40 10 50 30 C60 10 80 0 100 0 L100 100 L0 100 Z"
        fill={color}
        opacity="0.1"
      />
      <Path
        d="M10 10 Q50 10 50 50 Q10 50 10 10"
        fill="none"
        stroke={color}
        strokeWidth="2"
      />
    </Svg>
  </View>
);

// 3. Om Symbol Watermark
export const OmWatermark = ({ color = "#f97316", size = 120, style }) => (
  <View style={[style, { width: size, height: size, opacity: 0.05 }]}>
    <Svg width="100%" height="100%" viewBox="0 0 500 500">
      <Path
        d="M250 100 C200 100 150 150 150 200 C150 250 200 250 200 250 C150 250 100 300 100 350 C100 450 250 450 250 350 M250 250 C300 250 350 300 350 350 M350 200 Q400 100 450 150 M350 100 Q400 50 450 100"
        fill="none"
        stroke={color}
        strokeWidth="20"
        strokeLinecap="round"
      />
    </Svg>
  </View>
);

// 4. Decorative Divider (Traditional Border)
export const DivineDivider = ({ color = "#e8d5c4" }) => (
  <View style={{ height: 12, width: '100%', overflow: 'hidden', marginVertical: 8 }}>
    <Svg height="100%" width="100%">
      <Defs>
        <Pattern id="border" x="0" y="0" width="20" height="12" patternUnits="userSpaceOnUse">
          <Path
            d="M0 6 Q5 0 10 6 Q15 12 20 6"
            fill="none"
            stroke={color}
            strokeWidth="1.5"
          />
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
