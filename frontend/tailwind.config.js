/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        netflix: {
          red: '#e50914',
          black: '#221f1f',
          gray: '#f5f5f1',
        }
      }
    },
  },
  plugins: [],
} 