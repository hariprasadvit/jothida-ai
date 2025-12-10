/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Custom colors for astrology theme
        'astro-gold': '#f59e0b',
        'astro-purple': '#8b5cf6',
      },
      fontFamily: {
        tamil: ['Noto Sans Tamil', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
