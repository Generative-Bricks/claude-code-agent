/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Financial advisor themed colors
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          900: '#0c2d6b',
        },
        success: {
          600: '#16a34a',
          700: '#15803d',
        },
        warning: {
          600: '#ea580c',
          700: '#c2410c',
        },
        danger: {
          600: '#dc2626',
          700: '#b91c1c',
        },
      },
      spacing: {
        'safe': 'max(1rem, env(safe-area-inset-left))',
      },
    },
  },
  plugins: [],
}
