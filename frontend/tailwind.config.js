/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'rag-primary': '#3B82F6',
        'rag-secondary': '#64748B',
        'rag-accent': '#10B981',
        'rag-bg': '#F8FAFC',
        'rag-sidebar': '#F1F5F9',
        'rag-border': '#E2E8F0',
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}